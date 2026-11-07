# Sim C-Series Run Report: Choice Architecture & Nudge Dynamics

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **COMPOUND PASS (3/3)**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **C1: Default Nudge Adherence** | +70% weight to default cooperative action | Adherence $\ge 75.0\%$ | **94.8\%** (vs 70.7\% neutral) | **PASS** |
| **C2: Loss Framing Asymmetry** | Loss framing ($\lambda^-=0.02$) vs Gain ($\lambda^+=0.005$) | Ratio $\ge 3.0\times$ | **51.42\times** | **PASS** |
| **C3: Cognitive Friction Damping** | 3 units friction penalty (-20%/unit) | Opt-out ratio $\le 0.50$ | **0.40** (60.0\% suppression) | **PASS** |

---

## 2. Engineering Calibrations for Production Simulator

1. **Choice Architecture Toggle:** Enabling `mech-choice` modulates agent prior expectation by default weight $W = +0.70$, elevating default option adherence to 94.8%.
2. **Framing Multiplier:** Loss-framed agreements engage the 4:1 asymmetric penalty, yielding 51.42x higher behavioral retention.
