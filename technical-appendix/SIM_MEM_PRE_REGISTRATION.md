# PRE-REGISTRATION — Sim MEM: The Membrane as the Universal Physical Locus of Memory and Selection

**Date:** 2026-11-01  
**Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)

## 1. Theoretical Motivation: Memory Requires a Boundary

In physics, biology, and computational architectures, memory is frequently treated as an abstract internal state. This simulation formalizes a physical inversion: **memory does not float in empty space; it is the physical state change of a semi-permeable boundary.**

Without a membrane, an agent has no "inside" to store a state and no "outside" to validate against; it is an undifferentiated thermodynamic soup. An impenetrable wall prevents external noise but causes informational and metabolic starvation. Therefore, selection and memory formation can only occur at a semi-permeable interface. This principle is scale-invariant:
1.  **Molecules:** The Coulomb electrostatic potential barrier and Pauli exclusion principle form the van der Waals boundary, enabling covalent bonds (Assembly Theory / Sim AT).
2.  **Cells:** The lipid bilayer acts as an electrical capacitor, storing morphogenetic memory via resting potentials (Bioelectrics / Sim B).
3.  **Neurons:** Synaptic Long-Term Potentiation (LTP) is the physical insertion of AMPA/NMDA receptors into the cell membrane (DOCAS).
4.  **Hardware:** Memristors (memory resistors) store data by altering the physical resistance of a thin-film membrane.
5.  **Protocols:** The Fresh Protocol (TFP) constructs a digital cellular wall (database-per-tenant edge vaults), storing verified historical state at the cryptographic boundary.

## 2. Simulation Architecture (Sim MEM)

We model $N = 1,000$ agents maintaining an internal memory state ($S_t$) over $T = 5,000$ timesteps under ambient environmental noise ($\sigma_{\text{env}} = 2.0$). 
The Master Stability Law updates state via boundary interactions: $\Delta S_t = \lambda(V_t - E_t)$.

**Three Regimes Tested:**
1.  **No Membrane (Thermodynamic Soup):** $\gamma = 1.0$. The agent's internal state is fully exposed to environmental thermal noise.
2.  **Impenetrable Wall (Starvation):** $\gamma = 0.0$. Total isolation; no noise enters, but no validation signals can be sampled.
3.  **Semi-Permeable Membrane (Memory Interface):** $\gamma = 0.15$. The boundary filters ambient noise while actively sampling validation signals to update memory via the GTT operator.

## 3. Frozen Empirical Criteria

1.  **Criterion MEM-1 (The Necessity of Isolation for Memory):** Without a membrane, internal state variance must explode, destroying temporal autocorrelation (amnesia). The semi-permeable membrane must constrain internal variance $\text{Var}(S) \le 0.5$ while maintaining a positive temporal autocorrelation ($r_{\text{lag-1}} \ge 0.90$).
2.  **Criterion MEM-2 (The Impenetrable Starvation Trap):** Total isolation ($\gamma=0.0$) must result in zero accumulation of verified trust/memory, such that the terminal state variance is exactly zero ($\text{Var}(S) \approx 0.0$) and total absolute update magnitude is negligible.
3.  **Criterion MEM-3 (The Boundary Locus of Selection):** For the semi-permeable agent, the terminal internal memory state $S_{T}$ must be mathematically identical ($r = 1.000$) to the cumulative integral of boundary-gated prediction errors $\sum (\lambda \cdot \gamma \cdot \varepsilon_t)$, proving the membrane is the exclusive locus of selection.

## 4. Execution Plan
- **File:** `technical-appendix/sim-code/sim_mem_membrane_memory.py`
- **Output:** `technical-appendix/numbers/sim_mem_results.json` and `papers/source/figures/fig_sim_mem_membrane.png`.
- **Verdict:** A **COMPOUND PASS (3/3)** is required to formally integrate the Membrane Memory theorem across the DOCAS, GTT, TFP, and philosophical preface manuscripts.
