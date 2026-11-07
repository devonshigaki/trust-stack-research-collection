# Sim CRIT-Series Run Report: Neural Criticality & Avalanche Dynamics

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **COMPOUND FAIL (2/3 PASS)**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **CRIT-1: Dynamic Range** | Peak dynamic range in $[0.95, 1.05]$ | Peak in window $\wedge$ excess $\ge 15.0\text{ dB}$ | **$\sigma^* = 1.00$** (Excess: 18.1 dB) | **PASS** |
| **CRIT-2: Avalanche Power Law** | Scaling exponent $\alpha$ at $\sigma = 1.0$ | $\alpha \in [1.40, 1.60], R^2 \ge 0.95$ | **$\alpha = 0.682, R^2 = 0.8666$** | **FAIL** |
| **CRIT-3: Info Transmission** | Off-criticality information collapse | Ratio $\le 0.65$ | **Ratio = 0.50** | **PASS** |

---

## 2. Engineering Calibrations for Production Simulator

1. **Criticality Toggle (`mech-criticality`):** When enabled in Layer 4, the network operates at $\sigma = 1.00$, maximizing sensory dynamic range to 32.4 dB. When disabled, the network operates in a subcritical dampened state ($\sigma = 0.70$), suppressing false-alarm cascade propagation at the cost of a 40% reduction in mutual information.
