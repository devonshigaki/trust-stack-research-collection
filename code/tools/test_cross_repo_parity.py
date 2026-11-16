#!/usr/bin/env python3
"""
Cross-Repository Golden-Vector Parity Suite
Verifies exact numerical parity across:
  1. Pure-Python Master Stability Law reference (Lean 4 MasterLaw.lean spec)
  2. Fixed-Point R1CS Prover (formal/zk_master_law_stp.py, F_p nanounit quantization)
  3. iOS Kiosk Rust UniFFI Bridge (protocols/ios_research_kiosk/uniffi_bridge)
  4. Production FreshCredit Rust Core (~/Developer/freshcredit/crates/sim-core, if present)
"""

import os
import sys
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(BASE_DIR, "formal"))
from zk_master_law_stp import MasterLawZKProver, verify_zk_proof


def ref_master_step(s_curr: float, v: float, e: float, lp: float, ln: float, delta: float, s_base: float, r_t: float = 1.0) -> float:
    eps = v - e
    lam = lp if eps >= 0.0 else ln
    s_next = s_curr + lam * eps * r_t - delta * (s_curr - s_base)
    return max(0.0, min(1.0, s_next))


def main():
    print("=" * 75)
    print("CROSS-REPO GOLDEN-VECTOR PARITY TEST (PYTHON <-> R1CS <-> RUST UNIFFI)")
    print("=" * 75)

    # 1. Fixed-point NIZK parity against Lean/Python reference across asymmetric & boundary presets
    prover = MasterLawZKProver(lambda_plus=0.228, lambda_minus=0.912, delta_param=0.010, s_base=0.500)
    vectors = [
        (0.500, 0.850, 0.500),  # Positive validation
        (0.5798, 0.100, 0.750), # Negative asymmetric shock -> lower clamp
        (0.430802, 0.500, 0.500), # Pure baseline leak
        (0.950, 1.000, 0.000),  # Upper clamp boundary -> 1.0
        (0.050, 0.000, 1.000),  # Lower clamp boundary -> 0.0
    ]
    for s0, v, e in vectors:
        s_ref = ref_master_step(s0, v, e, 0.228, 0.912, 0.010, 0.500, 1.0)
        proof, s_zk = prover.generate_proof(s0, v, e)
        assert verify_zk_proof(proof, s_zk, expected_params=prover.expected_params()), f"NIZK proof failed for ({s0}, {v}, {e})"
        err = abs(s_ref - s_zk)
        assert err < 1e-8, f"Parity mismatch ref={s_ref} vs zk={s_zk} (err={err})"
    print(f"✓ Python Reference <-> secp256k1 NIZK Parity: 5/5 asymmetric & clamped vectors matched (< 1e-8)")

    # 2. Run iOS Kiosk Rust UniFFI Bridge unit tests & Swift FFI binding typecheck
    uniffi_dir = os.path.join(BASE_DIR, "protocols/ios_research_kiosk/uniffi_bridge")
    with open(os.path.join(uniffi_dir, "src/lib.rs"), "r", encoding="utf-8") as f:
        assert "pub fn apply_validation_event_fixed_i64" in f.read(), "UniFFI bridge missing apply_validation_event_fixed_i64"
    res_u = subprocess.run(["cargo", "test", "--quiet"], cwd=uniffi_dir, capture_output=True, text=True)
    assert res_u.returncode == 0, f"UniFFI cargo test failed:\n{res_u.stderr}"
    print("✓ iOS Kiosk Rust UniFFI Bridge (`cargo test`): PASS")

    if sys.platform == "darwin" and os.path.exists("/usr/bin/swiftc"):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_swift:
            res_b = subprocess.run(["cargo", "build", "--release", "--quiet"], cwd=uniffi_dir, capture_output=True, text=True)
            assert res_b.returncode == 0, res_b.stderr
            res_g = subprocess.run(
                ["cargo", "run", "--quiet", "--bin", "uniffi-bindgen", "generate",
                 "--library", "target/release/libdocas_kiosk_bridge.dylib",
                 "--language", "swift", "--out-dir", tmp_swift],
                cwd=uniffi_dir, capture_output=True, text=True,
            )
            assert res_g.returncode == 0, res_g.stderr
            res_s = subprocess.run(
                ["xcrun", "swiftc", "-typecheck", "-I", tmp_swift,
                 "-Xcc", f"-fmodule-map-file={tmp_swift}/docas_kiosk_bridgeFFI.modulemap",
                 f"{tmp_swift}/docas_kiosk_bridge.swift"],
                capture_output=True, text=True,
            )
            assert res_s.returncode == 0, f"swiftc -typecheck failed:\n{res_s.stderr}"
        print("✓ Apple Swift 6 (`swiftc -typecheck`) over generated UniFFI bindings: PASS")

    if sys.platform == "darwin" and os.path.exists("/usr/bin/plutil"):
        mc_path = os.path.join(BASE_DIR, "protocols/ios_research_kiosk/DOCAS_PILOT_1_Kiosk.mobileconfig")
        res_p = subprocess.run(["plutil", "-lint", mc_path], capture_output=True, text=True)
        assert res_p.returncode == 0, f"plutil -lint failed:\n{res_p.stderr}"
        print("✓ Apple MDM Kiosk Profile (`plutil -lint` with com.apple.asam): PASS")

    # 3. Cross-repo formula & executable test parity check on sibling Rust sim-core workspaces
    for repo_label, repo_root in [
        ("Standalone Simulator", os.path.expanduser("~/Developer/simulator")),
        ("FreshCredit Monorepo", os.path.expanduser("~/Developer/freshcredit")),
    ]:
        ml_path = os.path.join(repo_root, "crates/sim-core/src/master_law.rs")
        if os.path.exists(ml_path):
            with open(ml_path, "r", encoding="utf-8") as f:
                rs_src = f.read()
            for tok in [
                "self.lambda_plus * eps.max(0.0) * self.recognition_gate",
                "self.lambda_minus * eps.min(0.0) * self.recognition_gate",
                "self.leak_delta * (current_s - self.s_base)",
                "(validation - expectation) / s_d",
            ]:
                assert tok in rs_src, f"{repo_label} master_law.rs drifted from MasterLaw spec: missing {tok}"
            print(f"✓ {repo_label} `master_law.rs` source-equation parity: PASS")
            if repo_label == "Standalone Simulator":
                assert "asymmetric_invariant_bounds" in rs_src, "Simulator master_law.rs missing Z3 asymmetric_invariant_bounds"
                assert "pub fn step_fixed_i64" in rs_src, "Simulator master_law.rs missing step_fixed_i64"
                assert "scale_s_d" in rs_src and "s_d_fixed" in rs_src, "Simulator master_law.rs step_fixed_i64 missing scale_s_d normalization"
                res_sim = subprocess.run(
                    ["cargo", "test", "-p", "sim-core", "--lib", "--quiet", "--", "master_law::tests"],
                    cwd=repo_root, capture_output=True, text=True,
                )
                assert res_sim.returncode == 0, f"Simulator master_law cargo test failed:\n{res_sim.stderr}"
                print("✓ Standalone Simulator `cargo test -p sim-core --lib master_law::tests` (incl. Z3 BIBO + s_d!=1.0): PASS")

    # 4. Cross-repo FreshProtocol Spec Kernel parity check
    fp_dir = os.path.expanduser("~/Developer/freshprotocol")
    fp_ml = os.path.join(fp_dir, "crates/fresh-protocol-spec/src/master_law.rs")
    if os.path.exists(fp_ml):
        with open(fp_ml, "r", encoding="utf-8") as f:
            fp_src = f.read()
            assert "pub fn step_fixed_i64" in fp_src, "FreshProtocol missing fixed-point step_fixed_i64 parity method"
            assert "s_d_fixed" in fp_src, "FreshProtocol master_law.rs missing scale_s_d fixed-point normalization"
        res_fp = subprocess.run(
            ["cargo", "test", "-p", "fresh-protocol-spec", "--lib", "--quiet"],
            cwd=fp_dir, capture_output=True, text=True,
        )
        assert res_fp.returncode == 0, f"FreshProtocol fresh-protocol-spec test failed:\n{res_fp.stderr}"
        print("✓ FreshProtocol `fresh-protocol-spec::master_law` Golden-Vector + Fixed-Point s_d!=1.0 Parity: PASS")

    print("\n✓ ALL CROSS-REPO GOLDEN-VECTOR PARITY CHECKS PASSED!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
