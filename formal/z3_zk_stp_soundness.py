#!/usr/bin/env python3
"""
Z3 Formal Verifier-Soundness & Real-vs-Fixed-Point Refinement Proofs for ZK-STP v8
1. Verifier Soundness (Z3-ZK-1): Proves that every witness satisfying verify_zk_proof's
   algebraic equations + 33-bit non-negativity constraints strictly satisfies
   s_next == clamp(s_unclamped, 0, SCALE), and demonstrates that omitting the
   s_next / s_next_rem range constraint permits a SAT Branch-0 overflow exploit.
2. Quantization Refinement (Z3-ZK-2): Proves that single-step truncation error between
   MasterLaw.lean (R) and ZK-STP (SCALE = 10^9 integer floor division) is strictly < 2/SCALE,
   and cumulative drift under leak delta_S in (0, 1] is bounded by 2 / (SCALE * delta_S).
"""

import sys
import z3


def prove_verifier_soundness():
    print("=" * 72)
    print(" Z3-ZK-1: ZK-STP Verifier Soundness (Clamp Branch 0 Overflow Guard)")
    print("=" * 72)
    SCALE = 1_000_000_000
    Q_OFFSET = 2 * SCALE
    MAX_33 = (1 << 33) - 1

    def make_vars():
        s_c, s_next, v, e = z3.Ints("s_c s_next v e")
        eps_p, eps_n = z3.Ints("eps_p eps_n")
        q_d_off, r_d, q_l_off, r_l = z3.Ints("q_d_off r_d q_l_off r_l")
        u_low, u_high = z3.Ints("u_low u_high")
        s_c_rem, s_next_rem, v_rem, e_rem, r_d_rem, r_l_rem = z3.Ints(
            "s_c_rem s_next_rem v_rem e_rem r_d_rem r_l_rem"
        )
        lp, ln, delta, s_base = z3.Ints("lp ln delta s_base")
        return {
            "s_c": s_c, "s_next": s_next, "v": v, "e": e,
            "eps_p": eps_p, "eps_n": eps_n,
            "q_d_off": q_d_off, "r_d": r_d, "q_l_off": q_l_off, "r_l": r_l,
            "u_low": u_low, "u_high": u_high,
            "s_c_rem": s_c_rem, "s_next_rem": s_next_rem,
            "v_rem": v_rem, "e_rem": e_rem, "r_d_rem": r_d_rem, "r_l_rem": r_l_rem,
            "lp": lp, "ln": ln, "delta": delta, "s_base": s_base,
        }

    def base_constraints(V, include_s_next_range: bool):
        q_d = V["q_d_off"] - Q_OFFSET
        q_l = V["q_l_off"] - Q_OFFSET
        s_unclamped = V["s_c"] + q_d - q_l
        cs = [
            V["lp"] >= 0, V["lp"] <= SCALE,
            V["ln"] >= 0, V["ln"] <= SCALE,
            V["delta"] >= 0, V["delta"] <= SCALE,
            V["s_base"] >= 0, V["s_base"] <= SCALE,
            V["v"] - V["e"] == V["eps_p"] - V["eps_n"],
            z3.Or(V["eps_p"] == 0, V["eps_n"] == 0),
            SCALE * q_d + V["r_d"] == V["lp"] * V["eps_p"] - V["ln"] * V["eps_n"],
            SCALE * q_l + V["r_l"] == V["delta"] * (V["s_c"] - V["s_base"]),
            z3.Or(
                V["s_next"] == s_unclamped,
                z3.And(V["s_next"] == 0, s_unclamped + V["u_low"] == 0),
                z3.And(V["s_next"] == SCALE, s_unclamped - V["u_high"] == SCALE),
            ),
            V["s_c"] + V["s_c_rem"] == SCALE,
            V["v"] + V["v_rem"] == SCALE,
            V["e"] + V["e_rem"] == SCALE,
            V["r_d"] + V["r_d_rem"] == SCALE - 1,
            V["r_l"] + V["r_l_rem"] == SCALE - 1,
        ]
        rng_keys = [
            "s_c", "s_c_rem", "v", "v_rem", "e", "e_rem",
            "eps_p", "eps_n", "q_d_off", "q_l_off",
            "r_d", "r_d_rem", "r_l", "r_l_rem", "u_low", "u_high",
        ]
        if include_s_next_range:
            cs.append(V["s_next"] + V["s_next_rem"] == SCALE)
            rng_keys.extend(["s_next", "s_next_rem"])
        for k in rng_keys:
            cs.append(V[k] >= 0)
            cs.append(V[k] <= MAX_33)
        return cs, s_unclamped

    V_bug = make_vars()
    cs_bug, _ = base_constraints(V_bug, include_s_next_range=False)
    s_bug = z3.Solver()
    s_bug.add(*cs_bug, V_bug["s_next"] > SCALE)
    assert s_bug.check() == z3.sat, "Expected SAT Branch-0 overflow exploit when s_next range is omitted!"
    m = s_bug.model()
    print(f"[NECESSITY CONFIRMED - SAT] Unpatched verifier accepts Branch 0 overflow: s_next={m[V_bug['s_next']]}")

    V_fix = make_vars()
    cs_fix, s_unclamped_fix = base_constraints(V_fix, include_s_next_range=True)
    exact_clamped = z3.If(
        s_unclamped_fix < 0,
        0,
        z3.If(s_unclamped_fix > SCALE, SCALE, s_unclamped_fix),
    )
    s_sat = z3.Solver()
    s_sat.add(*cs_fix)
    assert s_sat.check() == z3.sat, "Premises must be satisfiable (non-vacuous)!"

    s_sound = z3.Solver()
    s_sound.add(*cs_fix)
    s_sound.add(z3.Or(V_fix["s_next"] != exact_clamped, V_fix["s_next"] < 0, V_fix["s_next"] > SCALE))
    res = s_sound.check()
    print(f"[VERIFIED - NON-VACUOUS {str(res).upper()}] Patched ZK-STP verifier enforces s_next == clamp(s_unclamped, 0, SCALE).")
    assert res == z3.unsat, f"Verifier soundness counterexample: {s_sound.model()}"

def prove_quantization_refinement():
    print("\n" + "=" * 72)
    print(" Z3-ZK-2: Real (MasterLaw.lean) vs Fixed-Point (ZK-STP) Refinement")
    print("=" * 72)
    SCALE = 1_000_000_000
    S_real, V_real, E_real = z3.Reals("S_real V_real E_real")
    lp, ln, delta, S_base = z3.Reals("lp ln delta S_base")
    S_fp_curr, q_d, q_l = z3.Reals("S_fp_curr q_d q_l")
    rem_d, rem_l = z3.Reals("rem_d rem_l")

    eps = V_real - E_real
    lam = z3.If(eps >= 0, lp, ln)
    S_real_unclamped = S_real + lam * eps - delta * (S_real - S_base)
    S_fp_unclamped = S_fp_curr + q_d - q_l

    def clamp01(x):
        return z3.If(x < 0, z3.RealVal(0), z3.If(x > 1, z3.RealVal(1), x))

    S_real_next = clamp01(S_real_unclamped)
    S_fp_next = clamp01(S_fp_unclamped)

    inv_scale = z3.RealVal(1) / z3.RealVal(SCALE)
    step_err_bound = z3.RealVal(2) * inv_scale
    cum_bound = step_err_bound / delta

    s = z3.Solver()
    s.add(
        lp >= 0, lp <= 1, ln >= 0, ln <= 1,
        delta > 0, delta <= 1, S_base >= 0, S_base <= 1,
        S_real >= 0, S_real <= 1, S_fp_curr >= 0, S_fp_curr <= 1,
        V_real >= 0, V_real <= 1, E_real >= 0, E_real <= 1,
        rem_d >= 0, rem_d < inv_scale,
        rem_l >= 0, rem_l < inv_scale,
        q_d == lam * eps - rem_d,
        q_l == delta * (S_fp_curr - S_base) - rem_l,
        z3.Abs(S_real - S_fp_curr) <= cum_bound,
    )
    assert s.check() == z3.sat, "Quantization refinement premises must be SAT!"
    s.add(z3.Abs(S_real_next - S_fp_next) > cum_bound)
    res = s.check()
    print(f"[VERIFIED - NON-VACUOUS {str(res).upper()}] |S_t^R - S_t^ZK| <= 2/(SCALE*delta) inductively preserved.")
    assert res == z3.unsat, f"Refinement counterexample: {s.model()}"


if __name__ == "__main__":
    prove_verifier_soundness()
    prove_quantization_refinement()
    print("\nVERDICT: ZK-STP SOUNDNESS & REAL-TO-FIXED-POINT REFINEMENT PROVEN.")
    sys.exit(0)

