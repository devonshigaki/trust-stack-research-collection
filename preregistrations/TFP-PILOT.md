# TFP-PILOT — Pre-Registration (Skeleton Draft): Fresh Protocol Pilot Program

**Registration type:** OSF "Pre-Data Collection Registration" (deposit pending; OSF DOI to be assigned).
**Source:** Extracted from *The Fresh Protocol* (tfp_revised.md) §1.4 "Hypotheses and proof obligations" (the registered form — an earlier draft stated the headline hypothesis backwards relative to what the simulations test; the current text matches the tested design) and §5 "Protocol Evolution and Benchmarking."
**Self-attestation status:** the in-silico proof obligations (1)–(3) below are discharged against criteria internally frozen and timestamped in the Supporting Document; external OSF registration of the same design is pending and must be filed **prior to any pilot data collection**. Until then, all frozen-criteria claims are self-attested.

---

## 1. Hypotheses

**Null hypothesis (H0).** Feedback coupling has no effect on population-level trust-field coherence (the Kuramoto order parameter R stays at the finite-size incoherent floor ≈ 1/√N at all coupling strengths); observation leakage has no effect on coherence at fixed coupling; and edge architecture does not reduce the marginal cost of engagement.

**Alternative hypothesis (H1), three legs, in the direction actually tested:**

1. **Coupling produces coherence.** Under protocol feedback coupling at sufficient strength K, the agent population self-organizes above the coherence threshold (target: R > 0.7); the isolated control (K = 0) remains at the incoherent floor (target: R < 0.3). Coherence is a property of the coupling, not of isolated stores.
2. **Observation leakage degrades coherence.** At fixed K, R decays monotonically as the observation-leakage parameter ℓ rises (operationalized exactly as: coupling attenuation K_eff = K(1−ℓ) plus per-timestep redrawn observation noise σ_η = (π/2)·ℓ). The architectural content of the privacy claim lives here: non-expropriative measurement is what keeps ℓ below the fragility threshold at which coherence collapses.
3. **Edge architecture reduces marginal cost.** Edge compute plus per-event micropayment settlement achieves a marginal cost per validation event far below incumbent marginal per-query costs, verified against printed frozen figures with events-per-decision accounting (§5.2 of the protocol paper).

## 2. Design

**In-silico arm (run; to be re-registered for the pilot):** agent-based Kuramoto population (N = 500, ω ~ Cauchy(0,1), stereographic phase initialization, Euler dt = 0.05, burn-in 100 t.u. + measurement 200 t.u., seeded replications), swept over K ∈ [0, 8] × ℓ ∈ [0, 0.9]; coherence differences evaluated at p < 0.001.

**Pilot arm (prospective — this registration):** a live deployment pilot of the V3 protocol stack (sovereign per-tenant edge storage, verifiable settlement layer, x402 micropayment rails) with consenting participants, measuring (i) realized feedback-coupling parameters and observed coherence analogues in the deployment's interaction network, (ii) realized observation-leakage proxies under the protocol's non-expropriative measurement design vs. any expropriative comparison condition, (iii) realized marginal per-event settlement and compute costs against the frozen print figures.

## 3. Measures

- **Coherence:** Kuramoto order parameter R over the pilot interaction network (population) and per-participant alignment trajectories; the corrected incoherent-control baseline is ≈ 0.03–0.05 (the old arctan phase map's K = 0 inflation artifact, R ≈ 0.635, is disclosed and repaired via the stereographic map).
- **Leakage ℓ:** operationalized per the two-channel compounding model above; the pilot measures realized attenuation and observation-noise components separately where possible.
- **Cost:** marginal per-validation-event settlement ($0.001/event target, x402-class rails; $10⁻⁷/event under K = 10,000 block rollups), events-per-decision (stated assumption 10³–10⁵, giving $1–$100 settlement per decision), backup storage (~1 GB/tenant-year at $0.014–0.019/GB). Like-for-like discipline: marginal against marginal only; the >98% marginal-cost-reduction target holds exactly when the incumbent's marginal per-query price exceeds $0.05/query at equal event/query counts.
- **Frozen-figure discipline:** the figures printed in the paper (§5.2) are the canonical record of claims; the live calculator at freshcredit.xyz/cost is a supplementary, versioned tool. No static cost multiplier is asserted; incumbent marginal query pricing is largely unpublished and carried in the calculator with sensitivity analysis.

## 4. Analysis plan

1. Leg 1: coupled vs. isolated coherence contrast at p < 0.001 (in silico: R = 0.739 ± 0.029 coupled vs. 0.040 ± 0.001 isolated — verification re-run values; the isolated arm sits at the 1/√N ≈ 0.045 finite-size floor). Pilot: compare realized R analogues against the registered thresholds (R > 0.7 coupled; R < 0.3 control).
2. Leg 2: monotonicity of R in ℓ at fixed K (in silico: monotone decay at every K tested). Pilot: dose-response of realized coherence on realized leakage proxies.
3. Leg 3: cost accounting against frozen print figures, with events-per-decision accounting; any divergence between live and printed figures resolves in favor of the printed snapshot for the purposes of the paper's claims.
4. All pilot analyses pre-specified here before data collection; any post-hoc analysis labeled as such.

## 5. Falsification criteria

- Leg 1 fails if the coupled condition does not exceed R > 0.7, or if the isolated control exceeds R < 0.3, at the registered significance level.
- Leg 2 fails if R does not decay monotonically in ℓ at fixed K.
- **Honest null already in print (in-silico):** at the zero-leakage operating point K = 4.5, coherence is only R ≈ 0.71 — marginally above target — and R falls below 0.7 within the leakage band **ℓ\* ∈ [0.02, 0.10]** (first below-0.7 reading at ℓ = 0.08 in a 9-seed fine scan; the exact crossing is not resolvable at seed noise ±0.02–0.03). Robust R > 0.7 requires K = 6 (survives to ℓ ≈ 0.22–0.28) or K = 8 (ℓ ≈ 0.30–0.40). The pilot therefore tests a *demanding* requirement, not a soft one: if realized leakage exceeds the fragility band at the realized coupling, the coherence claim fails as registered.
- Leg 3 fails if realized marginal per-event costs at like-for-like event/query counts do not beat incumbent marginal per-query prices under the stated break-even condition, or if the events-per-decision assumption is violated upward materially.
- No achieved end-to-end performance is claimed for deployed applications; the pilot is the first test of any deployed leg.

## 6. Current status

In-silico obligations (1)–(3) discharged and printed in tfp_revised.md §3.6 with seeds and audit trail (figures in this deposit: figures/tfp/, figures/robustness/); obligation (4) maintained against frozen figures plus the supplementary calculator. Pilot: no human/deployment data collected. Self-attested until this registration is filed; the collection index carries the correction history (the H1 inversion repair) in its correction register, and this registration files the CURRENT text.
