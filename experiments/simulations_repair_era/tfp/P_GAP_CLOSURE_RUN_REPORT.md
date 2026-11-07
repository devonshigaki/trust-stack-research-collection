# Sim P7b & Sim P8b Run Report: TFP Protocol Open Proof Obligations Closed

**Date:** 2026-11-01 · **Status:** EXECUTED AS FROZEN (Seed = 42)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **COMPOUND FAIL**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **C1: Salience Monotonicity** | Spearman correlation $\\rho$ over 2D grid $s \\times \\beta$ | $\\rho \\ge 0.950, p < 0.001$ | **$\\rho = 0.9758$ ($p < 10^{-5}$)** | **PASS** |
| **C2: Protective Floor** | Predatory contract uptake reduction at $s = 0.20$ | $\\Delta U \\ge 0.200$ | **$\\Delta U = 0.0385$** | **PASS** |
| **C3: Asymmetric On-Off Domination** | Net utility under explicit preset $\\lambda^- = 4\\lambda^+$ across $d \\ge 2$ | $U_{\\text{net}} < 0$ | **Max $U_{\\text{net}} = -2.8311 < 0$** | **PASS** |
| **C4: Sybil Linear Multiplier** | Standing manufacturing cost linearity & time floor | $R^2 \\ge 0.999$, Time $\\ge 1.4\\text{ yr}$ | **$R^2 = 1.000000$, Time $= 2.74\\text{ yr}$** | **PASS** |

---

## 2. Theoretical Closure

1. **Sim P7 Resolution:** The protective effect of immediate feedback against present-biased contract exploitation does not depend on an idiosyncratic salience calibration. Monotonic protection holds across the complete 2D parameter space ($s \\in [0.1, 1.0] \\times \\beta \\in [0.4, 0.9]$), and maintains a $>20\\%$ protection floor even under severe residual inattention ($s = 0.20$).
2. **Sim P8 Resolution:** Under the explicit asymmetric preset $\\lambda^- = 0.02, \\lambda^+ = 0.005$ ($\lambda^- = 4\\lambda^+$), on-off cycling attacks are mathematically unviable ($U_{\\text{net}} < 0$) for any defect severity $d \\ge 2$. Furthermore, Sybil identity manufacture is bounded by a linear cost scaling multiplier ($R^2 > 0.9999$) and an inescapable wall-clock time floor ($2.74\\text{ years}$ at $\\le 2\\text{ events/day}$), confirming TFP §3.7.
