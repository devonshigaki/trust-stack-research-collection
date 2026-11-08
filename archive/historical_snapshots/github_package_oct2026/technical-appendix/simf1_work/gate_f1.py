"""Sim F1 reference gate, RAM-safe build from /tmp/graph783.npz.
Frozen protocol: whole-brain v783, default params, 20/21 sugar GRNs at 150 Hz,
MN9 readout, n_run=4 drive + 4 shuffle (seed 42)."""
import json, time, sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/tmp/Drosophila_brain_model-main')
from model import default_params as P
from brian2 import (NeuronGroup, Synapses, PoissonInput, SpikeMonitor, Network,
                    mV, ms)

REPO = '/tmp/Drosophila_brain_model-main'
OUT = '/mnt/agents/output/simf1_work'
SUGAR = [720575940624963786,720575940630233916,720575940637568838,720575940638202345,
         720575940617000768,720575940630797113,720575940632889389,720575940621754367,
         720575940621502051,720575940640649691,720575940639332736,720575940616885538,
         720575940639198653,720575940620900446,720575940617937543,720575940632425919,
         720575940633143833,720575940612670570,720575940628853239,720575940629176663,
         720575940611875570]
MN9 = 720575940660219265
N_RUN = 4

comp = pd.read_csv(f'{REPO}/Completeness_783.csv', index_col=0)
roster = comp.index.to_numpy()
flyid2i = {j: k for k, j in enumerate(roster)}
sugar_present = [s for s in SUGAR if s in flyid2i]
mn9_i = flyid2i[MN9]
print(f'sugar present {len(sugar_present)}/21; MN9 idx {mn9_i}', flush=True)

g = np.load('/tmp/graph783.npz')
ei, ej, ew = g['i'], g['j'], g['w']
print('graph loaded', len(ei), 'edges', flush=True)

rng = np.random.default_rng(42)
forbidden = set(SUGAR) | {MN9}
pool = np.array([k for k in range(len(roster)) if roster[k] not in forbidden])
shuffle_idx = np.sort(rng.choice(pool, size=len(sugar_present), replace=False))

results = {'n_run': N_RUN, 'mn9_id': MN9, 'sugar_ids_present': sugar_present,
           'shuffle_flywire_ids': [int(roster[k]) for k in shuffle_idx]}

def build(exc_idx):
    neu = NeuronGroup(len(roster), model=P['eqs'], method='linear',
                      threshold=P['eq_th'], reset=P['eq_rst'], refractory='rfc',
                      namespace=P)
    neu.v = P['v_0']; neu.g = 0; neu.rfc = P['t_rfc']
    syn = Synapses(neu, neu, 'w : volt', on_pre='g += w', delay=P['t_dly'])
    syn.connect(i=ei, j=ej)
    syn.w = ew * P['w_syn']
    spk = SpikeMonitor(neu)
    pois = [PoissonInput(neu[k], 'v', 1, P['r_poi'], P['w_syn'] * P['f_poi'])
            for k in exc_idx]
    for k in exc_idx:
        neu[k].rfc = 0 * ms
    net = Network(neu, syn, spk, *pois)
    net.store('init')
    return net, spk

for cond, exc in [('drive', [flyid2i[s] for s in sugar_present]),
                  ('shuffle', list(shuffle_idx))]:
    t0 = time.time()
    net, spk = build(exc)
    print(f'[{cond}] build {time.time()-t0:.0f}s', flush=True)
    mn9c, totc, rt = [], [], []
    for r in range(N_RUN):
        t1 = time.time()
        net.restore('init')
        net.run(P['t_run'])
        tr = spk.spike_trains()
        mn9c.append(int(len(tr.get(mn9_i, []))))
        totc.append(int(sum(len(v) for v in tr.values())))
        rt.append(round(time.time() - t1, 1))
        print(f'[{cond}] run {r}: MN9={mn9c[-1]} total={totc[-1]} ({rt[-1]}s)',
              flush=True)
    results[cond] = {'mn9_spike_counts': mn9c, 'total_spikes': totc,
                     'run_seconds': rt}
    del net, spk

with open(f'{OUT}/gate_f1_results.json', 'w') as f:
    json.dump(results, f, indent=1)
print('GATE DONE', flush=True)
