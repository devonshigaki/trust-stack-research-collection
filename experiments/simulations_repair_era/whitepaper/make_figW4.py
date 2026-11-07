"""figW4_adoption_compounding.png — Sim W-map 4 (W4): adoption compounding with
densification feedback.

Model (documented in numbers_whitepaper.md, W4):
    dA/dt = h0(1-A)q + g0 q A(1-A) - c0 (1-q) A
    q(A)  = exp(-t_dec(A)/tau)
    t_dec = time-to-first-decisionable-score from the W3 cold-start engine at
            event rate r(A) = r_floor + kappa*A
    h0 = 0.05/yr, g0 = 1.2/yr, c0 = 0.6/yr, tau = 0.5 yr, A0 = 1%.

t_dec is tabulated from the printed W3 re-run (seed 42) anchor days
(numbers_whitepaper.md W3 table) with log-log interpolation:
    0.01/d -> 563 d, 0.05 -> 144, 0.1 -> 140, 0.5 -> 120, 1 -> 72, 5 -> 24.
Below 0.01/day the engine trap dominates; the last printed leg is extrapolated.

Repair note: the original layout placed the panel-(b) legend at 'upper left'
with ylim (0,1), where the densification-alone trajectory (r=0, k=5) ran
through the legend box and struck through its last entry. The axes headroom is
raised to ylim (0,1.3) so the legend stays in curve-free space, and the
colorbar is offset with pad so its label clears panel (b)'s ylabel.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else "figW4_adoption_compounding.png"

# ---- W3 cold-start engine anchor table (printed re-run, seed 42) ----
ANCH_R = np.array([0.01, 0.05, 0.1, 0.5, 1.0, 5.0])      # events/day
ANCH_T = np.array([563.0, 144.0, 140.0, 120.0, 72.0, 24.0])  # days
EXTRAP_P = np.log(ANCH_T[0] / ANCH_T[1]) / np.log(ANCH_R[1] / ANCH_R[0])


def t_dec_years(r):
    """Time to first decisionable score (years) at organic event rate r/day."""
    r = np.asarray(r, dtype=float)
    out = np.full_like(r, np.inf)
    pos = r > 0
    lr = np.log(r[pos])
    t = np.exp(np.interp(lr, np.log(ANCH_R), np.log(ANCH_T),
                         left=np.nan, right=np.nan))
    below = r[pos] < ANCH_R[0]
    t[below] = ANCH_T[0] * (r[pos][below] / ANCH_R[0]) ** (-EXTRAP_P)
    above = r[pos] > ANCH_R[-1]
    # beyond 5/day the engine is decisionable in well under a month; hold 24 d
    t[above] = ANCH_T[-1]
    out[pos] = t / 365.0
    return out


# ---- W4 adoption ODE ----
H0, G0, C0, TAU, A0 = 0.05, 1.2, 0.6, 0.5, 0.01
YEARS = 10.0
DT = 0.002


def q_of(A, r_floor, kappa):
    td = np.atleast_1d(t_dec_years(r_floor + kappa * A))
    q = np.exp(-td / TAU)
    q[~np.isfinite(td)] = 0.0
    return q if q.size > 1 else q[0]


def trajectory(r_floor, kappa):
    ts = np.arange(0.0, YEARS + DT, DT)
    A = np.empty_like(ts)
    A[0] = A0
    for i in range(1, len(ts)):
        a = A[i - 1]
        q = float(q_of(a, r_floor, kappa))
        dA = H0 * (1 - a) * q + G0 * q * a * (1 - a) - C0 * (1 - q) * a
        A[i] = a + dA * DT
    return ts, A


# ---- (a) heatmap over (floor x kappa) ----
floors = np.logspace(-3, np.log10(3.0), 46)
kappas = np.linspace(0.0, 5.0, 41)
Z = np.empty((len(kappas), len(floors)))
for iy, k in enumerate(kappas):
    for ix, f in enumerate(floors):
        Z[iy, ix] = trajectory(f, k)[1][-1]

fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2))
ax = axes[0]
pc = ax.pcolormesh(floors, kappas, Z, cmap="RdYlGn", vmin=0.0, vmax=1.0,
                   shading="auto")
ax.set_xscale("log")
ax.set_xlabel("organic event floor (events/day, log)", fontsize=9)
ax.set_ylabel("densification $\\kappa$\n(events/day per adopted fraction)",
              fontsize=9)
ax.set_title("(a) Adopted fraction after 10 yr vs (floor, $\\kappa$)\n"
             "stalls at low-both; exact trap at (0,0)", fontsize=10)
cs = ax.contour(floors, kappas, Z, levels=[0.2], colors="red", linewidths=1.5)
cs2 = ax.contour(floors, kappas, Z, levels=[0.8], colors="darkgreen",
                 linewidths=1.5)
ax.clabel(cs2, fmt={0.8: "compounds A*=0.8"}, fontsize=8)
ax.grid(alpha=0.3)

# ---- (b) representative trajectories ----
axb = axes[1]
arms = [
    (0.0, 0.0, "r=0, $\\kappa$=0 — trap (collapse)", "darkred"),
    (0.001, 0.2, "r=0.001, $\\kappa$=0.2 — stalls", "red"),
    (0.01, 1.0, "r=0.01, $\\kappa$=1 — partial/slow", "orange"),
    (0.1, 2.0, "r=0.1, $\\kappa$=2 — compounds", "green"),
    (0.0, 5.0, "r=0, $\\kappa$=5 — densification alone bootstraps "
     "(off 1% initial cohort)", "teal"),
]
for f, k, lab, col in arms:
    ts, A = trajectory(f, k)
    axb.plot(ts, A, color=col, lw=2.2, label=lab)
axb.set_xlabel("years", fontsize=9)
axb.set_ylabel("adopted fraction A(t)", fontsize=9)
axb.set_title("(b) Representative trajectories\n"
              "(h0=0.05, g0=1.2, churn=0.6 /yr; patience 0.5 yr; A0=1%)",
              fontsize=10)
axb.set_ylim(0, 1.3)
axb.set_xlim(0, 10)
# repaired: the original 'upper left' legend at ylim (0,1) was struck through
# by the k=5 densification arm; the axes headroom is raised to ylim (0,1.3) so
# the legend sits in curve-free space above the trajectories.
axb.legend(loc="upper left", fontsize=8, framealpha=1.0)
axb.grid(alpha=0.2)

cb = fig.colorbar(pc, ax=axes[0], label="adopted fraction, year 10", pad=0.14)
cb.ax.tick_params(labelsize=8)
cb.set_label("adopted fraction, year 10", fontsize=9)

fig.suptitle("Sim W-map 4 — Adoption compounding with densification feedback: "
             "where it holds vs stalls (seed 42)", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(OUT, dpi=150)
print("saved", OUT)

# ---- region sanity printout (must match caption regions) ----
def Astar(f, k):
    return trajectory(f, k)[1][-1]
print("trap (0,0):", Astar(0.0, 0.0))
print("stall (0.01,0.5):", Astar(0.01, 0.5))
print("compound (0.1,0):", Astar(0.1, 0.0))
print("compound (0,2):", Astar(0.0, 2.0))
print("dens-only (0,5):", Astar(0.0, 5.0))
