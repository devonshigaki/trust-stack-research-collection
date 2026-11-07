# PRE-REGISTRATION — Sim K-Series: Genealogical Coalescence, Kingman Intensity & Heritability Calibration

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §3 / DOCAS §4.1 / GTT §2.2  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Kingman (1982) Coalescent; Falconer's formula for twin heritability $h^2 = 2(r_{\text{MZ}} - r_{\text{DZ}})$; DOCAS §4.1 empirical twin literature target $h^2 \approx 0.32$.

---

## 1. Domain Hypotheses & Theoretical Motivation

In the production simulator (Layer 2: Genealogy), the UI exposes "Kingman Intensity" ($\kappa \in [0.1, 2.0]$) and "Lineage Depth", implying an empirical relationship to population trust dynamics. In DOCAS §4.1, we cite twin studies demonstrating that the heritability of trust behaviors settles at $h^2 \approx 0.32$ (CI: $[0.25, 0.40]$). However, the mathematical connection between the backward-time Kingman coalescent rate $\lambda = \binom{k}{2} \cdot \kappa$ and forward-time phenotypic trust sensitivity ($\lambda_i$) has not been formally simulated or calibrated.

Here, we deploy an integrated forward-time Wright-Fisher agent population with additive genetic inheritance, subject to environmental selection on trust capital ($S_t$), and reconstruct retrospective Kingman coalescent trees across 50 generations to calibrate the Kingman intensity slider.

---

### Hypothesis K1: Heritability Calibration to Empirical Twin Benchmark
Across a sweep of Kingman intensity $\kappa \in [0.1, 2.0]$ ($N = 1,024$ agents, 50 generations, $100$ monozygotic and $100$ dizygotic twin pairs sampled under identical environmental stimuli per Falconer's formula), the emergent heritability $h^2 = 2(r_{\text{MZ}} - r_{\text{DZ}})$ will scale monotonically with intensity, crossing the empirical literature target corridor $h^2 \in [0.28, 0.36]$ at a calibrated default intensity $\kappa^* \in [0.80, 1.20]$.
* **Criterion C1:** Calibrated intensity $\kappa^*$ must fall within $[0.80, 1.20]$ to yield $h^2 \in [0.28, 0.36]$ with $p < 0.001$.

---

### Hypothesis K2: TMRCA Acceleration under Adaptive Trust Selection
Directional selection on trust capital ($W_i = \operatorname{logistic}(S_i)$) accelerates the coalescence rate relative to neutral Kingman drift, reducing the time to the Most Recent Common Ancestor ($T_{\text{MRCA}}$) by at least $35.0\%$ relative to the neutral baseline:
$$\frac{T_{\text{MRCA}}^{\text{selection}}}{T_{\text{MRCA}}^{\text{neutral}}} \le 0.65$$
* **Criterion C2:** $T_{\text{MRCA}}$ ratio $\le 0.65$ ($\ge 35.0\%$ acceleration in lineage coalescence).

---

### Hypothesis K3: Genetic Stratification of Trust Inequality
At the calibrated Kingman intensity $\kappa^*$, additive genetic variance ($\sigma_g^2$) must account for between $25.0\%$ and $45.0\%$ of the population's steady-state Gini coefficient of trust standing ($S_t$), confirming that trust inequality is a polygenic-environmental co-construction.
* **Criterion C3:** Genetic variance contribution $R^2_{\text{genetic}} \in [0.25, 0.45]$.

---

## 2. Experimental Parameters

- Population: $N = 1,024$ agents, $G = 50$ generations.
- Genome: 20 diploid loci with additive phenotypic mapping to $\lambda_i \in [0.1, 0.9]$.
- Mutation rate: $\mu = 0.005$ per locus per generation.
- Environmental stimulus: 50 interaction cycles with stochastic noise $\sigma = 0.15$.
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria (C1, C2, C3) met.
- **FAIL:** Any criterion fails as frozen.
