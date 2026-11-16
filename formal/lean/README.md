# Trust Stack — Lean 4 Formal Verification

Machine-checked verification of the core formal claims of the GTT layer of the
Trust Stack papers (companion to `papers/source/gtt.tex` in this repository).

## Status: VERIFIED — green build & `leanchecker` kernel replay (v4.5.0, November 2026)

**The library compiles green against the pinned toolchain.** Build record:
Lean `4.35.0` (`leanprover/lean4:v4.35.0`) with Mathlib4 pinned in
`lake-manifest.json`; `lake build TrustStack` and kernel replay via
`lake env leanchecker TrustStack.Tilt` and `lake env leanchecker TrustStack.MasterLaw`
completed with zero errors. The sources contain **no `sorry` placeholders**,
and `Check.lean` (`lake env lean Check.lean`) audits all **36 theorems**
(recorded in `VERIFICATION_AXIOMS.txt`): every theorem depends solely on
the standard classical axioms `[propext, Classical.choice, Quot.sound]`,
including clamped `[0, 1]` invariance (`masterStepClamped_mem_unit`,
`trajClamped_mem_unit`, `clamp_unit_lipschitz`) and non-commutativity
(`masterStepClamped_not_comm`). No `sorryAx` appears anywhere.

## What is proved, and where it maps to the paper

| Lean theorem | Paper statement (GTT) |
|---|---|
| `TrustStack.tiltP_pos`, `TrustStack.tiltP_sum` | Property 1: the tilted vector P̃ is a probability vector (positivity, normalization) |
| `TrustStack.tiltP_neutral` | Property 2: neutral reduction — at ι = 0, P̃ = P and eq:eu reduces to standard expected utility |
| `TrustStack.EU_mono` | Property 3: monotone optimism — tilted EU is nondecreasing in the trust index ι (integrated form of dEU/dι ≥ 0; proved elementarily by double-sum symmetrization, no differentiation machinery) |
| `TrustStack.tilt_log_bound` | Property 4: bounded distortion — \|log(P̃(o)/P(o))\| ≤ \|γι\|·(max U − min U), the sharp form of the printed looser bound 2γ·max\|û\| at \|ι\| ≤ 1 |
| `TrustStack.masterStep_physics` | §2.2: the physics-layer preset of the master law (eq:masterlaw) is exactly the Rescorla–Wagner stability axiom (eq:stability) |
| `TrustStack.contraction` | Leak stability: zero-input state decays geometrically to baseline, (1 − δ)^t |
| `TrustStack.input_bound`, `TrustStack.bibo`, `TrustStack.bibo_of_eps_bound` | Bounded-input bounded-state stability: \|S_t − S_base\| ≤ (1 − δ)^t·\|S₀ − S_base\| + (λ⁺+λ⁻)·E/δ for \|ε\| ≤ E, r ∈ [0,1] |

## Build

```bash
# 1. Install elan (Lean version manager), if not present:
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh

# 2. From this directory:
lake exe cache get   # download prebuilt Mathlib cache (pinned toolchain)
lake build           # verify all proofs
```

A green `lake build` verifies every claim in the table above against the
pinned toolchain (`lean-toolchain`). The stronger audit is
`lake env lean Check.lean`, which prints the axiom basis of each theorem
(expect `[propext, Classical.choice, Quot.sound]` for all ten; the recorded
output is `VERIFICATION_AXIOMS.txt`). Nothing else in the repository depends
on this directory; it is an audit artifact.

## Scope note

The formalization covers the finite-outcome tilt and the discrete-time master
law as printed. It does not (yet) cover the OU/ψ observation-drift theory of
TFP §4 (needs SDE infrastructure beyond Mathlib's current scope) or the
numerical simulation batteries (those are code-verified, not proof-verified,
and live in `technical-appendix/`).
