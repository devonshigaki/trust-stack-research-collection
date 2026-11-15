# PRE-REGISTRATION: SIMULATION CRIT-2
**Connectome Spectral Radius & Quasicritical Attractor Invariant**  
**Document ID:** `SIM_CRIT2_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.3)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — empirical connectomics & spectral graph theory]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
To resolve the Critical Brain Hypothesis (CBH) and the Critical Slowing Down paradox by establishing that mammalian cortical wiring does not sit statically at exact criticality ($\sigma = 1.000$), but operates as a **quasicritical reverberating attractor ($\rho \approx 0.98$)** whose stability is dynamically maintained by the GTT Master Law via cAMP allosteric modulation.

Evaluates the raw, empirical synaptic adjacency matrix of the **MICrONS mouse visual cortex connectome** (42,744 nodes, 722,253 synapses) and the **FlyWire whole-brain connectome** under realistic membrane leak conductance.

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (Quasicritical Corridor):** Under physiological membrane leak ($\delta_{\mathrm{leak}} \in [0.01, 0.04]$), the leading eigenvalue (spectral radius $\rho(W)$) of the empirical recurrent connectome organically evaluates to $\rho \in [0.95, 0.99]$, definitively verifying the Wilting-Priesemann quasicritical safety margin.
*   **Hypothesis H2 (Subcritical Void Separation):** Shuffling synaptic weights or imposing hyper-damped inhibition collapses the spectral radius to $\rho < 0.85$, demonstrating the hypo-responsive "void."
*   **Hypothesis H3 (Supercritical Chaos Separation):** Unconstrained recurrent excitation without leak or inhibition forces $\rho > 1.05$, triggering runaway cascade instability ("chaos").

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Quasicritical Operating Point):**
    The empirical spectral radius of the normalized MICrONS connectome must satisfy:
    $$\rho(W_{\mathrm{microns}}) \in [0.960, 0.985]$$
*   **Criterion C2 (Void Boundary Check):**
    Hyper-damped control must yield $\rho \le 0.850$.
*   **Criterion C3 (Chaos Boundary Check):**
    Unconstrained excitatory control must yield $\rho \ge 1.050$.

---

## 4. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/criticality/sim_crit2_connectome_spectral_radius.py`
*   **Output Files:** `sim_crit2_results.json`, `fig_crit2_connectome_spectral_radius.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 23.
