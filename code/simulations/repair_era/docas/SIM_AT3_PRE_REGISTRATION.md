# PRE-REGISTRATION: SIMULATION AT-3
**Quantum Molecular Expectation vs. Active Biological Repair**  
**Document ID:** `SIM_AT3_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.2)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION & FORMAL SMT — quantum chemistry & biophysics]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
To resolve whether inanimate matter (such as an atomic crystal lattice of quartz) possesses "expectation," Sim AT-3 models the Silicon–Oxygen (Si–O) covalent bond under a quantum Morse potential:
$$V_{\mathrm{Morse}}(r) = D_e (1 - e^{-a(r - r_e)})^2$$
and compares it against active biological repair driven by the GTT Master Law ($\Delta S = \lambda(V - E)$) fueled by metabolic energy (ATP $\to$ cAMP, $MA=14$).

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (Linear Isomorphism):** Near ground-state equilibrium ($r \to r_e$), the conservative quantum restoring force linearizes identically to the GTT Master Law transverse contraction: $\lim_{\varepsilon \to 0} F_{\mathrm{Morse}}(\varepsilon) / (-k_{\mathrm{eff}} \varepsilon) = 1.0$.
*   **Hypothesis H2 (The Abiotic Fracture Boundary):** Under shear displacements exceeding the potential well's inflection point ($r > r_{\mathrm{yield}}$), the restoring force vanishes ($F \to 0$), causing the inanimate crystal to shatter irreversibly.
*   **Hypothesis H3 (Active Non-Equilibrium Biological Repair):** Living systems escape this fracture boundary by deploying an active restoring pump ($F_{\mathrm{active}} = -k_{\mathrm{pump}}\operatorname{sgn}(\varepsilon)$) fueled by ATP $\to$ cAMP ($MA=14$), restoring the bond to equilibrium even across the dissociation tail.

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Harmonic Spring Constant):** Near equilibrium, $k_{\mathrm{eff}} = 2 D_e a^2 \ge 30.0\text{ eV/\AA}^2$ with Pearson correlation $r = 1.0$ against linear contraction.
*   **Criterion C2 (Abiotic Fracture):** Severe shear displacement forces the inanimate bond into the dissociation tail ($r > 10.0\text{ \AA}$), with `Broken = True`.
*   **Criterion C3 (Active Biological Repair):** Active metabolic pumping restores displaced bonds back to $|r - r_e| \le 0.10\text{ \AA}$, with `Repaired = True`.

---

## 4. Execution Artifacts
*   **Simulation Script:** `experiments/simulations_repair_era/docas/sim_quantum_molecular_expectation.py`
*   **Formal SMT Proofs:** `formal-verification/z3_quantum_molecular_isomorphism.py` (Theorems Q-1–Q-4)
*   **Output Files:** `sim_at3_results.json`, `fig_at3_quantum_molecular_expectation.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Tasks 14 & 16.
