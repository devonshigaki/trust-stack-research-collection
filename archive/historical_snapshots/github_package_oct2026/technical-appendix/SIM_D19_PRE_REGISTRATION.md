# PRE-REGISTRATION — Sim D19: Perky Reality-Monitoring Perception Filter & Realistic Cognitive Noise in Credit Offer Uptake

**Date:** 2026-10-29 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §5.8 / GTT §3 / TFP §3.7 / FreshCredit Whitepaper §3.4 / Brain-IT In-Silico Pipeline  
**Random Seed:** 42 everywhere  
**Theoretical Anchors:**  
- Dijkstra, N., & Fleming, S. M. (2023). "Subjective signal strength distinguishes reality from imagination." *Nature Communications*, 14, 1627. [DOI: 10.1038/s41467-023-37322-1](https://doi.org/10.1038/s41467-023-37322-1)  
- Perky, C. W. (1910). "An experimental study of imagination." *The American Journal of Psychology*, 21(3), 422–452.  
- General Theory of Trust (GTT) Reconciled Master Stability Law: $\Delta S_t = \lambda(V_t - E_t) - \delta(S_t - S_{\text{base}})$.  
- DOCAS 5-channel manifold $\mathring{\Delta}^4$ ($D$: Dopamine, $O$: Oxytocin, $C$: Cortisol, $A$: Adrenaline, $S$: Serotonin).  
- Bounded Rationality & Scarcity Framework (Mullainathan & Shafir, 2013).

---

## 1. Domain Hypotheses & Theoretical Motivation

Standard economic consumer-choice and algorithmic agent simulations introduce cognitive noise using **symmetric zero-mean Gaussian perturbations**:
$$U_{\text{eff}} = U_{\text{true}} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$$
This legacy formulation is biologically and psychologically invalid:
1. Symmetric white noise preserves unbiased expectations ($\mathbb{E}[U_{\text{eff}}] = U_{\text{true}}$).
2. It fails to account for the neurobiology of sensory-imagery interaction, attention gating, and the psychophysics of "reality monitoring."

### The Perky Effect & The Modern Dijkstra-Fleming Reality Threshold
In 1910, Mary Cheves West Perky demonstrated that when individuals engage in mental imagery while being exposed to faint, real visual stimuli below their conscious threshold, they mistake real physical stimuli for internally generated imagery (**Perky blindness**). 

In 2023, Dijkstra and Fleming (*Nature Communications*) resolved the neural mechanism using psychophysics and neuroimaging in the modernized **"Perky line test"** (detecting faint oriented line gratings during mental imagery of lines):
1. **Shared Substrate:** Visual perception (external sensory evidence $X$) and mental imagery (internally generated expectation $V$) share early visual cortical substrates (V1–V4).
2. **Scalar Reality Signal:** The brain combines sensory evidence and mental imagery into a single decision variable:
   $$m = \alpha X + V + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma_{\text{sensory}}^2)$$
   where $\alpha$ is sensory salience (contrast/gain), $X$ is external contract evidence, $V$ is mental imagery strength, and $\epsilon$ is sensory observation noise.
3. **The Reality Threshold Gate ($T_{\text{reality}}$):** The brain applies a criterion threshold:
   - If $m > T_{\text{reality}}$: The feature is tagged as **externally real** and integrated into conscious evaluation.
   - If $m \le T_{\text{reality}}$: The feature is classified as **imagined or absent**, and faint external sensory evidence is **"explained away" (suppressed)**.

### Application to Consumer Credit Offers & Visual Cloaking
In consumer finance, individuals under severe liquidity constraints (low cognitive bandwidth $\kappa_i$) suffer elevated Cortisol ($C$) and high exploratory Dopaminergic drive ($D$). This state generates:
1. **Hyper-vivid optimistic relief imagery ($V_{\text{promo}} \gg 0$):** The desperate expectation of receiving liquid cash funds.
2. **Aversive fine-print silencing ($V_{\text{disc}} \approx 0$):** Cognitive suppression of punitive clauses, high default APRs, and legal disclaimers.

When paired with predatory visual cloaking (Sim D16), where promotional headlines have high visual edge energy ($\alpha_{\text{promo}} \approx 1.0$) and fine-print disclaimers have low visual edge energy ($\alpha_{\text{disc}} = 1/\chi \ll 1.0$):
- **Promotional Headline:** $m_{\text{promo}} = 1.0 \cdot X_{\text{promo}} + V_{\text{promo}} + \epsilon \gg T_{\text{reality}}$. It breaches the threshold decisively, confirmed as vivid reality.
- **Cloaked Fine-Print Disclaimer:** $m_{\text{disc}} = \alpha_{\text{disc}} \cdot X_{\text{disc}} + V_{\text{disc}} + \epsilon \le T_{\text{reality}}$. Because $\alpha_{\text{disc}}$ is suppressed by typographic layout and $V_{\text{disc}} \approx 0$, $m_{\text{disc}}$ fails to cross $T_{\text{reality}}$.
- **Perky Blindness Consequence:** The consumer literally explains away the fine print, experiencing an illusory "safe loan" while the predatory penalty collapses to zero in their mental ledger ($U_{\text{penalty}} \to 0$).

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

All four quantitative criteria are strictly frozen prior to simulation execution.

### Hypothesis D19.1: Fine-Print Perky Blindness (Suppression Gate)
* **Criterion C1:** Under the realistic Perky reality-monitoring filter across the 27 visual credit agreements, the fine-print disclaimer in predatory contracts must fall below the reality threshold ($m_{\text{disc}} \le T_{\text{reality}}$) in at least $60.0\%$ of simulated agent evaluations:
  $$\text{Suppression Rate}_{\text{PRED}} = \mathbb{E}[\mathbb{I}(m_{\text{disc}} \le T_{\text{reality}})] \ge 0.600$$

### Hypothesis D19.2: Asymmetric Realistic Noise vs. Symmetric Gaussian Noise Surge
* **Criterion C2:** The realistic Perky reality-monitoring filter (Arm 2) must produce a dramatic, statistically significant excess in predatory contract uptake over the standard symmetric Gaussian noise model (Arm 1) of at least 25 percentage points:
  $$\Delta\text{Uptake} = U_{\text{Perky}} - U_{\text{Gaussian}} \ge 0.250 \quad (+25.0\%)$$

### Hypothesis D19.3: Exploitation Vulnerability Gradient (Decile Odds Ratio)
* **Criterion C3:** The bottom decile of agent cognitive bandwidth (D1, most stressed / lowest $\kappa_i$) must experience an odds ratio of predatory contract uptake $\ge 15.0\times$ compared to the top decile (D10, high bandwidth / secure):
  $$\text{OR}_{\text{D1}/\text{D10}} = \frac{p_{\text{D1}} / (1 - p_{\text{D1}})}{p_{\text{D10}} / (1 - p_{\text{D10}})} \ge 15.00\times$$

### Hypothesis D19.4: Permutation Significance under Shuffled Visual Salience
* **Criterion C4:** In a two-sided permutation test with $B = 2,000$ label iterations, shuffling the visual cloaking ratios across stimulus categories must abolish the excess exploitation shift, yielding:
  $$p_{\text{perm}} \le 0.001$$

**Compound Verdict Rule:**  
- **PASS:** All four criteria (C1, C2, C3, C4) satisfied simultaneously.  
- **FAIL:** Any criterion fails as frozen. Results will be reported transparently without post-hoc threshold adjustment.

---

## 3. Mathematical Model & Experimental Specification

### Population Parameters:
- Sample size: $N = 1,000$ heterogeneous agents.
- Cognitive bandwidth: $\kappa_i \sim \text{Beta}(2, 5)$ (mean $\mu_\kappa \approx 0.286$).
- Reservation utility: $U_{\text{res}, i} \sim \mathcal{N}(0.10, 0.04)$.
- Random seed: 42 everywhere.

### Dijkstra Reality-Monitoring Constants:
- Reality Threshold: $T_{\text{reality}} = 2.5$ (empirical population mean from Dijkstra & Fleming, 2023).
- Sensory Observation Noise: $\sigma_{\text{sensory}} = 0.5$.
- Desperation Relief Imagery: $\mu_{V,\text{promo}} = 2.5 + 1.8 \cdot (1 - \kappa_i)$, $V_{\text{promo}} \sim \mathcal{N}^+(\mu_{V,\text{promo}}, 0.90)$.
- Threat Anticipation Imagery: $\mu_{V,\text{disc}} = 0.8 \cdot \kappa_i$, $V_{\text{disc}} \sim \mathcal{N}^+(\mu_{V,\text{disc}}, 0.60)$.

### 4 Experimental Arms:
1. **Arm 0 (Veridical Rational Benchmark):** Full information, veridical utility evaluation:
   $$U_0 = -\frac{\text{APR}_{\text{true}}}{100} \cdot \left(\frac{\text{Amount}}{10000}\right) + U_{\text{cash}}$$
2. **Arm 1 (Standard Symmetric Gaussian Noise):**
   $$U_1 = U_0 + \epsilon_{\text{gauss}}, \quad \epsilon_{\text{gauss}} \sim \mathcal{N}\left(0, 0.15 \cdot (1.5 - \kappa_i)\right)$$
3. **Arm 2 (Perky / Dijkstra Reality-Monitoring Noise Filter):**
   $$m_{\text{promo}} = 1.0 \cdot 1.0 + V_{\text{promo}} + \epsilon_{\text{promo}}$$
   $$m_{\text{disc}} = \alpha_{\text{disc}} \cdot \text{PenaltySeverity} + V_{\text{disc}} + \epsilon_{\text{disc}}$$
   where $\alpha_{\text{disc}} = 1 / \chi_i$ from Brain-IT Branch A structural reconstructions.
   $$\text{PerceivedPenalty} = \begin{cases} \frac{\alpha_{\text{disc}} \cdot \text{TrueCost} + V_{\text{disc}} \cdot 0.05}{\alpha_{\text{disc}} + V_{\text{disc}} + 10^{-5}}, & \text{if } m_{\text{disc}} > T_{\text{reality}} \\ 0.0, & \text{if } m_{\text{disc}} \le T_{\text{reality}} \text{ (explained away)} \end{cases}$$
4. **Arm 3 (FreshCredit Salience Countermeasure):**
   Forced visual prominence ($\alpha_{\text{disc}} = 2.8 \gg T_{\text{reality}}$) guaranteeing that fine-print terms cross the reality threshold and restore informed decision-making.

---

## 4. Expected Deliverables & Artifacts
- Frozen Pre-registration: `technical-appendix/SIM_D19_PRE_REGISTRATION.md`
- Simulation Implementation: `experiments/brainit-fmri/insilico/sim_d19_perky_reality_filter.py`
- Statistical Results: `experiments/brainit-fmri/results/sim_d19_results.json`
- 4-Panel Publication Diagram: `figures/docas/pipeline/fig_sim_d19_perky_reality_filter.png`
- Accounting Audit Trail: Updated `SIMULATION_ACCOUNTING.md` and `VERSIONS.md`
