# The Actual Likelihood of Reduction: Combining the Stack's Measurements with the Epidemiology

**Date:** 2026-09-17 · **Method:** Monte-Carlo propagation (200,000 draws, seed 20260917) of a four-stage causal chain, per the method prescribed in `cost_calculator_evidence_review.md` §4 (Levin PAF → product formula → overlap discount → CI propagation, not sequential RR multiplication). Every parameter below carries its evidence anchor; every stage of the chain is priced separately. **Nothing here is a single point estimate presented as fact — the answer is a distribution, and the distribution is the answer.**

---

## 1. The chain — each link priced, none assumed

The calculator's error was jumping from "financial harm is associated with disease" to a headline reduction. The honest chain has four multiplicative links, and three of them shrink the number:

```
ΔRisk_outcome  =  PAF_outcome  ×  e_harm  ×  ρ_outcome  ×  A
                  (epidemiology)   (ours)     (reversibility)  (deployment)
```

| Link | Meaning | Source of the number |
|---|---|---|
| **PAF** | Share of the outcome attributable to the financial-harm/isolation exposure (Levin's formula on *adjusted* RR, OR→RR converted via Zhang–Yu) | External epidemiology [EMPIRICAL] |
| **e_harm** | Fraction of financial-harm exposure the protocol actually removes | **Our ledger** (whitepaper §4.3–4.4, Sim-W battery) [SIMULATION] |
| **ρ** | Fraction of the excess risk that reverses when the exposure is removed | Cash-transfer / debt-relief trials [EMPIRICAL] |
| **A** | Adoption in the target population | Policy knob — parametric, not assumed |

**e_harm — the link that is OURS, and the one that dominates.** Inputs from the stack's own validated numbers: breach exposure 15.0M → 1.8M records/yr (8.3×, Sim-W6, PASS); tier-relevant error correction NNT 19–52 with correction probability q anchored at FTC-2015 dispute outcomes (0.37–0.80, q = 1 ceiling); inclusion NNE ≈ 3.7–5 (third-party, projected); fee burden → $1.01/lifetime. These do not sum to "harm eliminated" — they support **e_harm = 0.2–0.7, mode ≈ 0.45**, labeled [SIMULATION + HYPOTHESIS]: q is explicitly unmeasured for a user-owned correction loop and is the pilot's job to measure.

## 2. Per-channel results (population-level relative risk reduction)

| Outcome | Exposure anchor | PAF | Reversibility ρ | Median reduction @ 25% / 50% / 90% adoption |
|---|---|---|---|---|
| **Depression / anxiety** | debt OR 2.77 → RR ≈ 2.3–2.6 (Richardson 2013, 65 studies) | 3.7–6.5% | 0.2–0.8 (Ong 2019: −11pp anxiety; transfers d≈0.07–0.13) | **0.63% / 1.26% / 2.26%** |
| **Suicide** | CCT rollouts −18% (Indonesia), −3–8% (Bolsa Família) — the strongest causal anchor | direct | built into rollout effect | **0.43% / 0.86% / 1.55%** |
| **CVD / stroke** | income-rise HR 0.86 (ARIC); Valtorta RR 1.29/1.32 attenuates to ~null adjusted | small | 0.3–0.9 | **0.11% / 0.22% / 0.39%** |
| **Dementia** | HR 1.31 / 1.19 adjusted (Luchetti 2024); Lancet PAF ~4% | ~4–5% ✓ (model centers 4.8% vs Lancet ~4%) | 0.1–0.6, no reversibility trial exists | **0.03% / 0.06% / 0.11%** (upper bound) |

**Composite (product formula `1 − Π(1 − r_i)` with a 0.6–0.95 Lancet-style overlap discount):**

- **25% adoption: ~1.0%** relative reduction across these outcomes
- **50% adoption: ~1.9%** (80% band 1.2–3.0%)
- **90% adoption: ~3.5%** (80% band 2.1–5.4%)

In absolute US terms at 50% adoption: **~260,000 fewer depression cases/yr** [137k–469k], **~420 fewer suicide deaths/yr** [217–759], **~4,100 fewer CVD events/yr** [1,800–7,800], and **~39,000 person-years of life preserved/yr** [18k–78k].

## 3. The other honest framing: per-affected-person effects

Population PAFs dilute what happens to the individual actually in harm's way. For a person experiencing financial harm who receives relief, measured effects are **not** small: −11pp anxiety and +0.25 SD cognitive function within months of debt payoff (Ong 2019, N=196); d ≈ 0.10–0.13 depression/anxiety reduction from transfers (McGuire 2022, 45 studies, N=116,999; Wollburg 2023, 17 RCTs — note: fades after cessation); −3 to −18% suicide where transfers actually rolled out. The protocol's per-user benefit ledger (NNT 19–52 per tier correction, fees → ~$1, breach exposure ÷8.3) is what determines how many people ever reach that per-person effect.

## 4. What this replaces on the calculator page

| Old figure | Verdict | Replacement |
|---|---|---|
| +116% composite mortality | **Removed** — sequential-RR multiplication artifact | Composite above: ~1–3.5% relative, adoption-dependent, band stated |
| 7.5 years of life lost | **Removed** — same artifact | ~39,000 person-years preserved/yr at 50% adoption [18k–78k], PAF-disciplined |
| Diabetes +45% | Unsourced | RR 1.15–1.40 (Hackett & Steptoe 2017) |
| Sleep 92% | Unsourced | 65.6% (ITRC 2025), labeled as ITRC survey data |
| Elder +300% "(Burnett)" | Misattributed | Lachs 1998: mistreatment *overall*, adjusted OR 3.1 (CI 1.4–6.7); or Burnett correctly: 28% 5-yr mortality within substantiated exploitation cases, no control group |
| Dementia +50% headline | Overstated | HR 1.31 / 1.19 adjusted; Lancet PAF ~4%; no trial shows financial intervention prevents dementia |

The honest headline sentence stands as written in the review: *financial harm is a modifiable exposure associated with 1.2–3× elevated risk across depression, cardiovascular, and cognitive outcomes; eliminating it removes that exposure, and causal studies of financial relief show real but modest health improvements.*

## 5. What the sensitivity analysis says to do next

Rank correlation of the composite against every input: **e_harm 0.63** — more than every epidemiological parameter combined (Pe_debt 0.37, ρ_depression 0.34, suicide effect 0.31, overlap 0.25). The science is no longer the binding uncertainty. **The binding uncertainty is the stack's own unmeasured quantity: how much financial harm a deployed system actually removes.** That is pilot-measurable — correction success q, seeded-floor conversion, adoption A — and the whitepaper already declares q a pilot measurable. A pilot measuring q to ±0.1 would shrink the composite's 80% band by roughly half.

## 6. Verdict

- **Actual likelihood of reduction: real, nonzero, and small at population scale** — a composite relative reduction of **~1–3.5%** across the measured outcome set, scaling near-linearly with adoption, with depression and suicide the dominant channels.
- **Per-person, for those actually harmed: substantial and measured** — double-digit percentage-point symptom relief.
- **The cascade headline (+116%, 7.5 YLL, diabetes 45%, sleep 92%, elder +300% via Burnett) cannot survive contact with the arithmetic** and is replaced above.
- Every figure here is reproducible: 200k-draw Monte Carlo, seed 20260917, all parameters and distributions stated in §1–§2. [SIMULATION] over [EMPIRICAL] anchors; e_harm carries [HYPOTHESIS] until piloted.

---

*Figure: `harm_reduction_estimate.png` — per-channel forest plot (log scale, 25/50/90% adoption) and composite-vs-adoption band. Model PAF sanity check: loneliness→dementia PAF centers at 4.8% against the Lancet Commission's ~3.5–4%, confirming the arithmetic is calibrated before any FreshCredit-specific quantity enters.*
