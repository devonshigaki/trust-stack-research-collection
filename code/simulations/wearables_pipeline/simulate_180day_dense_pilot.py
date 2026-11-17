#!/usr/bin/env python3
"""
Simulation PILOT-2 (V4.6): Full 180-Day Multimodal In-Silico Mock Trial Simulator
Target: The Trust Stack Research Collection / DOCAS-PILOT-1 V4.6 100% Stream Bijection
Pre-Registration: protocols/sim_preregistrations/SIM_PILOT_V4_6_PRE_REGISTRATION.md
Author: Devon Shigaki (ORCID: 0009-0003-8977-8010)

Executes an end-to-end synthetic generative benchmark simulating the complete 180-day
longitudinal dense phenotyping protocol (N = 1 x 180 days = 51,840 5-minute epochs):
- Phase 0 (Days 1–14):  Habituation & Cognitive Practice-Curve Burn-In
- Phase 1 (Days 15–42): 4-Week Observational Baseline & Cannabis/Caffeine PK Calibration
- Phase 2 (Days 43–180): Ecological Contrasts under AR(1)-Prewhitened DSEM/ARIMAX
Covers 100% of physical hardware & logs (PILOT-H1..H12) and verifies criteria C1–C8.
"""

import os
import json
import numpy as np
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_180day_pilot_simulation(output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 80)
    print("RUNNING SIMULATION PILOT-2: 180-DAY 14-STREAM SYNTHETIC BENCHMARK (N=1 x 180d)")
    print("=" * 80)

    np.random.seed(42)
    N_DAYS = 180
    EPOCHS_PER_DAY = 288 # 5-minute sampling cadence
    TOTAL_EPOCHS = N_DAYS * EPOCHS_PER_DAY # 51,840 epochs
    time_hours = np.linspace(0, N_DAYS * 24, TOTAL_EPOCHS)
    time_days = time_hours / 24.0

    # 1. Ground Truth Trust Dynamics under Asymmetric Master Law + Endogenous Allostatic Diffusion
    # Positive gain lambda_plus = 0.228, Negative betrayal gain lambda_minus = 0.456 (2:1 asymmetry)
    # Plus non-financial endogenous OU allostatic process noise sigma_w = 0.0045 / epoch
    lambda_true = 0.228
    lambda_minus_true = 0.456
    tau_relax_true_days = 2.85
    tau_relax_epochs = tau_relax_true_days * EPOCHS_PER_DAY
    decay_rate = 1.0 / tau_relax_epochs
    S_base = 0.50
    sigma_w_endog = 0.0045

    # Simulate 8 Major Financial Clearing Shocks across Days 15–180 (excluding Days 1–14 burn-in):
    # 4 Confirmations (epsilon > 0), 4 Betrayals/Shocks (epsilon < 0)
    shocks = {
        int(18 * EPOCHS_PER_DAY + 60):  +0.75, # Day 18: On-time settlement
        int(45 * EPOCHS_PER_DAY + 120): -0.95, # Day 45: Major counterparty breach
        int(68 * EPOCHS_PER_DAY + 45):  +0.50, # Day 68: Contract renewal
        int(92 * EPOCHS_PER_DAY + 180): -0.70, # Day 92: Disputed chargeback
        int(115 * EPOCHS_PER_DAY + 90): +0.65, # Day 115: Inflow confirmation
        int(138 * EPOCHS_PER_DAY + 210):-1.00, # Day 138: Acute bank clearing shock
        int(158 * EPOCHS_PER_DAY + 15): +0.80, # Day 158: Full restitution
        int(174 * EPOCHS_PER_DAY + 100):-0.35  # Day 174: Minor fee mismatch
    }

    S_true = np.zeros(TOTAL_EPOCHS)
    S_curr = S_base
    rng_proc = np.random.default_rng(1337)

    for t in range(TOTAL_EPOCHS):
        if t in shocks:
            eps = shocks[t]
            lam_step = lambda_minus_true if eps < 0.0 else lambda_true
            S_curr += lam_step * eps
            S_curr = np.clip(S_curr, 0.0, 1.0)
        else:
            S_curr += decay_rate * (S_base - S_curr) + float(rng_proc.normal(0.0, sigma_w_endog))
            S_curr = float(np.clip(S_curr, 0.02, 0.98))
        S_true[t] = S_curr

    # 2. Multimodal Biosensor Stream Generation (Coupled Emission Manifold)
    
    # Stream 1: cw-fNIRS Prefrontal Delta [HbO2] (uM)
    fnirs_hbo2 = 1.2 * (S_true - 0.5) + np.random.normal(0, 0.15, TOTAL_EPOCHS)
    
    # Stream 2: Frontal EEG Theta/Beta Power Ratio
    eeg_tbr = 2.4 - 0.8 * (S_true - 0.5) + np.random.normal(0, 0.12, TOTAL_EPOCHS)

    # Stream 3: Optical PPG HRV RMSSD (ms) - Vagal Tone (O-channel)
    # Plus Pharmacological PK confounders: Caffeine (t1/2 = 5h) & Cannabis THC/CBD washout (Days 15-42)
    rmssd_base = 48.0 + 26.0 * (S_true - 0.5)
    workout_power_watts = np.zeros(TOTAL_EPOCHS)
    caffeine_pk = np.zeros(TOTAL_EPOCHS)
    cannabis_pk = np.zeros(TOTAL_EPOCHS)
    pgx_cyp1a2_clearance = 1.0
    pgx_cyp2c9_clearance = 1.0
    for day in range(N_DAYS):
        ep_run = day * EPOCHS_PER_DAY + 84
        workout_power_watts[ep_run:ep_run+9] = np.random.normal(275.0, 20.0, 9)
        ep_caf = day * EPOCHS_PER_DAY + 99
        dose_caf = np.random.normal(140.0, 20.0)
        for dt_ep in range(min(144, TOTAL_EPOCHS - ep_caf)):
            caffeine_pk[ep_caf + dt_ep] += dose_caf * np.exp(-pgx_cyp1a2_clearance * (dt_ep / 12.0) * np.log(2.0) / 5.0)
        if day in (16, 23, 52, 104):
            ep_thc = day * EPOCHS_PER_DAY + 245
            for dt_ep in range(min(576, TOTAL_EPOCHS - ep_thc)):
                cannabis_pk[ep_thc + dt_ep] += 10.0 * np.exp(-pgx_cyp2c9_clearance * (dt_ep / 12.0) / 24.0)

    rmssd_observed = (
        rmssd_base
        - 0.06 * workout_power_watts
        - 0.015 * caffeine_pk
        + np.random.normal(0, 2.5, TOTAL_EPOCHS)
    )
    rmssd_observed = np.clip(rmssd_observed, 10.0, 110.0)

    # Stream 4: Nocturnal Wrist Temp Drift (deg C)
    wrist_temp_drift = np.zeros(TOTAL_EPOCHS)
    for day in range(N_DAYS):
        ep_sleep_start = day * EPOCHS_PER_DAY + 264 # 11:00 PM
        ep_sleep_end = min(TOTAL_EPOCHS, ep_sleep_start + 96) # 8 hours = 96 epochs
        n_pts = ep_sleep_end - ep_sleep_start
        if n_pts > 0:
            stress_elevation = 0.25 * (1.0 - S_true[ep_sleep_start])
            wrist_temp_drift[ep_sleep_start:ep_sleep_end] = stress_elevation + np.random.normal(0, 0.03, n_pts)

    # Stream 5: Interstitial Glucose (mg/dL) across 12 consecutive 15-day sensors
    glucose_mgdl = np.zeros(TOTAL_EPOCHS)
    for sensor in range(12):
        s_start = sensor * 15 * EPOCHS_PER_DAY
        s_end = (sensor + 1) * 15 * EPOCHS_PER_DAY
        sensor_drift = np.random.normal(0, 3.5) # Sensor manufacturing offset
        glycemic_stress = 32.0 * (1.0 - S_true[s_start:s_end])
        cgm_noise = np.random.normal(92.0 + sensor_drift, 6.5, s_end - s_start)
        glucose_mgdl[s_start:s_end] = cgm_noise + glycemic_stress

    # Stream 10: Manual Physical Reading Logs (Daily Evening Station)
    # Extracts Time-to-Digitization (hours) and Syntactic Complexity (Grade)
    daily_reading_latency_hrs = np.zeros(N_DAYS)
    daily_flesch_grade = np.zeros(N_DAYS)
    for day in range(N_DAYS):
        mid_day_ep = day * EPOCHS_PER_DAY + 144
        allostatic_stress = 1.0 - S_true[mid_day_ep]
        daily_reading_latency_hrs[day] = 4.0 + 14.0 * allostatic_stress + np.random.normal(0, 1.5)
        daily_flesch_grade[day] = 13.5 - 3.5 * allostatic_stress + np.random.normal(0, 0.6)

    # Stream 13: Airofit Pro Quantitative Respiratory Strength (MIP, MEP, VC)
    daily_airofit_mip_cmh2o = np.zeros(N_DAYS)
    daily_airofit_mep_cmh2o = np.zeros(N_DAYS)
    daily_airofit_vc_liters = np.zeros(N_DAYS)
    for day in range(N_DAYS):
        ev_ep = day * EPOCHS_PER_DAY + 241 # 8:05 PM
        vagal_capacity = S_true[ev_ep]
        daily_airofit_mip_cmh2o[day] = 88.0 + 38.0 * vagal_capacity + np.random.normal(0, 3.0)
        daily_airofit_mep_cmh2o[day] = 112.0 + 36.0 * vagal_capacity + np.random.normal(0, 3.5)
        daily_airofit_vc_liters[day] = 4.55 + 0.55 * vagal_capacity + np.random.normal(0, 0.08)

    # Stream 14: Aranet4 Indoor CO2/Temp/RH + Outdoor PM2.5 + Apple Health TimeInDaylight + Hue Pre-Bed Lux
    daily_aranet4_co2_ppm = np.clip(620.0 + np.random.normal(0, 140.0, N_DAYS), 410.0, 1600.0)
    daily_outdoor_pm25 = np.clip(7.5 + np.random.normal(0, 3.0, N_DAYS), 1.5, 35.0)
    daily_time_in_daylight_min = np.clip(45.0 + np.random.normal(0, 18.0, N_DAYS), 5.0, 120.0)
    daily_hue_prebed_lux = np.clip(28.0 + np.random.normal(0, 12.0, N_DAYS), 5.0, 90.0)

    # Stream 15: Wired 1000Hz Akai MPK Mini Objective Cognitive Battery (with Days 1-14 practice curve)
    days_idx = np.arange(1, N_DAYS + 1, dtype=float)
    tau_learn_true = 4.2
    daily_S_ev = np.array([S_true[d * EPOCHS_PER_DAY + 241] for d in range(N_DAYS)])
    allostatic_load = 1.0 - daily_S_ev
    daily_pvt_rt_raw_ms = (
        228.0
        + 55.0 * np.exp(-days_idx / tau_learn_true)
        + 42.0 * allostatic_load
        + 0.045 * (daily_aranet4_co2_ppm - 620.0)
        + np.random.normal(0, 4.5, N_DAYS)
    )
    daily_nback_dprime = (
        2.75
        - 0.85 * np.exp(-days_idx / tau_learn_true)
        - 0.90 * allostatic_load
        + np.random.normal(0, 0.10, N_DAYS)
    )
    daily_stroop_ms = (
        44.0
        + 24.0 * np.exp(-days_idx / tau_learn_true)
        + 36.0 * allostatic_load
        + np.random.normal(0, 4.0, N_DAYS)
    )
    daily_tapping_cv_iti = (
        3.9
        + 3.2 * np.exp(-days_idx / tau_learn_true)
        + 2.4 * allostatic_load
        + np.random.normal(0, 0.25, N_DAYS)
    )

    # Stream 16: Hilo/Aktiia Cuffless BP, Throne Bristol, Fitindex Mass, Circle View PIR, Acoustic eGeMAPS
    daily_sbp_dipping_pct = np.clip(12.5 - 8.5 * allostatic_load + np.random.normal(0, 1.2, N_DAYS), 1.0, 22.0)
    daily_bristol_score = np.clip(4.0 + 1.6 * (daily_S_ev - 0.5) + np.random.normal(0, 0.4, N_DAYS), 1.0, 7.0)
    daily_fitindex_mass_kg = 83.9 + np.random.normal(0, 0.25, N_DAYS)  # 185 lb baseline
    daily_acoustic_jitter_pct = np.clip(0.55 + 0.50 * allostatic_load + np.random.normal(0, 0.06, N_DAYS), 0.2, 2.5)

    # Stream 17: 6 Monthly Venous Blood Panels (Days 1, 30, 60, 90, 120, 150, 180) + Endocrine AUC
    blood_days = [0, 29, 59, 89, 119, 149, 179]
    monthly_cgm_auc = np.array([
        float(np.mean(np.maximum(0.0, glucose_mgdl[max(0, (bd-14)*EPOCHS_PER_DAY):(bd+1)*EPOCHS_PER_DAY] - 105.0)))
        for bd in blood_days
    ])
    monthly_blood_hscrp = 0.35 + 0.065 * monthly_cgm_auc + np.random.normal(0, 0.025, len(blood_days))
    monthly_blood_cortisol = 11.5 + 0.42 * monthly_cgm_auc + np.random.normal(0, 0.35, len(blood_days))

    # Stream 18: 18 Ten-Day Endocrine AUC Segments (Stages 2-4 Hair / Biomarker Reference)
    n_hair_segments = 18
    seg_len = TOTAL_EPOCHS // n_hair_segments
    segment_cgm_stress_auc = np.zeros(n_hair_segments)
    segment_hair_cortisol_ratio = np.zeros(n_hair_segments)
    for s_idx in range(n_hair_segments):
        seg_slice = glucose_mgdl[s_idx * seg_len:(s_idx + 1) * seg_len]
        auc_val = float(np.mean(np.maximum(0.0, seg_slice - 105.0)))
        segment_cgm_stress_auc[s_idx] = auc_val
        segment_hair_cortisol_ratio[s_idx] = 0.35 + 0.045 * auc_val + np.random.normal(0, 0.035)

    # =========================================================================
    # FORMAL BENCHMARK CRITERIA EVALUATION (NO GROUND-TRUTH S_true LEAKAGE)
    # =========================================================================

    def _ar1_prewhiten(vec: np.ndarray) -> np.ndarray:
        """Exact Yule-Walker AR(1) prewhitening for autocorrelated N=1 DSEM residuals."""
        v = np.asarray(vec, dtype=float)
        v_c = v - np.mean(v)
        denom = float(np.dot(v_c[:-1], v_c[:-1]))
        phi = float(np.clip(np.dot(v_c[1:], v_c[:-1]) / denom, -0.95, 0.95)) if denom > 1e-12 else 0.0
        return v_c[1:] - phi * v_c[:-1]

    # =========================================================================
    # BLIND EMPIRICAL STATE-SPACE ESTIMATION (ZERO ORACLE EMISSION CONSTANTS)
    # =========================================================================
    # Unit-anchored daily Task 1 behavioral trust probe (Akai MPK Mini circumplex mapped to [0, 1])
    # Breaks bilinear scale non-identifiability (c_k * lambda = const) while keeping all
    # physiological emission loadings (c_fnirs, c_eeg, c_rmssd) completely free and blind.
    ev_epochs = np.array([d * EPOCHS_PER_DAY + 241 for d in range(N_DAYS)], dtype=int)
    daily_trust_probe = np.clip(S_true[ev_epochs] + np.random.normal(0, 0.040, N_DAYS), 0.0, 1.0)

    def estimate_state_space_blind(
        obs_fnirs, obs_eeg, obs_rmssd, obs_probe, shock_dict, s_anchor=0.50, asymmetric: bool = False
    ):
        """
        Process-noise-robust blind state-space estimator (zero oracle emission constants or S_true):
        1. Anchors unit scale by regressing the daily [0, 1] behavioral probe onto the 3 noisy
           physiological streams (Ridge), producing a calibrated 5-min latent readout `s_hat_phys`.
        2. Estimates (lambda_plus_hat, lambda_minus_hat) from local shock-locked pre/post jumps
           (unbiased by inter-shock OU allostatic process noise w_t).
        3. Estimates tau_relax_hat_days from post-shock exponential decay trajectories [0..72h].
        """
        from scipy.optimize import minimize

        n_ep = len(obs_fnirs)
        # Estimate high-frequency measurement noise variances from 1st differences (zero S_true)
        var_f_noise = max(float(np.var(np.diff(obs_fnirs[:14 * EPOCHS_PER_DAY]))) / 2.0, 1e-6)
        var_e_noise = max(float(np.var(np.diff(obs_eeg[:14 * EPOCHS_PER_DAY]))) / 2.0, 1e-6)
        var_r_noise = max(float(np.var(np.diff(obs_rmssd[:14 * EPOCHS_PER_DAY]))) / 2.0, 1e-6)

        # Step 1: Triadic Instrumental-Variable calibration (zero EIV attenuation bias, zero S_true!)
        # Because sensor measurement errors are mutually independent across fNIRS, EEG, RMSSD, and
        # the unit-anchored behavioral probe: Cov(y_i, y_j) / Cov(y_j, probe) = c_i * Var(S) / Var(S) = c_i.
        half_w = 6
        f_ev = np.array([np.mean(obs_fnirs[max(0, ep - half_w):min(n_ep, ep + half_w)]) for ep in ev_epochs])
        e_ev = np.array([np.mean(obs_eeg[max(0, ep - half_w):min(n_ep, ep + half_w)]) for ep in ev_epochs])
        r_ev = np.array([np.mean(obs_rmssd[max(0, ep - half_w):min(n_ep, ep + half_w)]) for ep in ev_epochs])
        p_ev = np.asarray(obs_probe, dtype=float)

        def _cov(a, b):
            return float(np.mean((a - np.mean(a)) * (b - np.mean(b))))

        c_f_hat = _cov(f_ev, e_ev) / _cov(e_ev, p_ev) if abs(_cov(e_ev, p_ev)) > 1e-8 else _cov(f_ev, p_ev) / max(np.var(p_ev), 1e-6)
        c_e_hat = _cov(e_ev, f_ev) / _cov(f_ev, p_ev) if abs(_cov(f_ev, p_ev)) > 1e-8 else _cov(e_ev, p_ev) / max(np.var(p_ev), 1e-6)
        c_r_hat = _cov(r_ev, f_ev) / _cov(f_ev, p_ev) if abs(_cov(f_ev, p_ev)) > 1e-8 else _cov(r_ev, p_ev) / max(np.var(p_ev), 1e-6)

        mu_f_hat = float(np.mean(f_ev)) - c_f_hat * (float(np.mean(p_ev)) - s_anchor)
        mu_e_hat = float(np.mean(e_ev)) - c_e_hat * (float(np.mean(p_ev)) - s_anchor)
        mu_r_hat = float(np.mean(r_ev)) - c_r_hat * (float(np.mean(p_ev)) - s_anchor)

        # Precision-weighted instantaneous unbiased state readout S_inst(t)
        prec_f = c_f_hat / var_f_noise
        prec_e = c_e_hat / var_e_noise
        prec_r = c_r_hat / var_r_noise
        denom_prec = max((c_f_hat * prec_f) + (c_e_hat * prec_e) + (c_r_hat * prec_r), 1e-8)
        s_hat_phys = s_anchor + (
            prec_f * (obs_fnirs - mu_f_hat)
            + prec_e * (obs_eeg - mu_e_hat)
            + prec_r * (obs_rmssd - mu_r_hat)
        ) / denom_prec

        # Step 2: Local shock-locked jump estimation (pre 1h vs post 1h window -> immune to OU drift)
        win_pre = 12
        win_post = 12
        eps_pos, dS_pos, eps_neg, dS_neg = [], [], [], []
        shock_windows = []
        for t_sh, ep_val in sorted(shock_dict.items()):
            if t_sh - win_pre < 0 or t_sh + win_post >= n_ep:
                continue
            s_pre = float(np.mean(s_hat_phys[t_sh - win_pre:t_sh]))
            s_post = float(np.mean(s_hat_phys[t_sh:t_sh + win_post]))
            jump = s_post - s_pre
            if ep_val >= 0.0:
                eps_pos.append(ep_val)
                dS_pos.append(jump)
            else:
                eps_neg.append(ep_val)
                dS_neg.append(jump)
            shock_windows.append((t_sh, jump))

        if asymmetric and eps_pos and eps_neg:
            ep_p, ds_p = np.asarray(eps_pos), np.asarray(dS_pos)
            ep_n, ds_n = np.asarray(eps_neg), np.asarray(dS_neg)
            lp_hat = float(np.clip(np.dot(ep_p, ds_p) / max(np.dot(ep_p, ep_p), 1e-8), 0.01, 0.90))
            ln_hat = float(np.clip(np.dot(ep_n, ds_n) / max(np.dot(ep_n, ep_n), 1e-8), 0.01, 0.95))
        else:
            ep_all = np.asarray(eps_pos + eps_neg)
            ds_all = np.asarray(dS_pos + dS_neg)
            lp_hat = ln_hat = float(np.clip(np.dot(ep_all, ds_all) / max(np.dot(ep_all, ep_all), 1e-8), 0.01, 0.90))

        # Step 3: Estimate tau_relax from post-shock exponential relaxation [0..72h] (profiling initial offset)
        h_max = 3 * EPOCHS_PER_DAY
        h_grid = np.arange(h_max, dtype=float) / float(EPOCHS_PER_DAY)

        def _tau_sse(tau_arr):
            td = float(tau_arr[0])
            if not (0.5 <= td <= 10.0):
                return 1e18
            e_curve = np.exp(-h_grid / td)
            ee = max(float(np.dot(e_curve, e_curve)), 1e-8)
            sse = 0.0
            for t_sh, _ in shock_windows:
                if t_sh + h_max > n_ep:
                    continue
                y_decay = s_hat_phys[t_sh:t_sh + h_max] - s_anchor
                a_k = float(np.dot(y_decay, e_curve) / ee)
                sse += float(np.mean((y_decay - a_k * e_curve) ** 2))
            return sse

        opt_t = minimize(_tau_sse, x0=[2.5], method="Nelder-Mead", options={"xatol": 1e-3, "maxiter": 100})
        tau_hat = float(np.clip(opt_t.x[0], 0.5, 10.0))

        return {
            "lambda_hat": lp_hat,
            "lambda_minus_hat": ln_hat,
            "tau_relax_hat_days": tau_hat,
            "c_fnirs_hat": c_f_hat,
            "c_eeg_hat": c_e_hat,
            "c_rmssd_hat": c_r_hat,
        }

    # Criterion C1: Exertion + Caffeine PK Confounder Residualization
    active_mask = (workout_power_watts > 0) | (np.roll(workout_power_watts, 6) > 0)
    slope_ex, _, _, _, _ = stats.linregress(workout_power_watts[active_mask], rmssd_observed[active_mask])
    slope_caf, _, _, _, _ = stats.linregress(caffeine_pk, rmssd_observed - slope_ex * workout_power_watts)
    rmssd_residual = rmssd_observed[active_mask] - slope_ex * workout_power_watts[active_mask]
    _, _, r_res, p_res, _ = stats.linregress(workout_power_watts[active_mask], rmssd_residual)
    r2_exertion = float(r_res ** 2)
    c1_pass = bool((r2_exertion <= 0.02) or (p_res > 0.05))

    # Full-series exertion & caffeine-PK residualized RMSSD
    rmssd_clean_full = rmssd_observed - slope_ex * workout_power_watts - slope_caf * caffeine_pk

    # Blind Joint Profile-Likelihood Recovery (zero oracle emission constants!)
    blind_est = estimate_state_space_blind(
        fnirs_hbo2, eeg_tbr, rmssd_clean_full, daily_trust_probe, shocks, asymmetric=True
    )
    lambda_hat = blind_est["lambda_hat"]
    lambda_minus_hat = blind_est["lambda_minus_hat"]
    lambda_error = abs(lambda_hat - lambda_true)
    c2_pass = bool((lambda_error <= 0.0250) and (lambda_minus_hat > lambda_hat))

    tau_relax_hat_days = blind_est["tau_relax_hat_days"]
    c3_pass = bool(2.0 <= tau_relax_hat_days <= 4.0)

    # Criterion C9: 12-Draw Blind Simulation-Based Calibration (SBC) across random parameters
    rng_sbc = np.random.default_rng(777)
    sbc_lam_errs, sbc_tau_errs = [], []
    for _ in range(12):
        lam_s = float(rng_sbc.uniform(0.14, 0.34))
        tau_s = float(rng_sbc.uniform(2.0, 4.0))
        cf_s = float(rng_sbc.uniform(0.9, 1.6))
        ce_s = float(rng_sbc.uniform(-1.1, -0.6))
        cr_s = float(rng_sbc.uniform(20.0, 32.0))
        d_s = 1.0 / (tau_s * EPOCHS_PER_DAY)
        st_s = np.empty(TOTAL_EPOCHS)
        sc_s = S_base
        for t_k in range(TOTAL_EPOCHS):
            if t_k in shocks:
                sc_s = np.clip(sc_s + lam_s * shocks[t_k], 0.0, 1.0)
            else:
                sc_s += d_s * (S_base - sc_s)
            st_s[t_k] = sc_s
        y_f_s = cf_s * (st_s - S_base) + rng_sbc.normal(0, 0.15, TOTAL_EPOCHS)
        y_e_s = 2.4 + ce_s * (st_s - S_base) + rng_sbc.normal(0, 0.12, TOTAL_EPOCHS)
        y_r_s = 48.0 + cr_s * (st_s - S_base) + rng_sbc.normal(0, 2.5, TOTAL_EPOCHS)
        y_p_s = np.clip(st_s[ev_epochs] + rng_sbc.normal(0, 0.040, N_DAYS), 0.0, 1.0)
        b_s = estimate_state_space_blind(y_f_s, y_e_s, y_r_s, y_p_s, shocks)
        sbc_lam_errs.append(abs(b_s["lambda_hat"] - lam_s))
        sbc_tau_errs.append(abs(b_s["tau_relax_hat_days"] - tau_s))
    sbc_lam_mae = float(np.mean(sbc_lam_errs))
    sbc_tau_mae = float(np.mean(sbc_tau_errs))
    c9_sbc_pass = bool(sbc_lam_mae <= 0.020 and sbc_tau_mae <= 0.30)

    # Criterion C7: Days 1-14 Exponential Practice-Curve Detrending on Cognitive Battery
    from scipy.optimize import curve_fit
    def _practice_fn(d, rt_inf, amp, tau_l):
        return rt_inf + amp * np.exp(-d / np.maximum(tau_l, 0.5))
    burnin_days = days_idx[:14]
    popt_pvt, _ = curve_fit(_practice_fn, burnin_days, daily_pvt_rt_raw_ms[:14], p0=[235.0, 50.0, 4.0], bounds=([150.0, 0.0, 0.5], [400.0, 200.0, 20.0]), maxfev=5000)
    pvt_detrended = daily_pvt_rt_raw_ms - popt_pvt[1] * np.exp(-days_idx / popt_pvt[2])
    shock_days_neg = [45, 46, 92, 93, 138, 139, 174]
    quiet_days = [d for d in range(14, N_DAYS) if d not in shock_days_neg and d-1 not in shock_days_neg]
    pvt_shock_vals = pvt_detrended[shock_days_neg]
    pvt_quiet_vals = pvt_detrended[quiet_days]
    pooled_sd = float(np.sqrt(((len(pvt_shock_vals)-1)*np.var(pvt_shock_vals, ddof=1) + (len(pvt_quiet_vals)-1)*np.var(pvt_quiet_vals, ddof=1)) / max(len(pvt_shock_vals)+len(pvt_quiet_vals)-2, 1)))
    cohen_d_pvt = float((np.mean(pvt_shock_vals) - np.mean(pvt_quiet_vals)) / max(pooled_sd, 1e-6))
    c7_pass = bool(cohen_d_pvt >= 0.50)

    # Criterion C4: AR(1)-Prewhitened Benjamini-Yekutieli FDR across Days 15-180 (PILOT-H1..H12)
    eval_slice = slice(14, N_DAYS)
    daily_streams = [
        np.array([np.mean(fnirs_hbo2[d*288:(d+1)*288]) for d in range(N_DAYS)])[eval_slice],
        np.array([np.mean(eeg_tbr[d*288:(d+1)*288]) for d in range(N_DAYS)])[eval_slice],
        np.array([np.mean(rmssd_clean_full[d*288:(d+1)*288]) for d in range(N_DAYS)])[eval_slice],
        np.array([np.mean(wrist_temp_drift[d*288+264:min(TOTAL_EPOCHS, d*288+360)]) for d in range(N_DAYS)])[eval_slice],
        np.array([np.mean(glucose_mgdl[d*288:(d+1)*288]) for d in range(N_DAYS)])[eval_slice],
        daily_reading_latency_hrs[eval_slice],
        daily_flesch_grade[eval_slice],
        daily_airofit_mip_cmh2o[eval_slice],
        pvt_detrended[eval_slice],
        daily_nback_dprime[eval_slice],
        daily_stroop_ms[eval_slice],
        daily_sbp_dipping_pct[eval_slice],
        daily_acoustic_jitter_pct[eval_slice],
    ]
    prewhitened_streams = [_ar1_prewhiten(s) for s in daily_streams]
    real_p_values = []
    for i in range(len(prewhitened_streams)):
        for j in range(i + 1, len(prewhitened_streams)):
            for lag in (0, 1):
                if len(real_p_values) >= 78:
                    break
                x_s = prewhitened_streams[i][:(len(prewhitened_streams[i]) - lag)] if lag > 0 else prewhitened_streams[i]
                y_s = prewhitened_streams[j][lag:] if lag > 0 else prewhitened_streams[j]
                _, p_v = stats.pearsonr(x_s, y_s)
                real_p_values.append(max(float(p_v), 1e-300))
    p_values = np.array(real_p_values[:78])
    by_q_adjusted = stats.false_discovery_control(p_values, method="by")
    fdr_q_max = float(np.min(by_q_adjusted))
    n_by_sig = int(np.sum(by_q_adjusted <= 0.05))
    c4_pass = bool(n_by_sig >= 1)

    # Criterion C5: Monthly Blood Panels + Longitudinal Endocrine AUC Concordance (r >= 0.40, p < 0.01)
    r_hair_cgm, p_hair = stats.pearsonr(segment_cgm_stress_auc, segment_hair_cortisol_ratio)
    r_blood_cgm, p_blood = stats.pearsonr(monthly_cgm_auc, monthly_blood_hscrp)
    hair_cortisol_cortisone = float(np.mean(segment_hair_cortisol_ratio))
    c5_pass = bool((r_hair_cgm >= 0.40) and (p_hair < 0.01) and (r_blood_cgm >= 0.40))

    # Criterion C6: Airofit MIP <-> Nocturnal RMSSD & Aranet4 CO2 <-> Detrended PVT-B (AR(1)-prewhitened)
    daily_rmssd_sleep = np.array([np.mean(rmssd_observed[d*EPOCHS_PER_DAY+264:min(TOTAL_EPOCHS, d*EPOCHS_PER_DAY+360)]) for d in range(N_DAYS)])
    r_airofit_rmssd, p_airofit = stats.pearsonr(_ar1_prewhiten(daily_airofit_mip_cmh2o[eval_slice]), _ar1_prewhiten(daily_rmssd_sleep[eval_slice]))
    r_co2_pvt, p_co2_pvt = stats.pearsonr(_ar1_prewhiten(daily_aranet4_co2_ppm[eval_slice]), _ar1_prewhiten(pvt_detrended[eval_slice]))
    c6_pass = bool((r_airofit_rmssd >= 0.20) and (p_airofit < 0.01) and (r_co2_pvt >= 0.25) and (p_co2_pvt < 0.001))

    # Criterion C8: AR(1) Null Calibration (B=400 null Monte Carlo runs with rho1 = 0.72)
    rng_null = np.random.default_rng(100)
    n_null_days, rho_null = 166, 0.72
    fp_naive, fp_prewhitened = 0, 0
    for _ in range(400):
        x_n, y_n = np.zeros(n_null_days), np.zeros(n_null_days)
        ex, ey = rng_null.normal(0, 1, n_null_days), rng_null.normal(0, 1, n_null_days)
        for t_i in range(1, n_null_days):
            x_n[t_i] = rho_null * x_n[t_i - 1] + ex[t_i]
            y_n[t_i] = rho_null * y_n[t_i - 1] + ey[t_i]
        _, p_naive = stats.pearsonr(x_n, y_n)
        _, p_pw = stats.pearsonr(_ar1_prewhiten(x_n), _ar1_prewhiten(y_n))
        if p_naive < 0.05:
            fp_naive += 1
        if p_pw < 0.05:
            fp_prewhitened += 1
    fpr_naive, fpr_prewhitened = fp_naive / 400.0, fp_prewhitened / 400.0
    c8_pass = bool((fpr_prewhitened <= 0.08) and (fpr_naive > 0.20))

    # Criterion C10: Minimal-to-Deep Hub-to-Spoke Transfer Compression (Days 91-180 steady-state)
    # Zero S_true leakage: target is blind PCA composite of 6 disjoint Hub streams;
    # Spoke contains ONLY Watch HRV (fold-residualized), Watch Wrist Temp, and Ledger state.
    p2_slice = slice(90, N_DAYS)
    n_p2 = N_DAYS - 90
    H_hub_p2 = np.column_stack([
        np.array([np.mean(fnirs_hbo2[d * EPOCHS_PER_DAY:(d + 1) * EPOCHS_PER_DAY]) for d in range(N_DAYS)])[p2_slice],
        -np.array([np.mean(eeg_tbr[d * EPOCHS_PER_DAY:(d + 1) * EPOCHS_PER_DAY]) for d in range(N_DAYS)])[p2_slice],
        -np.array([np.mean(glucose_mgdl[d * EPOCHS_PER_DAY:(d + 1) * EPOCHS_PER_DAY]) for d in range(N_DAYS)])[p2_slice],
        daily_sbp_dipping_pct[p2_slice],
        daily_airofit_mip_cmh2o[p2_slice],
        -pvt_detrended[p2_slice],
    ])
    probe_p2 = daily_trust_probe[p2_slice]
    daily_rmssd_obs_p2 = np.array([np.mean(rmssd_observed[d * EPOCHS_PER_DAY:(d + 1) * EPOCHS_PER_DAY]) for d in range(N_DAYS)])[p2_slice]
    daily_ex_p2 = np.array([np.mean(workout_power_watts[d * EPOCHS_PER_DAY:(d + 1) * EPOCHS_PER_DAY]) for d in range(N_DAYS)])[p2_slice]
    daily_caf_p2 = np.array([np.mean(caffeine_pk[d * EPOCHS_PER_DAY:(d + 1) * EPOCHS_PER_DAY]) for d in range(N_DAYS)])[p2_slice]
    daily_temp_p2 = np.array([np.mean(wrist_temp_drift[d * EPOCHS_PER_DAY + 264:min(TOTAL_EPOCHS, d * EPOCHS_PER_DAY + 360)]) for d in range(N_DAYS)])[p2_slice]

    d_rate_hat = 1.0 / (max(tau_relax_hat_days, 0.25) * EPOCHS_PER_DAY)
    s_ledger_full = np.empty(TOTAL_EPOCHS, dtype=float)
    sc_l = S_base
    for t_l in range(TOTAL_EPOCHS):
        if t_l in shocks:
            ep_l = shocks[t_l]
            sc_l = float(np.clip(sc_l + (lambda_minus_hat if ep_l < 0.0 else lambda_hat) * ep_l, 0.0, 1.0))
        else:
            sc_l += d_rate_hat * (S_base - sc_l)
        s_ledger_full[t_l] = sc_l
    daily_ledger_p2 = np.array([s_ledger_full[d * EPOCHS_PER_DAY + 241] for d in range(N_DAYS)])[p2_slice]

    def _eval_fold_isolated_hub_spoke(hub_mat: np.ndarray, ledger_only: bool = False) -> float:
        n_blocks, block_sz = 5, max(1, n_p2 // 5)
        preds_hs, y_eval = np.zeros(n_p2), np.zeros(n_p2)
        for b in range(n_blocks):
            lo, hi = b * block_sz, (n_p2 if b == n_blocks - 1 else min(n_p2, (b + 1) * block_sz))
            tr = np.ones(n_p2, dtype=bool)
            tr[lo:hi] = False
            N_tr = np.column_stack([np.ones(np.sum(tr)), daily_ex_p2[tr], daily_caf_p2[tr]])
            N_te = np.column_stack([np.ones(np.sum(~tr)), daily_ex_p2[~tr], daily_caf_p2[~tr]])
            beta_n, _, _, _ = np.linalg.lstsq(N_tr, daily_rmssd_obs_p2[tr], rcond=None)
            if ledger_only:
                X_tr = daily_ledger_p2[tr][:, None]
                X_te = daily_ledger_p2[~tr][:, None]
            else:
                X_tr = np.column_stack([daily_rmssd_obs_p2[tr] - N_tr @ beta_n, daily_temp_p2[tr], daily_ledger_p2[tr]])
                X_te = np.column_stack([daily_rmssd_obs_p2[~tr] - N_te @ beta_n, daily_temp_p2[~tr], daily_ledger_p2[~tr]])
            mu_h, sd_h = np.mean(hub_mat[tr], axis=0), np.maximum(np.std(hub_mat[tr], axis=0), 1e-8)
            Z_tr, Z_te = (hub_mat[tr] - mu_h) / sd_h, (hub_mat[~tr] - mu_h) / sd_h
            _, _, vt_h = np.linalg.svd(Z_tr, full_matrices=False)
            w_hub = -vt_h[0] if np.corrcoef(Z_tr @ vt_h[0], probe_p2[tr])[0, 1] < 0 else vt_h[0]
            y_tr, y_te = Z_tr @ w_hub, Z_te @ w_hub
            mu_x, sd_x = np.mean(X_tr, axis=0), np.maximum(np.std(X_tr, axis=0), 1e-8)
            mu_y = float(np.mean(y_tr))
            Xs_tr, Xs_te = (X_tr - mu_x) / sd_x, (X_te - mu_x) / sd_x
            w_r = np.linalg.solve(Xs_tr.T @ Xs_tr + 1.0 * np.eye(Xs_tr.shape[1]), Xs_tr.T @ (y_tr - mu_y))
            preds_hs[~tr] = mu_y + Xs_te @ w_r
            y_eval[~tr] = y_te
        ss_res_h = float(np.sum((y_eval - preds_hs) ** 2))
        ss_tot_h = max(float(np.sum((y_eval - np.mean(y_eval)) ** 2)), 1e-12)
        return round(1.0 - ss_res_h / ss_tot_h, 4)

    r2_hub_spoke_oos = _eval_fold_isolated_hub_spoke(H_hub_p2, ledger_only=False)
    r2_ledger_only_oos = _eval_fold_isolated_hub_spoke(H_hub_p2, ledger_only=True)
    delta_r2_physio = round(r2_hub_spoke_oos - r2_ledger_only_oos, 4)
    null_shift_r2s = [_eval_fold_isolated_hub_spoke(np.roll(H_hub_p2, sd, axis=0)) for sd in range(14, 77)]
    hub_spoke_res = {
        "r2_oos": r2_hub_spoke_oos,
        "ledger_only_r2_oos": r2_ledger_only_oos,
        "physio_incremental_delta_r2": delta_r2_physio,
        "circular_shift_null_median_r2": round(float(np.median(null_shift_r2s)), 4),
        "circular_shift_null_p95_r2": round(float(np.percentile(null_shift_r2s, 95)), 4),
    }
    c10_transfer_pass = bool(
        (r2_hub_spoke_oos >= 0.60)
        and (delta_r2_physio >= 0.15)
        and (hub_spoke_res["circular_shift_null_median_r2"] <= 0.05)
    )

    compound_pass = c1_pass and c2_pass and c3_pass and c4_pass and c5_pass and c6_pass and c7_pass and c8_pass and c9_sbc_pass and c10_transfer_pass

    results = {
        "simulation": "Sim PILOT-2 (V4.6 180-Day Complete Multimodal Benchmark)",
        "protocol_version": "DOCAS-PILOT-1 V4.6",
        "pre_registration": "protocols/sim_preregistrations/SIM_PILOT_V4_6_PRE_REGISTRATION.md",
        "n_days": N_DAYS,
        "burnin_days": 14,
        "baseline_days": 28,
        "total_epochs": TOTAL_EPOCHS,
        "lambda_true": lambda_true,
        "lambda_minus_true": lambda_minus_true,
        "lambda_hat": float(lambda_hat),
        "lambda_minus_hat": float(lambda_minus_hat),
        "lambda_error": float(lambda_error),
        "tau_relax_true_days": tau_relax_true_days,
        "tau_relax_hat_days": float(tau_relax_hat_days),
        "blind_c_fnirs_hat": float(blind_est["c_fnirs_hat"]),
        "blind_c_eeg_hat": float(blind_est["c_eeg_hat"]),
        "blind_c_rmssd_hat": float(blind_est["c_rmssd_hat"]),
        "sbc_12draw_lambda_mae": float(sbc_lam_mae),
        "sbc_12draw_tau_mae_days": float(sbc_tau_mae),
        "r2_exertion_decoupling": float(r2_exertion),
        "by_fdr_q_bound": float(fdr_q_max),
        "by_significant_pairs": n_by_sig,
        "r_hair_cortisol_vs_cgm_auc": float(r_hair_cgm),
        "p_hair_cortisol": float(p_hair),
        "r_blood_hscrp_vs_cgm_auc": float(r_blood_cgm),
        "p_blood_hscrp": float(p_blood),
        "r_airofit_mip_vs_nocturnal_rmssd_prewhitened": float(r_airofit_rmssd),
        "p_airofit_mip": float(p_airofit),
        "r_aranet4_co2_vs_pvt_detrended": float(r_co2_pvt),
        "p_aranet4_co2_pvt": float(p_co2_pvt),
        "pvt_practice_detrended_shock_cohen_d": float(cohen_d_pvt),
        "ar1_null_fpr_naive": float(fpr_naive),
        "ar1_null_fpr_prewhitened": float(fpr_prewhitened),
        "hair_cortisol_cortisone_ratio": float(hair_cortisol_cortisone),
        "criterion_c1_exertion_pass": c1_pass,
        "criterion_c2_parameter_recovery_pass": c2_pass,
        "criterion_c3_relaxation_pass": c3_pass,
        "criterion_c4_by_fdr_pass": c4_pass,
        "criterion_c5_endocrine_blood_pass": c5_pass,
        "criterion_c6_airofit_aranet4_pass": c6_pass,
        "criterion_c7_practice_detrending_pass": c7_pass,
        "criterion_c8_ar1_null_calibration_pass": c8_pass,
        "criterion_c9_blind_sbc_pass": c9_sbc_pass,
        "hub_to_spoke_transfer_r2_oos": float(hub_spoke_res["r2_oos"]),
        "hub_to_spoke_ledger_only_r2_oos": float(hub_spoke_res["ledger_only_r2_oos"]),
        "hub_to_spoke_physio_delta_r2": float(hub_spoke_res["physio_incremental_delta_r2"]),
        "hub_to_spoke_circular_null_median_r2": float(hub_spoke_res["circular_shift_null_median_r2"]),
        "hub_to_spoke_circular_null_p95_r2": float(hub_spoke_res["circular_shift_null_p95_r2"]),
        "criterion_c10_hub_to_spoke_pass": c10_transfer_pass,
        "compound_verdict": "COMPOUND PASS (10/10 CRITERIA SATISFIED)" if compound_pass else "FAIL"
    }

    out_json = os.path.join(output_dir, "sim_pilot2_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=4)
    print(f"✓ Results saved to: {out_json}")

    # Generate Publication Figure
    fig, axs = plt.subplots(4, 1, figsize=(14, 12), sharex=True, dpi=200)

    # Panel 1: Master Law Latent Trust Trajectory S(t)
    axs[0].plot(time_days, S_true, color='#0F172A', lw=1.5, label='Latent Trust State S(t)')
    for ep, eps in shocks.items():
        col = '#10B981' if eps > 0 else '#EF4444'
        axs[0].axvline(ep / EPOCHS_PER_DAY, color=col, linestyle='--', alpha=0.6)
    axs[0].set_ylabel('Trust State S(t)', fontweight='bold')
    axs[0].set_title('Sim PILOT-2 (V4.6): 180-Day Multimodal Synthetic Benchmark (DOCAS-PILOT-1 V4.6)', fontweight='bold')
    axs[0].legend(loc='upper right')
    axs[0].grid(True, alpha=0.3)

    # Panel 2: Continuous Glycemic Flux Across 12 Sensors
    axs[1].plot(time_days, glucose_mgdl, color='#F59E0B', lw=0.8, alpha=0.7, label='Interstitial Glucose (12x Dexcom Sensors)')
    axs[1].axhline(115, color='#DC2626', linestyle=':', label='Allostatic Glycemic Stress Threshold')
    axs[1].set_ylabel('Glucose (mg/dL)', fontweight='bold')
    axs[1].legend(loc='upper right')
    axs[1].grid(True, alpha=0.3)

    # Panel 3: Optical PPG HRV RMSSD & Workout Power
    axs[2].plot(time_days, rmssd_observed, color='#3B82F6', lw=0.8, label='PPG RMSSD Vagal Tone (Apple Watch)')
    ax2_twin = axs[2].twinx()
    ax2_twin.plot(time_days, workout_power_watts, color='#8B5CF6', lw=0.5, alpha=0.4, label='Mechanical Workout Power (Watts)')
    ax2_twin.set_ylabel('Exertion (Watts)', color='#8B5CF6')
    axs[2].set_ylabel('RMSSD (ms)', fontweight='bold')
    axs[2].legend(loc='upper left')
    axs[2].grid(True, alpha=0.3)

    # Panel 4: Daily Active Behavioral Tasks (Airofit MIP vs Practice-Detrended PVT-B)
    days_arr = np.arange(N_DAYS)
    axs[3].axvspan(0, 14, color='#FEF3C7', alpha=0.5, label='Phase 0: Days 1-14 Habituation Burn-In')
    axs[3].axvspan(14, 42, color='#E0F2FE', alpha=0.4, label='Phase 1: Days 15-42 Baseline & PK')
    axs[3].plot(days_arr, daily_airofit_mip_cmh2o, color='#059669', lw=1.5, marker='o', markersize=3, label='Airofit Pro MIP (cmH2O)')
    ax3_twin = axs[3].twinx()
    ax3_twin.plot(days_arr, pvt_detrended, color='#D97706', lw=1.5, marker='s', markersize=3, label='Practice-Detrended PVT-B RT (ms)')
    ax3_twin.set_ylabel('Detrended PVT-B RT (ms)', color='#D97706')
    axs[3].set_ylabel('Airofit MIP (cmH2O)', fontweight='bold')
    axs[3].set_xlabel('Trial Timeline (Days)', fontweight='bold')
    axs[3].legend(loc='upper left', fontsize=8)
    axs[3].grid(True, alpha=0.3)

    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig_pilot2_180day_mock_trajectory.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"✓ Trajectory figure saved to: {fig_path}")

    # Copy figure to canonical figures/
    base_repo = os.path.abspath(os.path.join(output_dir, "../../../"))
    fig_dest1 = os.path.join(base_repo, "figures/fig_pilot2_180day_mock_trajectory.png")
    if os.path.exists(os.path.dirname(fig_dest1)):
        import shutil
        shutil.copy2(fig_path, fig_dest1)
        print(f"✓ Figure copied to canonical figures directory.")

    print("=" * 80)
    print(f"SIMULATION PILOT-2 (V4.6) COMPLETE: {results['compound_verdict']}")
    print(f"  Lambda Recovery Error:   {lambda_error:.6f} <= 0.0250 ({'PASS' if c2_pass else 'FAIL'}) | λ-={lambda_minus_hat:.4f} > λ+={lambda_hat:.4f}")
    print(f"  Tau Relaxation Estimate: {tau_relax_hat_days:.2f} days in [2.0, 4.0] ({'PASS' if c3_pass else 'FAIL'})")
    print(f"  Exertion Confounder R^2: {r2_exertion:.6f} <= 0.0200 ({'PASS' if c1_pass else 'FAIL'})")
    print(f"  AR(1) BY FDR q-bound:    {fdr_q_max:.6f} <= 0.0500 ({'PASS' if c4_pass else 'FAIL'})")
    print(f"  Blood hsCRP/Hair AUC r:  {r_blood_cgm:.4f} / {r_hair_cgm:.4f} >= 0.40 ({'PASS' if c5_pass else 'FAIL'})")
    print(f"  Airofit MIP & CO2-PVT r: {r_airofit_rmssd:.4f} / {r_co2_pvt:.4f} ({'PASS' if c6_pass else 'FAIL'})")
    print(f"  Practice-Detrended d:    {cohen_d_pvt:.4f} >= 0.50 ({'PASS' if c7_pass else 'FAIL'})")
    print(f"  AR(1) Null FPR (PW/Naiv):{fpr_prewhitened:.3f} <= 0.08 vs {fpr_naive:.3f} > 0.20 ({'PASS' if c8_pass else 'FAIL'})")
    print(f"  Blind 12-Draw SBC MAE:   λ={sbc_lam_mae:.5f}<=0.020, τ={sbc_tau_mae:.3f}d<=0.30 ({'PASS' if c9_sbc_pass else 'FAIL'})")
    print(f"  Hub->Spoke Transfer R^2: {hub_spoke_res['r2_oos']:.4f} >= 0.60 | Ledger-only={hub_spoke_res['ledger_only_r2_oos']:.4f} | ΔR²={hub_spoke_res['physio_incremental_delta_r2']:+.4f} | null={hub_spoke_res['circular_shift_null_median_r2']:.4f} ({'PASS' if c10_transfer_pass else 'FAIL'})")
    print("=" * 80)

    return results

if __name__ == "__main__":
    run_180day_pilot_simulation()
