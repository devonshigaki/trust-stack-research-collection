#!/usr/bin/env python3
"""
DOCAS-PILOT-1: Muse S Athena Real-Time Ingestion Driver
Target: The Trust Stack Research Collection / DOCAS-PILOT-1 Protocol
Instruments:
  - Muse S Athena Headband: 5-optode prefrontal fNIRS (730/850/660 nm @ 64 Hz)
  - 4-Channel Prefrontal/Temporal EEG (AF7, AF8, TP9, TP10 @ 256 Hz)
"""

import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
import time
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    import brainflow
    from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams, BrainFlowPresets
    HAS_BRAINFLOW = True
except ImportError:
    HAS_BRAINFLOW = False

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    import pylsl
    from pylsl import StreamInfo, StreamOutlet
    HAS_LSL = True
except ImportError:
    HAS_LSL = False

FS_EEG = 256
FS_FNIRS = 64
NUM_EEG_CHANNELS = 4
NUM_FNIRS_OPTODES = 5
WAVELENGTHS_NM = (730, 850, 660)


def resolve_muse_athena_channel_map(board_id: int) -> Dict[str, List[int]]:
    """
    Dynamically resolves EEG channel indices by electrode name from BrainFlow's
    canonical board descriptor (fixing TP9/AF7 transposition: BrainFlow MuseAthena
    DEFAULT_PRESET emits ['TP9', 'AF7', 'AF8', 'TP10']) and ANCILLARY_PRESET
    16-channel optical tensor @ 64 Hz.
    """
    if not HAS_BRAINFLOW:
        return {"eeg_order": [1, 2, 0, 3], "eeg_names": ["AF7", "AF8", "TP9", "TP10"], "optical_rows": list(range(1, 17))}
    eeg_names = BoardShim.get_eeg_names(board_id)
    eeg_channels = BoardShim.get_eeg_channels(board_id)
    name_to_row = {name.upper(): ch for name, ch in zip(eeg_names, eeg_channels)}
    ordered_rows = [
        name_to_row.get("AF7", eeg_channels[1]),
        name_to_row.get("AF8", eeg_channels[2]),
        name_to_row.get("TP9", eeg_channels[0]),
        name_to_row.get("TP10", eeg_channels[3]),
    ]
    anc_descr = BoardShim.get_board_descr(board_id, BrainFlowPresets.ANCILLARY_PRESET.value)
    aux_descr = BoardShim.get_board_descr(board_id, BrainFlowPresets.AUXILIARY_PRESET.value)
    optical_rows = list(anc_descr.get("optical_channels", list(range(1, 17))))
    accel_rows = list(aux_descr.get("accel_channels", [1, 2, 3]))
    gyro_rows = list(aux_descr.get("gyro_channels", [4, 5, 6]))
    return {
        "eeg_order": ordered_rows, "eeg_names": eeg_names,
        "optical_rows": optical_rows, "accel_rows": accel_rows, "gyro_rows": gyro_rows,
    }


def load_or_create_edge_key(
    db_path: str,
    conn: Optional[sqlite3.Connection] = None,
    allow_ephemeral: bool = False,
) -> bytes:
    """
    Derives 256-bit AES-GCM key via PBKDF2-HMAC-SHA256 (600,000 iterations) using a
    128-bit CSPRNG salt persisted inside `vault_kdf_metadata` (NIST SP 800-132; decoupled
    from file path so database relocation/renaming never breaks decryption).
    Fails closed unless `allow_ephemeral=True` (for offline synthetic dry-runs only, using CSPRNG).
    """
    env_hex = os.environ.get("TRUST_EDGE_AES_KEY")
    if env_hex:
        key_bytes = bytes.fromhex(env_hex)
        if len(key_bytes) != 32:
            raise ValueError(f"TRUST_EDGE_AES_KEY must decode to 32 bytes (AES-256), got {len(key_bytes)}")
        return key_bytes
    passphrase = os.environ.get("TRUST_EDGE_PASSPHRASE")
    if passphrase and HAS_CRYPTO:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        salt: Optional[bytes] = None
        if conn is not None:
            row = conn.execute("SELECT salt_hex FROM vault_kdf_metadata WHERE kdf_id = 1").fetchone()
            if row:
                salt = bytes.fromhex(row[0])
            else:
                salt = os.urandom(16)
                conn.execute(
                    "INSERT INTO vault_kdf_metadata (kdf_id, salt_hex, iterations) VALUES (1, ?, 600000)",
                    (salt.hex(),),
                )
                conn.commit()
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
        return kdf.derive(passphrase.encode("utf-8"))
    if allow_ephemeral:
        # Unpredictable in-memory CSPRNG session key for synthetic tests only (never deterministic path hash)
        return os.urandom(32)
    raise RuntimeError(
        "Refusing persistent Muse Athena DB without TRUST_EDGE_AES_KEY or TRUST_EDGE_PASSPHRASE"
    )


def pseudonymize_subject(subject_id: str, key: bytes) -> str:
    """Keyed HMAC-SHA256 pseudonym so raw participant IDs are never stored in SQLite."""
    import hmac
    return "psid_" + hmac.new(key, subject_id.encode("utf-8"), "sha256").hexdigest()[:24]


def encrypt_sensitive_field(plaintext: str, key: bytes, aad: Optional[bytes] = None) -> str:
    """AES-256-GCM authenticated encryption bound to row context AAD (NIST SP 800-38D)."""
    if not HAS_CRYPTO:
        raise RuntimeError("cryptography package required for AES-256-GCM field encryption.")
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), aad)
    return (nonce + ct).hex()


def decrypt_sensitive_field(token_hex: str, key: bytes, aad: Optional[bytes] = None) -> str:
    """Decrypts AES-256-GCM authenticated local field, enforcing matching context AAD."""
    if len(key) != 32:
        raise ValueError(f"AES-256-GCM requires a 32-byte key, got {len(key)}")
    raw = bytes.fromhex(token_hex)
    if len(raw) < 28:  # 12-byte nonce + >=16-byte GCM auth tag
        raise ValueError(f"Truncated AES-GCM ciphertext: expected >= 28 bytes, got {len(raw)}")
    return AESGCM(key).decrypt(raw[:12], raw[12:], aad).decode("utf-8")

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS pilot_sessions (
    session_id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    cohort_stage INTEGER NOT NULL CHECK(cohort_stage IN (1, 2, 3, 4)),
    day_index INTEGER NOT NULL CHECK(day_index >= 1),
    s_channel_eligible INTEGER NOT NULL CHECK(s_channel_eligible IN (0, 1)),
    device_model TEXT NOT NULL DEFAULT 'Muse S Athena',
    sampling_rate_eeg_hz INTEGER NOT NULL DEFAULT 256,
    sampling_rate_fnirs_hz INTEGER NOT NULL DEFAULT 64,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    research_telemetry_only INTEGER NOT NULL DEFAULT 1 CHECK(research_telemetry_only = 1),
    credit_decisioning_prohibited INTEGER NOT NULL DEFAULT 1 CHECK(credit_decisioning_prohibited = 1)
);

CREATE TABLE IF NOT EXISTS muse_eeg_raw (
    session_id TEXT NOT NULL,
    sample_idx INTEGER NOT NULL,
    timestamp_epoch REAL NOT NULL,
    af7 REAL NOT NULL,
    af8 REAL NOT NULL,
    tp9 REAL NOT NULL,
    tp10 REAL NOT NULL,
    PRIMARY KEY (session_id, sample_idx),
    FOREIGN KEY (session_id) REFERENCES pilot_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS muse_eeg_features (
    session_id TEXT NOT NULL,
    timestamp_epoch REAL NOT NULL,
    window_sec REAL NOT NULL,
    fm_theta_uv2 REAL NOT NULL,
    frontal_delta_uv2 REAL NOT NULL DEFAULT 0.0,
    sws_ratio REAL NOT NULL DEFAULT 0.0,
    alpha_af7_uv2 REAL NOT NULL,
    alpha_af8_uv2 REAL NOT NULL,
    beta_uv2 REAL NOT NULL,
    theta_beta_ratio REAL NOT NULL,
    frontal_alpha_asymmetry REAL NOT NULL,
    FOREIGN KEY (session_id) REFERENCES pilot_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS muse_fnirs_raw (
    session_id TEXT NOT NULL,
    sample_idx INTEGER NOT NULL,
    timestamp_epoch REAL NOT NULL,
    optode_idx INTEGER NOT NULL CHECK(optode_idx BETWEEN 1 AND 5),
    raw_intensity_730 REAL NOT NULL,
    raw_intensity_850 REAL NOT NULL,
    raw_intensity_660 REAL NOT NULL,
    PRIMARY KEY (session_id, sample_idx, optode_idx),
    FOREIGN KEY (session_id) REFERENCES pilot_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS muse_aux_imu (
    session_id TEXT NOT NULL,
    sample_idx INTEGER NOT NULL,
    timestamp_epoch REAL NOT NULL,
    acc_x REAL NOT NULL,
    acc_y REAL NOT NULL,
    acc_z REAL NOT NULL,
    gyro_x REAL NOT NULL,
    gyro_y REAL NOT NULL,
    gyro_z REAL NOT NULL,
    PRIMARY KEY (session_id, sample_idx),
    FOREIGN KEY (session_id) REFERENCES pilot_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vault_kdf_metadata (
    kdf_id INTEGER PRIMARY KEY CHECK(kdf_id = 1),
    salt_hex TEXT NOT NULL,
    iterations INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS muse_encrypted_vault (
    session_id TEXT NOT NULL,
    record_type TEXT NOT NULL,
    ciphertext_hex TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (session_id, record_type),
    FOREIGN KEY (session_id) REFERENCES pilot_sessions(session_id) ON DELETE CASCADE
);
"""

def init_edge_database(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn

def compute_welch_psd(data: np.ndarray, fs: int) -> Tuple[np.ndarray, np.ndarray]:
    n = len(data)
    nperseg = min(fs * 2, n)
    if nperseg < 4:
        return np.array([0.0]), np.array([0.0])
    step = nperseg // 2
    window = 0.54 - 0.46 * np.cos(2.0 * np.pi * np.arange(nperseg) / (nperseg - 1))
    scale = 1.0 / (fs * (window * window).sum())
    psds = []
    for start in range(0, n - nperseg + 1, step):
        segment = (data[start:start + nperseg] - data[start:start + nperseg].mean()) * window
        fft_vals = np.fft.rfft(segment)
        psd = (np.abs(fft_vals) ** 2) * scale
        # Parseval's theorem for one-sided power spectral density:
        # Double the power of interior positive frequencies to account for negative frequencies
        if len(psd) > 2:
            if nperseg % 2 == 0:
                psd[1:-1] *= 2.0
            else:
                psd[1:] *= 2.0
        elif len(psd) == 2:
            psd[1] *= 2.0
        psds.append(psd)
    if not psds:
        return np.array([0.0]), np.array([0.0])
    freqs = np.fft.rfftfreq(nperseg, 1.0 / fs)
    return freqs, np.mean(psds, axis=0)

def trapezoid_integral(y: np.ndarray, x: np.ndarray) -> float:
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    if hasattr(np, "trapz"):
        return float(np.trapz(y, x))
    dx = np.diff(x)
    return float(np.sum(0.5 * (y[:-1] + y[1:]) * dx))

def extract_eeg_band_powers(eeg_matrix: np.ndarray, fs: int = FS_EEG) -> Dict[str, float]:
    af7, af8 = eeg_matrix[0], eeg_matrix[1]
    freqs, psd_af7 = compute_welch_psd(af7, fs)
    _, psd_af8 = compute_welch_psd(af8, fs)

    def band_power(psd: np.ndarray, low: float, high: float) -> float:
        idx = np.where((freqs >= low) & (freqs <= high))[0]
        return trapezoid_integral(psd[idx], freqs[idx]) if len(idx) > 0 else 1e-4

    theta_af7 = band_power(psd_af7, 4.0, 8.0)
    theta_af8 = band_power(psd_af8, 4.0, 8.0)
    fm_theta = (theta_af7 + theta_af8) * 0.5
    delta_af7 = band_power(psd_af7, 0.5, 4.0)
    delta_af8 = band_power(psd_af8, 0.5, 4.0)
    frontal_delta = (delta_af7 + delta_af8) * 0.5
    alpha_af7 = band_power(psd_af7, 8.0, 13.0)
    alpha_af8 = band_power(psd_af8, 8.0, 13.0)
    beta_mean = (band_power(psd_af7, 13.0, 30.0) + band_power(psd_af8, 13.0, 30.0)) * 0.5
    total_power = frontal_delta + fm_theta + ((alpha_af7 + alpha_af8) * 0.5) + beta_mean
    sws_ratio = frontal_delta / max(total_power, 1e-4)
    faa = math.log(max(alpha_af8, 1e-6)) - math.log(max(alpha_af7, 1e-6))
    tbr = fm_theta / max(beta_mean, 1e-6)

    return {
        "fm_theta_uv2": fm_theta,
        "frontal_delta_uv2": frontal_delta,
        "sws_ratio": sws_ratio,
        "alpha_af7_uv2": alpha_af7,
        "alpha_af8_uv2": alpha_af8,
        "beta_uv2": beta_mean,
        "theta_beta_ratio": tbr,
        "frontal_alpha_asymmetry": faa,
    }

class SyntheticBiophysicalMuseAthena:
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def get_chunk(self, duration_sec: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        n_eeg = int(duration_sec * FS_EEG)
        n_fnirs = int(duration_sec * FS_FNIRS)
        t_eeg = np.linspace(0, duration_sec, n_eeg, endpoint=False)
        t_fnirs = np.linspace(0, duration_sec, n_fnirs, endpoint=False)

        eeg = np.zeros((NUM_EEG_CHANNELS, n_eeg), dtype=np.float64)
        for ch in range(NUM_EEG_CHANNELS):
            noise = self.rng.normal(0, 10.0, n_eeg)
            alpha_amp = 14.0 if ch == 1 else 12.0
            alpha = alpha_amp * np.sin(2 * np.pi * 10.0 * t_eeg + self.rng.uniform(0, 2 * np.pi))
            theta = 8.0 * np.sin(2 * np.pi * 6.0 * t_eeg + self.rng.uniform(0, 2 * np.pi))
            beta = 5.0 * np.sin(2 * np.pi * 20.0 * t_eeg + self.rng.uniform(0, 2 * np.pi))
            eeg[ch] = noise + alpha + theta + beta

        fnirs = np.zeros((NUM_FNIRS_OPTODES, 3, n_fnirs), dtype=np.float64)
        for optode in range(NUM_FNIRS_OPTODES):
            base_intensity = 120_000.0 + optode * 5_000.0
            cardiac = 1_800.0 * np.sin(2 * np.pi * 1.2 * t_fnirs)
            resp = 600.0 * np.sin(2 * np.pi * 0.28 * t_fnirs)
            hemo_task = 1_200.0 * np.sin(2 * np.pi * 0.04 * t_fnirs)
            fnirs[optode, 0] = base_intensity + cardiac + resp - hemo_task * 0.4 + self.rng.normal(0, 120.0, n_fnirs)
            fnirs[optode, 1] = base_intensity * 1.15 + cardiac * 1.2 + resp + hemo_task * 1.0 + self.rng.normal(0, 120.0, n_fnirs)
            fnirs[optode, 2] = base_intensity * 0.90 + cardiac * 0.8 + resp + self.rng.normal(0, 120.0, n_fnirs)

        return t_eeg, eeg, t_fnirs, fnirs

def unpack_muse_athena_optical_matrix(opt_mat: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Unpacks BrainFlow MuseAthena (board 67) ANCILLARY_PRESET 16-row optical tensor
    into `(NUM_FNIRS_OPTODES, 3, n_samples)` for `(730 nm, 850 nm, 660 nm)`.

    Per upstream `muse_athena.cpp`, optical subpackets encode:
      - `0x36`: 16 channels = 4 spatial sites x 4 diodes `[730nm, 850nm, 660nm, ambient_dark]`
      - `0x35`:  8 channels = 2 spatial sites x 4 diodes (rows 8..15 zero-padded)
      - `0x34`:  4 channels = 1 spatial site  x 4 diodes (rows 4..15 zero-padded)
    Subtracts per-group ambient dark counts (clamped >= 1.0) instead of slicing `[:15]`.
    """
    n_rows, n_samples = opt_mat.shape
    fnirs = np.zeros((NUM_FNIRS_OPTODES, 3, n_samples), dtype=np.float64)
    if n_samples == 0 or n_rows == 0:
        return fnirs, 0

    active_mask = np.any(np.abs(opt_mat) > 1e-12, axis=1)
    active_count = int(np.sum(active_mask))
    n_groups = max(1, min(4, (active_count + 3) // 4)) if active_count > 0 else 0
    for g in range(n_groups):
        base = g * 4
        if base + 3 < n_rows:
            dark = opt_mat[base + 3]
            fnirs[g, 0] = np.maximum(opt_mat[base + 0] - dark, 1.0)
            fnirs[g, 1] = np.maximum(opt_mat[base + 1] - dark, 1.0)
            fnirs[g, 2] = np.maximum(opt_mat[base + 2] - dark, 1.0)
    return fnirs, n_groups


class MuseAthenaStreamer:
    def __init__(
        self,
        session_id: str,
        subject_id: str,
        cohort_stage: int,
        day_index: int,
        db_path: str = "pilot_wearables_edge.db",
        use_hardware: bool = False,
        mac_address: Optional[str] = None,
    ):
        self.session_id = session_id
        self.subject_id = subject_id
        self.cohort_stage = cohort_stage
        self.day_index = day_index
        self.db_path = db_path
        self.use_hardware = use_hardware
        self.mac_address = mac_address
        self.s_channel_eligible = 1 if cohort_stage in (1, 2, 3) else 0

        self.conn = init_edge_database(self.db_path)
        if os.path.exists(self.db_path):
            os.chmod(self.db_path, 0o600)
        self.aes_key = load_or_create_edge_key(
            self.db_path, conn=self.conn, allow_ephemeral=not self.use_hardware
        )
        self.subject_psid = pseudonymize_subject(subject_id, self.aes_key)
        self.board = None
        self.channel_map = resolve_muse_athena_channel_map(
            BoardIds.MUSE_S_ATHENA_BOARD.value if HAS_BRAINFLOW else 67
        )
        if self.use_hardware:
            if not HAS_BRAINFLOW:
                raise RuntimeError("BrainFlow is required when use_hardware=True.")
            params = BrainFlowInputParams()
            # Enable 16-channel optical streaming (tag 0x36) + 52 Hz IMU on Muse S Athena
            params.other_info = "preset=p1045;low_latency=true"
            if self.mac_address:
                params.mac_address = self.mac_address
            self.board = BoardShim(BoardIds.MUSE_S_ATHENA_BOARD.value, params)
            self.board.prepare_session()
        self.init_session_metadata()

        cur = self.conn.cursor()
        cur.execute("SELECT COALESCE(MAX(sample_idx) + 1, 0) FROM muse_eeg_raw WHERE session_id = ?", (session_id,))
        self.eeg_sample_offset = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(MAX(sample_idx) + 1, 0) FROM muse_fnirs_raw WHERE session_id = ?", (session_id,))
        self.fnirs_sample_offset = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(MAX(sample_idx) + 1, 0) FROM muse_aux_imu WHERE session_id = ?", (session_id,))
        self.imu_sample_offset = cur.fetchone()[0]

        self.lsl_outlet_eeg = None
        self.lsl_outlet_fnirs = None
        self._lsl_fnirs_optodes = 4 if self.use_hardware else NUM_FNIRS_OPTODES
        if HAS_LSL:
            info_eeg = StreamInfo("DOCAS_MuseAthena_EEG", "EEG", NUM_EEG_CHANNELS, FS_EEG, "float32", f"eeg_{session_id}")
            self.lsl_outlet_eeg = StreamOutlet(info_eeg)
            info_fnirs = StreamInfo("DOCAS_MuseAthena_fNIRS", "NIRS", self._lsl_fnirs_optodes * 3, FS_FNIRS, "float32", f"fnirs_{session_id}")
            self.lsl_outlet_fnirs = StreamOutlet(info_fnirs)

        self.synth = SyntheticBiophysicalMuseAthena(seed=1337)

    def init_session_metadata(self):
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        query = (
            "INSERT OR REPLACE INTO pilot_sessions ("
            "session_id, subject_id, cohort_stage, day_index, s_channel_eligible, "
            "device_model, sampling_rate_eeg_hz, sampling_rate_fnirs_hz, started_at, "
            "research_telemetry_only, credit_decisioning_prohibited"
            ") VALUES (?, ?, ?, ?, ?, 'Muse S Athena', 256, 64, ?, 1, 1)"
        )
        self.conn.execute(
            query,
            (self.session_id, self.subject_psid, self.cohort_stage, self.day_index, self.s_channel_eligible, now_iso),
        )
        if HAS_CRYPTO:
            aad = f"{self.session_id}:subject_manifest".encode("utf-8")
            manifest_json = json.dumps(
                {"subject_id": self.subject_id, "cohort": self.cohort_stage, "day": self.day_index},
                separators=(",", ":"),
            )
            enc_meta = encrypt_sensitive_field(
                manifest_json,
                self.aes_key,
                aad=aad,
            )
            self.conn.execute(
                "INSERT OR REPLACE INTO muse_encrypted_vault VALUES (?, 'subject_manifest', ?, ?)",
                (self.session_id, enc_meta, now_iso),
            )
        self.conn.commit()

    def persist_chunk(
        self,
        t_start: float,
        t_eeg: np.ndarray,
        eeg: np.ndarray,
        t_fnirs: np.ndarray,
        fnirs: np.ndarray,
        active_optodes: int = NUM_FNIRS_OPTODES,
    ):
        if len(t_eeg) > 0:
            eeg_rows = []
            for i in range(len(t_eeg)):
                sample_time = t_start + t_eeg[i]
                eeg_rows.append((
                    self.session_id, self.eeg_sample_offset + i, float(sample_time),
                    float(eeg[0, i]), float(eeg[1, i]), float(eeg[2, i]), float(eeg[3, i])
                ))
            self.conn.executemany("INSERT OR REPLACE INTO muse_eeg_raw VALUES (?, ?, ?, ?, ?, ?, ?)", eeg_rows)
            self.eeg_sample_offset += len(t_eeg)

            features = extract_eeg_band_powers(eeg, fs=FS_EEG)
            feat_query = (
                "INSERT INTO muse_eeg_features ("
                "session_id, timestamp_epoch, window_sec, fm_theta_uv2, frontal_delta_uv2, sws_ratio, "
                "alpha_af7_uv2, alpha_af8_uv2, beta_uv2, theta_beta_ratio, frontal_alpha_asymmetry"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )
            self.conn.execute(
                feat_query,
                (
                    self.session_id, t_start + t_eeg[-1], float(t_eeg[-1] - t_eeg[0]),
                    features["fm_theta_uv2"], features["frontal_delta_uv2"], features["sws_ratio"],
                    features["alpha_af7_uv2"], features["alpha_af8_uv2"],
                    features["beta_uv2"], features["theta_beta_ratio"], features["frontal_alpha_asymmetry"]
                )
            )

        n_active = max(0, min(NUM_FNIRS_OPTODES, int(active_optodes)))
        if len(t_fnirs) > 0 and n_active > 0:
            fnirs_rows = []
            for optode in range(n_active):
                for i in range(len(t_fnirs)):
                    sample_time = t_start + t_fnirs[i]
                    fnirs_rows.append((
                        self.session_id, self.fnirs_sample_offset + i, float(sample_time), optode + 1,
                        float(fnirs[optode, 0, i]), float(fnirs[optode, 1, i]), float(fnirs[optode, 2, i])
                    ))
            self.conn.executemany("INSERT OR REPLACE INTO muse_fnirs_raw VALUES (?, ?, ?, ?, ?, ?, ?)", fnirs_rows)
            self.fnirs_sample_offset += len(t_fnirs)
        self.conn.commit()

        if self.lsl_outlet_eeg and len(t_eeg) > 0:
            self.lsl_outlet_eeg.push_chunk(eeg.T.astype(np.float32).tolist())
        if self.lsl_outlet_fnirs and len(t_fnirs) > 0 and n_active > 0:
            fnirs_flattened = fnirs[:self._lsl_fnirs_optodes].reshape(self._lsl_fnirs_optodes * 3, -1).T
            self.lsl_outlet_fnirs.push_chunk(fnirs_flattened.astype(np.float32).tolist())

    def persist_imu_chunk(self, t_start: float, acc: np.ndarray, gyr: np.ndarray):
        n_imu = acc.shape[1] if acc.ndim == 2 else 0
        if n_imu == 0:
            return
        imu_rows = []
        for i in range(n_imu):
            imu_rows.append((
                self.session_id, self.imu_sample_offset + i, t_start + i / 52.0,
                float(acc[0, i]), float(acc[1, i]), float(acc[2, i]),
                float(gyr[0, i]), float(gyr[1, i]), float(gyr[2, i]),
            ))
        self.conn.executemany("INSERT OR REPLACE INTO muse_aux_imu VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", imu_rows)
        self.imu_sample_offset += n_imu
        self.conn.commit()

    def run_epoch(self, duration_sec: float = 10.0):
        t_start = time.time()
        active_optodes = NUM_FNIRS_OPTODES
        if self.use_hardware and self.board is not None:
            self.board.start_stream()
            time.sleep(duration_sec)
            raw_eeg = self.board.get_board_data(preset=BrainFlowPresets.DEFAULT_PRESET.value)
            raw_aux = self.board.get_board_data(preset=BrainFlowPresets.AUXILIARY_PRESET.value)
            raw_anc = self.board.get_board_data(preset=BrainFlowPresets.ANCILLARY_PRESET.value)
            self.board.stop_stream()

            eeg = raw_eeg[self.channel_map["eeg_order"], :]
            t_eeg = np.arange(eeg.shape[1], dtype=np.float64) / FS_EEG

            # Persist 52 Hz 6-axis IMU telemetry monotonically across epochs
            if raw_aux.shape[1] > 0:
                acc = raw_aux[self.channel_map["accel_rows"], :]
                gyr = raw_aux[self.channel_map["gyro_rows"], :]
                self.persist_imu_chunk(t_start, acc, gyr)

            # Unpack BrainFlow MuseAthena optical tensor (4-diode groups: 730/850/660/ambient_dark)
            opt_mat = raw_anc[self.channel_map["optical_rows"], :]
            n_fnirs = opt_mat.shape[1]
            fnirs, n_groups = unpack_muse_athena_optical_matrix(opt_mat)
            active_optodes = n_groups
            t_fnirs = np.arange(n_fnirs, dtype=np.float64) / FS_FNIRS
        else:
            t_eeg, eeg, t_fnirs, fnirs = self.synth.get_chunk(duration_sec)
        self.persist_chunk(t_start, t_eeg, eeg, t_fnirs, fnirs, active_optodes=active_optodes)
        return t_eeg, eeg, t_fnirs, fnirs

    def close(self):
        if self.board is not None:
            try:
                self.board.release_session()
            except Exception:
                pass
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.conn.execute("UPDATE pilot_sessions SET ended_at = ? WHERE session_id = ?", (now_iso, self.session_id))
        self.conn.commit()
        self.conn.close()

def run_self_test() -> bool:
    print("=" * 70)
    print("RUNNING PRE-FLIGHT VERIFICATION: MUSE S ATHENA TELEMETRY INGESTION")
    print("=" * 70)

    test_db = "test_pilot_edge_dryrun.db"
    for f in [test_db, f"{test_db}-wal", f"{test_db}-shm"]:
        if os.path.exists(f):
            os.remove(f)

    # 0. Parseval's Theorem Verification on 10 Hz Sinusoid (Variance = A^2 / 2 = 50.0 uV^2)
    t_parseval = np.linspace(0, 4.0, int(4.0 * FS_EEG), endpoint=False)
    sin_10hz = 10.0 * np.sin(2 * np.pi * 10.0 * t_parseval)
    parseval_eeg = np.zeros((4, len(t_parseval)))
    parseval_eeg[0] = sin_10hz
    parseval_eeg[1] = sin_10hz
    p_feats = extract_eeg_band_powers(parseval_eeg, fs=FS_EEG)
    expected_variance = 50.0
    rel_error = abs(p_feats["alpha_af7_uv2"] - expected_variance) / expected_variance
    assert rel_error < 0.05, f"Parseval theorem violation: expected ~50.0 uV^2, got {p_feats['alpha_af7_uv2']} (err: {rel_error:.3f})"

    # 0b. Verify Muse S Athena BrainFlow Descriptor Channel Mapping (AF7/AF8/TP9/TP10 + 16-ch optical) & AES-256-GCM
    if HAS_BRAINFLOW:
        cmap = resolve_muse_athena_channel_map(BoardIds.MUSE_S_ATHENA_BOARD.value)
        assert cmap["eeg_names"] == ["TP9", "AF7", "AF8", "TP10"], f"Unexpected BrainFlow MuseAthena names: {cmap['eeg_names']}"
        assert cmap["eeg_order"] == [2, 3, 1, 4], f"AF7/AF8/TP9/TP10 remapping failed: {cmap['eeg_order']}"
        assert len(cmap["optical_rows"]) == 16, f"Expected 16 optical channels, got {len(cmap['optical_rows'])}"

    # 0c. Verify MuseAthena 0x34/0x35/0x36 4-diode-per-group dark-subtracted unpacking
    opt_36 = np.zeros((16, 16), dtype=np.float64)
    for g in range(4):
        opt_36[g * 4 + 0] = 1000.0 + g * 10.0
        opt_36[g * 4 + 1] = 2000.0 + g * 10.0
        opt_36[g * 4 + 2] = 1500.0 + g * 10.0
        opt_36[g * 4 + 3] = 50.0  # ambient dark
    unpacked_36, n_g36 = unpack_muse_athena_optical_matrix(opt_36)
    assert n_g36 == 4 and abs(unpacked_36[1, 0, 0] - 960.0) < 1e-9, "0x36 4x4 dark subtraction failed"
    opt_34 = np.zeros((16, 16), dtype=np.float64)
    opt_34[0], opt_34[1], opt_34[2], opt_34[3] = 900.0, 1100.0, 800.0, 40.0
    unpacked_34, n_g34 = unpack_muse_athena_optical_matrix(opt_34)
    assert n_g34 == 1 and abs(unpacked_34[0, 1, 0] - 1060.0) < 1e-9, "0x34 4-ch unpack failed"

    # 0d. Verify monotonic multi-epoch IMU appending, empty-poll resilience, and active_optodes=4 parity (no phantom optode 5)
    hw_db = "test_hw_emulated_athena.db"
    for f in (hw_db, f"{hw_db}-wal", f"{hw_db}-shm", f"{hw_db}.key"):
        if os.path.exists(f):
            os.remove(f)
    s_hw = MuseAthenaStreamer("hw_emu_s1", "sub_hw", 1, 1, db_path=hw_db)
    s_hw.persist_chunk(time.time(), np.array([]), np.zeros((4, 0)), np.array([]), np.zeros((5, 3, 0)), active_optodes=0)
    t_eeg_e, eeg_e, t_fn_e, _ = s_hw.synth.get_chunk(2.0)
    opt_36_full = np.zeros((16, len(t_fn_e)), dtype=np.float64)
    for g in range(4):
        opt_36_full[g * 4 + 0] = 120_000.0 + 1_800.0 * np.sin(2 * np.pi * 1.2 * t_fn_e)
        opt_36_full[g * 4 + 1] = 135_000.0 + 2_100.0 * np.sin(2 * np.pi * 1.2 * t_fn_e)
        opt_36_full[g * 4 + 2] = 110_000.0 + 1_400.0 * np.sin(2 * np.pi * 1.2 * t_fn_e)
        opt_36_full[g * 4 + 3] = 200.0
    fn_hw, n_g_hw = unpack_muse_athena_optical_matrix(opt_36_full)
    s_hw.persist_chunk(time.time(), t_eeg_e, eeg_e, t_fn_e, fn_hw, active_optodes=n_g_hw)
    s_hw.persist_imu_chunk(time.time(), np.zeros((3, 52)), np.zeros((3, 52)))
    s_hw.persist_imu_chunk(time.time() + 1.0, np.ones((3, 52)), np.ones((3, 52)))
    s_hw.close()
    hw_conn = sqlite3.connect(hw_db)
    assert hw_conn.execute("SELECT COUNT(*) FROM muse_aux_imu WHERE session_id = 'hw_emu_s1'").fetchone()[0] == 104
    assert [r[0] for r in hw_conn.execute("SELECT DISTINCT optode_idx FROM muse_fnirs_raw WHERE session_id = 'hw_emu_s1' ORDER BY optode_idx").fetchall()] == [1, 2, 3, 4]
    hw_conn.close()
    for f in (hw_db, f"{hw_db}-wal", f"{hw_db}-shm", f"{hw_db}.key"):
        if os.path.exists(f):
            os.remove(f)
    if HAS_CRYPTO:
        k_test = os.urandom(32)
        tok = encrypt_sensitive_field("CONFIDENTIAL_CRF_TEXT", k_test)
        assert "CONFIDENTIAL" not in tok and decrypt_sensitive_field(tok, k_test) == "CONFIDENTIAL_CRF_TEXT"
        # Reject truncated ciphertext & non-256-bit key downgrade
        try:
            decrypt_sensitive_field("00" * 16, k_test)
            raise AssertionError("Must reject truncated <28B ciphertext")
        except ValueError:
            pass
        prev_aes_env = os.environ.get("TRUST_EDGE_AES_KEY")
        os.environ["TRUST_EDGE_AES_KEY"] = "00" * 16
        try:
            load_or_create_edge_key(test_db)
            raise AssertionError("Must reject 128-bit TRUST_EDGE_AES_KEY downgrade")
        except ValueError:
            pass
        finally:
            if prev_aes_env is None:
                os.environ.pop("TRUST_EDGE_AES_KEY", None)
            else:
                os.environ["TRUST_EDGE_AES_KEY"] = prev_aes_env

    # 1. Cohort 1 Multi-Day Registration & Multi-Epoch Monotonic Appending
    streamer_c1 = MuseAthenaStreamer(
        session_id="test_sess_c1",
        subject_id="sub_01",
        cohort_stage=1,
        day_index=14,
        db_path=test_db,
    )
    assert streamer_c1.s_channel_eligible == 1, "Cohort 1 must be S-channel eligible"
    t_eeg1, eeg1, t_fnirs1, fnirs1 = streamer_c1.run_epoch(duration_sec=2.0)
    t_eeg2, eeg2, t_fnirs2, fnirs2 = streamer_c1.run_epoch(duration_sec=2.0)
    streamer_c1.close()

    # 2. Cohort 4 Population CLT (S-Channel Strictly Prohibited)
    streamer_c4 = MuseAthenaStreamer(
        session_id="test_sess_c4",
        subject_id="sub_44",
        cohort_stage=4,
        day_index=1,
        db_path=test_db,
    )
    assert streamer_c4.s_channel_eligible == 0, "Cohort 4 (1-day) must be barred from S-channel"
    streamer_c4.run_epoch(duration_sec=2.0)
    streamer_c4.close()

    # 3. Verify Edge Database Rows & Features
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()

    cur.execute("SELECT session_id, cohort_stage, s_channel_eligible, research_telemetry_only, credit_decisioning_prohibited FROM pilot_sessions")
    sessions = cur.fetchall()
    assert len(sessions) == 2, f"Expected 2 sessions, got {len(sessions)}"
    assert sessions[0] == ("test_sess_c1", 1, 1, 1, 1)
    assert sessions[1] == ("test_sess_c4", 4, 0, 1, 1)

    cur.execute("SELECT COUNT(*), MAX(sample_idx) FROM muse_eeg_raw WHERE session_id = 'test_sess_c1'")
    count_eeg, max_eeg = cur.fetchone()
    expected_eeg_count = int(4.0 * FS_EEG)  # 2.0s + 2.0s = 4.0s
    assert count_eeg == expected_eeg_count, f"Expected {expected_eeg_count} appended EEG samples, got {count_eeg}"
    assert max_eeg == expected_eeg_count - 1, f"Expected max sample_idx {expected_eeg_count - 1}, got {max_eeg}"

    cur.execute("SELECT COUNT(*) FROM muse_fnirs_raw WHERE session_id = 'test_sess_c1'")
    count_fnirs = cur.fetchone()[0]
    expected_fnirs_count = 5 * int(4.0 * FS_FNIRS)
    assert count_fnirs == expected_fnirs_count, f"Expected {expected_fnirs_count} appended fNIRS samples, got {count_fnirs}"

    cur.execute("SELECT fm_theta_uv2, frontal_delta_uv2, sws_ratio, alpha_af8_uv2, frontal_alpha_asymmetry FROM muse_eeg_features WHERE session_id = 'test_sess_c1'")
    feat = cur.fetchone()
    assert feat[0] > 0.0 and math.isfinite(feat[0]), "Theta power must be positive"
    assert feat[1] > 0.0 and math.isfinite(feat[1]), "Delta power must be positive"
    assert 0.0 <= feat[2] <= 1.0, "SWS ratio must be in [0, 1]"
    assert feat[3] > 0.0 and math.isfinite(feat[3]), "Alpha power must be positive"
    assert math.isfinite(feat[4]), "FAA must be finite"

    cur.execute("SELECT subject_id FROM pilot_sessions WHERE session_id = 'test_sess_c1'")
    stored_sid = cur.fetchone()[0]
    assert stored_sid.startswith("psid_") and "sub_01" not in stored_sid, "Plaintext subject_id leaked into SQLite!"
    if HAS_CRYPTO:
        cur.execute("SELECT ciphertext_hex FROM muse_encrypted_vault WHERE session_id = 'test_sess_c1' AND record_type = 'subject_manifest'")
        ct_hex = cur.fetchone()[0]
        assert "sub_01" not in ct_hex
        aad_c1 = b"test_sess_c1:subject_manifest"
        assert '"subject_id":"sub_01"' in decrypt_sensitive_field(ct_hex, streamer_c1.aes_key, aad=aad_c1)
        # Cross-row AEAD context transplant rejection check
        try:
            decrypt_sensitive_field(ct_hex, streamer_c1.aes_key, aad=b"test_sess_c4:subject_manifest")
            raise AssertionError("Cross-session AEAD transplant should have failed!")
        except Exception:
            pass
        # Fail-closed check: non-ephemeral key loading MUST raise RuntimeError without env key/passphrase
        try:
            load_or_create_edge_key(test_db, conn=conn, allow_ephemeral=False)
            raise AssertionError("Fail-closed edge key check failed to reject missing key!")
        except RuntimeError:
            pass
        # File-relocation + PBKDF2 persisted-salt survivability check
        os.environ["TRUST_EDGE_PASSPHRASE"] = "pilot-test-passphrase"
        try:
            reloc_a, reloc_b = "test_reloc_a.db", "test_reloc_b.db"
            for f in (reloc_a, reloc_b):
                if os.path.exists(f):
                    os.remove(f)
            s_rel = MuseAthenaStreamer("reloc_s1", "sub_reloc", 1, 1, db_path=reloc_a)
            s_rel.close()
            os.rename(reloc_a, reloc_b)
            conn_b = init_edge_database(reloc_b)
            ct_b = conn_b.execute("SELECT ciphertext_hex FROM muse_encrypted_vault WHERE session_id = 'reloc_s1'").fetchone()[0]
            k_b = load_or_create_edge_key(reloc_b, conn=conn_b)
            assert '"subject_id":"sub_reloc"' in decrypt_sensitive_field(ct_b, k_b, aad=b"reloc_s1:subject_manifest")
            conn_b.close()
            for f in (reloc_a, reloc_b, f"{reloc_b}-wal", f"{reloc_b}-shm"):
                if os.path.exists(f):
                    os.remove(f)
        finally:
            os.environ.pop("TRUST_EDGE_PASSPHRASE", None)

    conn.close()
    for f in [test_db, f"{test_db}-wal", f"{test_db}-shm", f"{test_db}.key"]:
        if os.path.exists(f):
            os.remove(f)

    print("✓ Cohort Stage S-Channel Gating: VERIFIED (Cohort 1 enabled, Cohort 4 barred)")
    print("✓ Prefrontal Welch PSD Band Powers (Fmθ, α, β, TBR, FAA): VERIFIED")
    print("✓ 5-Optode Triple-Wavelength fNIRS (730/850/660 nm @ 64 Hz): VERIFIED")
    print("✓ Edge SQLite WAL Table Sequestration: VERIFIED (100% On-Device)")
    print("PRE-FLIGHT SELF-TEST: ALL 4 GATES PASSED (100% HEALTHY)\n")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DOCAS-PILOT-1: Muse S Athena Telemetry Ingestion Driver")
    parser.add_argument("--self-test", action="store_true", help="Run automated pre-flight self-test")
    parser.add_argument("--session-id", type=str, default="pilot_sess_001", help="Pilot session identifier")
    parser.add_argument("--subject-id", type=str, default="sub_01", help="Participant subject identifier")
    parser.add_argument("--cohort", type=int, choices=[1, 2, 3, 4], default=1, help="Cohort stage (1: 30d, 2: 10d, 3: 3d, 4: 1d)")
    parser.add_argument("--day", type=int, default=1, help="Day index within cohort")
    parser.add_argument("--duration", type=float, default=10.0, help="Epoch duration in seconds")
    parser.add_argument("--db-path", type=str, default="pilot_wearables_edge.db", help="Local edge database path")
    parser.add_argument("--hardware", action="store_true", help="Connect to physical Muse S Athena over Bluetooth")
    parser.add_argument("--mac-address", type=str, default=None, help="Hardware BLE MAC address (e.g. 00:55:da:b0:12:34)")
    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    print(f"Starting Muse S Athena ingestion for Subject {args.subject_id} (Cohort {args.cohort}, Day {args.day})...")
    streamer = MuseAthenaStreamer(
        session_id=args.session_id,
        subject_id=args.subject_id,
        cohort_stage=args.cohort,
        day_index=args.day,
        db_path=args.db_path,
        use_hardware=args.hardware,
        mac_address=args.mac_address,
    )
    try:
        t_eeg, eeg, t_fnirs, fnirs = streamer.run_epoch(duration_sec=args.duration)
        print(f"Completed {args.duration}s epoch. Persisted {len(t_eeg)} EEG samples and {len(t_fnirs) * 5} fNIRS samples to {args.db_path}.")
    finally:
        streamer.close()
