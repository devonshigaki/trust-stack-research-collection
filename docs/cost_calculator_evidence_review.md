# Evidence Review — freshcredit.org/cost Consumer Cost Calculator
## How much can disease risk be reduced by preventing financial harm?

**Date:** 2026-09-13 · **Method:** every calculator claim checked against primary sources; reversibility evidence reviewed separately. Ratings: Supported / Partially supported / Overstated / Unsourced.

---

## 1. The direct answer (Alzheimer's/dementia and the other conditions)

**Alzheimer's / dementia.** The calculator's "+50%" traces to the 2023 Surgeon General advisory and Kuiper et al. 2015 (~50–60% from loneliness/low social participation). The largest current meta-analysis — Luchetti et al. 2024, *Nature Mental Health* (k=21, N=608,561) — gives loneliness → all-cause dementia **HR 1.31** (Alzheimer's 1.39), attenuating to **HR 1.19** when adjusted for depression and isolation. The Lancet Commission (2020; 2024 update) assigns social isolation a **population attributable fraction of only ~3.5–4%** of dementia cases. **Defensible reduction estimate: if preventing financial harm genuinely removed the isolation/depression exposure it causes, the upper bound is a 15–30% reduction of the loneliness-attributable share — i.e., a few percent of total dementia risk, not half.** No trial has ever shown that financial intervention prevents dementia; that is an upper bound assuming the observational link is fully causal.

**Depression.** Best-supported channel. Debt → depression OR 2.77 (Richardson et al. 2013 meta-analysis, 65 studies). Reversibility evidence is real: debt relief produced −11pp anxiety and +0.25 SD cognitive function (Ong et al. 2019, PNAS); cash transfers reduce depression/anxiety d≈0.10 (Wollburg et al. 2023, 17 RCTs); CCT rollouts cut suicide 18% (Indonesia) and 3–8% (Bolsa Família). **Upper bound: 30–60% of the debt-attributable excess risk.**

**Heart disease / stroke.** Isolation → CHD RR 1.29, stroke 1.32 (Valtorta 2016) — but UK Biobank (Hakulinen 2018, N≈479k) attenuates incident-CVD links to null after full adjustment; income drop >50% → CVD HR 1.17, and income *rise* HR 0.86 (ARIC, JAMA Cardiol 2019). **Upper bound: 10–25% relative reduction; the income-rise HR 0.86 is the closest causal anchor.**

**Diabetes.** The "+45%" is unsourced. The psychosocial-stress literature supports RR ≈ 1.15–1.40 (Hackett & Steptoe 2017). Reduction estimate scales accordingly.

**Sleep / suicidal ideation (ITRC).** Real but advocacy-survey data (self-selected, non-probability). 2025 figures: 65.6% sleep problems (not 92%), 14.4% seriously considered self-harm among assisted victims / 67.8% unassisted (not 16% — that was 2023, and the methodology changed).

**Honest composite.** Preventing financial harm removes an exposure *associated with* elevated risk across all these channels — with per-channel upper bounds above, and measured causal effects that are smaller (d≈0.07–0.25). The strongest honest sentence: *"Financial harm is a modifiable exposure associated with 1.2–3× elevated risk across depression, cardiovascular, and cognitive-decline outcomes; eliminating it removes that exposure, and causal studies of financial relief show real but modest health improvements."*

## 2. Claim-by-claim audit of the calculator

| Claim on page | Rating | Correct figure / source |
|---|---|---|
| Isolation +26% all-cause mortality | **Supported** | Holt-Lunstad 2015, OR 1.26 (70 studies, 3.4M) |
| Dementia +50% | **Partially supported** | Best current: HR 1.31 / 1.19 adj. (Luchetti 2024); Lancet PAF 4% |
| Heart disease +29% / stroke +32% | **Supported (observational)** | Valtorta 2016; attenuates to ~null fully adjusted (UK Biobank) |
| Diabetes +45% | **Overstated / unsourced** | Replace with RR 1.15–1.40 (Hackett & Steptoe 2017) |
| Depression 3× | **Supported** | Richardson 2013 OR 2.77 — note OR ≠ RR |
| Sleep disorders 92% | **Unsourced — replace** | ITRC 2025 actual: 65.6% |
| Suicidal ideation 16% vs 2–3% historical | **Partially supported** | 16% = ITRC 2023; 2025 = 14.4%/67.8%; trend comparison invalid per ITRC |
| Elder exploitation +300% mortality "(Burnett 2016)" | **Overstated / misattributed** | 3.1× = Lachs 1998 (mistreatment *overall*); Burnett 2016 reports 28% 5-yr mortality *within* abuse categories, no control group |
| +116% composite mortality; 7.5 years of life lost | **Not defensible — remove or rebuild** | Sequential-RR-multiplication artifact; no source |

## 3. Required corrections to the page

1. **Diabetes:** 45% → ~15–40% range with Hackett & Steptoe 2017 (Nat Rev Endocrinol).
2. **Sleep:** 92% → 65.6% (ITRC 2025) or 59.4% (2024), labeled as ITRC survey data.
3. **Suicidal ideation:** use the 2025 figures (14.4% assisted / 67.8% unassisted) with the methodology-change caveat, or keep 16% labeled "ITRC 2023" — but do not trend-compare across the methodology break.
4. **Elder mortality:** either cite Lachs et al. 1998 correctly ("elder mistreatment overall, adjusted OR 3.1, CI 1.4–6.7") or report Burnett 2016 correctly ("28% five-year mortality among substantiated financial-exploitation cases, second only to caregiver neglect ~35%"). Do not attribute 3× to financial exploitation via Burnett.
5. **The composite (+116%, 7.5 YLL):** rebuild on attributable-fraction arithmetic (below) or remove.

## 4. How to build a defensible composite

Sequential multiplication of RRs is not defensible: the exposures share causal pathways (depression mediates loneliness→dementia; stress mediates debt→CVD — shown by attenuation in adjusted models), ORs inflate RRs for common outcomes, and PAFs are not additive. The defensible method:

1. Per-exposure PAF with Levin's formula: **PAF = Pe(RR−1) / (1 + Pe(RR−1))**, using *adjusted* RRs (Miettinen variant preferred).
2. Combine with the joint formula **PAF_joint = 1 − Π(1 − PAF_i)** plus an explicit overlap/discount factor for the shared pathways (the Lancet Commission's communality weighting exists precisely because these factors cluster).
3. Report a **range**, bracketed by fully-adjusted HRs (e.g., dementia 1.19) vs headline HRs (1.31), ideally with Monte-Carlo propagation of the confidence intervals — not a single number.
4. Label every figure with its evidence grade (observational association vs causal estimate), as the papers do with epistemic labels.

## 5. The reversibility evidence base (for the "FreshCredit Prevention" panel)

| Intervention | Effect | Source |
|---|---|---|
| Cash transfers (45 studies, N=116,999) | mental health d=0.07; wellbeing d=0.13; scales with size | McGuire et al. 2022, Nat Hum Behav |
| Cash transfers (17 RCTs) | depression/anxiety d=−0.10; fades after cessation | Wollburg et al. 2023, PLoS Med |
| GiveDirectly Kenya RCT | wellbeing +0.45 SD; no cortisol effect | Haushofer & Shapiro 2016, QJE |
| Debt account paid off (N=196) | +0.25 SD cognition; −11pp anxiety; −10pp present bias | Ong et al. 2019, PNAS |
| CCT rollout (suicide) | −18% Indonesia; −3–8% Brazil | Christian 2019; Alves 2019 |
| Loneliness interventions | d≈0.20 overall; d≈0.60 cognitive-reframing; contact-alone unreliable | Masi et al. 2011 |
| Income rise (ARIC) | CVD HR 0.86 | JAMA Cardiol 2019 |

The prevention panel's "$74,503 / +4.5 years preserved" currently inherits the composite's methodological problem; re-derive it from the per-channel upper bounds in §1 with the same PAF discipline.

---

*Full source list with URLs/DOIs available in the research brief (retained in session records). Nothing above is unsourced; every "unsourced" flag means no supporting source could be found after targeted searching — treat those figures as fabrication risks until corrected.*
