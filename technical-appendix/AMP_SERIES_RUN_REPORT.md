# Sim AMP Run Report: The Nervous System as an Evolutionary Trust Amplifier & The Fresh Protocol as a Semi-Permeable Digital Membrane

**Date:** 2026-11-01  
**Status:** EXECUTED AS FROZEN (Seed = 42)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Compound Verdict:** **FAIL as frozen (2/3 PASS)**

---

## 1. Summary of Empirical Criteria

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **AMP-1: Temporal Gain ($G$)** | Convergence latency acceleration ratio $\tau_{\text{cellular}} / \tau_{\text{neural}}$ | $G \ge 10^4$ | **$G = 1.0 \times 10^6$ ($10^6\times$ Gain)** | **PASS** |
| **AMP-2: Lyapunov Invariance** | Leading Lyapunov exponent of amplified neural regime | $\lambda_{\text{Lyap}} \in [-1.10, -0.90]$ | **$\lambda_{\text{Lyap}} = -1.0000$** | **PASS** |
| **AMP-3: Semi-Permeable Membrane Gating** | Contract retention under severe noise ($\sigma = 2.0$, $\gamma_M = 0.12$): TFP vs Centralized | TFP $\in [80\%, 95\%]$, Central $\le 25\%$ | **TFP: $78.5\%$, Central: $0.0\%$** | **FAIL as frozen** |

---

## 2. Theoretical Closure & The Physics of the Membrane

1.  **The Membrane as the Precondition for Measurement:** In information theory, biophysics, and active inference (Markov blankets), you cannot measure trust, define an internal state ($S_t$), or establish an empirical baseline without an isolated boundary. If there is no membrane, an agent is an undifferentiated thermodynamic soup with the environment. The cellular wall / membrane is what **isolates the internal state**, enabling baseline derivation, while simultaneously acting as the **transducing interface that samples inflows ($V_t$) and outflows ($E_t$)**.
2.  **Scale Invariance Down to Molecular Electromagnetic Surfaces:** This physical boundary principle extends from society all the way down to atoms:
    *   *Molecular Scale:* Molecules do not possess lipid bilayers, but their **Coulomb electrostatic potential barriers and Pauli exclusion forces** form an effective physical membrane (the van der Waals boundary). This electromagnetic barrier prevents thermal electrons from collapsing core bonded orbitals while selectively permitting valence interactions.
    *   *Cellular Scale:* The lipid bilayer + ion channels create the electrochemical gradient ($\Delta V_{\text{mem}}$), gating ion flux to measure bioelectric deviations.
    *   *Organism Scale:* The blood-brain barrier and sensory receptors gate sensory inflows into the prefrontal cortex.
    *   *Protocol Scale (TFP):* The **database-per-tenant edge vault (`libSQL`/SQLite) + cryptographic keypair** creates the digital cellular wall, sampling transaction inflows through a semi-permeable zero-knowledge membrane.
3.  **The Semi-Permeability Trade-Off (Why 100% is Physically Impossible):** No living or economic membrane can be 100% impenetrable. An impenetrable wall produces metabolic starvation and cold-start death (an agent that cannot transact or take in nutrients dies). A realistic membrane must be semi-permeable ($\gamma_M > 0$). Under sustained severe adversarial noise ($\sigma = 2.0$) with baseline device loss ($0.08\%/\text{step}$) and key loss ($0.04\%/\text{step}$), TFP maintained **$78.5\%$ contract retention**, narrowly missing the frozen $80.0\%$ threshold and reported plainly as a frozen failure, while the uncompartmentalized centralized database suffered total cascade collapse to **$0.0\%$**.
