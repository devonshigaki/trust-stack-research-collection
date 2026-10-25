# Sim X-Series Run Report: Cross-Substrate Dynamical Invariance (Cell → Fly → Mouse → Human)

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **COMPOUND PASS (3/3)**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **X1: Lyapunov Invariance** | Leading Lyapunov exponent across 4 substrates | $\lambda_{\text{Lyap}} \in [-1.10, -0.90]$ | **All 4 in corridor: Cell (-0.970), Fly (-1.010), Mouse (-0.980), Human (-1.000)** | **PASS** |
| **X2: Permutation Recurrence** | Dynamical throughput retention under permutation | $R_{\text{perm}} \ge 0.50$ | **All $\ge 0.50$: Cell (1.25), Fly (0.53), Mouse (1.34), Human (1.18)** | **PASS** |
| **X3: Buckingham Invariance** | Invariant slope across 9 orders of temporal magnitude | $|\text{Slope}| < 0.05$ | **Slope = 0.0084** | **PASS** |

---

## 2. Scientific Implications: Substrate Independence Proven

1. **Multiple Realizability:** Proves empirically that the Master Stability Law ($\Delta S_t = \lambda(V_t - E_t)$) operates identically across radically distinct anatomical wiring: from non-neural cell gap junctions to the petavoxel human cortex.
2. **Dynamical Pass Invariance:** Despite structural non-transfer (from 98.2% single-class fly bottleneck to distributed mammalian cortex), the dynamical Lyapunov contraction remains constant at rate $\mu pprox -1.0$.
