#!/usr/bin/env python3
"""
MUTABLE CANDIDATE ESTIMATOR (Edited by `autoresearch` Loop)
Baseline (Gen 0): Constant-gain Gaussian Kalman/EM + Two-Gain OLS (reproduces SIM-R1 failure).
"""

import json
import sys
import numpy as np


def estimate_user_gains(eps: np.ndarray, dH: np.ndarray):
    # Winning Gen 2 (autoresearch selected): Inverse-|eps| Huber IRLS (val_score=0.021486, TRAIN_GENERALIZED)
    abs_eps = np.abs(eps)
    w = 1.0 / np.maximum(abs_eps, 0.20)
    lam_init = float(np.sum(np.sign(eps) * dH) / max(np.sum(abs_eps), 1e-12))
    resid = dH - lam_init * eps
    scale = max(1.4826 * float(np.median(np.abs(resid))), 1e-4)
    w_rob = w / np.maximum(1.0, np.abs(resid) / (2.0 * scale))
    lam_hat = float(np.sum(w_rob * eps * dH) / max(np.sum(w_rob * eps ** 2), 1e-12))
    pos, neg = eps > 0.0, eps < 0.0
    lamp_hat = float(np.sum(w_rob[pos] * eps[pos] * dH[pos]) / max(np.sum(w_rob[pos] * eps[pos] ** 2), 1e-12))
    lamm_hat = float(np.sum(w_rob[neg] * eps[neg] * dH[neg]) / max(np.sum(w_rob[neg] * eps[neg] ** 2), 1e-12))
    return lam_hat, lamp_hat, lamm_hat


def main():
    in_path, out_path = sys.argv[1], sys.argv[2]
    users = json.load(open(in_path, "r", encoding="utf-8"))
    preds = []
    for u in users:
        eps = np.asarray(u["eps"], dtype=np.float64)
        dH = np.asarray(u["dH"], dtype=np.float64)
        lam, lp, ln = estimate_user_gains(eps, dH)
        preds.append({"lam_hat": lam, "lamp_hat": lp, "lamm_hat": ln})
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(preds, f)


if __name__ == "__main__":
    main()
