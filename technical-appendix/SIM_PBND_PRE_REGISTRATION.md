# SIM-PBND — Pre-Registration (frozen before execution)

**Date frozen:** 2026-09-20 · **Status:** registered BEFORE any run · **Scope:** in-silico arm of DOCAS §5.8 (boundary-dissolution prediction P-BND) · **Seed:** 20260920 (all generators)

## Question
Does relaxing prior precision in a network of master-law trust units produce, *as an organized state transition* (not noise): (a) decoherence of subject-specific functional-connectivity fingerprints, (b) convergence of subjects toward a common configuration, and (c) increased scale-invariant (fractal) organization of network-level activity — the in-silico counterpart of the Siegel et al. (2024) and Varley et al. (2020) perturbation signature scored in DOCAS §5.8?

## Model (frozen)
- K = 20 subjects. Each subject: N = 12 units, state Sᵢ(t) updated by the stack master law
  `Sᵢ(t+1) = Sᵢ(t) + λᵢ·εᵢ(t) − δ(Sᵢ(t) − S_base)` with subject-specific λᵢ ~ U(0.10, 0.40), δ = 0.02, S_base = 0.5.
- Prediction error εᵢ(t) = Vᵢ(t) − Eᵢ(t), where expectation E(t) is carried by a subject-specific top-down prior coupling matrix W (symmetric, spectral radius scaled to 0.6, entries N(0,1) then symmetrized and scaled) and validation V(t) is a common sensory stream (shared OU drive, θ = 0.3, σ = 0.25) plus unit noise.
- **Baseline condition:** prior weight g = 1.0, expectation process noise σ_E = 0.02.
- **Perturbation condition (5-HT2A-like):** prior weight g = 0.2 (relaxed priors), expectation process noise σ_E = 0.12; sensory channel untouched (same OU parameters, same input gain).
- T = 4,000 steps per run; first 1,000 discarded. Two runs per subject per condition (different noise draws) for fingerprinting.
- Functional connectivity (FC) = 12×12 Pearson correlation matrix of unit activity, per subject/run/condition.

## Frozen criteria (PASS/FAIL per criterion; no amendment after execution)
- **C1 — fingerprint decoherence:** median within-subject FC similarity (Spearman of upper triangles, run-1 vs run-2) under perturbation drops ≥ 30% relative to baseline.
- **C2 — convergence:** median between-subject FC similarity increases under perturbation (paired Wilcoxon, p < 0.05), AND run-matching identifiability (fraction of subjects whose run-2 FC is best matched by their own run-1) falls from ≥ 90% baseline to ≤ 50% perturbed.
- **C3 — scale-free reorganization:** Higuchi fractal dimension (k_max = 8) of the network-mean activity increases under perturbation (paired Wilcoxon, p < 0.05). Per-unit (signal-level) FD reported separately with no criterion — mirroring the disclosed Varley signal-level null trend.
- **C4 — organized transition, not noise:** the perturbed FC is not white desynchronization — leading-to-second eigenvalue ratio (λ₁/λ₂) of the mean perturbed FC exceeds the 95th percentile of a phase-randomized null (200 surrogates).

## Compound verdict
PASS = C1 ∧ C2 ∧ C3 ∧ C4. Any criterion failing is reported as failing; INDETERMINATE outcomes are reported, not dropped.

## Falsification
If prior-precision relaxation does not produce the fingerprint/convergence/fractal signature in this model, the in-silico arm of §5.8 FAILS and is reported as such; the §5.8 scoring of the human studies is unaffected (different evidence class).
