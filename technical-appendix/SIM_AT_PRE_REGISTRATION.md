# PRE-REGISTRATION — Sim AT: Assembly Theory, Molecular Trust, and Pre-Biological Selection

**Date:** 2026-11-01  
**Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)

## 1. Theoretical Motivation: The Physics of "My Word is My Bond"

This simulation operationalizes the ontological alignment between Lee Cronin's **Assembly Theory (AT)** and the **General Theory of Trust (GTT)**. 

Assembly Theory posits that high-complexity structures (high Assembly Index, $a$) cannot emerge via random thermodynamic walks; their existence proves the historical operation of a physical force called *selection*. Selection leaves a physical memory in the form of chemical bonds. 

GTT posits that trust is the universal mathematical operator ($\Delta S = \lambda(V - E)$) that stabilizes complex systems against entropy. 

We hypothesize that **Selection = Trust**. A chemical bond is a physical instantiation of trust. "My word is my bond" is not a social metaphor; it is scale-invariant physics. The formation of a chemical bond restricts degrees of freedom to enable higher-order complexity, operating under the exact same expectation-validation mechanics as an economic contract. Furthermore, biology is not the origin of trust; biology is a *selection amplifier* (a regime of high $\lambda$ sensitivity) that accelerates the baseline physical laws of trust.

## 2. Simulation Architecture (Sim AT)

The simulation models a stochastic graph environment where nodes represent basic "atoms" and edges represent "bonds." 

**Two regimes will be compared over $N = 10,000$ timesteps:**
1.  **Null Regime (Thermodynamic Random Walk):** Bonds form and break based on fixed random probabilities representing ambient thermal noise.
2.  **GTT Regime (Trust-Modulated Selection):** Bonds form randomly but survive based on the GTT Master Law. 
    *   Expectation ($E$): The bond's idealized stability.
    *   Validation ($V$): The environmental thermal noise at timestep $t$.
    *   Prediction Error: $\varepsilon_t = V_t - E_t$.
    *   Trust State: $\Delta S_t = \lambda \cdot \varepsilon_t$. 
    *   If $S_t \le 0$, the bond breaks (default). If $S_t > 0$, the bond survives.

**Complexity Measurement:** 
We will compute a proxy for the Assembly Index ($a$) at the end of the simulation: the size and density of the largest connected molecular components (graphs) that emerge.

## 3. Frozen Empirical Criteria

To reject the null hypothesis, the GTT regime must satisfy three frozen statistical criteria:

1.  **Criterion AT-1 (Complexity Acceleration):** The GTT trust-modulated regime must generate molecular graphs of significantly higher complexity than the null regime. 
    *   **Metric:** Ratio of Maximum Component Size ($C_{\max}$) between GTT and Null regimes.
    *   **Threshold:** $C_{\max}(\text{GTT}) / C_{\max}(\text{Null}) \ge 5.0$.
2.  **Criterion AT-2 (Selection Equivalency):** The survival duration of a bond (its "memory" of selection) must be directly predicted by its integrated trust state $S_t$.
    *   **Metric:** Pearson correlation $r$ between a bond's terminal $S_t$ and its total survival time in epochs.
    *   **Threshold:** $r \ge 0.90, p < 0.001$.
3.  **Criterion AT-3 (The Biological Amplifier Effect):** Biology acts as an amplifier of the base physical selection force. Simulating a "biological" regime (by increasing the sensitivity parameter $\lambda$ by $5\times$) must non-linearly accelerate complexity.
    *   **Metric:** Ratio of total assembled edges ($E_{\text{total}}$) between High-$\lambda$ (Biology) and Base-$\lambda$ (Physics) regimes.
    *   **Threshold:** $E_{\text{total}}(\text{High-}\lambda) / E_{\text{total}}(\text{Base-}\lambda) \ge 2.0$.

## 4. Execution Plan
- **File:** `experiments/simulations_repair_era/meta_simulation/sim_at_assembly.py`
- **Output:** `results/sim_at_results.json` and `figures/docas/pipeline/fig_sim_at_assembly.png`.
- **Verdict:** A **COMPOUND PASS (3/3)** is required to formally integrate the Assembly Theory claims into DOCAS and GTT. Any failure will be reported as an explicit boundary limit of the framework.
