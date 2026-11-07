# Sim DMN-Series Run Report: Bounded Counterfactual Rollouts & Deception Shielding

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **COMPOUND FAIL (2/3 PASS)**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **DMN-1: Deception Resistance** | Uptake under Sim D16 cloaking ($K=1$ vs $K=5$) | $\text{Uptake}_{K=5} / \text{Uptake}_{K=1} \le 0.60$ | **0.2312** (76.9% suppression) | **PASS** |
| **DMN-2: Standing Advantage** | Steady-state trust standing advantage ($K=5$ vs $K=1$) | $S_{K=5} / S_{K=1} \ge 1.30$ | **1.17\times** | **FAIL** |
| **DMN-3: Cognitive Saturation** | Marginal loss reduction from $K=7$ to $K=10$ | $\Delta \text{Loss} < 0.05$ | **0.0031** | **PASS** |

---

## 2. Engineering Calibrations for Production Simulator

1. **DMN Toggle Calibration:** Enabling `mech-dmn` activates counterfactual simulation. Calibrating depth to $K = 5$ suppresses predatory visual exploitation by 76.9% while keeping cognitive deliberation cost within the linear return corridor ($K \le 7$).
