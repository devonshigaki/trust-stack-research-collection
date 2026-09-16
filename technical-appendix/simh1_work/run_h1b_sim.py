"""Sim H1-B driver — SIM_H1_PRE_REGISTRATION.md (frozen 2026-09-12).
Brian2 LIF propagation on G_N (H01 neuronal typed subgraph): drive = all
spiny stellate neurons 150 Hz / 1000 ms (PoissonGroup + 1:1 synapses, rfc=0);
readout = pyramidal spikes in final 700 ms. Arms: intact vs class-faithful
global partner-permutation (seed 42, weights preserved). n_run=4, run-mean.
Edge signs by author class->E/I mapping; w = ±0.275 mV x synapse count.
(B1) intact gate: pyramidal spikes > 0 in >= 3/4 runs.
(B2) R_perm = permuted/intact pyramidal spike count >= 0.50.
Parameters per Shiu et al. 2024 default_params (cross-study calibration,
disclosed in registration)."""
import json, time, sys
import numpy as np

sys.path.append('/home/kimi/.local/lib/python3.12/site-packages')
sys.path.insert(0, '/tmp/Drosophila_brain_model-main')
from model import default_params as P
from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, Hz, mV

S = '/mnt/agents/output/simh1_work'
G = np.load('/tmp/h01/graph_h1.npz', allow_pickle=False)
pre, post, w1, w2 = G['pre'], G['post'], G['w1'], G['w2']
cls_pre, cls_post = G['cls_pre'], G['cls_post']

# node set = neuronal subgraph nodes; local index remap
nodes = np.unique(np.concatenate([pre, post]))
idx = {int(r): k for k, r in enumerate(nodes.tolist())}
li = np.array([idx[int(r)] for r in pre], dtype=np.int32)
lj = np.array([idx[int(r)] for r in post], dtype=np.int32)
N = len(nodes)

EXC = {'pyramidal neuron', 'spiny stellate neuron',
       'excitatory/spiny neuron with atypical tree'}
INH = {'interneuron'}
# signed weight: class-level E/I of the PRESYNAPTIC cell (registration 2a);
# magnitude = 0.275 mV x total synapse count; unclassified-mapped classes
# use synapse-level type split (w2 exc - w1 inh) per registration fallback note
sign = np.zeros(len(pre))
for e in range(len(pre)):
    c = cls_pre[e]
    if c in EXC: sign[e] = 1.0
    elif c in INH: sign[e] = -1.0
    # else: unmapped class (unclassified neuron) -> sign 0 => edge excluded
    # from signed propagation, the direct implementation of registration
    # section 2a ("unclassified neuron = unmapped"; class-level E/I only)
w_signed = sign * (w1 + w2)

node_cls = {}
for e in range(len(pre)):
    node_cls.setdefault(li[e], cls_pre[e]); node_cls.setdefault(lj[e], cls_post[e])
STEL = np.array([k for k, c in node_cls.items() if c == 'spiny stellate neuron'], dtype=np.int32)
PYR = np.array([k for k, c in node_cls.items() if c == 'pyramidal neuron'], dtype=np.int32)
print(f'G_N: {N} neurons, {len(li)} edges | stellate={len(STEL)} pyramidal={len(PYR)}')
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
    pg = PoissonGroup(len(STEL), rates=0 * Hz)
    s_in = Synapses(pg, neu, on_pre='v += w_drive',
                    namespace={'w_drive': P['w_syn'] * P['f_poi']})
    s_in.connect(i=np.arange(len(STEL)), j=STEL)
    for k in STEL:
        neu[k].rfc = 0 * ms
    net = Network(neu, syn, spk, pg, s_in)
    return net, spk, pg

def run_once(arm, run_id):
    net, spk, pg = build(arm)
    pg.rates = 150 * Hz
    net.run(1000 * ms)
    tr = spk.spike_trains()
    n = 0
    for k in PYR:
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
            rows.append({'arm': arm, 'run': r, 'pyr_spikes': n})
            print(f'{arm} run{r}: pyr_spikes={n} ({time.time()-t0:.0f}s)', flush=True)
    intact = [x['pyr_spikes'] for x in rows if x['arm'] == 'intact']
    perm = [x['pyr_spikes'] for x in rows if x['arm'] == 'perm']
    mi, mp = float(np.mean(intact)), float(np.mean(perm))
    B1 = sum(1 for x in intact if x > 0) >= 3
    R = mp / mi if mi > 0 else float('nan')
    res = {'rows': rows, 'intact_mean': mi, 'perm_mean': mp,
           'B1_gate': bool(B1), 'R_perm': R, 'B2_rule': '>=0.50',
           'B2_MET': bool(R >= 0.50) if B1 else None,
           'verdict_note': 'INDETERMINATE-instrument' if not B1 else 'scored'}
    json.dump(res, open(f'{S}/h1b_results.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == '__main__':
    main()
