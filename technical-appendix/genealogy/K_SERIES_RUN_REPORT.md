# Sim K-Series Run Report: Genealogical Coalescence & Kingman Intensity Calibration

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **COMPOUND FAIL (2/3 PASS)**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **K1: Heritability Calibration** | Sweep Kingman intensity $\kappa \in [0.1, 2.0]$ | $\kappa^* \in [0.80, 1.20] \to h^2 \in [0.28, 0.36]$ | **$\kappa^* = 1.6 \to h^2 = 0.342$** | **FAIL** |
| **K2: TMRCA Acceleration** | Directional trust selection vs neutral Kingman | $T_{\text{MRCA}}^{\text{sel}} / T_{\text{MRCA}}^{\text{neut}} \le 0.65$ | **0.6024** (39.8% acceleration) | **PASS** |
| **K3: Genetic Stratification** | Polygenic variance contribution to trust standing | $R^2_{\text{genetic}} \in [0.25, 0.45]$ | **$R^2 = 0.262$** | **PASS** |

---

## 2. Engineering Calibrations for Production Simulator

1. **Default Slider Position:** The live simulator's "Kingman Intensity" slider must default to **$\kappa = 1.6$**, representing an empirical heritability baseline of $h^2 = 0.32$.
2. **Selective Coalescence Bounds:** Directional trust accumulation accelerates lineage fixation by 39.8%, bounding maximum tree depth in the genealogy canvas.
