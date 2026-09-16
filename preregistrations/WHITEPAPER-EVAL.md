# WHITEPAPER-EVAL — Pre-Registration (Skeleton Draft): FreshCredit Pilot Evaluation Program

**Registration type:** OSF "Pre-Data Collection Registration" (deposit pending; OSF DOI to be assigned).
**Source:** Extracted from *FreshCredit: Credit as Trust Quantified* (whitepaper_revised.md) §4 "Benchmarks and Projections (Discipline)" — including its pre-registration commitment ("the dual-layer DOCAS validation and the pilot evaluation are pre-registered (OSF) before data analysis") — together with the concordance-pilot protocol of §3.4, which is the pilot evaluation's measurement design, and the harm/benefit ledgers of §4.3/§4.4, which define the evaluation's harm-side endpoints.
**Self-attestation status:** the pipeline-validation criteria below were frozen in code before the passing in-silico run (audit trail: four first-run failures preserved and disclosed); external OSF registration is pending. Until filed, all frozen-criteria and pre-registration claims are self-attested. The real-user concordance study is explicitly the stack's "A-grade gate."

---

## 1. Hypotheses

**Concordance pilot (the measurement-validation leg; per whitepaper §3.4):**
- **P1 — neural×behavioral geometry concordance.** Events that look similar in TRIBE v2's cortical-prediction space produce similar shifts in the user's estimated trust trajectory: Mantel permutation test between the neural reference geometry and the per-user behavioral event geometry, p < 0.05.
- **P2 — text×behavioral concordance (sanity control).** The CLICS text-semantic control geometry concords with the behavioral geometry (a positive control that must pass for P3 to be interpretable).
- **P3 — neural concordance survives controlling for text (partial Mantel).** The neural geometry adds something beyond raw semantics.

**Evaluation legs (per whitepaper §4 / §4.3–§4.4):**
- **E1 — estimator performance on real users.** The Kalman/EM state-space estimator recovers per-user latent trust trajectories T̂_t and trust-sensitivity λ̂ on real edge streams (Apple Health physiology; Plaid financial behavior) at accuracy compatible with the in-silico certification (|λ̂−λ| within the 0.15 tolerance at p95).
- **E2 — misclassification harm at the flagging stage is bounded by the printed ledger.** At 1% prevalence the instrument's PPV is 0.03 and NNH ≈ 1.03 (one wrongful flag per ~1.03 flags issued); the evaluation tests whether the mitigations (prevalence-aware thresholds, hardship flags, human review) move the realized wrongful-flag rate below the unmitigated prediction.
- **E3 — cold-start escape under the seeded floor.** A seeded, score-independent floor of 2 events/day for the first 30 days (provider-initiated onboarding events) yields a decisionable score at day 72 (in-silico: 4.4×/7.8× acceleration vs. the organic-only 0.01/day floor on the first-crossing/stabilization clocks). The evaluation measures realized time-to-decisionable against both convergence criteria, printed identically: first-crossing (S ≥ 0.9·S*) and stabilization-to-asymptote.
- **E4 — benefit channels at pilot scale.** Error-correction NNT 19–52 per tier-fix (q-dependent; q — user-owned correction success probability — is declared unmeasured and is a pilot measurable); cost benefit $50–$110 per avoided incumbent pull, net-of-attestation positive only for multiplier m ≲ 100; inclusion NNE ≈ 3.7–5 per additional approval (third-party anchors: Upstart NAL +27%, Livble ~3× — projected, not FreshCredit measurements).

## 2. Design

- Prospective pilot of consenting FreshCredit users on the live edge architecture (libSQL database-per-tenant; user-held keys; per-user estimator weights stored, trained, and executed locally; nothing leaves the edge database in the current design).
- Representational-similarity design for the concordance leg — no point-to-point translation between neural and behavioral spaces is needed or claimed (naive point-mapping already failed in the in-silico validation battery).
- Frozen population references: the neural reference geometry (TRIBE v2 predictions on the canonical offer-stimulus battery; 720-subject, 1,000+ scanning-hour anchor) and the pre-registered loading matrix ship frozen and are never updated from user data.
- Comparison layer: the only cross-space quantity computed is the concordance statistic itself, moved only as a selective-disclosure predicate the user chooses to present, never as raw geometry and never into the decision path.
- Frozen-figures discipline (whitepaper §4): all cost/speed/security comparisons are frozen dated snapshots; the live calculator is supplementary; printed figures govern claims.

## 3. Measures / instruments

- **Behavioral streams:** HealthKit physiology (HRV, resting heart rate, sleep, respiratory rate) and Plaid financial events (spend volatility, insufficient-funds events, payment timing, payday cycles) parsed at the edge.
- **Estimator:** the GTT §6 Kalman/EM pipeline producing T̂_t and λ̂ per user (own-loop trustor-side instance; the decision-relevant score is computed by the separate financial-stream-only instance).
- **Neural reference:** TRIBE v2 (real released checkpoint; CPU port with reference parity) run on the actual offer texts the user received.
- **Semantic control:** CLICS concept geometry (real CLICS4: 1,730 concepts / 51,562 edges).
- **Statistics:** Mantel permutation tests (P1, P2), partial Mantel given text (P3), plus a shuffled-label negative control that must remain null.

## 4. Analysis plan

1. Pipeline-gate checks on real data, mirroring the in-silico validation battery: trajectory recovery, λ̂ tolerance, negative controls (λ = 0; shuffled labels).
2. P1/P2/P3 Mantel and partial-Mantel permutation tests at the registered thresholds.
3. E2: realized PPV/wrongful-flag accounting at realized prevalence, with and without mitigations; reported in the NNH ledger format (incommensurate units; no composed single NNH asserted).
4. E3: time-to-decisionable under the seeded floor against both printed convergence criteria.
5. E4: measure q (correction success), realized avoided-pull counts, realized attestation pricing (the m multiplier — declared an open market question), and realized approval-conversion against the NNE anchors.
6. The one direct cross-domain test in the stack (DOCAS Sim D8 multilingual arms) failed its pre-registered criteria; domain-generality claims remain architectural, not demonstrated, and any cross-domain extension of this evaluation requires its own registration.

## 5. Falsification criteria

- **P1 fails** if neural×behavioral Mantel p ≥ 0.05 on real users. **P3 fails** if concordance does not survive controlling for text (the neural geometry then adds nothing beyond semantics and the dual-layer claim is withdrawn).
- **P2 is a sanity control:** if P2 fails, the pipeline is debugged before P1/P3 are interpreted.
- **E1 fails** if real-data λ̂ recovery exceeds the 0.15 tolerance at p95 against ground truth constructed per the registered protocol.
- **E2/E3 are ledger commitments:** realized harms exceeding the printed ledger (wrongful-flag rate above the unmitigated prediction under mitigations; failure of the seeded floor to produce decisionable scores near day 72) are reported as failures, not re-tuned.
- The distributional warning is registered: frequent-small losses land on the least-hygienic endpoints, plausibly concentrated in the thin-file population the product exists to serve — the evaluation must report distributional incidence of harms, not only means.
- In-silico validation caveat carried: the recovery certification ran under the same law's generative model; the SIM-R1 misspecification arm shows corridor-level corroboration is achievable by weighting bias alone, so the real-data model comparison (Behrens-style adaptive-λ rival) is load-bearing here too.

## 6. Current status

Machinery validated in silico against pre-registered criteria frozen in code before the passing run: latent trajectory recovery r = 0.879 (dual-layer scope; single-stream re-run median r = 1.000); λ̂ recovery error 0.024 vs. tolerance 0.15 (300-user re-run: mean 0.0074, p95 0.0215, max 0.0343; λ = 0 negative control max 0.0092; ultra-thin worst case 0.0737); planted concordance detected at Mantel r = 1.0, p = 0.002; partial given text p = 0.002; shuffled-label control correctly null (p = 0.684). Four first-run failures (non-identifiable loading matrix, off-by-one λ regression, geometry-destroying normalization, untestable generative design) found and corrected — disclosed. **No human data collected.** Self-attested until this registration is filed; filing is the declared A-grade gate for the collection.
