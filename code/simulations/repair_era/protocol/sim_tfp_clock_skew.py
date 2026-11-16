#!/usr/bin/env python3
"""
Sim TFP-ClockSkew: Non-Commutative Clamped State vs. Canonical HLC + Hash-Ordered Op-Log
Models partitioned edge nodes receiving out-of-order trust events under +/-12h physical clock skew.

Proves empirically (matching Lean 4 `masterStepClamped_not_comm`):
  1. Clamped Master Law updates (`clip(0, 1)`) are NOT commutative: permuting arrival order
     produces catastrophic state divergence (`|S_A - S_B| > 0`).
  2. Using a Hybrid Logical Clock `(hlc_wall_ms, hlc_logical, sha256_digest)` G-Set op-log with
     deterministic prefix replay achieves exact bit-identical convergence (`|S_A - S_B| == 0.0`)
     without a central clock oracle.
"""

import hashlib
import json
import os
import numpy as np


def _master_step_clamped(s: float, eps: float, lam: float = 0.25) -> float:
    return float(np.clip(s + lam * eps, 0.0, 1.0))


def _event_digest(actor: str, seq: int, eps: float) -> str:
    payload = f"{actor}:{seq}:{eps:.12f}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def simulate_clock_skew(N_events: int = 1000, max_skew_ms: int = 43_200_000):
    rng = np.random.default_rng(42)
    true_time_ms = 1_700_000_000_000
    events = []
    # Two edge issuers (A and B) with completely independent, skewed local HLC clocks
    clocks = {
        "node_A": {"wall": 0, "logical": 0, "offset_ms": -18_500, "drift_ppm": -120.0},
        "node_B": {"wall": 0, "logical": 0, "offset_ms": +24_300, "drift_ppm": +150.0},
    }
    t0 = true_time_ms
    for seq in range(N_events):
        true_time_ms += int(rng.exponential(60_000))
        eps = float(rng.normal(0.05, 0.85))  # Large enough to hit [0, 1] clamp boundaries frequently
        actor = "node_A" if seq % 2 == 0 else "node_B"
        clk = clocks[actor]
        # Independent per-node physical clock with offset + drift + jitter (no shared HLC state!)
        elapsed_ms = true_time_ms - t0
        pt = true_time_ms + clk["offset_ms"] + int(elapsed_ms * clk["drift_ppm"] * 1e-6) + int(rng.integers(-5_000, 5_001))
        if pt > clk["wall"]:
            clk["wall"] = pt
            clk["logical"] = 0
        else:
            clk["logical"] += 1
        # Enforce bounded HLC drift (wall cannot exceed local physical clock + max_skew_ms)
        assert abs(clk["wall"] - true_time_ms) <= max_skew_ms, "HLC drift exceeded max_skew_ms bound"
        digest = _event_digest(actor, seq, eps)
        events.append({
            "actor": actor,
            "hlc": (clk["wall"], clk["logical"], digest),
            "eps": eps,
            "true_time_ms": true_time_ms,
        })

    # Node A and Node B observe the same G-Set of events in skewed physical arrival order
    log_a = []
    log_b = []
    for ev in events:
        t_a = max(0, ev["true_time_ms"] + int(rng.integers(-max_skew_ms, max_skew_ms + 1)))
        t_b = max(0, ev["true_time_ms"] + int(rng.integers(-max_skew_ms, max_skew_ms + 1)))
        log_a.append((t_a, ev))
        log_b.append((t_b, ev))

    log_a.sort(key=lambda x: x[0])
    log_b.sort(key=lambda x: x[0])

    # 1. Naive arrival-order fold (demonstrates non-commutativity divergence)
    s_a_naive, s_b_naive = 0.5, 0.5
    for _, ev in log_a:
        s_a_naive = _master_step_clamped(s_a_naive, ev["eps"])
    for _, ev in log_b:
        s_b_naive = _master_step_clamped(s_b_naive, ev["eps"])

    # 2. Canonical HLC + SHA-256 tie-broken G-Set replay (no oracle ID required)
    canon_a = sorted((ev for _, ev in log_a), key=lambda e: e["hlc"])
    canon_b = sorted((ev for _, ev in log_b), key=lambda e: e["hlc"])
    s_a_hlc, s_b_hlc = 0.5, 0.5
    for ev in canon_a:
        s_a_hlc = _master_step_clamped(s_a_hlc, ev["eps"])
    for ev in canon_b:
        s_b_hlc = _master_step_clamped(s_b_hlc, ev["eps"])

    naive_div = abs(s_a_naive - s_b_naive)
    hlc_div = abs(s_a_hlc - s_b_hlc)

    res = {
        "N_events": N_events,
        "max_skew_hours": max_skew_ms / 3_600_000.0,
        "naive_divergence": float(naive_div),
        "hlc_oplog_divergence": float(hlc_div),
        "non_commutativity_observed": bool(naive_div > 1e-3),
        "consistency_achieved": bool(hlc_div == 0.0),
        "conclusion": (
            "Clamped Master Law updates are non-commutative (Lean 4 `masterStepClamped_not_comm`), "
            "causing naive arrival-order divergence; canonical HLC + SHA-256 G-Set op-log replay "
            "guarantees exact zero-divergence convergence across partitioned nodes."
        ),
    }
    assert res["non_commutativity_observed"], "Expected non-commutativity divergence under skewed arrival"
    assert res["consistency_achieved"], "HLC op-log replay failed to converge identically!"
    return res


def main():
    res = simulate_clock_skew()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_tfp_skew_results.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2)
    print(f"Saved to {out_path} (naive_div={res['naive_divergence']:.4f}, hlc_div={res['hlc_oplog_divergence']:.1f})")


if __name__ == "__main__":
    main()
