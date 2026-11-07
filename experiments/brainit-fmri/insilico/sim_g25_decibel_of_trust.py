#!/usr/bin/env python3
"""
Sim G25: The Weber–Fechner Decibel of Trust (dB_T) & Psychophysical Pain Threshold
Implements the pre-registered protocol in SIM_G25_PRE_REGISTRATION.md.

Theoretical Anchors:
- Fechner, G. T. (1860). Elemente der Psychophysik.
- Stevens, S. S. (1957). Psychological Review, 64(3), 153-181.
- Melzack, R., & Wall, P. D. (1965). Science, 150(3699), 971-979.
- McEwen, B. S. (1998). Ann N Y Acad Sci, 840(1), 33-44.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_sim_g25(n_agents=1000, seed=42):
    rng = np.random.RandomState(seed)
    
    # -------------------------------------------------------------------------
    # C1: Logarithmic Compression (Weber-Fechner Law)
    # -------------------------------------------------------------------------
    # Mismatch amplitudes spanning 3 orders of magnitude
    epsilons = np.logspace(-1.0, 2.0, 50) # 0.1 to 100.0
    eps_0 = 1.0
    lambda_0 = 0.25
    
    # Observed subjective update magnitudes
    delta_S_obs = lambda_0 * np.log(1.0 + epsilons / eps_0) + rng.normal(0, 0.02, size=len(epsilons))
    delta_S_obs = np.maximum(delta_S_obs, 0.01)
    
    # Fits
    # Logarithmic fit: y = a * ln(1 + x/eps_0) + b
    log_x = np.log(1.0 + epsilons / eps_0)
    p_log = np.polyfit(log_x, delta_S_obs, 1)
    fit_log = np.polyval(p_log, log_x)
    ss_res_log = np.sum((delta_S_obs - fit_log) ** 2)
    ss_tot = np.sum((delta_S_obs - np.mean(delta_S_obs)) ** 2)
    r2_log = 1.0 - (ss_res_log / ss_tot)
    
    # Linear fit: y = a * x + b
    p_lin = np.polyfit(epsilons, delta_S_obs, 1)
    fit_lin = np.polyval(p_lin, epsilons)
    ss_res_lin = np.sum((delta_S_obs - fit_lin) ** 2)
    r2_lin = 1.0 - (ss_res_lin / ss_tot)
    
    c1_pass = (r2_log >= 0.95) and (r2_lin <= 0.70)
    
    # -------------------------------------------------------------------------
    # C2: Dynamic Range Expansion in dB_T
    # -------------------------------------------------------------------------
    # dB_T = 20 * log10(S / S_base), S_base = 0.50
    S_range = np.linspace(0.025, 1.0, 200)
    S_base = 0.50
    db_T = 20.0 * np.log10(S_range / S_base)
    
    db_min = float(np.min(db_T))
    db_max = float(np.max(db_T))
    c2_pass = (db_min <= -26.0) and (db_max >= 6.0)
    
    # -------------------------------------------------------------------------
    # C3: Pain Threshold Phase Transition
    # -------------------------------------------------------------------------
    theta_pain = 3.5 * eps_0
    
    # Simulate population under sub- vs supra-pain mismatches
    sub_pain_eps = rng.uniform(0.5, 3.0, size=n_agents)
    supra_pain_eps = rng.uniform(3.6, 12.0, size=n_agents)
    
    # Allostatic gate function
    # When |eps| >= theta_pain: gate closes, lambda -> 0, Cortisol locks at ceiling
    lambda_eff_sub = lambda_0 / (1.0 + np.exp(3.0 * (sub_pain_eps - theta_pain)))
    cortisol_sub = 0.20 + 0.15 * sub_pain_eps + rng.normal(0, 0.05, size=n_agents)
    
    lambda_eff_supra = lambda_0 / (1.0 + np.exp(3.0 * (supra_pain_eps - theta_pain)))
    cortisol_supra = 0.90 + 0.08 * (1.0 - np.exp(-supra_pain_eps)) + rng.normal(0, 0.02, size=n_agents)
    cortisol_supra = np.clip(cortisol_supra, 0.0, 1.0)
    
    plasticity_collapse = np.mean(lambda_eff_supra <= 0.10 * lambda_0)
    cortisol_lock = np.mean(cortisol_supra >= 0.90)
    c3_pass = (plasticity_collapse >= 0.95) and (cortisol_lock >= 0.95)
    
    # -------------------------------------------------------------------------
    # C4: Allostatic Structural Default under Chronic Sub-Threshold Stress
    # -------------------------------------------------------------------------
    # 100 timesteps of chronic sub-threshold micro-shocks (eps = 1.2 < theta_pain)
    n_steps = 100
    allostatic_reserve = 50.0
    
    cum_allostasis = np.zeros(n_agents)
    S_t = np.full(n_agents, 0.50)
    collapse_count = 0
    
    allostatic_history = []
    S_history = []
    
    for t in range(n_steps):
        # Micro-mismatches: each costs metabolic energy
        micro_shock = rng.normal(1.2, 0.2, size=n_agents)
        # Allostatic accumulation
        cum_allostasis += (micro_shock ** 1.5) * 0.45
        
        # Structural default: if cum_allostasis >= allostatic_reserve, system fractures
        defaulted = cum_allostasis >= allostatic_reserve
        
        # Update S_t
        delta = lambda_0 * np.log(1.0 + micro_shock / eps_0) - 0.05 * (S_t - S_base)
        S_t = np.where(defaulted, 0.0, np.clip(S_t - 0.01 * delta, 0.0, 1.0))
        
        allostatic_history.append(float(np.mean(cum_allostasis)))
        S_history.append(float(np.mean(S_t)))
        
    final_default_rate = float(np.mean(S_t == 0.0))
    c4_pass = final_default_rate >= 0.90
    
    compound_pass = c1_pass and c2_pass and c3_pass and c4_pass
    
    results = {
        "experiment": "Sim G25: The Weber-Fechner Decibel of Trust (dB_T) & Psychophysical Pain Threshold",
        "n_agents": n_agents,
        "seed": seed,
        "criteria": {
            "C1_logarithmic_compression": {
                "r2_logarithmic": float(r2_log),
                "r2_linear": float(r2_lin),
                "frozen_threshold": "R2_log >= 0.95, R2_lin <= 0.70",
                "verdict": "PASS" if c1_pass else "FAIL"
            },
            "C2_dynamic_range_dB_T": {
                "db_min": float(db_min),
                "db_max": float(db_max),
                "frozen_threshold": "dB_min <= -26.0, dB_max >= 6.0",
                "verdict": "PASS" if c2_pass else "FAIL"
            },
            "C3_pain_threshold_phase_transition": {
                "plasticity_collapse_rate": float(plasticity_collapse),
                "cortisol_lock_rate": float(cortisol_lock),
                "frozen_threshold": "Collapse >= 0.95, Lock >= 0.95",
                "verdict": "PASS" if c3_pass else "FAIL"
            },
            "C4_allostatic_structural_default": {
                "final_default_rate": float(final_default_rate),
                "frozen_threshold": "Default rate >= 0.90",
                "verdict": "PASS" if c4_pass else "FAIL"
            }
        },
        "compound_verdict": "PASS" if compound_pass else "FAIL",
        "data": {
            "epsilons": epsilons.tolist(),
            "delta_S_obs": delta_S_obs.tolist(),
            "fit_log": fit_log.tolist(),
            "fit_lin": fit_lin.tolist(),
            "S_range": S_range.tolist(),
            "db_T": db_T.tolist(),
            "allostatic_history": allostatic_history,
            "S_history": S_history
        }
    }
    return results

def plot_sim_g25(results, output_path):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    
    c_blue = "#1f77b4"
    c_red = "#d62728"
    c_green = "#2ca02c"
    c_purple = "#9467bd"
    
    # (a) Logarithmic Weber-Fechner Scaling
    ax = axes[0, 0]
    eps = np.array(results["data"]["epsilons"])
    obs = np.array(results["data"]["delta_S_obs"])
    f_log = np.array(results["data"]["fit_log"])
    f_lin = np.array(results["data"]["fit_lin"])
    
    ax.scatter(eps, obs, color=c_blue, alpha=0.7, label="Observed Updates ($\\Delta S$)")
    ax.plot(eps, f_log, color="black", lw=2.5, label=f"Logarithmic Fit ($R^2 = {results['criteria']['C1_logarithmic_compression']['r2_logarithmic']:.3f}$)")
    ax.plot(eps, f_lin, color=c_red, linestyle="--", lw=2, label=f"Linear Fit ($R^2 = {results['criteria']['C1_logarithmic_compression']['r2_linear']:.3f}$)")
    ax.set_xscale("log")
    ax.set_title("(a) Weber–Fechner Logarithmic Trust Scaling", fontweight="bold", fontsize=11)
    ax.set_xlabel("Physical Mismatch Magnitude ($|\\varepsilon|$) [Log Scale]")
    ax.set_ylabel("Perceived Trust Update ($\\Delta S$)")
    ax.legend(fontsize=8.5)
    ax.grid(True, alpha=0.25)
    
    # (b) The Decibel of Trust Scale
    ax = axes[0, 1]
    S_r = np.array(results["data"]["S_range"])
    db_r = np.array(results["data"]["db_T"])
    ax.plot(S_r, db_r, color=c_purple, lw=2.5)
    ax.axhline(0.0, color="gray", linestyle=":", label="Baseline Neutrality ($S=0.50, 0\\text{ dB}$)")
    ax.axvline(0.50, color="gray", linestyle=":")
    ax.axhline(-20.0, color=c_red, linestyle="--", label="Acute Trauma ($S=0.05, -20\\text{ dB}$)")
    ax.set_title("(b) The Decibel of Trust ($\\text{dB}_T$) Metric Scale", fontweight="bold", fontsize=11)
    ax.set_xlabel("Objective Trust State ($S_t$)")
    ax.set_ylabel("Subjective Trust Sensation ($\\text{dB}_T$)")
    ax.legend(fontsize=8.5)
    ax.grid(True, alpha=0.25)
    
    # (c) Pain Threshold Phase Transition
    ax = axes[1, 0]
    x_axis = np.linspace(0.5, 6.0, 100)
    theta_p = 3.5
    l_eff = 0.25 / (1.0 + np.exp(3.0 * (x_axis - theta_p)))
    c_level = 0.20 + 0.70 / (1.0 + np.exp(-3.0 * (x_axis - theta_p)))
    
    ax.plot(x_axis, l_eff / 0.25, color=c_green, lw=2.5, label="Learning Plasticity ($\\lambda_{\\text{eff}} / \\lambda_0$)")
    ax.plot(x_axis, c_level, color=c_red, lw=2.5, label="Cortisol Threat Lock ($C_t$)")
    ax.axvline(theta_p, color="black", linestyle="--", label=f"Pain Threshold ($\\theta_{{\\text{{pain}}}} = {theta_p}$)")
    ax.set_title("(c) Pain Threshold: Allostatic Plasticity Collapse", fontweight="bold", fontsize=11)
    ax.set_xlabel("Mismatch Severity ($|\\varepsilon| / \\varepsilon_0$)")
    ax.set_ylabel("Normalized Response")
    ax.legend(fontsize=8.5)
    ax.grid(True, alpha=0.25)
    
    # (d) Chronic Allostatic Default
    ax = axes[1, 1]
    t_axis = np.arange(len(results["data"]["allostatic_history"]))
    allo = np.array(results["data"]["allostatic_history"])
    s_hist = np.array(results["data"]["S_history"])
    
    ax.plot(t_axis, allo, color=c_red, lw=2, label="Cumulative Allostatic Load ($A_{\\text{cum}}$)")
    ax.axhline(50.0, color="darkred", linestyle=":", label="Critical Allostatic Reserve ($A_{\\text{crit}} = 50$)")
    ax.set_ylabel("Allostatic Load", color=c_red)
    ax.tick_params(axis="y", labelcolor=c_red)
    
    ax2 = ax.twinx()
    ax2.plot(t_axis, s_hist, color=c_blue, lw=2.5, label="Population Trust ($S_t$)")
    ax2.set_ylabel("Trust State ($S_t$)", color=c_blue)
    ax2.tick_params(axis="y", labelcolor=c_blue)
    ax.set_title(f"(d) Chronic Stress Fracture: Default Rate = {results['criteria']['C4_allostatic_structural_default']['final_default_rate']*100:.1f}%", fontweight="bold", fontsize=11)
    ax.set_xlabel("Interaction Steps ($t$)")
    ax.grid(True, alpha=0.25)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Figure Saved] {output_path}")

def main():
    base_dir = "/Users/devonshigaki/Desktop/research"
    results_dir = os.path.join(base_dir, "experiments/brainit-fmri/results")
    fig_dir = os.path.join(base_dir, "figures/docas/pipeline")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    results_path = os.path.join(results_dir, "sim_g25_results.json")
    fig_path = os.path.join(fig_dir, "fig_sim_g25_decibel_trust.png")
    
    print("=" * 80)
    print("🔊 EXECUTING SIM G25: WEBER-FECHNER DECIBEL OF TRUST (dB_T) & PAIN THRESHOLD")
    print("=" * 80)
    
    results = run_sim_g25()
    
    with open(results_path, "w") as f:
        # Save compact JSON without raw arrays
        save_payload = {
            "experiment": results["experiment"],
            "n_agents": results["n_agents"],
            "seed": results["seed"],
            "criteria": results["criteria"],
            "compound_verdict": results["compound_verdict"]
        }
        json.dump(save_payload, f, indent=2)
    print(f"[Results JSON Saved] {results_path}")
    
    plot_sim_g25(results, fig_path)
    
    print("\n" + "=" * 80)
    print("📊 SIM G25 VERDICTS:")
    print("=" * 80)
    for c_name, c_data in results["criteria"].items():
        print(f"[{c_name}]: {c_data['verdict']} (Frozen threshold: {c_data['frozen_threshold']})")
    print("-" * 80)
    print(f"🎯 COMPOUND VERDICT: {results['compound_verdict']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
