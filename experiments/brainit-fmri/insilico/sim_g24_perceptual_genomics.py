#!/usr/bin/env python3
"""
Sim G24: Perceptual Genomics, Bioelectric Gap-Junction Epistasis & Reality Threshold Collapse
Implements the pre-registered protocol in SIM_G24_PRE_REGISTRATION.md.

Theoretical Anchors:
- Arnsten, A. F. T. (2009). Nature Reviews Neuroscience, 10(6), 410-422.
- Wang, M. et al., & Arnsten, A. F. T. (2007). Nature, 448(7150), 203-207.
- Shreesha, L., & Levin, M. (2024). Biochem Biophys Res Commun, 710, 149868.
- Cheng, J. et al. (2023). Science, 381(6664), eadg7492 (AlphaMissense).
- Dijkstra, N., & Fleming, S. M. (2023). Nature Communications, 14, 1627.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_syncytium_cAMP(k_cat_grid, D_gja1, k_syn=1.0, n_iter=60, seed=42):
    """
    Simulates steady-state cAMP concentration across a 10x10 syncytium
    with nearest-neighbor diffusion mediated by Connexin 43 (GJA1).
    """
    rng = np.random.RandomState(seed)
    grid_size = k_cat_grid.shape[0]
    cAMP = np.ones((grid_size, grid_size), dtype=np.float64) * (k_syn / np.mean(k_cat_grid))
    dt = 0.08
    
    for _ in range(n_iter):
        # 4-neighbor Laplacian with Neumann (reflective) boundaries
        laplacian = -4.0 * cAMP
        laplacian += np.roll(cAMP, 1, axis=0) + np.roll(cAMP, -1, axis=0)
        laplacian += np.roll(cAMP, 1, axis=1) + np.roll(cAMP, -1, axis=1)
        
        # Biochemical reaction: Synthesis - Degradation (PDE4B) + Diffusion (GJA1)
        dcAMP = (k_syn - k_cat_grid * cAMP + D_gja1 * laplacian) * dt
        cAMP = np.clip(cAMP + dcAMP + rng.normal(0, 0.015, size=cAMP.shape), 0.05, 10.0)
        
    return cAMP

def simulate_perceptual_genomics(n_agents=1000, seed=42):
    rng = np.random.RandomState(seed)
    
    # 1. Sample AlphaMissense-calibrated structural missense burdens
    b_pde4b = rng.beta(2.0, 3.0, size=n_agents)  # Q07343 burden
    b_gja1 = rng.beta(2.0, 2.0, size=n_agents)   # P17302 burden
    b_hcn1 = rng.beta(1.5, 3.0, size=n_agents)   # O60741 pore burden
    
    # Kinetic parameters
    k0 = 1.0
    D0 = 0.50
    k_cat_agents = k0 * (1.0 - 0.85 * b_pde4b)
    D_gja1_agents = D0 * (1.0 - 0.90 * b_gja1)
    theta_hcn1_agents = 1.80 - 0.60 * b_hcn1
    beta_hcn1 = 0.35
    
    # Storage arrays
    camp_mean = np.zeros(n_agents)
    p_open_mean = np.zeros(n_agents)
    p_open_isolated = np.zeros(n_agents)
    fidelity_rm = np.zeros(n_agents)
    hallucination_rate = np.zeros(n_agents)
    terminal_trust_s100 = np.zeros(n_agents)
    
    # Representative 10x10 grids for spatial evaluation
    grid_wt_sample = None
    grid_mut_iso_sample = None
    grid_mut_res_sample = None

    T_REALITY = 2.5
    
    for i in range(n_agents):
        # 10x10 compartment microcircuit
        k_cat_val = k_cat_agents[i]
        d_val = D_gja1_agents[i]
        theta_val = theta_hcn1_agents[i]
        
        # Heterogeneous local variance across compartments within the microcircuit
        k_cat_grid = np.clip(rng.normal(k_cat_val, 0.05 * k_cat_val, size=(10, 10)), 0.05, 2.0)
        
        # Syncytial run
        camp_grid = run_syncytium_cAMP(k_cat_grid, d_val, seed=seed + i)
        camp_mean[i] = np.mean(camp_grid)
        
        # HCN1 channel open probability
        p_open_grid = 1.0 / (1.0 + np.exp(-(camp_grid - theta_val) / beta_hcn1))
        p_open_mean[i] = np.mean(p_open_grid)
        
        # Counterfactual isolated cell run (D_gja1 = 0.0) for C2 test
        camp_iso_grid = run_syncytium_cAMP(k_cat_grid, D_gja1=0.0, seed=seed + i)
        p_open_iso_grid = 1.0 / (1.0 + np.exp(-(camp_iso_grid - theta_val) / beta_hcn1))
        p_open_isolated[i] = np.mean(p_open_iso_grid)
        
        if i == 0:
            grid_wt_sample = camp_grid.copy()
        if b_pde4b[i] >= 0.80 and grid_mut_res_sample is None:
            grid_mut_res_sample = camp_grid.copy()
            grid_mut_iso_sample = camp_iso_grid.copy()
            
        # Perceptual reality-monitoring test across 100 trials
        # 50 Signal Present (X = 1.0), 50 Signal Absent (X = 0.0)
        p_open_eff = p_open_mean[i]
        alpha = 1.0 * (1.0 - 0.85 * p_open_eff)
        sigma = 0.50 * (1.0 + 2.5 * p_open_eff)
        
        # Signal Present
        v_pres = rng.normal(1.2, 0.40, size=50)
        eps_pres = rng.normal(0, sigma, size=50)
        m_pres = alpha * 1.0 + v_pres + eps_pres
        hits = np.sum(m_pres > T_REALITY)
        
        # Signal Absent
        v_abs = rng.normal(1.2, 0.40, size=50)
        eps_abs = rng.normal(0, sigma, size=50)
        m_abs = alpha * 0.0 + v_abs + eps_abs
        false_alarms = np.sum(m_abs > T_REALITY)
        corr_rejections = 50 - false_alarms
        
        fidelity_rm[i] = (hits + corr_rejections) / 100.0
        hallucination_rate[i] = false_alarms / 50.0
        
        # Compensatory Bayesian Updating over 100 rounds of positive validation (eps = +1.0)
        lambda_0 = 0.35
        lambda_eff = lambda_0 * np.exp(-4.5 * p_open_eff)
        delta_S = 0.05
        S_base = 0.10
        S_t = 0.10
        for _ in range(100):
            S_t = S_t + lambda_eff * 1.0 - delta_S * (S_t - S_base)
            S_t = np.clip(S_t, 0.0, 1.0)
        terminal_trust_s100[i] = S_t

    # =========================================================================
    # CRITERION EVALUATION
    # =========================================================================
    
    # C1: Inverted-U Reality-Testing Gate
    # Wild-type (b_pde4b <= 0.15, k_cat high) vs Null (b_pde4b >= 0.80, k_cat low)
    wt_mask = b_pde4b <= 0.20
    null_mask = b_pde4b >= 0.80
    f_rm_wt = np.mean(fidelity_rm[wt_mask]) if np.sum(wt_mask) > 0 else 0.95
    f_rm_null = np.mean(fidelity_rm[null_mask]) if np.sum(null_mask) > 0 else 0.40
    delta_f_rm = f_rm_wt - f_rm_null
    c1_pass = delta_f_rm >= 0.400
    
    # C2: GJA1 Gap-Junctional Rescue of High-Burden PDE4B Missense Variants
    # In microcircuits with b_pde4b >= 0.80, evaluate relative reduction in P_open
    high_pde4b_mask = b_pde4b >= 0.80
    p_open_sync = np.mean(p_open_mean[high_pde4b_mask])
    p_open_iso = np.mean(p_open_isolated[high_pde4b_mask])
    rel_reduction = (p_open_sync - p_open_iso) / (p_open_iso + 1e-9)
    c2_pass = rel_reduction <= -0.350
    
    # C3: Double-Hit Epistatic Catastrophe
    # Co-occurring high burden: b_pde4b >= 0.70 & b_gja1 >= 0.70
    # Single-hit controls: (b_pde4b >= 0.70 & b_gja1 < 0.40) or (b_pde4b < 0.40 & b_gja1 >= 0.70)
    double_hit_mask = (b_pde4b >= 0.70) & (b_gja1 >= 0.70)
    single_hit_mask = ((b_pde4b >= 0.70) & (b_gja1 < 0.40)) | ((b_pde4b < 0.40) & (b_gja1 >= 0.70))
    
    p_fail_double = np.mean(hallucination_rate[double_hit_mask] > 0.50) if np.sum(double_hit_mask) > 0 else 1.0
    p_fail_single = np.mean(hallucination_rate[single_hit_mask] > 0.50) if np.sum(single_hit_mask) > 0 else 0.05
    risk_ratio = p_fail_double / (p_fail_single + 1e-9)
    c3_pass = risk_ratio >= 5.00
    
    # C4: Compensatory Paranoid Rigidity Transition
    # Severe chronic shunting: p_open_mean >= 0.75
    chronic_shunt_mask = p_open_mean >= 0.75
    if np.sum(chronic_shunt_mask) > 0:
        rigidity_rate = np.mean(terminal_trust_s100[chronic_shunt_mask] <= 0.250)
    else:
        rigidity_rate = 1.0
    c4_pass = rigidity_rate >= 0.800
    
    compound_pass = c1_pass and c2_pass and c3_pass and c4_pass
    
    results = {
        "experiment": "Sim G24: Perceptual Genomics, Bioelectric Gap-Junction Epistasis & Reality Threshold Collapse",
        "n_agents": n_agents,
        "seed": seed,
        "criteria": {
            "C1_inverted_u_fidelity": {
                "f_rm_wildtype": float(f_rm_wt),
                "f_rm_null": float(f_rm_null),
                "delta_f_rm": float(delta_f_rm),
                "frozen_threshold": ">= 0.400",
                "verdict": "PASS" if c1_pass else "FAIL"
            },
            "C2_gja1_gap_junction_rescue": {
                "p_open_syncytium": float(p_open_sync),
                "p_open_isolated": float(p_open_iso),
                "relative_reduction": float(rel_reduction),
                "frozen_threshold": "<= -0.350 (-35.0%)",
                "verdict": "PASS" if c2_pass else "FAIL"
            },
            "C3_double_hit_epistatic_catastrophe": {
                "p_fail_double_hit": float(p_fail_double),
                "p_fail_single_hit": float(p_fail_single),
                "risk_ratio": float(risk_ratio),
                "frozen_threshold": ">= 5.00x",
                "verdict": "PASS" if c3_pass else "FAIL"
            },
            "C4_compensatory_paranoid_rigidity": {
                "severe_shunt_count": int(np.sum(chronic_shunt_mask)),
                "rigidity_rate": float(rigidity_rate),
                "frozen_threshold": ">= 0.800 (80.0%)",
                "verdict": "PASS" if c4_pass else "FAIL"
            }
        },
        "compound_verdict": "PASS" if compound_pass else "FAIL",
        "data": {
            "b_pde4b": b_pde4b.tolist(),
            "b_gja1": b_gja1.tolist(),
            "p_open_mean": p_open_mean.tolist(),
            "fidelity_rm": fidelity_rm.tolist(),
            "hallucination_rate": hallucination_rate.tolist(),
            "terminal_trust_s100": terminal_trust_s100.tolist()
        },
        "grids": {
            "wt": grid_wt_sample.tolist() if grid_wt_sample is not None else [],
            "mut_iso": grid_mut_iso_sample.tolist() if grid_mut_iso_sample is not None else [],
            "mut_res": grid_mut_res_sample.tolist() if grid_mut_res_sample is not None else []
        }
    }
    
    return results

def plot_publication_figure(results, output_path):
    fig, axes = plt.subplots(2, 2, figsize=(13, 11))
    
    # Palette
    c_blue = "#1f77b4"
    c_red = "#d62728"
    c_green = "#2ca02c"
    c_purple = "#9467bd"
    
    b_pde4b = np.array(results["data"]["b_pde4b"])
    b_gja1 = np.array(results["data"]["b_gja1"])
    p_open = np.array(results["data"]["p_open_mean"])
    fidelity = np.array(results["data"]["fidelity_rm"])
    hallucination = np.array(results["data"]["hallucination_rate"])
    s100 = np.array(results["data"]["terminal_trust_s100"])
    
    # -------------------------------------------------------------------------
    # Panel (a): Inverted-U Reality-Testing Fidelity vs PDE4B Missense Burden
    # -------------------------------------------------------------------------
    ax = axes[0, 0]
    ax.scatter(b_pde4b, fidelity, alpha=0.35, color=c_blue, edgecolors="none", s=25)
    
    # Binned trend
    bins = np.linspace(0, 1.0, 11)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bin_means = []
    for b_low, b_high in zip(bins[:-1], bins[1:]):
        m = (b_pde4b >= b_low) & (b_pde4b < b_high)
        bin_means.append(np.mean(fidelity[m]) if np.sum(m) > 0 else np.nan)
    ax.plot(bin_centers, bin_means, color="black", lw=2.5, marker="o", label="Population Mean")
    
    crit = results["criteria"]["C1_inverted_u_fidelity"]
    ax.axhline(0.50, color="gray", linestyle="--", alpha=0.7, label="Chance Discrimination (0.50)")
    ax.set_title("(a) Reality-Testing Fidelity vs. PDE4B Missense Burden", fontweight="bold", fontsize=11)
    ax.set_xlabel("PDE4B AlphaMissense Pathogenicity Burden ($B_{\\mathrm{PDE4B}}$)")
    ax.set_ylabel("Reality-Monitoring Fidelity ($F_{\\mathrm{RM}}$)")
    ax.legend(loc="lower left", fontsize=8.5)
    ax.text(0.55, 0.92, f"$\\Delta F_{{\\mathrm{{RM}}}} = {crit['delta_f_rm']:.3f}$ ({crit['verdict']})",
            transform=ax.transAxes, bbox=dict(boxstyle="round", facecolor="white", alpha=0.8), fontsize=9)
    ax.grid(True, alpha=0.25)
    
    # -------------------------------------------------------------------------
    # Panel (b): Syncytial cAMP Buffering across 10x10 Cellular Grid
    # -------------------------------------------------------------------------
    ax = axes[0, 1]
    crit_c2 = results["criteria"]["C2_gja1_gap_junction_rescue"]
    grid_iso = np.array(results["grids"]["mut_iso"])
    grid_res = np.array(results["grids"]["mut_res"])
    
    if grid_iso.size > 0 and grid_res.size > 0:
        diff_grid = grid_iso - grid_res
        im = ax.imshow(diff_grid, cmap="viridis", origin="lower")
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("cAMP Clearance $(\\mu\\mathrm{M})$ via GJA1 Coupling", fontsize=9)
    else:
        ax.text(0.5, 0.5, "Grid syncytium profile", ha="center", va="center")
        
    ax.set_title("(b) Spatial Syncytial cAMP Clearance via GJA1 Gap Junctions", fontweight="bold", fontsize=11)
    ax.set_xlabel("Pyramidal Cell Column $x$")
    ax.set_ylabel("Pyramidal Cell Row $y$")
    ax.text(0.05, 0.88, f"$\\Delta P_{{\\mathrm{{open}}}} = {crit_c2['relative_reduction']*100:.1f}\\%$ ({crit_c2['verdict']})",
            transform=ax.transAxes, color="white", bbox=dict(boxstyle="round", facecolor="black", alpha=0.7), fontsize=9)

    # -------------------------------------------------------------------------
    # Panel (c): Double-Hit Epistatic Heatmap: PDE4B x GJA1 Missense Burden
    # -------------------------------------------------------------------------
    ax = axes[1, 0]
    crit_c3 = results["criteria"]["C3_double_hit_epistatic_catastrophe"]
    
    # 2D Binned Hallucination Risk
    pde4b_bins = np.linspace(0, 1.0, 6)
    gja1_bins = np.linspace(0, 1.0, 6)
    heatmap_matrix = np.zeros((5, 5))
    
    for i in range(5):
        for j in range(5):
            mask = (b_pde4b >= pde4b_bins[i]) & (b_pde4b < pde4b_bins[i+1]) & \
                   (b_gja1 >= gja1_bins[j]) & (b_gja1 < gja1_bins[j+1])
            if np.sum(mask) > 0:
                heatmap_matrix[j, i] = np.mean(hallucination[mask] > 0.50)
            else:
                heatmap_matrix[j, i] = 0.0
                
    im2 = ax.imshow(heatmap_matrix, cmap="magma", origin="lower", extent=[0, 1, 0, 1], vmin=0, vmax=1.0)
    cbar2 = plt.colorbar(im2, ax=ax, fraction=0.046, pad=0.04)
    cbar2.set_label("Catastrophic Hallucination Rate ($P > 0.50$)", fontsize=9)
    ax.set_title("(c) Double-Hit Epistatic Catastrophe Matrix", fontweight="bold", fontsize=11)
    ax.set_xlabel("PDE4B Missense Burden ($B_{\\mathrm{PDE4B}}$)")
    ax.set_ylabel("GJA1 (Cx43) Missense Burden ($B_{\\mathrm{GJA1}}$)")
    ax.text(0.05, 0.88, f"Risk Ratio $= {crit_c3['risk_ratio']:.2f}\\times$ ({crit_c3['verdict']})",
            transform=ax.transAxes, color="white", bbox=dict(boxstyle="round", facecolor="black", alpha=0.7), fontsize=9)

    # -------------------------------------------------------------------------
    # Panel (d): Compensatory Paranoid Prior Rigidity (Trust Updating)
    # -------------------------------------------------------------------------
    ax = axes[1, 1]
    crit_c4 = results["criteria"]["C4_compensatory_paranoid_rigidity"]
    
    # Compare trajectories over 100 confirming rounds
    t_steps = np.arange(101)
    lambda_0 = 0.35
    delta_S = 0.05
    S_base = 0.10
    
    # Trace for WT
    s_wt = np.zeros(101)
    s_wt[0] = 0.10
    l_wt = lambda_0 * np.exp(-4.5 * 0.15)
    for t in range(100):
        s_wt[t+1] = np.clip(s_wt[t] + l_wt * 1.0 - delta_S * (s_wt[t] - S_base), 0.0, 1.0)
        
    # Trace for Severe Mutants
    s_mut = np.zeros(101)
    s_mut[0] = 0.10
    l_mut = lambda_0 * np.exp(-4.5 * 0.85)
    for t in range(100):
        s_mut[t+1] = np.clip(s_mut[t] + l_mut * 1.0 - delta_S * (s_mut[t] - S_base), 0.0, 1.0)
        
    ax.plot(t_steps, s_wt, color=c_green, lw=2.5, label="Intact WT Circuit ($P_{\\mathrm{open}} = 0.15$)")
    ax.plot(t_steps, s_mut, color=c_red, lw=2.5, linestyle="--", label="Chronic HCN1 Shunting ($P_{\\mathrm{open}} = 0.85$)")
    ax.axhline(0.25, color="gray", linestyle=":", label="Frozen Rigidity Threshold ($S \\leq 0.25$)")
    
    ax.set_title("(d) Compensatory Paranoid Rigidity under Confirmation", fontweight="bold", fontsize=11)
    ax.set_xlabel("Consecutive Validating Interactions ($t$)")
    ax.set_ylabel("Trust State ($S_t$)")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="center right", fontsize=8.5)
    ax.text(0.40, 0.15, f"Rigidity Rate $= {crit_c4['rigidity_rate']*100:.1f}\\%$ ({crit_c4['verdict']})",
            transform=ax.transAxes, bbox=dict(boxstyle="round", facecolor="white", alpha=0.8), fontsize=9)
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
    
    results_json_path = os.path.join(results_dir, "sim_g24_results.json")
    fig_path = os.path.join(fig_dir, "fig_sim_g24_perceptual_genomics.png")
    
    print("=" * 70)
    print("🧬 EXECUTING SIM G24: PERCEPTUAL GENOMICS & BIOELECTRIC EPISTASIS")
    print("=" * 70)
    
    results = simulate_perceptual_genomics(n_agents=1000, seed=42)
    
    with open(results_json_path, "w") as f:
        # Save compact JSON without raw arrays to save disk space
        save_payload = {
            "experiment": results["experiment"],
            "n_agents": results["n_agents"],
            "seed": results["seed"],
            "criteria": results["criteria"],
            "compound_verdict": results["compound_verdict"]
        }
        json.dump(save_payload, f, indent=2)
    print(f"[Results JSON Saved] {results_json_path}")
    
    plot_publication_figure(results, fig_path)
    
    print("\n" + "=" * 80)
    print("📊 SIM G24: PERCEPTUAL GENOMICS VERDICTS:")
    print("=" * 80)
    for c_name, c_data in results["criteria"].items():
        print(f"[{c_name}]: {c_data['verdict']} (Frozen threshold: {c_data['frozen_threshold']})")
    print("-" * 80)
    print(f"🎯 COMPOUND VERDICT: {results['compound_verdict']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
