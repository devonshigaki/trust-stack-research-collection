# PRE-REGISTRATION — Sim AT-MUSIC: Macroscale Assembly Theory and GTT Causal Memory

**Date:** 2026-11-01  
**Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)

## 1. Theoretical Motivation: GTT as the Microscale Engine of Assembly Theory

Lee Cronin and Sara Walker's Assembly Theory (AT) posits that high-complexity objects require a physical force called *selection* to exist. However, AT is retrodictive: the Assembly Index ($a$) counts the steps required to build an object, but standard AT provides no forward dynamical equation for *why* a specific bond survives thermal noise. Furthermore, while the mass spectrometer measures $a$ for molecules, macroscale AT (language, music, ledgers) requires algorithmic graph decomposition (the Smallest Grammar Problem).

We hypothesize that the General Theory of Trust (GTT) is the missing microscale causal engine—the "Memory Maker." The discrete Master Stability Law ($\Delta S = \lambda(V - E)$) is the exact physical mechanism that evaluates validation and restricts degrees of freedom to form a bond (or musical motif), thereby generating macroscale Assembly.

## 2. Simulation Architecture (Sim AT-MUSIC)

We simulate the generation of a 1D symbolic sequence representing musical motifs over $N = 5,000$ steps.
*   **Alphabet:** 12 discrete pitch classes.
*   **Null Regime (Thermodynamic Walk):** Symbols are generated and joined completely at random.
*   **GTT Regime (Causal Memory Maker):** Symbols are joined into motifs. A motif survives and is appended to the sequence only if the environmental rhythmic validation ($V_t$) matches the expected meter ($E_t$). The motif's trust state updates via $\Delta S_t = \lambda(V_t - E_t)$. If $S_t \le 0$, the motif breaks (amnesia). 

**Measurement Tool (No Mass Spectrometer):**
We approximate the Assembly Index ($ASI$) of the generated sequences using the **Re-Pair (Recursive Pairing)** grammar compression algorithm, which iteratively identifies the most frequent adjacent digrams, constructing a Straight-Line Program (SLP).

## 3. Frozen Empirical Criteria

1.  **Criterion AT-M1 (Macro-Complexity Acceleration):** The GTT causal engine must generate a musical sequence with an Assembly Index significantly higher than the Null regime.
    *   **Metric:** Ratio of Assembly Index $ASI(\text{GTT}) / ASI(\text{Null})$.
    *   **Threshold:** Ratio $\ge 3.0$.
2.  **Criterion AT-M2 (The Selection Phase Transition):** The GTT sequence must cross the AT selection threshold, proving true historical memory accumulation, while the random walk fails.
    *   **Metric:** Absolute $ASI(\text{GTT})$.
    *   **Threshold:** $ASI(\text{GTT}) > 15$.
3.  **Criterion AT-M3 (Algorithmic Divergence):** The GTT process generates hierarchical motifs (lineage), not just random Kolmogorov incompressibility.
    *   **Metric:** Difference between standard LZW dictionary size and Re-Pair Assembly Index.
    *   **Threshold:** $ASI(\text{GTT}) < \text{LZW}(\text{GTT})$ (indicating structured, compressible motif hierarchy rather than pure noise).

## 4. Execution Plan
- **File:** `experiments/simulations_repair_era/meta_simulation/sim_at_music_macro.py`
- **Output:** `results/sim_at_music_results.json` and `figures/docas/pipeline/fig_sim_at_music.png`.
- **Verdict:** A **COMPOUND PASS (3/3)** is required to formally integrate the Macro-Assembly Theory claims into the music and TDF subsections.
