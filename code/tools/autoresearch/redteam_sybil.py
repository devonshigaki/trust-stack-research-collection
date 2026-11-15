#!/usr/bin/env python3
"""
Adversarial Red-Team `autoresearch` Harness (Track B)
Freezes the repaired `sim_p8_collusion.py` cryptographic-bond & cluster-entropy defense
and searches over 200 adversarial Sybil / collusion mutations (spoofed names, sub-threshold
bonds, cluster splits, asymmetric wash-trade schedules) to verify zero profitable bypass.
"""

import os
import sys
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, os.path.join(BASE_DIR, "code/simulations/repair_era/tfp"))
from sim_p8_collusion import MIN_BOND_USD, compute_verified_cluster_entropy


def evaluate_attack(attestations, total_cost_usd: float) -> float:
    """Attacker utility: effective standing accumulation per $1,000 spent."""
    h = compute_verified_cluster_entropy(attestations)
    eta = 1.0 - float(np.exp(-h))
    return eta / max(total_cost_usd / 1000.0, 1e-6)


def main():
    print("=" * 75)
    print("ADVERSARIAL `autoresearch` RED-TEAM HARNESS: TFP SYBIL/COLLUSION DEFENSE")
    print("=" * 75)
    rng = np.random.default_rng(42)

    best_unbonded_eta = 0.0
    best_single_cluster_eta = 0.0
    best_bonded_roi = 0.0
    cheapest_valid_bypass_usd = float("inf")

    # 200 autonomous adversarial mutations
    for gen in range(200):
        # Mutation Family 1: Unbonded / invalid-sig prefix spoofing ("bank_*" / "fed_*")
        n_sp = int(rng.integers(2, 50))
        sp_atts = [
            {
                "provider_id": f"bank_verified_{k}",
                "cluster_id": f"independent_{k}",
                "bonded_usd": float(rng.uniform(0.0, MIN_BOND_USD - 1.0)),
                "sig_valid": bool(rng.random() < 0.5),
                "weight": float(rng.uniform(0.01, 1.0)),
            }
            for k in range(n_sp)
        ]
        # Force at least one invalid check (either low bond or bad sig)
        for a in sp_atts:
            if a["sig_valid"] and a["bonded_usd"] >= MIN_BOND_USD:
                a["bonded_usd"] = MIN_BOND_USD - 1.0
        best_unbonded_eta = max(best_unbonded_eta, 1.0 - float(np.exp(-compute_verified_cluster_entropy(sp_atts))))

        # Mutation Family 2: Bonded single-cartel key splitting (varying splits & weights)
        n_cl = int(rng.integers(2, 30))
        cl_atts = [
            {
                "provider_id": f"node_{k}",
                "cluster_id": "cartel_root_0",
                "bonded_usd": MIN_BOND_USD,
                "sig_valid": True,
                "weight": float(rng.dirichlet(np.ones(n_cl))[k]),
            }
            for k in range(n_cl)
        ]
        best_single_cluster_eta = max(best_single_cluster_eta, 1.0 - float(np.exp(-compute_verified_cluster_entropy(cl_atts))))

        # Mutation Family 3: Multi-cluster independent capital bribery (legitimately bonding P >= 2 independent roots)
        p_ind = int(rng.integers(2, 12))
        weights = rng.dirichlet(np.ones(p_ind) * float(rng.uniform(0.2, 5.0)))
        ind_atts = [
            {
                "provider_id": f"ind_{k}",
                "cluster_id": f"cluster_{k}",
                "bonded_usd": MIN_BOND_USD,
                "sig_valid": True,
                "weight": float(weights[k]),
            }
            for k in range(p_ind)
        ]
        cost_usd = p_ind * MIN_BOND_USD
        eta_ind = 1.0 - float(np.exp(-compute_verified_cluster_entropy(ind_atts)))
        best_bonded_roi = max(best_bonded_roi, evaluate_attack(ind_atts, cost_usd))
        if eta_ind >= 0.63:  # Reaching H >= 1.0 nats threshold
            cheapest_valid_bypass_usd = min(cheapest_valid_bypass_usd, cost_usd)

    print(f"Max Unbonded/Spoofed Attack Efficiency (200 gens): {best_unbonded_eta:.6f} (must be 0.000000)")
    print(f"Max Single-Cartel Split Efficiency (200 gens):     {best_single_cluster_eta:.6f} (must be 0.000000)")
    print(f"Min Collateral Needed to Reach H>=1.0 Threshold:   ${cheapest_valid_bypass_usd:,.0f} (>= $150,000)")
    print(f"Max Bonded Bribery Efficiency per $1k Staked:      {best_bonded_roi:.5f}")

    assert best_unbonded_eta == 0.0, "Unbonded/spoofed attack succeeded!"
    assert best_single_cluster_eta == 0.0, "Single-cluster split bypassed entropy gate!"
    assert cheapest_valid_bypass_usd >= 3 * MIN_BOND_USD, "Threshold H>=1.0 requires >= 3 distinct bonded clusters!"
    print("\n✓ ADVERSARIAL RED-TEAM AUTORESEARCH PASSED (0 BYPASSES IN 200 MUTATION GENS)!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
