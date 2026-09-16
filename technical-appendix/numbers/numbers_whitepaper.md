# Whitepaper Simulation Battery — Re-run Numbers (SIM-W)

All runs: numpy/matplotlib/scipy, seed 42 (multi-seed medians noted where used), honest nulls included.
Figures at 150 dpi in `/mnt/agents/output/figures/whitepaper/`. Claims referenced to
`/mnt/agents/output/revised/whitepaper_revised.md` and Sim-Battery A/B (`/mnt/agents/work/sims/sim_results_A.md`, `sim_results_B.md`).

Conventions enforced: master law `S ← S + λ⁺max(ε̃,0) + λ⁻min(ε̃,0) − δ(S − S_base)`, ε̃ = (V−E)/s_d (§M4/M8);
stereographic phase map θ = 2 arctan(ε̃) (§M7); leakage K_eff = K(1−ℓ), σ_η = πℓ/2 (Sim-B Study 1 spec).

---

## W1 — Estimator validation (§3.4 pipeline validation; claim W9; corridor feed for GTT H2)

**Setup.** 300 synthetic users, true λ ~ U[0.05, 0.95]. Generative model = master law GTT preset
(S_{t+1} = S_t + λε̃_t + process noise σ=0.10). Mixed-sign ε̃ streams (12–15% negative, heavier-tailed
betrayals). Realistic cadence: Poisson arrivals 0.3–3.0 events/day × 365 days (median 569 events/user,
range 112–1100). Observations noisy and heavy-tailed (Student-t₅, σ=0.5); the Kalman/EM estimator runs
at *nominal, misspecified* noise (σ_proc=0.05, σ_obs=0.2). EM M-step: λ̂ = Σε̃·E[ΔS]/Σε̃² on RTS-smoothed means.

| Quantity | Whitepaper / certified | Re-run (seed 42) | Verdict |
|---|---|---|---|
| λ̂ recovery tolerance | ≤ 0.15 (certified) | mean 0.0074, median 0.0056, **p95 0.0215, max 0.0343** | **PASS** (all summary levels ≪ 0.15) |
| Realized λ̂ error | 0.024 printed | p95 = 0.0215 (mean 0.0074) | PASS — consistent with printed value |
| Trajectory recovery r | 0.879 (threshold 0.7) | median 1.000, p5 = 0.999, min 0.990 | PASS (see deviation note D1) |
| Ultra-thin stress (60–110 events, 40 users) | — | mean 0.0231, p95 0.0573, max 0.0737 | PASS (worst corner still < half the tolerance) |
| Negative control (λ = 0 planted, 40 users) | — | mean λ̂ = −0.0008, max|λ̂| = 0.0092 | PASS (no phantom sensitivity) |

**Figure:** `figW1_estimator_validation.png` — (a) true vs recovered λ scatter with ±0.15 band;
(b) error histogram vs certified tolerance and printed 0.024; (c) example latent-trajectory recovery.

## W2 — PPV / base-rate demonstration (Sim W7 re-run; §1.5 risk language)

Instrument identified from the printed numbers: **sensitivity 0.90, specificity 0.71** reproduces both.

| Claim | Printed | Analytic recompute | Monte-Carlo (2M files, seed 42) | Verdict |
|---|---|---|---|---|
| PPV at 22% prevalence | 0.47 | 0.4668 | 0.4672 | **PASS** |
| PPV at 1% prevalence | 0.03 | 0.0304 | 0.0306 | **PASS** |

Same instrument, 16× PPV collapse purely from the base rate. **Figure:** `figW2_ppv_baserate.png` —
(a) PPV vs prevalence with both printed points (analytic dots, Monte-Carlo crosses); (b) PPV vs
prevalence at sens=0.90 across specificities (specificity dominates PPV at low prevalence).

## W3 — Cold-start product figure (§4.7 channel 4; Sim-Battery A Study 1 re-run)

Reconciled master law (λ⁺=0.005, λ⁻=0.02, δ=0.01/event, S_base=0.5, S₀=0, 90/10 honest stream,
asymptote 0.75, decisionable = ≥90% of asymptote), event rate = r_floor + 5·S/day (Poisson).

| Organic floor | Printed day | Re-run day (seed 42) | Verdict |
|---|---|---|---|
| 0/day | never converges | never converges (trap confirmed) | **PASS** |
| 0.01/day | 562 | 563 | PASS (±1 day, threshold-crossing convention) |
| 0.05/day | 143 | 144 | PASS |
| 0.1/day | 139 | 140 | PASS |
| 0.5/day | 119 | 120 | PASS |
| 1/day | 71 | 72 | PASS |
| 5/day | 23 | 24 | PASS |

**New product arm (quantifies the §4.7 design requirement):** seeded score-independent floor of
2 events/day × 30 days + organic 0.01/day → decisionable at **day 72** (vs 563 organic-only) — a 7.8×
acceleration from a one-month provider-initiated onboarding floor.
**Figure:** `figW3_coldstart.png` — (a) S(t) trajectories: trap / 0.01-day / 5-day / seeded floor, with
decisionable threshold; (b) time-to-first-decisionable-score vs r_floor (median of 5 seeds), printed
points overlaid.

## W4 — Adoption compounding with densification feedback (§4.5 CAC densification claim; §4.7)

New model (no printed numbers to reproduce; parameters stated): adoption ODE
dA/dt = h₀(1−A)q + g₀qA(1−A) − c₀(1−q)A with q(A) = exp(−t_dec(A)/τ), t_dec from the W3 cold-start
engine at rate r(A) = r_floor + κA; h₀=0.05/yr, g₀=1.2/yr, c₀=0.6/yr, τ=0.5 yr patience, A₀=1%.

**Parameter regions (adopted fraction after 10 yr):**
- **Stalls** (A* < 0.2): floor ≲ 0.01/day AND κ ≲ 0.5 — the compounding assumption fails here.
- **Compounds** (A* ≥ 0.8): floor ≥ ~0.1/day, or κ ≥ ~2, or strong densification alone.
- **Exact trap**: r_floor = 0 AND κ = 0 → A collapses to 2×10⁻⁵ (population form of the W3 trap).
- Honest nuance (deviation from a naive reading of the individual-level trap): densification alone
  (κ=5, zero organic floor) bootstraps off the 1% initial cohort (A→0.95 by year 10) — the
  population-level trap requires *both* floors at zero; the individual-level trap (W3) is sharper.

**Figure:** `figW4_adoption_compounding.png` — (a) adoption-after-10-yr heatmap over (floor × κ) with
stall/compound contours; (b) representative trajectories including trap, stall, partial, compound, and
densification-only arms.

## W5 — Cost accounting (§4.5, §1.4; Sim-Battery A Study 3 arithmetic)

| Claim | Printed | Recomputed | Verdict |
|---|---|---|---|
| Events per 10-unit standing | 1,005 | 10 × 100.5 = 1,005 | **PASS** |
| Lifetime anchoring, unrolled | ~$1.01 | 1,005 × $0.001 = $1.005 | PASS |
| Lifetime anchoring, rolled (K=10⁴) | ~$0.0001 | $0.0001005 | PASS |
| Incumbent marginal pull | $50–$110+ | carried as stated (external) | — |
| Like-for-like, 20 verification queries | — | incumbent $1,000–$2,200 vs FreshCredit $1.01 (or $0.0001) once + ≈$0 local reads | consistent with §4.5's marginal-vs-marginal framing |

Caveat carried per the whitepaper itself: settlement fees are not a full-product price; the honest
juxtaposition is re-purchase-per-query vs anchor-once + local reads, and it is drawn that way.
**Figure:** `figW5_cost_accounting.png` — (a) cost/score vs events-per-score (10³–10⁵), unrolled vs
rolled (K=10⁴), incumbent per-pull band; (b) cumulative cost over repeated verification queries.

## W6 — NNH / harm quantification (§4.7; Sim-Battery A Study 2/3 numbers)

| Channel | Printed | Recomputed | Verdict |
|---|---|---|---|
| Per-event fees, lifetime unrolled / rolled | $1.01 / $0.0001 | $1.005 / $0.0001 | **PASS** |
| Incumbent fees | $50–$110+/pull; $510–$725/closed loan | carried as stated (external) | — |
| Centralized expected exposure (p_org=0.05, N=3×10⁸) | 15M/yr | 15.0M/yr | PASS |
| Per-tenant attacker-exposed win (p_dev=0.005, p_cm=0.001) | 1.8M/yr | 1.8M/yr (8.3× reduction) | PASS |
| Key/guardian loss at p_key = 0.001/0.005/0.01 | 0.3M / 1.5M / 3.0M /yr | 0.3 / 1.5 / 3.0 M/yr | PASS |
| Honest side-by-side | key-loss 1.5M/yr ≈ security win 1.8M/yr (same order) | confirmed exactly | PASS |

**Figure:** `figW6_nnh_harm.png` — (a) fee totals (log scale): fractions of a cent per lifetime vs
$50–$110+ per pull and $510–$725 per closed loan; (b) records/yr: centralized 15M, per-tenant 1.8M,
key-loss 1.5M/3.0M/0.3M — the win and the counter-term side by side.

## W7 — R(K,ℓ) surface re-render (whitepaper Figure 5; claim W4; Sim-Battery B Study 1 spec)

N=500, ω ~ Cauchy(0,1), stereographic init, K_eff = K(1−ℓ), σ_η = πℓ/2 (redrawn each step), dt=0.05,
100 t.u. burn-in + 200 t.u. measurement, seeds 42/1042 averaged; fine scans 3 seeds.

| Quantity | Printed (Sim-B / Fig. 5) | Re-run | Verdict |
|---|---|---|---|
| R(K=4.5, ℓ=0) | 0.709 | 0.709 | **PASS — exact** |
| R(K=4.5, ℓ=0.1 / 0.3 / 0.5) | 0.663 / 0.474 / 0.071 | 0.663 / 0.474 / 0.071 | **PASS — exact** |
| R(K=8, ℓ=0) | ≈0.85 | 0.850 | PASS |
| Incoherent floor | 0.03–0.05 (1/√N) | 0.040 | PASS |
| ℓ* at K=4.5 (R<0.7) | ≈0.02 | 0.02–0.03 (R: 0.705@0.01, 0.701@0.02, 0.698@0.03) | PASS |
| K≥6 survives to ℓ | ≈0.15 | 0.225 (R=0.715 @ ℓ=0.2) | PASS — printed value conservative (see D4) |
| K=8 survives to ℓ | ≈0.25 | >0.30 (R=0.743 @ ℓ=0.3) | PASS — printed value conservative |
| R=0.7 contour at ℓ=0.1 / 0.2 | K ≈ 5.5 / ≈ 7 | K ≈ 5.0 / ≈ 5.9 | minor deviation (see D4) |

**Figure:** `figW7_R_surface.png` — (a) R(K,ℓ) heatmap with R=0.3/0.5/0.7 contours and the K=4.5
operating point; (b) R vs ℓ at K=4.5 (fine scan, ℓ*≈0.02–0.03 marked), K=6, K=8, with the R=0.7 target
and the 1/√N floor.

---

## Deviation register

- **D1 — Trajectory recovery exceeds printed value.** Re-run median r = 1.000 vs printed 0.879. The
  re-run exercises the financial-stream state-space estimator alone; the printed 0.879 came from the
  full dual-layer (financial + physiological) pipeline with its loading matrix. Both pass the 0.7
  threshold; the printed number is *not reproduced*, not failed. The λ̂ tolerance — the load-bearing
  number for the GTT H2 corridor — replicates (p95 0.0215 vs printed 0.024, tolerance 0.15).
- **D2 — Cold-start days shift by +1.** 563/144/140/120/72/24 vs printed 562/143/139/119/71/23 —
  first-crossing vs stabilization convention; no claim affected.
- **D3 — W4 is a new model.** No printed numbers to reproduce; it supports the §4.5 densification
  mechanism with an explicit stall region, and adds the honest nuance that the population-level trap
  needs zero floor AND zero densification (a small initial cohort plus densification bootstraps).
- **D4 — Coherence contours slightly less retreated than printed.** R=0.7 crossings at K≈5.0 (ℓ=0.1)
  and ≈5.9 (ℓ=0.2) vs printed ≈5.5/≈7; K=6 robustness measured to ℓ≈0.225 vs printed ≈0.15. Direction
  of every claim intact; all operating-point and ℓ* numbers replicate exactly. The printed contour
  values were coarse read-offs (Sim-B's own wording); the re-run values are the more precise ones.

## Figure index

- `figW1_estimator_validation.png` — W1 scatter + error histogram + trajectory example
- `figW2_ppv_baserate.png` — W2 PPV vs prevalence, printed points reproduced
- `figW3_coldstart.png` — W3 trajectories + time-to-decisionable curve
- `figW4_adoption_compounding.png` — W4 hold/stall phase diagram + trajectories
- `figW5_cost_accounting.png` — W5 cost/score and cumulative-query cost
- `figW6_nnh_harm.png` — W6 fees + security win vs key-loss counter-term
- `figW7_R_surface.png` — W7 leakage-graded coherence surface (whitepaper Figure 5 re-render)
