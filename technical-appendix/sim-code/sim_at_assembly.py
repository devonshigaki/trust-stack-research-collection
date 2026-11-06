#!/usr/bin/env python3
import os
import json
import numpy as np
import networkx as nx
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def run_sim_at(seed=42):
    rng = np.random.default_rng(seed)
    N_atoms = 500
    timesteps = 2000  
    
    # Regimes to test
    # 1. Null (Thermodynamic Random Walk)
    # 2. Physics (Base Lambda GTT)
    # 3. Biology (High Lambda GTT)
    
    def simulate_regime(regime_name, use_gtt=False, lam=0.1):
        G = nx.Graph()
        G.add_nodes_from(range(N_atoms))
        
        # Track bond properties if GTT is used
        bond_S = {} # trust state S_t
        bond_lifetime = {}
        
        total_edges_history = []
        max_component_history = []
        
        # Simulation loop
        for t in range(timesteps):
            # Thermal noise (Validation)
            V_t = rng.normal(0, 1.0) 
            
            # 1. Random collisions attempt to form new bonds
            potential_pairs = rng.integers(0, N_atoms, size=(20, 2))
            for u, v in potential_pairs:
                if u != v and not G.has_edge(u, v):
                    G.add_edge(u, v)
                    e = (min(u, v), max(u, v))
                    if use_gtt:
                        # Initial trust state
                        bond_S[e] = 0.5 
                        bond_lifetime[e] = 0
            
            # 2. Existing bonds undergo stress/selection
            edges_to_remove = []
            for u, v in list(G.edges):
                e = (min(u, v), max(u, v))
                if use_gtt:
                    # GTT Update: Delta S = lambda * (V_t - E)
                    # For a bond, E is the expectation of stability (e.g., E = 0.5)
                    # We add some local structural stability (Expectation)
                    deg = G.degree(u) + G.degree(v)
                    E_t = 0.5 + (0.01 * deg)
                    
                    # Compute prediction error
                    eps = V_t - E_t
                    
                    # Update trust state
                    if e not in bond_S:
                        bond_S[e] = 0.5
                        bond_lifetime[e] = 0
                    
                    bond_S[e] += lam * eps
                    
                    # Selection
                    if bond_S[e] <= 0:
                        edges_to_remove.append((u, v))
                    else:
                        bond_lifetime[e] += 1
                else:
                    # Null Regime: pure random chance of breaking (thermal decay)
                    if rng.random() < 0.15: # Base decay rate
                        edges_to_remove.append((u, v))
                        
            G.remove_edges_from(edges_to_remove)
            if use_gtt:
                for u, v in edges_to_remove:
                    e = (min(u, v), max(u, v))
                    if e in bond_S: del bond_S[e]
            
            # Metrics
            total_edges_history.append(G.number_of_edges())
            if G.number_of_edges() > 0:
                max_comp = max(len(c) for c in nx.connected_components(G))
            else:
                max_comp = 1
            max_component_history.append(max_comp)
            
        return {
            "name": regime_name,
            "G": G,
            "bond_S": bond_S if use_gtt else None,
            "bond_lifetime": bond_lifetime if use_gtt else None,
            "total_edges": total_edges_history,
            "max_component": max_component_history
        }

    # Execute Regimes
    null_res = simulate_regime("Null", use_gtt=False)
    phys_res = simulate_regime("Physics (Base GTT)", use_gtt=True, lam=0.05)
    bio_res = simulate_regime("Biology (High GTT)", use_gtt=True, lam=0.25)
    
    # --- Compute Frozen Criteria ---
    
    # AT-1: Complexity Acceleration
    c_max_gtt = phys_res["max_component"][-1]
    c_max_null = null_res["max_component"][-1]
    c_max_ratio = c_max_gtt / c_max_null
    at1_pass = c_max_ratio >= 5.0
    
    # AT-2: Selection Equivalency
    S_vals = []
    lifetimes = []
    for u, v in phys_res["G"].edges:
        e = (min(u, v), max(u, v))
        if e in phys_res["bond_S"]:
            S_vals.append(phys_res["bond_S"][e])
            lifetimes.append(phys_res["bond_lifetime"][e])
    
    if len(S_vals) > 2:
        r, p_val = pearsonr(S_vals, lifetimes)
    else:
        r, p_val = 0.0, 1.0
    at2_pass = (r >= 0.90) and (p_val < 0.001)
    
    # AT-3: Biological Amplifier
    e_total_bio = bio_res["total_edges"][-1]
    e_total_phys = phys_res["total_edges"][-1]
    # To prevent div by zero
    e_total_phys_safe = max(e_total_phys, 1)
    amplifier_ratio = e_total_bio / e_total_phys_safe
    at3_pass = amplifier_ratio >= 2.0
    
    compound_pass = at1_pass and at2_pass and at3_pass
    verdict = "COMPOUND PASS (3/3)" if compound_pass else "FAIL as frozen"
    
    # --- Generate Figure ---
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures", exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 1. Complexity (Max Component Size)
    axes[0].plot(null_res["max_component"], label="Null (Random)")
    axes[0].plot(phys_res["max_component"], label="GTT (Physics)")
    axes[0].plot(bio_res["max_component"], label="GTT (Biology)")
    axes[0].set_title("Complexity: Max Component Size")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Nodes in Largest Graph")
    axes[0].legend()
    
    # 2. Selection Equivalency (S_t vs Lifetime)
    if len(S_vals) > 0:
        axes[1].scatter(S_vals, lifetimes, alpha=0.5, color="purple")
        axes[1].set_title(f"Selection Equivalency (r={r:.3f})")
        axes[1].set_xlabel("Bond Trust State $S_t$")
        axes[1].set_ylabel("Survival Lifetime (epochs)")
    
    # 3. Total Edges (Amplifier)
    axes[2].plot(null_res["total_edges"], label="Null")
    axes[2].plot(phys_res["total_edges"], label=r"Physics ($\lambda=0.05$)")
    axes[2].plot(bio_res["total_edges"], label=r"Biology ($\lambda=0.25$)")
    axes[2].set_title(f"Selection Amplifier (Ratio: {amplifier_ratio:.2f}x)")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("Total Sustained Bonds")
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures/fig_sim_at_assembly.png", dpi=300)
    
    # --- Save JSON ---
    out = {
        "timestamp": "2026-11-01",
        "seed": seed,
        "compound_verdict": verdict,
        "at1_complexity": {
            "c_max_gtt": c_max_gtt,
            "c_max_null": c_max_null,
            "ratio": c_max_ratio,
            "pass": bool(at1_pass)
        },
        "at2_selection": {
            "r": r,
            "p_val": p_val,
            "pass": bool(at2_pass)
        },
        "at3_amplifier": {
            "e_total_bio": e_total_bio,
            "e_total_phys": e_total_phys,
            "ratio": amplifier_ratio,
            "pass": bool(at3_pass)
        }
    }
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers", exist_ok=True)
    with open("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers/sim_at_results.json", "w") as f:
        json.dump(out, f, indent=2)
        
    print(f"AT-1 Complexity Ratio: {c_max_ratio:.2f} (>= 5.0) -> {at1_pass}")
    print(f"AT-2 Selection r: {r:.4f} (>= 0.90) -> {at2_pass}")
    print(f"AT-3 Amplifier Ratio: {amplifier_ratio:.2f} (>= 2.0) -> {at3_pass}")
    print(f"Verdict: {verdict}")

if __name__ == "__main__":
    run_sim_at()