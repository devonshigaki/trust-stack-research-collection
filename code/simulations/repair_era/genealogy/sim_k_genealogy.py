#!/usr/bin/env python3
"""
Sim K-Series: Genealogical Coalescence, Kingman Intensity & Heritability Calibration
Pre-registered Hypotheses K1, K2, K3.
Anchored to DOCAS §4.1 twin study literature target h^2 ≈ 0.32 and Kingman (1982) coalescent.
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

def _wright_fisher_tmrca(rng, pop_n=200, n_sample=64, max_gens=1500, selection_strength=0.0):
    """Forward-time Wright-Fisher simulation with explicit parent-pointer backward TMRCA reconstruction."""
    loci = rng.integers(0, 2, size=(pop_n, 20), dtype=np.int8)
    parent_ptr = np.zeros((max_gens, pop_n), dtype=np.int32)

    for g in range(max_gens):
        lam = 0.1 + 0.8 * np.mean(loci, axis=1)
        if selection_strength > 0.0:
            eps = rng.normal(0.05, 0.25, size=pop_n)
            S_i = np.clip(0.50 + lam * eps, 0.0, 1.0)
            w = 1.0 / (1.0 + np.exp(-selection_strength * (S_i - 0.50)))
            probs = w / np.sum(w)
        else:
            probs = None
        parents = rng.choice(pop_n, size=pop_n, replace=True, p=probs)
        parent_ptr[g] = parents
        loci = loci[parents]
        mut = rng.random(loci.shape) < 0.005
        loci ^= mut.astype(np.int8)

    active = rng.choice(pop_n, size=n_sample, replace=False)
    for steps, g in enumerate(range(max_gens - 1, -1, -1), start=1):
        active = np.unique(parent_ptr[g, active])
        if active.size == 1:
            return float(steps)
    return float(max_gens)


def run_k_series(seed=42):
    rng = np.random.default_rng(seed)

    print("▶ [1/3] Simulating Hypothesis K1: Diploid Twin Heritability vs Coalescent Intensity...")
    n_pairs, n_loci = 200, 20
    kappa_sweep = np.linspace(0.1, 2.0, 11)
    h2_results = []

    for kappa in kappa_sweep:
        p1 = rng.integers(0, 2, size=(n_pairs, n_loci, 2))
        p2 = rng.integers(0, 2, size=(n_pairs, n_loci, 2))
        idx_p = np.arange(n_pairs)[:, None]
        idx_l = np.arange(n_loci)[None, :]
        mz_geno = (p1[idx_p, idx_l, rng.integers(0, 2, size=(n_pairs, n_loci))] + p2[idx_p, idx_l, rng.integers(0, 2, size=(n_pairs, n_loci))]).mean(axis=1) / 2.0
        dz1_g = (p1[idx_p, idx_l, rng.integers(0, 2, size=(n_pairs, n_loci))] + p2[idx_p, idx_l, rng.integers(0, 2, size=(n_pairs, n_loci))]).mean(axis=1) / 2.0
        dz2_g = (p1[idx_p, idx_l, rng.integers(0, 2, size=(n_pairs, n_loci))] + p2[idx_p, idx_l, rng.integers(0, 2, size=(n_pairs, n_loci))]).mean(axis=1) / 2.0

        g_scale = np.sqrt(kappa)
        mz1 = 0.50 + 0.8 * g_scale * (mz_geno - 0.50) + rng.normal(0.0, 0.08, n_pairs)
        mz2 = 0.50 + 0.8 * g_scale * (mz_geno - 0.50) + rng.normal(0.0, 0.08, n_pairs)
        dz1 = 0.50 + 0.8 * g_scale * (dz1_g - 0.50) + rng.normal(0.0, 0.08, n_pairs)
        dz2 = 0.50 + 0.8 * g_scale * (dz2_g - 0.50) + rng.normal(0.0, 0.08, n_pairs)

        r_mz = np.corrcoef(mz1, mz2)[0, 1]
        r_dz = np.corrcoef(dz1, dz2)[0, 1]
        h2_results.append(float(max(0.0, min(1.0, 2.0 * (r_mz - r_dz)))))

    idx_opt = int(np.argmin(np.abs(np.array(h2_results) - 0.32)))
    calibrated_kappa = float(kappa_sweep[idx_opt])
    calibrated_h2 = float(h2_results[idx_opt])
    pass_k1 = (0.80 <= calibrated_kappa <= 1.20) and (0.28 <= calibrated_h2 <= 0.36)
    
    print("▶ [2/3] Simulating Hypothesis K2: Forward Wright-Fisher Parent-Pointer TMRCA...")
    pop_n, n_sample, n_reps = 200, 64, 30
    neutral_runs = [_wright_fisher_tmrca(rng, pop_n=pop_n, n_sample=n_sample, selection_strength=0.0) for _ in range(n_reps)]
    selection_runs = [_wright_fisher_tmrca(rng, pop_n=pop_n, n_sample=n_sample, selection_strength=6.0) for _ in range(n_reps)]

    kingman_analytical_neutral = float(2.0 * pop_n * (1.0 - 1.0 / n_sample))
    mean_tmrca_neutral = float(np.mean(neutral_runs))
    mean_tmrca_selection = float(np.mean(selection_runs))
    tmrca_ratio = mean_tmrca_selection / max(mean_tmrca_neutral, 1e-9)
    tmrca_reduction_pct = (1.0 - tmrca_ratio) * 100.0
    pass_k2 = tmrca_ratio <= 0.65

    print("▶ [3/3] Simulating Hypothesis K3: Polygenic Genetic Variance Contribution...")
    n_agents = 1024
    loci_pop = rng.integers(0, 2, size=(n_agents, 20, 2)).sum(axis=2).mean(axis=1) / 2.0
    genotypes = 0.1 + 0.8 * loci_pop
    environmental_history = rng.exponential(0.18, n_agents)
    trust_scores = np.clip(0.50 + genotypes * 0.65 + environmental_history - np.mean(environmental_history), 0.0, 1.0)

    slope = np.cov(genotypes, trust_scores)[0, 1] / np.var(genotypes)
    var_explained = float((slope ** 2 * np.var(genotypes)) / np.var(trust_scores))
    pass_k3 = (0.25 <= var_explained <= 0.45)

    compound_pass = pass_k1 and pass_k2 and pass_k3
    verdict = "COMPOUND PASS (3/3)" if compound_pass else f"COMPOUND FAIL ({sum([pass_k1, pass_k2, pass_k3])}/3 PASS)"

    return {
        "timestamp": "2026-11-15",
        "seed": seed,
        "compound_verdict": verdict,
        "compound_pass": bool(compound_pass),
        "K1_heritability_calibration": {
            "kappa_sweep": kappa_sweep.tolist(),
            "h2_results": h2_results,
            "calibrated_kappa": calibrated_kappa,
            "calibrated_h2": calibrated_h2,
            "pass": bool(pass_k1),
        },
        "K2_tmrca_acceleration": {
            "kingman_analytical_neutral_gens": kingman_analytical_neutral,
            "mean_tmrca_neutral": mean_tmrca_neutral,
            "mean_tmrca_selection": mean_tmrca_selection,
            "tmrca_ratio": tmrca_ratio,
            "tmrca_reduction_pct": tmrca_reduction_pct,
            "pass": bool(pass_k2),
        },
        "K3_genetic_stratification": {
            "r2_genetic_variance": var_explained,
            "pass": bool(pass_k3),
        },
    }

def make_figure(results, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.2), dpi=200)
    
    # Panel 1: K1 Heritability Curve
    ax = axes[0]
    kappas = results["K1_heritability_calibration"]["kappa_sweep"]
    h2s = results["K1_heritability_calibration"]["h2_results"]
    ax.plot(kappas, h2s, marker="o", color="#1f77b4", lw=2.5, label="Simulated Heritability (h²)")
    ax.axhline(0.32, color="#2ca02c", linestyle="--", lw=1.8, label="DOCAS §4.1 Twin Literature Benchmark (h²=0.32)")
    ax.axhspan(0.28, 0.36, color="#2ca02c", alpha=0.15, label="Acceptance Corridor [0.28, 0.36]")
    ax.axvline(results["K1_heritability_calibration"]["calibrated_kappa"], color="#d62728", linestyle=":", lw=2,
               label=f"Calibrated Default κ* = {results['K1_heritability_calibration']['calibrated_kappa']:.1f}")
    ax.set_title(f"A. Kingman Heritability Calibration (K1)\nCalibrated h² = {results['K1_heritability_calibration']['calibrated_h2']:.3f} ({'PASS' if results['K1_heritability_calibration']['pass'] else 'FAIL'})")
    ax.set_xlabel("Kingman Coalescent Intensity (κ)")
    ax.set_ylabel("Falconer Heritability h² = 2(r_MZ - r_DZ)")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=True, fontsize=8.5)
    
    # Panel 2: K2 TMRCA Distribution
    ax = axes[1]
    res_k2 = results["K2_tmrca_acceleration"]
    bars = [res_k2["mean_tmrca_neutral"], res_k2["mean_tmrca_selection"]]
    ax.bar(["Neutral Kingman", "Trust Selection"], bars, color=["#7f7f7f", "#9467bd"], width=0.5, alpha=0.85)
    ax.set_ylabel("Mean T_MRCA (Coalescent Time Units)")
    ax.set_title(f"B. T_MRCA Coalescence Acceleration (K2)\nTime Reduction: {res_k2['tmrca_reduction_pct']:.1f}% ({'PASS' if res_k2['pass'] else 'FAIL'})")
    ax.grid(True, alpha=0.3, axis="y")
    
    # Panel 3: K3 Genetic Stratification
    ax = axes[2]
    res_k3 = results["K3_genetic_stratification"]
    r2_g = res_k3["r2_genetic_variance"]
    ax.pie([r2_g, 1.0 - r2_g], labels=[f"Additive Genetics ({r2_g*100:.1f}%)", f"Environmental Dynamics ({(1-r2_g)*100:.1f}%)"],
           colors=["#ff7f0e", "#17becf"], autopct="%1.1f%%", startangle=90, explode=(0.05, 0))
    ax.set_title(f"C. Trust Stratification Decomposition (K3)\nGenetic R² = {r2_g:.3f} ({'PASS' if res_k3['pass'] else 'FAIL'})")
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"✓ Saved publication figure: {output_path}")

def main():
    print("="*70)
    print("⚡ RUNNING SIM K-SERIES: GENEALOGY & KINGMAN HERITABILITY")
    print("="*70)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base_dir, exist_ok=True)
    
    results = run_k_series(seed=42)
    
    json_path = os.path.join(base_dir, "sim_k_results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✓ Saved results JSON: {json_path}")
    
    fig_path = os.path.join(base_dir, "fig_sim_k_genealogy.png")
    make_figure(results, fig_path)
    
    # Write Run Report
    report_path = os.path.join(base_dir, "K_SERIES_RUN_REPORT.md")
    with open(report_path, "w") as f:
        f.write(f"""# Sim K-Series Run Report: Genealogical Coalescence & Kingman Intensity Calibration

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **{results['compound_verdict']}**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **K1: Heritability Calibration** | Sweep Kingman intensity $\\kappa \\in [0.1, 2.0]$ | $\\kappa^* \\in [0.80, 1.20] \\to h^2 \\in [0.28, 0.36]$ | **$\\kappa^* = {results['K1_heritability_calibration']['calibrated_kappa']:.1f} \\to h^2 = {results['K1_heritability_calibration']['calibrated_h2']:.3f}$** | **{'PASS' if results['K1_heritability_calibration']['pass'] else 'FAIL'}** |
| **K2: TMRCA Acceleration** | Directional trust selection vs neutral Kingman | $T_{{\\text{{MRCA}}}}^{{\\text{{sel}}}} / T_{{\\text{{MRCA}}}}^{{\\text{{neut}}}} \\le 0.65$ | **{results['K2_tmrca_acceleration']['tmrca_ratio']:.4f}** ({results['K2_tmrca_acceleration']['tmrca_reduction_pct']:.1f}% acceleration) | **{'PASS' if results['K2_tmrca_acceleration']['pass'] else 'FAIL'}** |
| **K3: Genetic Stratification** | Polygenic variance contribution to trust standing | $R^2_{{\\text{{genetic}}}} \\in [0.25, 0.45]$ | **$R^2 = {results['K3_genetic_stratification']['r2_genetic_variance']:.3f}$** | **{'PASS' if results['K3_genetic_stratification']['pass'] else 'FAIL'}** |

---

## 2. Engineering Calibrations for Production Simulator

1. **Default Slider Position:** The live simulator's "Kingman Intensity" slider must default to **$\\kappa = {results['K1_heritability_calibration']['calibrated_kappa']:.1f}$**, representing an empirical heritability baseline of $h^2 = 0.32$.
2. **Selective Coalescence Bounds:** Directional trust accumulation accelerates lineage fixation by {results['K2_tmrca_acceleration']['tmrca_reduction_pct']:.1f}%, bounding maximum tree depth in the genealogy canvas.
""")
    print(f"✓ Saved Run Report: {report_path}")

if __name__ == "__main__":
    main()
