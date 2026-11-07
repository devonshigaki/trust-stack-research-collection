#!/usr/bin/env python3
"""Simulation W8: Temporal SHAP Feature Engine & Counterfactual Recourse
ECOA / Regulation B (12 C.F.R. § 1002.9) Compliant Adverse Action Architecture
for the FreshCredit State-Space Scoring Model.

Implements exact coalitional Shapley feature attribution over 6 core cash-flow features,
extracts the 4 mandatory principal adverse-action reasons, and computes minimal
counterfactual recourse paths for credit-invisible and denied applicants.
"""

import os
import json
import math
import itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FEATURES = [
    "cash_flow_buffer_ratio",      # Ratio of monthly surplus to debt obligations
    "spend_volatility",            # Normalized SD of daily discretionary spending
    "nsf_frequency_90d",           # Overdraft / insufficient funds count in 90 days
    "income_timing_dispersion",    # Variance in payroll deposit intervals (days^2)
    "obligation_repayment_ratio",  # Verified on-time payment rate of rent/utilities
    "deposit_persistence_days"     # Consecutive days with positive liquid balance
]

FEATURE_NAMES = {
    "cash_flow_buffer_ratio": "Insufficient monthly cash flow buffer above obligations",
    "spend_volatility": "High volatility in discretionary expenditure",
    "nsf_frequency_90d": "Frequency of insufficient funds or overdraft events",
    "income_timing_dispersion": "Irregularity or unpredictability of income deposits",
    "obligation_repayment_ratio": "Delinquency or missed payments on recurring obligations",
    "deposit_persistence_days": "Insufficient continuous positive account balance duration"
}

# Linear-Quadratic surrogate proxy for the non-linear Kalman/EM state expectation
# Ground-truth weights representing risk sensitivity:
WEIGHTS = np.array([0.28, -0.18, -0.32, -0.14, 0.35, 0.20])
INTERCEPTS = 0.50

def scoring_function(X):
    """Computes trust-weighted credit score S in [0, 1]."""
    raw = INTERCEPTS + np.dot(X, WEIGHTS)
    return 1.0 / (1.0 + np.exp(-3.5 * (raw - 0.50)))

def exact_shapley(x, baseline_mean, feature_subset_evaluator):
    """Computes exact Shapley values for an applicant x against population baseline."""
    n_features = len(x)
    shapley_values = np.zeros(n_features)
    
    # All subsets
    all_indices = list(range(n_features))
    
    for i in all_indices:
        other_indices = [idx for idx in all_indices if idx != i]
        phi_i = 0.0
        
        for k in range(len(other_indices) + 1):
            subsets = list(itertools.combinations(other_indices, k))
            weight = (math.factorial(k) * math.factorial(n_features - k - 1)) / math.factorial(n_features)
            
            for subset in subsets:
                # With i
                s_with_i = list(subset) + [i]
                val_with = feature_subset_evaluator(x, baseline_mean, s_with_i)
                # Without i
                val_without = feature_subset_evaluator(x, baseline_mean, list(subset))
                
                phi_i += weight * (val_with - val_without)
                
        shapley_values[i] = phi_i
        
    return shapley_values

def subset_eval(x, baseline, active_indices):
    """Marginal evaluation where inactive features take baseline population means."""
    instance = baseline.copy()
    for idx in active_indices:
        instance[idx] = x[idx]
    return scoring_function(instance)

def run_shap_battery():
    print("=" * 65)
    print("RUNNING SIMULATION W8: TEMPORAL SHAP ADVERSE-ACTION ENGINE")
    print("=" * 65)

    np.random.seed(42)
    N = 1000

    # Generate synthetic population (Thin-file, Subprime, Near-prime, Prime)
    # Features normalized around standard operating scales
    X_buffer = np.random.gamma(2.0, 0.5, N)             # Mean ~ 1.0
    X_vol = np.random.beta(2, 5, N)                     # Mean ~ 0.28
    X_nsf = np.random.poisson(0.8, N)                   # Mean ~ 0.8 events
    X_disp = np.random.exponential(4.0, N)              # Mean ~ 4.0 days^2
    X_repay = np.random.beta(8, 2, N)                   # Mean ~ 0.80
    X_persist = np.random.exponential(120, N)           # Mean ~ 120 days

    X = np.column_stack([X_buffer, X_vol, X_nsf, X_disp, X_repay, X_persist])
    
    # Standardize features for scoring
    X_norm = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
    baseline_mean = np.zeros(len(FEATURES))
    baseline_score = scoring_function(baseline_mean)

    scores = scoring_function(X_norm)
    threshold = 0.60 # Decision cutoff for prime loan terms
    denied_indices = np.where(scores < threshold)[0]

    print(f"Total Applicants: {N}")
    print(f"Mean Population Score: {np.mean(scores):.3f}")
    print(f"Approved (S >= {threshold}): {np.sum(scores >= threshold)} ({np.mean(scores >= threshold):.1%})")
    print(f"Denied (S < {threshold}): {len(denied_indices)} ({len(denied_indices)/N:.1%})\n")

    # Audit a denied applicant
    sample_denied_idx = denied_indices[0]
    sample_x = X_norm[sample_denied_idx]
    sample_score = scores[sample_denied_idx]

    eval_fn = lambda x_inst, base, active: subset_eval(x_inst, base, active)
    shap_vals = exact_shapley(sample_x, baseline_mean, eval_fn)

    # Verification: Efficiency Property
    reconstructed_diff = np.sum(shap_vals)
    true_diff = sample_score - baseline_score
    efficiency_error = abs(reconstructed_diff - true_diff)

    print(f"Sample Denied Applicant #{sample_denied_idx}:")
    print(f"  Assigned Trust Score: {sample_score:.4f} (Threshold: {threshold:.2f})")
    print(f"  Sum of Shapley Attributions: {reconstructed_diff:+.6f}")
    print(f"  True Score Diff from Baseline: {true_diff:+.6f}")
    print(f"  Efficiency Discrepancy: {efficiency_error:.2e} (Machine-precision PASS)\n")

    # Principal Adverse Action Reasons (Reg B requires up to 4 principal reasons)
    # Most negative Shapley contributions:
    ranked_reasons_order = np.argsort(shap_vals) # lowest (most negative) first
    top_4_reasons = [FEATURES[idx] for idx in ranked_reasons_order[:4]]

    print("--- 12 C.F.R. § 1002.9 Disclosed Principal Reasons ---")
    for r_rank, r_idx in enumerate(ranked_reasons_order[:4], 1):
        f_key = FEATURES[r_idx]
        print(f"Reason {r_rank}: {FEATURE_NAMES[f_key]}")
        print(f"          (Shapley impact on score: {shap_vals[r_idx]:+.4f})")

    # Counterfactual Recourse Calculation:
    # How much must the worst feature improve to achieve score >= threshold?
    worst_idx = ranked_reasons_order[0]
    x_recourse = sample_x.copy()
    recourse_found = False
    for step in np.linspace(0, 3.0, 100):
        # Improve feature in positive direction
        if WEIGHTS[worst_idx] > 0:
            x_recourse[worst_idx] = sample_x[worst_idx] + step
        else:
            x_recourse[worst_idx] = sample_x[worst_idx] - step
            
        if scoring_function(x_recourse) >= threshold:
            recourse_found = True
            break

    print(f"\nActionable Counterfactual Recourse:")
    print(f"  Target Feature: {FEATURES[worst_idx]}")
    print(f"  Adjustment Required: {abs(x_recourse[worst_idx] - sample_x[worst_idx]):.2f} standard deviations")
    print(f"  Target Score Post-Recourse: {scoring_function(x_recourse):.4f} (APPROVED)")

    # Plot figure
    plt.figure(figsize=(10, 5), dpi=300)
    
    plt.subplot(1, 2, 1)
    y_pos = np.arange(len(FEATURES))
    colors = ['#d9534f' if v < 0 else '#5cb85c' for v in shap_vals]
    plt.barh(y_pos, shap_vals, color=colors, edgecolor='black', alpha=0.85)
    plt.yticks(y_pos, [f.replace('_', ' ').title() for f in FEATURES], fontsize=9)
    plt.axvline(0, color='black', lw=1.2)
    plt.title(f"Shapley Feature Attribution (Score: {sample_score:.2f})", fontsize=11, fontweight='bold')
    plt.xlabel("Impact on Trust Score S (Shapley phi)", fontsize=10)
    plt.grid(True, alpha=0.3, axis='x')

    plt.subplot(1, 2, 2)
    # Population Shapley Summary for Denied Applicants
    denied_sample = X_norm[denied_indices[:100]]
    all_shap = [exact_shapley(row, baseline_mean, eval_fn) for row in denied_sample]
    all_shap = np.array(all_shap)
    mean_abs_shap = np.mean(np.abs(all_shap), axis=0)
    sorted_idx = np.argsort(mean_abs_shap)
    
    plt.barh(np.arange(len(FEATURES)), mean_abs_shap[sorted_idx], color='#337ab7', edgecolor='black', alpha=0.85)
    plt.yticks(np.arange(len(FEATURES)), [FEATURES[i].replace('_', ' ').title() for i in sorted_idx], fontsize=9)
    plt.title("Population Global Feature Importance (Denied)", fontsize=11, fontweight='bold')
    plt.xlabel("Mean |Shapley phi| (N=100 Denied)", fontsize=10)
    plt.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    fig_path = os.path.join(os.path.dirname(__file__), "fig_w8_shap_adverse_action.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"\nSaved figure to: {fig_path}")

    # Output JSON summary
    summary_data = {
        "timestamp": "2026-11-06",
        "sample_applicant_id": int(sample_denied_idx),
        "score": float(sample_score),
        "threshold": float(threshold),
        "efficiency_error": float(efficiency_error),
        "reconstructed_diff": float(reconstructed_diff),
        "true_diff": float(true_diff),
        "principal_reasons": [
            {"rank": i+1, "feature": FEATURES[idx], "shapley_value": float(shap_vals[idx]), "disclosure_text": FEATURE_NAMES[FEATURES[idx]]}
            for i, idx in enumerate(ranked_reasons_order[:4])
        ],
        "counterfactual_target_achieved": bool(recourse_found),
        "c1_efficiency_pass": bool(efficiency_error < 1e-10),
        "c2_recourse_pass": bool(recourse_found)
    }

    json_path = os.path.join(os.path.dirname(__file__), "sim_shap_results.json")
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved results to: {json_path}")

    assert summary_data["c1_efficiency_pass"], "FAIL: Shapley efficiency violated!"
    assert summary_data["c2_recourse_pass"], "FAIL: Counterfactual recourse not found!"
    print("\n✓ ALL ADVERSE ACTION & RECOURSE INVARIANTS VERIFIED (PASS)!")

if __name__ == "__main__":
    run_shap_battery()
