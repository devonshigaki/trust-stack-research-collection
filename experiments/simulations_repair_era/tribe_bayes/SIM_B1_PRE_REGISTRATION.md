# PRE-REGISTRATION — Sim B1: Closed-Loop Streaming BOLD to Bayesian Filter (TRIBE-BAYES-STREAM)

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010]
**Research Stack:** DOCAS §5.2 / GTT §6

## 1. Domain Hypothesis & Theoretical Motivation

While `tdf.tex` §5.2 proved that TRIBE v2 deterministically maps text offers to cortical predictions (notably separating predatory vs. fair offers in the Default Mode Network, DMN), this was tested as an open-loop, static forward encoder. In real-time multi-turn trust interactions, an agent's hidden trust sensitivity ($\lambda_t$) fluctuates. 
**Hypothesis (B1):** Passing a live, 100-TR in-silico fsaverage5 cortical proxy (representing the DMN semantic threat activation) into a continuous Bayesian state-space tracker (Kalman/EM filter) during a 10-turn game will significantly improve the estimation accuracy (lower Mean Squared Error, MSE) of the agent's true hidden trust trajectory ($S_t$) compared to a behavioral-only (mismatch $\varepsilon_t$) baseline.

## 2. Frozen Quantitative Criteria

### Criterion C1 (Estimation Superiority):
The DMN-augmented Kalman filter must reduce the MSE of the tracked trust state $S_t$ by at least **40.0%** relative to the behavior-only baseline filter across 1,000 simulated multi-turn trajectories.

### Criterion C2 (Dynamic Parameter Tracking):
The DMN-augmented filter must maintain a Pearson correlation $r \ge 0.85$ between the estimated tracking sensitivity $\hat{\lambda}_t$ and the ground-truth volatility-driven $\lambda_t$.

## 3. Experimental Parameters & Methodology
- $N = 1,000$ episodes, $T = 10$ turns per episode.
- Ground truth $\lambda_t$ drifts via a random walk reflecting cognitive volatility.
- Observation vector $Y_t$ for Baseline: Behavioral mismatch $\varepsilon_t$.
- Observation vector $Y_t$ for Augmented: Behavioral mismatch $\varepsilon_t$ + DMN BOLD proxy activation $B_t$ (scaled by true $\lambda_t$ + noise).
- Kalman Filter tracks state $X_t = [S_t, \lambda_t]^T$.
- **Random Seed:** Strict `seed=42`.

## 4. Compound Verdict Rule
- **PASS:** Criteria C1 and C2 met under frozen thresholds.
- **FAIL:** Any criterion fails.