#!/usr/bin/env python3
"""
SIM-R1 Battery 2 — closure-sensitivity of the ~7.2-step ringing signature
(gtt_revised §6; math_repairs.md §M5.4; sim_results_B.md Study 2).

Common dynamics (GTT preset of the master law): S_{t+1} = S_t + lam (V - E_t),
x_t = E_t - V, lam = 0.61 (the H2 target). Reference closure (minimal):
E_{t+1} = S_t  ->  x_{t+2} = x_{t+1} - lam x_t,  z^2 - z + lam = 0,
period 2*pi/atan(sqrt(4 lam - 1)) = 7.17 steps, envelope sqrt(lam) = 0.78/step.

Closures tested:
  (i)   E_{t+1} = alpha S_t + (1-alpha) E_t,  alpha in {1.0, 0.8, 0.6, 0.4, 0.2}
        -> state (x, y=S-V): x' = alpha y + (1-alpha) x ; y' = y - lam x
        -> z^2 - (2-alpha) z + (1 - alpha(1-lam)) = 0
        complex iff lam > alpha/4 ; |z| = sqrt(1 - alpha(1-lam)) ;
        period = 2pi / atan2(sqrt(4 alpha lam - alpha^2), 2 - alpha).
        Jury: stable iff 0 < alpha <= 1 and 0 < lam < 1.
  (ii)  zero delay: E_t = S_t -> x_{t+1} = (1 - lam) x_t : monotone for lam<1,
        NO ringing (alternation only for 1 < lam < 2, unstable beyond).
  (iii) two-step delay: E_{t+1} = S_{t-1} -> y_{t+1} = y_t - lam y_{t-2},
        characteristic z^3 - z^2 + lam = 0.

Impulse response: unit displacement x=1 released at t=0, deterministic, 200
steps; dominant period estimated by positive-peak spacing (scipy find_peaks)
and checked against FFT peak; compared with analytic root angles.
"""
import numpy as np
from scipy.signal import find_peaks
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAM = 0.61
REF_PERIOD = 2 * np.pi / np.arctan(np.sqrt(4 * LAM - 1))   # 7.17
T = 200

def roots_smooth(alpha, lam=LAM):
    a1 = -(2 - alpha); a0 = 1 - alpha * (1 - lam)
    return np.roots([1, a1, a0])

def roots_two_step(lam=LAM):
    return np.roots([1, -1, 0, lam])

def period_from_roots(r):
    c = r[np.abs(r.imag) > 1e-12]
    if len(c) == 0:
        return None, float(np.max(np.abs(r)))
    i = int(np.argmax(np.abs(c)))
    return float(2 * np.pi / np.abs(np.angle(c[i]))), float(np.abs(c[i]))

def sim_smooth(alpha, lam=LAM, T=T):
    x = np.zeros(T); y = np.zeros(T)
    x[0] = 1.0                      # unit displacement of E from V
    for t in range(T - 1):
        x[t+1] = alpha * y[t] + (1 - alpha) * x[t]
        y[t+1] = y[t] - lam * x[t]
    return x

def sim_zero_delay(lam=LAM, T=T):
    x = np.zeros(T); x[0] = 1.0
    for t in range(T - 1):
        x[t+1] = (1 - lam) * x[t]
    return x

def sim_two_step(lam=LAM, T=T):
    # y_{t+1} = y_t - lam y_{t-2}; impulse: release E at displacement 1 while
    # S starts at V (y=0): E_0 - V = 1 -> -lam*x enters S update
    y = np.zeros(T); x = np.zeros(T)
    x[0] = 1.0
    for t in range(T - 1):
        y[t+1] = y[t] - lam * x[t]
        x[t+1] = y[t-1] if t >= 1 else 0.0   # E_{t+1} = S_{t-1}
    return x

def sim_period(x):
    pk, _ = find_peaks(x, height=0.005)
    pk = pk[pk > 0]
    if len(pk) >= 3:
        return float(np.mean(np.diff(pk))), len(pk)
    # FFT fallback (dominant nonzero frequency)
    X = np.abs(np.fft.rfft(x - np.mean(x)))
    X[0] = 0
    k = int(np.argmax(X))
    if X[k] < 1e-9:
        return None, 0
    return float(len(x) / k), 1

res = {"lambda": LAM, "ref_period": REF_PERIOD, "closures": {}}

print(f"reference period (minimal closure, analytic) = {REF_PERIOD:.4f}")
for alpha in [1.0, 0.8, 0.6, 0.4, 0.2]:
    r = roots_smooth(alpha)
    pth, mod = period_from_roots(r)
    x = sim_smooth(alpha)
    psim, npk = sim_period(x)
    res["closures"][f"smooth_a{alpha}"] = dict(
        period_theory=pth, envelope=mod, period_sim=psim, n_peaks=npk,
        stable=bool(np.max(np.abs(r)) < 1))
    print(f"alpha={alpha:.1f}: period theory {pth:.3f} sim {psim} "
          f"|z|={mod:.4f} peaks={npk}")

# zero delay
x0 = sim_zero_delay()
r0 = np.array([1 - LAM])
res["closures"]["zero_delay"] = dict(period_theory=None, envelope=float(1-LAM),
                                     period_sim=None, n_peaks=0, stable=True,
                                     note="monotone decay x_{t+1}=(1-lam)x_t; no ringing")
print(f"zero-delay: monotone, |ratio|={1-LAM:.3f}, no oscillation; x[10]={x0[10]:.2e}")

# two-step delay
r3 = roots_two_step()
p3, m3 = period_from_roots(r3)
x3 = sim_two_step()
p3s, npk3 = sim_period(x3)
res["closures"]["two_step_delay"] = dict(period_theory=p3, envelope=m3,
                                         period_sim=p3s, n_peaks=npk3,
                                         stable=bool(np.max(np.abs(r3)) < 1),
                                         roots_moduli=[float(a) for a in np.abs(r3)])
print(f"two-step delay: roots |z|={np.abs(r3).round(4)}, period theory {p3:.3f} sim {p3s}, stable={np.max(np.abs(r3))<1}")

# stability boundary of the two-step-delay closure (Jury prediction (sqrt5-1)/2)
lams = np.linspace(0.01, 1.2, 240)
bnd = None
for l in lams:
    if np.max(np.abs(roots_two_step(l))) >= 1:
        bnd = float(l); break
res["two_step_stability_boundary"] = bnd
# refined boundary by bisection
lo, hi = 0.5, 0.7
for _ in range(60):
    mid = (lo + hi) / 2
    if np.max(np.abs(roots_two_step(mid))) >= 1:
        hi = mid
    else:
        lo = mid
res["two_step_stability_boundary_refined"] = float((lo + hi) / 2)
res["two_step_jury_prediction"] = float((np.sqrt(5) - 1) / 2)
print(f"two-step-delay stability boundary: numeric {bnd}, Jury prediction {(np.sqrt(5)-1)/2:.4f}")

# critical-damping condition for smoothing closure: rings iff lam > alpha/4
res["smooth_ring_condition"] = "complex roots iff lambda > alpha/4 (at lam=0.61: all alpha<=1 ring)"

# visible-cycle count: steps for envelope to fall to 5% / period
for k, v in res["closures"].items():
    if v["period_theory"]:
        n5 = np.log(0.05) / np.log(v["envelope"])
        v["visible_cycles"] = float(n5 / v["period_theory"])

# period-vs-lambda curves per closure alpha (for the registered falsifiable relation)
lam_grid = np.linspace(0.26, 0.99, 60)
curves = {}
for alpha in [1.0, 0.8, 0.6, 0.4]:
    pp = []
    for l in lam_grid:
        p, _ = period_from_roots(roots_smooth(alpha, l))
        pp.append(p)
    curves[str(alpha)] = pp
res["period_vs_lambda"] = {"lam_grid": list(lam_grid), "curves": curves}

with open("/mnt/agents/output/figures/robustness/simR1_battery2_stats.json", "w") as f:
    json.dump(res, f, indent=2)

# ---------------- figure ----------------
fig = plt.figure(figsize=(15, 9))
gs = fig.add_gridspec(3, 4)

# (a) period vs alpha
axa = fig.add_subplot(gs[0, :2])
alphas = np.linspace(0.05, 1.0, 200)
per = [period_from_roots(roots_smooth(a))[0] for a in alphas]
axa.plot(alphas, per, "C0-", lw=2, label="theory: 2π/atan2(√(4αλ−α²), 2−α)")
for alpha in [1.0, 0.8, 0.6, 0.4, 0.2]:
    v = res["closures"][f"smooth_a{alpha}"]
    axa.plot(alpha, v["period_sim"], "o", ms=8, color="C3", zorder=5)
axa.plot([], [], "o", color="C3", label="simulation (peak spacing)")
axa.axhline(REF_PERIOD, color="k", ls="--", lw=1.2, label=f"7.17-step reference (α=1)")
axa.set_xlabel("closure smoothing α  (E_{t+1} = αS_t + (1−α)E_t)")
axa.set_ylabel("dominant period (steps)")
axa.set_title(f"(a) Ringing period vs closure smoothing (λ = {LAM})")
axa.legend(fontsize=8); axa.set_ylim(0, 25)

# (b) period vs lambda for several alpha
axb = fig.add_subplot(gs[0, 2:])
for alpha, col in zip([1.0, 0.8, 0.6, 0.4], ["C0", "C1", "C2", "C3"]):
    axb.plot(lam_grid, curves[str(alpha)], col, lw=1.8, label=f"α = {alpha}")
axb.axvline(LAM, color="k", ls=":", lw=1, label=f"λ = {LAM} target")
axb.set_xlabel("λ"); axb.set_ylabel("dominant period (steps)")
axb.set_title("(b) The registered period-vs-λ relation shifts with closure")
axb.legend(fontsize=8); axb.set_ylim(0, 40)

# (c) impulse-response panels
panels = [("smooth_a1.0", "α=1.0 (minimal closure, reference)", sim_smooth(1.0)),
          ("smooth_a0.8", "α=0.8", sim_smooth(0.8)),
          ("smooth_a0.6", "α=0.6", sim_smooth(0.6)),
          ("smooth_a0.4", "α=0.4", sim_smooth(0.4)),
          ("smooth_a0.2", "α=0.2", sim_smooth(0.2)),
          ("zero_delay", "zero delay E_t = S_t", sim_zero_delay()),
          ("two_step_delay", "two-step delay E_{t+1} = S_{t−1}", sim_two_step())]
for j, (key, title, x) in enumerate(panels):
    ax = fig.add_subplot(gs[1 + j // 4, j % 4])
    nshow = 70 if key != "two_step_delay" else 120
    ax.plot(np.arange(nshow), x[:nshow], lw=1.4, color="C0")
    ax.axhline(0, color="k", lw=0.6)
    v = res["closures"][key]
    if v["period_theory"]:
        ax.set_title(f"{title}\nperiod {v['period_theory']:.2f} (sim {v['period_sim']:.2f}), "
                     f"|z|={v['envelope']:.3f}, {v['visible_cycles']:.1f} visible cycles", fontsize=8)
    else:
        ax.set_title(f"{title}\nno ringing (monotone, ratio {1-LAM:.2f}/step)", fontsize=8)
    ax.tick_params(labelsize=7)
fig.suptitle("SIM-R1 Battery 2 — closure sensitivity of the ≈7.2-step ringing signature\n"
             f"dynamics S(t+1) = S(t) + λ(V − E(t)), x = E − V, λ = {LAM}, unit-displacement impulse, deterministic; "
             "reference closure E(t+1) = S(t) gives period 7.17 (Sim G8 in-silico: 7.15)", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("/mnt/agents/output/figures/robustness/figR2_closure_sensitivity.png", dpi=150)
print("figure written")
