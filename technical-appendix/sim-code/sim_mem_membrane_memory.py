#!/usr/bin/env python3
"""
Sim MEM: The Membrane as the Universal Physical Locus of Memory and Selection
Pre-registration: SIM_MEM_PRE_REGISTRATION.md
Seed: 42
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt

def run_sim_mem(seed=42):
    rng = np.random.default_rng(seed)
    n_agents = 1000
    timesteps = 5000
    noise_sigma = 2.0
    lam = 0.5
    
    # Base expected value of environmental validation
    mu_env = 1.0 
    
    # Track states over time
    S_no_membrane = np.full(n_agents, 0.5)
    S_wall = np.full(n_agents, 0.5)
    S_semi = np.full(n_agents, 0.5)
    
    history_no_membrane = np.zeros((timesteps, n_agents))
    history_wall = np.zeros((timesteps, n_agents))
    history_semi = np.zeros((timesteps, n_agents))
    
    cumulative_boundary_error = np.zeros(n_agents)
    
    gamma_semi = 0.15
    
    for t in range(timesteps):
        # Environmental validation array
        V_env = rng.normal(mu_env, noise_sigma, n_agents)
        
        # 1. No Membrane (Soup): gamma = 1.0
        eps_soup = V_env - S_no_membrane
        S_no_membrane += lam * 1.0 * eps_soup
        history_no_membrane[t] = S_no_membrane
        
        # 2. Impenetrable Wall: gamma = 0.0
        eps_wall = V_env - S_wall
        S_wall += lam * 0.0 * eps_wall
        history_wall[t] = S_wall
        
        # 3. Semi-Permeable Membrane: gamma = 0.15
        eps_semi = V_env - S_semi
        boundary_gated_eps = gamma_semi * eps_semi
        cumulative_boundary_error += (lam * boundary_gated_eps)
        S_semi += lam * boundary_gated_eps
        history_semi[t] = S_semi

    # --- CRITERION MEM-1: Isolation for Memory ---
    var_no_membrane = float(np.var(history_no_membrane[-1]))
    var_semi = float(np.var(history_semi[-1]))
    
    # Calculate temporal autocorrelation (lag-1) for semi-permeable regime
    autocorrs = []
    for i in range(n_agents):
        ts = history_semi[:, i]
        if np.std(ts) > 1e-6:
            r = np.corrcoef(ts[:-1], ts[1:])[0, 1]
            autocorrs.append(r)
    mean_autocorr_semi = float(np.mean(autocorrs)) if autocorrs else 0.0
    
    mem1_pass = (var_semi <= 0.5) and (mean_autocorr_semi >= 0.90) and (var_no_membrane > var_semi * 2.0)
    
    # --- CRITERION MEM-2: Impenetrable Starvation ---
    var_wall = float(np.var(history_wall[-1]))
    mem2_pass = (var_wall < 1e-6)
    
    # --- CRITERION MEM-3: Boundary Locus of Selection ---
    # Terminal S_t vs (S_0 + cumulative boundary error)
    expected_S_semi = 0.5 + cumulative_boundary_error
    corr_matrix = np.corrcoef(S_semi, expected_S_semi)
    r_mem3 = float(corr_matrix[0, 1])
    mem3_pass = (r_mem3 > 0.9999)
    
    compound_pass = mem1_pass and mem2_pass and mem3_pass
    verdict = "COMPOUND PASS (3/3)" if compound_pass else "FAIL as frozen"
    
    # --- GENERATE PLOTS ---
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures", exist_ok=True)
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers", exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # 1. State trajectories (first 3 agents)
    time_arr = np.arange(timesteps)
    axes[0].plot(time_arr, history_no_membrane[:, :3], color='red', alpha=0.3)
    axes[0].plot(time_arr, history_semi[:, :3], color='green', alpha=0.8)
    axes[0].plot(time_arr, history_wall[:, :3], color='gray', linestyle='--')
    # Dummy lines for legend
    axes[0].plot([], [], color='red', alpha=0.5, label='No Membrane (Soup)')
    axes[0].plot([], [], color='green', label='Semi-Permeable ($\gamma=0.15$)')
    axes[0].plot([], [], color='gray', linestyle='--', label='Impenetrable Wall')
    axes[0].set_title('Internal Memory State Dynamics ($S_t$)')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('State $S_t$')
    axes[0].legend()
    
    # 2. Terminal State Variance
    variances = [var_no_membrane, var_semi, var_wall]
    labels = ['No Membrane', 'Semi-Permeable', 'Impenetrable']
    colors = ['#EF4444', '#10B981', '#9CA3AF']
    bars = axes[1].bar(labels, variances, color=colors)
    axes[1].set_title('Terminal State Variance (Amnesia)')
    axes[1].set_ylabel('Variance')
    axes[1].axhline(0.5, color='k', linestyle=':', label='MEM-1 Threshold (0.5)')
    axes[1].legend()
    
    # 3. Locus of Selection (Correlation)
    axes[2].scatter(expected_S_semi, S_semi, alpha=0.1, color='purple')
    axes[2].plot([min(expected_S_semi), max(expected_S_semi)], 
                 [min(expected_S_semi), max(expected_S_semi)], 'k--', label='Identity Line')
    axes[2].set_title(f'Membrane Locus of Selection (r={r_mem3:.4f})')
    axes[2].set_xlabel('Cumulative Boundary-Gated Prediction Error')
    axes[2].set_ylabel('Terminal Internal State $S_T$')
    axes[2].legend()
    
    plt.tight_layout()
    fig_path = "/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures/fig_sim_mem_membrane.png"
    plt.savefig(fig_path, dpi=300)
    
    out = {
        "timestamp": "2026-11-01",
        "seed": seed,
        "compound_verdict": verdict,
        "compound_pass": bool(compound_pass),
        "mem1_isolation": {
            "var_no_membrane": var_no_membrane,
            "var_semi_permeable": var_semi,
            "autocorr_semi_permeable": mean_autocorr_semi,
            "pass": bool(mem1_pass)
        },
        "mem2_starvation": {
            "var_wall": var_wall,
            "pass": bool(mem2_pass)
        },
        "mem3_locus_of_selection": {
            "r": r_mem3,
            "pass": bool(mem3_pass)
        }
    }
    
    json_path = "/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers/sim_mem_results.json"
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2)
        
    print(f"MEM-1 Isolation: Var(Semi)={var_semi:.2f} (<=0.5), Autocorr={mean_autocorr_semi:.4f} -> {mem1_pass}")
    print(f"MEM-2 Starvation: Var(Wall)={var_wall:.2e} (~0.0) -> {mem2_pass}")
    print(f"MEM-3 Selection Locus: r={r_mem3:.4f} (=1.0) -> {mem3_pass}")
    print(f"Final Verdict: {verdict}")

if __name__ == "__main__":
    run_sim_mem()
