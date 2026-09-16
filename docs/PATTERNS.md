# Cross-Simulation Pattern Analysis — what the batteries say when read against each other

**Scope:** every simulation family in the deposit — GTT (G1–G22 + robustness
SIM-R1/R2, B3–B7), TFP (P1–P8), DOCAS (D-series genetics, F1 fly series, H1
mouse, D8–D13 linguistic/cortical batteries, N.3 encoding), whitepaper
(W-series, benefit ledger). Verdicts are the frozen-criterion verdicts as
printed in the papers and closure documents. Nothing here re-grades anything.

## The ledger (headline verdicts)

| Family | Verdicts |
|---|---|
| GTT core dynamics (G1–G21, fixed references) | verified in silico (convergence, noise floors, OU statistics, long-run, λ-battery) |
| G6-M1 manifold re-implementation | 60/60 replicas, d̄₀ = 0.284 — verdict reproduces |
| G22 reality monitoring | **compound FAIL** (C5 FAIL; C1–C4, C6 PASS) — published |
| SIM-R1 b1 (estimator misspecification) | prior certification circular in the registered way — disclosed |
| SIM-R1 b2 (ringing closures) | **qualitatively robust, quantitatively closure-fragile** |
| SIM-R2 B3 (reference scales) | relational conclusions robust |
| SIM-R2 B4 (sparse topologies) | R > 0.7 **fails** below ⟨k⟩ ≈ 25 — published boundary |
| SIM-R2 B5/B7 (24-test multiplicity; Simpson check) | Bonferroni 9/24; no Simpson reversal |
| TFP P1 / P1b / P1c | SUPPORTED / leakage-fragility band ℓ* ∈ [0.02, 0.10] / sparsity boundary |
| TFP P2, P3 | SUPPORTED *conditional on breach*; scaling-form only |
| TFP P4a/P4b | SUPPORTED with caveat; footprint negligible, lower-powered null preserved |
| TFP P5 | SUPPORTED in the statistical sense only (floor-adjacent; **no ratio headline**) |
| TFP P6 | structural argument; no cascade model — stated as a gap |
| TFP P7 / P8 | SUPPORTED with caveat / Sybil asymmetry priced; attack surfaces disclosed |
| DOCAS F1 series (fly) | gate PASS; F1a INDETERMINATE-instrument; **F1a2 FAIL**; **F1b PASS** (7/7 as frozen; 6–7 floor-saturation artifact disclosed) |
| DOCAS H1 (mouse) | **compound FAIL** (A1 FAIL; A2 MET 8/11; H1-B non-abolition 1.340 vs retention ≥0.50 MET) |
| DOCAS D-series / D8–D13 / N.3 | mixed: category-level encodings PASS; exact retrieval, Procrustes, point-mapping NULL/fail; D13 PASS after the registered stimulus-class fork |
| H01 (human) | pre-registered, **in progress** under the same frozen criteria |

## Pattern 1 — Dynamical-law claims survive; structural-transport claims fail

The update-law machinery verifies wherever it is tested on its own equations:
convergence, noise floors, stationary statistics, long-run recovery, λ
recovery, coherence onset. The failures cluster where a **specific structure**
is asked to transport: the fly's single-class budget dominance does not exist
in mouse cortex (H1-A1 FAIL); Kuramoto coherence at the operating point does
not survive network sparsification below ⟨k⟩ ≈ 25 (B4/P1c); the imagery
rescue fails when expectations are shared (G22 arm D). **The law is portable;
the wiring is not.** The papers now say exactly this (the H1 verdict's "the
single-class structural basis does not transfer" clause).

## Pattern 2 — Distributed/relational readouts pass; point-to-point mappings fail

Category-level and ridge-encoding tests pass (CLICS densities, N.3 mean-vertex
encoding, D13 after the fork, the LLaMA→eng1000 bridge). Exact retrieval
(top-1 = NULL), Procrustes alignment (NULL), second-encoder decode (NULL),
and single-word cortical/embedding Mantels (NULL) fail. This is why the
whitepaper's bridging design uses representational similarity analysis and
explicitly claims **no point-to-point translation** — the batteries
established that boundary before the application leaned on it.

## Pattern 3 — Floors and ceilings generate artifacts; the discipline catches them

F1b criteria 6–7 met at a floor-saturation value → disclosed as a calibration
artifact, evidential weight moved to criteria 1–5. P5 magnitudes floor-adjacent
→ no ratio headline, re-run registered. G1(b) convergence sits at the 1/√N
finite-size floor → printed as the floor, not as perfect coherence. The
N.3 category-LOO pass → artifact-flagged by its own semantic-only control
(templatic lexicon). **Repeated pattern: the frozen criteria plus the
artifact-hunting batteries convert silent overclaims into disclosed
limitations.**

## Pattern 4 — Quantitative signatures are closure-fragile; qualitative ones are not

The betrayal-ringing period drifts 7.2 → 17.7 steps across smoothing closures
and vanishes under zero-delay closure (GTT §6; SIM-R1 b2: "qualitatively
robust, quantitatively closure-fragile"). G22's corruption grows with imagery
vividness only under sparse outcomes. Consequence printed in the papers: tests
must verify the closure or joint-fit (λ, α) — the theory commits to
**relational** predictions (underdamped vs not; ordering of arms) and refuses
point predictions where the instrument under-determines them.

## Pattern 5 — Marginal results fail under family-wise discipline, and the prose already knew

In the 24-test family: Bonferroni 9/24, BH 13/24; the two weakest
("adjacency" 0.061, "D8 EN paraphrase" 0.046) fail even BH — and those are
exactly the claims the papers had already hedged as "weakly present" and
"marginal." Five of the BH survivors are post-hoc assemblies and are labeled
as such. **The hedging in the prose and the statistics agree** — the
epistemic labels are calibrated, not decorative.

## Pattern 6 — INDETERMINATE is doing work

F1a (instrument), D-series nulls, and the H1-A2/verdict asymmetry show the
three-state system functioning: instrument failures trigger amendments rather
than re-graded passes (F1a2 amendment; F1b appetitive re-run registered), and
mixed outcomes (H1: A1 FAIL / A2 MET / H1-B MET → compound FAIL on the frozen
composition rule) are reported as the composition, not cherry-picked.

## What this means for a reviewer

Read the collection as two claims with different evidence grades:
(1) a **dynamical measurement law** — heavily verified in silico, with its
boundaries (sparsity, leakage, closure, floors) mapped and printed;
(2) **structural instantiations** — biological and topological — which are
hypothesis-grade where the batteries have not confirmed transport, and which
the papers label accordingly. The failure record (G22, F1a2, H1, B4, the
24-test family) is not a weakness of the package; it is the mechanism by
which the surviving claims earn their labels.
