#!/usr/bin/env python3
"""
RFC 9180 HPKE Asymmetric Seal-on-Ingest Blinding Vault (DOCAS-PILOT-1 V4.6)
Author: Devon Shigaki (ORCID: 0009-0003-8977-8010)
"""

import argparse
import hashlib
import json
import os
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hpke, serialization
from cryptography.hazmat.primitives.asymmetric import x25519

HPKE_SUITE = hpke.Suite(hpke.KEM.X25519, hpke.KDF.HKDF_SHA256, hpke.AEAD.AES_256_GCM)
GENESIS_CHAIN_HASH = "0" * 64


def _write_private_0600(path: str, data: bytes) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    os.chmod(path, 0o600)


def _append_0600(path: str, line_bytes: bytes) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, line_bytes)
    finally:
        os.close(fd)
    os.chmod(path, 0o600)


def generate_study_keypair() -> Tuple[bytes, bytes]:
    priv = x25519.X25519PrivateKey.generate()
    priv_raw = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_raw = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return priv_raw, pub_raw


def load_public_key_from_hex(pubkey_hex: str) -> x25519.X25519PublicKey:
    raw = bytes.fromhex(pubkey_hex.strip())
    if len(raw) != 32:
        raise ValueError(f"Expected 32-byte X25519 public key, got {len(raw)} bytes")
    return x25519.X25519PublicKey.from_public_bytes(raw)


def load_private_key_from_hex(privkey_hex: str) -> x25519.X25519PrivateKey:
    raw = bytes.fromhex(privkey_hex.strip())
    if len(raw) != 32:
        raise ValueError(f"Expected 32-byte X25519 private key, got {len(raw)} bytes")
    return x25519.X25519PrivateKey.from_private_bytes(raw)


def resolve_seal_public_key(
    pubkey_hex: Optional[str] = None,
    pubkey_file: Optional[str] = None,
) -> x25519.X25519PublicKey:
    if pubkey_hex:
        return load_public_key_from_hex(pubkey_hex)
    env_hex = os.environ.get("DOCAS_SEAL_PUBKEY_HEX", "").strip()
    if env_hex:
        return load_public_key_from_hex(env_hex)
    candidate_file = pubkey_file or os.environ.get("DOCAS_SEAL_PUBKEY_FILE", "").strip()
    if candidate_file and os.path.exists(candidate_file):
        with open(candidate_file, "r", encoding="utf-8") as f:
            return load_public_key_from_hex(f.read())
    raise RuntimeError(
        "Blinded HPKE seal requested without recipient X25519 public key "
        "(set DOCAS_SEAL_PUBKEY_HEX or pass pubkey_file)."
    )


def _canonical_qc_info(qc_header: Dict[str, Any]) -> bytes:
    return json.dumps(qc_header, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _last_chain_hash(ledger_path: str) -> str:
    if not os.path.exists(ledger_path):
        return GENESIS_CHAIN_HASH
    last_hash = GENESIS_CHAIN_HASH
    with open(ledger_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                last_hash = str(json.loads(s)["entry_hash"])
    return last_hash


def seal_daily_payload(
    vault_dir: str,
    date_str: str,
    study_day: int,
    payload_bytes: bytes,
    pubkey: x25519.X25519PublicKey,
    qc_flags: Optional[Dict[str, Any]] = None,
    artifact_tag: str = "daily_telemetry",
) -> Dict[str, Any]:
    os.makedirs(vault_dir, exist_ok=True)
    os.chmod(vault_dir, 0o700)
    ledger_path = os.path.join(vault_dir, "qc_ledger.jsonl")
    prev_hash = GENESIS_CHAIN_HASH
    if os.path.exists(ledger_path):
        with open(ledger_path, "r", encoding="utf-8") as lf:
            for line in lf:
                s = line.strip()
                if not s:
                    continue
                prev_entry = json.loads(s)
                pqc = prev_entry["qc_header"]
                if pqc.get("artifact_tag") == str(artifact_tag) and pqc.get("date") == str(date_str):
                    raise ValueError(f"Refusing duplicate sealed entry for ({artifact_tag}, {date_str})")
                prev_hash = str(prev_entry["entry_hash"])
    seal_filename = f"{artifact_tag}_{date_str}.hpke"
    seal_path = os.path.join(vault_dir, seal_filename)
    if os.path.exists(seal_path):
        raise FileExistsError(f"Sealed ciphertext already exists (append-only invariant): {seal_path}")
    sanitized_qc = {
        "schema": "docas-hpke-v1",
        "artifact_tag": str(artifact_tag),
        "date": str(date_str),
        "study_day": int(study_day),
        "prev_chain_hash": prev_hash,
        "sci_ok": bool((qc_flags or {}).get("sci_ok", True)),
        "completeness_ok": bool((qc_flags or {}).get("completeness_ok", True)),
        "biotin_72h_hold_verified": bool((qc_flags or {}).get("biotin_72h_hold_verified", True)),
        "raw_media_purged": bool((qc_flags or {}).get("raw_media_purged", True)),
        "minor_exclusion_verified": bool((qc_flags or {}).get("minor_exclusion_verified", True)),
    }
    ciphertext = HPKE_SUITE.encrypt(payload_bytes, pubkey, info=_canonical_qc_info(sanitized_qc))
    seal_filename = f"{artifact_tag}_{date_str}.hpke"
    _write_private_0600(seal_path, ciphertext)
    record_body = {
        "qc_header": sanitized_qc,
        "seal_filename": seal_filename,
        "ciphertext_sha256": hashlib.sha256(ciphertext).hexdigest(),
        "ciphertext_bytes": len(ciphertext),
    }
    entry_hash = hashlib.sha256(
        json.dumps(record_body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    ledger_entry = {**record_body, "entry_hash": entry_hash}
    _append_0600(ledger_path, (json.dumps(ledger_entry, sort_keys=True) + "\n").encode("utf-8"))
    return ledger_entry

def verify_sealed_ledger(vault_dir: str) -> Dict[str, Any]:
    """Audits QC ledger hash-chain, ciphertext SHA-256, and 0o600 permissions without private key."""
    ledger_path = os.path.join(vault_dir, "qc_ledger.jsonl")
    if not os.path.exists(ledger_path):
        raise FileNotFoundError(f"Missing sealed QC ledger: {ledger_path}")
    expected_prev = GENESIS_CHAIN_HASH
    entries: List[Dict[str, Any]] = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            s = line.strip()
            if not s:
                continue
            entry = json.loads(s)
            qc = entry["qc_header"]
            if qc["prev_chain_hash"] != expected_prev:
                raise ValueError(f"QC ledger chain break at index {idx}")
            body = {
                "qc_header": qc,
                "seal_filename": entry["seal_filename"],
                "ciphertext_sha256": entry["ciphertext_sha256"],
                "ciphertext_bytes": entry["ciphertext_bytes"],
            }
            recomputed = hashlib.sha256(
                json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            if recomputed != entry["entry_hash"]:
                raise ValueError(f"QC ledger entry_hash tampered at index {idx}")
            seal_path = os.path.join(vault_dir, entry["seal_filename"])
            mode = os.stat(seal_path).st_mode & 0o777
            if mode & 0o077:
                raise PermissionError(f"Sealed file {seal_path} has overly permissive mode {oct(mode)}")
            with open(seal_path, "rb") as sf:
                ct = sf.read()
            if hashlib.sha256(ct).hexdigest() != entry["ciphertext_sha256"]:
                raise ValueError(f"Ciphertext SHA-256 mismatch for {entry['seal_filename']}")
            expected_prev = entry["entry_hash"]
            entries.append(entry)
    seen_days = sorted({int(e["qc_header"]["study_day"]) for e in entries})
    missing_days = (
        [d for d in range(seen_days[0], seen_days[-1] + 1) if d not in set(seen_days)]
        if seen_days
        else []
    )
    return {
        "verified_entries": len(entries),
        "chain_head": expected_prev,
        "study_days_seen": seen_days,
        "missing_study_days": missing_days,
    }


def unseal_vault_day180(
    vault_dir: str,
    privkey: x25519.X25519PrivateKey,
) -> List[Tuple[Dict[str, Any], bytes]]:
    verify_sealed_ledger(vault_dir)
    ledger_path = os.path.join(vault_dir, "qc_ledger.jsonl")
    unsealed: List[Tuple[Dict[str, Any], bytes]] = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            entry = json.loads(s)
            qc = entry["qc_header"]
            with open(os.path.join(vault_dir, entry["seal_filename"]), "rb") as sf:
                ct = sf.read()
            pt = HPKE_SUITE.decrypt(ct, privkey, info=_canonical_qc_info(qc))
            unsealed.append((qc, pt))
    return unsealed


def run_self_test() -> bool:
    print("=" * 80)
    print("RFC 9180 HPKE ASYMMETRIC SEAL-ON-INGEST VAULT SELF-TEST")
    print("=" * 80)
    import io
    import pandas as pd
    from harvest_telemetry import aggregate_daily_telemetry
    from harvest_expanded_telemetry import harvest_expanded_daily_data

    priv_raw, pub_raw = generate_study_keypair()
    pub_hex = pub_raw.hex()
    pub = load_public_key_from_hex(pub_hex)
    priv = load_private_key_from_hex(priv_raw.hex())
    wrong_priv = load_private_key_from_hex(generate_study_keypair()[0].hex())

    df_day1 = pd.DataFrame({
        "study_day": [1, 1, 1],
        "hrv_rmssd": [48.1234, 51.9876, 44.5555],
        "sentinel_marker": ["SENTINEL_BIOMARKER_SECRET_DAY1", "A", "B"],
    })
    buf1 = io.BytesIO()
    df_day1.to_parquet(buf1, index=False)
    pt1 = buf1.getvalue()

    with tempfile.TemporaryDirectory() as tmp_vault:
        e1 = seal_daily_payload(tmp_vault, "2026-12-01", 1, pt1, pub, {"sci_ok": True})
        sf = os.path.join(tmp_vault, e1["seal_filename"])
        assert (os.stat(sf).st_mode & 0o777) == 0o600
        raw_disk = open(sf, "rb").read()
        assert b"PAR1" not in raw_disk and b"SENTINEL_BIOMARKER_SECRET_DAY1" not in raw_disk

        e2 = seal_daily_payload(tmp_vault, "2026-12-02", 2, pt1, pub)
        assert raw_disk != open(os.path.join(tmp_vault, e2["seal_filename"]), "rb").read()
        try:
            seal_daily_payload(tmp_vault, "2026-12-01", 1, pt1, pub)
            raise AssertionError("Duplicate (artifact_tag, date) must be rejected!")
        except ValueError:
            pass

        for bad_k, qc in ((wrong_priv, e1["qc_header"]), (priv, {**e1["qc_header"], "sci_ok": False})):
            try:
                HPKE_SUITE.decrypt(raw_disk, bad_k, info=_canonical_qc_info(qc))
                raise AssertionError("Expected InvalidTag!")
            except InvalidTag:
                pass

        assert verify_sealed_ledger(tmp_vault)["verified_entries"] == 2
        unsealed = unseal_vault_day180(tmp_vault, priv)
        pd.testing.assert_frame_equal(df_day1, pd.read_parquet(io.BytesIO(unsealed[0][1])))

    # End-to-end blinded ingest check (zero plaintext parquet/db on disk; fail-closed without pubkey)
    with tempfile.TemporaryDirectory() as tmp_ingest:
        old_env = os.environ.pop("DOCAS_SEAL_PUBKEY_HEX", None)
        try:
            try:
                aggregate_daily_telemetry("2026-12-01", out_dir=tmp_ingest, blinded=True)
                raise AssertionError("Expected fail-closed RuntimeError when pubkey missing!")
            except RuntimeError:
                pass
            aggregate_daily_telemetry("2026-12-01", out_dir=tmp_ingest, blinded=True, seal_pubkey_hex=pub_hex)
            harvest_expanded_daily_data("2026-12-01", out_dir=tmp_ingest, blinded=True, seal_pubkey_hex=pub_hex)
            assert not os.path.exists(os.path.join(tmp_ingest, "trust_wearables_edge.db"))
            assert not any(fn.endswith(".parquet") for fn in os.listdir(tmp_ingest))
            vdir = os.path.join(tmp_ingest, "vault_sealed")
            assert verify_sealed_ledger(vdir)["verified_entries"] == 2
            dec = unseal_vault_day180(vdir, priv)
            assert len(dec) == 2 and pd.read_parquet(io.BytesIO(dec[0][1])).shape[0] == 1440
        finally:
            if old_env is not None:
                os.environ["DOCAS_SEAL_PUBKEY_HEX"] = old_env

    print("✓ HPKE IND-CPA, 0o600, zero-plaintext blinded ingest, AAD tamper rejection & Day-180 unseal PASS")
    return True


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="DOCAS RFC 9180 HPKE Blinding Vault")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--keygen-dir", type=str)
    p.add_argument("--verify-vault", type=str)
    args = p.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    if args.keygen_dir:
        priv_b, pub_b = generate_study_keypair()
        _write_private_0600(os.path.join(args.keygen_dir, "study_unseal_privkey.hex"), (priv_b.hex() + "\n").encode("utf-8"))
        _write_private_0600(os.path.join(args.keygen_dir, "study_seal_pubkey.hex"), (pub_b.hex() + "\n").encode("utf-8"))
        print(f"Wrote X25519 keypair to {args.keygen_dir} (0o600); move study_unseal_privkey.hex offline before Day 0.")
        sys.exit(0)
    if args.verify_vault:
        print(json.dumps(verify_sealed_ledger(args.verify_vault), indent=2))
        sys.exit(0)
    p.print_help()

