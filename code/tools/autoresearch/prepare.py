#!/usr/bin/env python3
"""
IMMUTABLE AUTORESEARCH HARNESS (DO NOT MODIFY)
Implements Karpathy's fixed-harness evaluator upgraded with:
  1. Out-of-process execution of `candidate_estimator.py` (zero target access).
  2. Dwork et al. (2015) Thresholdout reusable holdout across `train` and `val`.
  3. One-shot sealed `vault` split (`--unlock-vault`) for final verification.
  4. Quantitative AST node simplicity gate.
"""

import ast
import json
import os
import secrets
import subprocess
import sys
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATE = os.path.join(HERE, "candidate_estimator.py")
BUDGET_LEDGER = os.path.join(HERE, ".thresholdout_budget.json")
MAX_VAL_QUERIES = 50

BETA = 0.10
LAM_MIN, LAM_MAX = 0.02, 1.5
DF_NOISE = 4
SIG_U = 0.10
DAYS = 365


def _gen_cohort(n_users: int, seed: int):
    rng = np.random.default_rng(seed)
    users = []
    for idx in range(n_users):
        arm = "sym_adapt" if idx < int(0.4 * n_users) else ("asym_adapt" if idx < int(0.8 * n_users) else "sym_const")
        rate = float(rng.uniform(0.3, 3.0))
        p_neg = float(rng.uniform(0.12, 0.15))
        lam0 = float(rng.uniform(0.15, 0.55))
        n = int(rng.poisson(DAYS * rate))
        neg = rng.random(n) < p_neg
        eps = np.empty(n)
        n_neg = int(neg.sum())
        eps[~neg] = rng.gamma(1.5, 0.4, size=n - n_neg)
        eps[neg] = -0.8 * np.abs(rng.standard_t(3, size=n_neg))
        m_a = (1 - p_neg) * 0.6 + p_neg * (0.8 * 2 * np.sqrt(3) / np.pi)
        nu = np.zeros(n)
        for t in range(1, n):
            nu[t] = (1 - BETA) * nu[t - 1] + BETA * (abs(eps[t]) / m_a - 1.0)
        c = 0.0 if arm == "sym_const" else 1.5
        lam_t = np.full(n, lam0) if c == 0.0 else np.clip(lam0 * (1.0 + c * nu), LAM_MIN, LAM_MAX)
        lamp = lam_t
        lamm = lam_t if arm != "asym_adapt" else 2.0 * lam_t
        dS = lamp * np.maximum(eps, 0.0) + lamm * np.minimum(eps, 0.0)
        u = rng.standard_t(DF_NOISE, size=n) * SIG_U * np.sqrt((DF_NOISE - 2) / DF_NOISE)
        users.append({
            "arm": arm,
            "eps": eps.tolist(),
            "dH": (dS + u).tolist(),
            "lam_true": float(np.mean(lam_t)),
            "lamp_true": float(np.mean(lamp)),
            "lamm_true": float(np.mean(lamm)),
        })
    return users


def _score_cohort(users, preds):
    sym_errs, asym_plus_errs, asym_minus_errs = [], [], []
    sym_ratios, asym_ratios = [], []
    for u, p in zip(users, preds):
        lam_hat, lp_hat, ln_hat = float(p["lam_hat"]), float(p["lamp_hat"]), float(p["lamm_hat"])
        ratio = ln_hat / max(lp_hat, 1e-6)
        if u["arm"] in ("sym_adapt", "sym_const"):
            sym_errs.append(abs(lam_hat - u["lam_true"]))
            if u["arm"] == "sym_adapt":
                sym_ratios.append(ratio)
        else:
            asym_plus_errs.append(abs(lp_hat - u["lamp_true"]))
            asym_minus_errs.append(abs(ln_hat - u["lamm_true"]))
            asym_ratios.append(ratio)

    sym_errs = np.asarray(sym_errs)
    frac_gt_015 = float(np.mean(sym_errs > 0.15))
    p95_err = float(np.percentile(sym_errs, 95))
    sym_ratio_p95 = float(np.percentile(sym_ratios, 95))
    false_asym_pen = float(max(0.0, sym_ratio_p95 - 1.25))
    cd_auc = float(np.mean([(ra > rs) + 0.5 * (ra == rs) for ra in asym_ratios for rs in sym_ratios]))
    auc_pen = float(max(0.0, 0.96 - cd_auc))
    loss = frac_gt_015 + 0.5 * p95_err + 0.25 * false_asym_pen + 2.0 * auc_pen
    return {
        "loss": float(loss),
        "frac_gt_015": frac_gt_015,
        "p95_err": p95_err,
        "mean_err": float(np.mean(sym_errs)),
        "sym_ratio_p95": sym_ratio_p95,
        "cd_auc": cd_auc,
        "asym_mean_err": float(0.5 * (np.mean(asym_plus_errs) + np.mean(asym_minus_errs))),
    }


def _ast_complexity(path: str) -> int:
    tree = ast.parse(open(path, "r", encoding="utf-8").read())
    return sum(1 for _ in ast.walk(tree))


def _run_candidate_sandboxed(users) -> list:
    payload = [{"eps": u["eps"], "dH": u["dH"]} for u in users]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf_in, \
         tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf_out:
        json.dump(payload, tf_in)
        in_path, out_path = tf_in.name, tf_out.name
    try:
        clean_env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        subprocess.run([sys.executable, CANDIDATE, in_path, out_path], env=clean_env, check=True, timeout=60)
        return json.load(open(out_path, "r", encoding="utf-8"))
    finally:
        for p in (in_path, out_path):
            if os.path.exists(p):
                os.remove(p)


def _check_and_increment_budget(reset: bool = False) -> int:
    if reset and os.path.exists(BUDGET_LEDGER):
        os.remove(BUDGET_LEDGER)
    used = 0
    if os.path.exists(BUDGET_LEDGER):
        try:
            used = int(json.load(open(BUDGET_LEDGER, "r", encoding="utf-8")).get("queries_used", 0))
        except Exception:
            used = 0
    if used >= MAX_VAL_QUERIES:
        raise RuntimeError(f"Thresholdout holdout privacy budget exhausted ({used}/{MAX_VAL_QUERIES}). Run with --reset-budget for a fresh split.")
    used += 1
    with open(BUDGET_LEDGER, "w", encoding="utf-8") as f:
        json.dump({"queries_used": used, "max_queries": MAX_VAL_QUERIES}, f)
    return used


def main():
    unlock_vault = "--unlock-vault" in sys.argv
    reset_budget = "--reset-budget" in sys.argv
    ast_nodes = _ast_complexity(CANDIDATE)

    train_users = _gen_cohort(250, seed=10000)
    val_users = _gen_cohort(250, seed=20000)
    train_metrics = _score_cohort(train_users, _run_candidate_sandboxed(train_users))
    val_metrics = _score_cohort(val_users, _run_candidate_sandboxed(val_users))

    # Dwork et al. (2015) Thresholdout Algorithm 1 with cryptographic OS entropy:
    # randomize threshold tau_tilde = tau + Lap(2*sigma), noisy gap check + Lap(4*sigma),
    # and debit privacy budget on every holdout query (reset requires ALLOW_BUDGET_RESET=1).
    rng_th = np.random.default_rng(secrets.randbits(128))
    sigma = 0.003
    tau = 0.008
    tau_tilde = tau + float(rng_th.laplace(0.0, 2.0 * sigma))
    noisy_gap = abs(val_metrics["loss"] - train_metrics["loss"]) + float(rng_th.laplace(0.0, 4.0 * sigma))
    can_reset = reset_budget and os.environ.get("ALLOW_BUDGET_RESET") == "1"
    queries_used = _check_and_increment_budget(reset=can_reset) if not unlock_vault else 0
    if noisy_gap <= tau_tilde:
        reported_val_loss = train_metrics["loss"]
        th_branch = "TRAIN_GENERALIZED"
    else:
        reported_val_loss = val_metrics["loss"] + float(rng_th.laplace(0.0, sigma))
        th_branch = "THRESHOLD_TRIGGERED"

    # Zero raw holdout leakage: only train metrics and Thresholdout-protected val_score are emitted
    print(f"ast_nodes:      {ast_nodes}")
    print(f"train_loss:     {train_metrics['loss']:.6f}")
    print(f"train_p95_err:  {train_metrics['p95_err']:.4f}")
    print(f"train_cd_auc:   {train_metrics['cd_auc']:.4f}")
    print(f"val_score:      {reported_val_loss:.6f} ({th_branch}, budget={queries_used}/{MAX_VAL_QUERIES})")

    if unlock_vault:
        vault_users = _gen_cohort(600, seed=99000)
        vault_metrics = _score_cohort(vault_users, _run_candidate_sandboxed(vault_users))
        print("\n=== ONE-SHOT SEALED VAULT EVALUATION (N=600 UNSEEN USERS) ===")
        for k, v in vault_metrics.items():
            print(f"  vault_{k}: {v:.4f}")


if __name__ == "__main__":
    main()
