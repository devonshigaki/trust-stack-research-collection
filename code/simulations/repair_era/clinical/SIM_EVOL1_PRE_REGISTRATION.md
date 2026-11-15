# PRE-REGISTRATION: SIMULATION EVOL-1
**Cross-Species Evolutionary Conservation of the cAMP Coincidence Engine: Drosophila *rutabaga* to Human *ADCY8/1***  
**Document ID:** `SIM_EVOL1_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.3)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — evolutionary genomics & molecular conservation]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
To resolve whether the enzymatic synthesis of the $MA = 14$ cAMP prediction-error token is an idiosyncratic feature of mammalian brains or an invariant evolutionary mechanism for associative memory and reversal learning.

Examines the sequence, structural homology, and reversal-learning phenotype between the foundational *Drosophila melanogaster* associative learning gene ***rutabaga*** (FBgn0003301; Levin et al., 1992) and human calcium/calmodulin-stimulated adenylyl cyclases ***ADCY8*** (ENSG00000155897) and ***ADCY1*** (ENSG00000138399) across 600 million years of metazoan evolution.

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (Deep Catalytic Domain Homology):** The C1a and C2a catalytic domains that coordinate ATP cyclization ($MA=14$) exhibit $\ge 65.0\%$ amino acid sequence identity between Drosophila *rutabaga* and human *ADCY8*, proving that the molecular machinery of prediction-error synthesis predates the divergence of protostomes and deuterostomes.
*   **Hypothesis H2 (Calmodulin Binding Motif Invariance):** The 1-5-10 amphipathic alpha-helical Calmodulin-binding domain (CaMBD) maintains a conservation score $\ge 0.80$, preserving calcium-coincidence gating across evolutionary time.
*   **Hypothesis H3 (Cross-Species Reversal Extinction Phenotype):** In simulated associative conditioning assays, *rutabaga* loss-of-function mutants display $\ge 3.0\times$ longer extinction latencies when conditioned contingencies reverse, mirroring the paranoic prior rigidity observed under human *ADCY8* down-regulation.

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Catalytic Core Sequence Identity):**
    Pairwise sequence identity in the catalytic ATP-cyclization core must satisfy:
    $$\text{Identity}(rutabaga_{\mathrm{cat}}, ADCY8_{\mathrm{cat}}) \ge 65.0\%$$
*   **Criterion C2 (CaMBD Motif Conservation):**
    The amphipathic CaM-binding motif must achieve a conservation score $\ge 0.800$.
*   **Criterion C3 (Extinction Latency Phenotype):**
    Simulated contingency reversal extinction latency ratio between mutant and wild-type must satisfy:
    $$\tau_{\mathrm{extinction}}(\mathrm{mutant}) / \tau_{\mathrm{extinction}}(\mathrm{WT}) \ge 3.00\times$$

---

## 4. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/clinical/sim_evol1_rutabaga_adcy8_conservation.py`
*   **Output Files:** `sim_evol1_results.json`, `fig_evol1_rutabaga_adcy8.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 25.
