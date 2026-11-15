# DOCAS-GATE-1 — Registered Perturbation-Study Protocol and Independent-Rater Protocol for the DOCAS Exact-Form Claim

**Registration type:** OSF pre-registration (deposit pending; OSF DOI to be assigned). **Self-attestation status:** internally specified and timestamped in this deposit; external OSF registration pending — until the registration exists, the frozen-criteria claims herein are self-attested.
**Source document:** `CARRIER_GATE.md` (repair-era research output); content unchanged, retitled for deposit as registration DOCAS-GATE-1.
**Prepared by:** RES-4 (research agent)
**Date:** 2026
**Scope:** The DOCAS framework claims that trust dynamics decompose into five neuromodulatory channels (dopamine/expectation, oxytocin/validation, cortisol/recognition, adrenergic/activation, serotonin/stabilization) whose interactions are described by a gain matrix M that is *diagonally dominant* (the "exact-form" claim). Current instruments (HRV/sleep/activity wearables; TRIBE-style text→fMRI encoding models) are several inference steps removed from neuromodulatory tone and therefore cannot falsify diagonal dominance. This document specifies what *can*: (a) the verified pharmacological-perturbation literature, (b) a depositable registered perturbation protocol, (c) the independent-rater protocol for the CLICS concept sets and offer-stimulus categories, (d) honest feasibility and cost notes.

**Core thesis of this document:** Diagonal dominance is a claim about *selectivity of causal perturbations*, and the only established method for testing causal selectivity of human neuromodulatory systems is double-blind, placebo-controlled, within-subject pharmacological challenge with channel-selective probes, combined with a task battery containing expectation-violation events for every channel. Wearables and encoding models can then be validated *against* the perturbation ground truth — they cannot substitute for it.

---

## (a) VERIFIED LITERATURE TABLE

### A1. Dopamine / expectation channel

| Study | Probe & dose | Design, N | Readout | Result & effect size | Citation |
|---|---|---|---|---|---|
| Pessiglione et al. 2006 | L-DOPA 100 mg vs haloperidol 1 mg vs placebo | Between-subject, 3 groups, N=30; fMRI | Monetary instrumental RL task (75/25% probabilistic gain/loss pairs); striatal RPE BOLD | L-DOPA > haloperidol on reward-seeking (gain condition only); striatal PE signal modulated. No drug effect on loss avoidance. | Science 314:904–908. DOI: 10.1126/science.1130285 |
| Michely et al. 2023 (replication attempt) | L-DOPA 150 mg, haloperidol 2 mg, placebo | **Within-subject crossover**, N=31 males, fMRI | Stationary RL task + RL-DDM modeling | **Failed to replicate** the L-DOPA>haloperidol learning effect and the striatal PE effect; both drugs *reduced decision thresholds* (boundary separation). Critical honesty anchor: the canonical DA-RL behavioral result is fragile at N=30–31. | Nat Commun 14:7054. DOI: 10.1038/s41467-023-41130-y |
| Halahakoon et al. 2024 | Pramipexole, titrated to 1 mg/day × 2 weeks vs placebo | Between-subject RCT, N=40 healthy; fMRI | Probabilistic instrumental learning task (PILT); RL model (reward sensitivity / temperature / value decay) | Pramipexole ↑ reward-condition choice accuracy, no effect on loss condition; mechanism = reduced value decay; ↑ OFC BOLD during win expectation, ↓ vmPFC RPE response. | Biol Psychiatry 95(9):839–849. PMID: 37330165. DOI: 10.1016/j.biopsych.2023.06.020 |
| Rutledge et al. 2015 | L-DOPA 150 mg vs placebo | Within-subject, N=30 | Gambling task | L-DOPA ↑ gambling propensity. | (tabulated in Martins et al. 2021 review) J Neurosci 35:13884–13892. DOI: 10.1523/JNEUROSCI.1455-15.2015 |
| Westbrook et al. 2020 | Methylphenidate 20 mg / sulpiride 400 mg | Within-subject, N=50; [18F]FDOPA PET baseline | Effort-based choice | Catecholamine ↑ willingness to exert effort, strongest in low-baseline-DA-synthesis individuals (inverted-U). | Neuropsychopharmacology 45:1331–1341. DOI: 10.1038/s41386-020-0690-9 |
| Eisenegger et al. 2014; Jocham et al. 2011 | Sulpiride 800 mg (↓) / amisulpride 200 mg (low-dose presynaptic) | Between/within, N≈20–30 | RL tasks + fMRI | High-dose D2 blockade impairs reward learning; low-dose amisulpride *enhances* it — dose-direction non-monotonicity is a real confound for "one-probe" claims. | Jocham: J Neurosci 31:1606–1613. DOI: 10.1523/JNEUROSCI.5183-10.2011 |
| Martins et al. 2021 (review) | All DA manipulations in healthy adults | Systematic tabulation (N per study typically 16–50) | Reward functioning | Many nulls; effects dose-, task-, and baseline-dependent; **typical single-session DA challenge N=20–40 within / 15–21 per arm between**. | Front Psychol. PMC7855845. |

**Take-aways for the gate:** (1) Within-subject crossover is standard and detects medium effects at N≈20–40. (2) The flagship result (Pessiglione) failed direct replication at N=31 — so single-probe/single-task designs are not credible evidence; the gate needs target-engagement checks and multiple readouts. (3) D2 pharmacology is non-monotonic (presynaptic vs postsynaptic), so a *directional pair* (agonist + antagonist) is safer than a single dose for claiming channel specificity.

### A2. Noradrenaline (adrenergic) / activation channel

| Study | Probe & dose | Design, N | Readout | Result | Citation |
|---|---|---|---|---|---|
| O'Callaghan et al. 2025 | Atomoxetine 40 mg single dose vs placebo | Double-blind crossover, Parkinson's patients + age-matched controls | RL task + computational modeling + pupillometry | Atomoxetine ↑ learning (decision-noise ↓, more exploitative); **↑ baseline pupil diameter, ↑ phasic pupillary response to feedback**; pupil effects correlate with behavioral improvement. Direct evidence that 40 mg atomoxetine is a validated pupillometric target-engagement probe. | Commun Biol 8:189. DOI: 10.1038/s42003-025-08627-2 |
| Loughnane et al. 2019 | Methylphenidate, atomoxetine, citalopram, placebo | Double-blind 4-arm crossover, healthy adults | EEG oddball; P3b evidence-accumulation signature | Methylphenidate & atomoxetine (catecholamines) shortened RT via ↑ P3b buildup rate; citalopram (SSRI) did **not** — a demonstrated pharmacological *dissociation* between channels in one design. | J Cogn Neurosci 31:1044–1053. DOI: 10.1162/jocn_a_01393 |
| Warren et al. 2017 | Atomoxetine 40 mg vs placebo | Double-blind crossover, N=22 | Directed vs random exploration task | NA manipulation modulated exploration policy. | Psychopharmacology. DOI: 10.1007/s00213-017-4680-9 |
| De Martino et al. 2008 | Propranolol 40 mg (and 20 mg), nadolol 40 mg (peripheral control), reboxetine 4 mg | Double-blind, between-subject arms (N≈10–15/arm across 3 experiments) | Attentional blink (RSVP) | 40 mg propranolol impaired T2 detection regardless of valence; 20 mg and peripheral-only nadolol did not; reboxetine selectively ↑ emotional-T2 detection. Dose threshold and central-specificity controls demonstrated. | Psychopharmacology 197:127–136. DOI: 10.1007/s00213-007-1015-5 |
| Jepma et al. 2016, 2018 | Atomoxetine (NRI) / clonidine (α2-agonist, ↓NA) | Crossover | Volatility learning | Atomoxetine ↑, clonidine ↓ contingency updating under volatility — opposite-direction probes on the same channel. | (as reviewed; Plat thesis 2025, HAL tel-05457529) |
| Lawson et al. 2021 | Propranolol | — | Volatility learning | β-blockade modulates volatility-dependent learning rates. | (as reviewed, ibid.) |

**Take-aways:** Atomoxetine 40 mg with pupillometry is the best-instrumented NA probe (objective target engagement in the same session). Propranolol requires ≥40 mg for central behavioral effects; include nadolol as a peripheral-only control if propranolol is used. Clonidine provides the opposite-direction probe but is sedating.

### A3. Serotonin / stabilization channel

| Study | Probe & dose | Design, N | Readout | Result & effect size | Citation |
|---|---|---|---|---|---|
| Schweighofer et al. 2008 | Dietary tryptophan depletion (0 g) / control (2.3 g) / loading (10.3 g) | Within-subject, double-blind, counterbalanced, **N=20 males** | Experienced-delay discounting task + RL meta-parameters (γ discount, α learning rate, β temperature) | Low 5-HT steepened delay discounting (γ: 0.822 depletion vs 0.867 control vs 0.868 loading; main effect F(2,190)=5.37, p=.009 → ηp²≈0.053, **f≈0.24**); no effect on learning rate or choice variability. Direct, selective support for a 5-HT→temporal-stability mapping — but a small effect, noted by the authors themselves. | J Neurosci 28:4528–4532. DOI: 10.1523/JNEUROSCI.4982-07.2008 |
| Worbe et al. 2014 | Acute tryptophan depletion (ATD) | Crossover | 4-choice serial RT task ("waiting impulsivity"), cross-species translational | ATD induced premature responding (waiting impulsivity). | Neuropsychopharmacology 39:1519–1526. DOI: 10.1038/npp.2014.2 |
| Dougherty et al. 2010 | ATD vs balanced placebo | Between-task, N=90 (30 per impulsivity task) | Response initiation / inhibition / consequence sensitivity | ATD ↑ response-initiation and consequence-sensitivity impulsivity at 5–6 h peak depletion (plasma TRP −77% to −94%); **no effect on response inhibition** — within-channel dissociation matters for readout choice. | Int J Neuropsychopharmacol. PMC3195237. |
| Cools et al. 2008 | ATD | Crossover | Reward vs punishment prediction | ATD enhanced punishment prediction but did not affect reward prediction — DA/5-HT opponency evidence. | Neuropsychopharmacology 33:2291–2299. DOI: 10.1038/sj.npp.1301542 |
| Crockett et al. 2010 | ATD | Crossover | Delay discounting + Ultimatum Game | ATD ↑ impulsive choice (log discount parameter); Δplasma TRP correlated with Δdiscounting, r=0.572, p=.008; correlated with ↑ unfair-offer rejection. | (reported analysis; cf. Crockett et al. 2008, J Neurosci 28:10777–10780) |
| Skandali et al. 2018 | Acute escitalopram 20 mg vs placebo | Between-subject | CANTAB probabilistic learning, stop-signal, ID/ED, emotional processing | Acute SSRI **impaired** probabilistic learning (↑ lose-shift after misleading negative feedback), improved response inhibition (↓ SSRT) — acute SSRI effects are paradoxical vs chronic. | Neuropsychopharmacology 43:2645–2651. DOI: 10.1038/s41386-018-0229-z |
| Langley et al. 2023 | Escitalopram 10 mg/day × 3 weeks vs placebo | Double-blind semi-randomized, N=66 (34/32) | PRL + model-based/model-free task, hierarchical Bayesian modeling | Chronic SSRI ↓ reinforcement sensitivity on both tasks (Reward×Group coeff −0.34, p<.01) — "blunting." | Neuropsychopharmacology 48:664–670. DOI: 10.1038/s41386-022-01498-2 |

**Take-aways:** ATD is the strongest available 5-HT *depletion* probe (objective biochemical target engagement: plasma TRP −77–94% at 5–6 h). The "patience/stabilization" readout exists and is selective in Schweighofer (γ moved, α and β did not — a within-task dissociation that is exactly the kind of diagonal-dominance evidence DOCAS needs), but f≈0.24 means per-probe tests must be powered for small-to-medium effects. Acute SSRI is a *weak and sometimes paradoxical* opposite-direction probe; do not rely on it alone.

### A4. Cortisol / recognition (threat-mismatch) channel

| Study | Probe & dose | Design, N | Readout | Result & effect size | Citation |
|---|---|---|---|---|---|
| Lovallo et al. 2010 | Hydrocortisone 10 mg IV bolus vs saline | Double-blind between, N=21; continuous fMRI | Resting BOLD dynamics | Amygdala/parahippocampal BOLD ↓, **effect size approaching d=1.0** at 20–25 min post-injection, persisting ≥40 min. Establishes timing window and magnitude of a controlled glucocorticoid probe. | NeuroImage 49:864–870. DOI: 10.1016/j.neuroimage.2009.08.002 |
| Buchanan et al. 2001 | Hydrocortisone 20 mg oral | — | Plasma/salivary cortisol | 20 mg oral produces blood levels comparable to laboratory mental-stress responses — the reference dose for a "stress-equivalent" pharmacological probe. | Psychoneuroendocrinology 26:477–490. DOI: 10.1016/S0306-4530(01)00004-5 |
| Goodman et al. 2017 (meta-analysis) | Trier Social Stress Test (TSST) | Meta-analysis across TSST studies | Salivary cortisol reactivity | Robust cortisol response, **d ≈ 0.9–1.0** (best with 16–30 min acclimation, mixed-gender panel); VR-TSST achieves only d≈0.65. | Goodman et al., Psychoneuroendocrinology 84:26–40 (2017); VR meta-analysis: DOI 10.1016/j.psyneuen.2019.104412 |
| Simoens et al. 2007 | TSST (EEG-adapted) | Between | Mismatch negativity (MMN), N1/P2, salivary cortisol | Cortisol inversely related to duration-deviant MMN amplitude — direct evidence linking the cortisol channel to *mismatch/deviance detection* readouts. | Psychophysiology 44:106–111. PMID: 17241138. DOI: 10.1111/j.1469-8986.2006.00476.x |
| Terfehr et al. 2011 | Hydrocortisone 10 mg vs placebo | Between (MDD + controls; controls n≈56) | Working memory with emotional distractors | Hydrocortisone impaired WM specifically with *negative* distractors in healthy controls — valence-specific cortisol effect. | Psychopharmacology 218:621–629. |
| Acute stress ERP study (Neurobiol Stress) | TSST vs placebo, N=78 | Between | ERP (cue-N2, SPN, RewP, P3) in reward task | Acute stress blunted reward-magnitude sensitivity in **anticipation** (cue-N2, SPN) but not **consumption** (RewP, P3) — a cortisol-channel readout should target anticipatory/threat-mismatch, not consummatory, epochs. | Neurobiol Stress (2021). |

**Take-aways:** Hydrocortisone 20 mg oral (or 10 mg IV) is a well-controlled probe with large (d≈1.0) physiological effects; TSST is the ecologically valid alternative with d≈0.9–1.0 on cortisol but poor standardization of the *cognitive* state. The channel readout should be anticipatory threat/mismatch responses (MMN family, anticipatory ERPs, threat-of-shock paradigms), not consummatory reward responses.

### A5. Oxytocin / validation channel — what is defensible given the null literature

| Study | Probe | Design, N | Readout | Result | Citation |
|---|---|---|---|---|---|
| Kosfeld et al. 2005 | Intranasal oxytocin (IN-OT) | Between, N≈29/arm | Trust game | Original trust-enhancement claim; borderline, small N. | Nature 435:673–676. DOI: 10.1038/nature03701 |
| Nave, Camerer & McCullough 2015 | — | Critical review + meta-analysis of 7 trust-game studies, 481 subjects | Trust behavior | **Combined effect null: d = 0.077 [95% CI −0.124, 0.278], p=.45.** Cumulative evidence "does not provide robust convergent evidence that human trust is reliably associated with OT." | Perspect Psychol Sci 10:772–789. DOI: 10.1177/1745691615600138 |
| Declerck et al. 2020 | IN-OT | **Registered replication**, >95% powered, double-blind placebo-controlled | Trusting behavior | **Null.** | Nat Hum Behav 4:646–655. DOI: 10.1038/s41562-020-0878-x |
| Leng & Ludwig 2016 | — | Mechanistic critique | Pharmacokinetics | Only ~0.005% of a nasal dose reaches CSF; CNS target engagement of IN-OT is contested. | Biol Psychiatry 79:243–250. DOI: 10.1016/j.biopsych.2015.05.003 |
| Leppanen et al. 2017 | IN-OT | Meta-analysis, 33 studies | Emotion recognition | Small improvements in basic emotion recognition, strongest for fear — the most defensible residual IN-OT effect. | Neurosci Biobehav Rev 80:101–109. DOI: 10.1016/j.neubiorev.2017.05.004 |
| Paloyelis et al. 2016 | IN-OT | Within, ASL-MRI | Cerebral blood flow | Spatiotemporal CBF profile post-IN-OT — indirect central engagement evidence, not a behavioral trust effect. | Biol Psychiatry 79:693–705. DOI: 10.1016/j.biopsych.2014.10.005 |
| Power implication (from schizophrenia meta) | IN-OT | Meta-analytic | High-level social cognition | Small residual effect SMD≈0.20 would need **N=199 within-subject** for 80% power — far beyond typical IN-OT studies (median n≈35, power ≈21%). | Schizophr Bull Open. PMC5737621. |

**Defensible position for the gate:** The oxytocin arm is included as a *registered falsification probe of the framework's mapping*, not as a presumed-valid trust manipulation. Pre-registered expectation: near-null diagonal entry (d≈0.08–0.20). If the DOCAS "oxytocin/validation" channel readout moves under IN-OT with a large effect while the trust literature's gold-standard behavioral readout does not, that is evidence *against* the channel's construct validity as currently labeled. The honest alternative is to treat channel 5 as "social validation/affiliation (putatively oxytocin-linked)" and use a *behavioral* validation-manipulation (experimenter-administered acceptance/rejection feedback, e.g., social-evaluative paradigms) as the primary perturbation, with IN-OT as a secondary pharmacological probe.

### A6. PET imaging for neuromodulator systems

| System | Tracer(s) | What it measures | Sensitivity to endogenous release | Sample norms / reliability | Citation |
|---|---|---|---|---|---|
| Dopamine D2/D3 | [11C]raclopride; [11C]PHNO; [18F]fallypride | Receptor availability (BP_ND); displacement by endogenous DA | **Amphetamine challenge: ~10.9% ΔBP_ND; cognitive tasks: only ~2.7%** (4× smaller; meta-analysis of raclopride studies, Mol Psychiatry 2026, DOI: 10.1038/s41380-026-03826-7). Task-evoked DA is near/below detection threshold — a 2022 dual-bolus feasibility study (N=9 test–retest, N=10 task) found **no detectable BP change** from a reinforcement-learning task despite excellent reproducibility (MAD ~1.1%, ICC 0.959) | Typical human challenge PET: N=6–15 per group; striatal test–retest ICC >0.8 over 5 weeks (Alakurti et al. 2015) | DOI: 10.3389/fpsyt.2022.811136; Boileau et al. 2007 J Neurosci 27:3998 (conditioned DA release, VS ΔBP −23%) |
| DA synthesis | [18F]FDOPA | Presynaptic synthesis capacity (tonic trait) | Trait measure, not phasic release | Used as baseline-capacity covariate (Westbrook 2020) | — |
| Serotonin | [11C]DASB (SERT); [11C]WAY-100635 & [11C]CUMI-101 (5-HT1A); [18F]altanserin & [11C]Cimbi-36 (5-HT2A); [11C]AZ10419369 (5-HT1B) | Receptor/transporter availability; occupancy | Only **two** tracers shown sensitive to endogenous 5-HT release: [11C]AZ10419369 (5-HT1B) and [11C]Cimbi-36 (5-HT2A); CUMI-101 used in an SSRI/ATD challenge (Selvaraj et al. 2012, Mol Psychiatry 17:1254–1260). Occupancy studies (e.g., SERT occupancy ~50–80% after SSRI) are routine. | Occupancy studies typically N=6–16; regional ICCs variable (0.4–0.8) | PET/MR review: DOI 10.1186/s12993-020-0163-4 (PMC7238372); DASB occupancy: DOI 10.3389/fnmol.2019.00172 |
| Noradrenaline | [11C]MRB (methylreboxetine) | NET availability/occupancy | **No validated paradigm for endogenous NA release displacement.** NET occupancy imaging exists; phasic NA cannot currently be measured with PET. | Small occupancy cohorts | (tracer inventory: PMC11684923, Table 3) |
| Cortisol | None | — | Cortisol crosses the BBB freely; measured in plasma/saliva — PET unnecessary for this channel. | — | — |
| Oxytocin | None | — | No oxytocin-receptor PET tracer in routine human use. | — | — |

**PET verdict:** PET is feasible and standard for DA (raclopride displacement under amphetamine, ICC >0.8) and for 5-HT *occupancy*, but (i) task-evoked (non-pharmacological) release is mostly below detection threshold, (ii) NA and oxytocin have no endogenous-release paradigm, (iii) multi-tracer within-subject designs are constrained by radiation dose (≈2–3 scans/subject/year at ~5 mSv/scan for C-11 tracers) and on-site cyclotron requirements for C-11. **PET therefore cannot be the primary instrument for a 5-channel gain-matrix estimate**; its role is a *validation substudy* on a subset (e.g., raclopride displacement during the DA session) to confirm that the behavioral/physiological readouts track a molecularly verified channel perturbation.

---

*(document continues in part 2: the registered protocol)*


---

## (b) THE REGISTERED PROTOCOL — "DOCAS-GATE-1"

*Written to be depositable as an OSF registration. Placeholders in [brackets] are the only site-specific items.*

### 1. Title
Diagonal dominance of a five-channel neuromodulatory gain structure for trust dynamics: a double-blind, placebo-controlled, six-session within-subject pharmacological perturbation study.

### 2. Hypotheses

**H1 (primary, exact-form claim).** Within-subject, each channel-selective pharmacological probe changes its *own* channel readout more than it changes the other four channel readouts. Formally, for probe *p* targeting channel *j*=*p*: the diagonal-dominance statistic
> **D_p = Δ_pp − mean_{j≠p} Δ_pj** (standardized within-subject drug−placebo contrasts)
is positive for each of the five probes, and the pooled index **D̄ = mean_p D_p > 0**.

**H2 (secondary).** The DOCAS instrument battery (HRV/sleep/activity wearables + TRIBE-style text→fMRI encoding features) recovers the probe-induced channel perturbations with per-channel classification accuracy above chance, and its per-channel sensitivity ordering matches the behavioral/physiological gold standard (i.e., the wearables/text pipeline is *calibrated against* perturbation ground truth rather than asserted).

**H3 (registered negative control / honesty constraint).** The oxytocin probe is predicted to yield a small or null diagonal entry (d≈0.08–0.20; Nave et al. 2015; Declerck et al. 2020). A large oxytocin-probe effect on the "validation" channel readout that exceeds the drug's established behavioral effects would falsify the current channel operationalization (not the drug literature).

### 3. Design
Double-blind, placebo-controlled, within-subject crossover with **six sessions** per participant, separated by ≥7 days, session order counterbalanced with a 6×6 Williams Latin square:

| Session | Probe | Target channel | Direction | Target-engagement check (mandatory) |
|---|---|---|---|---|
| S0 | Placebo (matched) | — | — | All baseline assays |
| S1 | L-DOPA 150 mg + benserazide 37.5 mg | DA / expectation | ↑ | Prolactin suppression; [optional substudy: raclopride displacement] |
| S2 | Haloperidol 3 mg oral | DA / expectation | ↓ | Prolactin elevation (Frank & O'Reilly 2006 showed 2 mg ↑ prolactin; ≥3 mg recommended for functional effects, cf. Petrovic/Zack critiques) |
| S3 | Atomoxetine 40 mg | NA / activation | ↑ | Baseline pupil diameter ↑ + phasic feedback-evoked pupil ↑ (O'Callaghan et al. 2025) |
| S4 | Acute tryptophan depletion (100 g mix, 0 g TRP) | 5-HT / stabilization | ↓ | Plasma total/free TRP at 0 and +5.5 h (expect −77% to −94%) |
| S5 | Hydrocortisone 20 mg oral | Cortisol / recognition | ↑ | Salivary cortisol at −30, +60, +90 min (stress-equivalent levels per Buchanan et al. 2001) |
| S6* | Intranasal oxytocin 24 IU | Oxytocin / validation | ↑ (contested) | *None available* (no validated peripheral proxy of CNS engagement); registered as the exploratory/falsification arm |

\* If a strict six-session design is required for the Latin square, S6 pairs with S0-placebo and the design becomes 7 sessions (placebo + 6 probes) with N kept a multiple of 6. Recommended: **7 sessions, placebo + 6 probes**, because the DA channel needs its directional pair (S1, S2) to control for presynaptic/postsynaptic non-monotonicity.

**Why this is minimal-decisive:** Fewer than five probes cannot estimate a 5×5 gain matrix at all (unidentified). Fewer than the DA directional pair cannot disambiguate the sign of the DA diagonal. Placebo provides the within-subject baseline for all Δ contrasts. This is the smallest design in which the primary endpoint is identified; every removed session removes a row of M.

### 4. Participants
Healthy adults 18–40, 50% female target, screened per standard psychopharmacology criteria (no psychiatric/neurological history, no current medication, no steroid allergies; urine drug screen; ECG for atomoxetine/haloperidol QT screening; pregnancy testing). Exclusions: BMI <18 or >30 (L-DOPA pharmacokinetics), contraindication to any probe.

**Enrolled N = 60; target completers N = 48** (assumes 20% attrition across 7 sessions). N=48 preserves the Williams-square balance (multiple of 6) and meets the power requirement below.

### 5. Task battery (per session; identical across sessions, counterbalanced stimulus sets; total ≈ 90 min + engagement assays)

A single unified probabilistic-learning-and-social-evaluation battery engineered so that **every channel has expectation-violation events**:

1. **Volatility RL core (all-channel backbone; ~35 min).** Probabilistic reversal learning with embedded changepoints (volatile contingencies) and monetary gain/loss pairs. Yields per-channel model parameters: reward/punishment learning rates and striatal RPE responsivity (DA), volatility-coupled learning-rate adjustments with concurrent pupillometry (NA), and — via interleaved experienced-delay blocks (Schweighofer-style) — the discount factor γ (5-HT).
2. **Expectation-violation event blocks.** (i) Signed/unsigned RPE events at feedback (DA, NA pupil); (ii) unexpected contingency reversals without warning (NA, 5-HT); (iii) **anticipatory threat-mismatch block**: cued threat-of-shock/deviant-stimulus sequences with EEG MMN-family and anticipatory ERPs (cortisol channel readout; Simoens 2007; acute-stress ERP dissociation anticipatory-vs-consummatory, Neurobiol Stress 2021); (iv) **social validation/betrayal block**: iterated trust-game rounds against putative human partners with pre-programmed cooperation, betrayal, and apology/repair events, plus explicit experimenter-administered acceptance/rejection feedback epochs (validation channel readout).
3. **Physiology continuously recorded:** pupillometry (baseline + task-evoked), ECG/HRV, EDA, 64-channel EEG (RewP, P3, MMN, anticipatory SPN/N2), continuous wrist actigraphy + HRV wearable worn across the whole study period (between-session window), and standardized post-session narrative text samples (written debrief of the session's social events) for the TRIBE-style encoding pipeline.

### 6. Channel readout definitions (pre-registered composites; each preregistered with its validation citation)

- **R_DA (expectation):** reward learning rate + RL-model RPE responsivity on gain trials + feedback-related pupil/RewP. Anchors: Pessiglione 2006; Halahakoon 2024.
- **R_NA (activation):** baseline pupil diameter, phasic feedback-evoked pupil dilation, volatility-coupled learning-rate adaptation, P3b buildup rate. Anchors: O'Callaghan 2025; Loughnane 2019.
- **R_5HT (stabilization):** experienced-delay discount factor γ (experiential, not questionnaire — questionnaire discounting is insensitive to ATD per Crean 2002/Dougherty 2010), waiting-impulsivity premature responses, punishment-prediction asymmetry. Anchors: Schweighofer 2008; Worbe 2014; Cools 2008.
- **R_CORT (recognition):** anticipatory threat-mismatch responses (MMN-amplitude modulation, anticipatory cue-N2/SPN sensitivity to threat magnitude) + salivary cortisol AUC. Anchors: Simoens 2007; Neurobiol Stress 2021.
- **R_OXT (validation):** trust-game investment under betrayal/repair dynamics + emotion-recognition accuracy (the most defensible residual IN-OT effect; Leppanen 2017). Registered expectation: small/null.

Each readout is z-scored within subject across sessions before entry into M, making Δ_pj comparable across channels.

### 7. Primary endpoint and estimand

For participant *i*, probe *p*, channel *j*: **Δ_pj(i) = z(R_j | session p) − z(R_j | session placebo)**. The gain-matrix row for probe *p* is the vector (Δ_p1 … Δ_p5). **Primary endpoint: the five per-probe diagonal-dominance statistics D_p(i) = Δ_pp(i) − mean_{j≠p} Δ_pj(i), and the pooled D̄(i).**

**Success criterion (claim supported):** D̄ > 0 (one-sided, α=0.05) **and** at least 4 of 5 per-probe D_p > 0 at Bonferroni α = 0.05/5 = 0.01, with the oxytocin row handled under H3 (i.e., required: DA, NA, 5-HT, CORT + at least one of {DA direction pair consistent}).

**Falsification criteria (claim rejected):** (a) D̄ ≤ 0 or its 95% CI includes 0; (b) a pre-registered equivalence test (TOST, SESOI dz = 0.3) establishes D̄ is smaller than the smallest effect the framework considers substantively meaningful; (c) the maximum of the five channel responses occurs off-diagonal for ≥2 of the 4 pharmacologically valid probes; (d) any target-engagement check fails *and* the corresponding channel readout nonetheless moves (indicating non-specific/readout-driven effects).

### 8. Power analysis (shown; computed with statsmodels TTestPower, paired t-tests)

Within-subject rmANOVA effect size f maps to the paired-contrast dz via dz = f·√(2/(1−r)), r = within-subject correlation of repeated readouts.

| Scenario | f | r | dz | Test | α | N for 80% power | N for 90% power |
|---|---|---|---|---|---|---|---|
| Optimistic | 0.30 | 0.5 | 0.60 | per-probe D_p | 0.01 (Bonferroni /5) | 36 | 45 |
| Optimistic | 0.40 | 0.5 | 0.80 | per-probe D_p | 0.01 | 22 | 27 |
| Moderate | 0.30 | 0.3 | 0.51 | per-probe D_p | 0.01 | 50 | 63 |
| Pessimistic (Schweighofer-anchored: f≈0.24) | 0.24 | 0.5 | 0.48 | per-probe D_p | 0.01 | 53 | 66 |
| Pooled global test | 0.30 | 0.5 | 0.60 | D̄ | 0.05 | 24 | 31 |
| Pooled global test | — | — | 0.50 | D̄ | 0.05 | 34 | 44 |
| Pooled global test | — | — | 0.40 | D̄ | 0.05 | 51 | 68 |

**Design decision:** N=48 completers yields power = 0.92 for the per-probe test at dz=0.6 (optimistic), 0.86 at dz=0.55, 0.78 at dz=0.5 (moderate), and 0.92 for the pooled test at dz=0.5. The pessimistic per-probe scenario (dz=0.4) would require N≈76; we accept 78–80% power at dz=0.5 for per-probe tests with the pooled test as the primary decision criterion and per-probe tests as the pattern check. Enroll N=60 to complete 48 (20% multi-session attrition). If interim target-engagement checks show attenuated within-subject correlations (r<0.4), the pre-registered adaptation is to drop to the pooled primary test (powered at N=48 down to dz≈0.48 at 90%).

### 9. Analysis plan (pre-registered)
1. **Manipulation checks (gate to inference):** per-probe target engagement (prolactin, pupil, plasma TRP, salivary cortisol). Sessions failing engagement are excluded from that row of M and the exclusion is reported (per-protocol + ITT both reported).
2. **Primary:** paired t-tests on D̄ (α=0.05, one-sided as registered) and on each D_p (α=0.01); TOST equivalence at SESOI dz=0.3 if null. **Equivalence-arm power disclosure (registered):** the TOST equivalence arm at SESOI dz = 0.3 has power ≈ 0.31 at N = 48 — underpowered for concluding equivalence. The registered options are widening the SESOI to dz ≈ 0.45 (power ≈ 0.85) or raising N to ≈ 96 (80% power); the choice is registered here and is resolved at the interim target-engagement look, logged per §9 item 6.
3. **Secondary:** full M estimated in a linear mixed model: readout ~ probe × channel + (1|subject) + session-order; test the probe×channel interaction and report the full standardized matrix with CIs. Bayesian counterpart (hierarchical) reported for robustness.
4. **Convergent validation (H2):** wearable/text-pipeline features entered as predictors of probe condition (per-channel multinomial decoding, leave-one-session-out CV); report per-channel balanced accuracy vs the 20% chance level with permutation tests. Pre-registered success: DA, NA, CORT channels decode above chance (these have unambiguous physiological perturbations); no success claim is registered for the oxytocin channel.
5. **Multiplicity:** Bonferroni for the 5 per-probe tests; FDR (BH) for all secondary decoding analyses.
6. **Deviations:** any deviation from the registered plan is logged with timestamp and rationale in the OSF project.

### 10. Safety/ethics
Standard psychopharmacology safeguards: physician oversight; domperidone pre-treatment permitted for pramipexole-class nausea (not needed for L-DOPA at 150 mg with benserazide); cardiovascular monitoring on atomoxetine and hydrocortisone sessions; ATD monitored for mood (mood effects transient; exclusion of depression history); stopping rules pre-registered; DSMB for the multi-drug protocol. Total radiation exposure = 0 unless the PET substudy is joined (separate consent).

---

## (c) INDEPENDENT-RATER PROTOCOL — CLICS concept sets & offer-stimulus categories

**Purpose:** Remove author-selection bias from (i) the CLICS-based concept sets used to operationalize semantic content and (ii) the offer-stimulus category assignments used in the trust paradigms.

**Standards adopted (with sources):**
- **Krippendorff's α** as the primary reliability coefficient (any number of raters, missing data, any measurement level). Thresholds: **α ≥ 0.800 = reliable**; **0.667 ≤ α < 0.800 = tentative conclusions only**; **α < 0.667 = discard/revise** (Krippendorff 2004, *Content Analysis*, 2nd ed., p. 241; Krippendorff 2018, 4th ed.). Report α **with bootstrap 95% CI**, not a bare point estimate.
- **Cohen's κ** (exactly two raters) / **Fleiss' κ** (≥3 raters, nominal) as secondary coefficients; interpret with Landis & Koch (1977) bands (0.61–0.80 substantial; ≥0.81 almost perfect) — noting these are conventions; Neuendorf (2002): κ ≥ 0.80 acceptable to all, ≥ 0.60 acceptable in most situations. Fleiss' κ runs systematically lower than Cohen's; do not mix benchmarks.
- **Prevalence-paradox guard:** if any category has <20% or >80% prevalence, additionally report **Gwet's AC1/AC2** and raw percent agreement (kappa is known to collapse paradoxically under skew).
- **Rater count and workflow:** minimum **3 independent raters** per artifact (5 preferred for the concept sets); raters blind to the framework's hypotheses and to author assignments; no rater may be an author. Iterative rounds: independent rating → α computed → disagreements discussed against the written codebook → codebook revised → next round, until α ≥ 0.800 is **sustained over two consecutive rounds** (workflow per Wohlrab et al. human-validation guideline; arXiv 2508.15503). Consensus resolution is permitted only after the final reliability round; all pre-consensus alphas are reported.

**What is pre-registered (OSF, before rating begins):**
1. The full **codebook**: category definitions, inclusion/exclusion criteria per CLICS concept set, decision rules, worked examples, edge-case policy.
2. The **item universe** (all candidate concepts/stimuli before selection) and the sampling plan (rate 100% of items in the used sets; if a larger pool, a pre-specified random sample of ≥30% or n≥150, whichever larger, to bound the CI width of α).
3. Rater qualifications (e.g., 2 linguists + 1 naive native speaker per language family for CLICS; 3 trained coders for offer stimuli), independence attestation, compensation.
4. Reliability thresholds (α ≥ 0.800 gate; 0.667 floor), the exact coefficients to be computed (α primary with interval-level distance for ordinal ratings, nominal for categorical; Cohen's/Fleiss' κ secondary; Gwet's AC under prevalence skew), and the CI method.
5. The **adjudication rule** for items below threshold (drop vs revise-category vs expand codebook), decided *before* seeing data.
6. Analysis environment (R `irr::kripp.alpha` or Python `krippendorff`), seed, and the reporting template (α per set, per rater-pair matrix, prevalence table, CI).

**Acceptance gate:** the concept sets/stimuli may enter the perturbation study only if every used set clears α ≥ 0.800 (or 0.667–0.800 with an explicit "tentative" label carried into all downstream inference). Any set below 0.667 is rebuilt and re-rated; rebuilding is reported.

---

## (d) HONEST FEASIBILITY & COST NOTES

1. **Timeline/burden.** 7 sessions × ~2.5 h + screening + washouts ⇒ ~8–12 weeks per participant; multi-drug crossovers of this size are done (e.g., 4-drug crossovers exist; Loughnane 2019) but attrition of 15–25% is realistic, hence enroll 60 → 48.
2. **Cost, behavioral/physiology protocol (ballpark, US/EU academic rates):** participant payment 60 × 7 × ~$120 ≈ $50k; drugs + pharmacy blinding ≈ $10–20k; EEG/pupillometry/assay consumables + assays (TRP, cortisol, prolactin) ≈ $20–40k; personnel dominant. **Total ≈ $150–300k.** Entirely feasible at a standard cognitive-neuroscience lab.
3. **PET substudy (optional, DA validation only).** Research [11C]raclopride scans run roughly **$2,000–$6,000 per scan** (on-site cyclotron required; C-11 half-life 20 min); a within-subject amphetamine-displacement substudy on N=24 × 2 scans ≈ **$100–300k**, and radiation limits cap ≈2–3 C-11 scans/subject/year. Justified only as convergent validation of the DA row; **not** justified as the primary instrument: task-evoked DA displacement (~2.7% ΔBP) is at/below the detection threshold demonstrated by the dual-bolus feasibility study (no detectable task effect at ICC 0.959), and NA/oxytocin have no endogenous-release PET paradigm at all.
4. **What this design cannot fix.** (i) The oxytocin channel has no validated pharmacological perturbation in humans; the gate can only test whether the *behavioral* validation readout behaves as a channel, with IN-OT as a registered-likely-null probe. (ii) Diagonal dominance at the *group mean* level does not prove the exact-form holds in individual dynamics — hierarchical estimates (per-subject M with shrinkage) are reported, and between-subject heterogeneity is a secondary outcome. (iii) Pharmacological selectivity is relative, not absolute (e.g., atomoxetine also raises cortical DA; L-DOPA is precursor-not-receptor-specific): the design controls this via the off-diagonal structure itself (cross-channel leakage is *estimated*, not assumed away), but interpretation of any single cell of M must acknowledge co-modulation. (iv) Failed-replication history (Pessiglione 2006 → Michely 2023 null at N=31) is why target-engagement gates and N=48 (not N≈30) are non-negotiable.
5. **Deliverable sequence recommended:** (1) OSF registration of DOCAS-GATE-1 + rater protocol (zero cost, immediate); (2) rater study (weeks, <$10k); (3) pilot N=12 (engagement + within-subject reliability r estimation to verify the power assumptions); (4) full N=60 study; (5) PET substudy only if DA-row diagonal dominance is behaviorally established.

---

## APPENDIX — Key citation list (primary sources)

1. Pessiglione M, et al. Dopamine-dependent prediction errors underpin reward-seeking behaviour in humans. *Science* 2006;314:904–908. DOI: 10.1126/science.1130285.
2. Michely J, et al. Dopamine regulates decision thresholds in human reinforcement learning in males. *Nat Commun* 2023;14:7054. DOI: 10.1038/s41467-023-41130-y.
3. Halahakoon DC, et al. Pramipexole enhances reward learning by preserving value estimates. *Biol Psychiatry* 2024;95(9):839–849. PMID 37330165; DOI: 10.1016/j.biopsych.2023.06.020.
4. Westbrook A, et al. Dopamine promotes cognitive effort by biasing the benefits versus costs of cognitive work. *Science* 2020;367:1362–1366. (Effort/FDOPA anchoring; see also Neuropsychopharmacology 2020;45:1331–1341.)
5. O'Callaghan C, et al. Pharmacological and pupillary evidence for the noradrenergic contribution to reinforcement learning in Parkinson's disease. *Commun Biol* 2025;8:189. DOI: 10.1038/s42003-025-08627-2.
6. Loughnane GM, et al. Catecholamine modulation of evidence accumulation during perceptual decision formation: a randomized trial. *J Cogn Neurosci* 2019;31:1044–1053. DOI: 10.1162/jocn_a_01393.
7. De Martino B, Strange BA, Dolan RJ. Noradrenergic neuromodulation of human attention for emotional and neutral stimuli. *Psychopharmacology* 2008;197:127–136. DOI: 10.1007/s00213-007-1015-5.
8. Schweighofer N, et al. Low-serotonin levels increase delayed reward discounting in humans. *J Neurosci* 2008;28:4528–4532. DOI: 10.1523/JNEUROSCI.4982-07.2008.
9. Worbe Y, et al. Serotonin depletion induces 'waiting impulsivity' on the human four-choice serial reaction time task. *Neuropsychopharmacology* 2014;39:1519–1526. DOI: 10.1038/npp.2014.2.
10. Dougherty DM, et al. Effects of acute tryptophan depletion on three different types of behavioral impulsivity. *Int J Neuropsychopharmacol* (2010). PMC3195237.
11. Cools R, Robinson OJ, Sahakian B. Acute tryptophan depletion in healthy volunteers enhances punishment prediction but does not affect reward prediction. *Neuropsychopharmacology* 2008;33:2291–2299. DOI: 10.1038/sj.npp.1301542.
12. Skandali N, et al. Dissociable effects of acute SSRI (escitalopram) on executive, learning and emotional functions in healthy humans. *Neuropsychopharmacology* 2018;43:2645–2651. DOI: 10.1038/s41386-018-0229-z.
13. Langley C, et al. Chronic escitalopram in healthy volunteers has specific effects on reinforcement sensitivity. *Neuropsychopharmacology* 2023;48:664–670. DOI: 10.1038/s41386-022-01498-2.
14. Lovallo WR, et al. Acute effects of hydrocortisone on the human brain: an fMRI study. *NeuroImage* 2010;49:864–870. DOI: 10.1016/j.neuroimage.2009.08.002.
15. Buchanan TW, Lovallo WR. Enhanced memory for emotional material following stress-level cortisol treatment in humans. *Psychoneuroendocrinology* 2001;26:307–317 (dose calibration 20 mg ≈ lab stress levels).
16. Goodman WK, Janson J, Wolf JM. Meta-analytical assessment of the effects of protocol variations on cortisol responses to the TSST. *Psychoneuroendocrinology* 2017;81:26–35. (d≈0.9–1.0); VR-TSST meta: *Psychoneuroendocrinology* 2019. DOI: 10.1016/j.psyneuen.2019.104412.
17. Simoens VL, Tervaniemi M. Psychosocial stress attenuates general sound processing and duration change detection. *Psychophysiology* 2007;44:106–111. PMID 17241138.
18. Nave G, Camerer C, McCullough M. Does oxytocin increase trust in humans? A critical review of research. *Perspect Psychol Sci* 2015;10:772–789. DOI: 10.1177/1745691615600138.
19. Declerck CH, Boone C, Pauwels L, Vogt B, Fehr E. A registered replication study on oxytocin and trust. *Nat Hum Behav* 2020;4:646–655. DOI: 10.1038/s41562-020-0878-x.
20. Leng G, Ludwig M. Intranasal oxytocin: myths and delusions. *Biol Psychiatry* 2016;79:243–250. DOI: 10.1016/j.biopsych.2015.05.003.
21. Leppanen J, et al. Meta-analysis of the effects of intranasal oxytocin on interpretation and expression of emotions. *Neurosci Biobehav Rev* 2017;78:125–144 (33 studies; strongest effect for fear recognition).
22. Dual-bolus [11C]raclopride feasibility: Measurement of striatal dopamine release induced by neuropsychological stimulation. *Front Psychiatry* 2022;13:811136. DOI: 10.3389/fpsyt.2022.811136.
23. Meta-analysis of [11C]raclopride PET challenge studies (amphetamine ≈10.9% vs cognitive ≈2.7% ΔBP_ND). *Mol Psychiatry* 2026. DOI: 10.1038/s41380-026-03826-7.
24. Boileau I, et al. Conditioned dopamine release in humans: a [11C]raclopride PET study with amphetamine. *J Neurosci* 2007;27:3998–4003.
25. Selvaraj S, et al. Measuring endogenous changes in serotonergic neurotransmission in humans: a [11C]CUMI-101 PET challenge study. *Mol Psychiatry* 2012;17:1254–1260.
26. Sander CY, Hooker JM, et al. Advances in simultaneous PET/MR for imaging neuroreceptor function. *EJNMMI Phys* 2020. PMC7238372.
27. Krippendorff K. *Content Analysis: An Introduction to Its Methodology.* 2nd ed. 2004 (α thresholds, p. 241); 4th ed. 2018.
28. Landis JR, Koch GG. The measurement of observer agreement for categorical data. *Biometrics* 1977;33:159–174.
29. Neuendorf KA. *The Content Analysis Guidebook.* 2002.
30. Balieiro S, et al. Guidelines for empirical studies involving LLMs (human-validation workflow; α>0.8 sustained rounds). arXiv:2508.15503.
