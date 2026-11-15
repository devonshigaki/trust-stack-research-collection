# PRE-REGISTRATION: SIMULATION AT-5
**Multi-Constraint Information-Token Landscape & Monte Carlo Null Permutation Model**  
**Document ID:** `SIM_AT5_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.2)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — biophysical optimization & Monte Carlo statistics]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
To resolve whether the convergence of the second messengers cAMP and cGMP at $MA = 14$ on the Cronin life threshold is an artifact of "astronomical odds" or the unique global solution to an evolutionary constrained optimization problem.

The simulation formalizes the **Information-Token Optimization Problem**:
$$\min_{x \in \mathcal{M}} \left[ \text{Turnover Latency}(\tau) + \text{Synthesis Steps}(K) + \text{Landauer Dissipation}(\Delta Q) \right] \quad \text{s.t.} \quad \text{Steric Specificity}(x) \ge \theta_{\text{allosteric}}$$

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (Monte Carlo Empirical Sparsity):** Under an unconstrained null model drawing $N = 2,000,000$ random compounds from the empirical joint metabolome distribution (HMDB / KEGG parameter distributions), the empirical probability of randomly generating a compound meeting all 5 functional constraints of an intracellular prediction-error token is $P < 1.0 \times 10^{-6}$ (zero or near-zero hits in 2M trials).
*   **Hypothesis H2 (Pareto Optimality of $MA = 14$):** When plotting steric specificity against Landauer erasure cost, $MA = 14$ forms the unique Pareto frontier: molecules with $MA < 10$ fail the specificity lower bound ($\theta_{\text{allosteric}}$), while molecules with $MA \ge 18$ fail the 25 ms latency threshold.
*   **Hypothesis H3 (Physical Attractor vs. Coincidence):** Rather than an improbable lottery ticket, cAMP represents an evolutionary physical attractor—the unique mathematical supremum of single-step catalytic cyclization from ATP.

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Monte Carlo Null Rejection):**
    Across $N = 2,000,000$ Monte Carlo synthetic metabolome draws, the empirical joint probability of satisfying all 5 token axioms must be $P \le 5.0 \times 10^{-6}$ ($\le 10$ hits per 2 million; $p < 0.00001$).
*   **Criterion C2 (Pareto Invariant Boundary):**
    cAMP ($MA = 14$) must sit on the Pareto-optimal frontier, minimizing synthesis/erasure cost while maintaining steric specificity score $\ge 0.85$.
*   **Criterion C3 (Metabolome Ground Truth Concordance):**
    Across the real empirical human metabolome (HMDB 5.0), the only two compounds that satisfy all constraints must be the cyclic purine nucleotide twins (cAMP and cGMP).

---

## 4. Execution Artifacts
*   **Simulation Script:** `experiments/simulations_repair_era/docas/sim_at5_probabilistic_landscape.py`
*   **Output Files:** `sim_at5_results.json`, `fig_at5_probabilistic_landscape.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 16.
