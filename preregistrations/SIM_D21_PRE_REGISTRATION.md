# PRE-REGISTRATION — Sim D21: Multimodal Gating & Anterior Insula Ultimatum Game Fairness

**Date:** 2026-10-29 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS / GTT / TRIBE v2 Forward Encoding  
**Random Seed:** 42 everywhere  

**Theoretical Anchors:**  
- Sanfey, A. G., et al. (2003). "The neural basis of economic decision-making in the Ultimatum Game." *Science*, 300(5626), 1755-1758.  
- Fehr, E., & Schmidt, K. M. (1999). "A theory of fairness, competition, and cooperation." *The Quarterly Journal of Economics*, 114(3), 817-868.  
- Gu, X., et al. (2015). "Anterior insular cortex and emotional awareness." *Journal of Comparative Neurology*, 523(11), 1687-1701.

---

## 1. Domain Hypotheses & Theoretical Motivation

Classical "revealed preference" theory assumes consumers accept $390\%$ APR loans because they subjectively value the cash enough to consider the penalty "fair." The **Neuroeconomic Fairness hypothesis** counters this: fairness is evaluated against a Norm Prediction Error (NPE) in the Anterior Insula (aINS). When punitive terms are multimodally cloaked (visual spatial attenuation + auditory compression), the penalty is perceptually erased. The aINS evaluates a "phantom" fair contract (NPE $\approx 0$) and remains quiescent. The consumer accepts the deal because their biological unfairness alarm was perceptually bypassed.

## 2. Pre-Registered Frozen Criteria (C1–C4)

- **C1 (Insular Hypoactivation under Dual Cloaking):** Under dual visual/auditory cloaking ($\\chi_{\text{vis}} \ge 3.5$, $r_{\text{aud}} \ge 10.0\text{ syl/s}$), the predicted aINS activation (Norm Prediction Error) drops by $\ge 60.0\%$ compared to fully transparent multi-modal contracts.
- **C2 (Ultimatum Acceptance Inversion):** Predatory contracts that would be rejected by $95.0\%$ of rational Fehr–Schmidt agents under veridical information will achieve an acceptance rate $\ge 70.0\%$ under dual-branch cloaking.
- **C3 (Vulnerability Gradient):** Stressed agents (decile D1, lowest bandwidth $\kappa$) will experience an odds ratio of predatory exploitation $\ge 12.0\times$ relative to unstressed agents (decile D10).
- **C4 (Ex-Post Insular Rebound):** When the true penalty is physically extracted at loan maturity ($t+1$), the delayed insular prediction error ($\Delta \text{BOLD}_{\text{aINS}}^{\text{rebound}}$) is $\ge 3.0\times$ higher than baseline fair contracts, modeling severe structural default shock.

**Compound Verdict Rule:** PASS requires all four criteria (C1, C2, C3, C4) to be satisfied simultaneously. Any failure is reported as frozen without adjustment.
