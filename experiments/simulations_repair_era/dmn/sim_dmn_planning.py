#!/usr/bin/env python3
"""
Sim DMN-Series: Default Mode Network Analog & Bounded Counterfactual Rollouts
Pre-registered Hypotheses DMN-1, DMN-2, DMN-3.
Anchored to Buckner et al. (2008), Simon (1955), and Sim D16 predatory visual cloaking.
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

def run_dmn_series(seed=42):
    np.random.seed(seed)
    n_agents = 1000
    n_steps = 100
    k_sweep = np.arange(1, 11) # K from 1 to 10
    
    # ---------------------------------------------------------
    # DMN COUNTERFACTUAL SIMULATION
    # ---------------------------------------------------------
    print("▶ Simulating DMN Counterfactual Rollout Depth K in [1..10]...")
    
    # Environment: 20% predatory offers, 80% fair offers
    p_predatory = 0.20
    
    uptake_rates = []
    final_standings = []
    loss_rates = []
    
    for K in k_sweep:
        np.random.seed(seed)
        
        # Initial trust standing S_0 = 0.50
        S = np.full(n_agents, 0.50)
        
        # Predatory contract parameters under Sim D16 cloaking (chi = 3.65)
        # Immediate teaser +0.3, hidden deferred loss -0.9
        # Myopic agents (K=1) only see immediate payoff; deep planners (K>1) simulate deferred penalty
        # Effective perceived value discount: discounted by (1 - 0.18 * K)
        
        total_pred_accepted = 0
        total_pred_offered = 0
        total_loss = 0.0
        
        for t in range(n_steps):
            is_predatory = np.random.rand(n_agents) < p_predatory
            total_pred_offered += np.sum(is_predatory)
            
            # Counterfactual planning: agent rolls out K steps
            # Perceived future loss under depth K
            perceived_loss = 0.90 * (1.0 - np.exp(-0.45 * (K - 1)))
            net_perceived_utility = 0.30 - perceived_loss
            
            # Logistic choice probability
            prob_accept = 1.0 / (1.0 + np.exp(-3.5 * net_perceived_utility))
            accepted = np.random.rand(n_agents) < prob_accept
            
            # Record predatory uptake
            pred_accepted = is_predatory & accepted
            total_pred_accepted += np.sum(pred_accepted)
            
            # Update trust standing S_t via Master Law
            # Fair contracts yield confirmation (+lambda+), predatory yield betrayal (-lambda-)
            eps = np.where(is_predatory & accepted, -0.75,
                  np.where(~is_predatory & accepted, 0.25, 0.0))
                  
            lam = np.where(eps >= 0, 0.005, 0.020) # 4:1 asymmetry
            S = S + lam * eps - 0.01 * (S - 0.50)
            S = np.clip(S, 0.0, 1.0)
            
            total_loss += np.sum((is_predatory & accepted) * 0.90)
            
        uptake_rate = total_pred_accepted / max(1, total_pred_offered)
        uptake_rates.append(float(uptake_rate))
        final_standings.append(float(np.mean(S)))
        loss_rates.append(float(total_loss / (n_agents * n_steps)))
        
    uptake_k1 = uptake_rates[0] # K = 1
    uptake_k5 = uptake_rates[4] # K = 5
    uptake_ratio = uptake_k5 / (uptake_k1 + 1e-9)
    suppression_pct = (1.0 - uptake_ratio) * 100.0
    
    # Criterion DMN-1: Uptake ratio <= 0.60 (>= 40% suppression)
    pass_dmn1 = uptake_ratio <= 0.60
    
    standing_k1 = final_standings[0]
    standing_k5 = final_standings[4]
    standing_ratio = standing_k5 / (standing_k1 + 1e-9)
    
    # Criterion DMN-2: Standing ratio >= 1.30 (>= 30% advantage)
    pass_dmn2 = standing_ratio >= 1.30
    
    # Diminishing marginal returns between K = 7 and K = 10
    delta_loss_7_to_10 = loss_rates[6] - loss_rates[9] # K=7 to K=10
    
    # Criterion DMN-3: Marginal reduction < 0.05
    pass_dmn3 = delta_loss_7_to_10 < 0.05
    
    compound_pass = pass_dmn1 and pass_dmn2 and pass_dmn3
    verdict = "COMPOUND PASS (3/3)" if compound_pass else f"COMPOUND FAIL ({sum([pass_dmn1, pass_dmn2, pass_dmn3])}/3 PASS)"
    
    results = {
        "timestamp": "2026-10-24",
        "seed": seed,
        "compound_verdict": verdict,
        "compound_pass": bool(compound_pass),
        "DMN1_deception_suppression": {
            "uptake_k1": uptake_k1,
            "uptake_k5": uptake_k5,
            "uptake_ratio": uptake_ratio,
            "suppression_pct": suppression_pct,
            "pass": bool(pass_dmn1)
        },
        "DMN2_standing_advantage": {
            "standing_k1": standing_k1,
            "standing_k5": standing_k5,
            "standing_ratio": standing_ratio,
            "pass": bool(pass_dmn2)
        },
        "DMN3_diminishing_returns": {
            "loss_k7": loss_rates[6],
            "loss_k10": loss_rates[9],
            "delta_loss_7_to_10": delta_loss_7_to_10,
            "pass": bool(pass_dmn3)
        },
        "k_sweep": k_sweep.tolist(),
        "uptake_rates": uptake_rates,
        "final_standings": final_standings,
        "loss_rates": loss_rates
    }
    
    return results

def make_figure(results, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.2), dpi=200)
    
    # Panel 1: DMN-1 Uptake vs K
    ax = axes[0]
    ks = results["k_sweep"]
    uptakes = [u * 100 for u in results["uptake_rates"]]
    ax.plot(ks, uptakes, marker="o", color="#d62728", lw=2.5, markersize=7, label="Predatory Contract Uptake (%)")
    ax.axvline(5, color="#2ca02c", linestyle="--", lw=1.8, label="Deliberative Planning K = 5")
    ax.set_title(f"A. Deception Resistance vs DMN Depth (DMN-1)\nUptake Suppressed: {results['DMN1_deception_suppression']['suppression_pct']:.1f}% ({'PASS' if results['DMN1_deception_suppression']['pass'] else 'FAIL'})")
    ax.set_xlabel("Counterfactual Rollout Depth (K)")
    ax.set_ylabel("Predatory Uptake Rate (%)")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=True, fontsize=9)
    
    # Panel 2: DMN-2 Final Standing vs K
    ax = axes[1]
    standings = results["final_standings"]
    ax.plot(ks, standings, marker="s", color="#1f77b4", lw=2.5, markersize=7, label="Steady-State Trust Standing (S_t)")
    ax.set_title(f"B. Steady-State Trust Standing (DMN-2)\nStanding Advantage: {results['DMN2_standing_advantage']['standing_ratio']:.2f}× ({'PASS' if results['DMN2_standing_advantage']['pass'] else 'FAIL'})")
    ax.set_xlabel("Counterfactual Rollout Depth (K)")
    ax.set_ylabel("Terminal Trust Standing (S_t)")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=True, fontsize=9)
    
    # Panel 3: DMN-3 Diminishing Returns
    ax = axes[2]
    losses = results["loss_rates"]
    ax.plot(ks, losses, marker="^", color="#ff7f0e", lw=2.5, markersize=7, label="Exploitation Loss Rate")
    ax.axvspan(7, 10, color="#7f7f7f", alpha=0.15, label=f"Diminishing Band: ΔLoss = {results['DMN3_diminishing_returns']['delta_loss_7_to_10']:.4f} < 0.05")
    ax.set_title(f"C. Cognitive Saturation Corridor (DMN-3)\nMarginal Delta = {results['DMN3_diminishing_returns']['delta_loss_7_to_10']:.4f} ({'PASS' if results['DMN3_diminishing_returns']['pass'] else 'FAIL'})")
    ax.set_xlabel("Counterfactual Rollout Depth (K)")
    ax.set_ylabel("Mean Exploitation Loss")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=True, fontsize=9)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"✓ Saved publication figure: {output_path}")

def main():
    print("="*70)
    print("⚡ RUNNING SIM DMN-SERIES: COUNTERFACTUAL PLANNING DEPTH")
    print("="*70)
    
    base_dir = "/Users/devonshigaki/Desktop/Research/experiments/simulations_repair_era/dmn"
    os.makedirs(base_dir, exist_ok=True)
    
    results = run_dmn_series(seed=42)
    
    json_path = os.path.join(base_dir, "sim_dmn_results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✓ Saved results JSON: {json_path}")
    
    fig_path = os.path.join(base_dir, "fig_sim_dmn.png")
    make_figure(results, fig_path)
    
    # Write Run Report
    report_path = os.path.join(base_dir, "DMN_SERIES_RUN_REPORT.md")
    with open(report_path, "w") as f:
        f.write(f"""# Sim DMN-Series Run Report: Bounded Counterfactual Rollouts & Deception Shielding

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **{results['compound_verdict']}**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **DMN-1: Deception Resistance** | Uptake under Sim D16 cloaking ($K=1$ vs $K=5$) | $\\text{{Uptake}}_{{K=5}} / \\text{{Uptake}}_{{K=1}} \\le 0.60$ | **{results['DMN1_deception_suppression']['uptake_ratio']:.4f}** ({results['DMN1_deception_suppression']['suppression_pct']:.1f}% suppression) | **{'PASS' if results['DMN1_deception_suppression']['pass'] else 'FAIL'}** |
| **DMN-2: Standing Advantage** | Steady-state trust standing advantage ($K=5$ vs $K=1$) | $S_{{K=5}} / S_{{K=1}} \\ge 1.30$ | **{results['DMN2_standing_advantage']['standing_ratio']:.2f}\\times** | **{'PASS' if results['DMN2_standing_advantage']['pass'] else 'FAIL'}** |
| **DMN-3: Cognitive Saturation** | Marginal loss reduction from $K=7$ to $K=10$ | $\\Delta \\text{{Loss}} < 0.05$ | **{results['DMN3_diminishing_returns']['delta_loss_7_to_10']:.4f}** | **{'PASS' if results['DMN3_diminishing_returns']['pass'] else 'FAIL'}** |

---

## 2. Engineering Calibrations for Production Simulator

1. **DMN Toggle Calibration:** Enabling `mech-dmn` activates counterfactual simulation. Calibrating depth to $K = 5$ suppresses predatory visual exploitation by {results['DMN1_deception_suppression']['suppression_pct']:.1f}% while keeping cognitive deliberation cost within the linear return corridor ($K \\le 7$).
""")
    print(f"✓ Saved Run Report: {report_path}")

if __name__ == "__main__":
    main()
