"""Sim H1-B driver — MICrONS substrate (Amendments 2-4).
Brian2 LIF propagation on the sampled-posts neuronal graph
(graph_h1b_microns.npz, built by h1a_evaluate_microns.py):
  drive   = all 4P-class nodes, 150 Hz / 1000 ms
            (PoissonGroup + 1:1 synapses, rfc=0 — F-series drive pattern)
  readout = non-4P excitatory nodes, spikes in final 700 ms
  arms    = intact vs seed-42 global partner-permutation (postsynaptic
            partners permuted, weights preserved — the frozen recipe)
  n_run   = 4, run-mean primary
Edge signs by presynaptic class-level E/I (v661 classification_system);
w = ±0.275 mV x synapse count. All 11 MICrONS neuronal classes are mapped
(no unmapped class exists in this substrate).
(B1) intact gate: readout spikes > 0 in >= 3/4 runs else
     INDETERMINATE-instrument (pre-scored, reported).
(B2) R_perm = permuted/intact readout spike count >= 0.50.
Parameters per Shiu et al. 2024 default_params (disclosed calibration).
"""
import json, time, sys
import numpy as np

sys.path.append('/home/kimi/.local/lib/python3.12/site-packages')
sys.path.insert(0, '/tmp/Drosophila_brain_model-main')
from model import default_params as P
from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, Hz, mV

S = '/mnt/agents/output/simh1_work'
G = np.load(f'{S}/graph_h1b_microns.npz', allow_pickle=False)
pre, post, w = G['pre'], G['post'], G['w']
cls_pre, cls_post = G['cls_pre'], G['cls_post']

nodes = np.unique(np.concatenate([pre, post]))
idx = {int(r): k for k, r in enumerate(nodes.tolist())}
li = np.array([idx[int(r)] for r in pre], dtype=np.int32)
lj = np.array([idx[int(r)] for r in post], dtype=np.int32)
N = len(nodes)

EXC = {'23P', '4P', '5P-IT', '5P-ET', '5P-NP', '6P-IT', '6P-CT'}
INH = {'BC', 'MC', 'BPC', 'NGC'}
sign = np.zeros(len(pre))
for e in range(len(pre)):
    c = cls_pre[e]
    if c in EXC: sign[e] = 1.0
    elif c in INH: sign[e] = -1.0
assert (sign != 0).all(), 'unmapped class present — violates Amendment 3 mapping'
w_signed = sign * w

node_cls = {}
for e in range(len(pre)):
    node_cls.setdefault(li[e], cls_pre[e]); node_cls.setdefault(lj[e], cls_post[e])
DRIVE = np.array([k for k, c in node_cls.items() if c == '4P'], dtype=np.int32)
READOUT = np.array([k for k, c in node_cls.items()
                    if c in EXC and c != '4P'], dtype=np.int32)
# effective sets (disclosed): drivers with out-edges, readout with in-edges
out_edges = set(li.tolist()); in_edges = set(lj.tolist())
eff = {'drive_nodes': int(len(DRIVE)),
       'drive_with_outedges': int(sum(1 for k in DRIVE if k in out_edges)),
       'readout_nodes': int(len(READOUT)),
       'readout_with_inedges': int(sum(1 for k in READOUT if k in in_edges))}
print(f'G_N: {N} neurons, {len(li)} edges | {eff}', flush=True)
assert len(li) >= 10000, 'INDETERMINATE-instrument: G_N < 10,000 edges'

N_RUN = 4

def build(arm):
    neu = NeuronGroup(N, model=P['eqs'], method='linear', threshold=P['eq_th'],
                      reset=P['eq_rst'], refractory='rfc', namespace=P)
    neu.v = P['v_0']; neu.g = 0; neu.rfc = P['t_rfc']
    syn = Synapses(neu, neu, 'w : volt', on_pre='g += w', delay=P['t_dly'])
    if arm == 'perm':
        rng = np.random.default_rng(42)
        syn.connect(i=li, j=lj[rng.permutation(len(lj))])
    else:
        syn.connect(i=li, j=lj)
    syn.w = w_signed * P['w_syn']
    spk = SpikeMonitor(neu)
    pg = PoissonGroup(len(DRIVE), rates=0 * Hz)
    s_in = Synapses(pg, neu, on_pre='v += w_drive',
                    namespace={'w_drive': P['w_syn'] * P['f_poi']})
    s_in.connect(i=np.arange(len(DRIVE)), j=DRIVE)
    for k in DRIVE:
        neu[k].rfc = 0 * ms
    net = Network(neu, syn, spk, pg, s_in)
    return net, spk, pg

def run_once(arm, run_id):
    net, spk, pg = build(arm)
    pg.rates = 150 * Hz
    net.run(1000 * ms)
    tr = spk.spike_trains()
    n = 0
    for k in READOUT:
        t = tr.get(int(k), None)
        if t is not None:
            a = np.asarray(t / ms)
            n += int(((a >= 300) & (a < 1000)).sum())
    return n

def main():
    rows = []
    for arm in ['intact', 'perm']:
        for r in range(N_RUN):
            t0 = time.time()
            n = run_once(arm, r)
            rows.append({'arm': arm, 'run': r, 'readout_spikes': n})
            print(f'{arm} run{r}: readout_spikes={n} ({time.time()-t0:.0f}s)', flush=True)
    intact = [x['readout_spikes'] for x in rows if x['arm'] == 'intact']
    perm = [x['readout_spikes'] for x in rows if x['arm'] == 'perm']
    mi, mp = float(np.mean(intact)), float(np.mean(perm))
    B1 = sum(1 for x in intact if x > 0) >= 3
    R = mp / mi if mi > 0 else float('nan')
    res = {'substrate': 'minnie65_public v1822, sampled-posts graph (Amendments 2-4)',
           'graph': eff, 'edges': int(len(li)), 'nodes': int(N),
           'rows': rows, 'intact_mean': mi, 'perm_mean': mp,
           'B1_gate': bool(B1), 'R_perm': R, 'B2_rule': '>=0.50',
           'B2_MET': bool(R >= 0.50) if B1 else None,
           'verdict_note': 'INDETERMINATE-instrument' if not B1 else 'scored'}
    json.dump(res, open(f'{S}/h1b_results_microns.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == '__main__':
    main()
