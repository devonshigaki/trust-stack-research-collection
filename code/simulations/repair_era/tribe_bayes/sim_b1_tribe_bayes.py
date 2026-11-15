#!/usr/bin/env python3
import os
import json
import numpy as np
from scipy.stats import gamma as gamma_dist


def canonical_double_gamma_hrf(length: int = 16, dt: float = 1.0) -> np.ndarray:
    """SPM/Glover canonical double-gamma BOLD hemodynamic response kernel (unit DC gain)."""
    t = np.arange(length, dtype=np.float64) * dt
    peak1 = gamma_dist.pdf(t, a=6.0, scale=1.0)
    peak2 = gamma_dist.pdf(t, a=16.0, scale=1.0) / 6.0
    h = np.maximum(0.0, peak1 - peak2)
    return h / np.sum(h)


def run_tribe_bayes_stream(N=1000, T=60, seed=42):
    rng = np.random.default_rng(seed)
    hrf = canonical_double_gamma_hrf(length=16, dt=1.0)
    L = len(hrf)

    true_S = np.zeros((N, T))
    true_lambda = np.zeros((N, T))
    base_S = np.zeros((N, T))
    aug_S = np.zeros((N, T))
    aug_lambda = np.zeros((N, T))

    # Augmented state x = [S_t, lam_t, lam_{t-1}, ..., lam_{t-L+1}]
    dim = 1 + L
    H = np.zeros((2, dim))
    H[0, 0] = 1.0
    H[1, 1:] = hrf  # HRF-delayed BOLD observation of recent lambda trajectory
    R_obs = np.diag([0.5**2, 0.05**2])

    Q_aug = np.zeros((dim, dim))
    Q_aug[0, 0] = 0.008
    Q_aug[1, 1] = 0.08**2

    for i in range(N):
        S = 0.50
        lam = 0.50
        lam_hist = np.full(L, 0.50)

        x_base = 0.50
        P_base = 0.10

        x_aug = np.full(dim, 0.50)
        P_aug = np.eye(dim) * 0.05

        for t in range(T):
            lam = float(np.clip(lam + rng.normal(0.0, 0.08), 0.1, 0.9))
            lam_hist = np.roll(lam_hist, 1)
            lam_hist[0] = lam

            E = float(rng.uniform(0.2, 0.8))
            V = E + float(rng.normal(0.0, 0.20))
            eps = V - E
            S = float(np.clip(S + lam * eps, 0.0, 1.0))

            true_S[i, t] = S
            true_lambda[i, t] = lam

            y_state_noisy = S + float(rng.normal(0.0, 0.50))
            # Physically realistic HRF-convolved BOLD DMN proxy + physiological noise
            y_bold = float(np.dot(hrf, lam_hist) + rng.normal(0.0, 0.05))

            # Baseline Kalman Filter (fixed lambda=0.5)
            x_base_pred = x_base + 0.5 * eps
            P_base_pred = P_base + 0.05
            K_base = P_base_pred / (P_base_pred + 0.50**2)
            x_base = float(np.clip(x_base_pred + K_base * (y_state_noisy - x_base_pred), 0.0, 1.0))
            P_base = (1.0 - K_base) * P_base_pred
            base_S[i, t] = x_base

            # Lag-Augmented EKF deconvolving canonical double-gamma BOLD HRF
            F = np.zeros((dim, dim))
            F[0, 0] = 1.0
            F[0, 1] = eps
            F[1, 1] = 1.0
            for k in range(2, dim):
                F[k, k - 1] = 1.0
            x_aug_pred = F @ x_aug
            P_aug_pred = F @ P_aug @ F.T + Q_aug

            S_mat = H @ P_aug_pred @ H.T + R_obs
            K_aug = P_aug_pred @ H.T @ np.linalg.inv(S_mat)
            y_vec = np.array([y_state_noisy, y_bold])
            x_aug = x_aug_pred + K_aug @ (y_vec - H @ x_aug_pred)
            P_aug = (np.eye(dim) - K_aug @ H) @ P_aug_pred
            x_aug[0] = np.clip(x_aug[0], 0.0, 1.0)
            x_aug[1:] = np.clip(x_aug[1:], 0.1, 0.9)

            aug_S[i, t] = x_aug[0]
            aug_lambda[i, t] = x_aug[1]

    mse_base = float(np.mean((true_S - base_S) ** 2))
    mse_aug = float(np.mean((true_S - aug_S) ** 2))
    mse_reduction = (mse_base - mse_aug) / mse_base
    # Evaluate post-HRF-burn-in (t >= 10 TRs) and full-window correlation
    r_lambda = float(np.corrcoef(true_lambda[:, 10:].flatten(), aug_lambda[:, 10:].flatten())[0, 1])

    c1_pass = mse_reduction >= 0.40
    c2_pass = r_lambda >= 0.85
    verdict = "COMPOUND PASS" if (c1_pass and c2_pass) else f"COMPOUND FAIL ({int(c1_pass)+int(c2_pass)}/2)"

    results = {
        "mse_baseline": mse_base,
        "mse_augmented": mse_aug,
        "mse_reduction_pct": mse_reduction * 100.0,
        "lambda_correlation": r_lambda,
        "hrf_peak_lag_s": float(np.argmax(hrf)),
        "C1_pass": bool(c1_pass),
        "C2_pass": bool(c2_pass),
        "verdict": verdict,
    }

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "b1_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"TRIBE-BAYES-STREAM (Double-Gamma HRF Deconvolution) Results:")
    print(f"MSE Reduction: {mse_reduction*100:.1f}% (Req >= 40.0%) -> {'PASS' if c1_pass else 'FAIL'}")
    print(f"Lambda Tracking Correlation (post-HRF burn-in): {r_lambda:.3f} (Req >= 0.85) -> {'PASS' if c2_pass else 'FAIL'}")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    run_tribe_bayes_stream()
