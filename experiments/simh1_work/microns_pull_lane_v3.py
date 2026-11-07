#!/usr/bin/env python3
"""MICrONS sampled-posts synapse pull, lane v3.

Cooperative, idempotent, cross-machine:
  - 120 batches x 100 posts (seed-45 sample, materialization 1822)
  - claim = O_EXCL file in mclaims/ (atomic across kernel+shell workers)
  - done  = mparts/batch_XXXX.csv exists (pre,post,n with pre typed)
  - 'Limited query' truncation warning -> split batch in half and retry
  - status -> microns_status.json (done/rows/wall per batch)
"""
import os, sys, json, time, warnings, threading, traceback

sys.path.append('/home/kimi/.local/lib/python3.12/site-packages')
import pandas as pd
from caveclient import CAVEclient
from caveclient.materializationengine import MaterializationClient
from caveclient.auth import AuthClient

W = '/mnt/agents/output/simh1_work'
MPARTS = f'{W}/mparts'
CLAIMS = f'{W}/mclaims'
os.makedirs(MPARTS, exist_ok=True)
os.makedirs(CLAIMS, exist_ok=True)

TOKEN = '31b36cc83e079c03fc7c44f939231425'
VERSION = 1822
B = 100

sample = json.load(open(f'{W}/microns_sample_seed45.json'))['sample']
typed = set(json.load(open(f'{W}/microns_celltypes.json'))['cls'].keys())
typed = set(int(x) for x in typed)
batches = [sample[i:i+B] for i in range(0, len(sample), B)]
NB = len(batches)

_status_lock = threading.Lock()
def status_update(bi=None, rows=None, wall=None, note=None):
    with _status_lock:
        try:
            st = json.load(open(f'{W}/microns_status.json'))
        except Exception:
            st = {'total_batches': NB, 'done': 0, 'rows': 0, 'batches': {}}
        st['ts'] = time.time()
        if bi is not None:
            st.setdefault('batches', {})
            st['batches'][str(bi)] = {'rows': rows, 'wall': round(wall or 0, 1), 'note': note}
            done = len([f for f in os.listdir(MPARTS) if f.startswith('batch_')])
            st['done'] = done
            st['rows'] = sum(v.get('rows', 0) for v in st['batches'].values())
        json.dump(st, open(f'{W}/microns_status.json', 'w'))

def claim(bi):
    p = f'{CLAIMS}/batch_{bi:04d}.claim'
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(time.time()).encode()); os.close(fd)
        return True
    except FileExistsError:
        # steal stale claims older than 1h
        try:
            if time.time() - os.path.getmtime(p) > 3600:
                os.remove(p); return claim(bi)
        except Exception:
            pass
        return False

def query_posts(mc, posts, depth=0):
    """Query incoming synapses for a list of posts; split on truncation."""
    with warnings.catch_warnings(record=True) as wlist:
        warnings.simplefilter('always')
        df = mc.query_table('synapses_pni_2',
                            filter_in_dict={'post_pt_root_id': posts},
                            select_columns=['pre_pt_root_id', 'post_pt_root_id'])
    if any('Limited query' in str(w.message) for w in wlist):
        if len(posts) == 1:
            raise RuntimeError(f'truncated even for single post {posts[0]}')
        if depth > 7:
            raise RuntimeError('split depth exceeded')
        h = len(posts)//2
        a = query_posts(mc, posts[:h], depth+1)
        b = query_posts(mc, posts[h:], depth+1)
        return pd.concat([a, b], ignore_index=True)
    return df

def process_batch(mc, bi):
    posts = [int(x) for x in batches[bi]]
    t0 = time.time()
    df = query_posts(mc, posts)
    df = df[df['pre_pt_root_id'].isin(typed)]
    g = (df.groupby(['pre_pt_root_id', 'post_pt_root_id']).size()
           .reset_index(name='n'))
    out = f'{MPARTS}/batch_{bi:04d}.csv'
    tmp = out + f'.tmp{os.getpid()}.{threading.get_ident()}'
    g.to_csv(tmp, index=False)
    os.replace(tmp, out)
    status_update(bi, rows=int(g['n'].sum()) if len(g) else 0, wall=time.time()-t0)
    return len(g)

def worker(wid, budget_s):
    mc = MaterializationClient(
        server_address='https://minnie.microns-daf.com',
        datastack_name='minnie65_public',
        auth_client=AuthClient(token=TOKEN),
        version=VERSION)
    t_end = time.time() + budget_s
    while time.time() < t_end:
        progressed = False
        for bi in range(NB):
            if time.time() >= t_end:
                break
            if os.path.exists(f'{MPARTS}/batch_{bi:04d}.csv'):
                continue
            if not claim(bi):
                continue
            try:
                process_batch(mc, bi)
                progressed = True
            except Exception as e:
                status_update(bi, rows=0, wall=0,
                              note='ERR ' + str(e)[:160])
                try:
                    os.remove(f'{CLAIMS}/batch_{bi:04d}.claim')
                except Exception:
                    pass
                time.sleep(5)
        if not progressed:
            break

if __name__ == '__main__':
    nthreads = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
    status_update()
    ths = [threading.Thread(target=worker, args=(i, budget), daemon=True)
           for i in range(nthreads)]
    for t in ths: t.start()
    for t in ths: t.join()
    done = len([f for f in os.listdir(MPARTS) if f.startswith('batch_')])
    print(f'lane exit: {done}/{NB} batches done')
