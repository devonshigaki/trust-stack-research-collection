#!/usr/bin/env python3
"""
Sim N-Series: Non-Dualism, Markov Blanket Dissolution & Machiavellian Exploitation
Implements the pre-registered protocol in SIM_N_PRE_REGISTRATION.md.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_sim_n(n_agents=1000, n_steps=200, seed=42):
    rng = np.random.RandomState(seed)
    
    results = {}
    
    # --- C1: Metabolic Resilience (Cortisol Accumulation) ---
    # Agent Types: 0 = Non-Dual (mu_B = 0.1), 1 = Standard (mu_B = 0.9)
    # Machiavellian attacks are constant negative prediction errors (eps = -1.0)
    mu_B_non_dual = 0.1
    mu_B_standard = 0.9
    
    # Cortisol response scales with the thickness of the Markov blanket (dualism)
    # C_response = mu_B * |eps|
    attacks = np.full(n_steps, -1.0)
    
    load_non_dual = np.sum(mu_B_non_dual * np.abs(attacks))
    load_standard = np.sum(mu_B_standard * np.abs(attacks))
    
    c1_ratio = load_non_dual / load_standard
    c1_pass = c1_ratio <= 0.400
    
    # --- C2: Evolutionary Stable Strategy (Density Limit) ---
    # Simulate survival in mixed population under resource scarcity
    # Payoff matrix: Machiavelli exploits Non-Dual. Non-Dual share with Non-Dual.
    # Scarcity implies high death rate if payoff is low.
    densities = np.linspace(0.05, 0.95, 20)
    extinction_rates_low = []
    survival_high = []
    
    for rho in densities:
        n_nd = int(rho * 100)
        n_mach = 100 - n_nd
        
        # Simple replicator dynamics proxy
        payoff_nd = rho * 1.5 + (1 - rho) * (-0.5)
        payoff_mach = rho * 2.0 + (1 - rho) * 0.0
        
        if payoff_nd < 0:
            extinction_rate = 1.0 # Collapse
        else:
            extinction_rate = 0.0
            
        if rho < 0.25:
            extinction_rates_low.append(extinction_rate)
        elif rho >= 0.40:
            survival_high.append(payoff_nd > payoff_mach)
            
    c2_extinction_mean = np.mean(extinction_rates_low)
    c2_survival_mean = np.mean(survival_high) if survival_high else 0.0
    c2_pass = (c2_extinction_mean > 0.90) and (c2_survival_mean == 1.0)
    
    # --- C3: Equanimity Attractor ---
    # Non-dual agents internalize external states, leading to S_t -> 0.5
    s_t = 0.9 # Start high
    s_history = []
    for _ in range(n_steps):
        # eps_t is perceived as 0 due to blanket dissolution
        eps_t = 0.0
        s_t = s_t + 0.1 * eps_t - 0.05 * (s_t - 0.5) # Decay to center
        s_t += rng.normal(0, 0.01) # Small internal noise
        s_history.append(s_t)
        
    s_var = np.var(s_history[100:])
    s_mean = np.mean(s_history[100:])
    c3_pass = (np.abs(s_mean - 0.50) < 0.05) and (s_var <= 0.05)
    
    compound_pass = c1_pass and c2_pass and c3_pass
    
    results = {
        "experiment": "Sim N-Series: Non-Dualism & Markov Blanket Dissolution",
        "criteria": {
            "C1_metabolic_resilience": {
                "ratio": float(c1_ratio),
                "frozen_threshold": "<= 0.400",
                "verdict": "PASS" if c1_pass else "FAIL"
            },
            "C2_ess_density_limit": {
                "collapse_low_density": float(c2_extinction_mean),
                "survive_high_density": float(c2_survival_mean),
                "frozen_threshold": "Collapse <0.25, Survive >=0.40",
                "verdict": "PASS" if c2_pass else "FAIL"
            },
            "C3_equanimity_attractor": {
                "variance": float(s_var),
                "mean": float(s_mean),
                "frozen_threshold": "var <= 0.05, mean ~0.5",
                "verdict": "PASS" if c3_pass else "FAIL"
            }
        },
        "compound_verdict": "PASS" if compound_pass else "FAIL",
        "data": {
            "s_history": s_history,
            "densities": densities.tolist(),
            "payoffs_nd": [(r * 1.5 + (1-r)*(-0.5)) for r in densities],
            "payoffs_mach": [(r * 2.0 + (1-r)*0.0) for r in densities]
        }
    }
    return results

def plot_sim_n(results, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # C1
    axes[0].bar(["Non-Dual", "Standard/Machiavellian"], [0.1, 0.9], color=["blue", "red"])
    axes[0].set_title("(a) Cumulative Allostatic Load (Cortisol)")
    axes[0].set_ylabel("Metabolic Cost")
    
    # C2
    d = results["data"]["densities"]
    p_nd = results["data"]["payoffs_nd"]
    p_mach = results["data"]["payoffs_mach"]
    axes[1].plot(d, p_nd, label="Non-Dual", color="blue")
    axes[1].plot(d, p_mach, label="Machiavellian", color="red")
    axes[1].axvline(0.25, color='gray', linestyle='--', label="Collapse Threshold")
    axes[1].axvline(0.40, color='black', linestyle=':', label="ESS Threshold")
    axes[1].set_title("(b) Evolutionary Payoff vs Density")
    axes[1].set_xlabel("Initial Non-Dual Density ($\\rho$)")
    axes[1].legend()
    
    # C3
    axes[2].plot(results["data"]["s_history"], color="purple")
    axes[2].axhline(0.5, color='gray', linestyle='--')
    axes[2].set_title("(c) Equanimity Attractor ($S_t \\to 0.5$)")
    axes[2].set_xlabel("Time Step")
    axes[2].set_ylabel("Trust State ($S_t$)")
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    results = run_sim_n()
    base_dir = "/Users/devonshigaki/Desktop/research"
    results_path = os.path.join(base_dir, "experiments/brainit-fmri/results/sim_n_results.json")
    fig_path = os.path.join(base_dir, "figures/docas/pipeline/fig_sim_n_non_dualism.png")
    
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
        
    plot_sim_n(results, fig_path)
    print("Sim N Complete. Verdict:", results["compound_verdict"])
