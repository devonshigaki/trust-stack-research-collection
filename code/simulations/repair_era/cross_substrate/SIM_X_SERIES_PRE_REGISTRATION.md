# PRE-REGISTRATION — Sim X-Series: Cross-Substrate Dynamical Invariance (Cell → Fly → Mouse → Human)

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** GTT §3.1 / DOCAS §5.7 / TAME Framework  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Substrate Independence & Multiple Realizability; Maximal Lyapunov Exponent Invariance; Buckingham $\Pi$ Scaling.

---

## 1. Domain Hypotheses & Theoretical Motivation

A core claim of the Trust Stack is that the Master Stability Law ($\Delta S_t = \lambda(V_t - E_t)$) is **substrate-independent**: it governs collective coordination across all phylogenetic layers—from non-neural cells and insect connectomes to mammalian cortex and human social institutions—even though the underlying physical carriers vary radically (voltage gradients, synaptic vesicles, neuromodulators, cryptographic credentials).

Here, we simulate all four phylogenetic substrates under the exact same Master Stability Law to evaluate whether dynamical stability invariants recur across scales.

---

### Hypothesis X1: Universal Lyapunov Contraction
Across all four substrates (Layer 1: Cell bioelectrics; Layer 2: Fly FlyWire MBON; Layer 3: Mouse MICrONS; Layer 4: Human H01 / semantics), the leading Lyapunov exponent $\lambda_{\text{Lyap}}$ is strictly negative and falls within the contraction corridor:
$$\lambda_{\text{Lyap}} \in [-1.10, -0.90]$$
confirming transverse phase-volume contraction at rate $\mu = 1.0$.
* **Criterion X1:** $\lambda_{\text{Lyap}} \in [-1.10, -0.90]$ across all 4 substrates.

---

### Hypothesis X2: Permutation Throughput Recurrence
Under randomized partner permutation of network connections, all four substrates exhibit dynamical throughput retention $R_{\text{perm}} \ge 0.50$, proving that dynamical stability does not depend on any specific anatomical wiring diagram.
* **Criterion X2:** $R_{\text{perm}} \ge 0.50$ across all 4 substrates.

---

### Hypothesis X3: Dimensionless Trust Scaling Invariance
The dimensionless scaling ratio $\Pi_{\text{Trust}} = \frac{t_{\text{act}}}{t_{\text{ret}}} \cdot \frac{\lambda^-}{\lambda^+}$ collapses all four substrates onto a single master operating curve, spanning 9 orders of magnitude from ion channels ($10^{-1}\text{ s}$) to human credit histories ($10^8\text{ s}$).
* **Criterion X3:** Master curve goodness-of-fit $R^2 \ge 0.95$.

---

## 2. Experimental Parameters

- Substrates:
  1. Cell: 1,024-node bioelectric lattice ($\gamma_O = 0.50$).
  2. Fly: 1,024-node Kenyon-MBON convergent network (FlyWire ratio 98.2%).
  3. Mouse: 1,024-node MICrONS distributed network (dominant class 31.3%).
  4. Human: 1,024-node H01 / semantic graph (mean input budget 3.2).
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria met.
- **FAIL:** Any criterion fails as frozen.
