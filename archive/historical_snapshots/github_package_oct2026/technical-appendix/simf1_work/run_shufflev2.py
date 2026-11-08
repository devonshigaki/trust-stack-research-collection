import importlib.util, numpy as np, pandas as pd, json, time
spec = importlib.util.spec_from_file_location('f1','/tmp/run_f1a2.py')
f1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f1)

# deterministic permutation identical to build('shuffle'): seed 42
rng = np.random.default_rng(42)
j2 = f1.lj[rng.permutation(len(f1.lj))]
PL = np.where(np.isin(f1.li, f1.KC) & np.isin(j2, f1.MBON))[0].astype(np.int64)
print('shuffle-v2 plastic edges (KC->MBON of permuted graph):', len(PL))
KC2E = {}
for e in PL:
    KC2E.setdefault(int(f1.li[e]), []).append(int(e))
f1.PLASTIC = PL
f1.KC2E = {k: np.array(v, dtype=np.int64) for k, v in KC2E.items()}

rows = []
for r in range(4):
    t0 = time.time()
    B0, probes = f1.run_arm('shuffle', r)
    acq = [p for p in probes if p[0] == 'acq']
    for phase, after, rate in probes:
        rows.append({'arm': 'shuffle_v2', 'run': r, 'phase': phase,
                     'after_trial': after, 'mbon_rate_hz': rate,
                     'B0': B0, 'R': rate / B0 if B0 > 0 else np.nan})
    pd.DataFrame(rows).to_csv('/mnt/agents/output/simf1_work/f1a2_probe_readouts_shufflev2.csv', index=False)
    print(f'shuffle_v2 run{r}: B0={B0:.2f} R_acq_final={acq[-1][2]/B0:.3f} ({time.time()-t0:.0f}s)', flush=True)
print('SHUFFLEV2 DONE')
