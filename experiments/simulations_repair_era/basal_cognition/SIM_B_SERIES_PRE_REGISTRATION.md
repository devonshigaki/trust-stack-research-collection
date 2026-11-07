# PRE-REGISTRATION — Sim B-Series: Basal Cognition, Non-Neural Problem-Solving & Barrier Circumvention

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §5.10 / GTT §2.2 / TAME Framework (Levin 2019, 2022)  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Michael Levin (Basal Cognition without Neurons); *Physarum polycephalum* maze navigation; Gap-junctional stress-leakage steering.

---

## 1. Domain Hypotheses & Theoretical Motivation

A foundational tenet of Michael Levin’s basal cognition paradigm is that **intelligence, goal-directed problem solving, and cooperation do not require a brain, neurons, or synaptic plasticity**. Primitive living tissues—from slime molds to embryonic cell sheets—solve dynamic navigation problems in morphospace and physical space by propagating physiological prediction errors across gap junctions.

Here, we evaluate a collective of $N = 512$ non-neural cells navigating an unfamiliar 2D environment containing an impenetrable transverse barrier (dead end) between start position $\mathbf{X}_0 = (0.15, 0.50)$ and distant target attractor $E^* = (0.85, 0.50)$. We test whether leaky gap-junctional stress sharing ($\gamma_O = 0.60$) allows the brainless collective to detect the obstacle, reorient its motility, and reach the target without any centralized pathfinder.

---

### Hypothesis B1: Non-Neural Barrier Circumvention
When gap-junctional stress sharing is active ($\gamma_O = 0.60$), the collective of cells will circumvent the dead-end barrier and reach the target attractor ($d(\mathbf{X}_t, E^*) \le 0.05$) within $T = 300$ timesteps with success rate $\ge 90.0\%$. Conversely, an uncoupled collective ($\gamma_O = 0.0$, insular cells) will become permanently pinned against the barrier, failing to navigate around the obstacle ($0.0\%$ success).
* **Criterion B1:** Success rate $\ge 90.0\%$ at $\gamma_O = 0.60$ vs $0.0\%$ at $\gamma_O = 0.0$.

---

### Hypothesis B2: Transverse Stress Gradient Steering
Collisions between lead cells and the barrier generate an acute localized prediction error surge ($|\varepsilon| > \theta_C$). Leaking this mismatch backward through gap junctions generates an emergent transverse repelling force $\vec{F}_{\text{steer}} = -\gamma_O \nabla \tilde{\varepsilon}$, rotating collective motility by $\ge 60^\circ$ away from the dead end prior to complete entrapment.
* **Criterion B2:** Mean trajectory deflection angle $\theta_{\text{deflect}} \ge 60.0^\circ$ at the barrier interface.

---

### Hypothesis B3: Non-Neural Trajectory Recall (Basal Memory)
Following successful circumvention, the collective encodes the bypass trajectory in its persistent bioelectric state field ($S_t$). Upon re-exposure to the same obstacle environment (Trial 2), the collective reaches the target in at least $35.0\%$ less time ($t_{\text{trial2}} \le 0.65 \cdot t_{\text{trial1}}$), demonstrating non-neural spatial learning.
* **Criterion B3:** Navigation time ratio $t_{\text{trial2}} / t_{\text{trial1}} \le 0.65$ ($\ge 35.0\%$ recall acceleration).

---

## 2. Experimental Parameters

- Population: $N = 512$ cells, 2D continuous coordinates $\mathbf{x}_i \in [0, 1]^2$.
- Barrier: Vertical wall at $x = 0.50$, extending $y \in [0.25, 0.75]$.
- Start: Gaussian cluster centered at $(0.15, 0.50)$; Target $E^* = (0.85, 0.50)$.
- Master Law presets: $\lambda = 0.61$, $\beta_C = 5.0$, $\theta_C = 0.05$, $\sigma = 0.02$.
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria met.
- **FAIL:** Any criterion fails as frozen.
