# PRE-REGISTRATION: SIMULATION PATCH-1
**Multicompartmental Pyramidal Cell HCN1 Shunting Kinetics**  
**Document ID:** `SIM_PATCH1_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.2)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — biophysical electrophysiology & cable theory]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
Models Amy Arnsten's prefrontal Layer III apical dendritic spine microcircuits under stress. Incorporates Constantinos Paspalas's gold-labeled immuno-EM localization of HCN1 and KCNQ channels to test how a supercritical cAMP storm (1.50 uM) alters dendritic cable transfer and shunts somatic EPSP transmission.

---

## 2. Frozen Verification Criteria
*   **Criterion C1 (cAMP-Dependent Half-Activation Shift):**
    Supercritical cAMP ($1.50\text{ }\mu\text{M}$) must shift HCN1 $V_{1/2}$ depolarizing by $\ge +8.0\text{ mV}$ (from $-85.0\text{ mV}$ to $\ge -75.0\text{ mV}$).
*   **Criterion C2 (Dendritic Attenuation Ratio):**
    Peak apical-to-soma EPSP voltage transfer ratio ($V_{\mathrm{soma}} / V_{\mathrm{dend}}$) must drop by $\ge 25\%$ (from baseline $0.463$ to $\le 0.347$).
*   **Criterion C3 (Somatic EPSP Suppression):**
    Somatic EPSP peak amplitude must be suppressed by $\ge 35\%$ under supercritical cAMP (from baseline $4.63\text{ mV}$ to $\le 3.00\text{ mV}$).

---

## 3. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/docas/sim_patch_clamp_hcn_shunting.py`
*   **Output Files:** `sim_patch1_results.json`, `fig_patch1_hcn_shunting.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 13.
