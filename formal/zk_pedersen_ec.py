#!/usr/bin/env python3
"""
secp256k1 Pedersen Commitments, Abe-Ohkubo-Suzuki 1-of-K Schnorr OR-Proofs,
and 33-Bit Binary Bit-Decomposition Range Proofs (Zero Witness/Salt Leakage).

SECURITY NOTICE (RESEARCH_REFERENCE_ONLY):
This pure-Python secp256k1 implementation is an executable mathematical reference
for formal soundness & completeness auditing. Because Python big-integer arithmetic
and nibble-table indexing are not constant-time, production wallet/prover nodes MUST
use constant-time field/group arithmetic (e.g., Rust `k256` or C `libsecp256k1`).
"""

RESEARCH_REFERENCE_ONLY = True

import hmac
import secrets
import hashlib
from typing import Dict, List, Optional, Tuple

P_CURVE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G_PT = (GX, GY)


def _modinv(a: int, m: int) -> int:
    return pow(a % m, -1, m)


def pt_add(p1: Optional[Tuple[int, int]], p2: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if (y1 + y2) % P_CURVE == 0:
            return None
        lam = (3 * x1 * x1 * _modinv(2 * y1, P_CURVE)) % P_CURVE
    else:
        lam = ((y2 - y1) * _modinv(x2 - x1, P_CURVE)) % P_CURVE
    x3 = (lam * lam - x1 - x2) % P_CURVE
    y3 = (lam * (x1 - x3) - y1) % P_CURVE
    return (x3, y3)


def pt_neg(p: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    return None if p is None else (p[0], (-p[1]) % P_CURVE)


def pt_sub(p1: Optional[Tuple[int, int]], p2: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    return pt_add(p1, pt_neg(p2))


def pt_mul(k: int, p: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    k %= N_ORDER
    if k == 0 or p is None:
        return None
    res = None
    cur = p
    while k:
        if k & 1:
            res = pt_add(res, cur)
        cur = pt_add(cur, cur)
        k >>= 1
    return res


def pt_ser(p: Optional[Tuple[int, int]]) -> str:
    if p is None:
        return "00" * 33
    return ("02" if (p[1] & 1) == 0 else "03") + f"{p[0]:064x}"


def pt_deser(hex_str: str) -> Optional[Tuple[int, int]]:
    if hex_str == "00" * 33:
        return None
    if len(hex_str) != 66 or hex_str[:2] not in ("02", "03"):
        raise ValueError("Invalid compressed secp256k1 point")
    x = int(hex_str[2:], 16)
    if not (0 <= x < P_CURVE):
        raise ValueError("Point X out of range")
    rhs = (pow(x, 3, P_CURVE) + 7) % P_CURVE
    y = pow(rhs, (P_CURVE + 1) // 4, P_CURVE)
    if (y * y) % P_CURVE != rhs:
        raise ValueError("Point not on curve")
    if (y & 1) != (0 if hex_str[:2] == "02" else 1):
        y = P_CURVE - y
    return (x, y)


def _derive_pedersen_h() -> Tuple[int, int]:
    ctr = 0
    while True:
        digest = hashlib.sha256(f"TFP_ZK_PEDERSEN_H_SECP256K1_V1:{ctr}".encode()).digest()
        x = int.from_bytes(digest, "big") % P_CURVE
        rhs = (pow(x, 3, P_CURVE) + 7) % P_CURVE
        y = pow(rhs, (P_CURVE + 1) // 4, P_CURVE)
        if (y * y) % P_CURVE == rhs:
            return (x, y if (y & 1) == 0 else P_CURVE - y)
        ctr += 1


H_PT = _derive_pedersen_h()


def _build_radix16_table(base: Tuple[int, int]):
    tbl = []
    cur = base
    for _ in range(64):
        row = [None]
        acc = None
        for d in range(1, 16):
            acc = pt_add(acc, cur)
            row.append(acc)
        tbl.append(row)
        for _ in range(4):
            cur = pt_add(cur, cur)
    return tbl


_G_TBL = _build_radix16_table(G_PT)
_H_TBL = _build_radix16_table(H_PT)


def pt_mul_fast(k: int, p: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    k %= N_ORDER
    if k == 0 or p is None:
        return None
    if p == G_PT or p == H_PT:
        tbl = _G_TBL if p == G_PT else _H_TBL
        res = None
        for i in range(64):
            nib = (k >> (4 * i)) & 0xF
            if nib:
                res = pt_add(res, tbl[i][nib])
        return res
    res = None
    cur = p
    while k:
        if k & 1:
            res = pt_add(res, cur)
        cur = pt_add(cur, cur)
        k >>= 1
    return res


def pedersen_commit(val: int, r: int) -> Optional[Tuple[int, int]]:
    return pt_add(pt_mul_fast(val, G_PT), pt_mul_fast(r, H_PT))


def hash_challenge(tag: str, points: List[Optional[Tuple[int, int]]]) -> int:
    h = hashlib.sha256()
    h.update(tag.encode("utf-8"))
    for p in points:
        h.update(bytes.fromhex(pt_ser(p)))
    return int.from_bytes(h.digest(), "big") % N_ORDER


class Transcript:
    """Stateful STROBE/Merlin-style Fiat-Shamir transcript binding all public parameters and commitments."""

    def __init__(self, domain: str):
        self._h = hashlib.sha256()
        self.absorb_bytes("domain", domain.encode("utf-8"))

    def clone(self) -> "Transcript":
        t = Transcript.__new__(Transcript)
        t._h = self._h.copy()
        return t

    def absorb_bytes(self, label: str, data: bytes) -> None:
        lb = label.encode("utf-8")
        self._h.update(len(lb).to_bytes(4, "big") + lb + len(data).to_bytes(4, "big") + data)

    def absorb_int(self, label: str, val: int) -> None:
        self.absorb_bytes(label, val.to_bytes(32, "big", signed=False))

    def absorb_point(self, label: str, p: Optional[Tuple[int, int]]) -> None:
        self.absorb_bytes(label, bytes.fromhex(pt_ser(p)))

    def challenge_scalar(self, label: str, points: List[Optional[Tuple[int, int]]]) -> int:
        t = self.clone()
        t.absorb_bytes("chal_tag", label.encode("utf-8"))
        for idx, p in enumerate(points):
            t.absorb_point(f"p{idx}", p)
        return int.from_bytes(t._h.digest(), "big") % N_ORDER


def prove_or_zero_tuple(
    branches: List[List[Optional[Tuple[int, int]]]],
    true_idx: int,
    true_rs: List[int],
    tag: str,
    tr: Optional[Transcript] = None,
) -> Dict:
    """1-of-K Sigma OR-Proof over conjunctions of zero commitments under a shared branch challenge."""
    k_b = len(branches)
    cs = [0] * k_b
    ss: List[List[str]] = [[] for _ in range(k_b)]
    all_As: List[Optional[Tuple[int, int]]] = []
    flat_targets = [pt for br in branches for pt in br]

    ks_true = [secrets.randbelow(N_ORDER - 1) + 1 for _ in branches[true_idx]]
    for j in range(k_b):
        if j == true_idx:
            all_As.extend([pt_mul_fast(km, H_PT) for km in ks_true])
        else:
            cs[j] = secrets.randbelow(N_ORDER)
            ss_j = [secrets.randbelow(N_ORDER) for _ in branches[j]]
            ss[j] = [hex(x) for x in ss_j]
            all_As.extend([pt_sub(pt_mul_fast(ss_j[m], H_PT), pt_mul_fast(cs[j], branches[j][m])) for m in range(len(branches[j]))])

    pts_in = flat_targets + all_As
    c_tot = tr.challenge_scalar(tag, pts_in) if tr is not None else hash_challenge(tag, pts_in)
    c_true = (c_tot - sum(cs)) % N_ORDER
    cs[true_idx] = c_true
    ss[true_idx] = [hex((ks_true[m] + c_true * (true_rs[m] % N_ORDER)) % N_ORDER) for m in range(len(branches[true_idx]))]
    return {"c": [hex(x) for x in cs], "s": ss}


def _parse_canonical_scalar(hex_str: str) -> int:
    if not isinstance(hex_str, str):
        raise ValueError("Scalar must be hex string")
    val = int(hex_str, 16)
    if not (0 <= val < N_ORDER):
        raise ValueError("Non-canonical scalar outside [0, N_ORDER)")
    return val


def verify_or_zero_tuple(
    branches: List[List[Optional[Tuple[int, int]]]],
    proof: Dict,
    tag: str,
    tr: Optional[Transcript] = None,
) -> bool:
    try:
        k_b = len(branches)
        cs = [_parse_canonical_scalar(x) for x in proof["c"]]
        if len(cs) != k_b or len(proof["s"]) != k_b:
            return False
        flat_targets = [pt for br in branches for pt in br]
        all_As: List[Optional[Tuple[int, int]]] = []
        for j in range(k_b):
            ss_j = [_parse_canonical_scalar(x) for x in proof["s"][j]]
            if len(ss_j) != len(branches[j]):
                return False
            for m in range(len(branches[j])):
                all_As.append(pt_sub(pt_mul_fast(ss_j[m], H_PT), pt_mul_fast(cs[j], branches[j][m])))
        pts_in = flat_targets + all_As
        c_tot = tr.challenge_scalar(tag, pts_in) if tr is not None else hash_challenge(tag, pts_in)
        return (sum(cs) % N_ORDER) == c_tot
    except Exception:
        return False


def prove_zero(P: Optional[Tuple[int, int]], r: int, tag: str, tr: Optional[Transcript] = None) -> Dict[str, str]:
    k = secrets.randbelow(N_ORDER - 1) + 1
    A = pt_mul_fast(k, H_PT)
    c = tr.challenge_scalar(tag, [P, A]) if tr is not None else hash_challenge(tag, [P, A])
    s = (k + c * (r % N_ORDER)) % N_ORDER
    return {"A": pt_ser(A), "s": hex(s)}


def verify_zero(P: Optional[Tuple[int, int]], proof: Dict[str, str], tag: str, tr: Optional[Transcript] = None) -> bool:
    try:
        A = pt_deser(proof["A"])
        s = _parse_canonical_scalar(proof["s"])
        c = tr.challenge_scalar(tag, [P, A]) if tr is not None else hash_challenge(tag, [P, A])
        return pt_mul_fast(s, H_PT) == pt_add(A, pt_mul_fast(c, P))
    except Exception:
        return False


def prove_or_zero(targets: List[Optional[Tuple[int, int]]], true_idx: int, true_r: int, tag: str, tr: Optional[Transcript] = None) -> Dict[str, List[str]]:
    res = prove_or_zero_tuple([[t] for t in targets], true_idx, [true_r], tag, tr=tr)
    return {"c": res["c"], "s": [row[0] for row in res["s"]]}


def verify_or_zero(targets: List[Optional[Tuple[int, int]]], proof: Dict[str, List[str]], tag: str, tr: Optional[Transcript] = None) -> bool:
    try:
        wrapped = {"c": proof["c"], "s": [[x] for x in proof["s"]]}
        return verify_or_zero_tuple([[t] for t in targets], wrapped, tag, tr=tr)
    except Exception:
        return False


def prove_nonneg(C_val: Optional[Tuple[int, int]], val: int, r_val: int, n_bits: int, tag: str, tr: Optional[Transcript] = None) -> Dict:
    if not (0 <= val < (1 << n_bits)):
        raise ValueError(f"Value {val} out of [0, 2^{n_bits}) range")
    bits, bit_or = [], []
    r_sum = 0
    for j in range(n_bits):
        b = (val >> j) & 1
        rj = secrets.randbelow(N_ORDER - 1) + 1
        Bj = pedersen_commit(b, rj)
        r_sum = (r_sum + (rj << j)) % N_ORDER
        bits.append(pt_ser(Bj))
        bit_or.append(prove_or_zero([Bj, pt_sub(Bj, G_PT)], b, rj, f"{tag}:b{j}", tr=tr))
    r_diff = (r_val - r_sum) % N_ORDER
    return {"B": bits, "bit_or": bit_or, "sum_zero": prove_zero(pt_mul_fast(r_diff, H_PT), r_diff, f"{tag}:sum", tr=tr)}


def verify_nonneg(C_val: Optional[Tuple[int, int]], proof: Dict, n_bits: int, tag: str, tr: Optional[Transcript] = None) -> bool:
    try:
        if len(proof["B"]) != n_bits or len(proof["bit_or"]) != n_bits:
            return False
        B_pts = [pt_deser(b_hex) for b_hex in proof["B"]]
        for j in range(n_bits):
            Bj = B_pts[j]
            if not verify_or_zero([Bj, pt_sub(Bj, G_PT)], proof["bit_or"][j], f"{tag}:b{j}", tr=tr):
                return False
        C_acc = None
        for Bj in reversed(B_pts):
            C_acc = pt_add(pt_add(C_acc, C_acc), Bj)
        return verify_zero(pt_sub(C_val, C_acc), proof["sum_zero"], f"{tag}:sum", tr=tr)
    except Exception:
        return False


class IssuerKeypair:
    """Trusted secp256k1 Schnorr attestation issuer keypair for authenticated event provenance."""

    def __init__(self, sk: int):
        if not (1 <= sk < N_ORDER):
            raise ValueError("Secret key must lie in [1, N_ORDER)")
        self.sk = sk
        self.pk = pt_mul_fast(sk, G_PT)
        self.pk_hex = pt_ser(self.pk)

    @classmethod
    def generate(cls) -> "IssuerKeypair":
        return cls(secrets.randbelow(N_ORDER - 1) + 1)


def _attestation_challenge(
    issuer_pk_pt: Tuple[int, int],
    R_pt: Tuple[int, int],
    account_id: str,
    seq_t: int,
    C_v_pt: Optional[Tuple[int, int]],
    C_e_pt: Optional[Tuple[int, int]],
) -> int:
    tr = Transcript("TFP-ATT-v1")
    tr.absorb_point("issuer_pk", issuer_pk_pt)
    tr.absorb_bytes("account_id", account_id.encode("utf-8"))
    tr.absorb_int("seq_t", int(seq_t))
    tr.absorb_point("C_v", C_v_pt)
    tr.absorb_point("C_e", C_e_pt)
    return tr.challenge_scalar("ATT:schnorr", [issuer_pk_pt, R_pt])


def sign_event_attestation(
    issuer: IssuerKeypair,
    account_id: str,
    seq_t: int,
    C_v: Optional[Tuple[int, int]],
    C_e: Optional[Tuple[int, int]],
) -> Dict[str, object]:
    if seq_t < 0:
        raise ValueError("seq_t must be non-negative")
    k = secrets.randbelow(N_ORDER - 1) + 1
    R = pt_mul_fast(k, G_PT)
    e = _attestation_challenge(issuer.pk, R, account_id, seq_t, C_v, C_e)
    s = (k + e * issuer.sk) % N_ORDER
    return {
        "scheme": "TFP-ATT-v1",
        "issuer_pk": issuer.pk_hex,
        "account_id": account_id,
        "seq_t": int(seq_t),
        "C_v": pt_ser(C_v),
        "C_e": pt_ser(C_e),
        "R": pt_ser(R),
        "s": hex(s),
    }


def verify_event_attestation(
    att: Dict[str, object],
    expected_issuer_pk: str,
    expected_account_id: str,
    expected_seq_t: int,
    expected_C_v_hex: str,
    expected_C_e_hex: str,
) -> bool:
    try:
        if att.get("scheme") != "TFP-ATT-v1":
            return False
        if att.get("issuer_pk") != expected_issuer_pk:
            return False
        if att.get("account_id") != expected_account_id:
            return False
        if int(att.get("seq_t", -1)) != int(expected_seq_t):
            return False
        if att.get("C_v") != expected_C_v_hex or att.get("C_e") != expected_C_e_hex:
            return False
        pk = pt_deser(str(att["issuer_pk"]))
        R = pt_deser(str(att["R"]))
        C_v_pt = pt_deser(expected_C_v_hex)
        C_e_pt = pt_deser(expected_C_e_hex)
        if pk is None or R is None:
            return False
        s = _parse_canonical_scalar(str(att["s"]))
        e = _attestation_challenge(pk, R, expected_account_id, int(expected_seq_t), C_v_pt, C_e_pt)
        return pt_mul_fast(s, G_PT) == pt_add(R, pt_mul_fast(e, pk))
    except Exception:
        return False


def compute_event_chain_tip(event_commit_pairs: List[Tuple[str, str]]) -> str:
    """Rolling SHA-256 chain tip over attested (C_v, C_e) commitments (zero private S_t dependency)."""
    h = hashlib.sha256(b"TFP-EVENT-CHAIN-GENESIS").digest()
    for seq_t, (cv_hex, ce_hex) in enumerate(event_commit_pairs):
        h = hashlib.sha256(
            h + int(seq_t).to_bytes(8, "big") + bytes.fromhex(cv_hex) + bytes.fromhex(ce_hex)
        ).digest()
    return h.hex()


def _stream_head_challenge(
    issuer_pk_pt: Tuple[int, int],
    R_pt: Tuple[int, int],
    account_id: str,
    total_events: int,
    epoch_id: int,
    events_chain_tip_hex: str,
) -> int:
    tr = Transcript("TFP-HEAD-v2")
    tr.absorb_point("issuer_pk", issuer_pk_pt)
    tr.absorb_bytes("account_id", account_id.encode("utf-8"))
    tr.absorb_int("total_events", int(total_events))
    tr.absorb_int("epoch_id", int(epoch_id))
    tr.absorb_bytes("events_chain_tip", bytes.fromhex(events_chain_tip_hex))
    return tr.challenge_scalar("HEAD:schnorr", [issuer_pk_pt, R_pt])


def sign_stream_head(
    issuer: IssuerKeypair,
    account_id: str,
    total_events: int,
    epoch_id: int,
    events_chain_tip_hex: str,
) -> Dict[str, object]:
    if total_events <= 0 or epoch_id < 0 or len(events_chain_tip_hex) != 64:
        raise ValueError("Invalid stream-head parameters")
    k = secrets.randbelow(N_ORDER - 1) + 1
    R = pt_mul_fast(k, G_PT)
    e = _stream_head_challenge(issuer.pk, R, account_id, total_events, epoch_id, events_chain_tip_hex)
    s = (k + e * issuer.sk) % N_ORDER
    return {
        "scheme": "TFP-HEAD-v2",
        "issuer_pk": issuer.pk_hex,
        "account_id": account_id,
        "total_events": int(total_events),
        "epoch_id": int(epoch_id),
        "events_chain_tip": events_chain_tip_hex,
        "R": pt_ser(R),
        "s": hex(s),
    }


def verify_stream_head(
    head: Dict[str, object],
    expected_issuer_pk: str,
    expected_account_id: str,
    expected_total_events: int,
    expected_min_epoch: int,
    expected_events_chain_tip_hex: str,
) -> bool:
    try:
        if head.get("scheme") != "TFP-HEAD-v2":
            return False
        if head.get("issuer_pk") != expected_issuer_pk or head.get("account_id") != expected_account_id:
            return False
        if int(head.get("total_events", -1)) != int(expected_total_events) or int(expected_total_events) <= 0:
            return False
        epoch_id = int(head.get("epoch_id", -1))
        if epoch_id < int(expected_min_epoch):
            return False
        if head.get("events_chain_tip") != expected_events_chain_tip_hex:
            return False
        pk = pt_deser(str(head["issuer_pk"]))
        R = pt_deser(str(head["R"]))
        if pk is None or R is None:
            return False
        s = _parse_canonical_scalar(str(head["s"]))
        e = _stream_head_challenge(pk, R, expected_account_id, int(expected_total_events), epoch_id, expected_events_chain_tip_hex)
        return pt_mul_fast(s, G_PT) == pt_add(R, pt_mul_fast(e, pk))
    except Exception:
        return False


class FurnisherAuthority:
    """
    Isolated Data-Furnisher Signing Authority (3-Party Separation):
    Holds `sk_issuer`, commits & signs individual `(V_t, E_t)` events plus the
    event-commitment chain tip `TFP-HEAD-v2`, and NEVER sees or computes `S_t`.
    """

    def __init__(self, keypair: Optional[IssuerKeypair] = None, handle_blinding_key: Optional[bytes] = None):
        self._kp = keypair if keypair is not None else IssuerKeypair.generate()
        self._handle_key = handle_blinding_key if handle_blinding_key is not None else secrets.token_bytes(32)
        if len(self._handle_key) < 32:
            raise ValueError("Handle blinding key must be >= 256 bits (32 bytes)")

    @property
    def pk_hex(self) -> str:
        return self._kp.pk_hex

    def issue_signed_event_bundle(
        self,
        account_secret: str,
        verifier_id: str,
        epoch_id: int,
        events_ve: List[Tuple[float, float]],
        scale: int = 1_000_000_000,
    ) -> Dict[str, object]:
        # High-entropy 256-bit HMAC blinding prevents offline dictionary/rainbow-table handle correlation
        acct_handle = hmac.new(
            self._handle_key,
            f"TFP-PSEUDO-v2:{verifier_id}:{epoch_id}:{account_secret}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()[:32]
        opened_events = []
        attestations = []
        commit_pairs = []
        for idx, (v_val, e_val) in enumerate(events_ve):
            v_f = int(round(v_val * scale))
            e_f = int(round(e_val * scale))
            r_v = secrets.randbelow(N_ORDER - 1) + 1
            r_e = secrets.randbelow(N_ORDER - 1) + 1
            C_v = pedersen_commit(v_f, r_v)
            C_e = pedersen_commit(e_f, r_e)
            opened_events.append({"v": v_val, "e": e_val, "r_v": r_v, "r_e": r_e})
            attestations.append(sign_event_attestation(self._kp, acct_handle, idx, C_v, C_e))
            commit_pairs.append((pt_ser(C_v), pt_ser(C_e)))
        tip = compute_event_chain_tip(commit_pairs)
        stream_head = sign_stream_head(self._kp, acct_handle, len(events_ve), epoch_id, tip)
        return {
            "account_id": acct_handle,
            "epoch_id": int(epoch_id),
            "opened_events": opened_events,
            "attestations": attestations,
            "stream_head": stream_head,
        }

