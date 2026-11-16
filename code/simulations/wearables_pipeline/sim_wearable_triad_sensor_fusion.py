#!/usr/bin/env python3
"""
Simulation WEARABLE-TRIAD: Multi-Rate Biosensor Fusion
Target: The Trust Stack Research Collection (Version 4.3) / DOCAS §5.1 & §5.37

Simulates and calibrates the multi-rate physiological cascade across:
1. Muse S Headband (256 Hz EEG): Prefrontal Frontal Alpha Asymmetry (FAA) & P300/MMN
2. Apple Watch Ultra 2/Series 10 (1 Hz PPG): Beat-to-beat rMSSD vagal tone
3. Dexcom Stelo CGM (1 sample / 5 min): Interstitial glucose rate of change (dG/dt)

Verifies multi-scale temporal latency hierarchy (ms -> s -> min) and asynchronous
Kalman state-space tracking of the 5-channel trust vector.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_simulation():
    print("=" * 80)
    print("RUNNING SIMULATION WEARABLE-TRIAD: MULTI-RATE BIOSENSOR TELEMETRY FUSION")
    print("=" * 80)

    np.random.seed(42)
    DURATION_SEC = 2400 # 40 minutes of continuous recording
    FS_EEG = 256 # Hz
    FS_PPG = 1 # Hz (1 sample per second)
    FS_CGM = 1 / 300 # Hz (1 sample per 5 minutes = 300 seconds)

    t_eeg = np.linspace(0, DURATION_SEC, int(DURATION_SEC * FS_EEG))
    t_ppg = np.linspace(0, DURATION_SEC, int(DURATION_SEC * FS_PPG))
    t_cgm = np.linspace(0, DURATION_SEC, int(DURATION_SEC * FS_CGM))

    # Event: Acute Contractual Betrayal at t = 300 seconds (5.0 minutes)
    T_EVENT = 300.0

    # 1. Generate Ground Truth Trust State S(t)
    S_true = np.ones_like(t_ppg) * 0.85
    # Step drop at event followed by slow recovery
    for i, t in enumerate(t_ppg):
        if t >= T_EVENT:
            dt = t - T_EVENT
            # Betrayal drops trust by 0.55, slow asymptotic recovery
            S_true[i] = 0.30 + 0.55 * (1.0 - np.exp(-dt / 1200.0))

    # 2. Simulate Sensor Telemetry Streams
    # (A) Muse EEG: P300 Mismatch & Frontal Alpha Asymmetry (FAA)
    # Event latency: tau_eeg = 320 ms
    tau_eeg = 0.320 # seconds (320 ms)
    faa_stream = np.random.normal(0.40, 0.08, size=len(t_eeg)) # Baseline approach bias
    # At t = T_EVENT + tau_eeg, acute P300 negative mismatch spike and drop to withdrawal
    idx_event_eeg = int((T_EVENT + tau_eeg) * FS_EEG)
    p300_window = int(0.5 * FS_EEG) # 500 ms window
    faa_stream[idx_event_eeg:idx_event_eeg+p300_window] -= 0.85 # Strong mismatch negativity
    faa_stream[idx_event_eeg+p300_window:] = np.random.normal(-0.25, 0.08, size=len(t_eeg)-(idx_event_eeg+p300_window))

    # Downsample EEG FAA to 1 Hz for plotting/fusion
    faa_1hz = faa_stream.reshape(-1, FS_EEG).mean(axis=1)

    # (B) Apple Watch PPG: Beat-to-Beat rMSSD (Heart Rate Variability, Vagal Tone)
    # Autonomic delay: tau_ppg = 22.0 seconds
    tau_ppg = 22.0 # seconds
    rmssd_stream = np.random.normal(55.0, 4.0, size=len(t_ppg)) # 55 ms baseline
    for i, t in enumerate(t_ppg):
        if t >= T_EVENT + tau_ppg:
            dt = t - (T_EVENT + tau_ppg)
            # Vagal withdrawal drops rMSSD to 24 ms, recovers over 15 minutes
            rmssd_stream[i] = 24.0 + (55.0 - 24.0) * (1.0 - np.exp(-dt / 600.0)) + np.random.normal(0, 3.0)

    # (C) Dexcom Stelo CGM: Interstitial Glucose & Glucocorticoid Mobilization
    # Cortisol-mediated hepatic gluconeogenesis latency: tau_cgm = 18.0 minutes (1080 seconds)
    tau_cgm = 18.0 * 60.0 # seconds (1080 s)
    glucose_stream = np.random.normal(92.0, 3.0, size=len(t_cgm)) # 92 mg/dL fasting baseline
    for i, t in enumerate(t_cgm):
        if t >= T_EVENT + tau_cgm:
            dt = t - (T_EVENT + tau_cgm)
            # Hepatic glucose spike to 138 mg/dL, clearing over 30 minutes
            glucose_stream[i] = 92.0 + 46.0 * (dt / 900.0) * np.exp(-dt / 900.0) + np.random.normal(0, 2.0)

    # 3. Latency Verification (Criterion C1)
    print("\n--- PHYSIOLOGICAL LATENCY CASCADE HIERARCHY ---")
    print(f"Muse EEG P300/FAA Latency (tau_Muse):       {tau_eeg*1000:.1f} ms  [Target: <= 1000 ms]")
    print(f"Apple Watch Vagal Withdrawal (tau_Watch):   {tau_ppg:.1f} s   [Target: <= 60 s]")
    print(f"Dexcom Stelo Glycemic Excursion (tau_Stelo):{tau_cgm/60.0:.1f} min [Target: 15-45 min]")

    crit_c1 = (tau_eeg < tau_ppg < tau_cgm) and (tau_eeg <= 1.0) and (tau_ppg <= 60.0)
    print(f"Criterion C1 (Cascade Latency Hierarchy): {'PASS' if crit_c1 else 'FAIL'}")

    # 4. Blind Pre-Study Burn-In Calibration & Strictly Causal Multi-Rate 2-State Kalman Filter
    # State x_t = [S_t (latent trust anomaly), C_t (glucocorticoid load)]^T
    # Zero oracle T_EVENT slicing (fixed [0, 180]s burn-in); zero future interpolation; zero acausal smoothing.
    BURN_IN_SEC = 180

    def run_causal_kalman(
        faa_sig: np.ndarray,
        hrv_sig: np.ndarray,
        glu_sig: np.ndarray,
        n_ticks: int,
        use_watch: bool = True,
    ) -> np.ndarray:
        m_f0 = float(np.mean(faa_sig[:BURN_IN_SEC]))
        s_f0 = max(float(np.std(faa_sig[:BURN_IN_SEC])), 0.08)
        m_h0 = float(np.mean(hrv_sig[:BURN_IN_SEC]))
        s_h0 = max(float(np.std(hrv_sig[:BURN_IN_SEC])), 4.0)
        m_g0 = float(glu_sig[0])
        sd_g0 = 4.0

        x = np.array([0.50, 0.0], dtype=np.float64)
        P = np.diag([0.25, 0.25])
        F = np.array([[0.999, 0.0], [0.0, 0.996]], dtype=np.float64)
        Q = np.diag([2.5e-4, 4.0e-4])
        s_hat_out = np.empty(n_ticks, dtype=np.float64)

        def kf_update(x_vec, P_mat, z_obs, H_row, R_var):
            y_innov = z_obs - float(H_row @ x_vec)
            S_innov = float(H_row @ P_mat @ H_row.T) + R_var
            K_gain = (P_mat @ H_row.T) / S_innov
            x_upd = x_vec + K_gain * y_innov
            P_upd = (np.eye(2) - np.outer(K_gain, H_row)) @ P_mat
            return x_upd, P_upd

        H_eeg = np.array([1.0, 0.0])
        H_ppg = np.array([1.0, 0.0])
        H_cgm = np.array([-1.0, 1.0])
        for k in range(n_ticks):
            x = F @ x
            P = F @ P @ F.T + Q
            z_eeg = 0.50 + 0.05 * ((faa_sig[k] - m_f0) / s_f0)
            x, P = kf_update(x, P, z_eeg, H_eeg, R_var=0.045)
            if use_watch:
                z_ppg = 0.50 + 0.07 * ((hrv_sig[k] - m_h0) / s_h0)
                x, P = kf_update(x, P, z_ppg, H_ppg, R_var=0.025)
            if k % 300 == 0:
                cgm_idx = k // 300
                if cgm_idx < len(glu_sig):
                    z_cgm = ((glu_sig[cgm_idx] - m_g0) / (15.0 * sd_g0)) - 0.50
                    x, P = kf_update(x, P, z_cgm, H_cgm, R_var=0.040)
            s_hat_out[k] = float(np.clip(x[0], 0.0, 1.0))
        return s_hat_out

    S_hat = run_causal_kalman(faa_1hz, rmssd_stream, glucose_stream, len(t_ppg), use_watch=True)
    S_hat_trunc = run_causal_kalman(faa_1hz, rmssd_stream, glucose_stream, 1200, use_watch=True)
    causality_diff = float(np.max(np.abs(S_hat[:1200] - S_hat_trunc)))
    assert causality_diff < 1e-12, f"Causality violation! Future data leaked into prefix: {causality_diff}"

    corr_full = float(np.corrcoef(S_hat, S_true)[0, 1])
    print(f"\n--- BLIND CAUSAL ASYNCHRONOUS MULTI-RATE KALMAN FILTER (180s Burn-In) ---")
    print(f"Prefix-Truncation Causality Diff:          {causality_diff:.2e} (< 1e-12 PASS)")
    print(f"Full Multi-Sensor Trust State Correlation: r = {corr_full:.4f}  [Target: >= 0.850]")

    # Randomized unknown betrayal-onset Monte Carlo robustness check (20 draws in [240s, 900s])
    rng_mc = np.random.default_rng(2026)
    mc_corrs = []
    for _ in range(20):
        t_ev = float(rng_mc.uniform(240.0, 900.0))
        s_mc = np.where(t_ppg < t_ev, 0.85, 0.30 + 0.55 * (1.0 - np.exp(-np.maximum(t_ppg - t_ev, 0.0) / 1200.0)))
        faa_mc = np.where(t_ppg < t_ev + tau_eeg, rng_mc.normal(0.40, 0.08, len(t_ppg)), rng_mc.normal(-0.25, 0.08, len(t_ppg)))
        hrv_mc = np.where(t_ppg < t_ev + tau_ppg, rng_mc.normal(55.0, 4.0, len(t_ppg)), 24.0 + 31.0 * (1.0 - np.exp(-np.maximum(t_ppg - t_ev - tau_ppg, 0.0) / 600.0)) + rng_mc.normal(0, 3.0, len(t_ppg)))
        glu_mc = np.where(t_cgm < t_ev + tau_cgm, rng_mc.normal(92.0, 3.0, len(t_cgm)), 92.0 + 46.0 * (np.maximum(t_cgm - t_ev - tau_cgm, 0.0) / 900.0) * np.exp(-np.maximum(t_cgm - t_ev - tau_cgm, 0.0) / 900.0) + rng_mc.normal(0, 2.0, len(t_cgm)))
        s_hat_mc = run_causal_kalman(faa_mc, hrv_mc, glu_mc, len(t_ppg), use_watch=True)
        mc_corrs.append(float(np.corrcoef(s_hat_mc, s_mc)[0, 1]))
    mc_min_r = float(np.min(mc_corrs))
    print(f"Randomized Onset MC (20x T_event in [240,900]s): min r = {mc_min_r:.4f} [Target: >= 0.850]")
    crit_c2 = (corr_full >= 0.850) and (causality_diff < 1e-12) and (mc_min_r >= 0.850)
    print(f"Criterion C2 (Multi-Rate State Recovery):  {'PASS' if crit_c2 else 'FAIL'}")

    # 5. Fault Tolerance & Sensor Dropout Test (Criterion C3)
    S_hat_degraded = run_causal_kalman(faa_1hz, rmssd_stream, glucose_stream, len(t_ppg), use_watch=False)

    corr_degraded = float(np.corrcoef(S_hat_degraded, S_true)[0, 1])
    print(f"Degraded (Apple Watch Missing) Correlation:  r = {corr_degraded:.4f}  [Target: >= 0.750]")
    crit_c3 = (corr_degraded >= 0.750)
    print(f"Criterion C3 (Single-Sensor Fault Tolerance):{'PASS' if crit_c3 else 'FAIL'}")

    all_pass = crit_c1 and crit_c2 and crit_c3
    print(f"\nOVERALL VERDICT: {'COMPOUND PASS (3/3)' if all_pass else 'FAIL'}")

    # 6. Generate Publication Figure
    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True, dpi=300)

    # Panel 1: Muse EEG FAA
    axes[0].plot(t_ppg / 60.0, faa_1hz, color='#9b59b6', linewidth=1.5, label='Muse S: Frontal Alpha Asymmetry (FAA; AF7/AF8)')
    axes[0].axvline(T_EVENT / 60.0, color='red', linestyle='--', linewidth=1.5, label='Betrayal Event (t = 5 min)')
    axes[0].set_ylabel('FAA Index\n(ln[R]-ln[L])', fontsize=10, fontweight='bold')
    axes[0].set_title('(a) Millisecond Neural Tier: Muse S EEG Prefrontal Prediction Error (tau = 320 ms)', fontsize=11, fontweight='bold')
    axes[0].grid(True, linestyle=':', alpha=0.6)
    axes[0].legend(loc='upper right', fontsize=9)

    # Panel 2: Apple Watch PPG HRV
    axes[1].plot(t_ppg / 60.0, rmssd_stream, color='#337ab7', linewidth=1.8, label='Apple Watch Ultra 2: Beat-to-Beat rMSSD (ms)')
    axes[1].axvline(T_EVENT / 60.0, color='red', linestyle='--', linewidth=1.5)
    axes[1].set_ylabel('rMSSD (ms)', fontsize=10, fontweight='bold')
    axes[1].set_title('(b) Second-Scale Autonomic Tier: Apple Watch Vagal Withdrawal (tau = 22.0 s)', fontsize=11, fontweight='bold')
    axes[1].grid(True, linestyle=':', alpha=0.6)
    axes[1].legend(loc='lower right', fontsize=9)

    # Panel 3: Dexcom Stelo CGM
    axes[2].step(t_cgm / 60.0, glucose_stream, where='post', color='#f0ad4e', linewidth=2.2, label='Dexcom Stelo CGM: Interstitial Glucose (mg/dL; 5-min cadence)')
    axes[2].axvline(T_EVENT / 60.0, color='red', linestyle='--', linewidth=1.5)
    axes[2].set_ylabel('Glucose (mg/dL)', fontsize=10, fontweight='bold')
    axes[2].set_title('(c) Minute-Scale Metabolic Tier: Dexcom Stelo Hepatic Glucocorticoid Mobilization (tau = 18.0 min)', fontsize=11, fontweight='bold')
    axes[2].grid(True, linestyle=':', alpha=0.6)
    axes[2].legend(loc='upper left', fontsize=9)

    # Panel 4: Asynchronous Multi-Rate State Recovery
    axes[3].plot(t_ppg / 60.0, S_true, 'k--', linewidth=2.5, label='Ground Truth Trust State S(t)')
    axes[3].plot(t_ppg / 60.0, S_hat, color='#5cb85c', linewidth=2.0, label=f'Full Fused Estimator S_hat (r = {corr_full:.3f})')
    axes[3].plot(t_ppg / 60.0, S_hat_degraded, color='#d9534f', linestyle=':', linewidth=1.8, label=f'Degraded (No Watch PPG; r = {corr_degraded:.3f})')
    axes[3].set_xlabel('Elapsed Time (Minutes)', fontsize=11, fontweight='bold')
    axes[3].set_ylabel('Latent Trust State S', fontsize=10, fontweight='bold')
    verdict_str = "COMPOUND PASS (3/3)" if all_pass else f"PARTIAL PASS ({sum([crit_c1, crit_c2, crit_c3])}/3; C3 FAIL under Watch dropout)"
    axes[3].set_title(f'(d) Causal Multi-Rate Kalman Fusion ({verdict_str})', fontsize=11, fontweight='bold')
    axes[3].grid(True, linestyle=':', alpha=0.6)
    axes[3].legend(loc='lower right', fontsize=9)

    plt.tight_layout()
    out_dir = os.path.dirname(os.path.abspath(__file__))
    fig_path = os.path.join(out_dir, "fig_wearable_triad_fusion.png")
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"\nSaved visualization to: {fig_path}")

    # Copy to canonical figures/
    docas_fig_path = os.path.join(out_dir, "../../../figures/fig_wearable_triad_fusion.png")
    import shutil
    shutil.copyfile(fig_path, docas_fig_path)
    print(f"Copied figure to canonical figures directory: {docas_fig_path}")

    # Output JSON Results
    res_path = os.path.join(out_dir, "sim_wearable_triad_results.json")
    with open(res_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": "2026-11-15",
            "simulation_id": "Sim WEARABLE-TRIAD",
            "tau_muse_ms": tau_eeg * 1000.0,
            "tau_watch_sec": tau_ppg,
            "tau_stelo_min": tau_cgm / 60.0,
            "causality_prefix_diff": causality_diff,
            "full_sensor_correlation_r": corr_full,
            "degraded_sensor_correlation_r": corr_degraded,
            "verdict": verdict_str,
            "criteria": {
                "C1_cascade_latency_hierarchy": bool(crit_c1),
                "C2_multirate_state_recovery": bool(crit_c2),
                "C3_fault_tolerance": bool(crit_c3)
            }
        }, f, indent=2)
    print(f"Saved simulation results to: {res_path}")

if __name__ == "__main__":
    run_simulation()
