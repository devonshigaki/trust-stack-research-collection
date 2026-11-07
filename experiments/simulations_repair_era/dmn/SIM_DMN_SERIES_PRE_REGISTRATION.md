# PRE-REGISTRATION — Sim DMN-Series: Default Mode Network Analog & Bounded Counterfactual Rollouts

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §6.2 / GTT §1.2b / `crates/sim-core/src/dmn.rs`  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Buckner et al. (2008) DMN counterfactual simulation; Simon (1955) Bounded Rationality; Sim D16 Perceptual Cloaking vulnerability.

---

## 1. Domain Hypotheses & Theoretical Motivation

In the production simulator (Layer 5: Psychology), the UI exposes a Default Mode Network toggle (`mech-dmn`), backed by `crates/sim-core/src/dmn.rs`. The code models the DMN as a bounded counterfactual rollout planner: before taking a physical action, an agent simulates $K$ steps into the future, evaluating expected outcome validation ($V_{t+k}$) against priors ($E_{t+k}$). 

Here, we systematically evaluate how counterfactual rollout depth $K \in [1, 10]$ alters an agent's vulnerability to predatory deception (Sim D16) and long-horizon trust accumulation across 1,000 simulated interactions.

---

### Hypothesis DMN-1: Deception Resistance under Perceptual Cloaking
Increasing counterfactual planning depth from $K = 1$ (myopic impulse) to $K = 5$ (deliberative simulation) will suppress predatory contract uptake under Sim D16 visual cloaking ($\chi = 3.65$) by at least $40.0\%$:
$$\frac{\text{Uptake}(K=5)}{\text{Uptake}(K=1)} \le 0.60$$
* **Criterion DMN-1:** Uptake ratio $\le 0.60$ ($\ge 40.0\%$ suppression).

---

### Hypothesis DMN-2: Steady-State Trust Standing Advantage
In an adversarial environment containing $20\%$ predatory defectors, agents with counterfactual planning depth $K = 5$ will maintain a steady-state trust standing ($S_t$) at least $30.0\%$ higher than myopic agents ($K = 1$):
$$\frac{S_{\text{final}}(K=5)}{S_{\text{final}}(K=1)} \ge 1.30$$
* **Criterion DMN-2:** Standing ratio $\ge 1.30$.

---

### Hypothesis DMN-3: Cognitive Energy Diminishing Returns
Increasing planning depth beyond $K = 7$ yields diminishing marginal benefit: the marginal reduction in exploitation loss between $K = 7$ and $K = 10$ is strictly less than $5.0\%$, demonstrating that bounded cognitive constraints naturally truncate human counterfactual depth:
$$\Delta \text{Loss}(K=7 \to 10) < 0.05$$
* **Criterion DMN-3:** Marginal reduction $< 0.05$.

---

## 2. Experimental Parameters

- Population: $N = 1,000$ agents.
- Planning depth sweep: $K \in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]$.
- Adversarial defectors: $20\%$ predatory offer prevalence.
- Master Law presets: $\lambda^+ = 0.005, \lambda^- = 0.020, \delta_S = 0.01$.
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria met.
- **FAIL:** Any criterion fails as frozen.
