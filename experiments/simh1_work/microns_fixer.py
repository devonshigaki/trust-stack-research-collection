#!/usr/bin/env python3
"""Fixer for deterministically failing batches (IncompleteRead at fixed
offsets): process batches 39 and 60 with split-on-any-error recursion."""
import os, sys, json, time, warnings
sys.path.append('/home/kimi/.local/lib/python3.12/site-packages')
import pandas as pd
from caveclient.materializationengine import MaterializationClient
from caveclient.auth import AuthClient

W = '/mnt/agents/output/simh1_work'
sample = json.load(open(f'{W}/microns_sample_seed45.json'))['sample']
typed = set(int(x) for x in json.load(open(f'{W}/microns_celltypes_artifact_superseded.json'))['cls'].keys())
B = 100
batches = [sample[i:i+B] for i in range(0, len(sample), B)]

mc = MaterializationClient(server_address='https://minnie.microns-daf.com',
    datastack_name='minnie65_public',
    auth_client=AuthClient(token='31b36cc83e079c03fc7c44f939231425'),
    version=1822)

def query_posts(posts, depth=0):
    if depth > 8:
        raise RuntimeError('split depth exceeded')
    try:
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter('always')
            df = mc.query_table('synapses_pni_2',
                                filter_in_dict={'post_pt_root_id': posts},
                                select_columns=['pre_pt_root_id', 'post_pt_root_id'])
        if any('Limited query' in str(w.message) for w in wl):
            raise RuntimeError('truncated')
        return df
    except Exception as e:
        if len(posts) == 1:
            raise
        h = len(posts)//2
        print(f'split at depth {depth} ({len(posts)} posts): {str(e)[:80]}', flush=True)
        return pd.concat([query_posts(posts[:h], depth+1),
                          query_posts(posts[h:], depth+1)], ignore_index=True)

for bi in [39, 60]:
    out = f'{W}/mparts/batch_{bi:04d}.csv'
    if os.path.exists(out):
        continue
    posts = [int(x) for x in batches[bi]]
    t0 = time.time()
    df = query_posts(posts)
    df = df[df['pre_pt_root_id'].isin(typed)]
    g = df.groupby(['pre_pt_root_id', 'post_pt_root_id']).size().reset_index(name='n')
    tmp = out + '.tmpfix'
    g.to_csv(tmp, index=False)
    os.replace(tmp, out)
    print(f'batch {bi}: {len(g)} pairs, {int(g["n"].sum())} synapses, '
          f'{time.time()-t0:.0f}s', flush=True)
print('fixer done')
