# PRE-REGISTRATION — Sim S-Series: Semantic Drift, Linguistic Conventions & Betrayal Entropy Spikes

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §4.5 / DOCAS §4.6 / GTT §3.4  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Lewis (1969) Conventions; CLICS 4.0 cross-linguistic colexification; `crates/sim-core/src/language_drift.rs` empirical predictions (LING-C1, LING-C2, LING-C4).

---

## 1. Domain Hypotheses & Theoretical Motivation

In the production simulator (Layer 6: Philosophy), the UI exposes a "Semantic Drift Rate" slider ($0.0\text{--}10.0$) and a "Coherence Threshold" slider ($0.70$), backed by `crates/sim-core/src/language_drift.rs`. In DOCAS §4.5 and §4.6, we established that linguistic conventions are shared expectation streams across the D–O–C–A–S semantic manifold, predicting that low trust accelerates semantic drift and that trust betrayal triggers an acute entropy spike in concept embeddings.

Here, we deploy an $N = 256$ agent population communicating across an 8D concept embedding space ($\mathbb{R}^8$, initialized from CLICS colexification manifolds) to test the three core linguistic predictions.

---

### Hypothesis S1: Inverse Trust Drift Law (LING-C1)
Semantic drift rate $v_{\text{drift}} = \frac{1}{\Delta t} \|\vec{c}_{i,t} - \vec{c}_{i,t-\Delta t}\|$ across the lexicon is inversely correlated with an agent's trust standing $\tau_i$:
$$r\left( v_{\text{drift}}, \frac{1}{\tau} \right) \ge 0.65, \quad p < 0.001$$
* **Criterion S1:** Pearson correlation $r \ge 0.65$ with $p < 0.001$.

---

### Hypothesis S2: Trust Betrayal Semantic Entropy Spike (LING-C2)
A catastrophic trust betrayal event ($\varepsilon_t < -\theta_C$, severe expectation mismatch) induces an immediate destabilization of the agent's semantic lexicon, triggering an entropy spike with effect size:
$$\text{Cohen's } d \ge 0.80$$
* **Criterion S2:** Pre- vs post-betrayal concept entropy shift exceeds Cohen's $d = 0.80$.

---

### Hypothesis S3: Lexical Turnover & Disconnection under Low Trust (LING-C4)
In populations where mean trust drops below the critical fragmentation threshold $\bar{\tau} < 0.35$, semantic coherence collapses, increasing lexical turnover by at least $2.0\times$ relative to high-trust populations ($\bar{\tau} \ge 0.70$):
$$\frac{\text{Turnover}_{\text{low}}}{\text{Turnover}_{\text{high}}} \ge 2.0$$
* **Criterion S3:** Turnover ratio $\ge 2.0\times$.

---

## 2. Experimental Parameters

- Population: $N = 256$ communicating agents.
- Embedding space: 8 dimensions per concept, 16 core concepts (DOCAS D-O-C-A-S lexicon).
- Drift window: $100$ ticks.
- Betrayal severity: $\Delta \varepsilon = -0.75$.
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria (S1, S2, S3) met.
- **FAIL:** Any criterion fails as frozen.
