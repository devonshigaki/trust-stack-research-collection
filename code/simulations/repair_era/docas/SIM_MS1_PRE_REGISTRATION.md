# PRE-REGISTRATION: SIMULATION MS-1
**Tandem Mass Spectrometry (LC-MS/MS) Fragmentation Assembly Benchmark**  
**Document ID:** `SIM_MS1_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.2)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — analytical mass spectrometry & assembly theory]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
Implements Lee Cronin's experimental mass-spectrometry assembly benchmark (Marshall et al., Nature Comm 2021) to algorithmically derive the Molecular Assembly Index ($MA$) from simulated Collision-Induced Dissociation (CID) fragmentation trees across the neuromodulatory and second-messenger cascade.

---

## 2. Frozen Verification Criteria
*   **Criterion C1 (Monotone Assembly-Peak Correlation):**
    Simulated CID tandem MS/MS peak counts must correlate with theoretical $MA$ at Pearson $r \ge 0.90$.
*   **Criterion C2 (cAMP Inflection Calibration):**
    The simulated fragmentation tree for cAMP ($m/z = 329.05$) must yield an empirical assembly index of $MA = 14 \pm 0.5$, exactly one unit below the life threshold ($MA = 15$).
*   **Criterion C3 (Prebiotic vs. Biological Separation):**
    Prebiotic amino acids/bases (Glycine, Adenine, Dopamine) must sit strictly at $MA \le 8$, while complex biological regulators (Cortisol, Oxytocin) sit strictly at $MA \ge 18$.

---

## 3. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/docas/sim_tandem_ms_assembly_trees.py`
*   **Output Files:** `sim_ms1_results.json`, `fig_ms1_fragmentation_assembly.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 12.
