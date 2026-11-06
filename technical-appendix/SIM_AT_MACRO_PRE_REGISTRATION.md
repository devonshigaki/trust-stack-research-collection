# PRE-REGISTRATION — Sim AT-MACRO: Economic Assembly Theory and the Origin of Wealth

**Date:** 2026-11-01  
**Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)

## 1. Theoretical Motivation: Beinhocker Complexity and GTT

In *The Origin of Wealth*, Eric Beinhocker frames the economy as a Complex Adaptive System driven by the evolutionary algorithm of Differentiation, Selection, and Amplification. Economic wealth is mathematically defined as order (low entropy/high complexity) generated out of chaos. 

In Assembly Theory (AT), the Assembly Index ($a$) quantifies the historical memory (selection steps) required to build a complex object. While AT is retrodictive, we posit that the General Theory of Trust (GTT) is the forward causal engine—the "memory maker." The discrete Master Stability Law ($\Delta S_t = \lambda(V_t - E_t)$) provides the exact mathematical mechanism for Beinhocker's "Selection" step. An economic contract (a bond) survives environmental shocks only if trust remains positive.

## 2. Simulation Architecture (Sim AT-MACRO)

We model an economic ledger over $N = 5,000$ epochs among $500$ agents.
*   **The Ledger:** Represented as a 1D sequence of executed contracts (e.g., Agent A trades with Agent B). 
*   **Null Regime (Frictionless / Random Economy):** Agents trade randomly, representing a high-entropy, low-memory economic environment.
*   **GTT Regime (Trust-Bound Economy):** Agents establish continuous trading relationships (economic bonds). A bond is validated by market conditions ($V_t$) against the contractual expectation ($E_t$). Trust updates via $\Delta S = \lambda(V - E)$. The trade is only executed and logged if $S_t > 0$. If $S_t \le 0$, the relationship breaks (bankruptcy/defection).

**Measurement Tool:**
We approximate the Macro-Assembly Index ($ASI$) of the economic ledger using the **Re-Pair (Recursive Pairing)** algorithm, which extracts the smallest grammar (hierarchical supply chains and institutional structures) from the transaction sequence.

## 3. Frozen Empirical Criteria

1.  **Criterion AT-MAC-1 (Institutional Complexity Generation):** The GTT-driven economy must generate a ledger with an Assembly Index significantly higher than the random economy, proving that trust allows complex supply chains (hierarchical motifs) to form.
    *   **Metric:** Ratio of Assembly Index $ASI(\text{GTT}) / ASI(\text{Null})$.
    *   **Threshold:** Ratio $\ge 2.0$.
2.  **Criterion AT-MAC-2 (Algorithmic Divergence / Wealth as Order):** Beinhocker posits that wealth is order. A purely random economy will have high Kolmogorov complexity (incompressible noise) but low Assembly (no reusable lineage). The GTT economy must show structured divergence.
    *   **Metric:** Difference between standard LZW dictionary size (noise) and Re-Pair Assembly Index (order).
    *   **Threshold:** $ASI(\text{GTT}) < 0.5 \times \text{LZW}(\text{GTT})$.
3.  **Criterion AT-MAC-3 (The Institutional Phase Transition):** The GTT ledger must cross the AT selection threshold ($ASI > 15$), proving it is a product of true historical selection rather than stochastic fluctuation.
    *   **Metric:** Absolute $ASI(\text{GTT})$.
    *   **Threshold:** $ASI(\text{GTT}) > 15$.

## 4. Execution Plan
- **File:** `experiments/simulations_repair_era/meta_simulation/sim_at_macro_society.py`
- **Output:** `results/sim_at_macro_results.json` and `figures/docas/pipeline/fig_sim_at_macro.png`.
- **Verdict:** A **COMPOUND PASS (3/3)** is required to formally integrate the Macro-Assembly Theory claims into the Whitepaper and GTT macroeconomics sections.
