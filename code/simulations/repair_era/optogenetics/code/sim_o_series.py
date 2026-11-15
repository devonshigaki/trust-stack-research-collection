"""
Sim O-Series: Optogenetic Causal Interventions
Pre-registered Hypotheses O1, O2, O3.
Demonstrates causal biological mechanisms of trust via simulated light-gated opsins.
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

def four_state_opsin_model(light_on, t_steps, type="ChR2"):
    """
    Authentic 4-state Markov kinetic opsin ODE (Grossman et al. 2011; Nikolic et al. 2009):
      States p = [C1, O1, O2, C2]^T on the 3-simplex (exact sum(p) == 1.0 at every step,
      matching formal/lean/TrustStack/MasterLaw.lean `markov_euler_simplex_invariant`).
    """
    dt = 0.1
    substeps = 10
    p = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)  # C1, O1, O2, C2
    current = np.zeros(t_steps, dtype=np.float64)
    gd1, gd2, e12, e21, gr = 0.13, 0.025, 0.022, 0.014, 0.004

    for t in range(t_steps):
        ga1 = 0.50 if light_on[t] else 0.0
        ga2 = 0.12 if light_on[t] else 0.0
        for _ in range(substeps):
            c1, o1, o2, c2 = p
            dc1 = -ga1 * c1 + gd1 * o1 + gr * c2
            do1 = ga1 * c1 - (gd1 + e12) * o1 + e21 * o2
            do2 = e12 * o1 - (gd2 + e21) * o2 + ga2 * c2
            dc2 = gd2 * o2 - (ga2 + gr) * c2
            p = p + dt * np.array([dc1, do1, do2, dc2])
            assert abs(float(np.sum(p)) - 1.0) < 1e-12, f"Simplex conservation violated: {np.sum(p)}"
            assert np.all(p >= -1e-15), f"Negative Markov state probability: {p}"
        # Normalized open-state conductance proxy (O1 + 0.2 * O2) / peak_open
        open_cond = min(1.0, (p[1] + 0.2 * p[2]) / 0.55)
        current[t] = -open_cond if type == "ArchT" else open_cond

    return current

# ---------------------------------------------------------
# Hypothesis O1: The Dopaminergic "Trust Lesion"
# ---------------------------------------------------------
def run_o1_dopamine_lesion(seed=42):
    np.random.seed(seed)
    T = 100
    
    # Master law parameters
    lam_p = 0.35
    lam_m = 0.84  # 2.4x loss aversion
    delta = 0.05
    S_base = 0.20
    
    # Control: Normal D activation
    S_ctrl = np.zeros(T)
    S_ctrl[0] = S_base
    D_ctrl = np.zeros(T)
    
    # Lesion: ArchT inhibited D
    S_lesion = np.zeros(T)
    S_lesion[0] = S_base
    D_lesion = np.zeros(T)
    
    # Light pulse for lesion (continuous yellow light during interaction)
    light_on = np.ones(T, dtype=bool)
    # Simulate ArchT photocurrent
    I_archt = four_state_opsin_model(light_on, T, type="ArchT")
    
    for t in range(T-1):
        # "FAIR" interaction: positive validation epsilon ~ 0.5
        eps_t = 0.5 + np.random.normal(0, 0.05)
        
        # D channel encodes reward prediction. 
        D_ctrl[t] = max(0, eps_t)
        # Optogenetic suppression of D channel
        D_lesion[t] = max(0, eps_t + 2.0 * I_archt[t]) # Strong inhibition
        
        # Update law couples D to lam_p
        eff_lam_p_ctrl = lam_p * D_ctrl[t]
        eff_lam_p_lesion = lam_p * D_lesion[t]
        
        S_ctrl[t+1] = S_ctrl[t] + eff_lam_p_ctrl * 1.0 - delta * (S_ctrl[t] - S_base)
        S_lesion[t+1] = S_lesion[t] + eff_lam_p_lesion * 1.0 - delta * (S_lesion[t] - S_base)

    final_suppression = 1.0 - (S_lesion[-1] - S_base) / (S_ctrl[-1] - S_base)
    pass_o1 = final_suppression >= 0.90
    
    return {
        "T": T,
        "S_ctrl": S_ctrl,
        "S_lesion": S_lesion,
        "final_suppression": final_suppression,
        "pass": pass_o1
    }

# ---------------------------------------------------------
# Hypothesis O2: Induced Vulnerability & Predatory Cloaking
# ---------------------------------------------------------
def run_o2_induced_vulnerability(seed=42):
    np.random.seed(seed)
    n_agents = 250 # Top quartile D10 "Secure" agents
    
    # Baseline cognitive bandwidth for D10
    kappa_base = np.random.beta(8, 2, size=n_agents) # High bandwidth
    
    # Simulate ChR2 activation on Cortisol (C) Threat network
    light_on = np.ones(n_agents, dtype=bool)
    I_chr2 = four_state_opsin_model(light_on, n_agents, type="ChR2")
    
    # Stress induction compresses cognitive bandwidth
    # kappa_eff = kappa_base * exp(-alpha * C)
    stress_coupling = 3.5
    kappa_stressed = kappa_base * np.exp(-stress_coupling * I_chr2)
    
    # Sim D16 Predatory Cloaking parameters
    chi = 3.65 # High cloaking ratio
    gamma = 8.0
    tau = 0.20
    u_res = np.random.normal(0.10, 0.04, size=n_agents)
    
    apr_promo = 0.0
    apr_true = 390.0
    urgency = 0.25
    u_cash = 0.40 * 0.4 # normalized amount 4000/10000
    amt_norm = 0.4
    
    def simulate_uptake(kappa_arr):
        p_disc = 1.0 / (1.0 + np.exp(-gamma * (kappa_arr / chi - tau)))
        r_draw = np.random.uniform(0, 1, size=n_agents)
        u_seen_disc = r_draw < p_disc
        
        u_eff = np.where(
            u_seen_disc,
            -(apr_true / 100.0) * amt_norm + u_cash,
            -(apr_promo / 100.0) * amt_norm + u_cash + urgency
        )
        dec = u_eff > u_res
        return np.mean(dec)
        
    uptake_control = simulate_uptake(kappa_base)
    uptake_stressed = simulate_uptake(kappa_stressed)
    
    rel_risk = uptake_stressed / (uptake_control + 1e-6)
    pass_o2 = rel_risk >= 5.0
    
    return {
        "kappa_base": kappa_base,
        "kappa_stressed": kappa_stressed,
        "uptake_control": uptake_control,
        "uptake_stressed": uptake_stressed,
        "rel_risk": rel_risk,
        "pass": pass_o2
    }

# ---------------------------------------------------------
# Hypothesis O3: Macroeconomic Fragmentation
# ---------------------------------------------------------
def run_o3_kuramoto_fragmentation(seed=42):
    np.random.seed(seed)
    N = 500 # agents
    T = 200 # steps
    dt = 0.1
    K = 3.0 # Coupling constant above critical threshold
    
    # Intrinsic frequencies (normal market dynamics)
    omega = np.random.normal(1.0, 0.2, size=N)
    theta_ctrl = np.random.uniform(0, 2*np.pi, size=N)
    theta_lesion = theta_ctrl.copy()
    
    # 10% subpopulation with inhibited Oxytocin (O) and Serotonin (S)
    n_mut = int(0.10 * N)
    mut_idx = np.arange(n_mut)
    
    # Healthy network simulation
    R_ctrl = np.zeros(T)
    for t in range(T):
        R_c = np.abs(np.mean(np.exp(1j * theta_ctrl)))
        R_ctrl[t] = R_c
        
        # Mean field
        psi_c = np.angle(np.mean(np.exp(1j * theta_ctrl)))
        dtheta_c = omega + K * R_c * np.sin(psi_c - theta_ctrl)
        theta_ctrl += dtheta_c * dt
        
    # Lesioned network simulation
    # O/S inhibition functionally zeroes out their coupling term K
    K_eff = np.ones(N) * K
    K_eff[mut_idx] = 0.0 # Severed from social validation
    
    R_lesion = np.zeros(T)
    for t in range(T):
        R_l = np.abs(np.mean(np.exp(1j * theta_lesion)))
        R_lesion[t] = R_l
        
        psi_l = np.angle(np.mean(np.exp(1j * theta_lesion)))
        # Mutants ignore the mean field (K_eff = 0) and free-run
        dtheta_l = omega + K_eff * R_l * np.sin(psi_l - theta_lesion)
        theta_lesion += dtheta_l * dt
        
    term_R_ctrl = np.mean(R_ctrl[-20:])
    term_R_lesion = np.mean(R_lesion[-20:])
    collapse_pct = (term_R_ctrl - term_R_lesion) / term_R_ctrl
    pass_o3 = collapse_pct >= 0.40
    
    return {
        "R_ctrl": R_ctrl,
        "R_lesion": R_lesion,
        "term_R_ctrl": term_R_ctrl,
        "term_R_lesion": term_R_lesion,
        "collapse_pct": collapse_pct,
        "pass": pass_o3
    }

def make_o_series_figure(res_o1, res_o2, res_o3, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=180)
    
    # O1: Dopamine Lesion
    ax = axes[0]
    ax.plot(res_o1["S_ctrl"], label="Healthy Control", color="#3B82F6", linewidth=2.5)
    ax.plot(res_o1["S_lesion"], label="DA Inhibited (ArchT)", color="#EF4444", linewidth=2.5, linestyle="--")
    ax.axhline(0.20, color="#94A3B8", linestyle=":", label="Baseline")
    ax.set_title(f"O1: Dopaminergic Trust Lesion\n(Suppression: {res_o1['final_suppression']*100:.1f}%)")
    ax.set_xlabel("Interaction Steps")
    ax.set_ylabel("Trust State S_t")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.3)
    
    # O2: Induced Vulnerability
    ax = axes[1]
    labels = ["Secure (Control)", "ChR2 Stressed"]
    rates = [res_o2["uptake_control"]*100, res_o2["uptake_stressed"]*100]
    bars = ax.bar(labels, rates, color=["#10B981", "#EF4444"], edgecolor="black", width=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1, f"{h:.1f}%", ha="center", fontweight="bold")
    ax.set_title(f"O2: Optogenetically Induced Vulnerability\n(Rel. Risk: {res_o2['rel_risk']:.1f}x)")
    ax.set_ylabel("Predatory Contract Uptake (%)")
    ax.set_ylim(0, max(rates)*1.2)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    
    # O3: Macroeconomic Fragmentation
    ax = axes[2]
    ax.plot(res_o3["R_ctrl"], label="100% Healthy Network", color="#3B82F6", linewidth=2.5)
    ax.plot(res_o3["R_lesion"], label="10% O/S Inhibited", color="#D97706", linewidth=2.5, linestyle="--")
    ax.set_title(f"O3: Macroeconomic Kuramoto Fragmentation\n(Coherence Collapse: {res_o3['collapse_pct']*100:.1f}%)")
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Global Coherence (R)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.3)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"[Figure] Saved: {output_path}")

def main():
    print("=======================================================================")
    print("🚀 EXECUTING SIM O-SERIES: OPTOGENETIC CAUSAL INTERVENTIONS")
    print("=======================================================================")
    
    res_o1 = run_o1_dopamine_lesion()
    res_o2 = run_o2_induced_vulnerability()
    res_o3 = run_o3_kuramoto_fragmentation()
    
    results = {
        "experiment": "Sim O-Series: Optogenetics",
        "seed": 42,
        "criteria_evaluations": {
            "O1_Dopamine_Lesion": {
                "observed_suppression": res_o1["final_suppression"],
                "threshold": 0.90,
                "verdict": "PASS" if res_o1["pass"] else "FAIL"
            },
            "O2_Induced_Vulnerability": {
                "observed_relative_risk": res_o2["rel_risk"],
                "threshold": 5.0,
                "verdict": "PASS" if res_o2["pass"] else "FAIL"
            },
            "O3_Macro_Fragmentation": {
                "observed_collapse": res_o3["collapse_pct"],
                "threshold": 0.40,
                "verdict": "PASS" if res_o3["pass"] else "FAIL"
            }
        },
        "compound_verdict": "PASS" if all([res_o1["pass"], res_o2["pass"], res_o3["pass"]]) else "FAIL"
    }
    
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "sim_o_series_results.json"), "w") as f:
        json.dump(results, f, indent=2)
        
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    fig_path = os.path.join(repo_root, "figures/optogenetics/fig_sim_o_series.png")
    make_o_series_figure(res_o1, res_o2, res_o3, fig_path)

    print("\n📊 SIM O-SERIES CRITERIA VERDICTS:")
    print("-" * 80)
    for c_name, c_data in results["criteria_evaluations"].items():
        print(f"[{c_name}]")
        print(f"  Observed: {c_data.get('observed_suppression') or c_data.get('observed_relative_risk') or c_data.get('observed_collapse'):.4f} vs Threshold: {c_data['threshold']} ==> {c_data['verdict']}")
    print("-" * 80)
    print(f"🎯 COMPOUND VERDICT: {results['compound_verdict']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
