#!/usr/bin/env python3
"""SIM-R1 Battery 1 figures (150 dpi, captioned)."""
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "/mnt/agents/output/figures/robustness/"
z = np.load(D + "simR1_battery1_rows.npz")
s = json.load(open(D + "simR1_battery1_stats.json"))

# ---------- figR1_error_distributions.png ----------
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
bins = np.linspace(0, 0.6, 61)
a = np.abs(z["A_err"]); b_bar = np.abs(z["B_err_bar"]); b_w = np.abs(z["B_err_w"])
ax[0].hist(a, bins=bins, alpha=0.75, density=True,
           label=f"constant-λ truth (arm A): mean {a.mean():.4f}, p95 {np.percentile(a,95):.4f}, max {a.max():.4f}")
ax[0].hist(b_bar, bins=bins, alpha=0.65, density=True,
           label=f"adaptive-λ truth vs time-avg λ̄ (arm B): mean {b_bar.mean():.3f}, p95 {np.percentile(b_bar,95):.3f}, max {b_bar.max():.3f}")
ax[0].hist(b_w, bins=bins, alpha=0.55, density=True,
           label=f"adaptive-λ truth vs ε²-weighted λ̄_w: mean {b_w.mean():.4f}, p95 {np.percentile(b_w,95):.4f}")
ax[0].axvline(0.15, color="k", ls="--", lw=1.2, label="certified tolerance 0.15")
ax[0].set_xlabel("|λ̂ − λ_target|"); ax[0].set_ylabel("density")
ax[0].set_title("(a) Recovery-error distributions"); ax[0].legend(fontsize=7.5)

signed = z["B_err_bar"]
bins2 = np.linspace(-0.15, 0.65, 81)
ax[1].hist(signed, bins=bins2, color="C1", alpha=0.8, density=True)
ax[1].axvline(0, color="k", lw=1); ax[1].axvline(signed.mean(), color="r", ls="--",
        label=f"mean signed error +{signed.mean():.3f} (upward bias)")
ax[1].set_xlabel("λ̂ − λ̄  (signed, adaptive truth)"); ax[1].set_ylabel("density")
ax[1].set_title("(b) Constant-λ estimator is biased UP\nunder volatility-linked gain"); ax[1].legend(fontsize=8)

cs = [0.75, 1.5, 3.0]
bias = [s["c_scan"][str(c)]["pop_mean_hat"] - s["c_scan"][str(c)]["pop_mean_true"] for c in cs]
frac = [s["c_scan"][str(c)]["vs_timeavg"]["frac_gt_015"] for c in cs]
ax[2].plot(cs, bias, "o-", color="C3", label="population bias: mean λ̂ − mean λ̄")
ax[2].set_xlabel("volatility coupling c  (λ_t = λ₀(1+c·ν_t))"); ax[2].set_ylabel("bias in λ")
ax2 = ax[2].twinx()
ax2.plot(cs, frac, "s--", color="C4", label="fraction of users |err| > 0.15")
ax2.set_ylabel("fraction outside corridor", color="C4"); ax2.tick_params(axis="y", labelcolor="C4")
ax[2].axhline(0.15, color="k", ls=":", lw=1, label="0.15 corridor half-width")
ax[2].set_title("(c) Misspecification bias scales\nwith gain volatility")
h1,l1 = ax[2].get_legend_handles_labels(); ax[2].legend(h1, l1, fontsize=8, loc="upper left")
fig.suptitle("SIM-R1 Battery 1 — constant-λ Kalman/EM estimator under adaptive-λ (Behrens-style) ground truth\n"
             "N=300 users, Poisson cadence 0.3–3/day × 365 days (median 596 events), Student-t(4) obs noise, "
             "λ_t = λ₀(1+cν_t), ν_t = 0.9ν_{t−1}+0.1(|ε_t|/m_a−1), λ₀~U[0.15,0.55] (λ̄≈0.35), c=1.5, seed 42",
             fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(D + "figR1_error_distributions.png", dpi=150)
plt.close(fig)

# ---------- figR1_scatter_adaptive.png ----------
fig, ax = plt.subplots(1, 2, figsize=(12, 5.4))
lb, lw, lh = z["B_lam_bar"], z["B_lam_bar_w"], z["B_lam_hat"]
ax[0].scatter(lb, lh, s=14, alpha=0.6, color="C1", label="λ̂ vs time-average λ̄  (the misspecified target)")
ax[0].scatter(lw, lh, s=14, alpha=0.6, color="C0", label="λ̂ vs ε²-weighted λ̄_w  (what the estimator identifies)")
lims = [0.1, 1.0]
ax[0].plot(lims, lims, "k-", lw=1)
ax[0].fill_between(lims, [x-0.15 for x in lims], [x+0.15 for x in lims], color="k", alpha=0.08,
                   label="±0.15 corridor")
ax[0].set_xlabel("true gain (per user)"); ax[0].set_ylabel("constant-λ estimate λ̂")
ax[0].set_title("(a) Estimated vs true λ under adaptive truth\n(pop. mean λ̂ = %.3f vs time-avg λ̄ = %.3f)"
                % (lh.mean(), lb.mean()))
ax[0].legend(fontsize=8, loc="upper left"); ax[0].set_xlim(lims); ax[0].set_ylim(lims)

ax[1].scatter(z["C_lamp_hat"], z["C_lamm_hat"], s=14, alpha=0.6, color="C3",
              label=f"asymmetric truth λ⁻=2λ⁺ (arm C): ratio {np.mean(z['C_ratio']):.2f} "
                    f"[p05 {np.percentile(z['C_ratio'],5):.2f}, p95 {np.percentile(z['C_ratio'],95):.2f}]")
ax[1].scatter(z["C_lamp_true"], z["C_lamm_true"], s=10, alpha=0.35, color="k", marker="x",
              label="time-average truth (arm C)")
ax[1].scatter(z["C_lamp_true_w"], z["C_lamm_true_w"], s=10, alpha=0.5, color="C0", marker="+",
              label="ε²-weighted truth (arm C)")
ths = np.linspace(0, 1.5, 10)
ax[1].plot(ths, ths, "k--", lw=1, label="ratio 1 (symmetric)")
ax[1].plot(ths, 2*ths, "k:", lw=1.2, label="ratio 2 (planted)")
ax[1].scatter(z["D_lamp_hat"], z["D_lamm_hat"], s=14, alpha=0.6, color="C2",
              label=f"symmetric adaptive control (arm D): ratio {np.mean(z['D_ratio']):.2f} "
              f"[p95 {np.percentile(z['D_ratio'],95):.2f}] — spurious asymmetry")
ax[1].set_xlabel("λ̂⁺ (build gain)"); ax[1].set_ylabel("λ̂⁻ (break gain)")
ax[1].set_title(f"(b) Two-gain estimator: asymmetry detected but inflated\n(ratio AUC vs symmetric control = {s['CD_ratio_AUC']:.3f})")
ax[1].legend(fontsize=7.5, loc="upper left")
fig.suptitle("SIM-R1 Battery 1 — what the constant-gain estimator actually identifies under gain adaptation",
             fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(D + "figR1_scatter_adaptive.png", dpi=150)
plt.close(fig)
print("figures written")
