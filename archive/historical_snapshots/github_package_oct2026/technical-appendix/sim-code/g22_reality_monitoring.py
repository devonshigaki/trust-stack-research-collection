#!/usr/bin/env python3
"""
Sim G22 - Reality-monitoring corruption of trust-stage dynamics.
Source-mixing extension of Sim G6-M1 (GTT). Implements SIM_G22_PRE_REGISTRATION.md exactly.

Source-mixing model per Dijkstra & Fleming (2023, Nat. Commun., DOI 10.1038/s41467-023-37322-1):
perceived signal = V + alpha*X (imagery intermixed with perception); judged real iff > T.
Trust dynamics: theta_{t+1} = theta_t + lam*(S_t - theta_t) on Delta^4, lam = 0.35 planted.
Distance: Hellinger chord sqrt(1 - sum(sqrt(theta*phi))) - the G6-M1 printed convention.

Frozen constants: seed 20260913 (legacy RandomState), 60 ICs ~ Dirichlet(1), 25 steps,
T* = uniform over 5 stage components (0.2 x 5), alpha = 1, T = 2.5, v_i ~ N(mu_v, 1) truncated >= 0, grid {0,1.25,2.5,3.75,5.0}.
Status: first and only run of the frozen spec.
"""
import numpy as np, json, os

SEED = 20260913
N = 60; STEPS = 25; LAM = 0.35; ALPHA = 1.0; T_THRESH = 2.5; K = 8
GRID = [0.0, 1.25, 2.5, 3.75, 5.0]
TST = np.full(5, 0.2)  # Delta^4 = 5 stage components (uniform 0.2 x 5)

def chord(a, b):  # Hellinger chord distance
    return float(np.sqrt(max(0.0, 1.0 - np.sum(np.sqrt(a * b)))))

def trunc_norm(rng, mu, sd=1.0):
    return max(0.0, rng.normal(mu, sd))

def run_arm0():  # clean-perception gate: exact G6-M1 reproduction
    rng = np.random.RandomState(SEED)
    ic = rng.dirichlet(np.ones(5), size=N)
    th = ic.copy(); d0 = np.mean([chord(t, TST) for t in th])
    for _ in range(STEPS):
        th = th + LAM * (TST - th)
    d7 = None
    th = ic.copy()
    for s in range(STEPS):
        th = th + LAM * (TST - th)
        if s == 6: d7 = np.array([chord(t, TST) for t in th])
    d25 = np.array([chord(t, TST) for t in th])
    return dict(ic=ic.tolist(), d0=float(d0), d7=d7.tolist(), d25=d25.tolist(),
                ratio=float(np.mean(d25) / d0), inside7=int(np.sum(d7 < 0.05)))

def draw_ev(rng, mu_v, n):
    E = rng.dirichlet(np.ones(5), size=n)
    v = np.array([trunc_norm(rng, mu_v) for _ in range(n)])
    return E, v

def step_update(th, target):
    return th + LAM * (target - th)

def run_armA(mu_v, gi):
    rng = np.random.RandomState(SEED); ic = rng.dirichlet(np.ones(5), size=N)  # same IC stream as Arm 0
    rng2 = np.random.RandomState(SEED + gi); E, v = draw_ev(rng2, mu_v, N)
    th = ic.copy(); no_upd = 0; tot = 0
    for _ in range(STEPS):
        for i in range(N):
            tot += 1
            m = v[i] + ALPHA  # x=1 dense
            if m > T_THRESH:
                S = (ALPHA * TST + v[i] * E[i]) / (ALPHA + v[i])
                th[i] = step_update(th[i], S)
            else:
                no_upd += 1
    dT = np.array([chord(th[i], TST) for i in range(N)])
    dE = np.array([chord(th[i], E[i]) for i in range(N)])
    return dict(mu_v=mu_v, d25T=dT.tolist(), d25E=dE.tolist(),
                no_upd_frac=float(no_upd / tot))

def run_armB(mu_v, gi):
    rng = np.random.RandomState(SEED); ic = rng.dirichlet(np.ones(5), size=N)
    rng2 = np.random.RandomState(SEED + gi); E, v = draw_ev(rng2, mu_v, N)
    rng3 = np.random.RandomState(SEED + 100 + gi)
    th = ic.copy(); imag_upd = 0; tot = 0
    for _ in range(STEPS):
        for i in range(N):
            tot += 1
            x = rng3.binomial(1, 0.5)
            m = v[i] + ALPHA * x
            if m > T_THRESH:
                if x == 1:
                    S = (ALPHA * TST + v[i] * E[i]) / (ALPHA + v[i])
                else:
                    S = E[i]; imag_upd += 1
                th[i] = step_update(th[i], S)
    dT = np.array([chord(th[i], TST) for i in range(N)])
    dE = np.array([chord(th[i], E[i]) for i in range(N)])
    return dict(mu_v=mu_v, d25T=dT.tolist(), d25E=dE.tolist(),
                imag_upd_frac=float(imag_upd / tot))

def run_armCD(mu_v, gi, correlated):
    rng = np.random.RandomState(SEED); ic = rng.dirichlet(np.ones(5), size=N)
    sub = SEED + (200 if correlated else 0) + gi
    rng2 = np.random.RandomState(sub)
    E_all = np.zeros((N, K, 5)); v_all = np.zeros((N, K))
    for i in range(N):
        if correlated:
            Es = rng2.dirichlet(np.ones(5))
            for c in range(K):
                E_all[i, c] = Es; v_all[i, c] = trunc_norm(rng2, mu_v)
        else:
            for c in range(K):
                E_all[i, c] = rng2.dirichlet(np.ones(5)); v_all[i, c] = trunc_norm(rng2, mu_v)
    th = ic.copy()
    for _ in range(STEPS):
        for i in range(N):
            acc = []
            for c in range(K):  # x=1 dense; ungated per-channel threshold
                if v_all[i, c] + ALPHA > T_THRESH:
                    acc.append((ALPHA * TST + v_all[i, c] * E_all[i, c]) / (ALPHA + v_all[i, c]))
            if acc:
                th[i] = step_update(th[i], np.mean(acc, axis=0))
    dT = np.array([chord(th[i], TST) for i in range(N)])
    dEref = E_all[:, 0, :]
    dE = np.array([chord(th[i], dEref[i]) for i in range(N)])
    return dict(mu_v=mu_v, d25T=dT.tolist(), d25E=dE.tolist())

def boot_ci(x, seed=SEED + 999):
    rng = np.random.RandomState(seed); x = np.asarray(x); n = len(x)
    bs = [np.mean(x[rng.randint(0, n, n)]) for _ in range(10000)]
    return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]

out = {"spec": "SIM_G22_PRE_REGISTRATION.md", "seed": SEED, "N": N, "steps": STEPS,
       "lam": LAM, "alpha": ALPHA, "T": T_THRESH, "K": K, "grid": GRID,
       "distance": "Hellinger chord (G6-M1 printed convention)"}

a0 = run_arm0(); out["arm0"] = {k: v for k, v in a0.items() if k != "ic"}
out["arm0"]["d25_ci"] = boot_ci(a0["d25"])
out["armA"] = {}; out["armB"] = {}; out["armC"] = {}; out["armD"] = {}
for gi, mu in enumerate(GRID):
    a = run_armA(mu, gi); out["armA"][str(mu)] = {**{k: v for k, v in a.items() if k not in ("d25T", "d25E")},
        "d25T_mean": float(np.mean(a["d25T"])), "d25T_ci": boot_ci(a["d25T"]),
        "d25E_mean": float(np.mean(a["d25E"])), "d25E_ci": boot_ci(a["d25E"])}
    b = run_armB(mu, gi); out["armB"][str(mu)] = {**{k: v for k, v in b.items() if k not in ("d25T", "d25E")},
        "d25T_mean": float(np.mean(b["d25T"])), "d25E_mean": float(np.mean(b["d25E"]))}
    c = run_armCD(mu, gi, False); out["armC"][str(mu)] = {"d25T_mean": float(np.mean(c["d25T"])),
        "d25T_ci": boot_ci(c["d25T"]), "d25E_mean": float(np.mean(c["d25E"]))}
    d = run_armCD(mu, gi, True); out["armD"][str(mu)] = {"d25T_mean": float(np.mean(d["d25T"])),
        "d25T_ci": boot_ci(d["d25T"]), "d25E_mean": float(np.mean(d["d25E"]))}
    print(f"mu_v={mu:5.2f}  A dT={out['armA'][str(mu)]['d25T_mean']:.4f} noUpd={a['no_upd_frac']:.2f} | "
          f"B dT={out['armB'][str(mu)]['d25T_mean']:.4f} imgUpd={b['imag_upd_frac']:.2f} | "
          f"C dT={out['armC'][str(mu)]['d25T_mean']:.4f} | D dT={out['armD'][str(mu)]['d25T_mean']:.4f}")

# --- frozen evaluation ---
d0 = a0["d0"]; ratio0 = a0["ratio"]
c1 = out["arm0"]["inside7"] == 60
a50 = out["armA"]["5.0"]; a25 = out["armA"]["2.5"]; a125 = out["armA"]["1.25"]
b50 = out["armB"]["5.0"]; c50 = out["armC"]["5.0"]; d50 = out["armD"]["5.0"]
c2 = (a25["d25T_mean"] > 0.05) and (a50["d25T_mean"] > 0.05) and (a50["d25E_mean"] < a50["d25T_mean"])
c3 = (a125["no_upd_frac"] >= 0.5) and (a125["d25T_mean"] > 0.05)
c4 = (b50["imag_upd_frac"] >= 0.10) and (b50["d25E_mean"] < b50["d25T_mean"])
ratioC = c50["d25T_mean"] / d0
c5 = (c50["d25T_mean"] <= 0.05) and (abs(ratioC) <= 1.25 * ratio0)
c6 = d50["d25T_mean"] > 0.05
verdict = {"C1_gate": "PASS" if c1 else "FAIL->INDETERMINATE",
           "C2_corruption": "PASS" if c2 else "FAIL",
           "C3_stagnation": "PASS" if c3 else "FAIL",
           "C4_sparse_hallucination": "PASS" if c4 else "FAIL",
           "C5_aggregation_rescue": "PASS" if c5 else "FAIL",
           "C6_collective_illusion_boundary": "PASS" if c6 else "FAIL"}
verdict["compound"] = "PASS" if (c1 and c2 and c5 and c6) else ("INDETERMINATE" if not c1 else "FAIL")
out["verdict"] = verdict
out["arm0"]["d0"] = d0

dst = "/mnt/agents/output/osf_deposit/technical-appendix/numbers/g22_results.json"
json.dump(out, open(dst, "w"), indent=1)
print("\nVERDICT:", json.dumps(verdict, indent=1))
print("arm0: d0=%.4f d25mean=%.4f ratio=%.4f inside7=%d/60" % (d0, np.mean(a0["d25"]), ratio0, a0["inside7"]))
print("saved:", dst)
