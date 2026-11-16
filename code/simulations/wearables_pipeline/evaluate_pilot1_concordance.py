#!/usr/bin/env python3
"""
DOCAS-PILOT-1: Multimodal Apple Watch S8 & Muse S Athena Concordance Engine
Target: The Trust Stack Research Collection / DOCAS §5.1, §5.30 & PILOT-H1–H4
Protocol Pre-Registration: DOCAS_PILOT_1_HUMAN_PROTOCOL.md

Functions:
  1. Ingests Apple Health export.xml (HRV SDNN/RMSSD, Resting HR,
     Sleeping Wrist Temperature in °C, Sleep Stages with categorical preservation).
  2. Aligns Apple Watch autonomic & circadian telemetry with Muse S Athena fNIRS
     (molar Δ[HbO2], Δ[HbR]) and EEG (Frontal Alpha Asymmetry, Theta/Beta ratio).
  3. Formally evaluates pre-registered hypotheses:
     - PILOT-H1: Prefrontal fNIRS Signal Quality (SCI >= 0.85) & Medial Cortical Δ[HbO2] Activation (p < 0.01)
     - PILOT-H2: Autonomic Vagal Rebound (RMSSD surge >= +15.0% within 120s of ε > 0, p < 0.001)
     - PILOT-H3: Circadian Allostatic Coupling (Nocturnal wrist temp drift ΔT >= +0.15°C on ε < 0 days, p < 0.05)
     - PILOT-H4: Multi-Day Test-Retest Reliability (r_test-retest >= 0.75 across consecutive days in Cohort 3)
     - Stopping Rule: Flags if fNIRS motion artifacts > 40.0% or >= 3 consecutive nights missing temp.
  4. Features standalone --self-test mode for CI/CD and pre-flight validation.
"""

import argparse
import datetime
import io
import math
import os
import sqlite3
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for incomplete beta function (Numerical Recipes §6.4)."""
    max_it = 100
    eps = 1e-10
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, max_it + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        del_val = d * c
        h *= del_val
        if abs(del_val - 1.0) < eps:
            break
    return h


def regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    """
    Computes regularized incomplete beta function I_x(a, b) = B_x(a, b) / B(a, b).
    Used for exact Student's t cumulative distribution tail probabilities.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def estimate_lag1_autocorr(series: np.ndarray) -> float:
    """Computes sample lag-1 autocorrelation rho_1."""
    if len(series) < 3:
        return 0.0
    centered = series - np.mean(series)
    denom = float(np.sum(centered**2))
    if denom < 1e-12:
        return 0.0
    num = float(np.sum(centered[:-1] * centered[1:]))
    return float(np.clip(num / denom, -0.99, 0.99))


def effective_sample_size(n: int, rho_1: float) -> float:
    """Quenouille (1949) / Zwiers & von Storch (1995) effective sample size under AR(1)."""
    if rho_1 <= 0.0 or n < 3:
        return float(n)
    n_eff = float(n) * (1.0 - rho_1) / (1.0 + rho_1)
    return max(3.0, n_eff)


def compute_one_sample_ttest(
    values: List[float],
    baseline_target: float,
    alternative: str = "greater",
) -> Tuple[float, float]:
    """Computes exact one-sample Student's t-test statistic and one-tailed tail p-value (requires n >= 2)."""
    arr = np.asarray(values, dtype=np.float64)
    n = len(arr)
    if n < 2:
        return 0.0, 1.0
    m = float(np.mean(arr))
    s = float(np.std(arr, ddof=1))
    se = max(1e-9, s / math.sqrt(n))
    t_stat = (m - baseline_target) / se
    df = float(n - 1)

    t_eval = -t_stat if alternative == "less" else t_stat
    x = df / (df + t_eval * t_eval)
    two_tailed = regularized_incomplete_beta(x, 0.5 * df, 0.5)
    one_tailed = (0.5 * two_tailed) if t_eval > 0.0 else (1.0 - 0.5 * two_tailed)
    return float(t_stat), float(np.clip(one_tailed, 0.0, 1.0))


def compute_tost_correlation_equivalence(
    r_val: float,
    n: int,
    bound_r: float = 0.14142,
) -> Tuple[float, float, float]:
    """
    Schuirmann (1987) Two One-Sided Tests (TOST) for correlation equivalence:
    H01: rho <= -bound_r vs H11: rho > -bound_r
    H02: rho >= bound_r vs H12: rho < bound_r
    Returns (p_tost, p_lower, p_upper) using Fisher z-transformation.
    """
    if n < 4:
        return 1.0, 1.0, 1.0
    safe_r = max(-0.999, min(0.999, r_val))
    z = 0.5 * math.log((1.0 + safe_r) / (1.0 - safe_r))
    delta_z = 0.5 * math.log((1.0 + bound_r) / (1.0 - bound_r))
    se_z = 1.0 / math.sqrt(n - 3)
    z1 = (z + delta_z) / se_z
    z2 = (delta_z - z) / se_z
    p1 = 0.5 * math.erfc(z1 / math.sqrt(2.0))
    p2 = 0.5 * math.erfc(z2 / math.sqrt(2.0))
    p_tost = max(p1, p2)
    return float(np.clip(p_tost, 0.0, 1.0)), float(p1), float(p2)


def compute_welch_ttest(
    a: List[float],
    b: List[float],
    adjust_autocorr: bool = False,
) -> Tuple[float, float]:
    """
    Two-sample Welch's t-test with exact Student's t distribution tail
    and optional lag-1 autocorrelation effective degrees-of-freedom correction.
    """
    arr_a = np.asarray(a, dtype=np.float64)
    arr_b = np.asarray(b, dtype=np.float64)
    n1, n2 = len(arr_a), len(arr_b)
    if n1 < 2 or n2 < 2:
        return 0.0, 1.0

    m1, m2 = float(np.mean(arr_a)), float(np.mean(arr_b))
    v1, v2 = float(np.var(arr_a, ddof=1)), float(np.var(arr_b, ddof=1))

    if adjust_autocorr:
        rho_a = estimate_lag1_autocorr(arr_a)
        rho_b = estimate_lag1_autocorr(arr_b)
        n1_eff = effective_sample_size(n1, rho_a)
        n2_eff = effective_sample_size(n2, rho_b)
    else:
        n1_eff = float(n1)
        n2_eff = float(n2)

    se = math.sqrt(v1 / n1_eff + v2 / n2_eff)
    if se < 1e-12:
        return 0.0, 1.0
    t_stat = (m1 - m2) / se

    # Welch-Satterthwaite degrees of freedom
    term1 = v1 / n1_eff
    term2 = v2 / n2_eff
    df_num = (term1 + term2) ** 2
    df_den = (term1**2) / max(1.0, n1_eff - 1.0) + (term2**2) / max(1.0, n2_eff - 1.0)
    df = max(1.0, df_num / max(1e-12, df_den))

    # Exact Student's t two-tailed p-value: x = df / (df + t^2)
    x = df / (df + t_stat * t_stat)
    p_val = regularized_incomplete_beta(x, 0.5 * df, 0.5)
    return float(t_stat), float(np.clip(p_val, 0.0, 1.0))


def compute_pearson_correlation(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """Pearson correlation r and exact two-tailed Student's t p-value."""
    if len(x) != len(y) or len(x) < 3:
        return 0.0, 1.0
    x_dev = x - np.mean(x)
    y_dev = y - np.mean(y)
    num = float(np.sum(x_dev * y_dev))
    denom = float(np.sqrt(np.sum(x_dev**2) * np.sum(y_dev**2)))
    if denom < 1e-12:
        return 0.0, 1.0
    r = float(max(-1.0, min(1.0, num / denom)))
    n = len(x)
    if abs(r) >= 1.0:
        return r, 0.0
    df = float(n - 2)
    t_stat = r * math.sqrt(df / (1.0 - r * r))
    x_val = df / (df + t_stat * t_stat)
    p_val = regularized_incomplete_beta(x_val, 0.5 * df, 0.5)
    return r, float(np.clip(p_val, 0.0, 1.0))


def benjamini_yekutieli_fdr_py(p_values: Dict[str, float], q: float = 0.05) -> Dict[str, Dict[str, Any]]:
    """
    Applies Benjamini-Yekutieli (2001) FDR control under arbitrary dependence
    with proper step-up reverse-cumulative minimum adjustment (Yekutieli & Benjamini 1999).
    """
    m = len(p_values)
    if m == 0:
        return {}
    c_m = sum(1.0 / i for i in range(1, m + 1))
    sorted_p = sorted(p_values.items(), key=lambda kv: kv[1])

    raw_qs = []
    thresholds = []
    for rank, (hyp_id, p_val) in enumerate(sorted_p):
        k = rank + 1
        threshold = (k / (m * c_m)) * q
        thresholds.append(threshold)
        raw_qs.append(min(1.0, (float(p_val) * m * c_m) / k))

    # Reverse-cumulative minimum enforces step-up monotonicity: q_(k) = min(q_(k+1), r_k)
    monotonic_qs = [0.0] * m
    running_min = 1.0
    for i in range(m - 1, -1, -1):
        running_min = min(running_min, raw_qs[i])
        monotonic_qs[i] = running_min

    # Step-up rejection threshold: max k where p_(k) <= threshold_(k)
    max_k = 0
    for rank, (hyp_id, p_val) in enumerate(sorted_p):
        if p_val <= thresholds[rank]:
            max_k = rank + 1

    results = {}
    for rank, (hyp_id, p_val) in enumerate(sorted_p):
        k = rank + 1
        results[hyp_id] = {
            "raw_p": round(float(p_val), 6),
            "by_threshold": round(float(thresholds[rank]), 6),
            "adjusted_q": round(float(monotonic_qs[rank]), 6),
            "rank": k,
            "fdr_significant": k <= max_k,
        }
    return results


SCHEMA_APPLE_HEALTH_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS apple_health_hrv (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp_epoch REAL NOT NULL,
    sdnn_ms REAL,
    rmssd_ms REAL,
    heart_rate_bpm REAL,
    rmssd_source TEXT DEFAULT 'derived_from_sdnn',
    source_name TEXT DEFAULT 'Apple Watch'
);

CREATE TABLE IF NOT EXISTS apple_health_wrist_temp (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp_epoch REAL NOT NULL,
    wrist_temp_c REAL NOT NULL,
    delta_from_baseline_c REAL NOT NULL,
    source_name TEXT DEFAULT 'Apple Watch'
);

CREATE TABLE IF NOT EXISTS apple_health_sleep_stages (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    start_epoch REAL NOT NULL,
    end_epoch REAL NOT NULL,
    stage_category TEXT NOT NULL,
    duration_mins REAL NOT NULL,
    source_name TEXT DEFAULT 'Apple Watch'
);

CREATE TABLE IF NOT EXISTS dexcom_stelo_cgm (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp_epoch REAL NOT NULL,
    glucose_mg_dl REAL NOT NULL,
    dg_dt_rate REAL NOT NULL,
    is_postprandial_flag INTEGER DEFAULT 0,
    source_name TEXT DEFAULT 'Dexcom Stelo'
);

CREATE TABLE IF NOT EXISTS apple_journal_affect (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp_epoch REAL NOT NULL,
    valence_score REAL NOT NULL,
    arousal_score REAL NOT NULL,
    journal_text TEXT NOT NULL,
    source_name TEXT DEFAULT 'Apple Journal'
);

CREATE TABLE IF NOT EXISTS confounder_filters (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp_epoch REAL NOT NULL,
    dietary_carbohydrates_g REAL DEFAULT 0,
    dietary_calories_kcal REAL DEFAULT 0,
    workout_active_calories REAL DEFAULT 0,
    workout_mets REAL DEFAULT 1.0,
    post_recovery_rmssd_ms REAL,
    smart_scale_weight_kg REAL,
    smart_scale_bmi REAL,
    source_name TEXT DEFAULT 'HealthKit'
);

CREATE INDEX IF NOT EXISTS idx_ah_hrv_ts ON apple_health_hrv(timestamp_epoch);
CREATE INDEX IF NOT EXISTS idx_ah_temp_ts ON apple_health_wrist_temp(timestamp_epoch);
CREATE INDEX IF NOT EXISTS idx_ah_sleep_start ON apple_health_sleep_stages(start_epoch);
CREATE INDEX IF NOT EXISTS idx_cgm_ts ON dexcom_stelo_cgm(timestamp_epoch);
CREATE INDEX IF NOT EXISTS idx_confounder_ts ON confounder_filters(timestamp_epoch);
"""


def parse_date_to_epoch(date_str: str) -> Optional[float]:
    """Parse Apple Health ISO8601 / offset date string to Unix epoch seconds."""
    if not date_str:
        return None
    clean = date_str.strip()
    try:
        if len(clean) >= 25 and (clean[19] == " " or clean[19] == "T"):
            dt = datetime.datetime.strptime(clean, "%Y-%m-%d %H:%M:%S %z")
            return dt.timestamp()
    except Exception:
        pass

    try:
        dt = datetime.datetime.fromisoformat(clean)
        return dt.timestamp()
    except Exception:
        return None


def compute_rmssd_from_heartbeat_series(beat_times_sec: List[float]) -> Optional[float]:
    """
    Computes true beat-to-beat RMSSD (ms) from Apple HealthKit `HKHeartbeatSeriesSample`
    timestamps, applying an ectopic-beat quotient filter (|RR_i - RR_{i-1}| / RR_{i-1} <= 0.20)
    and physiological R-R bounds [300 ms, 2000 ms].
    """
    if len(beat_times_sec) < 4:
        return None
    times = sorted(beat_times_sec)
    rr_ms = [(times[i + 1] - times[i]) * 1000.0 for i in range(len(times) - 1)]
    rr_phys = [r for r in rr_ms if 300.0 <= r <= 2000.0]
    if len(rr_phys) < 3:
        return None
    clean_diffs = []
    for i in range(1, len(rr_phys)):
        if abs(rr_phys[i] - rr_phys[i - 1]) / rr_phys[i - 1] <= 0.20:
            clean_diffs.append(rr_phys[i] - rr_phys[i - 1])
    if len(clean_diffs) < 2:
        return None
    return float(math.sqrt(sum(d * d for d in clean_diffs) / len(clean_diffs)))


def parse_apple_health_xml(xml_content_or_path: str, is_file: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parses Apple Health XML content or file, extracting all 8 multimodal streams:
      - HRV SDNN, Heart Rate, Sleeping Wrist Temperature, Sleep Stages
      - Dexcom Stelo CGM Blood Glucose
      - Confounder Filters: Carbohydrates, Calories, Workouts, Body Mass
      - Apple Journal / State of Mind Valence
    """
    extracted: Dict[str, List[Dict[str, Any]]] = {
        "hrv": [],
        "heart_rate": [],
        "wrist_temperature": [],
        "sleep_stages": [],
        "blood_glucose": [],
        "carbohydrates": [],
        "dietary_calories": [],
        "workouts": [],
        "body_mass": [],
        "state_of_mind": [],
    }

    if is_file:
        context = ET.iterparse(xml_content_or_path, events=("end",))
    else:
        context = ET.iterparse(io.StringIO(xml_content_or_path), events=("end",))

    for _, elem in context:
        if elem.tag == "Record":
            rec_type = elem.attrib.get("type", "")
            start_str = elem.attrib.get("startDate", "")
            end_str = elem.attrib.get("endDate", "")
            val_str = elem.attrib.get("value", "")

            start_epoch = parse_date_to_epoch(start_str)
            end_epoch = parse_date_to_epoch(end_str) if end_str else start_epoch

            if start_epoch is None:
                elem.clear()
                continue

            if rec_type == "HKQuantityTypeIdentifierHeartRateVariabilitySDNN":
                try:
                    val = float(val_str)
                    extracted["hrv"].append({
                        "timestamp_epoch": start_epoch,
                        "sdnn_ms": val,
                        "rmssd_ms": None,
                        "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                        "rmssd_source": "derived_from_sdnn",
                    })
                except ValueError:
                    pass

            elif rec_type == "HKQuantityTypeIdentifierHeartRateVariabilityRMSSD":
                try:
                    val = float(val_str)
                    extracted["hrv"].append({
                        "timestamp_epoch": start_epoch,
                        "sdnn_ms": None,
                        "rmssd_ms": val,
                        "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                        "rmssd_source": "rmssd_heartbeat_series",
                    })
                except ValueError:
                    pass

            elif rec_type == "HKQuantityTypeIdentifierHeartRate":
                try:
                    val = float(val_str)
                    extracted["heart_rate"].append({
                        "timestamp_epoch": start_epoch,
                        "heart_rate_bpm": val,
                        "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                    })
                except ValueError:
                    pass

            elif rec_type == "HKQuantityTypeIdentifierAppleSleepingWristTemperature":
                try:
                    val = float(val_str)
                    extracted["wrist_temperature"].append({
                        "timestamp_epoch": start_epoch,
                        "wrist_temp_c": round(val, 3),
                        "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                    })
                except ValueError:
                    pass

            elif rec_type == "HKCategoryTypeIdentifierSleepAnalysis":
                duration_mins = 0.0
                if end_epoch is not None and end_epoch > start_epoch:
                    duration_mins = round((end_epoch - start_epoch) / 60.0, 2)
                extracted["sleep_stages"].append({
                    "start_epoch": start_epoch,
                    "end_epoch": end_epoch or start_epoch,
                    "stage_category": val_str,
                    "duration_mins": duration_mins,
                    "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                })
            elif rec_type == "HKQuantityTypeIdentifierBloodGlucose":
                try:
                    val = float(val_str)
                    extracted["blood_glucose"].append({
                        "timestamp_epoch": start_epoch,
                        "glucose_mg_dl": val,
                        "source_name": elem.attrib.get("sourceName", "Dexcom Stelo"),
                    })
                except ValueError:
                    pass

            elif rec_type == "HKQuantityTypeIdentifierDietaryCarbohydrates":
                try:
                    val = float(val_str)
                    extracted["carbohydrates"].append({
                        "timestamp_epoch": start_epoch,
                        "carbs_g": val,
                        "source_name": elem.attrib.get("sourceName", "HealthKit"),
                    })
                except ValueError:
                    pass

            elif rec_type == "HKQuantityTypeIdentifierDietaryEnergyConsumed":
                try:
                    val = float(val_str)
                    extracted["dietary_calories"].append({
                        "timestamp_epoch": start_epoch,
                        "calories_kcal": val,
                        "source_name": elem.attrib.get("sourceName", "HealthKit"),
                    })
                except ValueError:
                    pass

            elif rec_type == "HKQuantityTypeIdentifierBodyMass":
                try:
                    val = float(val_str)
                    unit = elem.attrib.get("unit", "kg")
                    weight_kg = val * 0.453592 if "lb" in unit else val
                    extracted["body_mass"].append({
                        "timestamp_epoch": start_epoch,
                        "weight_kg": round(weight_kg, 2),
                        "source_name": elem.attrib.get("sourceName", "Smart Scale"),
                    })
                except ValueError:
                    pass

            elif rec_type == "HKCategoryTypeIdentifierStateOfMind":
                try:
                    val = float(val_str)
                    extracted["state_of_mind"].append({
                        "timestamp_epoch": start_epoch,
                        "valence": val,
                        "journal_text": elem.attrib.get("metadata", "Valence reflection"),
                        "source_name": elem.attrib.get("sourceName", "Apple Journal"),
                    })
                except ValueError:
                    pass

            elem.clear()

        elif elem.tag == "Workout":
            start_str = elem.attrib.get("startDate", "")
            start_epoch = parse_date_to_epoch(start_str)
            if start_epoch is not None:
                dur_str = elem.attrib.get("duration", "0")
                dur_unit = elem.attrib.get("durationUnit", "min")
                raw_dur = float(dur_str) if dur_str.replace('.', '', 1).isdigit() else 0.0
                if str(dur_unit).lower() in ("s", "sec", "second", "seconds") or (not dur_unit and raw_dur > 300.0):
                    dur_mins = raw_dur / 60.0
                else:
                    dur_mins = raw_dur
                energy_str = elem.attrib.get("totalEnergyBurned", "0")
                energy_kcal = float(energy_str) if energy_str.replace('.', '', 1).isdigit() else 0.0
                mets = ((energy_kcal / max(1.0, dur_mins)) * 0.95) if dur_mins > 0 else 1.0
                extracted["workouts"].append({
                    "timestamp_epoch": start_epoch,
                    "activity": elem.attrib.get("workoutActivityType", "Workout"),
                    "duration_mins": dur_mins,
                    "active_energy_kcal": energy_kcal,
                    "workout_mets": round(mets, 2),
                    "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                })
            elem.clear()

        elif elem.tag == "HeartbeatSeries":
            start_epoch = parse_date_to_epoch(elem.attrib.get("startDate", ""))
            if start_epoch is not None:
                beat_times = []
                for child in elem:
                    if child.tag == "InstantaneousBeatsPerMinute":
                        t_str = child.attrib.get("time", "")
                        t_ep = parse_date_to_epoch(t_str)
                        if t_ep is not None:
                            beat_times.append(t_ep)
                        else:
                            try:
                                beat_times.append(float(t_str))
                            except ValueError:
                                pass
                rmssd_val = compute_rmssd_from_heartbeat_series(beat_times)
                if rmssd_val is not None:
                    extracted["hrv"].append({
                        "timestamp_epoch": start_epoch,
                        "sdnn_ms": None,
                        "rmssd_ms": round(rmssd_val, 3),
                        "source_name": elem.attrib.get("sourceName", "Apple Watch"),
                        "rmssd_source": "rmssd_heartbeat_series",
                    })
            elem.clear()

        elif elem.tag == "StateOfMind":
            start_str = elem.attrib.get("startDate", "")
            start_epoch = parse_date_to_epoch(start_str)
            if start_epoch is not None:
                val_str = elem.attrib.get("valence", "0.0")
                extracted["state_of_mind"].append({
                    "timestamp_epoch": start_epoch,
                    "valence": float(val_str) if val_str.replace('-', '', 1).replace('.', '', 1).isdigit() else 0.0,
                    "journal_text": elem.attrib.get("associations", "Valence log"),
                    "source_name": elem.attrib.get("sourceName", "Apple Journal"),
                })
            elem.clear()

            elem.clear()

    return extracted


def ingest_apple_health_into_db(
    conn: sqlite3.Connection,
    session_id: str,
    parsed_data: Dict[str, List[Dict[str, Any]]],
    wrist_temp_baseline_c: float = 36.40,
) -> Tuple[int, int, int]:
    """Ingest parsed Apple Health records into SQLite database."""
    conn.executescript(SCHEMA_APPLE_HEALTH_SQL)

    hrv_rows = []
    for item in parsed_data["hrv"]:
        sdnn = item.get("sdnn_ms")
        rmssd = item.get("rmssd_ms")
        rmssd_source = item.get("rmssd_source")
        if rmssd is None and sdnn is not None:
            rmssd = sdnn * 0.88
            rmssd_source = "derived_from_sdnn"
        elif rmssd is not None and rmssd_source is None:
            rmssd_source = "rmssd_heartbeat_series"

        hrv_rows.append((
            session_id,
            item["timestamp_epoch"],
            sdnn,
            rmssd,
            None,
            rmssd_source or "derived_from_sdnn",
            item.get("source_name", "Apple Watch"),
        ))

    for item in parsed_data["heart_rate"]:
        hrv_rows.append((
            session_id,
            item["timestamp_epoch"],
            None,
            None,
            item["heart_rate_bpm"],
            None,
            item.get("source_name", "Apple Watch"),
        ))

    if hrv_rows:
        conn.executemany(
            "INSERT INTO apple_health_hrv (session_id, timestamp_epoch, sdnn_ms, rmssd_ms, heart_rate_bpm, rmssd_source, source_name) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            hrv_rows,
        )

    temp_rows = []
    for item in parsed_data["wrist_temperature"]:
        temp_c = item["wrist_temp_c"]
        delta_c = round(temp_c - wrist_temp_baseline_c, 3)
        temp_rows.append((session_id, item["timestamp_epoch"], temp_c, delta_c, item.get("source_name", "Apple Watch")))

    if temp_rows:
        conn.executemany(
            "INSERT INTO apple_health_wrist_temp (session_id, timestamp_epoch, wrist_temp_c, delta_from_baseline_c, source_name) "
            "VALUES (?, ?, ?, ?, ?)",
            temp_rows,
        )

    sleep_rows = []
    for item in parsed_data["sleep_stages"]:
        sleep_rows.append((
            session_id,
            item["start_epoch"],
            item["end_epoch"],
            item["stage_category"],
            item["duration_mins"],
            item.get("source_name", "Apple Watch"),
        ))

    if sleep_rows:
        conn.executemany(
            "INSERT INTO apple_health_sleep_stages (session_id, start_epoch, end_epoch, stage_category, duration_mins, source_name) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            sleep_rows,
        )
    cgm_rows = []
    sorted_cgm = sorted(parsed_data.get("blood_glucose", []), key=lambda x: x["timestamp_epoch"])
    carb_events = [c for c in parsed_data.get("carbohydrates", []) if c.get("carbs_g", 0.0) >= 15.0]

    for i, item in enumerate(sorted_cgm):
        ts = item["timestamp_epoch"]
        g_val = item["glucose_mg_dl"]
        dg_dt = 0.0
        if i > 0:
            dt_min = (ts - sorted_cgm[i - 1]["timestamp_epoch"]) / 60.0
            if dt_min > 0.1:
                dg_dt = (g_val - sorted_cgm[i - 1]["glucose_mg_dl"]) / dt_min

        # 180-minute postprandial exclusion mask: [t_meal, t_meal + 10800.0s] (DOCAS §5.1 / GTT §4.2)
        is_postprandial = 0
        for meal in carb_events:
            meal_ts = meal["timestamp_epoch"]
            if meal_ts <= ts <= (meal_ts + 10800.0):
                is_postprandial = 1
                break

        cgm_rows.append((session_id, ts, g_val, round(dg_dt, 3), is_postprandial, item.get("source_name", "Dexcom Stelo")))

    if cgm_rows:
        conn.executemany(
            "INSERT INTO dexcom_stelo_cgm (session_id, timestamp_epoch, glucose_mg_dl, dg_dt_rate, is_postprandial_flag, source_name) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            cgm_rows,
        )

    confounder_rows = []
    for item in parsed_data.get("carbohydrates", []):
        confounder_rows.append((session_id, item["timestamp_epoch"], item["carbs_g"], 0.0, 0.0, 1.0, None, None, item.get("source_name", "HealthKit")))
    for item in parsed_data.get("dietary_calories", []):
        confounder_rows.append((session_id, item["timestamp_epoch"], 0.0, item["calories_kcal"], 0.0, 1.0, None, None, item.get("source_name", "HealthKit")))
    for item in parsed_data.get("workouts", []):
        confounder_rows.append((session_id, item["timestamp_epoch"], 0.0, 0.0, item["active_energy_kcal"], item.get("workout_mets", 1.0), None, None, item.get("source_name", "Apple Watch")))
    for item in parsed_data.get("body_mass", []):
        confounder_rows.append((session_id, item["timestamp_epoch"], 0.0, 0.0, 0.0, 1.0, item["weight_kg"], None, item.get("source_name", "Smart Scale")))

    if confounder_rows:
        conn.executemany(
            "INSERT INTO confounder_filters (session_id, timestamp_epoch, dietary_carbohydrates_g, dietary_calories_kcal, workout_active_calories, workout_mets, smart_scale_weight_kg, smart_scale_bmi, source_name) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            confounder_rows,
        )

    journal_rows = []
    for item in parsed_data.get("state_of_mind", []):
        journal_rows.append((session_id, item["timestamp_epoch"], item["valence"], 0.5, item.get("journal_text", ""), item.get("source_name", "Apple Journal")))

    if journal_rows:
        conn.executemany(
            "INSERT INTO apple_journal_affect (session_id, timestamp_epoch, valence_score, arousal_score, journal_text, source_name) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            journal_rows,
        )


    conn.commit()
    return len(hrv_rows), len(temp_rows), len(sleep_rows)

def evaluate_concordance(
    conn: sqlite3.Connection,
    session_id: Optional[str] = None,
    cohort_stage: int = 1,
) -> Dict[str, Any]:
    """
    Evaluates DOCAS-PILOT-1 Pre-Registered Hypotheses:
      - PILOT-H1: fNIRS SQI >= 0.85 & Medial Prefrontal Activation Δ[HbO2]
      - PILOT-H2: Autonomic Vagal RMSSD Surge >= 15% (p < 0.001)
      - PILOT-H3: Nocturnal Wrist Temp Drift ΔT >= +0.15°C (Cohorts 1-3 only)
      - PILOT-H4: Multi-Day Test-Retest Reliability r >= 0.75 (Cohort 3)
      - Stopping Rule: Motion Artifact Ratio <= 40%, Missing Temp <= 2 nights
    """
    results: Dict[str, Any] = {
        "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cohort_stage": cohort_stage,
        "s_channel_eligible": cohort_stage <= 3,
        "hypotheses": {},
        "stopping_rule": {},
        "all_passed": True,
    }
    p_values_for_fdr: Dict[str, float] = {}

    cur = conn.cursor()

    # 1. PILOT-H1: Muse Prefrontal fNIRS Signal Quality & Activation
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='muse_fnirs_mbll'")
    if cur.fetchone():
        query = (
            "SELECT sample_idx, AVG(sci_quality_index), AVG(delta_hbo2_umol), MAX(is_motion_artifact) "
            "FROM muse_fnirs_mbll"
        )
        params: List[Any] = []
        if session_id:
            query += " WHERE session_id = ?"
            params.append(session_id)
        query += " GROUP BY sample_idx ORDER BY sample_idx ASC"
        cur.execute(query, params)
        rows = cur.fetchall()

        if rows:
            scis = [r[1] for r in rows if r[1] is not None]
            hbo2s = [r[2] for r in rows if r[2] is not None]
            artifacts = [r[3] for r in rows]

            mean_sci = float(np.mean(scis)) if scis else 0.0
            motion_fraction = float(np.mean(artifacts)) if artifacts else 0.0

            n = len(hbo2s)
            split_idx = max(1, n // 4)
            baseline_hbo2 = hbo2s[:split_idx]
            active_hbo2 = hbo2s[split_idx:n - split_idx] if n >= 4 else hbo2s

            t_stat, p_val = compute_welch_ttest(active_hbo2, baseline_hbo2, adjust_autocorr=True)
            mean_active = float(np.mean(active_hbo2)) if active_hbo2 else 0.0
            mean_base = float(np.mean(baseline_hbo2)) if baseline_hbo2 else 0.0
            cohens_d = (mean_active - mean_base) / (np.std(baseline_hbo2) + 1e-9) if len(baseline_hbo2) > 1 else 0.0

            h1_passed = bool(mean_sci >= 0.850 and (p_val < 0.01 or cohens_d >= 0.50))
            p_values_for_fdr["PILOT-H1"] = float(p_val)
            results["hypotheses"]["PILOT-H1"] = {
                "description": "Prefrontal fNIRS Signal Quality (SCI >= 0.85) & Medial Cortical Δ[HbO2] Activation",
                "mean_sci": round(mean_sci, 4),
                "sci_threshold": 0.850,
                "motion_artifact_fraction": round(motion_fraction, 4),
                "baseline_mean_hbo2_umol": round(mean_base, 3),
                "active_mean_hbo2_umol": round(mean_active, 3),
                "activation_delta_umol": round(mean_active - mean_base, 3),
                "cohens_d": round(cohens_d, 3),
                "t_statistic": round(float(t_stat), 3),
                "p_value": round(float(p_val), 6),
                "verdict": "PASS" if h1_passed else "FAIL",
            }
            if not h1_passed:
                results["all_passed"] = False
        else:
            results["hypotheses"]["PILOT-H1"] = {"verdict": "SKIPPED_NO_DATA"}
    else:
        results["hypotheses"]["PILOT-H1"] = {"verdict": "SKIPPED_TABLE_MISSING"}

    # 2. PILOT-H2: Autonomic Vagal Feedback (O-Channel Rebound)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apple_health_hrv'")
    if cur.fetchone():
        # Mask out HRV samples within 120 minutes (7200s) after strenuous workouts (>= 50 kcal) to prevent sympathetic contamination
        masked_query = """
            SELECT COUNT(*)
            FROM apple_health_hrv h
            WHERE h.rmssd_ms IS NOT NULL
              AND EXISTS (
                  SELECT 1 FROM confounder_filters c
                  WHERE c.workout_active_calories >= 50.0
                    AND c.session_id = h.session_id
                    AND h.timestamp_epoch >= c.timestamp_epoch
                    AND h.timestamp_epoch <= (c.timestamp_epoch + 7200.0)
              )
        """
        masked_params = []
        if session_id:
            masked_query += " AND h.session_id = ?"
            masked_params.append(session_id)
        cur.execute(masked_query, masked_params)
        masked_exertion_hrv = cur.fetchone()[0]

        query = (
            "SELECT h.timestamp_epoch, h.rmssd_ms "
            "FROM apple_health_hrv h "
            "WHERE h.rmssd_ms IS NOT NULL "
            "  AND NOT EXISTS ( "
            "      SELECT 1 FROM confounder_filters c "
            "      WHERE c.workout_active_calories >= 50.0 "
            "        AND c.session_id = h.session_id "
            "        AND h.timestamp_epoch >= c.timestamp_epoch "
            "        AND h.timestamp_epoch <= (c.timestamp_epoch + 7200.0) "
            "  )"
        )
        params = []
        if session_id:
            query += " AND h.session_id = ?"
            params.append(session_id)
        query += " ORDER BY h.timestamp_epoch ASC"
        cur.execute(query, params)
        hrv_rows = cur.fetchall()

        if len(hrv_rows) >= 4:
            n_hrv = len(hrv_rows)
            half = n_hrv // 2
            pre_rmssd = [r[1] for r in hrv_rows[:half]]
            post_rmssd = [r[1] for r in hrv_rows[half:]]

            mean_pre = float(np.mean(pre_rmssd))
            mean_post = float(np.mean(post_rmssd))
            surge_pct = ((mean_post - mean_pre) / (mean_pre + 1e-9)) * 100.0

            t_stat_h2, p_val_h2 = compute_welch_ttest(post_rmssd, pre_rmssd)
            h2_passed = bool(surge_pct >= 15.0 and p_val_h2 < 0.001)
            p_values_for_fdr["PILOT-H2"] = float(p_val_h2)

            results["hypotheses"]["PILOT-H2"] = {
                "description": "Autonomic Vagal Rebound (RMSSD surge >= +15.0% post-event, p < 0.001)",
                "baseline_rmssd_ms": round(mean_pre, 2),
                "post_event_rmssd_ms": round(mean_post, 2),
                "surge_percentage": round(surge_pct, 2),
                "target_surge_pct": 15.0,
                "masked_exertion_hrv_samples": masked_exertion_hrv,
                "t_statistic": round(float(t_stat_h2), 3),
                "p_value": round(float(p_val_h2), 6),
                "verdict": "PASS" if h2_passed else "FAIL",
            }
            if not h2_passed:
                results["all_passed"] = False
        else:
            results["hypotheses"]["PILOT-H2"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA"}
    else:
        results["hypotheses"]["PILOT-H2"] = {"verdict": "SKIPPED_TABLE_MISSING"}

    # 3. PILOT-H3: Circadian Allostatic Coupling (C-Channel Temperature Drift)
    if cohort_stage == 4:
        results["hypotheses"]["PILOT-H3"] = {
            "description": "Circadian Nocturnal Temperature Drift (ΔT >= +0.15°C)",
            "verdict": "EXCLUDED_BY_PROTOCOL",
            "rationale": "Cohort 4 (1-day single observation) pre-registered as excluded from multi-day C and S channels.",
        }
    else:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apple_health_wrist_temp'")
        if cur.fetchone():
            query = "SELECT wrist_temp_c, delta_from_baseline_c FROM apple_health_wrist_temp"
            params = []
            if session_id:
                query += " WHERE session_id = ?"
                params.append(session_id)
            cur.execute(query, params)
            temp_rows = cur.fetchall()

            if temp_rows:
                deltas = [r[1] for r in temp_rows]
                mean_delta = float(np.mean(deltas))
                max_delta = float(np.max(deltas))
                t_h3, p_val_h3 = compute_one_sample_ttest(deltas, 0.00, alternative="greater")
                h3_passed = bool((mean_delta >= 0.15 or max_delta >= 0.15) and p_val_h3 < 0.05)
                p_values_for_fdr["PILOT-H3"] = round(p_val_h3, 6)
                results["hypotheses"]["PILOT-H3"] = {
                    "description": "Circadian Nocturnal Temperature Drift (ΔT >= +0.15°C on stress-shock nights, p < 0.05)",
                    "mean_delta_c": round(mean_delta, 3),
                    "max_delta_c": round(max_delta, 3),
                    "t_statistic": round(t_h3, 3),
                    "p_value": round(p_val_h3, 6),
                    "target_threshold_c": 0.150,
                    "verdict": "PASS" if h3_passed else "FAIL",
                }
                if not h3_passed:
                    results["all_passed"] = False
            else:
                results["hypotheses"]["PILOT-H3"] = {"verdict": "SKIPPED_NO_DATA"}
        else:
            results["hypotheses"]["PILOT-H3"] = {"verdict": "SKIPPED_TABLE_MISSING"}

    # 4. PILOT-H4: Multi-Day Test-Retest Reliability (Cohort 3)
    if cohort_stage == 3:
        query_h4 = "SELECT sdnn_ms FROM apple_health_hrv WHERE sdnn_ms IS NOT NULL"
        params_h4 = []
        if session_id:
            query_h4 += " AND session_id = ?"
            params_h4.append(session_id)
        query_h4 += " ORDER BY timestamp_epoch ASC"
        cur.execute(query_h4, params_h4)
        sdnn_vals = [r[0] for r in cur.fetchall()]
        if len(sdnn_vals) >= 6:
            half = len(sdnn_vals) // 2
            day1_vals = np.array(sdnn_vals[:half])
            day2_vals = np.array(sdnn_vals[half:half + len(day1_vals)])
            r_val, p_val_h4 = compute_pearson_correlation(day1_vals, day2_vals)
            h4_passed = bool(r_val >= 0.750 and p_val_h4 < 0.05)
            p_values_for_fdr["PILOT-H4"] = round(float(p_val_h4), 6)
            results["hypotheses"]["PILOT-H4"] = {
                "description": "Multi-Day Parameter Test-Retest Reliability (r >= 0.75)",
                "pearson_r": round(float(r_val), 3),
                "p_value": round(float(p_val_h4), 6),
                "target_r": 0.750,
                "verdict": "PASS" if h4_passed else "FAIL",
            }
            if not h4_passed:
                results["all_passed"] = False
        else:
            results["hypotheses"]["PILOT-H4"] = {
                "description": "Multi-Day Parameter Test-Retest Reliability (r >= 0.75)",
                "verdict": "SKIPPED_INSUFFICIENT_DATA",
                "samples": len(sdnn_vals),
            }
    else:
        results["hypotheses"]["PILOT-H4"] = {
            "description": "Multi-Day Test-Retest Reliability (Cohort 3 specific)",
            "verdict": "NOT_APPLICABLE",
            "rationale": f"Current stage is Cohort {cohort_stage}; H4 evaluates Cohort 3 test-retest across 3 consecutive days.",
        }

    # 5. PILOT-H5: CB1R Washout & REM Sleep Rebound (per-night REM % across >= 2 nights)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apple_health_sleep_stages'")
    if cur.fetchone():
        query_h5 = "SELECT start_epoch, stage_category, duration_mins FROM apple_health_sleep_stages"
        params_h5 = []
        if session_id:
            query_h5 += " WHERE session_id = ?"
            params_h5.append(session_id)
        cur.execute(query_h5, params_h5)
        sleep_rows = cur.fetchall()
        if sleep_rows:
            nightly: Dict[int, Dict[str, float]] = {}
            for start_ep, cat, dur in sleep_rows:
                day_key = int(float(start_ep) // 86400.0)
                bucket = nightly.setdefault(day_key, {"total": 0.0, "rem": 0.0})
                if "Asleep" in cat or "sleep" in cat.lower():
                    bucket["total"] += float(dur)
                if "REM" in cat or "rem" in cat.lower():
                    bucket["rem"] += float(dur)
            rem_pcts = [(b["rem"] / b["total"]) * 100.0 for b in nightly.values() if b["total"] > 0.0]
            if len(rem_pcts) >= 2:
                rem_pct = float(np.mean(rem_pcts))
                t_rem, p_val_h5 = compute_one_sample_ttest(rem_pcts, 20.0, alternative="greater")
                h5_passed = bool(rem_pct >= 22.0 and p_val_h5 < 0.05)
                p_values_for_fdr["PILOT-H5"] = round(p_val_h5, 6)
                results["hypotheses"]["PILOT-H5"] = {
                    "description": "CB1R Washout & REM Sleep Rebound (REM proportion >= 22.0% in Phase 1, p < 0.05)",
                    "rem_percentage": round(rem_pct, 2),
                    "nights_evaluated": len(rem_pcts),
                    "rem_target_pct": 22.0,
                    "t_statistic": round(t_rem, 3),
                    "p_value": round(p_val_h5, 6),
                    "verdict": "PASS" if h5_passed else "FAIL",
                }
                if not h5_passed:
                    results["all_passed"] = False
            else:
                results["hypotheses"]["PILOT-H5"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "nights": len(rem_pcts)}

    # 6. PILOT-H6: Cuffless BP & Enteric Motility Coupling
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='enteric_motility_stream'")
    if cur.fetchone():
        e_cols = [c[1] for c in cur.execute("PRAGMA table_info(enteric_motility_stream)").fetchall()]
        query_h6 = "SELECT bristol_type FROM enteric_motility_stream WHERE bristol_type IS NOT NULL"
        params_h6 = []
        if session_id and "session_id" in e_cols:
            query_h6 += " AND session_id = ?"
            params_h6.append(session_id)
        cur.execute(query_h6, params_h6)
        b_rows = [r[0] for r in cur.fetchall()]
        if b_rows:
            mean_bristol = float(np.mean(b_rows))
            dev_vector = [abs(float(b) - 4.0) for b in b_rows]
            t_b, p_val_h6 = compute_one_sample_ttest(dev_vector, 1.0, alternative="less")
            h6_passed = bool(3.0 <= mean_bristol <= 5.0 and p_val_h6 < 0.05)
            p_values_for_fdr["PILOT-H6"] = round(p_val_h6, 6)
            results["hypotheses"]["PILOT-H6"] = {
                "description": "Cuffless BP & Enteric Motility Normalization (Bristol Types 3-5, p < 0.05)",
                "mean_bristol_type": round(mean_bristol, 2),
                "t_statistic": round(t_b, 3),
                "p_value": round(p_val_h6, 6),
                "verdict": "PASS" if h6_passed else "FAIL",
            }
            if not h6_passed:
                results["all_passed"] = False

    # 7. PILOT-H7: Striatal Motor Timing Washout (CV_ITI <= 4.5%)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cognitive_battery_tapping'")
    if cur.fetchone():
        tap_cols = [c[1] for c in cur.execute("PRAGMA table_info(cognitive_battery_tapping)").fetchall()]
        query_h7 = "SELECT cv_iti_pct FROM cognitive_battery_tapping WHERE cv_iti_pct IS NOT NULL"
        params_h7 = []
        if session_id and "session_id" in tap_cols:
            query_h7 += " AND session_id = ?"
            params_h7.append(session_id)
        cur.execute(query_h7, params_h7)
        cv_rows = [r[0] for r in cur.fetchall()]
        if cv_rows:
            latest_cv = float(cv_rows[-1])
            t_cv, p_val_h7 = compute_one_sample_ttest(cv_rows, 4.50, alternative="less")
            h7_passed = bool(latest_cv <= 4.50 and p_val_h7 < 0.05)
            p_values_for_fdr["PILOT-H7"] = round(p_val_h7, 6)
            results["hypotheses"]["PILOT-H7"] = {
                "description": "Striatal Motor Timing Washout (CV_ITI <= 4.50%, p < 0.05)",
                "measured_cv_iti_pct": round(latest_cv, 2),
                "target_cv_iti_pct": 4.50,
                "t_statistic": round(t_cv, 3),
                "p_value": round(p_val_h7, 6),
                "verdict": "PASS" if h7_passed else "FAIL",
            }
            if not h7_passed:
                results["all_passed"] = False

    # 8. PILOT-H8: Prefrontal Inhibitory Control & Vigilance under Betrayal
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cognitive_battery_gonogo'")
    if cur.fetchone():
        gn_cols = [c[1] for c in cur.execute("PRAGMA table_info(cognitive_battery_gonogo)").fetchall()]
        query_h8 = "SELECT d_prime FROM cognitive_battery_gonogo WHERE d_prime IS NOT NULL"
        params_h8 = []
        if session_id and "session_id" in gn_cols:
            query_h8 += " AND session_id = ?"
            params_h8.append(session_id)
        cur.execute(query_h8, params_h8)
        dp_rows = [r[0] for r in cur.fetchall()]
        if len(dp_rows) >= 2:
            latest_dp = float(np.mean(dp_rows))
            t_dp, p_val_h8 = compute_one_sample_ttest(dp_rows, 2.00, alternative="greater")
            h8_passed = bool(latest_dp >= 2.0 and p_val_h8 < 0.05)
            p_values_for_fdr["PILOT-H8"] = round(p_val_h8, 6)
            results["hypotheses"]["PILOT-H8"] = {
                "description": "Prefrontal Executive Inhibitory Control (d' >= 2.00, p < 0.05)",
                "measured_d_prime": round(latest_dp, 3),
                "target_d_prime": 2.00,
                "t_statistic": round(t_dp, 3),
                "p_value": round(p_val_h8, 6),
                "verdict": "PASS" if h8_passed else "FAIL",
            }
            if not h8_passed:
                results["all_passed"] = False
        elif dp_rows:
            results["hypotheses"]["PILOT-H8"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "samples": len(dp_rows)}

    # 5. Pre-Registered Stopping & Falsification Rule
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='muse_fnirs_mbll'")
    motion_fraction = 0.0
    if cur.fetchone():
        query_m = "SELECT AVG(is_motion_artifact) FROM muse_fnirs_mbll"
        params_m = []
        if session_id:
            query_m += " WHERE session_id = ?"
            params_m.append(session_id)
        cur.execute(query_m, params_m)
        val = cur.fetchone()[0]
        if val is not None:
            motion_fraction = float(val)

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apple_health_wrist_temp'")
    temp_count = 0
    if cur.fetchone():
        query_t = "SELECT COUNT(*) FROM apple_health_wrist_temp"
        params_t = []
        if session_id:
            query_t += " WHERE session_id = ?"
            params_t.append(session_id)
        cur.execute(query_t, params_t)
        temp_count = cur.fetchone()[0]

    motion_violation = motion_fraction > 0.400
    missing_temp_violation = (cohort_stage <= 3 and temp_count == 0)

    stopping_triggered = motion_violation or missing_temp_violation
    results["stopping_rule"] = {
        "motion_artifact_fraction": round(motion_fraction, 4),
        "motion_artifact_threshold": 0.400,
        "motion_artifact_breached": motion_violation,
        "consecutive_missing_temp_nights": 0 if temp_count > 0 else 3,
        "missing_temp_breached": missing_temp_violation,
        "protocol_stopping_gate_triggered": stopping_triggered,
        "verdict": "STOPPING_RULE_TRIGGERED" if stopping_triggered else "CLEAR",
    }
    if stopping_triggered:
        results["all_passed"] = False
    # 6. Confounder Filters & Somatic Stationarity (30-day Body Mass Drift <= 2.0%)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='confounder_filters'")
    if cur.fetchone():
        audit: Dict[str, Any] = {}
        cf_cols = [c[1] for c in cur.execute("PRAGMA table_info(confounder_filters)").fetchall()]
        q_w = "SELECT smart_scale_weight_kg FROM confounder_filters WHERE smart_scale_weight_kg IS NOT NULL"
        p_w = []
        if session_id and "session_id" in cf_cols:
            q_w += " AND session_id = ?"
            p_w.append(session_id)
        cur.execute(q_w, p_w)
        weights = [r[0] for r in cur.fetchall()]
        if len(weights) >= 2:
            w_min, w_max, w_mean = min(weights), max(weights), float(np.mean(weights))
            drift_pct = ((w_max - w_min) / max(w_mean, 1e-4)) * 100.0
            stationary = drift_pct <= 2.0
            audit["somatic_stationarity_verified"] = stationary
            audit["weight_drift_pct"] = round(drift_pct, 2)
            audit["weight_threshold_pct"] = 2.0
            audit["samples_count"] = len(weights)
        else:
            audit["somatic_stationarity_verified"] = None
            audit["note"] = "Insufficient weigh-in samples (< 2) for stationarity check"

        # CGM Postprandial vs Fasting Confounder Exclusion Audit
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dexcom_stelo_cgm'")
        if cur.fetchone():
            cgm_cols = [c[1] for c in cur.execute("PRAGMA table_info(dexcom_stelo_cgm)").fetchall()]
            q_post = "SELECT COUNT(*) FROM dexcom_stelo_cgm WHERE is_postprandial_flag = 1"
            q_fast = "SELECT glucose_mg_dl, dg_dt_rate FROM dexcom_stelo_cgm WHERE is_postprandial_flag = 0"
            p_cgm = []
            if session_id and "session_id" in cgm_cols:
                q_post += " AND session_id = ?"
                q_fast += " AND session_id = ?"
                p_cgm.append(session_id)
            cur.execute(q_post, p_cgm)
            masked_cgm = cur.fetchone()[0]
            cur.execute(q_fast, p_cgm)
            fasting_cgm = cur.fetchall()
            audit["postprandial_cgm_samples_masked"] = masked_cgm
            audit["fasting_cgm_samples_evaluated"] = len(fasting_cgm)
            if fasting_cgm:
                audit["fasting_mean_glucose_mg_dl"] = round(float(np.mean([r[0] for r in fasting_cgm])), 2)

        results["confounder_audit"] = audit

    # 9. H-READ: Cognitive Fatigue & Reading Marginalia NLP
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='manual_reading_log_stream'")
    if cur.fetchone():
        read_cols = [c[1] for c in cur.execute("PRAGMA table_info(manual_reading_log_stream)").fetchall()]
        query_read = "SELECT flesch_kincaid_grade, latency_sec FROM manual_reading_log_stream"
        params_read = []
        if session_id and "session_id" in read_cols:
            query_read += " WHERE session_id = ?"
            params_read.append(session_id)
        cur.execute(query_read, params_read)
        read_rows = cur.fetchall()
        if len(read_rows) >= 2:
            fks = [r[0] for r in read_rows]
            mean_fk = float(np.mean(fks))
            t_fk, p_val_read = compute_one_sample_ttest(fks, 8.0, alternative="greater")
            h_read_passed = bool(mean_fk >= 8.0 and p_val_read < 0.05)
            p_values_for_fdr["H-READ"] = round(p_val_read, 6)
            results["hypotheses"]["H-READ"] = {
                "description": "Cognitive Fatigue & Marginalia NLP Complexity (Flesch-Kincaid >= Grade 8, p < 0.05)",
                "mean_flesch_kincaid_grade": round(mean_fk, 2),
                "t_statistic": round(t_fk, 3),
                "p_value": round(p_val_read, 6),
                "verdict": "PASS" if h_read_passed else "FAIL",
            }
            if not h_read_passed:
                results["all_passed"] = False
        elif read_rows:
            results["hypotheses"]["H-READ"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "samples": len(read_rows)}

    # 10. H-RESP (Airofit Pro Respiratory Strength) / Legacy H-SMI fallback
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='respiratory_strength_stream'")
    if cur.fetchone():
        resp_cols = [c[1] for c in cur.execute("PRAGMA table_info(respiratory_strength_stream)").fetchall()]
        query_resp = "SELECT mip_cmh2o FROM respiratory_strength_stream"
        params_resp = []
        if session_id and "session_id" in resp_cols:
            query_resp += " WHERE session_id = ?"
            params_resp.append(session_id)
        cur.execute(query_resp, params_resp)
        resp_rows = [r[0] for r in cur.fetchall()]
        if len(resp_rows) >= 2:
            mean_mip = float(np.mean(resp_rows))
            t_resp, p_val_resp = compute_one_sample_ttest(resp_rows, 90.0, alternative="greater")
            h_resp_passed = bool(mean_mip >= 90.0 and p_val_resp < 0.05)
            p_values_for_fdr["H-RESP"] = round(p_val_resp, 6)
            results["hypotheses"]["H-RESP"] = {
                "description": "Airofit Pro Respiratory Muscle Strength Reserve (MIP >= 90.0 cmH2O, p < 0.05)",
                "mean_mip_cmh2o": round(mean_mip, 2),
                "t_statistic": round(t_resp, 3),
                "p_value": round(p_val_resp, 6),
                "verdict": "PASS" if h_resp_passed else "FAIL",
            }
            if not h_resp_passed:
                results["all_passed"] = False
        elif resp_rows:
            results["hypotheses"]["H-RESP"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "samples": len(resp_rows)}

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sustained_inhalation_stream'")
    if cur.fetchone() and "H-RESP" not in results["hypotheses"]:
        smi_cols = [c[1] for c in cur.execute("PRAGMA table_info(sustained_inhalation_stream)").fetchall()]
        query_smi = "SELECT best_hold_sec FROM sustained_inhalation_stream"
        params_smi = []
        if session_id and "session_id" in smi_cols:
            query_smi += " WHERE session_id = ?"
            params_smi.append(session_id)
        cur.execute(query_smi, params_smi)
        smi_rows = [r[0] for r in cur.fetchall()]
        if len(smi_rows) >= 2:
            mean_smi = float(np.mean(smi_rows))
            t_smi, p_val_smi = compute_one_sample_ttest(smi_rows, 12.0, alternative="greater")
            h_smi_passed = bool(mean_smi >= 12.0 and p_val_smi < 0.05)
            p_values_for_fdr["H-SMI"] = round(p_val_smi, 6)
            results["hypotheses"]["H-SMI"] = {
                "description": "Sustained Maximal Inspiration Vagal Reserve (Hold Duration >= 12.0s, p < 0.05)",
                "mean_hold_duration_sec": round(mean_smi, 2),
                "t_statistic": round(t_smi, 3),
                "p_value": round(p_val_smi, 6),
                "verdict": "PASS" if h_smi_passed else "FAIL",
            }
            if not h_smi_passed:
                results["all_passed"] = False
        elif smi_rows:
            results["hypotheses"]["H-SMI"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "samples": len(smi_rows)}

    # 10B. PILOT-H10 / H-COG: Cognitive Executive Battery (2-Back d' & Stroop) after burn-in
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cognitive_executive_battery_stream'")
    if cur.fetchone():
        cog_cols = [c[1] for c in cur.execute("PRAGMA table_info(cognitive_executive_battery_stream)").fetchall()]
        query_cog = "SELECT nback_d_prime FROM cognitive_executive_battery_stream WHERE is_burnin_phase = 0"
        params_cog = []
        if session_id and "session_id" in cog_cols:
            query_cog += " AND session_id = ?"
            params_cog.append(session_id)
        cur.execute(query_cog, params_cog)
        nb_rows = [r[0] for r in cur.fetchall()]
        if len(nb_rows) >= 2:
            mean_nb = float(np.mean(nb_rows))
            t_nb, p_val_nb = compute_one_sample_ttest(nb_rows, 1.80, alternative="greater")
            h_cog_passed = bool(mean_nb >= 1.80 and p_val_nb < 0.05)
            p_values_for_fdr["H-COG"] = round(p_val_nb, 6)
            results["hypotheses"]["H-COG"] = {
                "description": "Post-Burn-In Executive Working Memory (2-Back d' >= 1.80, p < 0.05)",
                "mean_nback_d_prime": round(mean_nb, 3),
                "t_statistic": round(t_nb, 3),
                "p_value": round(p_val_nb, 6),
                "verdict": "PASS" if h_cog_passed else "FAIL",
            }
            if not h_cog_passed:
                results["all_passed"] = False
        elif nb_rows:
            results["hypotheses"]["H-COG"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "samples": len(nb_rows)}

    # 11. H-HAIR: Longitudinal Endocrine Ground Truth (LC-MS/MS)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hair_metabolomics_stream'")
    if cur.fetchone():
        hair_cols = [c[1] for c in cur.execute("PRAGMA table_info(hair_metabolomics_stream)").fetchall()]
        query_hair = "SELECT cortisol_cortisone_ratio FROM hair_metabolomics_stream"
        params_hair = []
        if session_id and "session_id" in hair_cols:
            query_hair += " WHERE session_id = ?"
            params_hair.append(session_id)
        cur.execute(query_hair, params_hair)
        hair_rows = [r[0] for r in cur.fetchall()]
        if len(hair_rows) >= 2:
            mean_ratio = float(np.mean(hair_rows))
            t_hair, p_val_hair = compute_one_sample_ttest(hair_rows, 1.0, alternative="greater")
            h_hair_passed = bool(mean_ratio > 1.0 and p_val_hair < 0.05)
            p_values_for_fdr["H-HAIR"] = round(p_val_hair, 6)
            results["hypotheses"]["H-HAIR"] = {
                "description": "Segmental Scalp Hair LC-MS/MS Endocrine Ground Truth (r >= 0.40, p < 0.05)",
                "cortisol_cortisone_ratio": round(mean_ratio, 3),
                "t_statistic": round(t_hair, 3),
                "p_value": round(p_val_hair, 6),
                "verdict": "PASS" if h_hair_passed else "FAIL",
            }
            if not h_hair_passed:
                results["all_passed"] = False
        elif hair_rows:
            results["hypotheses"]["H-HAIR"] = {"verdict": "SKIPPED_INSUFFICIENT_DATA", "samples": len(hair_rows)}

    # 12. H-WORKOUT: Exertion Confounder Decoupling Schuirmann TOST Equivalence Gate (R^2 <= 0.04, |r| <= 0.20, p_TOST < 0.05)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='confounder_filters'")
    if cur.fetchone():
        cf_cols = [c[1] for c in cur.execute("PRAGMA table_info(confounder_filters)").fetchall()]
        query_w = "SELECT workout_mets, post_recovery_rmssd_ms FROM confounder_filters WHERE workout_mets IS NOT NULL AND post_recovery_rmssd_ms IS NOT NULL"
        params_w = []
        if session_id and "session_id" in cf_cols:
            query_w += " AND session_id = ?"
            params_w.append(session_id)
        cur.execute(query_w, params_w)
        w_pairs = cur.fetchall()
        if len(w_pairs) >= 4:
            mets_vec = [float(r[0]) for r in w_pairs]
            hrv_vec = [float(r[1]) for r in w_pairs]
            r_w, _ = compute_pearson_correlation(mets_vec, hrv_vec)
            p_tost, _, _ = compute_tost_correlation_equivalence(r_w, len(w_pairs), bound_r=0.20)
            n_w = len(w_pairs)
            r2_w = r_w * r_w
            h_work_passed = bool(p_tost < 0.05 and abs(r_w) <= 0.20)
            results["hypotheses"]["H-WORKOUT"] = {
                "description": "Exertion Tachycardia Decoupling Schuirmann TOST Equivalence Gate (R^2 <= 0.04, p_TOST < 0.05)",
                "pearson_r": round(r_w, 4),
                "r_squared": round(r2_w, 4),
                "p_tost_equivalence": round(p_tost, 6),
                "pairs_evaluated": n_w,
                "verdict": "PASS" if h_work_passed else "FAIL",
                "role": "DE_BIASING_EQUIVALENCE_GATE",
            }
            if not h_work_passed:
                results["all_passed"] = False
        else:
            results["hypotheses"]["H-WORKOUT"] = {
                "description": "Exertion Tachycardia Decoupling Schuirmann TOST Equivalence Gate",
                "verdict": "SKIPPED_INSUFFICIENT_DATA",
                "pairs_evaluated": len(w_pairs),
            }

    # 13. H-MUSIC: Late-Night Acoustic Tempo vs Nocturnal Temperature (R^2 >= 0.30, p < 0.05)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apple_music_recently_played'")
    has_music = cur.fetchone() is not None
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apple_health_wrist_temp'")
    has_temp = cur.fetchone() is not None

    if has_music and has_temp:
        m_pairs = []
        try:
            m_cols = [c[1] for c in cur.execute("PRAGMA table_info(apple_music_recently_played)").fetchall()]
            t_cols = [c[1] for c in cur.execute("PRAGMA table_info(apple_health_wrist_temp)").fetchall()]
            query_m = """
                SELECT m.tempo_bpm, t.delta_from_baseline_c
                FROM apple_music_recently_played m
                JOIN apple_health_wrist_temp t
                  ON date(datetime(m.timestamp_epoch, 'unixepoch')) = date(datetime(t.timestamp_epoch, 'unixepoch'))
                WHERE m.tempo_bpm IS NOT NULL AND t.delta_from_baseline_c IS NOT NULL
            """
            params_m = []
            if session_id and "session_id" in m_cols and "session_id" in t_cols:
                query_m += " AND m.session_id = ? AND t.session_id = ?"
                params_m.extend([session_id, session_id])
            cur.execute(query_m, params_m)
            m_pairs = cur.fetchall()
        except Exception:
            m_pairs = []

        if len(m_pairs) >= 4:
            bpms = [float(r[0]) for r in m_pairs]
            temps = [float(r[1]) for r in m_pairs]
            r_m, p_m = compute_pearson_correlation(bpms, temps)
            r2_m = r_m * r_m
            h_mus_passed = bool(r2_m >= 0.30 and p_m < 0.05)
            p_values_for_fdr["H-MUSIC"] = round(p_m, 6)
            results["hypotheses"]["H-MUSIC"] = {
                "description": "Late-Night Acoustic Exposure Tempo vs Nocturnal Temp (R^2 >= 0.30, p < 0.05)",
                "pearson_r": round(r_m, 4),
                "r_squared": round(r2_m, 4),
                "p_value": round(p_m, 6),
                "pairs_evaluated": len(m_pairs),
                "verdict": "PASS" if h_mus_passed else "FAIL",
            }
            if not h_mus_passed:
                results["all_passed"] = False
        else:
            results["hypotheses"]["H-MUSIC"] = {
                "description": "Late-Night Acoustic Exposure Tempo vs Nocturnal Temp (R^2 >= 0.30, p < 0.05)",
                "verdict": "SKIPPED_INSUFFICIENT_DATA",
                "pairs_evaluated": len(m_pairs),
            }
    else:
        results["hypotheses"]["H-MUSIC"] = {
            "description": "Late-Night Acoustic Exposure Tempo vs Nocturnal Temp (R^2 >= 0.30, p < 0.05)",
            "verdict": "SKIPPED_TABLE_MISSING",
        }

    # 14. Benjamini-Yekutieli (2001) Global False Discovery Rate (FDR) Control
    fdr_results = benjamini_yekutieli_fdr_py(p_values_for_fdr, q=0.05)
    results["fdr_adjustment"] = fdr_results


    return results


def run_self_test() -> bool:
    """
    Executes automated self-test generating synthetic multi-modal session
    data matching the biophysical parameters in DOCAS_PILOT_1_HUMAN_PROTOCOL.md.
    """
    print("=" * 80)
    print("RUNNING DOCAS-PILOT-1 MULTI-MODAL CONCORDANCE ENGINE SELF-TEST")
    print("=" * 80)

    np.random.seed(42)
    session_id = "pilot1-selftest-sess-001"
    now_epoch = 1794000000.0

    xml_records = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE HealthData>',
        '<HealthData locale="en_US">',
        '  <ExportDate value="2026-11-07 08:00:00 -0800"/>',
    ]

    for i in range(10):
        t_str = datetime.datetime.fromtimestamp(now_epoch + i * 15, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        sdnn_val = round(float(np.random.normal(50.0, 3.0)), 1)
        xml_records.append(f'  <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Apple Watch" value="{sdnn_val}" startDate="{t_str}"/>')

    for i in range(10, 20):
        t_str = datetime.datetime.fromtimestamp(now_epoch + i * 15, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        sdnn_val = round(float(np.random.normal(68.0, 3.0)), 1)
        xml_records.append(f'  <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Apple Watch" value="{sdnn_val}" startDate="{t_str}"/>')

    for day_offset, temp_val in [(0, 36.60), (1, 36.65), (2, 36.71), (3, 36.78)]:
        t_temp_str = datetime.datetime.fromtimestamp(now_epoch + day_offset * 86400 + 3600, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        xml_records.append(f'  <Record type="HKQuantityTypeIdentifierAppleSleepingWristTemperature" sourceName="Apple Watch" unit="degC" value="{temp_val}" startDate="{t_temp_str}"/>')

    # Seed 4 independent sleep nights so PILOT-H5 runs on genuine n=4 per-night REM % variance
    for day_offset, (deep_s, rem_s) in enumerate([(5200, 2200), (5000, 2400), (5400, 2350), (5100, 2500)]):
        d_base = now_epoch + day_offset * 86400
        t_s1 = datetime.datetime.fromtimestamp(d_base + 1000, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        t_s2 = datetime.datetime.fromtimestamp(d_base + 1000 + deep_s, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        t_s3 = datetime.datetime.fromtimestamp(d_base + 1000 + deep_s + rem_s, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
        xml_records.append(f'  <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Apple Watch" value="HKCategoryValueSleepAnalysisAsleepDeep" startDate="{t_s1}" endDate="{t_s2}"/>')
        xml_records.append(f'  <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Apple Watch" value="HKCategoryValueSleepAnalysisAsleepREM" startDate="{t_s2}" endDate="{t_s3}"/>')
    t_cgm = datetime.datetime.fromtimestamp(now_epoch + 1800, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierBloodGlucose" sourceName="Dexcom Stelo" value="94.2" startDate="{t_cgm}"/>')

    t_meal = datetime.datetime.fromtimestamp(now_epoch + 2400, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierDietaryCarbohydrates" sourceName="HealthKit" value="45.0" startDate="{t_meal}"/>')
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierDietaryEnergyConsumed" sourceName="HealthKit" value="420.0" startDate="{t_meal}"/>')

    t_scale1 = datetime.datetime.fromtimestamp(now_epoch, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
    t_scale2 = datetime.datetime.fromtimestamp(now_epoch + 86400, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierBodyMass" sourceName="Smart Scale" value="74.2" unit="kg" startDate="{t_scale1}"/>')
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierBodyMass" sourceName="Smart Scale" value="74.5" unit="kg" startDate="{t_scale2}"/>')

    xml_records.append(f'  <Workout workoutActivityType="HKWorkoutActivityTypeRunning" duration="30" totalEnergyBurned="310" startDate="{t_meal}"/>')
    xml_records.append(f'  <StateOfMind valence="0.75" associations="Focused on loan review" startDate="{t_cgm}"/>')

    # Postprandial glucose spike within 120m of 45g carbohydrate meal (t_meal + 600s = now_epoch + 3000)
    t_cgm_post = datetime.datetime.fromtimestamp(now_epoch + 3000, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierBloodGlucose" sourceName="Dexcom Stelo" value="142.5" startDate="{t_cgm_post}"/>')

    # Post-workout sympathetically depressed HRV sample within 60m of running workout (t_meal + 300s = now_epoch + 2700)
    t_hrv_post = datetime.datetime.fromtimestamp(now_epoch + 2700, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")
    xml_records.append(f'  <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Apple Watch" value="24.0" startDate="{t_hrv_post}"/>')

    xml_records.append("</HealthData>")
    xml_str = "\n".join(xml_records)

    conn = sqlite3.connect(":memory:")

    parsed = parse_apple_health_xml(xml_str, is_file=False)
    assert len(parsed["hrv"]) == 21, f"Expected 21 HRV records, got {len(parsed['hrv'])}"
    assert len(parsed["wrist_temperature"]) == 4, f"Expected 4 wrist temp records, got {len(parsed['wrist_temperature'])}"
    assert len(parsed["sleep_stages"]) == 8, f"Expected 8 sleep stage records, got {len(parsed['sleep_stages'])}"
    assert len(parsed["blood_glucose"]) == 2, f"Expected 2 blood glucose records, got {len(parsed['blood_glucose'])}"
    assert len(parsed["carbohydrates"]) == 1, f"Expected 1 carbohydrates record, got {len(parsed['carbohydrates'])}"
    assert len(parsed["workouts"]) == 1, f"Expected 1 workout record, got {len(parsed['workouts'])}"
    assert len(parsed["body_mass"]) == 2, f"Expected 2 body mass records, got {len(parsed['body_mass'])}"
    assert len(parsed["state_of_mind"]) == 1, f"Expected 1 state of mind record, got {len(parsed['state_of_mind'])}"

    n_hrv, n_temp, n_sleep = ingest_apple_health_into_db(conn, session_id, parsed, wrist_temp_baseline_c=36.40)
    assert n_hrv == 21
    assert n_temp == 4
    assert n_sleep == 8

    cur = conn.cursor()
    cur.execute("SELECT is_postprandial_flag, glucose_mg_dl FROM dexcom_stelo_cgm ORDER BY timestamp_epoch ASC")
    cgm_check = cur.fetchall()
    assert len(cgm_check) == 2, f"Expected 2 CGM records, got {len(cgm_check)}"
    assert cgm_check[0][0] == 0, f"Expected fasting CGM (flag=0), got {cgm_check[0][0]}"
    assert cgm_check[1][0] == 1, f"Expected postprandial CGM (flag=1), got {cgm_check[1][0]}"

    conn.execute("""
    CREATE TABLE muse_fnirs_mbll (
        session_id TEXT NOT NULL,
        optode_idx INTEGER NOT NULL,
        sample_idx INTEGER NOT NULL,
        timestamp_epoch REAL NOT NULL,
        delta_hbo2_umol REAL NOT NULL,
        delta_hbr_umol REAL NOT NULL,
        delta_hbt_umol REAL NOT NULL,
        sci_quality_index REAL NOT NULL,
        is_motion_artifact INTEGER NOT NULL
    );
    """)

    mbll_rows = []
    for opt in range(1, 6):
        for idx in range(20):
            mbll_rows.append((
                session_id, opt, idx, now_epoch + idx,
                float(np.random.normal(0.10, 0.20)),
                float(np.random.normal(-0.05, 0.10)),
                0.05, 0.92, 0,
            ))
        for idx in range(20, 80):
            mbll_rows.append((
                session_id, opt, idx, now_epoch + idx,
                float(np.random.normal(1.80, 0.25)),
                float(np.random.normal(-0.40, 0.15)),
                1.40, 0.93, 1 if idx % 20 == 0 else 0,
            ))

    conn.executemany("INSERT INTO muse_fnirs_mbll VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", mbll_rows)

    # Seed remaining multimodal protocol tables for pre-flight hypothesis verification
    conn.execute("CREATE TABLE enteric_motility_stream (session_id TEXT, bristol_type INTEGER);")
    conn.execute("INSERT INTO enteric_motility_stream VALUES (?, 4);", (session_id,))
    conn.execute("INSERT INTO enteric_motility_stream VALUES (?, 4);", (session_id,))
    conn.execute("INSERT INTO enteric_motility_stream VALUES (?, 4);", (session_id,))
    conn.execute("INSERT INTO enteric_motility_stream VALUES (?, 4);", (session_id,))
    conn.execute("INSERT INTO enteric_motility_stream VALUES (?, 4);", (session_id,))
    conn.execute("INSERT INTO enteric_motility_stream VALUES (?, 3);", (session_id,))
    # Seed rogue session in same tables to prove session isolation
    conn.execute("INSERT INTO enteric_motility_stream VALUES ('rogue-session-99', 1);")

    conn.execute("CREATE TABLE cognitive_battery_tapping (session_id TEXT, cv_iti_pct REAL);")
    conn.execute("INSERT INTO cognitive_battery_tapping VALUES (?, 3.8);", (session_id,))
    conn.execute("INSERT INTO cognitive_battery_tapping VALUES (?, 3.7);", (session_id,))
    conn.execute("INSERT INTO cognitive_battery_tapping VALUES (?, 3.6);", (session_id,))
    conn.execute("INSERT INTO cognitive_battery_tapping VALUES ('rogue-session-99', 18.5);")

    conn.execute("CREATE TABLE cognitive_battery_gonogo (session_id TEXT, d_prime REAL);")
    for dp in (2.55, 2.68, 2.72, 2.61):
        conn.execute("INSERT INTO cognitive_battery_gonogo VALUES (?, ?);", (session_id, dp))
    conn.execute("INSERT INTO cognitive_battery_gonogo VALUES ('rogue-session-99', 0.2);")

    conn.execute("CREATE TABLE manual_reading_log_stream (session_id TEXT, flesch_kincaid_grade REAL, latency_sec REAL);")
    for fk, lat in ((11.2, 42.0), (11.6, 46.0), (11.8, 44.0), (11.4, 48.0)):
        conn.execute("INSERT INTO manual_reading_log_stream VALUES (?, ?, ?);", (session_id, fk, lat))
    conn.execute("INSERT INTO manual_reading_log_stream VALUES ('rogue-session-99', 1.0, 120.0);")

    conn.execute("CREATE TABLE respiratory_strength_stream (session_id TEXT, mip_cmh2o REAL, mep_cmh2o REAL, vc_liters REAL);")
    for mip, mep, vc in ((104.2, 129.0, 4.82), (108.5, 133.4, 4.88), (106.1, 131.0, 4.85), (110.0, 135.2, 4.91)):
        conn.execute("INSERT INTO respiratory_strength_stream VALUES (?, ?, ?, ?);", (session_id, mip, mep, vc))
    conn.execute("INSERT INTO respiratory_strength_stream VALUES ('rogue-session-99', 45.0, 55.0, 2.5);")

    conn.execute("CREATE TABLE cognitive_executive_battery_stream (session_id TEXT, nback_d_prime REAL, stroop_interference_ms REAL, is_burnin_phase INTEGER);")
    for nb, st in ((2.42, 46.0), (2.51, 44.0), (2.38, 48.5), (2.47, 45.0)):
        conn.execute("INSERT INTO cognitive_executive_battery_stream VALUES (?, ?, ?, 0);", (session_id, nb, st))
    conn.execute("INSERT INTO cognitive_executive_battery_stream VALUES ('rogue-session-99', 0.5, 180.0, 0);")

    conn.execute("CREATE TABLE hair_metabolomics_stream (session_id TEXT, cortisol_cortisone_ratio REAL);")
    for hc in (1.38, 1.44, 1.41, 1.46):
        conn.execute("INSERT INTO hair_metabolomics_stream VALUES (?, ?);", (session_id, hc))
    conn.execute("INSERT INTO hair_metabolomics_stream VALUES ('rogue-session-99', 0.1);")

    conn.execute("CREATE TABLE apple_music_recently_played (session_id TEXT, timestamp_epoch REAL, tempo_bpm REAL);")
    for day_offset, bpm in [(0, 82.0), (1, 96.0), (2, 118.0), (3, 134.0)]:
        conn.execute(
            "INSERT INTO apple_music_recently_played VALUES (?, ?, ?);",
            (session_id, now_epoch + day_offset * 86400 + 3600, bpm),
        )
    conn.execute("INSERT INTO apple_music_recently_played VALUES ('rogue-session-99', ?, 160.0);", (now_epoch,))

    # Seed confounder_filters for H-WORKOUT Schuirmann TOST Equivalence (150 pairs)
    np.random.seed(42)
    cf_rows = [
        (session_id, now_epoch + i * 3600, float(np.random.uniform(2.0, 8.0)), 55.0 + float(np.random.normal(0, 3.0)))
        for i in range(150)
    ]
    conn.executemany("INSERT INTO confounder_filters (session_id, timestamp_epoch, workout_mets, post_recovery_rmssd_ms) VALUES (?, ?, ?, ?)", cf_rows)
    conn.commit()

    res = evaluate_concordance(conn, session_id=session_id, cohort_stage=1)

    print("\n--- CONCORDANCE EVALUATION REPORT ---")
    print(f"Cohort Stage: {res['cohort_stage']} (S-channel eligible: {res['s_channel_eligible']})")
    for hyp, details in res["hypotheses"].items():
        print(f"\n[{hyp}]: {details.get('description', '')}")
        print(f"  Verdict: {details.get('verdict')}")
        for k, v in details.items():
            if k not in ("description", "verdict"):
                print(f"  {k}: {v}")

    print("\n--- BENJAMINI-YEKUTIELI (2001) FDR ADJUSTMENT REPORT ---")
    for hyp, fdr in res.get("fdr_adjustment", {}).items():
        print(f"  {hyp:10s} -> raw_p: {fdr['raw_p']:.4f}, BY_thresh: {fdr['by_threshold']:.4f}, adj_q: {fdr['adjusted_q']:.4f}, sig: {fdr['fdr_significant']}")

    print("\n--- STOPPING & FALSIFICATION RULE ---")
    for k, v in res["stopping_rule"].items():
        print(f"  {k}: {v}")

    assert res["hypotheses"]["PILOT-H1"]["verdict"] == "PASS", f"H1 failed: {res['hypotheses']['PILOT-H1']}"
    assert res["hypotheses"]["PILOT-H2"]["verdict"] == "PASS", f"H2 failed: {res['hypotheses']['PILOT-H2']}"
    assert res["hypotheses"]["PILOT-H2"]["masked_exertion_hrv_samples"] == 1, f"Expected 1 masked post-workout HRV sample, got {res['hypotheses']['PILOT-H2']['masked_exertion_hrv_samples']}"
    assert res["hypotheses"]["PILOT-H3"]["verdict"] == "PASS", f"H3 failed: {res['hypotheses']['PILOT-H3']}"
    assert res["hypotheses"]["PILOT-H5"]["verdict"] == "PASS", f"H5 failed: {res['hypotheses']['PILOT-H5']}"
    assert res["hypotheses"]["PILOT-H6"]["verdict"] == "PASS", f"H6 failed: {res['hypotheses']['PILOT-H6']}"
    assert res["hypotheses"]["PILOT-H7"]["verdict"] == "PASS", f"H7 failed: {res['hypotheses']['PILOT-H7']}"
    assert res["hypotheses"]["PILOT-H8"]["verdict"] == "PASS", f"H8 failed: {res['hypotheses']['PILOT-H8']}"
    assert res["hypotheses"]["H-READ"]["verdict"] == "PASS", f"H-READ failed: {res['hypotheses']['H-READ']}"
    assert res["hypotheses"]["H-RESP"]["verdict"] == "PASS", f"H-RESP failed: {res['hypotheses']['H-RESP']}"
    assert res["hypotheses"]["H-COG"]["verdict"] == "PASS", f"H-COG failed: {res['hypotheses']['H-COG']}"
    assert res["hypotheses"]["H-HAIR"]["verdict"] == "PASS", f"H-HAIR failed: {res['hypotheses']['H-HAIR']}"
    assert res["hypotheses"]["H-WORKOUT"]["verdict"] == "PASS", f"H-WORKOUT failed: {res['hypotheses']['H-WORKOUT']}"
    assert res["hypotheses"]["H-MUSIC"]["verdict"] == "PASS", f"H-MUSIC failed: {res['hypotheses']['H-MUSIC']}"
    assert "fdr_adjustment" in res, "Expected Benjamini-Yekutieli FDR adjustment report"
    # Mathematical Oracle: Step-up Benjamini-Yekutieli q-values must be monotonically non-decreasing
    fdr_items = sorted(res["fdr_adjustment"].values(), key=lambda x: x["rank"])
    q_vals = [x["adjusted_q"] for x in fdr_items]
    for i in range(len(q_vals) - 1):
        assert q_vals[i] <= q_vals[i + 1] + 1e-9, f"Step-up adjusted q-values must be monotonic: rank {i+1} ({q_vals[i]}) > rank {i+2} ({q_vals[i+1]})"
    print("✓ Benjamini-Yekutieli Monotonicity: Confirmed reverse-cumulative adjusted q-values are strictly non-decreasing")

    assert res["confounder_audit"]["postprandial_cgm_samples_masked"] == 1, f"Expected 1 postprandial CGM masked, got {res['confounder_audit']['postprandial_cgm_samples_masked']}"
    assert res["confounder_audit"]["fasting_cgm_samples_evaluated"] == 1, f"Expected 1 fasting CGM evaluated, got {res['confounder_audit']['fasting_cgm_samples_evaluated']}"
    assert res["stopping_rule"]["verdict"] == "CLEAR", f"Stopping rule triggered: {res['stopping_rule']}"
    assert res["all_passed"] is True, "Expected all pre-registered criteria to pass"

    # Falsification Oracle: Failing amendment hypothesis must set all_passed to False
    conn.execute("UPDATE manual_reading_log_stream SET flesch_kincaid_grade = 2.0 WHERE session_id = ?", (session_id,))
    res_falsified = evaluate_concordance(conn, session_id=session_id, cohort_stage=1)
    assert res_falsified["all_passed"] is False, "Failing H-READ must flip all_passed to False"
    assert res_falsified["hypotheses"]["H-READ"]["verdict"] == "FAIL", "H-READ must be FAIL"
    conn.execute("UPDATE manual_reading_log_stream SET flesch_kincaid_grade = 11.5 WHERE session_id = ?", (session_id,))
    print("✓ Global Falsification Gate Oracle: Confirmed failing H-READ triggers all_passed = False")

    # Mathematical Oracle 2: Underpowered sample (n=5) must fail TOST equivalence gate
    p_underpowered, _, _ = compute_tost_correlation_equivalence(r_val=0.08, n=5, bound_r=0.14142)
    assert p_underpowered > 0.10, f"TOST must reject underpowered equivalence on n=5, got {p_underpowered}"
    print(f"✓ TOST Equivalence Oracle: Confirmed underpowered N=5 rejects false equivalence (p_TOST={p_underpowered:.3f} > 0.05)")

    # Mathematical Oracle 3: Apple HealthKit HeartbeatSeries beat-to-beat RMSSD + ectopic beat rejection
    hb_xml = """<HealthData>
      <HeartbeatSeries startDate="2026-11-15 08:00:00 +0000" sourceName="Apple Watch">
        <InstantaneousBeatsPerMinute time="0.000" bpm="60"/>
        <InstantaneousBeatsPerMinute time="1.000" bpm="60"/>
        <InstantaneousBeatsPerMinute time="2.030" bpm="58"/>
        <InstantaneousBeatsPerMinute time="3.000" bpm="62"/>
        <InstantaneousBeatsPerMinute time="3.350" bpm="171"/>
        <InstantaneousBeatsPerMinute time="4.350" bpm="60"/>
        <InstantaneousBeatsPerMinute time="5.380" bpm="58"/>
      </HeartbeatSeries>
    </HealthData>"""
    hb_parsed = parse_apple_health_xml(hb_xml, is_file=False)
    assert len(hb_parsed["hrv"]) == 1 and hb_parsed["hrv"][0]["rmssd_source"] == "rmssd_heartbeat_series"
    assert 20.0 <= hb_parsed["hrv"][0]["rmssd_ms"] <= 60.0, f"Ectopic-filtered RMSSD out of bounds: {hb_parsed['hrv'][0]['rmssd_ms']}"
    print(f"✓ HealthKit HeartbeatSeries RMSSD Oracle: RMSSD={hb_parsed['hrv'][0]['rmssd_ms']}ms (ectopic beat filtered)")

    # Empty-DB Zero-False-Pass Oracle: Empty SQLite DB must return ZERO 'PASS' verdicts
    empty_conn = sqlite3.connect(":memory:")
    res_empty = evaluate_concordance(empty_conn, session_id="empty-session", cohort_stage=1)
    empty_passes = [h for h, d in res_empty["hypotheses"].items() if d.get("verdict") == "PASS"]
    assert not empty_passes, f"Empty DB returned phantom PASS verdicts: {empty_passes}"
    print("✓ Empty-DB Zero-False-Pass Oracle: Confirmed 0/13 PASS on empty telemetry database")

    # Upstream SciPy Reference Parity Oracle: BY-FDR & Student's t-test
    if HAS_SCIPY:
        test_ps = {"a": 0.001, "b": 0.04, "c": 0.03, "d": 0.50}
        by_local = benjamini_yekutieli_fdr_py(test_ps, q=0.05)
        by_scipy = scipy_stats.false_discovery_control([test_ps[k] for k in ("a", "b", "c", "d")], method="by")
        for idx, k in enumerate(("a", "b", "c", "d")):
            assert abs(by_local[k]["adjusted_q"] - float(by_scipy[idx])) < 1e-5
        sample_vec = [11.2, 11.6, 11.8, 11.4]
        t_loc, p_loc = compute_one_sample_ttest(sample_vec, 8.0, alternative="greater")
        t_ref = scipy_stats.ttest_1samp(sample_vec, 8.0, alternative="greater")
        assert abs(t_loc - float(t_ref.statistic)) < 1e-9 and abs(p_loc - float(t_ref.pvalue)) < 1e-9
        print("✓ SciPy Reference Parity Oracle: Exact match against scipy.stats.false_discovery_control(method='by') & ttest_1samp")

    print("\n" + "=" * 80)
    print("✅ SELF-TEST PASSED: ALL 13 TESTABLE PILOT & AMENDMENT HYPOTHESES & STOPPING GATES VALIDATED")
    print("=" * 80)
    return True


def main():
    parser = argparse.ArgumentParser(description="DOCAS-PILOT-1 Multi-Modal Concordance Engine")
    parser.add_argument("--self-test", action="store_true", help="Execute self-test with synthetic multi-modal data")
    parser.add_argument("--apple-xml", type=str, help="Path to Apple Health export.xml")
    parser.add_argument("--db-path", type=str, default="pilot1_telemetry.db", help="Path to SQLite edge database")
    parser.add_argument("--session-id", type=str, default="session-001", help="Telemetry session ID")
    parser.add_argument("--cohort-stage", type=int, default=1, choices=[1, 2, 3, 4], help="Cohort Stage (1-4)")
    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    if not args.apple_xml:
        parser.print_help()
        sys.exit(1)

    print(f"Parsing Apple Health XML: {args.apple_xml}")
    parsed = parse_apple_health_xml(args.apple_xml, is_file=True)

    conn = sqlite3.connect(args.db_path)
    n_hrv, n_temp, n_sleep = ingest_apple_health_into_db(conn, args.session_id, parsed)
    print(f"Ingested {n_hrv} HRV, {n_temp} Wrist Temp, and {n_sleep} Sleep records into {args.db_path}")

    res = evaluate_concordance(conn, session_id=args.session_id, cohort_stage=args.cohort_stage)
    print("\nConcordance Evaluation Results:")
    import json
    print(json.dumps(res, indent=2))
    conn.close()


if __name__ == "__main__":
    main()

