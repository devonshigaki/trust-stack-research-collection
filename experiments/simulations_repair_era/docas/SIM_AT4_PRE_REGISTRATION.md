# PRE-REGISTRATION: SIMULATION AT-4
**Metabolome-Wide Molecular Assembly & Allosteric Information-Token Partition**  
**Document ID:** `SIM_AT4_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.2)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — biophysics & chemical graph theory]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
In Assembly Theory (Cronin, Walker, Marshall, 2021, 2023), $MA \ge 15$ is established as the empirical threshold where spontaneous abiotic thermal formation becomes statistically zero ($P < 10^{-23}$), serving as a definitive biosignature of life and selection. In Sim AT-2, cyclic adenosine monophosphate (cAMP) was derived at $MA = 14$—sitting on the exact razor's edge of living selection.

**Core Research Question:**
Is the positioning of cAMP at $MA = 14$ an arbitrary numerical coincidence, or does it represent an invariant biophysical property of cellular information processing? Specifically, among the ~18,000 small molecules in the human metabolome (HMDB / KEGG), do other molecules share $MA = 13\text{--}15$, and if so, how does their functional teleology differ from cAMP?

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (The Transition Window Cluster):** A non-zero fraction (~3% to 6%) of small-molecule human metabolites will exhibit $MA \in [13, 15]$, corresponding to the molecular weight window of 250–400 Da.
*   **Hypothesis H2 (The Functional Divide):** Non-token metabolites in the $MA \in [13, 15]$ window will fall into one of three distinct classes:
    1.  *Metabolic Fuels* (e.g., Fructose-1,6-bisphosphate), which are catabolized and destroyed for thermodynamic free energy ($\Delta G$).
    2.  *Genetic Monomers* (e.g., AMP, GMP, PRPP), which serve as structural building blocks.
    3.  *Catalytic Cofactors* (e.g., Biotin, $BH_4$, PLP), which are permanently bound enzyme prosthetics with slow turnover ($\tau > 10\text{ s}$).
*   **Hypothesis H3 (The Information-Token Singularity):** Across the entire metabolome, **only the cyclic purine nucleotide twins—cAMP ($MA = 14$) and cGMP ($MA = 14$)—operate as pure, non-consumed allosteric information tokens** characterized by sub-100 ms turnover clearance.

---

## 3. Dataset & Sampling Frame
A stratified sample of 57 endogenous human metabolites spanning all 6 primary biochemical functional classes:
1.  Allosteric Information Tokens (cAMP, cGMP, cCMP, cUMP, IP3, DAG).
2.  Prebiotic / Simple Neurotransmitters (NO, GABA, Glycine, Glutamate, Dopamine, Serotonin, Acetylcholine).
3.  Central Metabolic Fuels (Pyruvate, Lactate, Citrate, Fumarate, Glucose-6-P, Fructose-1,6-bisphosphate).
4.  Genetic Monomers & Nucleotide Phosphates (Adenine, Adenosine, AMP, ADP, ATP, GMP, GTP, PRPP).
5.  Catalytic Cofactors & Vitamins (Biotin, $BH_4$, PLP, Pantothenate, TPP, NAD+, CoA).
6.  Endocrine Steroids & Peptides (Cortisol, Aldosterone, Testosterone, Estradiol, Oxytocin, Vasopressin).

---

## 4. Frozen Acceptance & Falsification Criteria
The simulation will evaluate three frozen criteria. A compound verdict of **PASS** requires satisfying all three simultaneously without post-hoc threshold adjustment:

*   **Criterion C1 (Life-Transition Alignment):**
    cAMP and cGMP must sit strictly at $MA = 14$, within the immediate sub-threshold boundary of life ($MA < 15$).
    *Threshold:* $MA(\text{cAMP}) = 14 \land MA(\text{cGMP}) = 14$.
*   **Criterion C2 (Fuel & Structural Exclusion):**
    Zero metabolic fuels or genetic monomers shall qualify as non-consumed allosteric information tokens.
    *Threshold:* False-positive token rate for metabolic fuels $= 0.0\%$.
*   **Criterion C3 (Purine Uniqueness):**
    cAMP and cGMP must be the unique dual cyclic purine tokens at $MA = 14$ combining sub-100 ms turnover with universal allosteric gating.
    *Threshold:* $\text{Set}(\text{Tokens at } MA=14) = \{\text{"cAMP"}, \text{"cGMP"}\}$.

---

## 5. Execution Script & Artifact Commit
*   **Script:** `experiments/simulations_repair_era/docas/sim_at4_metabolome_assembly_partition.py`
*   **Output Files:** `sim_at4_results.json`, `fig_at4_metabolome_assembly_partition.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 15.
