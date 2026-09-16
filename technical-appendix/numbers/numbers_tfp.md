# numbers_tfp.md — TFP full simulation battery re-run (SIM-P), claim vs re-run

All re-runs: numpy/scipy/matplotlib, seed 42, honest nulls preserved. Figures at 150 dpi in `/mnt/agents/output/figures/tfp/`.
Claims sourced from `/mnt/agents/output/revised/tfp_revised.md` (§3.6–3.10, Figures 2–10 captions) and the archived specs `/mnt/agents/work/sims/sim_results_A.md`, `sim_results_B.md`.
Verdicts: **PASS** = re-run inside claimed uncertainty or arithmetic exact; **DEVIATION** = mismatch that should change printed text.

---

## 1. Sim P1 — coherence, corrected phase map (figP1_coherence.png)

Spec: N=500 Kuramoto, ω ~ Cauchy(0,1), stereographic init θ=2·atan(ε̃), ε̃ ~ Cauchy(0,1); dt=0.05, burn-in 100 t.u. + measurement 200 t.u.; 8 replicas.

| Quantity | Claim | Re-run | Verdict |
|---|---|---|---|
| R, coupled K=4.5 (8 repl.) | 0.751 ± 0.041 | **0.739 ± 0.029** | PASS (inside claimed ±1σ) |
| R, isolated K=0 (8 repl.) | 0.032 ± 0.010 | **0.040 ± 0.001** | PASS (both at 1/√N = 0.045 floor; re-run sd smaller — floor draws barely vary across replicas) |
| atan artifact, K=0, 200 seeds | 0.635 ± 0.014 | **0.638 ± 0.014** | PASS (exact) |
| stereographic map, K=0, 200 seeds | 0.040 ± 0.021 | **0.040 ± 0.020** | PASS |
| raw uniform phases, 200 seeds | 0.039 ± 0.020 | **0.039 ± 0.020** | PASS |

The old `atan` artifact (an uncoupled population reporting R ≈ 0.64) is confirmed in the side panel; the corrected baseline is ≈ 0.03–0.05, consistent with P1's reported 0.032 having used raw uniform phases.

## 2. Sim P1b — leakage-graded surface (figP1b_surface.png) — HEADLINE FIGURE

Spec: K_eff = K(1−ℓ); observation noise η ~ N(0,(πℓ/2)²) redrawn every timestep; K ∈ [0,8] (17 pts) × ℓ ∈ [0,0.9] (10 pts), 2 seeds/grid point; fine scan at K=4.5 (9 seeds); mid scan at K=6,8 (3 seeds).

| Quantity | Claim | Re-run | Verdict |
|---|---|---|---|
| R(K=8, ℓ=0) | ≈ 0.85 | 0.871 | PASS |
| R(K=4.5, ℓ=0) | 0.709 | 0.717 (grid, 2 seeds); 0.738 ± 0.009 sem (fine, 9 seeds) | PASS |
| R(K=4.5): ℓ=0.1 / 0.3 / 0.5 / 0.9 | 0.663 / 0.474 / 0.071 / 0.041 | 0.684 / 0.526 / 0.076 / 0.041 | PASS (within seed noise) |
| monotone R decay in ℓ at every fixed K | yes | yes, within seed noise (largest upward blip +0.0036, only at K ≤ 2 where R sits at the floor) | PASS |
| **ℓ\* at K=4.5** | **ℓ\* ≈ 0.02** (0.705/0.701/0.698 at ℓ=0.01/0.02/0.03) | R hovers 0.69–0.74 across ℓ ∈ [0, 0.10] (9 seeds); first below-0.7 reading at ℓ=0.08; crossing resolvable only as a **band ℓ\* ∈ [0.02, 0.10]** | **DEVIATION** — the exact ℓ\* = 0.02 (and its suspiciously smooth sequence) is not resolvable at seed noise ±0.02–0.03; the qualitative fragility claim (R>0.7 at K=4.5 survives only a few percent of leakage) PASSES |
| robust region K ≥ 6 | survives ℓ ≈ 0.15 | survives to ℓ ≈ 0.28 (interp crossing) | **DEVIATION** — re-run is *more* robust than printed (paper conservative); qualitative claim PASSES |
| robust region K ≥ 8 | survives ℓ ≈ 0.25 | survives to ℓ ≈ 0.40 | **DEVIATION** — same direction (paper conservative) |

## 3. Sim P5 — transfer-entropy surveillance comparison (figP5_transfer_entropy.png)

Reconstruction caveat: the original battery's generative model (seed 20260905) is not archived in the provided specs; re-run uses a rebuilt coupled-AR(1) pair — protocol: symmetric coupling c=0.20 (bilateral validation); surveillance: one-way coupling c=0.45 agent→validator, no return edge. Estimator: 4-bin quantile quantization, 4,000 steps, surrogate correction = raw TE − mean of 20 circular-shift surrogates; 8 replicas, seed 42; 95% CIs across replicas (the registered re-run requirement — discharged here). Estimator validated against a brute-force implementation (agreement to 15 digits) and against analytic null bias (≈ B³/2N ln 2 ≈ 0.011 bits).

| Flow (bits) | Claim | Re-run (95% CI) | Replicas above 0.01-bit floor | Verdict |
|---|---|---|---|---|
| protocol agent→validator | 0.027 | 0.0315 ± 0.0029 | 8/8 | PASS |
| protocol validator→agent | 0.030 | 0.0283 ± 0.0022 | 8/8 | PASS |
| surveillance agent→validator | 0.110 | 0.1210 ± 0.0050 | 8/8 | PASS |
| surveillance validator→agent | 0.006 ("at or below threshold") | −0.0009 ± 0.0007 (surrogate overcorrection → ≈ 0) | 0/8 | PASS (direction; both below floor) |

Directions robust (every replica on the correct side of the floor in both architectures); magnitudes floor-adjacent (1–12× the 0.01-bit floor), so per instruction and per the paper's own caveat **no ratio headline is reported** (the raw forward-flow ratio ≈ 3.8× exists but is unreliable at these magnitudes).

## 4. Sim P8 — Sybil cost / whitewashing / deterrence, explicit master-law TFP preset (figP8_sybil_deterrence.png)

Preset (now explicit): λ⁻ = 0.02, λ⁺ = 0.005 (4×), δ = 0.01/event, S_base = 0.5, S₀ = 0.5. Stack figures: 100.5 events per unit standing, $0.001/event, target 10 units = 1,005 events.

| Quantity | Claim | Re-run | Verdict |
|---|---|---|---|
| unattested cost, 10 units | $1.01 | $1.005 | PASS (exact arithmetic) |
| attested, m = 10 / 100 / 1,000 | $10.05 / $100.50 / $1,005 | $10.05 / $100.50 / $1,005.00 | PASS (exact; linear in m — weak deterrent at m ≤ 10 confirmed) |
| time floor, ≤2/day | 1.4 yr minimum | 502.5 days = 1.38 yr | PASS |
| time floor, 0.5/day | 5.5 yr | 2,010 days = 5.50 yr | PASS (also 1/day → 2.75 yr, 5/day → 0.55 yr) |
| rollup K=10⁴: honest cost/event, lifetime | $10⁻⁷; $1.005 → $0.0001 | $10⁻⁷; $0.0001005 | PASS (exact; attacker time floor untouched) |

Whitewashing (reconstructed accounting: repair vs. fresh-identity-at-prior, mean standing over 300 post-decision events, 20 replicas): repair advantage +0.086 ± 0.020 (d=1), +0.079 (d=2), +0.067 (d=4), +0.042 (d=8), **−0.009 ± 0.020 (d=16)**. Verdict: PASS for d ≤ 8; **DEVIATION at d = 16** — under the bare standing metric repair and whitewashing are statistically tied at extreme severity (the λ⁻d = 0.32 standing hole is deep enough that restarting at the prior 0.5 is no worse); dominance at d=16 needs the §3.8 verifier-side fresh-record flag, which is a policy layer, not the update law. Custodial baseline (free re-entry at default standing) rewards whitewashing at every d — confirmed by construction of the comparison.

On-off cycling (20 honest : 1 defection, d=4, utility = standing-proportional income + fixed loot): protocol immediate feedback goes **net-negative at λ⁻ = 0.02 (−118 utility units)** and is profitable below λ⁻ ≈ 0.01 — the paper's threshold claim reproduced; custodial batched feedback + free re-entry is profitable at every severity d ≥ 2 (+675 at d=4; d=1 neutral because a defection displaces one honest income event in this accounting). Verdict: PASS (qualitative; original generative protocol not archived, accounting conventions stated).

## 5. Expected-loss breach model (fig_expected_loss.png)

Model: E_C = p_org·N_all, E_T = n_dev·p_dev + p_cm·N_all, N_all = n_dev = 3×10⁸. Deterministic — exact arithmetic.

| Quantity | Claim | Re-run | Verdict |
|---|---|---|---|
| E_C at p_org = 0.02/0.03/0.05/0.10 | 6M / 9M / 15M / 30M | 6M / 9M / 15M / 30M | PASS |
| favorable (p_dev=0.005, p_cm=0.001) | 1.8M (≈8× win) | 1.8M (8.3×) | PASS |
| loss case p_dev=0.06 / 0.10 | 18.3M / 30M+ | 18.3M / 30.3M | PASS |
| break-even | p_dev + p_cm < p_org (straight line on log axes) | identical (plotted as contour) | PASS |
| key/guardian loss at p_key=0.005 | +1.5M/yr, same order as the win | 1.5M/yr, plotted as separate access-loss term | PASS |

Heatmap over p_dev ∈ [0.001,0.1] × p_cm ∈ [10⁻⁴,10⁻²] at p_org = 0.05 shows both win and loss regions; honest headline unchanged: variance reduction, not elimination.

## 6. Cold start / event floor (fig_coldstart.png)

Spec: master law as above; honest stream 90% +1 / 10% −1; rate = r_floor + 5·S/day (Poisson); convergence = S within 10% of asymptote S* = 0.75.

| Quantity | Claim | Re-run (5 seeds) | Verdict |
|---|---|---|---|
| events to stabilize from S₀=0 | ~200 (theory 230) | 201 | PASS |
| r_floor = 0 | never converges | never converges (rate stays 0 forever) | PASS (exact — the trap is real) |
| escape days: 0.01/day | 562 | 318 ± 133 | **DEVIATION** (re-run faster; same ordering) |
| 0.05 / 0.1 / 0.5 / 1 / 5 per day | 143 / 139 / 119 / 71 / 23 | 189±32 / 149±22 / 112±11 / 76±14 / 30±9 | PASS within ~35% (re-run systematically modestly faster; original convergence criterion not archived — criterion here: S ≥ 0.9·S*) |

Design requirement stands: a seeded score-independent event floor is mandatory.

## 7. Storage-cost trend (fig_storage_refit.png) — series SOURCED, re-fit performed

Not DATA-REQUIRED: the full Komorowski table (273 drive-price points, 1980–2009) was transcribed from the cited public page (mkomo.com/cost-per-gigabyte), and Backblaze fleet endpoints from the cited blog ($0.114/GB 2009 → $0.0144/GB Nov 2022; −56.36% from 2017). Transcription validated: my full-series slope −0.2497 log₁₀/yr matches Komorowski's own published regression −0.2502 (r = 0.9916).

| Fit | Slope (%/yr) | 95% CI | R² | df |
|---|---|---|---|---|
| **Re-fit, full Komorowski 1980–2009** | **−43.7** | [−44.2, −43.2] | 0.984 | 271 |
| Re-fit extended to 2022 (+Backblaze endpoint) | −43.1 | [−43.7, −42.5] | 0.976 | 272 |
| Backblaze fleet 2009–2022 (endpoints) | −13.9 | — | — | — |
| Backblaze fleet 2017–2022 (endpoints) | −13.2 | — | — | — |
| Paper's printed claim | −31.6 | [−38.3, −24.2] | 0.915 | **7** |

**DEVIATION.** The printed fit is not reproducible from the cited series: df = 7 implies an unrecorded ~9-point subsample; the full series gives a *steeper* long-run decline (−43.7%/yr, halving every 1.2 yr, not 1.8), and the modern era is much *flatter* (~−14%/yr). The printed 1980 anchor "roughly $20,000/GB" also conflicts with the sourced Komorowski 1980 rows ($152k–$700k/GB). Recommendation: restate as an era-split result (long-run ≈ −44%/yr through 2009; ≈ −14%/yr since) or specify the subsample; the paper's NAND-shortage caveat already concedes the trend is not a law.

## 8. Adoption-compounding sensitivity (fig_adoption_sensitivity.png) — new model, labeled assumptions

Toy densification-feedback model Ȧ = A(1−A)[b·W(A) − s₀φ], W = g_act(A; r_floor)·R(K,ℓ)·p_att, with g_act = r/(r+r_h), r = r_floor + 5A events/day, R(K,ℓ) interpolated from the simulated P1b surface; b = 2/yr, r_h = 0.5/day, s₀ = 1/yr, A₀ = 0.02. Outcomes classified: compound (≤10 yr to 50% adoption), stall (>10 yr/never), reversal (collapse below 0.2·A₀).

| Region | Result |
|---|---|
| (r_floor, ℓ) plane at K=4.5 | 39% compound / 28% stall / 34% reversal; reversal for ℓ ≳ 0.30 at r_floor = 0.5; compounding requires r_floor ≳ 0.15/day even at ℓ = 0 |
| same plane at K=6 | 54% / 26% / 20%; reversal only for ℓ ≳ 0.54 — hardened coupling shrinks the failure region but does not remove the low-floor stall |
| (p_att, φ) plane (K=6, ℓ=0.05, r_floor=0.5) | 22% / 24% / 54%; compounding needs p_att ≳ 0.6 at φ = 0.2, or φ ≲ 0.42 at p_att = 0.8 |

Verdict: PASS for §3.10(iii)'s conditional claim — compounding operates only once a seeded event floor, low-leakage measurement, client diversity, and a minimum attesting-provider set are in place; the map now quantifies each failure region. (New quantitative content, no prior printed numbers to deviate from.)

---

## Deviation register (summary)

1. **ℓ\* ≈ 0.02 (P1b):** not resolvable as a point — re-run gives a crossing band ℓ\* ∈ [0.02, 0.10] at 9 seeds; qualitative fragility holds. Print the band.
2. **Robust regions (P1b):** re-run more robust than printed (K=6: ℓ ≈ 0.28 vs 0.15; K=8: ℓ ≈ 0.40 vs 0.25) — paper is conservative; update or note.
3. **Whitewashing at d = 16 (P8):** repair and whitewashing statistically tied under the bare standing metric; dominance needs the §3.8 verifier-side fresh-record flag. Paper's "dominated by repair at every severity" should be scoped to d ≤ 8 plus the policy layer.
4. **Cold-start escape days:** re-run systematically faster (worst: 318 vs 562 days at r_floor = 0.01/day); trap result exact. Convergence criterion should be archived with the numbers.
5. **Storage fit:** printed −31.6%/yr (df = 7) not reproducible from the cited Komorowski/Backblaze series; full-series re-fit −43.7%/yr [−44.2, −43.2] (matches Komorowski's own published regression), modern era ≈ −14%/yr. Restate era-split or specify the subsample.

## Figure index

- `figP1_coherence.png` — P1: R(t) coupled vs isolated (8 replicas), steady-state boxplots, atan-artifact side panel (200 seeds).
- `figP1b_surface.png` — P1b headline: R(K,ℓ) heatmap with R = 0.3/0.5/0.7 contours, operating point, robust-region annotations; leakage-fragility slice with ℓ\* band.
- `figP5_transfer_entropy.png` — surrogate-corrected TE, 4 flows, 95% CIs, 0.01-bit detection floor, no ratio headline.
- `figP8_sybil_deterrence.png` — Sybil cost vs attestation multiplier (log–log) with unattested and rollup baselines; wall-clock time floor; whitewash-vs-repair by severity; on-off net utility vs λ⁻.
- `fig_expected_loss.png` — log₁₀(E_T/E_C) heatmap with break-even contour and win/loss regions; expected-loss curves with the key/guardian access-loss term.
- `fig_coldstart.png` — cold start from S₀ = 0 (201 events); time-to-stabilize vs r_floor with the never-converging trap and paper-value comparison.
- `fig_storage_refit.png` — sourced Komorowski + Backblaze series, full-series re-fit vs printed claim; era-resolved decline rates.
- `fig_adoption_sensitivity.png` — adoption-compounding maps with stall/reversal regions over (r_floor, ℓ) at K = 4.5/6 and over (p_att, φ).
