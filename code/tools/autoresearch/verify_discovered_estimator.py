#!/usr/bin/env python3
"""
Post-Discovery Z3 Formalization & Vault Regression Check for `autoresearch` Winning Estimator
Verifies:
  1. Z3 Non-Vacuous Proof: Huber-IRLS weights w_rob satisfy 0 < w_rob <= 5.0 (no singularity)
     and exact unbiased recovery (lam_hat == lam_true) under zero noise.
  2. Sealed Vault Evaluation (`N = 600` unseen users): frac_gt_015 <= 0.02, p95_err <= 0.06, cd_auc >= 0.99.
"""

import os
import sys
import subprocess
import z3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, os.path.join(BASE_DIR, "formal"))
from z3_nonvacuity import prove_nonvacuous


def verify_estimator_z3():
    abs_eps, abs_res, scale, w, w_rob = z3.Reals("abs_eps abs_res scale w w_rob")
    denom_eps = z3.If(abs_eps >= 0.20, abs_eps, 0.20)
    huber_fac = z3.If(abs_res / (2.0 * scale) >= 1.0, abs_res / (2.0 * scale), 1.0)
    premises = [
        abs_eps >= 0, abs_res >= 0, scale >= 1e-4,
        w == 1.0 / denom_eps, w_rob == w / huber_fac,
    ]
    assert prove_nonvacuous(premises, z3.Or(w_rob <= 0.0, w_rob > 5.0), "IRLS Weight Bound")

    eps1, eps2, lam_true, w1, w2, lam_hat = z3.Reals("eps1 eps2 lam_true w1 w2 lam_hat")
    dH1, dH2 = lam_true * eps1, lam_true * eps2
    prem_unbiased = [
        w1 > 0, w1 <= 5.0, w2 > 0, w2 <= 5.0,
        eps1 != 0, eps2 != 0,
        lam_hat == (w1 * eps1 * dH1 + w2 * eps2 * dH2) / (w1 * eps1 * eps1 + w2 * eps2 * eps2),
    ]
    assert prove_nonvacuous(prem_unbiased, lam_hat != lam_true, "IRLS Zero-Noise Unbiasedness")
    print("✓ Z3 Non-Vacuous Proof: 0 < w_rob <= 5.0 & exact zero-noise unbiased recovery (PASS)")


def verify_ood_stress_tests():
    import numpy as np
    from candidate_estimator import estimate_user_gains

    rng = np.random.default_rng(12345)
    # 1. Planted zero-lambda control (pure Student-t4 noise, true lambda = 0)
    zero_errs = []
    for _ in range(200):
        eps = np.clip(rng.standard_t(4.0, 120) * 0.28, -1.5, 1.5)
        dH = rng.standard_t(4.0, 120) * 0.045
        lam_hat, _, _ = estimate_user_gains(eps, dH)
        zero_errs.append(abs(lam_hat))
    assert np.percentile(zero_errs, 95) <= 0.05, f"Planted lambda=0 p95 error too high: {np.percentile(zero_errs, 95)}"

    # 2. Ultra-thin stream (n=45 events, 10% negative events, planted 2x asymmetry)
    thin_errs, thin_ratios = [], []
    for _ in range(200):
        eps = np.where(rng.random(45) < 0.10, -1.0, 1.0) * np.clip(np.abs(rng.standard_t(4.0, 45)) * 0.25, 0.02, 1.5)
        lam_t = np.where(eps < 0, 0.36, 0.18)
        dH = lam_t * eps + rng.standard_t(4.0, 45) * 0.045
        lam_hat, lp_hat, ln_hat = estimate_user_gains(eps, dH)
        thin_errs.append(abs(lam_hat - float(np.mean(lam_t))))
        thin_ratios.append(ln_hat / max(lp_hat, 1e-6))
    assert np.mean(np.asarray(thin_errs) > 0.15) == 0.0, "Ultra-thin stream corridor failure > 0%"
    assert 1.5 <= np.median(thin_ratios) <= 2.5, f"Ultra-thin median ratio drifted: {np.median(thin_ratios)}"
    print(
        f"✓ OOD Stress Controls: Planted lambda=0 (p95={np.percentile(zero_errs, 95):.4f}) & "
        f"Thin-Stream n=45 (p95={np.percentile(thin_errs, 95):.4f}, ratio={np.median(thin_ratios):.2f}) PASS"
    )


def main():
    verify_estimator_z3()
    verify_ood_stress_tests()
    prep = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prepare.py")
    res = subprocess.run([sys.executable, prep, "--unlock-vault"], capture_output=True, text=True, check=True)
    print(res.stdout)
    for line in res.stdout.splitlines():
        if "vault_frac_gt_015:" in line:
            assert float(line.split(":")[1]) <= 0.02
        if "vault_p95_err:" in line:
            assert float(line.split(":")[1]) <= 0.06
        if "vault_cd_auc:" in line:
            assert float(line.split(":")[1]) >= 0.99
    print("✓ SEALED VAULT (N=600) + Z3 POST-DISCOVERY VERIFICATION PASSED!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
