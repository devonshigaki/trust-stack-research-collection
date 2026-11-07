"""Sim H1 — MICrONS substrate: merge mparts, build sampled-posts G_N,
evaluate frozen H1-A criteria (A1, A2) per SIM_H1_PRE_REGISTRATION.md §4
with Amendments 2-4 (MICrONS substrate; sampled-posts pull; rebuilt
first-wins v661 class map).

Run only after microns_status.json reports 120/120 batches.

Estimators (Amendment 3 §3): uniform postsynaptic sampling with COMPLETE
per-post incoming typed sets -> ratio estimators for s_AB and availability
are unbiased. s_AB[B] = synapses from neuronal class A onto SAMPLED class-B
posts / all typed-neuron -> sampled-B synapses. availability a_A = class-A
share of all typed-neuron -> sampled typed-neuron posts synapses.
"""
import json, glob, collections
import numpy as np
import pandas as pd

S = '/mnt/agents/output/simh1_work'

# --- completeness gate ---
st = json.load(open(f'{S}/microns_status.json'))
files = sorted(glob.glob(f'{S}/mparts/batch_*.csv'))
assert len(files) == 120, f'incomplete: {len(files)}/120 batches'

# --- class map (rebuilt, first-wins; Amendment 4) ---
m = json.load(open(f'{S}/microns_celltypes.json'))
cls_map = {int(k): v for k, v in m['cls'].items()}
sys_map = {int(k): v for k, v in m['sys'].items()}
NEUR_SYS = {'excitatory_neuron', 'inhibitory_neuron'}
neuronal = {r for r in sys_map if sys_map[r] in NEUR_SYS}

# --- frozen sample ---
sample = [int(x) for x in json.load(open(f'{S}/microns_sample_seed45.json'))['sample']]
sample_neur = [r for r in sample if r in neuronal]
post_cls = {r: cls_map[r] for r in sample_neur}
sample_set = set(sample_neur)
print(f'sampled posts: {len(sample)}; neuronal typed: {len(sample_neur)}')
print('per-class sampled posts:', dict(collections.Counter(post_cls.values())))

# --- merge parts: pairs pre->post onto sampled neuronal posts, pre neuronal ---
acc = collections.Counter()
rows_seen = 0
for f in files:
    d = pd.read_csv(f)
    d = d.rename(columns={'pre_pt_root_id': 'pre', 'post_pt_root_id': 'post'})
    rows_seen += int(d['n'].sum())
    for pre, post, n in zip(d['pre'], d['post'], d['n']):
        pre, post = int(pre), int(post)
        if post in sample_set and pre in neuronal:
            acc[(pre, post)] += int(n)
print(f'parts rows (old-filter superset): {rows_seen:,}; '
      f'kept typed-neuron pairs onto sampled posts: {len(acc):,}')

pre = np.array([k[0] for k in acc], dtype=np.int64)
post = np.array([k[1] for k in acc], dtype=np.int64)
w = np.array([v for v in acc.values()], dtype=np.int64)
cp = np.array([cls_map[p] for p in pre])
cq = np.array([cls_map[q] for q in post])

EXC = ['23P', '4P', '5P-IT', '5P-ET', '5P-NP', '6P-IT', '6P-CT']
INH = ['BC', 'MC', 'BPC', 'NGC']
classes = EXC + INH
assert set(cp) | set(cq) <= set(classes), (set(cp) | set(cq)) - set(classes)

total = int(w.sum())
avail = {A: float(w[cp == A].sum()) / total for A in classes}
s_AB = {}
for B in classes:
    mB = cq == B
    totB = float(w[mB].sum())
    s_AB[B] = {A: (float(w[mB & (cp == A)].sum()) / totB if totB else 0.0)
               for A in classes}

dom = {}
for B in classes:
    A_dom = max(s_AB[B], key=s_AB[B].get)
    dom[B] = {'dom_class': A_dom, 's_dom': s_AB[B][A_dom], 'a_dom': avail[A_dom],
              'gap': abs(s_AB[B][A_dom] - avail[A_dom]),
              'synapses_onto_class': int(w[cq == B].sum())}

dom_vals = [d['s_dom'] for d in dom.values()]
gaps_ok = sum(1 for d in dom.values() if d['gap'] <= 0.15)
A1 = float(np.median(dom_vals)) >= 0.50
A2 = gaps_ok > len(classes) / 2

out = {
  'substrate': {'datastack': 'minnie65_public', 'version': 1822,
                'celltype_table': 'aibs_metamodel_celltypes_v661 (first-wins, Amendment 4)',
                'sampled_posts': len(sample), 'typed_neuronal_posts': len(sample_neur),
                'posts_per_class': dict(collections.Counter(post_cls.values()))},
  'merge': {'typed_pairs_kept': len(acc), 'synapses_onto_sampled_posts': total},
  'availability': avail, 's_AB': s_AB, 'dominance': dom,
  'H1A': {'A1_median_dominance': float(np.median(dom_vals)), 'A1_rule': '>=0.50',
          'A1_MET': bool(A1),
          'A2_classes_within_0.15': f'{gaps_ok}/{len(classes)}',
          'A2_rule': 'majority', 'A2_MET': bool(A2)}}
json.dump(out, open(f'{S}/h1a_results_microns.json', 'w'), indent=1)

# --- H1-B graph (Amendment 3 §4): nodes = sampled posts + their typed pres ---
np.savez(f'{S}/graph_h1b_microns.npz', pre=pre, post=post, w=w,
         cls_pre=cp, cls_post=cq)
json.dump({'nodes': int(len(set(pre.tolist()) | set(post.tolist()))),
           'edges': int(len(w)), 'synapses': total},
          open(f'{S}/graph_h1b_microns_stats.json', 'w'))

print(json.dumps(out['merge'], indent=1))
print('A1 median dominance:', out['H1A']['A1_median_dominance'],
      'MET' if A1 else 'FAIL')
print('A2 within-0.15:', out['H1A']['A2_classes_within_0.15'],
      'MET' if A2 else 'FAIL')
for B in classes:
    d = dom[B]
    print(f"  {B:6s} dom={d['dom_class']:6s} s={d['s_dom']:.3f} "
          f"a={d['a_dom']:.3f} gap={d['gap']:.3f} n_syn={d['synapses_onto_class']:,}")
