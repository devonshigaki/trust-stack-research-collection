# SIM AXIOM-SERIES: PRE-REGISTRATION (Version 4.3)
**The Axioms of Trust: From Physical Bonds to Prototype vs. Trace Memory**

**Hypothesis Overview:**
This battery formally tests the hypothesis that physical and social bonds (Trust) precede Memory, and that the expectation-validation loop drives the thermodynamic work required to update the structural state (Memory) of a system. This unifies Lee Cronin's Assembly Theory, Michael Levin's bioelectric syncytia, and Eric Beinhocker's evolutionary economics.

**Sim AXIOM-1: Multiple-Trace Memory vs. Scalar Prototype Underwriting**
*   **Target Mechanism:** Cognitive architectures relying on "Prototypes" (scalar aggregates like FICO scores) suffer from prior rigidity ("stuck priors") under macroeconomic non-stationarity, whereas "Multiple-Trace" architectures (TFP event logs) remain adaptive.
*   **Simulation Design:** Model $N=1,000$ consumers experiencing a transient macroeconomic shock (e.g., inflation/employment spike) at $t=50$ within a 100-epoch window. Compare a Prototype Kalman-filter underwriter vs. a Multiple-Trace similarity-kernel underwriter.
*   **Frozen Criteria:**
    *   **Criterion AX1.A (Prior Rigidity):** Prototype underwriter exhibits a false-positive denial rate $\ge 3.0\times$ higher than the Multiple-Trace underwriter during the post-shock recovery phase.
    *   **Criterion AX1.B (Recovery Lag):** The Multiple-Trace model converges to ground-truth behavioral risk $\ge 50\%$ faster than the Prototype model (Time-to-Recovery ratio $\le 0.50$).

**Sim AXIOM-2: Beinhocker Evolutionary Assembly of Business Designs**
*   **Target Mechanism:** Economic survival under resource shocks requires a semi-permeable membrane (Business Design) that restricts entropy while allowing adaptive trade, mapping directly to cellular gap junctions and TFP's decentralized architecture.
*   **Simulation Design:** Model an ecology of $F=100$ firms competing for capital under resource scarcity. Firms possess variable contract network structures with varying Assembly Indices ($ASI_{\text{firm}}$) and boundary permeabilities ($\gamma_M$).
*   **Frozen Criteria:**
    *   **Criterion AX2.A (Evolutionary Boundary Selection):** Firms with semi-permeable boundaries ($\gamma_M \approx 0.15$) and high assembly indices ($ASI \ge 15$) survive at a rate $\ge 2.5\times$ higher than monolithic, uncompartmentalized firms ($\gamma_M = 1.0$).
    *   **Criterion AX2.B (Thermodynamic Buffer):** Semi-permeable decentralized firms retain strictly greater capital reserves during acute shocks ($\Delta \text{Reserves} > 0$ relative to monolithic baseline).

**Data Artifacts to Generate:**
*   `sim_axiom_results.json`
*   `fig_sim_axiom_trace_vs_proto.png`
*   `fig_sim_axiom_beinhocker.png`