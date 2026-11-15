# PRE-REGISTRATION: SIMULATION THERMO-1
**Thermodynamic Landauer Bound on Trust Erasure**  
**Document ID:** `SIM_THERMO1_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.2)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — non-equilibrium statistical mechanics]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
Under Landauer's Principle (Landauer, 1961; Bennett, 1982), erasing one bit of physical information in an environment at temperature $T$ dissipates a minimum thermodynamic heat penalty of:
$$\Delta Q \ge k_B T \ln 2$$
Sim THERMO-1 formalizes the thermodynamic cost of updating expectations in bounded cognitive and computational systems: validating an expected outcome ($\varepsilon > 0$) preserves internal model structure, whereas betrayal ($\varepsilon < 0$) forces an erasure and rewrite of internal priors, dissipating excess Landauer heat.

---

## 2. Frozen Verification Criteria
*   **Criterion C1 (Landauer Lower Bound Compliance):**
    Every single-bit model erasure under betrayal ($\lambda^- > \lambda^+$) must strictly dissipate $Q_{\mathrm{diss}} \ge k_B T \ln 2$ ($2.87 \times 10^{-21}\text{ J}$ at $298.15\text{ K}$).
*   **Criterion C2 (Asymmetric Heat Dissipation Ratio):**
    Because biological systems exhibit asymmetric betrayal weighting ($\lambda^- / \lambda^+ \approx 4.0$), model erasure under betrayal must dissipate $> 30\times$ more thermodynamic heat than confirmation ($Q_{\mathrm{betrayal}} / Q_{\mathrm{confirm}} \ge 30.0$).
*   **Criterion C3 (Silicon vs. Carbon Microarchitecture):**
    Silicon dispute resolution (executing Z3 SMT solver and cryptographic slashing on TFP nodes) must dissipate $> 2.0\times$ more energy than honest consensus updates.

---

## 3. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/docas/sim_landauer_trust_thermodynamics.py`
*   **Output Files:** `sim_thermo1_results.json`, `fig_thermo1_landauer_trust.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 11.
