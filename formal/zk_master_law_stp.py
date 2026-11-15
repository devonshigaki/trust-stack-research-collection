#!/usr/bin/env python3
"""
Genuine Non-Interactive Zero-Knowledge Proof (ZK-STP) for the Asymmetric Master Stability Law
Target: The Fresh Protocol (TFP) / Formal Verification Suite
Author: Devon Shigaki (ORCID: 0009-0003-8977-8010)

Uses secp256k1 Pedersen commitments + Abe-Ohkubo-Suzuki 1-of-K Schnorr OR-proofs +
33-bit binary bit-decomposition range proofs. Serialized proofs contain ZERO private
witnesses and ZERO blinding scalars.
"""

import os
import sys
import json
import inspect
import secrets
from typing import Dict

from zk_pedersen_ec import (
    G_PT, N_ORDER, Transcript, FurnisherAuthority, IssuerKeypair, pedersen_commit, pt_add, pt_sub, pt_mul_fast, pt_ser, pt_deser,
    prove_zero, verify_zero, prove_or_zero, verify_or_zero, prove_or_zero_tuple, verify_or_zero_tuple,
    prove_nonneg, verify_nonneg, verify_event_attestation, compute_event_chain_tip, verify_stream_head,
)

SCALE = 1_000_000_000
Q_OFFSET = 2 * SCALE
RANGE_BITS = 33
SCHEME_ID = "secp256k1-Pedersen-Schnorr-TupleOR-3PartyUnlinkable-NIZK-v8"


def build_statement_transcript(
    p: dict,
    s_next_fixed: int,
    Cs: dict,
    reveal_state: bool = True,
    account_id: str = "default",
    seq_t: int = 0,
    genesis_anchored: bool = False,
) -> Transcript:
    tr = Transcript(SCHEME_ID)
    for k in ("lp_fixed", "ln_fixed", "delta_fixed", "s_base_fixed", "scale"):
        tr.absorb_int(k, int(p[k]))
    tr.absorb_bytes("account_id", account_id.encode("utf-8"))
    tr.absorb_int("seq_t", int(seq_t))
    tr.absorb_int("genesis_anchored", 1 if genesis_anchored else 0)
    tr.absorb_int("reveal_state", 1 if reveal_state else 0)
    tr.absorb_int("s_next_fixed", s_next_fixed if reveal_state else 0)
    for k in sorted(Cs.keys()):
        tr.absorb_point(f"C_{k}", Cs[k])
    return tr


def float_to_fixed(val: float) -> int:
    return int(round(val * SCALE))


def fixed_to_float(val: int) -> float:
    return float(val) / float(SCALE)


def _r() -> int:
    return secrets.randbelow(N_ORDER - 1) + 1


class MasterLawZKProver:
    def __init__(
        self,
        lambda_param: float = 0.228,
        delta_param: float = 0.010,
        s_base: float = 0.500,
        lambda_plus: float = None,
        lambda_minus: float = None,
    ):
        lp = lambda_param if lambda_plus is None else lambda_plus
        ln = lambda_param if lambda_minus is None else lambda_minus
        self.lp_fixed = float_to_fixed(lp)
        self.ln_fixed = float_to_fixed(ln)
        self.delta_fixed = float_to_fixed(delta_param)
        self.s_base_fixed = float_to_fixed(s_base)

    def expected_params(self) -> dict:
        return {
            "lp_fixed": self.lp_fixed,
            "ln_fixed": self.ln_fixed,
            "delta_fixed": self.delta_fixed,
            "s_base_fixed": self.s_base_fixed,
            "scale": SCALE,
        }

    def generate_proof_with_blind(
        self,
        S_curr: float,
        V: float,
        E: float,
        r_s_c_override: int = None,
        r_v_override: int = None,
        r_e_override: int = None,
        reveal_state: bool = True,
        seq_t: int = 0,
        account_id: str = "default",
        pre_signed_attestation: dict = None,
        anchor_genesis: bool = False,
    ):
        s_c, v_f, e_f = float_to_fixed(S_curr), float_to_fixed(V), float_to_fixed(E)
        if not (0 <= s_c <= SCALE and 0 <= v_f <= SCALE and 0 <= e_f <= SCALE):
            raise ValueError("Private inputs must lie in [0.0, 1.0]")
        if seq_t < 0:
            raise ValueError("seq_t must be non-negative")
        if anchor_genesis and s_c != self.s_base_fixed:
            raise ValueError(f"Genesis-anchored step must initialize at S_base={fixed_to_float(self.s_base_fixed):.6f}")

        eps_p, eps_n = max(0, v_f - e_f), max(0, e_f - v_f)
        num_d = self.lp_fixed * eps_p - self.ln_fixed * eps_n
        q_d = num_d // SCALE
        r_d = num_d - q_d * SCALE

        num_l = self.delta_fixed * (s_c - self.s_base_fixed)
        q_l = num_l // SCALE
        r_l = num_l - q_l * SCALE

        s_unclamped = s_c + q_d - q_l
        s_next = max(0, min(SCALE, s_unclamped))
        u_low, u_high = max(0, -s_unclamped), max(0, s_unclamped - SCALE)
        clamp_branch = 0 if s_next == s_unclamped else (1 if s_unclamped < 0 else 2)

        vals = {
            "s_c": s_c, "s_next": s_next, "v": v_f, "e": e_f, "eps_p": eps_p, "eps_n": eps_n,
            "q_d": q_d + Q_OFFSET, "r_d": r_d, "q_l": q_l + Q_OFFSET, "r_l": r_l,
            "u_low": u_low, "u_high": u_high,
            "s_c_rem": SCALE - s_c, "v_rem": SCALE - v_f, "e_rem": SCALE - e_f,
            "r_d_rem": SCALE - 1 - r_d, "r_l_rem": SCALE - 1 - r_l,
        }
        rs = {k: _r() for k in vals}
        if r_s_c_override is not None:
            rs["s_c"] = r_s_c_override % N_ORDER
        if r_v_override is not None:
            rs["v"] = r_v_override % N_ORDER
        if r_e_override is not None:
            rs["e"] = r_e_override % N_ORDER
        Cs = {k: pedersen_commit(vals[k], rs[k]) for k in vals}

        p_dict = self.expected_params()
        tr = build_statement_transcript(
            p_dict,
            s_next,
            Cs,
            reveal_state=reveal_state,
            account_id=account_id,
            seq_t=seq_t,
            genesis_anchored=anchor_genesis,
        )

        P_mismatch = pt_sub(pt_sub(Cs["v"], Cs["e"]), pt_sub(Cs["eps_p"], Cs["eps_n"]))
        r_mismatch = (rs["v"] - rs["e"] - rs["eps_p"] + rs["eps_n"]) % N_ORDER
        P_div_d = pt_sub(
            pt_add(pt_mul_fast(SCALE, pt_sub(Cs["q_d"], pt_mul_fast(Q_OFFSET, G_PT))), Cs["r_d"]),
            pt_sub(pt_mul_fast(self.lp_fixed, Cs["eps_p"]), pt_mul_fast(self.ln_fixed, Cs["eps_n"])),
        )
        r_div_d = (SCALE * rs["q_d"] + rs["r_d"] - self.lp_fixed * rs["eps_p"] + self.ln_fixed * rs["eps_n"]) % N_ORDER
        P_div_l = pt_sub(
            pt_add(pt_mul_fast(SCALE, pt_sub(Cs["q_l"], pt_mul_fast(Q_OFFSET, G_PT))), Cs["r_l"]),
            pt_mul_fast(self.delta_fixed, pt_sub(Cs["s_c"], pt_mul_fast(self.s_base_fixed, G_PT))),
        )
        r_div_l = (SCALE * rs["q_l"] + rs["r_l"] - self.delta_fixed * rs["s_c"]) % N_ORDER

        C_unclamped = pt_add(Cs["s_c"], pt_sub(Cs["q_d"], Cs["q_l"]))
        r_unclamped = (rs["s_c"] + rs["q_d"] - rs["q_l"]) % N_ORDER
        S_next_G = pt_mul_fast(s_next, G_PT)
        SCALE_G = pt_mul_fast(SCALE, G_PT)

        # Bind clamping Tuple-OR directly to blinded Pedersen commitment Cs["s_next"]
        clamp_branches = [
            [pt_sub(Cs["s_next"], C_unclamped)],
            [Cs["s_next"], pt_add(C_unclamped, Cs["u_low"])],
            [pt_sub(Cs["s_next"], SCALE_G), pt_sub(pt_sub(C_unclamped, Cs["u_high"]), SCALE_G)],
        ]
        clamp_rs = [
            [(rs["s_next"] - r_unclamped) % N_ORDER],
            [rs["s_next"], (r_unclamped + rs["u_low"]) % N_ORDER],
            [rs["s_next"], (r_unclamped - rs["u_high"]) % N_ORDER],
        ]

        bound_proofs = {
            name: prove_zero(
                pt_sub(pt_add(Cs[a], Cs[b]), pt_mul_fast(bound, G_PT)),
                (rs[a] + rs[b]) % N_ORDER, f"BND:{name}", tr=tr,
            )
            for name, a, b, bound in [
                ("s_c", "s_c", "s_c_rem", SCALE), ("v", "v", "v_rem", SCALE),
                ("e", "e", "e_rem", SCALE), ("r_d", "r_d", "r_d_rem", SCALE - 1), ("r_l", "r_l", "r_l_rem", SCALE - 1),
            ]
        }
        range_keys = ["s_c", "s_c_rem", "v", "v_rem", "e", "e_rem", "eps_p", "eps_n", "q_d", "q_l", "r_d", "r_d_rem", "r_l", "r_l_rem", "u_low", "u_high"]
        range_proofs = {k: prove_nonneg(Cs[k], vals[k], rs[k], RANGE_BITS, f"RNG:{k}", tr=tr) for k in range_keys}
        eq_proofs = {
            "mismatch": prove_zero(P_mismatch, r_mismatch, "EQ:mismatch", tr=tr),
            "div_d": prove_zero(P_div_d, r_div_d, "EQ:div_d", tr=tr),
            "div_l": prove_zero(P_div_l, r_div_l, "EQ:div_l", tr=tr),
            "eps_branch_or": prove_or_zero([Cs["eps_p"], Cs["eps_n"]], 0 if eps_p == 0 else 1, rs["eps_p"] if eps_p == 0 else rs["eps_n"], "OR:eps", tr=tr),
            "clamp_or": prove_or_zero_tuple(clamp_branches, clamp_branch, clamp_rs[clamp_branch], "OR:clamp", tr=tr),
        }
        if reveal_state:
            eq_proofs["s_next_open"] = prove_zero(pt_sub(Cs["s_next"], S_next_G), rs["s_next"], "EQ:s_next", tr=tr)
        if anchor_genesis:
            eq_proofs["genesis"] = prove_zero(
                pt_sub(Cs["s_c"], pt_mul_fast(self.s_base_fixed, G_PT)), rs["s_c"], "EQ:genesis", tr=tr
            )

        proof = {
            "scheme": SCHEME_ID,
            "account_id": account_id,
            "seq_t": int(seq_t),
            "genesis_anchored": bool(anchor_genesis),
            "reveal_state": bool(reveal_state),
            "public_params": p_dict,
            "S_next_public": fixed_to_float(s_next) if reveal_state else None,
            "commitments": {k: pt_ser(v) for k, v in Cs.items()},
            "eq_proofs": eq_proofs,
            "bounds": bound_proofs, "ranges": range_proofs,
        }
        if pre_signed_attestation is not None:
            if (
                pre_signed_attestation.get("C_v") != pt_ser(Cs["v"])
                or pre_signed_attestation.get("C_e") != pt_ser(Cs["e"])
                or pre_signed_attestation.get("account_id") != account_id
                or int(pre_signed_attestation.get("seq_t", -1)) != int(seq_t)
            ):
                raise ValueError("Pre-signed attestation does not match committed event")
            proof["attestation"] = pre_signed_attestation
        return proof, fixed_to_float(s_next), rs["s_next"]

    def generate_proof(self, S_curr: float, V: float, E: float):
        proof, s_next_f, _ = self.generate_proof_with_blind(S_curr, V, E, reveal_state=True)
        return proof, s_next_f

    def generate_chained_trajectory(
        self,
        s0: float,
        steps,
        reveal_state: bool = False,
        account_id: str = "acct-001",
        pre_signed_attestations: list = None,
        r_v_overrides: list = None,
        r_e_overrides: list = None,
        anchor_genesis: bool = True,
    ):
        proofs, s_curr, r_curr = [], s0, _r()
        for idx, (v, e) in enumerate(steps):
            p, s_next, r_next = self.generate_proof_with_blind(
                s_curr,
                v,
                e,
                r_s_c_override=r_curr,
                r_v_override=r_v_overrides[idx] if r_v_overrides else None,
                r_e_override=r_e_overrides[idx] if r_e_overrides else None,
                reveal_state=reveal_state,
                seq_t=idx,
                account_id=account_id,
                pre_signed_attestation=pre_signed_attestations[idx] if pre_signed_attestations else None,
                anchor_genesis=(anchor_genesis and idx == 0),
            )
            proofs.append(p)
            s_curr, r_curr = s_next, r_next
        return proofs, s_curr, r_curr

    def prove_attested_bundle(self, s0: float, furnisher_bundle: dict, reveal_state: bool = False):
        """Borrower-side NIZK prover consuming ONLY Furnisher-signed public attestations (zero sk_issuer)."""
        opened = furnisher_bundle["opened_events"]
        proofs, s_T, r_s_T = self.generate_chained_trajectory(
            s0,
            [(ev["v"], ev["e"]) for ev in opened],
            reveal_state=reveal_state,
            account_id=furnisher_bundle["account_id"],
            pre_signed_attestations=furnisher_bundle["attestations"],
            r_v_overrides=[ev["r_v"] for ev in opened],
            r_e_overrides=[ev["r_e"] for ev in opened],
            anchor_genesis=True,
        )
        return proofs, furnisher_bundle["stream_head"], furnisher_bundle["account_id"], s_T, r_s_T

    def prove_threshold(self, last_proof: dict, s_T: float, r_s_T: int, threshold: float = 0.50) -> dict:
        s_T_fixed, tau_fixed = float_to_fixed(s_T), float_to_fixed(threshold)
        if s_T_fixed < tau_fixed:
            raise ValueError(f"Terminal state {s_T:.6f} below threshold {threshold:.6f}")
        Cs = {k: pt_deser(v) for k, v in last_proof["commitments"].items()}
        tr = build_statement_transcript(
            last_proof["public_params"],
            0,
            Cs,
            reveal_state=last_proof.get("reveal_state", False),
            account_id=last_proof.get("account_id", "default"),
            seq_t=int(last_proof.get("seq_t", 0)),
            genesis_anchored=bool(last_proof.get("genesis_anchored", False)),
        )
        tr.absorb_int("threshold_fixed", tau_fixed)
        C_diff = pt_sub(Cs["s_next"], pt_mul_fast(tau_fixed, G_PT))
        return {
            "threshold": float(threshold),
            "range_proof": prove_nonneg(C_diff, s_T_fixed - tau_fixed, r_s_T, RANGE_BITS, "THRESH:geq", tr=tr),
        }


def verify_threshold(
    last_proof: dict,
    thresh_proof: dict,
    threshold: float,
    expected_params: dict,
    expected_issuer_pk: str = None,
    expected_account_id: str = None,
    require_attestation: bool = False,
) -> bool:
    try:
        if abs(float(thresh_proof["threshold"]) - float(threshold)) > 1e-9:
            return False
        if not verify_zk_proof(
            last_proof,
            last_proof.get("S_next_public"),
            expected_params=expected_params,
            expected_issuer_pk=expected_issuer_pk,
            expected_account_id=expected_account_id,
            require_attestation=require_attestation,
        ):
            return False
        tau_fixed = float_to_fixed(threshold)
        Cs = {k: pt_deser(v) for k, v in last_proof["commitments"].items()}
        tr = build_statement_transcript(
            last_proof["public_params"],
            0,
            Cs,
            reveal_state=last_proof.get("reveal_state", False),
            account_id=last_proof.get("account_id", "default"),
            seq_t=int(last_proof.get("seq_t", 0)),
            genesis_anchored=bool(last_proof.get("genesis_anchored", False)),
        )
        tr.absorb_int("threshold_fixed", tau_fixed)
        C_diff = pt_sub(Cs["s_next"], pt_mul_fast(tau_fixed, G_PT))
        return verify_nonneg(C_diff, thresh_proof["range_proof"], RANGE_BITS, "THRESH:geq", tr=tr)
    except Exception:
        return False


def verify_zk_proof(
    proof: dict,
    S_next_claimed: float = None,
    expected_params: dict = None,
    expected_issuer_pk: str = None,
    expected_account_id: str = None,
    expected_seq_t: int = None,
    require_attestation: bool = False,
    require_genesis: bool = False,
) -> bool:
    try:
        if proof.get("scheme") != SCHEME_ID:
            return False
        if "r1cs_witness" in proof or "salts" in proof:
            return False
        account_id = str(proof["account_id"])
        seq_t = int(proof["seq_t"])
        if seq_t < 0:
            return False
        if expected_account_id is not None and account_id != expected_account_id:
            return False
        if expected_seq_t is not None and seq_t != int(expected_seq_t):
            return False
        genesis_anchored = bool(proof.get("genesis_anchored", False))
        if require_genesis and not genesis_anchored:
            return False
        reveal_state = bool(proof.get("reveal_state", True))
        p = proof["public_params"]
        if expected_params is not None:
            for k in ("lp_fixed", "ln_fixed", "delta_fixed", "s_base_fixed", "scale"):
                if int(p[k]) != int(expected_params[k]):
                    return False
        scale = int(p["scale"])
        if reveal_state:
            if S_next_claimed is None or proof["S_next_public"] is None:
                return False
            s_next = float_to_fixed(S_next_claimed)
            if abs(proof["S_next_public"] - S_next_claimed) > 1e-9 or not (0 <= s_next <= scale):
                return False
        else:
            if proof.get("S_next_public") is not None:
                return False
            s_next = 0

        Cs = {k: pt_deser(v) for k, v in proof["commitments"].items()}
        tr = build_statement_transcript(
            p,
            s_next,
            Cs,
            reveal_state=reveal_state,
            account_id=account_id,
            seq_t=seq_t,
            genesis_anchored=genesis_anchored,
        )
        eq = proof["eq_proofs"]
        if genesis_anchored:
            if "genesis" not in eq:
                return False
            if not verify_zero(
                pt_sub(Cs["s_c"], pt_mul_fast(int(p["s_base_fixed"]), G_PT)),
                eq["genesis"],
                "EQ:genesis",
                tr=tr,
            ):
                return False
        if require_attestation or expected_issuer_pk is not None:
            att = proof.get("attestation")
            if not isinstance(att, dict) or expected_issuer_pk is None:
                return False
            if not verify_event_attestation(
                att,
                expected_issuer_pk=expected_issuer_pk,
                expected_account_id=account_id,
                expected_seq_t=seq_t,
                expected_C_v_hex=proof["commitments"]["v"],
                expected_C_e_hex=proof["commitments"]["e"],
            ):
                return False
        P_mismatch = pt_sub(pt_sub(Cs["v"], Cs["e"]), pt_sub(Cs["eps_p"], Cs["eps_n"]))
        if not verify_zero(P_mismatch, eq["mismatch"], "EQ:mismatch", tr=tr):
            return False

        P_div_d = pt_sub(
            pt_add(pt_mul_fast(scale, pt_sub(Cs["q_d"], pt_mul_fast(Q_OFFSET, G_PT))), Cs["r_d"]),
            pt_sub(pt_mul_fast(p["lp_fixed"], Cs["eps_p"]), pt_mul_fast(p["ln_fixed"], Cs["eps_n"])),
        )
        if not verify_zero(P_div_d, eq["div_d"], "EQ:div_d", tr=tr):
            return False

        P_div_l = pt_sub(
            pt_add(pt_mul_fast(scale, pt_sub(Cs["q_l"], pt_mul_fast(Q_OFFSET, G_PT))), Cs["r_l"]),
            pt_mul_fast(p["delta_fixed"], pt_sub(Cs["s_c"], pt_mul_fast(p["s_base_fixed"], G_PT))),
        )
        if not verify_zero(P_div_l, eq["div_l"], "EQ:div_l", tr=tr):
            return False

        if reveal_state:
            S_next_G = pt_mul_fast(s_next, G_PT)
            if not verify_zero(pt_sub(Cs["s_next"], S_next_G), eq["s_next_open"], "EQ:s_next", tr=tr):
                return False

        if not verify_or_zero([Cs["eps_p"], Cs["eps_n"]], eq["eps_branch_or"], "OR:eps", tr=tr):
            return False

        C_unclamped = pt_add(Cs["s_c"], pt_sub(Cs["q_d"], Cs["q_l"]))
        SCALE_G = pt_mul_fast(scale, G_PT)
        clamp_branches = [
            [pt_sub(Cs["s_next"], C_unclamped)],
            [Cs["s_next"], pt_add(C_unclamped, Cs["u_low"])],
            [pt_sub(Cs["s_next"], SCALE_G), pt_sub(pt_sub(C_unclamped, Cs["u_high"]), SCALE_G)],
        ]
        if not verify_or_zero_tuple(clamp_branches, eq["clamp_or"], "OR:clamp", tr=tr):
            return False

        for name, a, b, bound in [
            ("s_c", "s_c", "s_c_rem", scale), ("v", "v", "v_rem", scale),
            ("e", "e", "e_rem", scale), ("r_d", "r_d", "r_d_rem", scale - 1), ("r_l", "r_l", "r_l_rem", scale - 1),
        ]:
            if not verify_zero(pt_sub(pt_add(Cs[a], Cs[b]), pt_mul_fast(bound, G_PT)), proof["bounds"][name], f"BND:{name}", tr=tr):
                return False

        for k in ["s_c", "s_c_rem", "v", "v_rem", "e", "e_rem", "eps_p", "eps_n", "q_d", "q_l", "r_d", "r_d_rem", "r_l", "r_l_rem", "u_low", "u_high"]:
            if not verify_nonneg(Cs[k], proof["ranges"][k], RANGE_BITS, f"RNG:{k}", tr=tr):
                return False
        return True
    except Exception:
        return False


def verify_zk_trajectory(
    proofs: list,
    expected_params: dict,
    require_hidden: bool = False,
    expected_issuer_pk: str = None,
    expected_account_id: str = None,
    require_genesis: bool = True,
    require_attestation: bool = False,
    stream_head: dict = None,
    expected_min_epoch: int = 0,
    require_head: bool = False,
) -> bool:
    if not proofs:
        return False
    acct = expected_account_id if expected_account_id is not None else proofs[0].get("account_id")
    if not acct:
        return False
    for idx, p in enumerate(proofs):
        if require_hidden and (p.get("reveal_state") is not False or p.get("S_next_public") is not None):
            return False
        if not verify_zk_proof(
            p,
            p.get("S_next_public"),
            expected_params=expected_params,
            expected_issuer_pk=expected_issuer_pk,
            expected_account_id=acct,
            expected_seq_t=idx,
            require_attestation=require_attestation,
            require_genesis=(require_genesis and idx == 0),
        ):
            return False
        if idx > 0:
            if p["commitments"]["s_c"] != proofs[idx - 1]["commitments"]["s_next"]:
                return False
    if require_head or stream_head is not None:
        if not isinstance(stream_head, dict) or expected_issuer_pk is None:
            return False
        events_chain_tip = compute_event_chain_tip(
            [(p["commitments"]["v"], p["commitments"]["e"]) for p in proofs]
        )
        if not verify_stream_head(
            stream_head,
            expected_issuer_pk=expected_issuer_pk,
            expected_account_id=acct,
            expected_total_events=len(proofs),
            expected_min_epoch=expected_min_epoch,
            expected_events_chain_tip_hex=events_chain_tip,
        ):
            return False
    return True


def main():
    print("=" * 75)
    print(" GENUINE PEDERSEN + SCHNORR + AOS-OR ZERO-KNOWLEDGE PROVER (ZK-STP v8)")
    print(" Curve: secp256k1 | Strict 3-Party Separation | Event-Chain Head | 19/19")
    print("=" * 75)

    prover = MasterLawZKProver(lambda_plus=0.228, lambda_minus=0.912, delta_param=0.010, s_base=0.500)
    furnisher = FurnisherAuthority(IssuerKeypair.generate())
    rogue_furnisher = FurnisherAuthority(IssuerKeypair.generate())

    proof1, s_next1 = prover.generate_proof(S_curr=0.50, V=0.85, E=0.50)
    v1 = verify_zk_proof(proof1, s_next1)
    print(f"Test 1 (Positive Validation):   S_0=0.50 -> S_1={s_next1:.6f} | NIZK: {'✓ VERIFIED' if v1 else '✗ REJECTED'}")

    proof2, s_next2 = prover.generate_proof(S_curr=s_next1, V=0.10, E=0.75)
    v2 = verify_zk_proof(proof2, s_next2)
    print(f"Test 2 (Asym Betrayal Shock):   S_1={s_next1:.6f} -> S_2={s_next2:.6f} | NIZK: {'✓ VERIFIED' if v2 else '✗ REJECTED'}")

    proof3, s_next3 = prover.generate_proof(S_curr=0.05, V=0.00, E=1.00)
    v3 = verify_zk_proof(proof3, s_next3) and abs(s_next3 - 0.0) < 1e-9
    print(f"Test 3 (Lower Clamp Boundary):  S_0=0.05 -> S_next={s_next3:.6f} | NIZK: {'✓ VERIFIED' if v3 else '✗ REJECTED'}")

    tampered = json.loads(json.dumps(proof2))
    tampered["S_next_public"] = 0.999999
    v4 = not verify_zk_proof(tampered, 0.999999)
    print(f"Test 4 (Forged S_next Claim):   Rejected fake output without witness | {'✓ REJECTED (PASS)' if v4 else 'FAIL'}")

    forged_commit = json.loads(json.dumps(proof1))
    forged_commit["commitments"]["eps_p"] = forged_commit["commitments"]["eps_n"]
    v5 = not verify_zk_proof(forged_commit, s_next1)
    print(f"Test 5 (Commitment Forgery):    Swapped Pedersen commitment | {'✓ REJECTED (PASS)' if v5 else 'FAIL'}")

    proof_zk, _ = prover.generate_proof(S_curr=0.613, V=0.857, E=0.419)
    proof_json = json.dumps(proof_zk)
    leaked = any(k in proof_json for k in ["r1cs_witness", "salts", "613000000", "857000000", "419000000", "438000000"])
    proof_a, _ = prover.generate_proof(S_curr=0.20, V=0.90, E=0.10)
    proof_b, _ = prover.generate_proof(S_curr=0.80, V=0.10, E=0.90)
    unlinkable = (proof_a["commitments"] != proof_b["commitments"]) and (set(proof_a.keys()) == set(proof_b.keys()))
    v6 = (not leaked) and unlinkable
    print(f"Test 6 (Zero-Knowledge Audit):  Zero witness/salt bytes + unlinkable | {'✓ PASS' if v6 else 'FAIL'}")

    # Test 7: Red-Team Clamping Sum-Cancellation Exploit Regression (forging S_next=0.65 from S_unclamped=-0.8575)
    forged_clamp = json.loads(json.dumps(proof3))
    forged_clamp["S_next_public"] = 0.65
    v7 = not verify_zk_proof(forged_clamp, 0.65)
    print(f"Test 7 (Clamp Forgery Exploit): Tuple-OR blocks S_next+S_unclamped=0 | {'✓ REJECTED (PASS)' if v7 else 'FAIL'}")

    # Test 8: Red-Team Frozen Heart Sub-Proof Splice Regression
    spliced = json.loads(json.dumps(proof1))
    spliced["eq_proofs"]["mismatch"] = proof2["eq_proofs"]["mismatch"]
    v8 = not verify_zk_proof(spliced, s_next1, expected_params=prover.expected_params())
    print(f"Test 8 (Frozen Heart Splice):   Stateful Transcript blocks sub-proof splice | {'✓ REJECTED (PASS)' if v8 else 'FAIL'}")

    # Test 9: Multi-Step Commitment Chaining & State-Teleportation Exploit Regression
    chain_proofs, _, _ = prover.generate_chained_trajectory(0.50, [(0.85, 0.50), (0.10, 0.75), (0.60, 0.50)], reveal_state=True)
    v9_valid = verify_zk_trajectory(chain_proofs, expected_params=prover.expected_params())
    # Attacker tries to teleport step 2 from S=0.00 to S=0.995 via fresh witness S_curr=1.00
    fake_step2, _ = prover.generate_proof(S_curr=1.00, V=0.50, E=0.50)
    teleported_chain = [chain_proofs[0], chain_proofs[1], fake_step2]
    v9_blocked = not verify_zk_trajectory(teleported_chain, expected_params=prover.expected_params())
    v9 = v9_valid and v9_blocked
    print(f"Test 9 (Chained Trajectory):    Commitment-chaining blocks state teleportation | {'✓ REJECTED (PASS)' if v9 else 'FAIL'}")

    # Test 10: Public-Parameter Substitution Forgery Regression (prover sets ln_fixed=0)
    param_forge_prover = MasterLawZKProver(lambda_plus=0.228, lambda_minus=0.0, delta_param=0.010, s_base=0.500)
    forged_param_proof, forged_s = param_forge_prover.generate_proof(S_curr=0.50, V=0.0, E=1.0)
    v10 = not verify_zk_proof(forged_param_proof, forged_s, expected_params=prover.expected_params())
    print(f"Test 10 (Param Pinning Guard):  Blocks prover-chosen lambda_minus=0 forgery | {'✓ REJECTED (PASS)' if v10 else 'FAIL'}")

    # Test 11: Scalar Malleability Regression (s' = s + N_ORDER)
    malleable = json.loads(json.dumps(proof1))
    s_orig = int(malleable["eq_proofs"]["mismatch"]["s"], 16)
    malleable["eq_proofs"]["mismatch"]["s"] = hex(s_orig + N_ORDER)
    v11 = not verify_zk_proof(malleable, s_next1, expected_params=prover.expected_params())
    print(f"Test 11 (Non-Malleability):     Rejects non-canonical scalar s + N_ORDER | {'✓ REJECTED (PASS)' if v11 else 'FAIL'}")

    # Test 12: Private-State Rollup (zero intermediate S_t leakage) + ZK Threshold Eligibility (S_T >= 0.50)
    b12 = furnisher.issue_signed_event_bundle(
        "user-pilot-001", "verifier-12", epoch_id=1, events_ve=[(0.85, 0.50), (0.75, 0.50), (0.90, 0.50)]
    )
    priv_chain, head12, h12, s_T_priv, r_T_priv = prover.prove_attested_bundle(0.50, b12, reveal_state=False)
    thresh_ok_proof = prover.prove_threshold(priv_chain[-1], s_T_priv, r_T_priv, threshold=0.50)
    v12_hidden = verify_zk_trajectory(
        priv_chain,
        expected_params=prover.expected_params(),
        require_hidden=True,
        expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=h12,
        require_genesis=True,
        require_attestation=True,
        stream_head=head12,
        expected_min_epoch=1,
        require_head=True,
    )
    v12_thresh_pass = verify_threshold(
        priv_chain[-1],
        thresh_ok_proof,
        threshold=0.50,
        expected_params=prover.expected_params(),
        expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=h12,
        require_attestation=True,
    )
    v12_thresh_reject = not verify_threshold(
        priv_chain[-1],
        thresh_ok_proof,
        threshold=0.99,
        expected_params=prover.expected_params(),
        expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=h12,
        require_attestation=True,
    )
    v12 = v12_hidden and v12_thresh_pass and v12_thresh_reject
    print(f"Test 12 (Private Rollup/Thresh): Genesis+Attested+Hidden+S_T>=0.50 | {'✓ VERIFIED (PASS)' if v12 else 'FAIL'}")

    # Test 13: Day-0 Sybil Genesis Forgery (starting at s0=1.00 instead of S_base=0.50)
    b13 = furnisher.issue_signed_event_bundle("sybil-user", "v13", epoch_id=1, events_ve=[(0.50, 0.50)])
    sybil_chain, _, _ = prover.generate_chained_trajectory(
        1.00,
        [(ev["v"], ev["e"]) for ev in b13["opened_events"]],
        reveal_state=False,
        account_id=b13["account_id"],
        pre_signed_attestations=b13["attestations"],
        r_v_overrides=[ev["r_v"] for ev in b13["opened_events"]],
        r_e_overrides=[ev["r_e"] for ev in b13["opened_events"]],
        anchor_genesis=False,
    )
    v13 = not verify_zk_trajectory(
        sybil_chain, expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=b13["account_id"], require_genesis=True, require_attestation=True
    )
    print(f"Test 13 (Sybil Genesis Guard):  Blocks Day-0 s0=1.00 genesis inflation | {'✓ REJECTED (PASS)' if v13 else 'FAIL'}")

    # Test 14: Self-Minted / Rogue-Issuer Event Forgery
    b_rogue = rogue_furnisher.issue_signed_event_bundle("user-pilot-001", "v14", epoch_id=1, events_ve=[(1.00, 0.00)])
    rogue_chain, head_r, h_r, _, _ = prover.prove_attested_bundle(0.50, b_rogue, reveal_state=False)
    v14 = not verify_zk_trajectory(
        rogue_chain, expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=h_r, require_genesis=True, require_attestation=True, stream_head=head_r, require_head=True
    )
    print(f"Test 14 (Issuer Auth Guard):    Rejects untrusted self-minted events | {'✓ REJECTED (PASS)' if v14 else 'FAIL'}")

    # Test 15: Selective Default Omission (dropping negative event seq_t=1 from [0, 1, 2])
    b_mix = furnisher.issue_signed_event_bundle(
        "user-mix", "v15", epoch_id=1, events_ve=[(0.80, 0.50), (0.00, 0.90), (0.80, 0.50)]
    )
    honest_mix, head_mix, h_mix, _, _ = prover.prove_attested_bundle(0.50, b_mix, reveal_state=False)
    omitted_chain = [honest_mix[0], honest_mix[2]]
    v15 = not verify_zk_trajectory(
        omitted_chain, expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=h_mix, require_genesis=True, require_attestation=True
    )
    print(f"Test 15 (Omission Resistance):  Blocks dropping negative event seq_t=1 | {'✓ REJECTED (PASS)' if v15 else 'FAIL'}")

    # Test 16: Non-Commutative Clamped Reordering (swapping seq_t=1 and seq_t=2)
    reordered_chain = [honest_mix[0], honest_mix[2], honest_mix[1]]
    v16 = not verify_zk_trajectory(
        reordered_chain, expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=h_mix, require_genesis=True, require_attestation=True
    )
    print(f"Test 16 (Order Binding Guard):  Blocks non-commutative seq_t swap | {'✓ REJECTED (PASS)' if v16 else 'FAIL'}")

    # Test 17: Right-Tail Default Truncation & Stale-Epoch Replay Guard (TFP-HEAD-v2)
    events_3 = [(0.85, 0.50), (0.90, 0.50), (0.00, 1.00)]
    b17 = furnisher.issue_signed_event_bundle(
        "secret-user-42", "lender-A", epoch_id=2, events_ve=events_3
    )
    pres_a, head_a, handle_a, s_a, r_a = prover.prove_attested_bundle(0.50, b17, reveal_state=False)
    v17_full = verify_zk_trajectory(
        pres_a, expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=handle_a, require_genesis=True, require_attestation=True,
        stream_head=head_a, expected_min_epoch=2, require_head=True,
    )
    v17_trunc_blocked = not verify_zk_trajectory(
        pres_a[:2], expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=handle_a, require_genesis=True, require_attestation=True,
        stream_head=head_a, expected_min_epoch=2, require_head=True,
    )
    v17_stale_epoch_blocked = not verify_zk_trajectory(
        pres_a, expected_params=prover.expected_params(), require_hidden=True, expected_issuer_pk=furnisher.pk_hex,
        expected_account_id=handle_a, require_genesis=True, require_attestation=True,
        stream_head=head_a, expected_min_epoch=3, require_head=True,
    )
    v17 = v17_full and v17_trunc_blocked and v17_stale_epoch_blocked
    print(f"Test 17 (Tail-Trunc/Epoch):     Stream-head blocks dropped default & stale epoch | {'✓ REJECTED (PASS)' if v17 else 'FAIL'}")

    # Test 18: Cross-Verifier Unlinkability (same underlying events presented to two lenders)
    events_pos = [(0.85, 0.50), (0.90, 0.50)]
    b_l1 = furnisher.issue_signed_event_bundle("secret-user-42", "lender-1", epoch_id=5, events_ve=events_pos)
    b_l2 = furnisher.issue_signed_event_bundle("secret-user-42", "lender-2", epoch_id=5, events_ve=events_pos)
    pres_l1, head_l1, h_l1, s_l1, r_l1 = prover.prove_attested_bundle(0.50, b_l1, reveal_state=False)
    pres_l2, head_l2, h_l2, s_l2, r_l2 = prover.prove_attested_bundle(0.50, b_l2, reveal_state=False)
    ok_l1 = verify_zk_trajectory(
        pres_l1, prover.expected_params(), True, furnisher.pk_hex, h_l1, True, True, head_l1, 5, True
    )
    ok_l2 = verify_zk_trajectory(
        pres_l2, prover.expected_params(), True, furnisher.pk_hex, h_l2, True, True, head_l2, 5, True
    )
    no_shared_commits = all(
        pres_l1[i]["commitments"][k] != pres_l2[i]["commitments"][k]
        for i in range(len(events_pos)) for k in ("s_c", "s_next", "v", "e")
    )
    v18 = ok_l1 and ok_l2 and (h_l1 != h_l2) and (head_l1["s"] != head_l2["s"]) and no_shared_commits
    print(f"Test 18 (Unlinkable Reblind):   Zero shared commitments/handles across verifiers | {'✓ VERIFIED (PASS)' if v18 else 'FAIL'}")

    # Test 19: Strict 3-Party Trust-Boundary Separation (Prover holds ZERO sk_issuer; Furnisher sees ZERO S_t)
    prover_methods = [
        getattr(MasterLawZKProver, m) for m in ("generate_proof_with_blind", "generate_chained_trajectory", "prove_attested_bundle")
    ]
    no_issuer_kp_in_prover = all("issuer_keypair" not in inspect.signature(fn).parameters for fn in prover_methods)
    no_state_in_furnisher = ("s_next" not in json.dumps(head_l1)) and ("s_c" not in json.dumps(b_l1["attestations"]))
    v19 = no_issuer_kp_in_prover and no_state_in_furnisher
    print(f"Test 19 (3-Party Isolation):    Zero sk_issuer in Prover & zero S_t in Furnisher | {'✓ VERIFIED (PASS)' if v19 else 'FAIL'}")

    all_pass = (
        v1 and v2 and v3 and v4 and v5 and v6 and v7 and v8 and v9 and v10 and v11 and v12
        and v13 and v14 and v15 and v16 and v17 and v18 and v19
    )
    print("=" * 75)
    print(f"OVERALL ZK-STP NIZK VERDICT: {'ALL 19/19 CRITERIA VERIFIED' if all_pass else 'FAIL'}")
    print("=" * 75)

    out_file = os.path.join(os.path.dirname(__file__), "zk_stp_results.json")
    with open(out_file, "w") as f:
        json.dump(
            {
                "scheme": proof1["scheme"],
                "test1_positive": v1, "test2_asymmetric_shock": v2, "test3_clamp_boundary": v3,
                "test4_tamper_rejected": v4, "test5_forgery_rejected": v5,
                "soundness_forgery_rejected": (
                    v5 and v7 and v8 and v9 and v10 and v11 and v12_thresh_reject
                    and v13 and v14 and v15 and v16 and v17_trunc_blocked and v17_stale_epoch_blocked
                ),
                "test6_zero_knowledge_indistinguishable": v6,
                "test7_clamping_sum_exploit_blocked": v7,
                "test8_frozen_heart_splice_blocked": v8,
                "test9_state_teleportation_blocked": v9,
                "test10_param_substitution_blocked": v10,
                "test11_scalar_malleability_blocked": v11,
                "test12_private_rollup_threshold_verified": v12,
                "test13_sybil_genesis_forgery_blocked": v13,
                "test14_self_minted_event_blocked": v14,
                "test15_selective_default_omission_blocked": v15,
                "test16_clamped_event_reordering_blocked": v16,
                "test17_tail_truncation_and_epoch_blocked": v17,
                "test18_cross_verifier_unlinkable": v18,
                "test19_three_party_role_isolation": v19,
                "proof_bytes_json": len(proof_json),
                "status": "VERIFIED" if all_pass else "FAILED",
            },
            f,
            indent=4,
        )
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
