# SIM G22 — Closure note
**Date:** 2026-09-13 · **Spec:** SIM_G22_PRE_REGISTRATION.md (frozen before data) · **Results:** technical-appendix/numbers/g22_results.json · **Code:** technical-appendix/sim-code/g22_reality_monitoring.py

## Audit trail (disclosed, per collection convention)

**First run failed the C1 instrument gate** — 0/60 trajectories inside the band, distance *increasing* (0.4232 → 0.4472). Diagnosis: implementation bug, not a spec problem — ICs were drawn `Dirichlet(ones(4))` with T\* = `full(4, 0.2)`, which is off-manifold (sums to 0.8); the frozen spec's Δ⁴ is the 4-dimensional simplex = **5** stage components (uniform 0.2 × 5, as printed in GTT §3.6). The frozen spec was not altered; the code was repaired to match it, and the buggy run is retained unchanged as `g22_firstrun_bug.json` (same convention as the original battery's `*_firstrun_bug.json` files). All numbers below come from the repaired run.

## Frozen-criterion outcomes (repaired run, seed 20260913)

| Criterion | Frozen rule | Observed | Verdict |
|---|---|---|---|
| **C1** instrument gate | Arm 0: 60/60 inside d_H < 0.05 at step 7 | 60/60 (mean 0.284 → 0.013 at step 7; ≈0.000 at step 25) | **PASS** |
| **C2** corruption (primary) | Arm A d̄₂₅(T\*) > 0.05 at μ_v = 2.5 and 5.0; capture ⟨d(θ₂₅,E)⟩ < ⟨d(θ₂₅,T\*)⟩ at 5.0 | 0.197 and 0.229 (both > 0.05); capture holds at 5.0 | **PASS** |
| **C3** stagnation | Arm A at μ_v = 1.25: no-update fraction ≥ 50% and d̄₂₅ > 0.05 | 57% no-update; d̄₂₅ = 0.249 | **PASS** |
| **C4** sparse hallucination | Arm B at 5.0: imagination-driven updates ≥ 10%; capture | 48% imagination-driven; capture holds | **PASS** |
| **C5** aggregation rescue | Arm C at 5.0: d̄₂₅ ≤ 0.05 and dispersion ratio ≤ 1.25× Arm 0 | d̄₂₅ = 0.079 — attenuated ≈2.9× vs ungated (0.229) but **outside the band** | **FAIL** |
| **C6** collective-illusion boundary | Arm D at 5.0: rescue fails under shared expectation | d̄₂₅ = 0.239 ≈ ungated single-channel level | **PASS** |

**Compound headline (C1 ∧ C2 ∧ C5 ∧ C6): FAIL** — because C5 failed. Reported as such; nothing dropped.

## What this establishes (and what it does not)

- **Established in silico:** under the Dijkstra–Fleming source-mixing model of perceptual reality monitoring, expectation imagery intermixed with outcome perception corrupts trust-stage convergence at empirically normal imagery strengths (μ_v = 2.5 is the population mean of the vividness distribution in the source study). Both predicted failure modes occur: capture by expectation at high vividness (update target pulled toward E) and explained-away stagnation at low vividness (genuine evidence attributed to self, no update). Under sparse outcomes, roughly half of all updates at high vividness are driven by hallucinated outcomes (imagery alone crossing the reality threshold). Aggregating k = 8 independent channels attenuates the corruption ≈2.9× but does not restore band-level convergence; under correlated (shared) expectations the aggregation defense collapses entirely — the sim's formalization of a collective illusion.
- **Not established:** anything about human trust dynamics empirically. The vividness distribution and threshold are imported from a visual-perception study; λ = 0.35 is planted; the rescue boundary depends on E ~ Dirichlet(1) idiosyncrasy. The registered GTT empirical program (§6) is where a human analog would be tested; vividness/imagery covariates now have a stated reason to be measured there.

Distance convention: Hellinger chord, matching the printed G6-M1 values.
