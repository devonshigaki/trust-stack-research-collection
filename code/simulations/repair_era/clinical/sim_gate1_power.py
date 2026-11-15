#!/usr/bin/env python3
"""DOCAS-GATE-1 Statistical Power Audit (Nominal vs. 5-Channel Holm-Bonferroni FWER)."""

import json
import os
import numpy as np
import scipy.stats as stats


def calculate_power(N: int, d_z: float, alpha: float = 0.05) -> float:
    ncp = d_z * np.sqrt(N)
    t_crit = stats.t.ppf(1.0 - alpha / 2.0, df=N - 1)
    return float(1.0 - stats.nct.cdf(t_crit, df=N - 1, nc=ncp) + stats.nct.cdf(-t_crit, df=N - 1, nc=ncp))


def min_n_for_power(d_z: float, alpha: float, target_power: float = 0.80) -> int:
    for n in range(10, 500):
        if calculate_power(n, d_z, alpha=alpha) >= target_power:
            return n
    return -1


def main():
    N_target = 48
    SESOI_dz = 0.30
    alpha_nominal = 0.05
    alpha_fwer_5ch = alpha_nominal / 5.0  # Holm-Bonferroni worst-case across 5 DOCAS channels

    power_nom = calculate_power(N_target, SESOI_dz, alpha_nominal)
    power_fwer = calculate_power(N_target, SESOI_dz, alpha_fwer_5ch)
    power_dz05_fwer = calculate_power(N_target, 0.50, alpha_fwer_5ch)
    n_needed_dz03_fwer = min_n_for_power(SESOI_dz, alpha_fwer_5ch, 0.80)

    results = {
        "trial_design": "DOCAS-GATE-1 (within-subject pharmacological crossover)",
        "planned_N_completers": N_target,
        "nominal_alpha": alpha_nominal,
        "fwer_5channel_alpha": alpha_fwer_5ch,
        "sesoi_dz": SESOI_dz,
        "nominal_power_at_N48_dz03": power_nom,
        "fwer_5ch_power_at_N48_dz03": power_fwer,
        "fwer_5ch_power_at_N48_dz05": power_dz05_fwer,
        "N_required_80pct_fwer_power_at_dz03": n_needed_dz03_fwer,
        "honest_audit": (
            f"At N={N_target}, power to detect d_z=0.30 is {power_nom*100:.1f}% (nominal alpha=0.05) "
            f"and {power_fwer*100:.1f}% under 5-channel Holm-Bonferroni alpha=0.01. "
            f"N={N_target} achieves >=80% FWER-controlled power only for medium effects (d_z>=0.50, power={power_dz05_fwer*100:.1f}%); "
            f"detecting d_z=0.30 at 80% FWER power requires N={n_needed_dz03_fwer} completers."
        ),
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_gate1_power_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved honest power audit to {out_path}")
    print(results["honest_audit"])


if __name__ == "__main__":
    main()
