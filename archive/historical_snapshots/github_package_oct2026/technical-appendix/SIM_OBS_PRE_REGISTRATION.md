# SIM-OBS — Pre-Registration (frozen before execution)

**Date frozen:** 2026-09-20 · **Status:** registered BEFORE any run · **Scope:** simulation arm of TFP §4 (Observation Distortion as an Engineering Constraint) and whitepaper §1.4 · **Seed:** 20260920

## Question
Does central observation of validation events measurably distort the very trust dynamics being measured, and does zero-knowledge verification remove that distortion? This is the in-silico form of the surveillance-bias argument (whitepaper §1.4; TFP §4): observed behavior is distorted behavior.

## Model (frozen)
- Cohort: M = 500 agents, master-law dynamics `S(t+1) = S(t) + λᵢ·ε(t) − δ(Sᵢ(t) − S_base)`, λᵢ ~ U(0.05, 0.60), δ = 0.01, S_base = 0.5, T = 2,000 steps.
- Ground-truth event stream: mixed-sign ε ~ N(0.02, 0.30) (mild positive drift), identical across conditions (same seed).
- **CENTRAL condition (surveillance):** agents know events are centrally observed and temper negative validations: reported ε' = ε·(1 − hᵢ) for ε < 0, hᵢ ~ U(0.10, 0.40); plus reporting noise σ = 0.05 on all events. This operationalizes demand-characteristics/hedging under observation.
- **ZK condition:** events verified without observation (cryptographic attestation stand-in); reported stream = ground truth + instrument noise σ = 0.02 only; no behavioral modification.
- Estimation: the stack's standard Kalman/EM estimator (Sim-W1 spec) recovers λ̂ and the trust trajectory Ŝ(t) from the reported stream.

## Frozen criteria (50 cohorts, seed-stratified)
- **C1 — distortion exists under surveillance:** CENTRAL estimate of mean terminal trust E[S(T)] is biased high (positive bias) with median bias ≥ +0.03 relative to ground truth (the hedged stream makes agents look more trust-stable than they are).
- **C2 — ZK removes it:** ZK median absolute bias of E[S(T)] ≤ 0.01.
- **C3 — the gap is systematic:** CENTRAL bias − ZK bias > 0 in ≥ 48/50 cohorts (sign test p < 0.001).
- **C4 — estimator integrity unaffected structurally:** λ̂ recovery error (ZK condition) matches Sim-W1 tolerances (p95 ≤ 0.15) — the distortion is behavioral, not instrumental.

## Compound verdict
PASS = C1 ∧ C2 ∧ C3 ∧ C4. Failures and INDETERMINATE outcomes are reported, never dropped.
