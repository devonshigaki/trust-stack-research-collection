# PRE-REGISTRATION — Sim AMP: The Nervous System as an Evolutionary Trust Amplifier & The Fresh Protocol as a Digital Cellular Membrane

**Date:** 2026-11-01  
**Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)

## 1. Theoretical Motivation: Amplification and the Digital Cell Wall

The Trust Stack establishes that "the brain did not invent trust; trust invented the brain." However, this raises an essential evolutionary question: if pre-neural tissues already measured trust through gap junctions across hours (Sim L-Series, Sim B-Series), why did biology evolve a metabolically expensive brain?

**The Core Insight:** The brain is an **impedance-matched biological amplifier of trust**. The nervous system (axons, myelin, monoaminergic channels) accelerates the expectation–validation loop ($\Delta S = \lambda(V - E)$) from the slow diffusion of pre-neural tissues ($10^3\text{ s}$) into millisecond precision ($10^{-3}\text{ s}$), achieving a temporal amplification gain $G \approx 10^6\times$.

**The Compartmentalization Boundary (Resolving Sim AT-3):** In Sim AT, high sensitivity without physical compartmentalization caused catastrophic bond shattering under thermal noise ($0.22\times$ edge retention). Life solved this by inventing the **lipid bilayer cell membrane** to buffer internal state space from environmental noise. 

At the societal and digital scale, **The Fresh Protocol (TFP)**—distinct from any single application like FreshCredit—acts as the **digital cellular wall**. By assigning every agent an edge database (`libSQL`/SQLite) they hold and control, combined with blockchain cryptographic attestation for tamper-proof guarantees, TFP provides an intelligent, semi-permeable membrane. This membrane selectively filters external validation inputs, protecting the agent from surveillance and catastrophic breach cascades. FreshCredit is simply one financial instantiation running on top of this membrane.

## 2. Simulation Architecture (Sim AMP)

We evaluate three interconnected computational regimes across $N = 1,000$ agents over $10,000$ steps:

1.  **Regime 1: Pre-Neural Bioelectric Tissue Lattice (Levin Baseline):**
    *   Agents communicate via passive diffusive gap junctions ($\tau_{\text{cellular}} \approx 10^3\text{ s}$). Error resolution is slow and local.
2.  **Regime 2: Amplified Neural Network (DOCAS Brain Model):**
    *   Agents communicate via fast axonal spikes and monoaminergic RPE bursts ($\tau_{\text{neural}} \approx 10^{-3}\text{ s}$).
    *   Measures the temporal acceleration gain $G$ and verifies leading Lyapunov exponent invariance ($\lambda_{\text{Lyap}}$).
3.  **Regime 3: Digital Membrane Protection (The Fresh Protocol Architecture):**
    *   Agents exposed to high-frequency external adversarial noise (surveillance, credit data leaks, spoofed validations).
    *   *Sub-case A (Uncompartmentalized Centralized Database):* Single global ledger; errors cascade globally.
    *   *Sub-case B (TFP Digital Membrane):* Database-per-tenant edge isolation with cryptographic blockchain verification; acts as an intelligent selective-disclosure membrane.

## 3. Frozen Empirical Criteria

1.  **Criterion AMP-1 (Temporal Amplification Gain):** The neural monoaminergic architecture must accelerate the rate of expectation–validation error convergence by a gain factor $G \ge 10^4\times$ (empirical target $10^6\times$) relative to non-neural bioelectric diffusion.
    *   **Metric:** Ratio of error convergence half-lives $\tau_{\text{cellular}} / \tau_{\text{neural}}$.
    *   **Threshold:** $G \ge 10^4$.
2.  **Criterion AMP-2 (Lyapunov Contraction Invariance):** Despite a million-fold acceleration in processing speed, the leading Lyapunov exponent must remain inside the universal contraction corridor $[-1.10, -0.90]$, proving the brain amplifies speed without inducing chaotic instability.
    *   **Metric:** $\lambda_{\text{Lyap}}$ of the amplified neural regime.
    *   **Threshold:** $\lambda_{\text{Lyap}} \in [-1.10, -0.90]$.
3.  **Criterion AMP-3 (Semi-Permeable Membrane Gating):** Under severe external validation noise ($\sigma = 2.0$), the TFP semi-permeable digital cellular membrane (database-per-tenant + blockchain verification with realistic permeability $\gamma_M = 0.12$, device loss, and key loss) must maintain contractual retention within $[80.0\%, 95.0\%]$, whereas the uncompartmentalized centralized architecture collapses below $25.0\%$.
    *   **Metric:** Ratio of surviving contracts under noise.
    *   **Threshold:** Retention(TFP) $\in [80.0\%, 95.0\%]$ and Retention(Centralized) $\le 25.0\%$.

## 4. Execution Plan
- **File:** `technical-appendix/sim-code/sim_amp_trust_amplifier.py`
- **Output:** `technical-appendix/numbers/sim_amp_results.json`, `papers/source/figures/fig_sim_amp_amplifier.png`, and `technical-appendix/AMP_SERIES_RUN_REPORT.md`.
- **Verdict:** A **COMPOUND PASS (3/3)** is required to formally integrate the Trust Amplifier and Digital Cellular Membrane claims into the manuscripts.
