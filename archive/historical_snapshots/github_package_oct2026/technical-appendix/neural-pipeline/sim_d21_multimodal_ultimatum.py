#!/usr/bin/env python3
"""
Sim D21: Multimodal Gating & Anterior Insula Ultimatum Game Fairness
Implements the pre-registered protocol in SIM_D21_PRE_REGISTRATION.md.

Theoretical Anchors:
- Sanfey, A. G., et al. (2003). Science, 300(5626), 1755-1758.
- Fehr, E., & Schmidt, K. M. (1999). QJE, 114(3), 817-868.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_sim_d21(n_agents=1000, seed=42):
    rng = np.random.RandomState(seed)
    
    # Cognitive bandwidth (D1-D10 deciles)
    kappa = rng.beta(2, 5, size=n_agents)
    
    # Ultimatum Game Parameters (Predatory Contract)
    # L = 1000 cash advance. True Penalty P = 3000 (balloon + fees).
    # Veridical offer share is heavily disadvantageous
    L = 1.0
    P_true = 3.0
    M = L + P_true
    
    # BOLD fMRI Proxy Simulation (Sanfey aINS Norm Prediction Error)
    # Norm expectation for fairness = 0.5 * M
    s_norm = 0.5 * M
    
    # Cloaking Conditions
    # Dual Cloak: Visually masked + Auditory > 10 syl/s
    chi_vis = 4.0
    r_aud = 11.5
    
    # Calculate Perceptual Shielding
    alpha_vis = 1.0 / chi_vis
    alpha_aud = 1.0 / (1.0 + np.exp(1.35 * (r_aud - 9.80)))
    
    # T_reality = 2.5 gating
    v_threat = 0.8 * kappa
    eps_vis = rng.normal(0, 0.5, size=n_agents)
    eps_aud = rng.normal(0, 0.5, size=n_agents)
    
    m_multi = 0.5 * (alpha_vis * P_true + v_threat + eps_vis) + 0.5 * (alpha_aud * P_true + v_threat + eps_aud)
    
    perceived_penalty_cloaked = np.where(m_multi > 2.5, P_true, 0.0)
    perceived_penalty_veridical = np.full(n_agents, P_true)
    
    # aINS Activation Proxy (Norm Prediction Error)
    s_observed_cloaked = L - perceived_penalty_cloaked
    delta_NPE_cloaked = s_norm - s_observed_cloaked
    bold_aINS_cloaked = np.maximum(0, delta_NPE_cloaked)
    
    s_observed_veridical = L - perceived_penalty_veridical
    delta_NPE_veridical = s_norm - s_observed_veridical
    bold_aINS_veridical = np.maximum(0, delta_NPE_veridical)
    
    # Fehr-Schmidt Evaluation (Accept/Reject)
    # Disadvantageous inequality aversion alpha_i
    alpha_fehr_0 = rng.uniform(0.5, 3.0, size=n_agents)
    
    # Under aINS activation, inequality aversion spikes. Under silence, it drops.
    alpha_f_cloaked = alpha_fehr_0 * (1.0 + np.tanh(bold_aINS_cloaked - 1.0))
    alpha_f_veridical = alpha_fehr_0 * (1.0 + np.tanh(bold_aINS_veridical - 1.0))
    
    x_lender_cloaked = perceived_penalty_cloaked - L
    x_i_cloaked = L - perceived_penalty_cloaked
    U_cloaked = x_i_cloaked - alpha_f_cloaked * np.maximum(x_lender_cloaked - x_i_cloaked, 0)
    uptake_cloaked = (U_cloaked > 0)
    
    x_lender_veridical = perceived_penalty_veridical - L
    x_i_veridical = L - perceived_penalty_veridical
    U_veridical = x_i_veridical - alpha_f_veridical * np.maximum(x_lender_veridical - x_i_veridical, 0)
    uptake_veridical = (U_veridical > 0)
    
    # Ex-Post Shock (t+1)
    # Penalty physically extracted
    bold_aINS_rebound = np.maximum(0, s_norm - (L - P_true))
    
    # C1: Insular Hypoactivation
    c1_suppression = 1.0 - (np.mean(bold_aINS_cloaked) / np.mean(bold_aINS_veridical))
    c1_pass = c1_suppression >= 0.60
    
    # C2: Ultimatum Acceptance Inversion
    c2_accept_cloak = np.mean(uptake_cloaked)
    c2_reject_verid = 1.0 - np.mean(uptake_veridical)
    c2_pass = (c2_reject_verid >= 0.95) and (c2_accept_cloak >= 0.70)
    
    # C3: Vulnerability Gradient
    k_sorted = np.argsort(kappa)
    d1_agents = k_sorted[:n_agents//10]
    d10_agents = k_sorted[-n_agents//10:]
    p_d1 = np.mean(uptake_cloaked[d1_agents])
    p_d10 = np.mean(uptake_cloaked[d10_agents])
    odds_d1 = p_d1 / (1.0 - p_d1 + 1e-9)
    odds_d10 = p_d10 / (1.0 - p_d10 + 1e-9)
    odds_ratio = odds_d1 / (odds_d10 + 1e-9)
    c3_pass = odds_ratio >= 12.0
    
    # C4: Ex-Post Insular Rebound
    # Compare rebound to fair contract (L=1, P=0)
    bold_aINS_fair = np.maximum(0, s_norm - (L - 0.0))
    rebound_ratio = np.mean(bold_aINS_rebound) / (np.mean(bold_aINS_fair) + 1e-9)
    c4_pass = rebound_ratio >= 3.0
    
    compound_pass = c1_pass and c2_pass and c3_pass and c4_pass
    
    results = {
        "experiment": "Sim D21: Multimodal Gating & Ultimatum Game Fairness",
        "n_agents": n_agents,
        "seed": seed,
        "criteria": {
            "C1_insular_hypoactivation": {
                "suppression_rate": float(c1_suppression),
                "frozen_threshold": ">= 0.60",
                "verdict": "PASS" if c1_pass else "FAIL"
            },
            "C2_ultimatum_acceptance_inversion": {
                "reject_veridical": float(c2_reject_verid),
                "accept_cloaked": float(c2_accept_cloak),
                "frozen_threshold": "Accept >= 0.70, Reject >= 0.95",
                "verdict": "PASS" if c2_pass else "FAIL"
            },
            "C3_vulnerability_gradient": {
                "odds_ratio": float(odds_ratio),
                "frozen_threshold": ">= 12.0",
                "verdict": "PASS" if c3_pass else "FAIL"
            },
            "C4_ex_post_insular_rebound": {
                "rebound_ratio": float(rebound_ratio),
                "frozen_threshold": ">= 3.0",
                "verdict": "PASS" if c4_pass else "FAIL"
            }
        },
        "compound_verdict": "PASS" if compound_pass else "FAIL",
        "data": {
            "bold_aINS_cloaked": bold_aINS_cloaked.tolist(),
            "bold_aINS_veridical": bold_aINS_veridical.tolist(),
            "uptake_cloaked": uptake_cloaked.tolist(),
            "uptake_veridical": uptake_veridical.tolist(),
            "kappa": kappa.tolist()
        }
    }
    return results

def plot_sim_d21(results, output_path):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # (a) Insular Hypoactivation
    ax = axes[0, 0]
    data = [results["data"]["bold_aINS_veridical"], results["data"]["bold_aINS_cloaked"]]
    ax.boxplot(data, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Veridical", "Multimodal Cloak"])
    ax.set_title("(a) Anterior Insula BOLD Surrogate (NPE)", fontweight='bold')
    ax.set_ylabel("Norm Prediction Error (aINS)")
    ax.grid(alpha=0.3)
    
    # (b) Uptake Inversion
    ax = axes[0, 1]
    v_up = np.mean(results["data"]["uptake_veridical"])
    c_up = np.mean(results["data"]["uptake_cloaked"])
    ax.bar(["Veridical", "Multimodal Cloak"], [v_up, c_up], color=["black", "red"])
    ax.set_title(f"(b) Ultimatum Acceptance (Cloaked: {c_up*100:.1f}%)", fontweight='bold')
    ax.set_ylabel("Acceptance Rate")
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3, axis='y')
    
    # (c) Vulnerability Gradient
    ax = axes[1, 0]
    k = np.array(results["data"]["kappa"])
    up = np.array(results["data"]["uptake_cloaked"])
    
    bins = np.linspace(0, 1, 11)
    bin_means = []
    for i in range(10):
        mask = (k >= bins[i]) & (k < bins[i+1])
        bin_means.append(np.mean(up[mask]) if np.sum(mask) > 0 else np.nan)
        
    ax.plot(np.arange(1, 11), bin_means[::-1], marker='o', color='purple', lw=2)
    ax.set_title(f"(c) Vulnerability Gradient (OR = {results['criteria']['C3_vulnerability_gradient']['odds_ratio']:.2f})", fontweight='bold')
    ax.set_xlabel("Cognitive Bandwidth Decile (D1=Stressed, D10=Secure)")
    ax.set_ylabel("Predatory Uptake Rate")
    ax.grid(alpha=0.3)
    
    # (d) Rebound
    ax = axes[1, 1]
    ax.bar(["Ex-Ante (Cloaked)", "Ex-Post Shock (Default)"], 
           [np.mean(results["data"]["bold_aINS_cloaked"]), np.mean(results["data"]["bold_aINS_veridical"])], 
           color=["gray", "darkred"])
    ax.set_title("(d) Delayed Insular Rebound at Maturity", fontweight='bold')
    ax.set_ylabel("aINS BOLD Surrogate")
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def main():
    results = run_sim_d21()
    base_dir = "/Users/devonshigaki/Desktop/research"
    results_path = os.path.join(base_dir, "experiments/brainit-fmri/results/sim_d21_results.json")
    fig_path = os.path.join(base_dir, "figures/docas/pipeline/fig_sim_d21_multimodal_fairness.png")
    
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        # Save compact JSON without raw arrays to save disk space
        save_payload = {
            "experiment": results["experiment"],
            "n_agents": results["n_agents"],
            "seed": results["seed"],
            "criteria": results["criteria"],
            "compound_verdict": results["compound_verdict"]
        }
        json.dump(save_payload, f, indent=2)
        
    plot_sim_d21(results, fig_path)
    print("Sim D21 (Multimodal Ultimatum Game) Complete.")

if __name__ == "__main__":
    main()
