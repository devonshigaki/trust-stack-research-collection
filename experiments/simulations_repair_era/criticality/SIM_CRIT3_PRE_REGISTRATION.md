# PRE-REGISTRATION: SIMULATION CRIT-3
**Bayes Factor Model Falsification: Quasicritical Trust vs. Standard Non-Critical Learning Models**  
**Document ID:** `SIM_CRIT3_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.3)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — Bayesian model comparison & spectral time-series]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
To test whether empirical human trust dynamics in multi-round iterative trust games (e.g., King-Casas et al., 2005; Berg et al., 1995) require a **Quasicritical Attractor substrate ($\rho \approx 0.98$)** or can be explained by standard non-critical learning architectures (Rescorla-Wagner, Drift-Diffusion Models, or fixed-scale Hierarchical Gaussian Filters).

Evaluates the Long-Range Temporal Correlation (LRTC) scaling exponent $\beta$ in the Power Spectral Density ($S(f) \propto 1/f^\beta$) of the prediction-error stream, and computes the formal marginal likelihood and Bayes Factor ($\text{BF}_{10}$) across candidate models.

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (Scale-Free Pink Noise Signature):** The GTT Quasicritical Master Law operating at $\rho = 0.98$ generates a power spectral density exponent $\beta \in [0.70, 1.20]$ ($1/f^\beta$ pink noise), matching empirical electrophysiological and behavioral fluctuation dynamics.
*   **Hypothesis H2 (Markovian Failure):** Standard non-critical models fail to capture long-range memory: Rescorla-Wagner produces white noise ($\beta < 0.30$), while Drift-Diffusion Models produce random-walk red noise ($\beta \ge 1.70$).
*   **Hypothesis H3 (Decisive Bayesian Evidence):** In a formal Bayesian model comparison across $N = 100$ iterative trust sessions, the marginal log-likelihood of the Quasicritical model decisively exceeds standard non-critical models by a Bayes Factor $\text{BF} \ge 100.0$ ($\log_{10} \text{BF} \ge 2.0$; decisive evidence on Jeffreys' scale).

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Quasicritical LRTC Exponent):**
    The spectral decay exponent of the GTT model must satisfy $\beta_{\mathrm{GTT}} \in [0.75, 1.15]$.
*   **Criterion C2 (Model Discrimination Spread):**
    $|\beta_{\mathrm{GTT}} - \beta_{\mathrm{RW}}| \ge 0.50$ and $|\beta_{\mathrm{GTT}} - \beta_{\mathrm{DDM}}| \ge 0.50$.
*   **Criterion C3 (Decisive Bayes Factor):**
    The Bayes Factor favoring the Quasicritical model over the next best non-critical model must satisfy:
    $$\text{BF}_{10} \ge 100.0 \quad (\Delta \mathrm{BIC} \ge 10.0)$$

---

## 4. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/criticality/sim_crit3_bayes_factor_comparison.py`
*   **Output Files:** `sim_crit3_results.json`, `fig_crit3_bayes_factors.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 26.
