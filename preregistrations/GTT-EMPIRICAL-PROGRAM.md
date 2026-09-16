# GTT-EMPIRICAL-PROGRAM — Pre-Registration (Skeleton Draft)

**Registration type:** OSF "Pre-Data Collection Registration" (deposit pending; OSF DOI to be assigned).
**Source:** Extracted from *The General Theory of Trust* (gtt_revised.md) §6 "Proposed Empirical Program" — the prospective-studies section of the theory paper. All hypotheses below are stated in their current, post-repair form.
**Self-attestation status:** internally specified and timestamped in this deposit; external OSF registration pending. Until this registration exists, all pre-registration and frozen-criteria claims referenced here are self-attested by the author. This deposit replaces that caveat once the OSF DOI is assigned.

---

## 1. Hypotheses

**R1 (registered program hypothesis — stability law).** In repeated-interaction data with recorded expectations and outcomes, ΔS_t (operationalized via the DOCAS stage markers) follows the stability law S_t = S_{t−1} + λ·ε(t−1) with subject-specific λ_i, with ε in the stack-wide V − E convention. Distinct from the theory paper's §1.1 hypothesis H1.

**H2 (target coefficient).** The population mean trust-sensitivity is pre-registered as the target μ_λ = 0.61 with an equivalence corridor [0.46, 0.76].
- 0.61 is a *target hypothesis*, not an estimate, not a derived quantity, and not a universal constant; no derivation of its value is claimed. The simulation battery shows no dynamical feature at 0.61.
- The corridor half-width 0.15 is a pre-registered smallest effect size of interest (SESOI) — a substantive choice, not instrument resolution (the estimator pipeline's demonstrated recovery error is far finer: mean 0.0074, p95 0.0215, max 0.0343; ultra-thin worst case 0.0737). Corridor corroboration is therefore *weak evidence*; the primary test is the model comparison in §5.

**H2a (measurement invariance).** λ̂ is equal across domains (financial, social, physiological) after dimensionless normalization (Definition 2a), up to the corridor.

**H2b (rank-order stability).** The ordering of individuals' λ_i is stable across domains and across repeated measurement windows, even if levels drift.

**Closed-loop behavioral prediction (from Sim G8).** Under the minimal loop closure E_{t+1} = S_t the dynamics reduce to x_{t+2} = x_{t+1} − λx_t: stable iff 0 < λ < 1, critically damped at λ* = 1/4, underdamped above it. Following signed mismatch events, S should overshoot and oscillate with period P(λ̂) = 2π/atan(√(4λ̂−1)) (≈ 7.2 steps at λ = 0.61), decaying at √λ̂ per step. Closure-conditional (SIM-R1 battery 2): under exponential-smoothing closures E_{t+1} = αS_t + (1−α)E_t the period drifts 7.17 → 17.65 steps as α runs 1.0 → 0.2; the zero-delay closure destroys ringing entirely. Tests must therefore verify the closure or jointly fit (λ, α).

**H0a (registered rival — lumpability).** The ι-projected scalar process is strongly lumpable (Kemeny–Snell condition) with respect to the multi-channel trust dynamics — i.e., a scalar sufficient. Test: non-Markovianity of the projection and hysteresis at fixed ι. Rejection of lumpability corroborates the vector-necessity claim (theory H1). If stage activities prove unmeasurable on current instruments, H0a is untestable and this limitation will be stated.

**H3 (phase transition).** Trust networks parameterized by feedback quality exhibit the Kuramoto-*form* threshold: below a critical coupling (feedback bandwidth/latency), collective Phase Alignment Score (PAS) collapses toward zero independent of mean individual dispositions. The pre-registered prediction is the functional form — continuous onset of PAS coherence at a critical feedback quality — not the mean-field number K_c = 2/πg(0), which requires network corrections on sparse, weighted real networks.

**H4 (measurement dependence).** Salient observation of the measurement process shifts the effective dissipation of the mismatch stream (the behavioral observer effect, ψ(m)). Falsifiable signature: **joint movement of rising stationary variance σ²/(2(μ+ψ)) together with rising lag-1 autocorrelation** of the mismatch stream (dissipation-floor slowing as ψ → −μ⁺; in-silico inflation ×1.25 / ×2 / ×10 at ψ = −0.2μ / −0.5μ / −0.9μ, Sim G9). Direction and magnitude predicted per agent from baseline vigilance markers. No instrument achieves ψ = 0; residual-salience controls included.

## 2. Design

- Repeated-interaction, within-subject longitudinal design with recorded expectations E_t and outcomes V_t per event, across three domains (financial, social, physiological) for the invariance tests.
- Observation cadence is fixed per domain a priori so that per-event dimensionless λ's are commensurable (the cadence caveat: per-event and per-unit-time λ are the same parameter only under stationary, stated event rates).
- Identification of λ requires within-subject variation in ε_t conditional on S_{t−1} — events in which expectation and validation diverge by a recorded, exogenous amount. The DOCAS offer-stimulus paradigm (registration DOCAS-GATE-1, in this deposit) is designed to generate exactly such variation.
- H4 requires an exogenous salience manipulation plus a baseline condition: ψ enters every observable only through the sum μ + ψ, so a salience effect is not separately identifiable from a single condition. The H4 statistic is computed in raw units with s_d held fixed across salience conditions, so no rescaling of the expectation axis can mimic or mask a dissipation change.
- All precision/prior parameters fixed a priori (or fit on a training partition); post-hoc adjustment of precisions after a failed prediction is forbidden by protocol.

## 3. Sampling plan

- Population: adults in repeated-interaction settings with instrumented expectation/outcome streams (financial stream via the FreshCredit pilot infrastructure; social and physiological streams per domain protocols).
- Sample size and power: power analysis to be fixed in this registration before data collection; the ringing prediction at realistic irregular cadence (0.3–3 events/day) requires the registered power analysis — if underpowered, the ringing prediction is falsifiable in principle but unresolved by the proposed instruments, and that outcome will itself be reported.
- Exclusion criteria: to be specified here before data analysis.

## 4. Instruments / measures

- H_t: the observable stabilization readout — the DOCAS stage-marker composite proxying S (distinct from the latent state).
- State-space model: Observation ΔH_t = λ_H·ε(t) + u_t ; State S_t = S_{t−1} + λ·ε(t−1) + η_t, fit by Kalman filtering / EM, plus a Bayesian hierarchical variant λ_{H,i} ~ 𝒩(μ_λ, τ_λ²) reporting the population posterior μ_λ and individual heterogeneity.
- The Fresh Protocol's financial application (TFP paper and FreshCredit whitepaper, in this collection) implements the measurement infrastructure; the DOCAS stage mapping (D=expectation, O=validation, C=recognition, A=activation, S=stabilization) is frozen by pre-registration before any data are analyzed.
- Estimator certification (already run in silico): mean |λ̂−λ| 0.0074, p95 0.0215, max 0.0343 against the 0.15 tolerance; λ = 0 negative control max 0.0092; ultra-thin streams (60–110 events) max error 0.0737.

## 5. Analysis plan

1. Fit the state-space model per subject; hierarchical posterior for μ_λ.
2. Equivalence test of μ_λ against the corridor [0.46, 0.76] at the pre-registered credible level.
3. Cross-domain invariance: per-domain population means must not differ by more than the corridor width after per-domain normalization (H2a); rank-order correlation of λ_i across domains and windows (H2b).
4. Ringing test: fit the closed-loop impulse response; compare observed period to P(λ̂, α) with the closure verified or (λ, α) jointly fit.
5. **Model comparison (the primary test).** On the same data, formally compare: (a) the fixed-λ delta rule (Rescorla–Wagner limit of the master law); (b) the adaptive-λ extension; (c) a Behrens-style hierarchical Bayesian learner with volatility-sensitive learning rate — the established superior account of human social learning, treated as a competitor to beat. Comparison by Bayes factors (or protected exceedance probabilities), pre-registered, all hyperparameters fixed a priori.
6. H0a: lumpability test via non-Markovianity of the ι-projection and hysteresis at fixed ι.
7. H3: fit the onset of PAS coherence vs. feedback quality; test for continuous-onset functional form.
8. H4: joint variance + lag-1-autocorrelation test across salience conditions, per-agent direction/magnitude predictions from baseline vigilance markers.

## 6. Falsification criteria

- **H2 refuted** by any of: (i) the hierarchical posterior for μ_λ excludes [0.46, 0.76] at the pre-registered credible level; (ii) cross-domain measurement invariance fails (showing 0.61 to be a property of one instrument); (iii) the constant-λ state equation fails posterior predictive checks against the adaptive-λ extension — in which case any point prediction is moot and the fixed-λ theory is retained only as a tractable approximation.
- **Structural-misspecification warning (SIM-R1 battery 1, run in silico):** corridor corroboration is achievable by misspecification bias alone — under a Behrens-style adaptive-λ truth (time-average λ̄ = 0.355) the certified constant-λ estimator lands at λ̂ = 0.472, *inside* the corridor while the truth lies outside (21.7% of users outside at coupling c = 1.5; population bias +0.117). The model comparison of criterion (iii) is therefore load-bearing, not optional.
- **Ringing claim refuted** if the population is recovered in the overdamped branch (λ < 1/4), or if observed ringing period fails the formula conditional on the verified closure.
- **H0a:** failure to reject lumpability corroborates the scalar-sufficiency rival and weakens the vector-necessity claim; rejection corroborates H1.
- **H3 refuted** if no critical-quality onset of coherence is observed (e.g., coherence tracks mean individual dispositions instead).
- **H4 refuted** if salience manipulations fail to move variance and lag-1 autocorrelation jointly in the predicted direction.

## 7. Current status

Prospective. No human data collected or analyzed. In-silico legs run and disclosed: estimator certification (whitepaper Fig. 8), SIM-R1 battery 1 (misspecification) and battery 2 (closure sensitivity), Sim G8 (closed-loop ringing), Sim G9 (ψ-model statistics). Self-attested until OSF registration is completed; this skeleton is the registration text to be filed verbatim with sample-size/power/exclusion fields completed before data collection.
