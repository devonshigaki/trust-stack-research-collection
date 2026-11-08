# PRE-REGISTRATION: SIMULATION PERSUADE-1
**The Lindquist-Watson Agential Convergence: Distributed Mutual Persuasion Across Neural & Visceral Scales**  
**Document ID:** `SIM_PERSUADE1_PRE_REGISTRATION.md`  
**Registration Date:** November 2026 (Version 4.3)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — multi-agent dynamical systems & affective allostasis]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Conceptual Convergence
To resolve the classical Cartesian mind-body bottleneck by formalizing the mathematical convergence between:
1. **Kristen Lindquist's Affective Neuroscience:** The brain does not dictate deterministic top-down commands to a passive body; it operates as an **allostatic prediction engine** balancing metabolic resource budgets via visceromotor predictions and interoceptive prediction errors, constructing conscious emotion from Core Affect.
2. **Richard A. Watson's Complex Evolutionary Systems:** Higher-level entities cannot dictate orders to lower-level sub-components once those sub-components possess local agency; control transitions into **continuous, bidirectional mutual persuasion and reciprocal constraint satisfaction**.

---

## 2. Mathematical Formalization of the Interoceptive-Agential Loop
The organism is formalized as a coupled two-tier dynamical system:
*   **Predictive Controller (Brain):** Generates visceromotor predictions $\boldsymbol{\mu}_t \in \mathbb{R}^k$ (dopaminergic expectation $D$, allostatic setpoints) minimizing predictive free energy $F(\boldsymbol{\mu})$.
*   **Physiological Plant (Body):** Visceral sub-agents $\mathbf{y}_t \in \mathbb{R}^k$ (cardiovascular HRV, interstitial glucose flux, nocturnal temperature) minimizing metabolic expenditure $E(\mathbf{y})$.

The interaction is governed by the **Bilateral Persuasion Coupled ODE**:
$$\frac{d\boldsymbol{\mu}}{dt} = -\nabla_{\boldsymbol{\mu}} F(\boldsymbol{\mu}) + \mathbf{K}_{\mathrm{up}} (\mathbf{y} - \boldsymbol{\mu})$$
$$\frac{d\mathbf{y}}{dt} = -\nabla_{\mathbf{y}} E(\mathbf{y}) + \mathbf{K}_{\mathrm{down}} (\boldsymbol{\mu} - \mathbf{y})$$

Where $\mathbf{K}_{\mathrm{down}}$ represents visceromotor top-down persuasion (allostatic guidance), and $\mathbf{K}_{\mathrm{up}}$ represents interoceptive bottom-up constraint (somatic reality grounding).

---

## 3. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (The Dictatorial Collapse):** Top-down unconstrained command ($\mathbf{K}_{\mathrm{up}} = 0$) results in allostatic exhaustion: under environmental volatility, the mismatch between neural command and bodily capacity causes a $\ge 300\%$ increase in cumulative somatic stress ($p < 10^{-6}$).
*   **Hypothesis H2 (The Reflexive Chaos):** Bottom-up reflex without prediction ($\mathbf{K}_{\mathrm{down}} = 0$) causes myopic instability: metabolic energy dissipation increases by $\ge 200\%$, precluding long-term goal-directed agency.
*   **Hypothesis H3 (The Persuasive Quasicritical Poise):** Balanced bidirectional mutual persuasion ($\mathbf{K}_{\mathrm{up}} \approx \mathbf{K}_{\mathrm{down}} > 0$) minimizes joint free energy ($\Delta F \le -35\%$), establishes the quasicritical attractor ($\rho \approx 0.98$), and constructs stable Core Affect.

---

## 4. Frozen Verification Criteria
*   **Criterion C1 (Allostatic Overload Ratio):**
    Cumulative somatic stress under dictatorial control vs. mutual persuasion must satisfy:
    $$\frac{\text{Stress}(\mathbf{K}_{\mathrm{up}} = 0)}{\text{Stress}(\mathbf{K}_{\mathrm{mutual}})} \ge 3.00\times$$
*   **Criterion C2 (Energetic Dissipation Ratio):**
    Metabolic dissipation under reflexive control vs. mutual persuasion must satisfy:
    $$\frac{\text{Dissipation}(\mathbf{K}_{\mathrm{down}} = 0)}{\text{Dissipation}(\mathbf{K}_{\mathrm{mutual}})} \ge 2.00\times$$
*   **Criterion C3 (Joint Free Energy Minimization):**
    Mutual persuasion must achieve relative free energy reduction:
    $$\Delta F_{\mathrm{joint}} \le -20.0\% \quad (p < 10^{-12})$$

---

## 5. Execution Artifacts
*   **Script:** `experiments/simulations_repair_era/agency/sim_persuade1_mutual_persuasion.py`
*   **Output Files:** `sim_persuade1_results.json`, `fig_persuade1_lindquist_watson.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 29.
