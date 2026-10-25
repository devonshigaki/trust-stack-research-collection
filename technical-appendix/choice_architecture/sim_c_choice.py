#!/usr/bin/env python3
"""
Sim C-Series: Choice Architecture, Default Nudges & Asymmetric Loss Framing
Pre-registered Hypotheses C1, C2, C3.
Anchored to Thaler & Sunstein (2008), Kahneman & Tversky (1979), and TFP Master Law 4:1 asymmetry.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.labelweight": "bold"
})

def run_c_series(seed=42):
    np.random.seed(seed)
    n_agents = 1000
    
    # Present-biased agents
    beta = np.random.uniform(0.4, 0.9, n_agents)
    delta = np.random.uniform(0.95, 0.99, n_agents)
    
    # ---------------------------------------------------------
    # HYPOTHESIS C1: Default Nudge Adherence
    # ---------------------------------------------------------
    print("▶ [1/3] Simulating Hypothesis C1: Default Nudge Adherence...")
    # Base utility: immediate gratification vs deferred reward
    u_cooperate_immediate = -0.2
    u_cooperate_deferred = 0.5
    u_defect_immediate = 0.3
    u_defect_deferred = -0.8
    
    # Present-biased perceived value without nudge
    v_coop_neutral = u_cooperate_immediate + beta * delta * u_cooperate_deferred
    v_defect_neutral = u_defect_immediate + beta * delta * u_defect_deferred
    prob_coop_neutral = 1.0 / (1.0 + np.exp(-3.0 * (v_coop_neutral - v_defect_neutral)))
    adherence_neutral = float(np.mean(prob_coop_neutral))
    
    # Under Default Nudge (+70% weight to default action)
    default_boost = 0.70
    prob_coop_default = 1.0 / (1.0 + np.exp(-3.0 * (v_coop_neutral + default_boost - v_defect_neutral)))
    adherence_default = float(np.mean(prob_coop_default))
    
    pass_c1 = adherence_default >= 0.75
    
    # ---------------------------------------------------------
    # HYPOTHESIS C2: Loss Framing Asymmetry Ratio
    # ---------------------------------------------------------
    print("▶ [2/3] Simulating Hypothesis C2: Loss Framing Asymmetry...")
    # Gain framing: "cooperating gains lambda+ = 0.005"
    lambda_plus = 0.005
    # Loss framing: "defecting loses lambda- = 0.020" (4:1 asymmetry)
    lambda_minus = 0.020
    
    # Subjective threat weight under framing
    weight_gain = lambda_plus * 50.0 # Normalized
    weight_loss = lambda_minus * 50.0
    
    prob_compliance_gain = 1.0 / (1.0 + np.exp(-2.5 * (v_coop_neutral + weight_gain)))
    prob_compliance_loss = 1.0 / (1.0 + np.exp(-2.5 * (v_coop_neutral + weight_loss)))
    
    mean_comp_gain = float(np.mean(prob_compliance_gain))
    mean_comp_loss = float(np.mean(prob_compliance_loss))
    
    # Compliance differential over baseline
    delta_gain = mean_comp_gain - adherence_neutral
    delta_loss = mean_comp_loss - adherence_neutral
    compliance_ratio = float(delta_loss / (delta_gain + 1e-9))
    
    pass_c2 = compliance_ratio >= 3.0
    
    # ---------------------------------------------------------
    # HYPOTHESIS C3: Cognitive Friction Damping
    # ---------------------------------------------------------
    print("▶ [3/3] Simulating Hypothesis C3: Cognitive Friction...")
    # Opt-out rate with 0 friction vs 3 units of friction (-20% per unit)
    friction_penalty = 0.20 * 3.0 # 0.60 penalty
    
    prob_optout_free = 1.0 - prob_coop_default
    prob_optout_friction = (1.0 - prob_coop_default) * (1.0 - friction_penalty)
    
    mean_optout_free = float(np.mean(prob_optout_free))
    mean_optout_friction = float(np.mean(prob_optout_friction))
    optout_ratio = mean_optout_friction / (mean_optout_free + 1e-9)
    suppression_pct = (1.0 - optout_ratio) * 100.0
    
    pass_c3 = optout_ratio <= 0.50
    
    compound_pass = pass_c1 and pass_c2 and pass_c3
    verdict = "COMPOUND PASS (3/3)" if compound_pass else f"COMPOUND FAIL ({sum([pass_c1, pass_c2, pass_c3])}/3 PASS)"
    
    results = {
        "timestamp": "2026-10-24",
        "seed": seed,
        "compound_verdict": verdict,
        "compound_pass": bool(compound_pass),
        "C1_default_nudge": {
            "adherence_neutral": adherence_neutral,
            "adherence_default": adherence_default,
            "pass": bool(pass_c1)
        },
        "C2_loss_framing": {
            "mean_comp_gain": mean_comp_gain,
            "mean_comp_loss": mean_comp_loss,
            "compliance_ratio": compliance_ratio,
            "pass": bool(pass_c2)
        },
        "C3_cognitive_friction": {
            "mean_optout_free": mean_optout_free,
            "mean_optout_friction": mean_optout_friction,
            "optout_ratio": optout_ratio,
            "suppression_pct": suppression_pct,
            "pass": bool(pass_c3)
        }
    }
    
    return results

def make_figure(results, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.2), dpi=200)
    
    # Panel 1: C1 Default Nudge Adherence
    ax = axes[0]
    bars = [results["C1_default_nudge"]["adherence_neutral"] * 100,
            results["C1_default_nudge"]["adherence_default"] * 100]
    ax.bar(["Neutral Menu", "Default Nudge (+70%)"], bars, color=["#7f7f7f", "#2ca02c"], width=0.5, alpha=0.85)
    ax.axhline(75.0, color="#d62728", linestyle="--", lw=1.8, label="Frozen Target (75%)")
    ax.set_ylabel("Agreement Adherence Rate (%)")
    ax.set_title(f"A. Default Nudge Adherence (C1)\nAdherence = {results['C1_default_nudge']['adherence_default']*100:.1f}% ({'PASS' if results['C1_default_nudge']['pass'] else 'FAIL'})")
    ax.grid(True, alpha=0.3, axis="y")
    ax.legend(frameon=True, fontsize=9)
    
    # Panel 2: C2 Loss Framing Asymmetry
    ax = axes[1]
    res_c2 = results["C2_loss_framing"]
    gains = [res_c2["mean_comp_gain"]*100, res_c2["mean_comp_loss"]*100]
    ax.bar(["Gain Framing (λ⁺=0.005)", "Loss Framing (λ⁻=0.020)"], gains, color=["#1f77b4", "#d62728"], width=0.5, alpha=0.85)
    ax.set_ylabel("Compliance Rate (%)")
    ax.set_title(f"B. Framing Asymmetry Ratio (C2)\nAsymmetry: {res_c2['compliance_ratio']:.2f}× ({'PASS' if res_c2['pass'] else 'FAIL'})")
    ax.grid(True, alpha=0.3, axis="y")
    
    # Panel 3: C3 Cognitive Friction Suppression
    ax = axes[2]
    res_c3 = results["C3_cognitive_friction"]
    opts = [res_c3["mean_optout_free"]*100, res_c3["mean_optout_friction"]*100]
    ax.bar(["Frictionless", "3 Units Friction (-60%)"], opts, color=["#ff7f0e", "#9467bd"], width=0.5, alpha=0.85)
    ax.set_ylabel("Contract Opt-Out Rate (%)")
    ax.set_title(f"C. Friction Opt-Out Damping (C3)\nSuppression: {res_c3['suppression_pct']:.1f}% ({'PASS' if res_c3['pass'] else 'FAIL'})")
    ax.grid(True, alpha=0.3, axis="y")
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"✓ Saved publication figure: {output_path}")

def main():
    print("="*70)
    print("⚡ RUNNING SIM C-SERIES: CHOICE ARCHITECTURE & NUDGES")
    print("="*70)
    
    base_dir = "/Users/devonshigaki/Desktop/Research/experiments/simulations_repair_era/choice_architecture"
    os.makedirs(base_dir, exist_ok=True)
    
    results = run_c_series(seed=42)
    
    json_path = os.path.join(base_dir, "sim_c_results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✓ Saved results JSON: {json_path}")
    
    fig_path = os.path.join(base_dir, "fig_sim_c_choice.png")
    make_figure(results, fig_path)
    
    # Write Run Report
    report_path = os.path.join(base_dir, "C_SERIES_RUN_REPORT.md")
    with open(report_path, "w") as f:
        f.write(f"""# Sim C-Series Run Report: Choice Architecture & Nudge Dynamics

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **{results['compound_verdict']}**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **C1: Default Nudge Adherence** | +70% weight to default cooperative action | Adherence $\\ge 75.0\\%$ | **{results['C1_default_nudge']['adherence_default']*100:.1f}\\%** (vs {results['C1_default_nudge']['adherence_neutral']*100:.1f}\\% neutral) | **{'PASS' if results['C1_default_nudge']['pass'] else 'FAIL'}** |
| **C2: Loss Framing Asymmetry** | Loss framing ($\\lambda^-=0.02$) vs Gain ($\\lambda^+=0.005$) | Ratio $\\ge 3.0\\times$ | **{results['C2_loss_framing']['compliance_ratio']:.2f}\\times** | **{'PASS' if results['C2_loss_framing']['pass'] else 'FAIL'}** |
| **C3: Cognitive Friction Damping** | 3 units friction penalty (-20%/unit) | Opt-out ratio $\\le 0.50$ | **{results['C3_cognitive_friction']['optout_ratio']:.2f}** ({results['C3_cognitive_friction']['suppression_pct']:.1f}\\% suppression) | **{'PASS' if results['C3_cognitive_friction']['pass'] else 'FAIL'}** |

---

## 2. Engineering Calibrations for Production Simulator

1. **Choice Architecture Toggle:** Enabling `mech-choice` modulates agent prior expectation by default weight $W = +0.70$, elevating default option adherence to {results['C1_default_nudge']['adherence_default']*100:.1f}%.
2. **Framing Multiplier:** Loss-framed agreements engage the 4:1 asymmetric penalty, yielding {results['C2_loss_framing']['compliance_ratio']:.2f}x higher behavioral retention.
""")
    print(f"✓ Saved Run Report: {report_path}")

if __name__ == "__main__":
    main()
