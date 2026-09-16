"""Sim H1 — merge parts, build G_N, evaluate frozen H1-A criteria.
Run only after h01_done.json covers all 166 shards."""
import json, glob
import numpy as np
import pandas as pd

S = '/mnt/agents/output/simh1_work'
shards = json.load(open(f'{S}/h01_shard_list.json'))
done = set(json.load(open(f'{S}/h01_done.json')))
assert len(done) == len(shards), f'incomplete: {len(done)}/{len(shards)}'

cells = json.load(open(f'{S}/h01_cell_data.json'))
celltype = {}
collisions = 0
for c in cells:
    k = int(c['agglo_seg'])
    if k in celltype: collisions += 1
    else: celltype[k] = c['type']

NEURONAL = {'pyramidal neuron', 'interneuron', 'spiny stellate neuron',
            'excitatory/spiny neuron with atypical tree', 'unclassified neuron'}

# merge pair parts
pairs = {}
rows_tot = 0
for f in glob.glob(f'{S}/parts/pairs_*.csv'):
    d = pd.read_csv(f)
    rows_tot += int(d.t1.sum() + d.t2.sum())
    for pre, post, a, b in zip(d.pre, d.post, d.t1, d.t2):
        key = (pre, post)
        acc = pairs.setdefault(key, [0, 0])
        acc[0] += a; acc[1] += b

pre = np.array([k[0] for k in pairs], dtype=np.int64)
post = np.array([k[1] for k in pairs], dtype=np.int64)
w1 = np.array([v[0] for v in pairs.values()], dtype=np.int64)  # type1 (inhibitory per registration)
w2 = np.array([v[1] for v in pairs.values()], dtype=np.int64)  # type2 (excitatory)
w = w1 + w2

# neuronal subgraph G_N
cls_pre = np.array([celltype.get(p, '?') for p in pre])
cls_post = np.array([celltype.get(p, '?') for p in post])
nm = np.isin(cls_pre, list(NEURONAL)) & np.isin(cls_post, list(NEURONAL))
pre_n, post_n, w_n = pre[nm], post[nm], w[nm]
cp_n, cq_n = cls_pre[nm], cls_post[nm]

total_nn = int(w_n.sum())
classes = sorted(NEURONAL)
avail = {A: int(w_n[cp_n == A].sum()) / total_nn for A in classes}
s_AB = {}
for B in classes:
    tot_B = int(w_n[cq_n == B].sum())
    s_AB[B] = {A: (int(w_n[(cp_n == A) & (cq_n == B)].sum()) / tot_B if tot_B else 0.0)
               for A in classes}

dom = {}
for B in classes:
    A_dom = max(s_AB[B], key=s_AB[B].get)
    dom[B] = {'dom_class': A_dom, 's_dom': s_AB[B][A_dom], 'a_dom': avail[A_dom],
              'gap': abs(s_AB[B][A_dom] - avail[A_dom])}

dom_vals = [d['s_dom'] for d in dom.values()]
gaps_ok = sum(1 for d in dom.values() if d['gap'] <= 0.15)
A1 = float(np.median(dom_vals)) >= 0.50
A2 = gaps_ok > len(classes) / 2

out = {'merge': {'unique_typed_pairs': len(pairs), 'typed_typed_synapses': rows_tot,
                 'neuron_neuron_edges': int(nm.sum()), 'neuron_neuron_synapses': total_nn,
                 'id_collisions_first_wins': collisions},
       'availability': avail, 's_AB': s_AB, 'dominance': dom,
       'H1A': {'A1_median_dominance': float(np.median(dom_vals)), 'A1_rule': '>=0.50', 'A1_MET': bool(A1),
               'A2_classes_within_0.15': f'{gaps_ok}/{len(classes)}', 'A2_rule': 'majority', 'A2_MET': bool(A2)}}
json.dump(out, open(f'{S}/h1a_results.json', 'w'), indent=1)
np.savez('/tmp/h01/graph_h1.npz', pre=pre, post=post, w1=w1, w2=w2,
         cls_pre=cls_pre, cls_post=cls_post)
print(json.dumps(out['merge'], indent=1))
print('A1:', out['H1A']['A1_median_dominance'], 'MET' if A1 else 'FAIL')
print('A2:', out['H1A']['A2_classes_within_0.15'], 'MET' if A2 else 'FAIL')
for B in classes: print(f"  {B:45s} dom={dom[B]['dom_class']:12s} s={dom[B]['s_dom']:.3f} a={dom[B]['a_dom']:.3f} gap={dom[B]['gap']:.3f}")
