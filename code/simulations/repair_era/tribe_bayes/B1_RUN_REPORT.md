# Sim B1 Run Report: Closed-Loop Streaming BOLD to Bayesian Filter

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN (Seed = 42)
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010]
**Compound Verdict:** **COMPOUND PASS (2/2 CRITERIA SATISFIED)**

---

## 1. Summary of Pre-Registered Results

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **C1: Estimation Superiority** | MSE reduction of tracked trust state $S_t$ using DMN-augmented Kalman filter vs behavior-only baseline. | $\ge 40.0\%$ | **$46.9\%$** | **PASS** |
| **C2: Dynamic Parameter Tracking** | Pearson correlation $r$ between estimated tracking sensitivity $\hat{\lambda}_t$ and ground-truth $\lambda_t$. | $r \ge 0.85$ | **$r = 0.996$** | **PASS** |

---

## 2. Theoretical Breakdown and Findings

This simulation bridges the open-loop fMRI predictions of TRIBE v2 (from `tdf.tex` §5.2) with the active dynamic tracking of the General Theory of Trust (`gtt.tex` §6). By simulating a 10-turn trust game where the agent's underlying trust sensitivity ($\lambda_t$) drifts due to cognitive volatility, we established that behavior alone is insufficient to track rapid sensitivity shifts (especially under high process noise, resulting in poor baseline open-loop integration).

However, introducing an in-silico DMN (Default Mode Network) BOLD proxy—which measures the neural threat/safety semantics evaluated by TRIBE v2—provides the Kalman/EM filter with an independent continuous reading of the latent $\lambda_t$ variable. The augmented filter successfully exploited this multimodal proxy, yielding a 46.9% reduction in tracking MSE and near-perfect parameter tracking ($r=0.996$). This confirms that closed-loop neural encoding dramatically outperforms pure behavioral observation when estimating transient cognitive trust states.