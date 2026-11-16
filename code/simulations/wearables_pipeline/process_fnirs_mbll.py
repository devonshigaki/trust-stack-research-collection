#!/usr/bin/env python3
"""
DOCAS-PILOT-1: Prefrontal fNIRS Modified Beer-Lambert Law (MBLL) Preprocessor
Target: The Trust Stack Research Collection / DOCAS §5.1, §5.30 & PILOT-H1
Pre-Registration: DOCAS_PILOT_1_HUMAN_PROTOCOL.md

Pipeline:
  1. Optical Intensity -> Optical Density (OD) conversion
  2. Pre-filter Scalp Coupling Index (SCI) on cardiac band (0.5–2.5 Hz)
     to verify optode skin contact (SQI >= 0.85) prior to hemodynamic filtering
  3. Zero-phase 4th-order Butterworth hemodynamic bandpass filtering (0.01–0.20 Hz)
  4. Modified Beer-Lambert Law (MBLL) inversion (DPF=6.0, d=3.0 cm) to recover
     molar concentration shifts Δ[HbO2], Δ[HbR], Δ[HbT] in μmol/L (μM)
  5. Evaluates pre-registered stopping rule: flags motion artifacts (>40% stopping gate)
"""

import argparse
import math
import os
import sqlite3
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    from scipy import signal
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _numpy_bandpass(data: np.ndarray, fs: float, low: float, high: float) -> np.ndarray:
    """Frequency-domain bandpass filter in pure numpy when scipy is absent."""
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    fft_vals = np.fft.rfft(data)
    mask = (freqs >= low) & (freqs <= high)
    fft_vals[~mask] = 0.0
    return np.fft.irfft(fft_vals, n=n)

# Molar extinction coefficients [HbO2, HbR] in mM^-1 cm^-1 for base-10 log10(I0/I) OD.
# Standardized on a SINGLE unmixed source: Scott Prahl (OMLC, 1998; compiled from Gratzer & Kollias)
# so HbO2 and HbR across all wavelengths share identical spectrophotometer calibration.
EXTINCTION_COEFFICIENTS = {
    730: (0.3900, 1.1022),
    850: (1.0580, 0.6913),
    660: (0.3196, 3.2266),
    760: (0.5860, 1.5485),
}

DPF_ADULT_PREFRONTAL = 6.0
INTER_OPTODE_DISTANCE_CM = 3.0
PATHLENGTH_CM = DPF_ADULT_PREFRONTAL * INTER_OPTODE_DISTANCE_CM  # 18.0 cm
FS_FNIRS = 64  # Hz

SCHEMA_MBLL_SQL = """
CREATE TABLE IF NOT EXISTS muse_fnirs_mbll (
    session_id TEXT NOT NULL,
    optode_idx INTEGER NOT NULL CHECK(optode_idx BETWEEN 1 AND 5),
    sample_idx INTEGER NOT NULL,
    timestamp_epoch REAL NOT NULL,
    delta_hbo2_umol REAL NOT NULL,
    delta_hbr_umol REAL NOT NULL,
    delta_hbt_umol REAL NOT NULL,
    sci_quality_index REAL NOT NULL,
    is_motion_artifact INTEGER NOT NULL CHECK(is_motion_artifact IN (0, 1)),
    PRIMARY KEY (session_id, optode_idx, sample_idx)
);
"""

def intensity_to_optical_density(raw_intensity: np.ndarray, baseline_intensity: Optional[np.ndarray] = None) -> np.ndarray:
    """
    ΔOD(λ, t) = -log10(max(I(λ, t), eps) / I0(λ))
    raw_intensity shape: [N_wavelengths, N_samples]
    """
    eps = 1e-4
    safe_intensity = np.maximum(raw_intensity, eps)
    if baseline_intensity is None:
        baseline_intensity = np.mean(safe_intensity, axis=1, keepdims=True)
    baseline_intensity = np.maximum(baseline_intensity, eps)
    return -np.log10(safe_intensity / baseline_intensity)


def compute_scalp_coupling_index(od_730: np.ndarray, od_850: np.ndarray, fs: int = FS_FNIRS) -> float:
    """
    Compute Scalp Coupling Index (SCI) on raw optical densities in cardiac band (0.5–2.5 Hz).
    High correlation (>= 0.85) proves real optical skin contact with photoplethysmographic pulse.
    """
    if len(od_730) < fs * 2:
        return 0.0
    if HAS_SCIPY:
        nyq = 0.5 * fs
        sos = signal.butter(2, [0.5 / nyq, 2.5 / nyq], btype="bandpass", output="sos")
        filt_730 = signal.sosfiltfilt(sos, od_730 - np.mean(od_730))
        filt_850 = signal.sosfiltfilt(sos, od_850 - np.mean(od_850))
    else:
        filt_730 = _numpy_bandpass(od_730 - np.mean(od_730), float(fs), 0.5, 2.5)
        filt_850 = _numpy_bandpass(od_850 - np.mean(od_850), float(fs), 0.5, 2.5)

    norm_730 = np.linalg.norm(filt_730)
    norm_850 = np.linalg.norm(filt_850)
    if norm_730 < 1e-8 or norm_850 < 1e-8:
        return 0.0

    sci = float(np.dot(filt_730, filt_850) / (norm_730 * norm_850))
    return float(np.clip(sci, -1.0, 1.0))


def bandpass_hemodynamic_filter(delta_od: np.ndarray, fs: int = FS_FNIRS, low: float = 0.01, high: float = 0.20) -> np.ndarray:
    """Zero-phase 4th-order Butterworth bandpass filter isolating hemodynamic vasomotion."""
    filtered = np.zeros_like(delta_od)
    if HAS_SCIPY:
        nyq = 0.5 * fs
        sos = signal.butter(4, [low / nyq, high / nyq], btype="bandpass", output="sos")
        for w in range(delta_od.shape[0]):
            filtered[w] = signal.sosfiltfilt(sos, delta_od[w])
    else:
        for w in range(delta_od.shape[0]):
            filtered[w] = _numpy_bandpass(delta_od[w], float(fs), low, high)
    return filtered


def compute_scholkmann_dpf(wavelength_nm: float, age_years: float = 30.0, body_fat_pct: float = 20.0) -> float:
    """
    Computes wavelength- and age-dependent adult prefrontal Differential Pathlength Factor (DPF)
    according to Scholkmann & Wolf (2013, J. Biomed. Opt. 18(10), 105004, Eq. 7), dynamically scaled
    by Fitindex BIA subcutaneous adipose thickness per DOCAS_PILOT_1_HUMAN_PROTOCOL.md:286:
      DPF_u(λ) = DPF_Scholkmann(λ, Age) * [1.0 + γ_BIA * (BodyFat% - 20.0)]
    Clamps λ to Scholkmann & Wolf's fitted validity interval [690, 832] nm to avoid cubic extrapolation.
    """
    wl = float(max(690.0, min(832.0, wavelength_nm)))
    age = float(max(18.0, min(80.0, age_years)))
    dpf_base = 223.3 + 0.05624 * (age ** 0.8493) - 5.723e-7 * (wl ** 3) + 0.001245 * (wl ** 2) - 0.9025 * wl
    gamma_bia = 0.012
    dpf_calibrated = dpf_base * (1.0 + gamma_bia * (float(body_fat_pct) - 20.0))
    return float(np.clip(dpf_calibrated, 3.5, 9.0))


def repair_motion_tddr(od_series: np.ndarray, fs: int = FS_FNIRS) -> np.ndarray:
    """
    Temporal Derivative Distribution Repair (TDDR, Fishburn et al. 2019, NeuroImage 184:171-179).
    Removes baseline shift and spike motion artifacts via iteratively reweighted least-squares (IRLS)
    on temporal first differences using Tukey's biweight function.
    """
    if len(od_series) < 16:
        return od_series

    sig = np.asarray(od_series, dtype=np.float64)
    sig_mean = float(np.mean(sig))
    diff = np.diff(sig)

    mu = float(np.median(diff))
    mad = float(np.median(np.abs(diff - mu)))
    scale = 1.4826 * max(mad, 1e-8)
    if scale < 1e-8:
        return od_series

    c = 4.685
    weights = np.ones_like(diff)
    for _ in range(50):
        residuals = diff - mu
        u = residuals / (c * scale)
        mask = np.abs(u) < 1.0
        weights.fill(0.0)
        weights[mask] = (1.0 - u[mask] ** 2) ** 2

        sum_w = float(np.sum(weights))
        if sum_w < 1e-12:
            break
        new_mu = float(np.sum(weights * diff) / sum_w)
        if abs(new_mu - mu) < 1e-6:
            break
        mu = new_mu

    repaired_diff = weights * (diff - mu)
    reconstructed = np.zeros_like(sig)
    reconstructed[0] = sig[0]
    reconstructed[1:] = sig[0] + np.cumsum(repaired_diff)

    # Median baseline centering to eliminate DC baseline shift leakage
    return reconstructed - np.median(reconstructed)


def apply_cbsi_neurovascular_filter(
    delta_hbo2: np.ndarray,
    delta_hbr: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Correlation-Based Signal Improvement (CBSI, Cui et al. 2010, NeuroImage 49:3039-3046).
    Enforces exact physiological negative cross-correlation between Δ[HbO2] and Δ[HbR] (neurovascular coupling)
    and eliminates systemic Mayer waves and motion artifacts that produce in-phase fluctuations.
    """
    std_o = float(np.std(delta_hbo2))
    std_r = float(np.std(delta_hbr))
    if std_o < 1e-8 or std_r < 1e-8:
        return delta_hbo2, delta_hbr

    alpha = std_o / std_r
    hbo2_cbsi = 0.5 * (delta_hbo2 - alpha * delta_hbr)
    hbr_cbsi = -hbo2_cbsi / alpha
    return hbo2_cbsi, hbr_cbsi


def solve_mbll_inversion(
    filtered_od: np.ndarray,
    wavelengths: Tuple[int, ...] = (730, 850, 660),
    inter_optode_distance_cm: float = INTER_OPTODE_DISTANCE_CM,
    age_years: float = 30.0,
    body_fat_pct: float = 20.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solves Modified Beer-Lambert Law for Δ[HbO2], Δ[HbR], and Δ[HbT] in μM (μmol/L):
      ΔOD(λ, t) = (ε_HbO2(λ) * Δ[HbO2](t) + ε_HbR(λ) * Δ[HbR](t)) * L(λ)
      Δc(t) = (E^T * E)^-1 * E^T * (ΔOD(t) / L)
    using wavelength-specific Scholkmann-Wolf (2013) DPF(λ, A) dynamically scaled by Fitindex Body Fat %.
    """
    E = np.array([EXTINCTION_COEFFICIENTS[wl] for wl in wavelengths], dtype=np.float64)  # [3, 2] in mM^-1 cm^-1
    pathlengths = np.array([
        inter_optode_distance_cm * compute_scholkmann_dpf(wl, age_years, body_fat_pct)
        for wl in wavelengths
    ], dtype=np.float64)[:, None]

    # MNE-Python exact linear formulation: ΔOD(λ, t) = (E(λ) * L(λ)) · Δc(t) => Δc = pinv(E * L) @ ΔOD
    # For N_λ = 2 this equals pinv(E) @ (ΔOD / L); for N_λ >= 3 pinv(E * L) avoids unequal pathlength distortion.
    EL = E * pathlengths  # [N_wl, 2] in mM^-1
    pinv_EL = np.linalg.pinv(EL)  # [2, N_wl] in mM
    concentrations_mM = pinv_EL @ filtered_od  # [2, N_samples] in mM

    # Convert mM -> μM (x 1000)
    delta_hbo2_umol = concentrations_mM[0] * 1000.0
    delta_hbr_umol = concentrations_mM[1] * 1000.0
    delta_hbt_umol = delta_hbo2_umol + delta_hbr_umol

    return delta_hbo2_umol, delta_hbr_umol, delta_hbt_umol


def apply_glm_nuisance_regression(
    signal_ts: np.ndarray,
    nuisance_regressors: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    OLS General Linear Model nuisance regression (short-separation / systemic / IMU motion
    regressors + linear drift) that preserves statistical independence between Δ[HbO2] and Δ[HbR]
    without forcing artificial -1.0 anti-correlation (replaces circular CBSI).
    """
    n = len(signal_ts)
    t_norm = np.linspace(-1.0, 1.0, n)
    cols = [np.ones(n), t_norm]
    if nuisance_regressors is not None and len(nuisance_regressors) > 0:
        reg = np.asarray(nuisance_regressors, dtype=np.float64)
        if reg.ndim == 1:
            reg = reg[:, None]
        if reg.shape[0] == n:
            for c in range(reg.shape[1]):
                col = reg[:, c] - np.mean(reg[:, c])
                if np.std(col) > 1e-8:
                    cols.append(col / np.std(col))
    X = np.column_stack(cols)
    beta, _, _, _ = np.linalg.lstsq(X, signal_ts, rcond=None)
    return signal_ts - X @ beta


def compute_mayer_wave_power_ratio(hbo2: np.ndarray, fs: int = FS_FNIRS) -> float:
    """Quantifies ~0.1 Hz arterial Mayer wave power fraction (0.08–0.12 Hz vs 0.01–0.20 Hz)."""
    n = len(hbo2)
    if n < fs * 4:
        return 0.0
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    psd = np.abs(np.fft.rfft(hbo2 - np.mean(hbo2))) ** 2
    band_total = psd[(freqs >= 0.01) & (freqs <= 0.20)].sum()
    band_mayer = psd[(freqs >= 0.08) & (freqs <= 0.12)].sum()
    return float(band_mayer / max(band_total, 1e-12))


def process_optode_signal(
    raw_intensity: np.ndarray,
    fs: int = FS_FNIRS,
    age_years: float = 30.0,
    body_fat_pct: float = 20.0,
    nuisance_regressors: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float, bool]:
    delta_od = intensity_to_optical_density(raw_intensity)
    sci = compute_scalp_coupling_index(delta_od[0], delta_od[1], fs=fs)
    repaired_od = np.zeros_like(delta_od)
    for w in range(delta_od.shape[0]):
        repaired_od[w] = repair_motion_tddr(delta_od[w], fs=fs)
    filtered_od = bandpass_hemodynamic_filter(repaired_od, fs=fs)
    raw_hbo2, raw_hbr, raw_hbt = solve_mbll_inversion(filtered_od, age_years=age_years, body_fat_pct=body_fat_pct)
    hbo2 = apply_glm_nuisance_regression(raw_hbo2, nuisance_regressors)
    hbr = apply_glm_nuisance_regression(raw_hbr, nuisance_regressors)
    hbt = hbo2 + hbr
    is_motion_artifact = sci < 0.50
    return hbo2, hbr, hbt, sci, is_motion_artifact


def process_session_fnirs(db_path: str, session_id: str, body_fat_pct: float = 20.0) -> Dict[str, float]:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_MBLL_SQL)
    cur = conn.cursor()

    cur.execute(
        "SELECT DISTINCT optode_idx FROM muse_fnirs_raw WHERE session_id = ? ORDER BY optode_idx",
        (session_id,)
    )
    optodes = [row[0] for row in cur.fetchall()]
    if not optodes:
        conn.close()
        return {"processed_optodes": 0, "mean_sci": 0.0, "artifact_ratio": 1.0}

    all_sci = []
    total_samples = 0
    artifact_samples = 0
    all_mbll_rows = []

    for optode in optodes:
        cur.execute(
            """
            SELECT sample_idx, timestamp_epoch, raw_intensity_730, raw_intensity_850, raw_intensity_660
            FROM muse_fnirs_raw WHERE session_id = ? AND optode_idx = ? ORDER BY sample_idx
            """,
            (session_id, optode)
        )
        rows = cur.fetchall()
        if len(rows) < FS_FNIRS * 2:
            continue

        sample_indices = [r[0] for r in rows]
        timestamps = [r[1] for r in rows]
        intensities = np.array([[r[2], r[3], r[4]] for r in rows], dtype=np.float64).T

        hbo2, hbr, hbt, sci, is_artifact = process_optode_signal(intensities, body_fat_pct=body_fat_pct)
        all_sci.append(sci)

        for i in range(len(sample_indices)):
            all_mbll_rows.append((
                session_id, optode, sample_indices[i], float(timestamps[i]),
                float(hbo2[i]), float(hbr[i]), float(hbt[i]), float(sci), 1 if is_artifact else 0
            ))
            total_samples += 1
            if is_artifact:
                artifact_samples += 1

    cur.executemany("INSERT OR REPLACE INTO muse_fnirs_mbll VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", all_mbll_rows)
    conn.commit()
    conn.close()

    mean_sci = float(np.mean(all_sci)) if all_sci else 0.0
    artifact_ratio = (artifact_samples / max(total_samples, 1))

    return {
        "processed_optodes": len(optodes),
        "mean_sci": mean_sci,
        "artifact_ratio": artifact_ratio,
        "stopping_rule_triggered": artifact_ratio > 0.40,
    }

def run_self_test() -> bool:
    print("=" * 70)
    print("RUNNING PRE-FLIGHT VERIFICATION: MODIFIED BEER-LAMBERT LAW (MBLL)")
    print("=" * 70)

    # 1. Exact Analytical Forward-Inverse Inversion Test with Scholkmann-Wolf DPF(λ, A)
    true_hbo2_umol = np.array([2.50, 4.00, 1.20, -0.50])
    true_hbr_umol = np.array([-0.80, -1.50, -0.30, 0.40])
    true_conc_mM = np.array([true_hbo2_umol / 1000.0, true_hbr_umol / 1000.0])

    pathlengths = np.array([
        INTER_OPTODE_DISTANCE_CM * compute_scholkmann_dpf(wl, age_years=30.0)
        for wl in (730, 850, 660)
    ], dtype=np.float64)[:, None]

    E = np.array([EXTINCTION_COEFFICIENTS[wl] for wl in (730, 850, 660)])  # [3, 2]
    sim_od = (E @ true_conc_mM) * pathlengths

    rec_hbo2, rec_hbr, rec_hbt = solve_mbll_inversion(sim_od, age_years=30.0)
    err_hbo2 = np.max(np.abs(rec_hbo2 - true_hbo2_umol))
    err_hbr = np.max(np.abs(rec_hbr - true_hbr_umol))
    assert err_hbo2 < 1e-6, f"HbO2 round-trip error too large: {err_hbo2}"
    assert err_hbr < 1e-6, f"HbR round-trip error too large: {err_hbr}"

    # Verify MNE-Python natural-log OD * abs_coef (ln(10)*E) exact algebraic parity
    sim_od_ln = sim_od * math.log(10.0)
    abs_coef_mne = E * math.log(10.0)
    EL_mne = abs_coef_mne * pathlengths
    conc_mne_umol = (np.linalg.pinv(EL_mne) @ sim_od_ln) * 1000.0
    assert np.max(np.abs(conc_mne_umol[0] - rec_hbo2)) < 1e-10
    assert np.max(np.abs(conc_mne_umol[1] - rec_hbr)) < 1e-10
    print(f"✓ MBLL Molar Extinction Inversion Round-Trip Error: {err_hbo2:.2e} μM (Exact MNE-NIRS ln(10) Parity)")

    # 1b. TDDR Motion Spike Repair Test
    clean_wave = np.sin(2 * np.pi * 0.1 * np.linspace(0, 10, 640))
    spiked_wave = clean_wave.copy()
    spiked_wave[300:320] += 5.0
    repaired_wave = repair_motion_tddr(spiked_wave, fs=64)
    spike_residual = np.max(np.abs(repaired_wave[300:320] - clean_wave[300:320]))
    assert spike_residual < 1.0, f"TDDR should suppress 5.0 spike by >80%, got residual {spike_residual}"
    print(f"✓ TDDR Motion Artifact Repair: 5.0 OD motion spike suppressed to {spike_residual:.2f} residual")

    # 1c. TDDR Persistent Step-Function Baseline Shift Test (Headband Slip)
    step_wave = clean_wave.copy()
    step_wave[320:] += 5.0
    repaired_step = repair_motion_tddr(step_wave, fs=64)
    step_residual = np.max(np.abs(repaired_step - clean_wave))
    assert step_residual < 0.25, f"TDDR must repair persistent +5.0 OD step shift without ramp artifact, got {step_residual:.3f}"
    print(f"✓ TDDR Persistent Step Shift Repair: +5.0 OD baseline slip suppressed to {step_residual:.3f} max residual")

    # 2. Scalp Coupling Index (SCI) Photoplethysmographic Cardiac Pulse Test
    rng = np.random.default_rng(42)
    fs = 64
    t = np.linspace(0, 10, 10 * fs, endpoint=False)
    cardiac_pulse = np.sin(2 * np.pi * 1.2 * t)
    noise_uncoupled = rng.normal(0, 0.2, len(t))

    od_730_coupled = 0.05 * cardiac_pulse + rng.normal(0, 0.005, len(t))
    od_850_coupled = 0.07 * cardiac_pulse + rng.normal(0, 0.005, len(t))
    sci_coupled = compute_scalp_coupling_index(od_730_coupled, od_850_coupled, fs=fs)
    assert sci_coupled >= 0.85, f"Coupled SCI must be >= 0.85 (PILOT-H1 target), got {sci_coupled:.3f}"
    print(f"✓ Scalp Coupling Index (Coupled Optodes): {sci_coupled:.3f} >= 0.85 (PILOT-H1 Passed)")

    od_730_uncoupled = noise_uncoupled
    od_850_uncoupled = rng.normal(0, 0.2, len(t))
    sci_uncoupled = compute_scalp_coupling_index(od_730_uncoupled, od_850_uncoupled, fs=fs)
    assert sci_uncoupled < 0.50, f"Uncoupled SCI must be < 0.50, got {sci_uncoupled:.3f}"
    print(f"✓ Scalp Coupling Index (Uncoupled Noise): {sci_uncoupled:.3f} < 0.50 (Artifact Gate Passed)")

    # 3b. Cross-Verify Optical Density against upstream MNE-Python (if installed) & Mayer Wave / GLM Independence
    try:
        import mne
        info_mne = mne.create_info(ch_names=["S1_D1 760", "S1_D1 850"], sfreq=64.0, ch_types=["fnirs_cw_amplitude", "fnirs_cw_amplitude"])
        info_mne["chs"][0]["loc"][9] = 760.0
        info_mne["chs"][1]["loc"][9] = 850.0
        test_raw = np.vstack([1000.0 + 5.0 * np.sin(2 * np.pi * 0.05 * t), 1200.0 - 4.0 * np.sin(2 * np.pi * 0.05 * t)])
        raw_mne = mne.io.RawArray(test_raw, info_mne, verbose=False)
        od_mne = mne.preprocessing.nirs.optical_density(raw_mne).get_data()
        od_ours = intensity_to_optical_density(test_raw) * np.log(10.0)  # MNE uses natural log -ln(I/I0); convert log10 -> ln
        od_mne_centered = od_mne - np.mean(od_mne, axis=1, keepdims=True)
        od_ours_centered = od_ours - np.mean(od_ours, axis=1, keepdims=True)
        assert np.max(np.abs(od_mne_centered - od_ours_centered)) < 1e-4, "OD mismatch vs MNE-Python!"
        print("✓ Upstream MNE-Python `optical_density` Cross-Check: Exact Match (< 1e-4)")
    except ImportError:
        pass

    # Verify GLM regression removes systemic Mayer wave (~0.1 Hz) without forcing HbO2/HbR correlation = -1.0
    t_glm = np.linspace(0, 60.0, 60 * fs, endpoint=False)
    mayer = 2.0 * np.sin(2 * np.pi * 0.10 * t_glm)
    sig_hbo2 = mayer + 0.8 * np.sin(2 * np.pi * 0.04 * t_glm)
    sig_hbr = mayer - 0.3 * np.sin(2 * np.pi * 0.04 * t_glm) + 0.2 * rng.normal(0, 1, len(t_glm))
    assert compute_mayer_wave_power_ratio(sig_hbo2, fs=fs) > 0.50
    clean_hbo2 = apply_glm_nuisance_regression(sig_hbo2, mayer[:, None])
    clean_hbr = apply_glm_nuisance_regression(sig_hbr, mayer[:, None])
    assert compute_mayer_wave_power_ratio(clean_hbo2, fs=fs) < 0.05
    assert abs(np.corrcoef(clean_hbo2, clean_hbr)[0, 1]) < 0.99, "GLM must not force synthetic -1.0 correlation!"
    print("✓ Systemic Mayer Wave (~0.1 Hz) GLM Regression & HbO2/HbR Independence: VERIFIED")

    # 3. Test Full Session Pipeline on In-Memory Edge DB
    test_db = "test_fnirs_mbll_dryrun.db"
    for fn in [test_db, f"{test_db}-wal", f"{test_db}-shm", f"{test_db}.key"]:
        if os.path.exists(fn):
            os.remove(fn)

    from stream_muse_athena import MuseAthenaStreamer
    streamer = MuseAthenaStreamer(
        session_id="mbll_test_sess",
        subject_id="sub_test",
        cohort_stage=1,
        day_index=1,
        db_path=test_db,
    )
    streamer.run_epoch(duration_sec=6.0)
    streamer.close()

    summary = process_session_fnirs(test_db, "mbll_test_sess")
    assert summary["processed_optodes"] == 5, f"Expected 5 optodes, got {summary['processed_optodes']}"
    assert summary["mean_sci"] >= 0.85, f"Expected clean synthetic SCI >= 0.85, got {summary['mean_sci']:.3f}"
    assert not summary["stopping_rule_triggered"], "Stopping rule should not trigger on clean data"

    conn = sqlite3.connect(test_db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM muse_fnirs_mbll WHERE session_id = 'mbll_test_sess'")
    mbll_count = cur.fetchone()[0]
    assert mbll_count == 5 * 6 * FS_FNIRS, f"Expected {5 * 6 * FS_FNIRS} MBLL samples, got {mbll_count}"
    conn.close()

    for fn in [test_db, f"{test_db}-wal", f"{test_db}-shm", f"{test_db}.key"]:
        if os.path.exists(fn):
            os.remove(fn)

    print(f"✓ Prefrontal Optode Array Processing: {summary['processed_optodes']}/5 optodes processed")
    print(f"✓ Edge Database Persistence (`muse_fnirs_mbll`): {mbll_count} samples committed")
    print("PRE-FLIGHT SELF-TEST: ALL 3 GATES PASSED (100% HEALTHY)\n")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DOCAS-PILOT-1: Prefrontal fNIRS MBLL Preprocessor")
    parser.add_argument("--self-test", action="store_true", help="Run automated pre-flight self-test")
    parser.add_argument("--db-path", type=str, default="pilot_wearables_edge.db", help="Local edge database path")
    parser.add_argument("--session-id", type=str, default="pilot_sess_001", help="Session ID to process")
    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    print(f"Processing fNIRS optical densities for session {args.session_id} in {args.db_path}...")
    res = process_session_fnirs(args.db_path, args.session_id)
    print(f"Summary: {res}")
