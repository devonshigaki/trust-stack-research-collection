# PRE-REGISTRATION — Sim CRIT-Series: Neural Criticality, Branching Parameters & Dynamic Range

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §4.4 / GTT §3.1  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Beggs & Plenz (2003) Neuronal avalanches; Kinouchi & Copelli (2006) Optimal dynamic range at criticality; Touboul & Destexhe (2010, 2017) Non-critical power-law alternatives.

---

## 1. Domain Hypotheses & Theoretical Motivation

In the production simulator (Layer 4: Neurobiology), the UI exposes a "Neural Criticality" toggle (`mech-criticality`). In DOCAS §4.4, we explicitly framed the criticality hypothesis inside its active methodological controversy: while Beggs & Plenz (2003) claim cortical networks self-organize to a critical branching parameter $\sigma = 1.0$ to maximize dynamic range, Destexhe & Touboul (2021) demonstrated that apparent power-law avalanche statistics can arise from neutral subcritical filtering.

Here, we evaluate how the branching parameter $\sigma \in [0.6, 1.4]$ alters avalanche size scaling, sensory dynamic range, and Master Stability Law information transmission across a 1,024-node recurrent network.

---

### Hypothesis CRIT-1: Dynamic Range Maximization
The network's dynamic range $\Delta = 10 \log_{10}(S_{90} / S_{10})$ (dB) of responsiveness to input stimulus intensity will peak within the critical corridor $\sigma^* \in [0.95, 1.05]$, exceeding subcritical ($\sigma = 0.7$) and supercritical ($\sigma = 1.3$) networks by at least $15.0\text{ dB}$:
$$\Delta(\sigma^*) - \max(\Delta_{0.7}, \Delta_{1.3}) \ge 15.0\text{ dB}$$
* **Criterion CRIT-1:** Dynamic range peak within $[0.95, 1.05]$ with $\ge 15.0\text{ dB}$ excess.

---

### Hypothesis CRIT-2: Avalanche Size Power-Law Scaling
At the critical branching parameter $\sigma \approx 1.0$, avalanche size distributions follow a power law $P(S) \propto S^{-\alpha}$ with scaling exponent $\alpha \in [1.40, 1.60]$ ($R^2 \ge 0.95$ over two decades), matching the canonical theoretical exponent $\alpha = 3/2 = 1.50$.
* **Criterion CRIT-2:** Exponent $\alpha \in [1.40, 1.60]$ with $R^2 \ge 0.95$.

---

### Hypothesis CRIT-3: Bounded Information Transmission Collapse
Both subcritical quiescence ($\sigma = 0.7$) and supercritical runaway activity ($\sigma = 1.3$) suppress the Master Stability Law's mutual information transmission rate $I(V_t; E_t)$ by at least $35.0\%$ relative to the critical operating point:
$$\frac{I(\sigma_{\text{sub/super}})}{I(\sigma^*)} \le 0.65$$
* **Criterion CRIT-3:** Information ratio $\le 0.65$ ($\ge 35.0\%$ drop off-criticality).

---

## 2. Experimental Parameters

- Network: $N = 1,024$ leaky integrate-and-fire nodes with sparse random connectivity ($p = 0.05$).
- Branching parameter sweep: $\sigma \in [0.60, 0.70, 0.80, 0.90, 0.95, 1.00, 1.05, 1.10, 1.20, 1.30, 1.40]$.
- Avalanche binning: $\Delta t = 4\text{ ms}$, $10{,}000$ timesteps per condition.
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria met.
- **FAIL:** Any criterion fails as frozen.
