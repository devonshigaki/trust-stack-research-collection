# PRE-REGISTRATION: SIMULATION WEARABLE-TRIAD
**Multi-Rate Sensor Fusion of Wearable Biosensors (Muse EEG, Apple Watch PPG, Dexcom Stelo CGM) for Grounding the 5-Channel Trust Vector**  
**Document ID:** `SIM_WEARABLE_TRIAD_PRE_REGISTRATION.md`  
**Date of Registration:** November 2026 (Version 4.3)  
**Author:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Epistemic Label:** `[SIMULATION — multi-rate biosensor telemetry & physiological calibration]`  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## 1. Theoretical Objective & Scope
To formalize and verify the asynchronous multi-rate sensor fusion pipeline that maps non-invasive consumer wearable telemetry onto the 5 DOCAS functional channels:
1. **Muse S Headband (256 Hz EEG):** Captures prefrontal Event-Related Potentials (P300/MMN) and Frontal Alpha Asymmetry (FAA) on prefrontal channels AF7/AF8 (D & A channels).
2. **Apple Watch Ultra 2/Series 10 (PPG):** Captures beat-to-beat inter-beat intervals (rMSSD) and high-frequency vagal parasympathetic power (C & S channels).
3. **Dexcom Stelo (Continuous Glucose Monitor, 5-min intervals):** Captures interstitial glucose flux ($dG/dt$) and metabolic allostatic load driven by glucocorticoid activation (Allosteric cAMP/ATP substrate depletion).

---

## 2. Pre-Registered Hypotheses (Frozen Prior to Execution)
*   **Hypothesis H1 (Temporal Cascade Sequence):** A contractual betrayal event ($\varepsilon_t < 0$) produces a statistically significant, time-staggered physiological cascade across the triad:
    $$\tau_{\text{EEG (Muse)}} \in [200, 500\text{ ms}] \quad < \quad \tau_{\text{PPG (Watch)}} \in [10, 45\text{ s}] \quad < \quad \tau_{\text{CGM (Stelo)}} \in [15, 45\text{ min}]$$
*   **Hypothesis H2 (Multi-Rate Kalman Coherence):** An asynchronous Kalman state-space estimator tracking the latent trust state $S_t$ from the combined multi-rate streams achieves a state recovery correlation $r \ge 0.850$ against synthetic ground truth.
*   **Hypothesis H3 (Sensor Decoupling Specificity):** Synthetic artifact corruption of any single sensor stream degrades overall state recovery by no more than $15.0\%$, demonstrating graceful degradation and sensor redundancy.

---

## 3. Frozen Verification Criteria
*   **Criterion C1 (Cascade Latency Hierarchy):**
    Empirical latencies must strictly satisfy: $\tau_{\text{Muse}} < \tau_{\text{Watch}} < \tau_{\text{Stelo}}$ with $\tau_{\text{Muse}} \le 1.0\text{ s}$ and $\tau_{\text{Watch}} \le 60.0\text{ s}$.
*   **Criterion C2 (Multi-Rate State Recovery):**
    Latent trust state correlation must satisfy: $r(\hat{S}_t, S_t) \ge 0.850$.
*   **Criterion C3 (Single-Sensor Fault Tolerance):**
    Under total simulated drop of the Apple Watch PPG channel, state recovery must maintain: $r_{\text{degraded}} \ge 0.750$.

---

## 4. Execution Artifacts
*   **Script:** `experiments/wearables_pipeline/sim_wearable_triad_sensor_fusion.py`
*   **Output Files:** `sim_wearable_triad_results.json`, `fig_wearable_triad_fusion.png`
*   **Verification Status:** Integrated into `run_tier1_tier2_suite.py` as Task 28.
