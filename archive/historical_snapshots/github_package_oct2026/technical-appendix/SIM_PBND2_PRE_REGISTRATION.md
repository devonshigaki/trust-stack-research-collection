# SIM-PBND-2 — Pre-registration (robustness battery)

**Registered:** 2026-09-21, before any data contact for this run.
**Seed:** 20260921. **Status:** criteria frozen below; no amendment permitted
without disclosure in this document before the amended analysis runs.

## Relation to SIM-PBND

SIM-PBND (seed 20260920, compound PASS 4/4) established the in-silico
perturbation signature at one scale (20 subjects, 12 units) and one
perturbation level. SIM-PBND-2 is the robustness battery: scale-up,
dose-response, specificity control, and recovery. The third-party scoring of
DOCAS §5.8 remains post-hoc regardless of this run's outcome; this battery
strengthens the prospective (in-silico, registered) evidence arm only.

## Model (same harness family as SIM-PBND v3c, scaled)

- 40 subjects; each a 24-unit network of master-law trust units.
- Subject-specific symmetric coupling matrix W_s (random, spectral-radius
  normalized), AR(2) intrinsic colored dynamics per unit, shared sensory OU
  input (one realization, common across subjects), sensory noise σE.
- Unit update: x(t+1) = g·(AR(2) intrinsic + κ·W x(t)) + (1−g)·(ξ(t) + σE·η(t)),
  with ξ the shared OU sensory stream and η iid unit noise.
- Perturbation = prior-weight relaxation g: 0.90 → {0.45, 0.20, 0.05} (dose
  levels); σE fixed at 0.02 for dose-response.
- Specificity control: sensory-channel perturbation σE: 0.02 → σE*, with g held
  at 0.90; σE* calibrated on a separate 10-subject calibration batch (not part
  of the 40 scored subjects) so the within-subject FC drop matches the g=0.05
  condition to within ±5 percentage points.
- Recovery: after the g=0.05 epoch, g restored to 0.90 for an equal-length
  recovery epoch; FC recomputed over the recovery window.
- T = 2000 samples per epoch after 500-sample burn-in. FC = Pearson
  correlation matrix across units. Similarity = normalized Frobenius
  similarity 1 − ||A−B||_F/||A||_F (the v3c metric). Identifiability =
  nearest-neighbor run matching (Frobenius) of perturbed FCs to baseline FCs.

## Frozen criteria (compound verdict requires all four)

- **C1 (replication at scale):** within-subject FC similarity (baseline vs
  g=0.05) drops ≥ 30% relative to baseline split-half reliability, at 40
  subjects / 24 units.
- **C2 (dose-response):** between-subject FC similarity increases
  monotonically with perturbation strength across the four g levels;
  Spearman ρ ≥ 0.8 (subject-mean level), one-sided p < 0.05.
- **C3 (specificity):** the between-subject convergence increase under
  prior-precision perturbation (g=0.05) is ≥ 2× that under the matched
  sensory-channel perturbation, and the difference is significant
  (two-sided p < 0.05 across subjects).
- **C4 (recovery):** after restoration, within-subject similarity to own
  baseline recovers to ≥ 70% of baseline split-half reliability (median
  across subjects).

## Reporting commitments

Compound verdict PASS requires C1–C4. Any criterion's failure is reported,
never dropped; INDETERMINATE is a reportable outcome. A first-run artifact is
preserved if the harness faults (`sim_pbnd2_firstrun_bug.json`). Results to
`sim_pbnd2_results.json`.


## Amendment A1 (2026-09-21, disclosed before the main batch was run)

The calibration batch (10 subjects, never scored) shows the sensory-noise
control specified in C3 is infeasible in this model family: at g = 0.90 the
sensory term carries weight 0.10, and no σE in the grid {0.05 … 0.30}
reproduces the within-subject FC dissolution of the prior-relaxation
condition (drops −0.04…−0.02 vs 1.05). The sensory channel cannot mimic
prior-precision relaxation at any tested noise level — itself a specificity
datum, reported as such.

C3 is therefore amended to a two-control specificity test, same thresholds:
the between-subject convergence increase under shared-sensory prior
relaxation (g = 0.05) must be ≥ 2× that under EACH of
  (a) the sensory-noise control at σE = 0.30 (grid maximum), g = 0.90; and
  (b) a subject-specific-sensory control: g = 0.05 with INDEPENDENT OU
      sensory streams per subject (same σE = 0.02) — dissociating
      convergence (shared-stream dominance) from decoherence (intrinsic
      suppression);
with the difference significant across subjects (two-sided p < 0.05).
Criteria C1, C2, C4 are untouched. Calibration code, grid values, and the
calibration batch seed (20260921+777) are recorded with the run.


---

## RESULTS (appended after the run, 2026-09-21)

Main batch executed as registered (seed 20260921; 40 subjects × 24-unit
networks; Amendment A1 applied). Full machine-readable record:
`numbers/sim_pbnd2_results.json`. Verdicts against the frozen criteria:

| Criterion | Frozen threshold | Result | Verdict |
|---|---|---|---|
| C1 replication-at-scale (within-subject drop) | ≥ 0.30 | 1.127 | **PASS** |
| C2 dose-response (Spearman across 4 g-levels) | ρ ≥ 0.8, p < 0.05 | ρ = 1.0 (asymptotic p < 0.05) | **PASS** |
| C3 specificity (≥ 2× vs EACH A1 control, p < 0.05) | ≥ 2× both | vs sensory-noise: ratio unbounded, p = 1.8×10⁻¹²; vs subject-specific-sensory: **1.0×** | **FAIL** |
| C4 recovery (median fraction) | ≥ 0.70 | 1.000 | **PASS** |

**COMPOUND VERDICT: FAIL (3/4).**

Identifiability: 100% → 2.5%.

The C3 failure is instrument-level and substantive: at full prior collapse
(g = 0.05) the dynamics are dominated by the sensory stream, and ANY single
dominant stream — shared or subject-specific — homogenizes the correlation
FC matrices toward identity (convergence increase 1.328 vs 1.329). The
normalized-Frobenius similarity metric cannot see stream identity. The
convergent appearance of the fully collapsed state is single-driver
homogenization, not convergence on a shared reality.

C2 supplementary (computed after the frozen battery, labeled as such in the
results JSON): at n = 4 levels the exact permutation floor is p = 1/12 ≈
0.083 for any outcome, so the frozen p < 0.05 clause is satisfiable only
under the asymptotic test (as recorded); the powered read is the
subject-level trend across 160 subject–dose pairs (|ρ| = 0.968, p =
4.7×10⁻⁹⁷).

Exploratory follow-ups (run after the battery, labeled post-battery; not
scored against criteria):

- E1 shared vs independent sensory streams at PARTIAL relaxation (g = 0.65,
  0.55, 0.45): convergence metric still cannot distinguish stream identity
  (0.988 vs 0.990 at g = 0.65) — the instrument limitation is not confined
  to total collapse.
- E2 fine dose grid: sharp threshold-like transition between g = 0.90
  (−0.36) and g = 0.75 (0.794), consistent with the "organized state
  transition" reading of DOCAS §5.8 component (a).

Interpretation recorded with the run: the discriminating content of the
perturbation signature is the fingerprint decoherence (C1) and the
dose-graded transition (C2/E2), not between-subject convergence at full
collapse. This constrains the human-side reading of DOCAS §5.8 component
(b): FC-level convergence is the expected instrument signature of any
dominant-driver state; the fingerprint loss carries the identifying weight.

No first-run bug artifact for SIM-PBND-2 (`firstrun_bug = null` in the
results JSON — the harness was the debugged SIM-PBND lineage).
