# PRE-REGISTRATION: SIMULATION GEN-4
**Adenylyl Cyclase Coincidence Engine eQTL & Cognitive Flexibility Mendelian Randomization**  
**Document ID:** `SIM_GEN4_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.3)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — statistical genomics & causal inference]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
While *PDE4B* acts as the enzymatic degradation brake on the $MA = 14$ cAMP prediction-error token (Sim G24 / Sim GEN-2 / Sim PATCH-1), the actual enzymatic synthesis and coincidence detection of the token is driven by three specific adenylyl cyclases:
1.  **ADCY5 (Striatum):** Integrates cortical glutamate with phasic dopamine ($G_{\alpha\mathrm{olf}}$) and cholinergic signals ($G_{\alpha\mathrm{i}}$) in Medium Spiny Neurons.
2.  **ADCY1 (Hippocampus/PFC):** Calcium/calmodulin-stimulated ($\text{Ca}^{2+}/\text{CaM}$) adenylyl cyclase driving LTP and initial trust-trace consolidation.
3.  **ADCY8 (Cortex/Thalamus):** Calcium/calmodulin-stimulated adenylyl cyclase mediating depotentiation (LTD), reversal learning, and cognitive flexibility to overwrite outdated priors after contractual betrayal (*rutabaga* ortholog).

**Core Research Question:**
Do genetically instrumented expression levels of *ADCY1*, *ADCY8*, and *ADCY5* in human brain tissue causally predict behavioral trust updating, cognitive flexibility, and protection against paranoic prior rigidity?

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (The Synthesis Engine Triad):** Genetically instrumented brain eQTLs for *ADCY5*, *ADCY1*, and *ADCY8* will account for $> 65\%$ of the total heritable variance in second-messenger cAMP coincidence capacity across basal ganglia and association cortex.
*   **Hypothesis H2 (ADCY8 Reversal Learning Causal Effect):** Genetically elevated *ADCY8* expression in cortical tissue causally predicts higher cognitive flexibility and faster Bayesian updating following betrayal ($\beta_{\mathrm{IVW}} > 0.15, p < 1.0 \times 10^{-6}$), preventing compensatory paranoid prior rigidity ($S_{100} \le 0.250$).
*   **Hypothesis H3 (ADCY5 Striatal Reinforcement Integrity):** Genetically predicted *ADCY5* deficiency is associated with impaired reward-prediction sensitivity ($\lambda_{\mathrm{reward}}$) and elevated motor-decision latency.

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Instrument Strength & F-Statistic):**
    All independent eQTL instrumental variables for *ADCY5*, *ADCY1*, and *ADCY8* must satisfy the weak instrument exclusion threshold: $F > 25.0$.
*   **Criterion C2 (Causal Reversal Association):**
    Inverse-Variance Weighted (IVW) 2S-MR effect of genetically instrumented *ADCY8* on cognitive flexibility / betrayal updating rate must be positive and statistically significant:
    $$\beta_{\mathrm{IVW}}(\text{ADCY8}) \ge 0.150, \quad p_{\mathrm{IVW}} \le 1.0 \times 10^{-6}$$
*   **Criterion C3 (Egger Pleiotropy Intercept):**
    MR-Egger horizontal pleiotropy intercept must not significantly differ from zero: $|p_{\mathrm{intercept}}| > 0.05$.

---

## 4. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/clinical/sim_adcy_coincidence_genomics.py`
*   **Output Files:** `sim_gen4_results.json`, `fig_gen4_adcy_coincidence.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 24.
