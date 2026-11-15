# PRE-REGISTRATION — Sim D16: Perceptual Cloaking & Predatory Uptake under Dual-Branch Visual-Cognitive Gating

**Date:** 2026-10-09 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §5.8 / TFP §3.7 / FreshCredit Whitepaper §3.4  
**Random Seed:** 42 everywhere

---

## 1. Domain Hypothesis & Theoretical Motivation

Standard economic consumer-choice models assume agents possess unbounded visual-perceptual capacity and evaluate credit contracts over full mathematical parameter vectors $(\text{APR}, \text{principal}, \text{fees})$. Real human decision-makers, however, possess bounded visual attention and cognitive bandwidth.

In the Brain-IT in-silico framework:
- **Branch A (Low-Level Structural / VGG):** Encodes the physical spatial layout, typographic edge energy, background contrast, and layout boxes.
- **Branch B (High-Level Semantic / CLIP):** Encodes the true underlying contractual and semantic content.

**The Domain Hypothesis [HYPOTHESIS / SIMULATION]:**  
Visual design in consumer credit agreements drives systematic consumer exploitation via **perceptual cloaking**. When predatory lenders engineer agreements with high visual salience in promotional teaser headlines ($E_{\text{promo}}$) and low edge-energy in legally mandated disclaimers ($E_{\text{disc}}$), the visual cloaking ratio:
$$\chi = \frac{E_{\text{promo}}}{E_{\text{disc}} + \epsilon}$$
acts as an attention filter. Agents with low-to-moderate cognitive bandwidth will fail to perceive the predatory terms, inducing a statistically significant and economically substantial surge in predatory contract uptake that collapses under transparent (isomorphic-salience) layouts.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

All criteria are frozen before executing the simulation script.

* **Criterion C1 (Visual Salience Asymmetry Gate):**  
  The visual cloaking ratio extracted from Brain-IT Branch A structural edge-energy maps must satisfy:
  $$\chi_{\text{PREDATORY}} \ge 2.5 \cdot \chi_{\text{FAIR}}$$
* **Criterion C2 (Excess Exploitation Uptake Gap):**  
  In a population of $N = 1,000$ heterogeneous agents ($\kappa_i \sim \text{Beta}(2, 5)$ modeling stressed/low-bandwidth consumers), the average predatory uptake rate under the visually cloaked design ($U_{\text{cloaked}}$) must exceed the uptake rate under the transparent layout ($U_{\text{transparent}}$) by at least 30 percentage points:
  $$\Delta\text{Uptake} = U_{\text{cloaked}} - U_{\text{transparent}} \ge 0.30$$
* **Criterion C3 (Vulnerability Gradient / Decile Odds Ratio):**  
  The bottom decile of agent cognitive bandwidth (D1, most stressed) must suffer an odds ratio of predatory exploitation $\ge 3.0\times$ compared to the top decile (D10, least stressed):
  $$\text{OR}_{\text{D1}/\text{D10}} \ge 3.0$$
* **Criterion C4 (Permutation Significance):**  
  Shuffling visual layout energy maps across stimulus conditions must destroy the excess exploitation ($p < 0.0005$ under 2,000 permutation nulls).

**Compound Verdict Rule:**  
- **PASS:** All 4 criteria (C1–C4) met.  
- **FAIL:** Any criterion fails as frozen (no post-hoc parameter adjustments allowed).

---

## 3. Mathematical Model Specification

### Agent Population:
$N = 1,000$ agents. Cognitive bandwidth $\kappa_i \sim \text{Beta}(\alpha=2, \beta=5)$ (mean $\mu_\kappa \approx 0.286$, reflecting low-income / credit-stressed populations).  
Reservation utility $U_{\text{res}, i} \sim \mathcal{N}(0.10, 0.05)$.

### Perception & Attention Filter:
Given an offer with cloaking ratio $\chi$ and agent bandwidth $\kappa_i$, the probability of discovering and integrating the fine-print disclaimer is:
$$P_{\text{disc}, i} = \frac{1}{1 + \exp\left( -\gamma \left( \frac{\kappa_i}{\chi} - \tau \right) \right)}$$
where $\gamma = 8.0$ (attention sharpness) and $\tau = 0.20$ (perceptual threshold).

### Perceived vs. True Utility:
- If disclaimer is perceived ($r_i < P_{\text{disc}, i}$):
  $$U_i = -\frac{\text{APR}_{\text{true}}}{100} \cdot \left(\frac{\text{Amount}}{10000}\right) + \text{Utility}_{\text{cash}}$$
- If disclaimer is cloaked ($r_i \ge P_{\text{disc}, i}$):
  $$U_i = -\frac{\text{APR}_{\text{promo}}}{100} \cdot \left(\frac{\text{Amount}}{10000}\right) + \text{Utility}_{\text{cash}} + \text{UrgencyBonus}$$
An agent accepts the offer if $U_i > U_{\text{res}, i}$.
