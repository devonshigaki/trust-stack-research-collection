"""Sim F1a conditioning driver — implements Design Addendum A verbatim.
Arms: intact-aversive, D-ablated (eta=0), intact-appetitive, OA-ablated appetitive,
shuffle (partners permuted, seed 42), S-ablated (tau_S=3; arm added to evaluate
frozen criterion 4 — clerical omission from arm list, documented).
n_run=4 per arm. Aggregation locked BEFORE conditioning data: criteria evaluated
on the run-mean curve; per-run values reported secondary."""
import json, time, sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/tmp/Drosophila_brain_model-main')
from model import default_params as P
from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, Hz, mV

OUT = '/mnt/agents/output/simf1_work'
C = np.load('/tmp/circuit_f1.npz')
POPS = np.load('/tmp/circuit_pops.npz')
with open('/tmp/kc_to_edges.json') as f:
    KC2E = {int(k): np.array(v, dtype=np.int64) for k, v in json.load(f).items()}

li, lj, lw = C['i'], C['j'], C['w']
PLASTIC = C['plastic_edges']          # sorted ascending
N = len(C['roots'])
ORN, SUGAR = POPS['ORN_DL3'], POPS['sugar']
PPL1, PAM, OA, MBON, KC = POPS['PPL1'], POPS['PAM'], POPS['OA'], POPS['MBON'], POPS['KC']

ETA, THETA, TAU_S = 0.25, 20.0, 12
N_RUN = 4
CS_RATE = P['r_poi']; US_RATE = P['r_poi']
PROBE_MS, CS_MS, US_MS = 1000, 900, 700
PRE_US_MS = CS_MS - US_MS
ACQ_PROBES_AFTER = {1, 2, 3, 4, 6, 8, 10, 12}
N_EXT = 8

def build(arm):
    neu = NeuronGroup(N, model=P['eqs'], method='linear', threshold=P['eq_th'],
                      reset=P['eq_rst'], refractory='rfc', namespace=P)
    neu.v = P['v_0']; neu.g = 0; neu.rfc = P['t_rfc']
    syn = Synapses(neu, neu, 'w : volt', on_pre='g += w', delay=P['t_dly'])
    if arm == 'shuffle':
        rng = np.random.default_rng(42)
        syn.connect(i=li, j=lj[rng.permutation(len(lj))])
    else:
        syn.connect(i=li, j=lj)
    syn.w = lw * P['w_syn']
    if arm == 'OA_abl':
        oa_mask = np.isin(li, OA)
        syn.w[np.where(oa_mask)[0]] = 0 * mV
    spk = SpikeMonitor(neu)
    w_drive = P['w_syn'] * P['f_poi']
    pgs, pois = [], {}
    for name, idxs in [('CS', ORN), ('US_A', PPL1), ('US_APP', SUGAR)]:
        pg = PoissonGroup(len(idxs), rates=0 * Hz)
        s_in = Synapses(pg, neu, on_pre='v += w_drive', namespace={'w_drive': w_drive})
        s_in.connect(i=np.arange(len(idxs)), j=idxs)
        for k in idxs:
            neu[k].rfc = 0 * ms
        pois[name] = pg
        pgs += [pg, s_in]
    net = Network(neu, syn, spk, *pgs)
    w0_mV = np.asarray(syn.w[PLASTIC] / mV).copy()
    return net, spk, syn, pois, w0_mV

def set_rate(pg, rate):
    pg.rates = rate

def spikes_in(spk, idxs, t0_ms, t1_ms):
    tr = spk.spike_trains()
    out = {}
    for k in idxs:
        t = tr.get(int(k), None)
        if t is None:
            out[int(k)] = 0
        else:
            a = np.asarray(t / ms)
            out[int(k)] = int(((a >= t0_ms) & (a < t1_ms)).sum())
    return out

def run_arm(arm, run_id):
    net, spk, syn, pois, w0_mV = build(arm)
    eta = 0.0 if arm == 'D_abl' else ETA
    tau = 3 if arm == 'S_abl' else TAU_S
    appetitive = arm in ('appetitive', 'OA_abl')
    us_key = 'US_APP' if appetitive else 'US_A'
    dan_pop = PAM if appetitive else PPL1
    t_abs = 0.0
    probes = []

    def probe(phase, after):
        nonlocal t_abs
        set_rate(pois['CS'], CS_RATE)
        net.run(PROBE_MS * ms)
        t_abs += PROBE_MS
        set_rate(pois['CS'], 0 * Hz)
        c = spikes_in(spk, MBON, t_abs - 700, t_abs)
        rate = sum(c.values()) / len(MBON) / 0.7
        probes.append((phase, after, rate))

    for b in range(3):
        probe('baseline', b)
    B0 = float(np.mean([p[2] for p in probes]))

    for trial in range(1, 13):
        set_rate(pois['CS'], CS_RATE)
        t0 = t_abs
        net.run(PRE_US_MS * ms)
        t_abs += PRE_US_MS
        set_rate(pois[us_key], US_RATE)
        us0 = t_abs
        net.run(US_MS * ms)
        t_abs += US_MS
        set_rate(pois['CS'], 0 * Hz)
        set_rate(pois[us_key], 0 * Hz)
        kc_sp = spikes_in(spk, KC, t0, t0 + CS_MS)
        dan = spikes_in(spk, dan_pop, us0, us0 + US_MS)
        dan_rate = sum(dan.values()) / len(dan_pop) / (US_MS / 1000.0)
        if dan_rate > THETA and eta > 0:
            w_mV = np.asarray(syn.w[PLASTIC] / mV).copy()
            for k, cnt in kc_sp.items():
                if cnt > 0 and k in KC2E:
                    pos = np.searchsorted(PLASTIC, KC2E[k])
                    w_mV[pos] *= (1 - eta)
            syn.w[PLASTIC] = w_mV * mV
        if trial in ACQ_PROBES_AFTER:
            probe('acq', trial)

    for e in range(N_EXT):
        if e > 0:
            w_mV = np.asarray(syn.w[PLASTIC] / mV).copy()
            syn.w[PLASTIC] = (w_mV + (w0_mV - w_mV) / tau) * mV
        probe('ext', e + 1)

    return B0, probes

def main():
    arms = ['intact_av', 'D_abl', 'appetitive', 'OA_abl', 'shuffle', 'S_abl']
    rows = []
    out_csv = f'{OUT}/f1a_probe_readouts.csv'
    for arm in arms:
        for r in range(N_RUN):
            t0 = time.time()
            B0, probes = run_arm(arm, r)
            acq = [p for p in probes if p[0] == 'acq']
            for phase, after, rate in probes:
                rows.append({'arm': arm, 'run': r, 'phase': phase,
                             'after_trial': after, 'mbon_rate_hz': rate,
                             'B0': B0, 'R': rate / B0 if B0 > 0 else np.nan})
            pd.DataFrame(rows).to_csv(out_csv, index=False)
            r_fin = acq[-1][2] / B0 if B0 > 0 else float('nan')
            print(f'{arm} run{r}: B0={B0:.2f}Hz R_acq_final={r_fin:.3f} '
                  f'({time.time()-t0:.0f}s)', flush=True)
    print('F1A DONE', flush=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'smoke':
        net, spk, syn, pois, w0 = build('intact_av')
        set_rate(pois['CS'], CS_RATE)
        t = time.time()
        net.run(1000 * ms)
        c = spikes_in(spk, MBON, 300, 1000)
        kc = spikes_in(spk, KC, 0, 1000)
        nkc = sum(1 for v in kc.values() if v > 0)
        print(f'SMOKE: MBON rate={sum(c.values())/len(MBON)/0.7:.2f}Hz '
              f'active_KCs={nkc}/{len(KC)} wall={time.time()-t:.0f}s')
    else:
        main()
