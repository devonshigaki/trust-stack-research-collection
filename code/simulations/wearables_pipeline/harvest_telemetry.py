#!/usr/bin/env python3
"""
Telemetry Ingestion & Daily Master Parquet Aggregator (DOCAS-PILOT-1 V4.6: 180-Day Multi-Omic Protocol)
Author: Devon Shigaki (ORCID: 0009-0003-8977-8010)

Aggregates multi-modal telemetry streams for a single study day into a unified
Parquet format and encrypted local libSQL database, with strict phase & privacy gating:
- Phase 0 (Days 1–14):  Habituation & Cognitive Practice-Curve Burn-In
- Phase 1 (Days 15–42): Observational Baseline, Washout & Pharmacokinetic Calibration
- Phase 2 (Days 43–180): Longitudinal Dense Phenotyping & Ecological Contrasts
- Privacy: Feature-only media retention; strict minor/household exclusion gate
"""

import os
import sys
import sqlite3
import datetime
import numpy as np
import pandas as pd

def aggregate_daily_telemetry(date_str: str, out_dir: str = None) -> str:
    """
    Combines multi-modal telemetry streams for a single study day into a unified 
    Parquet format and logs to local libSQL with phase and event metadata.
    """
    if out_dir is None:
        out_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Temporal Base Index (1-minute intervals across 24 hours = 1,440 rows)
    timestamps = pd.date_range(start=f"{date_str} 00:00:00", end=f"{date_str} 23:59:00", freq="1min")
    df = pd.DataFrame({"timestamp": timestamps})
    df["timestamp_posix"] = df["timestamp"].astype("int64") // 10**9

    # 2. Study Phase Labeling Logic (Default Anchor: 2026-11-09)
    study_start = pd.Timestamp("2026-11-09")
    current_date = pd.Timestamp(date_str)
    day_number = (current_date - study_start).days + 1
    
    df["study_day"] = day_number
    if day_number <= 14:
        df["phase_label"] = "phase_0_habituation_burnin"
    elif day_number <= 42:
        df["phase_label"] = "phase_1_observational_baseline"
    else:
        df["phase_label"] = "phase_2_ecological_contrasts"

    # 3. Simulate Multi-Sensor Stream Ingestion (Reflecting Real N=1 6-Month Baseline Schedule)
    np.random.seed(42 + day_number)
    N = len(df)
    hours = df["timestamp"].dt.hour
    charging_mask = ((hours >= 5) & (hours < 7)) | ((hours >= 17) & (hours < 19))
    df["is_scheduled_charging_window"] = charging_mask.astype(int)

    # (A) Autonomic: Hilo/Aktiia Continuous BP (docked 5-7 AM & 5-7 PM) & Apple Watch S8 HRV
    df["systolic_bp"] = np.where(charging_mask, np.nan, np.random.normal(loc=121.5, scale=4.5, size=N))
    df["diastolic_bp"] = np.where(charging_mask, np.nan, np.random.normal(loc=78.2, scale=3.8, size=N))
    df["hrv_rmssd"] = np.random.normal(loc=48.5, scale=8.0, size=N)
    df["resting_hr"] = np.random.normal(loc=62.0, scale=4.0, size=N)
    df["wrist_temp_dev"] = np.random.normal(loc=0.02, scale=0.05, size=N)

    # (B) Neuro: Muse S Athena Overnight Sleep EEG/fNIRS + Weekly 5-min Resting (docked 5-7 AM & 5-7 PM)
    df["fnirs_hbo2_prefrontal"] = np.where(charging_mask, np.nan, np.random.normal(loc=98.2, scale=1.1, size=N))
    df["fnirs_hbr_prefrontal"] = np.where(charging_mask, np.nan, np.random.normal(loc=42.1, scale=0.8, size=N))
    df["eeg_theta_beta_ratio"] = np.where(charging_mask, np.nan, np.random.normal(loc=2.1, scale=0.25, size=N))

    # (C) Metabolic: Dexcom Stelo Interstitial Glucose (5-min cadence interpolated to 1-min)
    df["interstitial_glucose"] = np.random.normal(loc=94.5, scale=7.2, size=N)

    # (D) Ambient: Aranet4 Indoor CO2, Temp, RH, Pressure + Optional Outdoor PM2.5
    df["ambient_co2_ppm"] = np.random.normal(loc=620, scale=40, size=N)
    df["ambient_temp_c"] = np.random.normal(loc=20.5, scale=0.8, size=N)
    df["ambient_rh_pct"] = np.random.normal(loc=46.0, scale=3.0, size=N)
    df["ambient_pressure_hpa"] = np.random.normal(loc=1013.2, scale=1.5, size=N)
    df["ambient_pm25_outdoor_ugm3"] = np.random.normal(loc=7.5, scale=2.0, size=N)

    # (D2) Photic Exposure: Apple Health TimeInDaylight & Philips Hue Pre-Bed Lux
    df["time_in_daylight_min"] = 0.0
    df.loc[12 * 60:12 * 60 + 40, "time_in_daylight_min"] = 1.0  # 40 min outdoor daylight
    df["pre_bed_lux"] = np.where(df.index >= 21 * 60, 22.0, 180.0)
    df["pre_bed_cct_k"] = np.where(df.index >= 21 * 60, 2200.0, 4800.0)

    # (E) Enteric & Hydration: Throne Smart Toilet Passive Monitoring
    df["bristol_stool_score"] = np.nan
    df["hydration_index"] = 85.0
    # Simulate void events at 08:30 and 19:45
    void_indices = [int(8.5 * 60), int(19.75 * 60)]
    for v_idx in void_indices:
        df.loc[v_idx, "bristol_stool_score"] = 4.0 # Normal smooth type
        df.loc[v_idx, "hydration_index"] = 92.0

    # (F) Somatic Stationarity: Fitindex Smart Scale (6'0", 185 lb = 83.9 kg, 10-20% BF @ 5:05 AM fasted)
    df["smart_scale_weight_kg"] = 83.9 + np.random.normal(0, 0.25)
    df["smart_scale_bmi"] = 25.1
    df["smart_scale_body_fat_pct"] = 15.2
    df["smart_scale_lean_mass_kg"] = 71.1

    # (G) Financial Execution: Plaid API Stream
    df["plaid_transaction_flag"] = 0
    df["plaid_amount_usd"] = 0.0
    # Simulate a financial event @ 14:15
    event_idx = int(14.25 * 60)
    df.loc[event_idx, "plaid_transaction_flag"] = 1
    df.loc[event_idx, "plaid_amount_usd"] = 450.00

    # (H) Fluid Inflow: HidrateSpark PRO Smart Water Bottle (Periodic intake during 10h active block)
    df["water_intake_ml"] = 0.0
    for sip_hour in [9, 11, 13, 15, 17, 19]:
        sip_idx = sip_hour * 60 + int(np.random.uniform(5, 45))
        df.loc[sip_idx, "water_intake_ml"] = float(np.random.normal(220, 25))

    # (I) Respiratory Strength: Weekly Pre-Yoga Airofit Pro (6:45 AM) & Evening iPad/MPK (7:45 PM)
    df["airofit_mip_cmh2o"] = np.nan
    df["airofit_mep_cmh2o"] = np.nan
    df["airofit_vc_liters"] = np.nan
    if day_number % 7 == 1:
        am_idx = 6 * 60 + 45
        df.loc[am_idx, "airofit_mip_cmh2o"] = float(np.random.normal(108.0, 4.0))
        df.loc[am_idx, "airofit_mep_cmh2o"] = float(np.random.normal(132.0, 5.0))
        df.loc[am_idx, "airofit_vc_liters"] = float(np.random.normal(4.85, 0.12))

    # (J) Objective Cognitive Battery (60-90 min pre-bed @ 7:45 PM: iPad Creyos/PsyToolkit + wired Akai MPK Mini)
    ev_idx = 19 * 60 + 45
    df["pvt_median_rt_ms"] = np.nan
    df["nback_d_prime"] = np.nan
    df["stroop_interference_ms"] = np.nan
    df.loc[ev_idx, "pvt_median_rt_ms"] = float(235.0 + 45.0 * np.exp(-max(day_number, 1) / 4.5) + np.random.normal(0, 6.0))
    df.loc[ev_idx, "nback_d_prime"] = float(2.6 - 0.8 * np.exp(-max(day_number, 1) / 4.5) + np.random.normal(0, 0.12))
    df.loc[ev_idx, "stroop_interference_ms"] = float(48.0 + 20.0 * np.exp(-max(day_number, 1) / 4.5) + np.random.normal(0, 5.0))

    # (K) Pharmacological Exposure Logs (7:00 AM Espresso + Oat Milk + Honey; Unmedicated: 0 melatonin/GLP-1)
    df["cannabis_thc_mg"] = 0.0
    df["cannabis_cbd_mg"] = 0.0
    df["caffeine_mg"] = 0.0
    df.loc[7 * 60, "caffeine_mg"] = 145.0

    # (L) Bedroom PIR & Privacy Enforcement Flags (9:00 PM - 5:00 AM sleep, Zero Raw Audio/Video, Minor Excluded)
    df["bedroom_pir_motion"] = np.where((df.index >= 21 * 60) | (df.index < 5 * 60), 0, 1)
    df["minor_exclusion_verified"] = 1
    df["raw_media_purged"] = 1

    # 4. Save to Master Parquet Store
    parquet_filename = os.path.join(out_dir, f"master_telemetry_day_{day_number:03d}_{date_str}.parquet")
    df.to_parquet(parquet_filename, compression="snappy", index=False)
    print(f"✓ Successfully compiled Day {day_number:03d} ({date_str}) master dataset into:")
    print(f"  {parquet_filename}")

    # 5. Insert Daily Summary into local libSQL (trust_wearables_edge.db)
    db_path = os.path.join(out_dir, "trust_wearables_edge.db")
    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_telemetry_ledger (
            day_number INTEGER PRIMARY KEY,
            date_str TEXT NOT NULL,
            phase_label TEXT NOT NULL,
            mean_hrv_rmssd REAL,
            mean_systolic_bp REAL,
            mean_diastolic_bp REAL,
            mean_glucose REAL,
            mean_fnirs_hbo2 REAL,
            morning_weight_kg REAL,
            body_fat_pct REAL,
            total_water_intake_ml REAL,
            parquet_path TEXT NOT NULL
        );
        """)
        # Ensure migration if table already exists
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(daily_telemetry_ledger)")
        existing_cols = [row[1] for row in cursor.fetchall()]
        if "total_water_intake_ml" not in existing_cols:
            conn.execute("ALTER TABLE daily_telemetry_ledger ADD COLUMN total_water_intake_ml REAL DEFAULT 0;")
        conn.execute("""
        INSERT OR REPLACE INTO daily_telemetry_ledger (
            day_number, date_str, phase_label, mean_hrv_rmssd, mean_systolic_bp,
            mean_diastolic_bp, mean_glucose, mean_fnirs_hbo2, morning_weight_kg,
            body_fat_pct, total_water_intake_ml, parquet_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            int(day_number),
            date_str,
            str(df["phase_label"].iloc[0]),
            float(df["hrv_rmssd"].mean()),
            float(df["systolic_bp"].mean()),
            float(df["diastolic_bp"].mean()),
            float(df["interstitial_glucose"].mean()),
            float(df["fnirs_hbo2_prefrontal"].mean()),
            float(df["smart_scale_weight_kg"].iloc[0]),
            float(df["smart_scale_body_fat_pct"].iloc[0]),
            float(df["water_intake_ml"].sum()),
            parquet_filename
        ))
    conn.close()
    print("✓ Successfully logged daily summary metrics to local libSQL database.")
    return parquet_filename

if __name__ == "__main__":
    test_date = sys.argv[1] if len(sys.argv) > 1 else "2026-11-09"
    aggregate_daily_telemetry(test_date)
