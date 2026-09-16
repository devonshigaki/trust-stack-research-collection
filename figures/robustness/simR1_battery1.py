#!/usr/bin/env python3
"""
SIM-R1 Battery 1 — structural-misspecification arm ("circular certification" fix).

Ground truth: master law (math_repairs.md §M4.1), GTT preset (r=1, delta_S=0):
    S_{t+1} = S_t + lambda_t * eps_t          (symmetric arm)
    S_{t+1} = S_t + lam+_t max(eps,0) + lam-_t min(eps,0)   (asymmetric arm)
with an ADAPTIVE Behrens-style volatility-linked gain:
    nu_t   = (1-beta) nu_{t-1} + beta (|eps_t|/m_a - 1),   beta=0.10, nu_0=0
    lam_t  = lam0 * (1 + c * nu_t),  clipped to [0.02, 1.5]
nu_t is a dimensionless centered EWMA of recent |eps| volatility relative to the
user's own stream mean m_a = E|eps|; lam_t rises after large mismatches
(change-point-flavored gain, cf. Behrens et al. 2007). E[lam_t] = lam0 when the
clip does not bind (verified empirically).

Cadence/noise spec matches the prior battery (whitepaper §3.4, Figure 8):
N=300 users; per-user rate ~ U[0.3, 3.0] events/day over 365 days (Poisson);
mixed-sign eps streams, 12-15% negative with heavier-tailed betrayals;
observation noise Student-t(df=4).

Estimator: the stack's constant-lambda Kalman/EM — constant-gain state-space
    state:  lam (scalar, process var Q = 0 -> constant gain restriction)
    obs:    dH_t = lam * eps_t + u_t,  u ~ N(0, R)   [misspecified: truth t_4]
EM over (lam, R); the Kalman recursions with Q=0 reduce exactly to Gaussian-MLE
regression dH ~ eps (verified to machine precision below).

Two-gain variant: obs dH_t = lam+ * eps+_t + lam- * eps-_t + u_t (orthogonal
regressors), same Gaussian-MLE/EM.

Seed 42. numpy/matplotlib/scipy only.
"""
import numpy as np
import json

RNG = np.random.default_rng(42)

# ---------------- generator ----------------
N_USERS   = 300
DAYS      = 365
RATE_LO, RATE_HI = 0.3, 3.0
P_NEG_LO, P_NEG_HI = 0.12, 0.15
BETA      = 0.10          # EWMA rate of the volatility link
LAM_MIN, LAM_MAX = 0.02, 1.5
DF_NOISE  = 4             # Student-t df of observation noise
SIG_U     = 0.10          # scale of observation noise (calibrated: constant-arm
                          # recovery error ~ prior battery's 0.0074)

def eps_moments(p_neg):
    """Analytic E|eps| and E[eps^2] for the mixture.
    positives: Gamma(k=1.5, theta=0.4): mean .6, E^2 = k(k+1)theta^2 = 0.6
    negatives: -0.8*|t_3|: E|t3| = 2*sqrt(3)/pi, E[t3^2] = 3."""
    m_pos, m2_pos = 0.6, 0.6
    m_neg = 0.8 * 2 * np.sqrt(3) / np.pi          # 0.8822
    m2_neg = 0.64 * 3.0                            # 1.92 (heavier-tailed)
    m_a  = (1 - p_neg) * m_pos + p_neg * m_neg
    m2   = (1 - p_neg) * m2_pos + p_neg * m2_neg
    return m_a, m2

def gen_eps(n, p_neg, rng):
    neg = rng.random(n) < p_neg
    eps = np.empty(n)
    n_neg = int(neg.sum())
    eps[~neg] = rng.gamma(1.5, 0.4, size=n - n_neg)
    eps[neg]  = -0.8 * np.abs(rng.standard_t(3, size=n_neg))
    return eps

def gen_user(rate, p_neg, lam0, c, rng, mode="symmetric", lam0_const=False):
    """Returns dict with eps, lam_t (common gain), lamp/lamm trajectories, dH."""
    n = rng.poisson(DAYS * rate)
    eps = gen_eps(n, p_neg, rng)
    m_a, _ = eps_moments(p_neg)
    nu = np.zeros(n)
    for t in range(1, n):
        nu[t] = (1 - BETA) * nu[t-1] + BETA * (abs(eps[t]) / m_a - 1.0)
    if lam0_const:
        lam_t = np.full(n, lam0)
    else:
        lam_t = np.clip(lam0 * (1 + c * nu), LAM_MIN, LAM_MAX)
    if mode == "symmetric":
        lamp, lamm = lam_t, lam_t
    else:                       # asymmetric: lam- = 2 lam+
        lamp, lamm = lam_t, 2.0 * lam_t
    dS = lamp * np.maximum(eps, 0) + lamm * np.minimum(eps, 0)
    tscale = SIG_U * np.sqrt((DF_NOISE - 2) / DF_NOISE)   # -> Var(u)=SIG_U^2
    u = rng.standard_t(DF_NOISE, size=n) * tscale
    dH = dS + u
    return dict(eps=eps, lam_t=lam_t, lamp=lamp, lamm=lamm, dH=dH, n=n)

# ---------------- estimators ----------------
def em_constant_gain(eps, dH):
    """Kalman/EM with constant-gain restriction (Q=0, diffuse prior P0=1e6).
    With Q=0 the filtered/smoothed state after one E-step is closed form:
        lam_hat = (lam0/P0 + sum(eps*dH)/R) / (1/P0 + sum(eps^2)/R)
    which is R-independent, so EM converges in one cycle; M-step: R=mean(resid^2).
    Equality with the explicit KF recursion is verified on 25 users below."""
    P0, lam0_init = 1e6, 0.3
    lam = (lam0_init / P0 + np.sum(eps * dH)) / (1.0 / P0 + np.sum(eps**2))
    R = float(np.mean((dH - eps * lam)**2))
    lam_ols = float(np.sum(eps * dH) / np.sum(eps**2))
    return float(lam), lam_ols, R

def kf_explicit(eps, dH, R, P0=1e6, lam0=0.3):
    """Explicit scalar Kalman-filter recursion, Q=0 (verification only)."""
    l_f, P_f = lam0, P0
    for t in range(len(eps)):
        K = P_f * eps[t] / (eps[t]**2 * P_f + R)
        l_f = l_f + K * (dH[t] - eps[t] * l_f)
        P_f = (1 - K * eps[t]) * P_f
    return l_f

def fit_two_gain(eps, dH):
    ep, em = np.maximum(eps, 0), np.minimum(eps, 0)
    lamp = float(np.sum(ep * dH) / np.sum(ep**2))
    lamm = float(np.sum(em * dH) / np.sum(em**2))
    return lamp, lamm

# ---------------- arms ----------------
def run_arm(c, mode, const_lam, seed_offset=0, lam0_lo=0.15, lam0_hi=0.55):
    rng = np.random.default_rng(42 + seed_offset)
    rows = []
    for i in range(N_USERS):
        rate  = rng.uniform(RATE_LO, RATE_HI)
        p_neg = rng.uniform(P_NEG_LO, P_NEG_HI)
        lam0  = rng.uniform(lam0_lo, lam0_hi)
        g = gen_user(rate, p_neg, lam0, c, rng, mode=mode, lam0_const=const_lam)
        eps, dH = g["eps"], g["dH"]
        lam_kf, lam_ols, R = em_constant_gain(eps, dH)
        lamp_hat, lamm_hat = fit_two_gain(eps, dH)
        # targets: time-average gain and eps^2-weighted gain (what a constant
        # gain identifies analytically: lam_hat -> sum(lam_t eps_t^2)/sum(eps_t^2))
        ep2 = np.maximum(eps, 0)**2; em2 = np.minimum(eps, 0)**2
        if mode == "symmetric":
            lam_bar   = float(np.mean(g["lam_t"]))
            lam_bar_w = float(np.sum(g["lam_t"] * eps**2) / np.sum(eps**2))
            lamp_true = lamm_true = lam_bar
            lamp_true_w = float(np.sum(g["lamp"] * ep2) / np.sum(ep2))
            lamm_true_w = float(np.sum(g["lamm"] * em2) / np.sum(em2))
        else:
            lam_bar   = float(np.mean(g["lamp"]))   # reference = build gain
            lam_bar_w = float(np.sum(g["lamp"] * eps**2) / np.sum(eps**2))
            lamp_true = float(np.mean(g["lamp"]))
            lamm_true = float(np.mean(g["lamm"]))
            lamp_true_w = float(np.sum(g["lamp"] * ep2) / np.sum(ep2))
            lamm_true_w = float(np.sum(g["lamm"] * em2) / np.sum(em2))
        rows.append(dict(i=i, n=g["n"], rate=rate, p_neg=p_neg, lam0=lam0,
                         lam_sd=float(np.std(g["lam_t"])),
                         lam_bar=lam_bar, lam_bar_w=lam_bar_w,
                         lam_kf=lam_kf, lam_ols=lam_ols, R=R,
                         lamp_hat=lamp_hat, lamm_hat=lamm_hat,
                         lamp_true=lamp_true, lamm_true=lamm_true,
                         lamp_true_w=lamp_true_w, lamm_true_w=lamm_true_w))
    return rows

def summarize(err):
    err = np.abs(np.asarray(err))
    return dict(mean=float(err.mean()), p95=float(np.percentile(err, 95)),
                max=float(err.max()),
                frac_gt_015=float(np.mean(err > 0.15)))

if __name__ == "__main__":
    out = {}

    # Arm A: constant-lambda truth (replication of the prior battery's spec)
    A = run_arm(c=None, mode="symmetric", const_lam=True, seed_offset=1000)
    errA = [r["lam_kf"] - r["lam_bar"] for r in A]
    out["A_constant_truth"] = summarize(errA)
    out["A_n_events"] = dict(median=float(np.median([r["n"] for r in A])),
                             min=int(min(r["n"] for r in A)),
                             max=int(max(r["n"] for r in A)))
    out["A_kf_vs_ols_maxdiff"] = float(max(abs(r["lam_kf"] - r["lam_ols"]) for r in A))
    out["A_lam_bar_range"] = [float(min(r["lam_bar"] for r in A)),
                              float(max(r["lam_bar"] for r in A))]
    out["A_pop_mean_hat"] = float(np.mean([r["lam_kf"] for r in A]))
    out["A_pop_mean_true"] = float(np.mean([r["lam_bar"] for r in A]))

    # Arm B: adaptive-lambda truth, primary coupling c = 1.5
    B = run_arm(c=1.5, mode="symmetric", const_lam=False, seed_offset=2000)
    errB_bar = [r["lam_kf"] - r["lam_bar"] for r in B]
    errB_w   = [r["lam_kf"] - r["lam_bar_w"] for r in B]
    out["B_adaptive_c1.5_vs_timeavg"] = summarize(errB_bar)
    out["B_adaptive_c1.5_vs_weighted"] = summarize(errB_w)
    out["B_pop_mean_hat"] = float(np.mean([r["lam_kf"] for r in B]))
    out["B_pop_mean_true_timeavg"] = float(np.mean([r["lam_bar"] for r in B]))
    out["B_pop_mean_true_weighted"] = float(np.mean([r["lam_bar_w"] for r in B]))
    out["B_clip_rate"] = None  # filled below by re-run check

    # c sensitivity
    out["c_scan"] = {}
    for c in [0.75, 1.5, 3.0]:
        rows = run_arm(c=c, mode="symmetric", const_lam=False, seed_offset=2000)
        err_bar = [r["lam_kf"] - r["lam_bar"] for r in rows]
        err_w   = [r["lam_kf"] - r["lam_bar_w"] for r in rows]
        out["c_scan"][c] = dict(vs_timeavg=summarize(err_bar),
                                vs_weighted=summarize(err_w),
                                pop_mean_hat=float(np.mean([r["lam_kf"] for r in rows])),
                                pop_mean_true=float(np.mean([r["lam_bar"] for r in rows])))

    # Arm C: adaptive ASYMMETRIC truth (lam- = 2 lam+), two-gain estimator
    C = run_arm(c=1.5, mode="asymmetric", const_lam=False, seed_offset=3000)
    ratios_C = np.array([r["lamm_hat"]/r["lamp_hat"] for r in C])
    out["C_asym"] = dict(
        err_plus_vs_timeavg=summarize([r["lamp_hat"] - r["lamp_true"] for r in C]),
        err_minus_vs_timeavg=summarize([r["lamm_hat"] - r["lamm_true"] for r in C]),
        err_plus_vs_weighted=summarize([r["lamp_hat"] - r["lamp_true_w"] for r in C]),
        err_minus_vs_weighted=summarize([r["lamm_hat"] - r["lamm_true_w"] for r in C]),
        ratio_weighted_true=float(np.mean([r["lamm_true_w"]/r["lamp_true_w"] for r in C])),
        ratio_hat_mean=float(np.mean([r["lamm_hat"]/r["lamp_hat"] for r in C])),
        ratio_hat_sd=float(np.std([r["lamm_hat"]/r["lamp_hat"] for r in C])),
        ratio_hat_p05=float(np.percentile([r["lamm_hat"]/r["lamp_hat"] for r in C], 5)),
        ratio_hat_p95=float(np.percentile([r["lamm_hat"]/r["lamp_hat"] for r in C], 95)),
        ratio_true=float(np.mean([r["lamm_true"]/r["lamp_true"] for r in C])),
        pop_lamp_hat=float(np.mean([r["lamp_hat"] for r in C])),
        pop_lamm_hat=float(np.mean([r["lamm_hat"] for r in C])),
        pop_lamp_true=float(np.mean([r["lamp_true"] for r in C])),
        pop_lamm_true=float(np.mean([r["lamm_true"] for r in C])))

    # Arm D: adaptive SYMMETRIC truth, two-gain estimator (asymmetry control)
    D = run_arm(c=1.5, mode="symmetric", const_lam=False, seed_offset=4000)
    ratios_D = np.array([r["lamm_hat"]/r["lamp_hat"] for r in D])
    # AUC: can the two-gain ratio separate true 2x asymmetry (C) from adaptive
    # symmetric truth (D)?
    auc = float(np.mean([(rc > rd) + 0.5*(rc == rd) for rc in ratios_C for rd in ratios_D]))
    out["CD_ratio_AUC"] = auc
    out["D_sym_control"] = dict(
        ratio_hat_mean=float(np.mean(ratios_D)),
        ratio_hat_sd=float(np.std(ratios_D)),
        ratio_hat_p05=float(np.percentile(ratios_D, 5)),
        ratio_hat_p95=float(np.percentile(ratios_D, 95)),
        frac_ratio_outside_1pm03=float(np.mean([abs(x-1) > 0.3 for x in ratios_D])))

    # Arm E: planted lambda = 0 negative control (adaptive machinery irrelevant)
    E = run_arm(c=0.0, mode="symmetric", const_lam=True, seed_offset=5000,
                lam0_lo=0.0, lam0_hi=0.0)
    out["E_zero_control"] = dict(max_abs_lamhat=float(max(abs(r["lam_kf"]) for r in E)),
                                 mean_abs_lamhat=float(np.mean([abs(r["lam_kf"]) for r in E])))

    # Verification: closed-form Kalman/EM == explicit KF recursion == OLS
    rng = np.random.default_rng(42 + 9000)
    kf_max, ols_max = 0.0, 0.0
    for _ in range(25):
        rate, p_neg, lam0 = rng.uniform(0.3, 3.0), rng.uniform(0.12, 0.15), rng.uniform(0.15, 0.55)
        g = gen_user(rate, p_neg, lam0, 1.5, rng)
        lam_cf, lam_ols, R = em_constant_gain(g["eps"], g["dH"])
        lam_kf2 = kf_explicit(g["eps"], g["dH"], R)
        kf_max = max(kf_max, abs(lam_cf - lam_kf2))
        ols_max = max(ols_max, abs(lam_cf - lam_ols))
    out["verification"] = dict(closedform_vs_explicitKF_maxdiff=kf_max,
                               closedform_vs_OLS_maxdiff=ols_max)

    # dump per-user rows for figures
    np.savez("/mnt/agents/output/figures/robustness/simR1_battery1_rows.npz",
             A_err=np.array([r["lam_kf"] - r["lam_bar"] for r in A]),
             B_err_bar=np.array([r["lam_kf"] - r["lam_bar"] for r in B]),
             B_err_w=np.array([r["lam_kf"] - r["lam_bar_w"] for r in B]),
             B_lam_bar=np.array([r["lam_bar"] for r in B]),
             B_lam_bar_w=np.array([r["lam_bar_w"] for r in B]),
             B_lam_hat=np.array([r["lam_kf"] for r in B]),
             B_n=np.array([r["n"] for r in B]),
             A_lam_bar=np.array([r["lam_bar"] for r in A]),
             A_lam_hat=np.array([r["lam_kf"] for r in A]),
             C_lamp_hat=np.array([r["lamp_hat"] for r in C]),
             C_lamm_hat=np.array([r["lamm_hat"] for r in C]),
             C_lamp_true=np.array([r["lamp_true"] for r in C]),
             C_lamm_true=np.array([r["lamm_true"] for r in C]),
             C_lamp_true_w=np.array([r["lamp_true_w"] for r in C]),
             C_lamm_true_w=np.array([r["lamm_true_w"] for r in C]),
             C_ratio=np.array(ratios_C),
             D_ratio=np.array(ratios_D),
             D_lamp_hat=np.array([r["lamp_hat"] for r in D]),
             D_lamm_hat=np.array([r["lamm_hat"] for r in D]),
             B_lam_sd=np.array([r["lam_sd"] for r in B]))

    # clip diagnostics for c=1.5 and c=3.0 (does E[lam_t]=lam0 survive clipping?)
    for c, tag in [(1.5, "clip_c1.5"), (3.0, "clip_c3.0")]:
        rng = np.random.default_rng(42 + 2000)
        ratios, at_floor = [], 0
        for i in range(N_USERS):
            rate  = rng.uniform(RATE_LO, RATE_HI)
            p_neg = rng.uniform(P_NEG_LO, P_NEG_HI)
            lam0  = rng.uniform(0.15, 0.55)
            n = rng.poisson(DAYS * rate)
            eps = gen_eps(n, p_neg, rng)
            m_a, _ = eps_moments(p_neg)
            nu = np.zeros(n)
            for t in range(1, n):
                nu[t] = (1 - BETA) * nu[t-1] + BETA * (abs(eps[t]) / m_a - 1.0)
            raw = lam0 * (1 + c * nu)
            at_floor += int(np.sum(raw < LAM_MIN))
            ratios.append(np.mean(np.clip(raw, LAM_MIN, LAM_MAX)) / lam0)
        out[tag] = dict(mean_realized_over_lam0=float(np.mean(ratios)),
                        frac_events_clipped=float(at_floor / sum(r["n"] for r in B)))

    with open("/mnt/agents/output/figures/robustness/simR1_battery1_stats.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
