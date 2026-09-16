"""Sim F1b driver — SIM_F1B_PRE_REGISTRATION.md (frozen 2026-09-12).
Compartment-resolved DAN gating: plastic set = KC->MBON edges onto the
triggered cluster's verified compartment set (M*_av 41 cells / M*_app MBON07).
Readouts: R_cond (conditioned set / its B0) and R_noncond (51 non-conditioned
cells / their B0). Arms: intact_av, D_abl, S_abl, gateshuf_av (plastic
re-routed to 41 random non-conditioned MBONs, seed 43), partnershuf_av
(graph partner-permuted seed 42, class-faithful plastic re-derivation,
descriptive only), intact_app, gateshuf_app (4 random non-conditioned, seed 44).
Constants/protocol/aggregation identical to F1a2."""
import json, time, sys, os
import numpy as np
import pandas as pd

sys.path.insert(0, '/tmp/Drosophila_brain_model-main')
from model import default_params as P
from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, Hz, mV

OUT = '/mnt/agents/output/simf1_work'
C = np.load('/tmp/circuit_f1.npz')
POPS = np.load('/tmp/circuit_pops.npz')
with open('/tmp/compartments.json') as f:
    COMP = json.load(f)
COND_AV = np.array(COMP['cond_av'], dtype=np.int64)
COND_APP = np.array(COMP['cond_app'], dtype=np.int64)
NONCOND = np.array(COMP['noncond'], dtype=np.int64)

li, lj, lw = C['i'], C['j'], C['w']
N = len(C['roots'])
ORN = POPS['uniPN']
PPL1, PAM, OA, MBON, KC = POPS['PPL1'], POPS['PAM'], POPS['OA'], POPS['MBON'], POPS['KC']

ETA, THETA, TAU_S = 0.25, 20.0, 12
N_RUN = 4
CS_RATE = P['r_poi']; US_RATE = P['r_poi']
PROBE_MS, CS_MS, US_MS = 1000, 900, 700
PRE_US_MS = CS_MS - US_MS
ACQ_PROBES_AFTER = {1, 2, 3, 4, 6, 8, 10, 12}
N_EXT = 8

# gate-map shuffles (frozen seeds; drawn from the non-conditioned pool,
# disjoint from the corresponding M* by construction)
M_SHUF_AV = np.sort(np.random.default_rng(43).choice(NONCOND, size=len(COND_AV), replace=False))
M_SHUF_APP = np.sort(np.random.default_rng(44).choice(NONCOND, size=len(COND_APP), replace=False))

def plastic_set(arm, jposts):
    if arm in ('intact_av', 'D_abl', 'S_abl'):
        tgt = COND_AV
    elif arm == 'gateshuf_av':
        tgt = M_SHUF_AV
    elif arm == 'partnershuf_av':
        tgt = COND_AV            # class-faithful: re-derived on permuted graph
    elif arm == 'intact_app':
        tgt = COND_APP
    elif arm == 'gateshuf_app':
        tgt = M_SHUF_APP
    else:
        raise ValueError(arm)
    pl = np.where(np.isin(li, KC) & np.isin(jposts, tgt))[0].astype(np.int64)
    kc2e = {}
    for e in pl:
        kc2e.setdefault(int(li[e]), []).append(int(e))
    return pl, {k: np.array(v, dtype=np.int64) for k, v in kc2e.items()}

def cond_readout_set(arm):
    return COND_APP if arm in ('intact_app', 'gateshuf_app') else COND_AV

def build(arm):
    neu = NeuronGroup(N, model=P['eqs'], method='linear', threshold=P['eq_th'],
                      reset=P['eq_rst'], refractory='rfc', namespace=P)
    neu.v = P['v_0']; neu.g = 0; neu.rfc = P['t_rfc']
    syn = Synapses(neu, neu, 'w : volt', on_pre='g += w', delay=P['t_dly'])
    if arm == 'partnershuf_av':
        rng = np.random.default_rng(42)
        jposts = lj[rng.permutation(len(lj))]
        syn.connect(i=li, j=jposts)
    else:
        jposts = lj
        syn.connect(i=li, j=lj)
    syn.w = lw * P['w_syn']
    PL, KC2E = plastic_set(arm, jposts)
    spk = SpikeMonitor(neu)
    w_drive = P['w_syn'] * P['f_poi']
    pgs, pois = [], {}
    for name, idxs in [('CS', ORN), ('US_A', PPL1), ('US_APP', PAM)]:
        pg = PoissonGroup(len(idxs), rates=0 * Hz)
        s_in = Synapses(pg, neu, on_pre='v += w_drive', namespace={'w_drive': w_drive})
        s_in.connect(i=np.arange(len(idxs)), j=idxs)
        for k in idxs:
            neu[k].rfc = 0 * ms
        pois[name] = pg
        pgs += [pg, s_in]
    net = Network(neu, syn, spk, *pgs)
    w0_mV = np.asarray(syn.w[PL] / mV).copy()
    return net, spk, syn, pois, w0_mV, PL, KC2E

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
    net, spk, syn, pois, w0_mV, PL, KC2E = build(arm)
    eta = 0.0 if arm == 'D_abl' else ETA
    tau = 3 if arm == 'S_abl' else TAU_S
    appetitive = arm in ('intact_app', 'gateshuf_app')
    us_key = 'US_APP' if appetitive else 'US_A'
    dan_pop = PAM if appetitive else PPL1
    COND = cond_readout_set(arm)
    t_abs = 0.0
    probes = []

    def probe(phase, after):
        nonlocal t_abs
        set_rate(pois['CS'], CS_RATE)
        net.run(PROBE_MS * ms)
        t_abs += PROBE_MS
        set_rate(pois['CS'], 0 * Hz)
        cc = spikes_in(spk, COND, t_abs - 700, t_abs)
        cn = spikes_in(spk, NONCOND, t_abs - 700, t_abs)
        rc = sum(cc.values()) / len(COND) / 0.7
        rn = sum(cn.values()) / len(NONCOND) / 0.7
        probes.append((phase, after, rc, rn))

    for b in range(3):
        probe('baseline', b)
    B0c = float(np.mean([p[2] for p in probes]))
    B0n = float(np.mean([p[3] for p in probes]))

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
            w_mV = np.asarray(syn.w[PL] / mV).copy()
            for k, cnt in kc_sp.items():
                if cnt > 0 and k in KC2E:
                    pos = np.searchsorted(PL, KC2E[k])
                    w_mV[pos] *= (1 - eta)
            syn.w[PL] = w_mV * mV
        if trial in ACQ_PROBES_AFTER:
            probe('acq', trial)

    for e in range(N_EXT):
        if e > 0:
            w_mV = np.asarray(syn.w[PL] / mV).copy()
            syn.w[PL] = (w_mV + (w0_mV - w_mV) / tau) * mV
        probe('ext', e + 1)

    return B0c, B0n, probes

ARMS = {
    '1': ['intact_av', 'D_abl', 'S_abl', 'gateshuf_av'],
    '2': ['partnershuf_av', 'intact_app', 'gateshuf_app'],
}

def main():
    which = os.environ.get('F1B_SET', '1')
    arms = ARMS[which]
    rows = []
    out_csv = f'{OUT}/f1b_probe_readouts_set{which}.csv'
    for arm in arms:
        for r in range(N_RUN):
            t0 = time.time()
            B0c, B0n, probes = run_arm(arm, r)
            acq = [p for p in probes if p[0] == 'acq']
            for phase, after, rc, rn in probes:
                rows.append({'arm': arm, 'run': r, 'phase': phase,
                             'after_trial': after,
                             'rate_cond': rc, 'rate_noncond': rn,
                             'B0_cond': B0c, 'B0_noncond': B0n,
                             'R_cond': rc / B0c if B0c > 0 else np.nan,
                             'R_noncond': rn / B0n if B0n > 0 else np.nan})
            pd.DataFrame(rows).to_csv(out_csv, index=False)
            r_fin = acq[-1][2] / B0c if B0c > 0 else float('nan')
            print(f'{arm} run{r}: B0_cond={B0c:.2f} B0_noncond={B0n:.2f} '
                  f'R_cond_final={r_fin:.3f} ({time.time()-t0:.0f}s)', flush=True)
    print('F1B DONE', flush=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'smoke':
        for arm in ['intact_av', 'gateshuf_av', 'intact_app', 'gateshuf_app']:
            net, spk, syn, pois, w0, PL, KC2E = build(arm)
            set_rate(pois['CS'], CS_RATE)
            t = time.time()
            net.run(1000 * ms)
            COND = cond_readout_set(arm)
            cc = spikes_in(spk, COND, 300, 1000)
            cn = spikes_in(spk, NONCOND, 300, 1000)
            print(f'SMOKE {arm}: plastic={len(PL)} '
                  f'cond={sum(cc.values())/len(COND)/0.7:.2f}Hz '
                  f'noncond={sum(cn.values())/len(NONCOND)/0.7:.2f}Hz '
                  f'wall={time.time()-t:.0f}s', flush=True)
    else:
        main()
