# PRE-REGISTRATION — Sim G26: Kant vs. Machiavelli in Individualist vs. Collectivist Topologies

**Date:** 2026-10-30 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** GTT §7 ($S_{\text{civ}}$ De-quarantining) / DOCAS §2.9 / Master Stability Law  
**Random Seed:** 42 everywhere  

**Theoretical Anchors:**  
- Kant, I. (1785). *Groundwork of the Metaphysics of Morals*. (Categorical Imperative: universal honesty prior).  
- Machiavelli, N. (1532). *The Prince*. (Instrumental defection: strategic exploitation prior).  
- Hofstede, G. (2011). "Dimensionalizing Cultures: The Hofstede Model in Context." (Individualism vs. Collectivism).  
- Watts, D. J., & Strogatz, S. H. (1998). "Collective dynamics of 'small-world' networks." *Nature*, 393(6684), 440–442.

---

## 1. Domain Hypotheses & Theoretical Motivation

In GTT §7, civilizational trust aggregation ($S_{\text{civ}}$) was placed under quarantine as `[SPECULATION]` due to the absence of a formal model uniting individual philosophical priors with societal network topologies. 

Sim G26 de-quarantines this section by parameterizing:
1. **Philosophical Priors (Agent Level):**
   - **Kantian Agents:** Deontological prior. High unconditional baseline expectation ($E_0 = 0.85$), symmetric updates ($\lambda^+ = \lambda^- = 0.20$), zero instrumental defection.
   - **Machiavellian Agents:** Strategic prior. Low baseline expectation ($E_0 = 0.20$), asymmetric updates ($\lambda^- = 4\lambda^+$), opportunistic defection whenever opponent perceived trust is high.
2. **Cultural Topologies (Societal Level):**
   - **Collectivist Culture:** High-clustering, lattice-coupled small-world network with high gap-junctional stress-sharing ($\gamma_O = 0.50$).
   - **Individualist Culture:** Low-clustering, scale-free Barabási–Albert network with isolated nodes ($\gamma_O = 0.0$).

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

- **C1 (Collectivist Shielding of Kantian Honesty):** Inside dense Collectivist networks, Kantian honest agents achieve a steady-state survival rate $\ge 85.0\%$ despite $30.0\%$ Machiavellian predator density, as high local clustering and stress diffusion isolate defectors.
- **C2 (Individualist Vulnerability to Machiavellian Extinction):** In sparse Individualist scale-free networks, Kantian agents suffer catastrophic extinction (survival $\le 20.0\%$) under the same $30.0\%$ Machiavellian predator density.
- **C3 (Societal Trust Bifurcation ($S_{\text{civ}}$)):** Civilizational trust $S_{\text{civ}} = \frac{1}{N}\sum S_i$ exhibits a sharp topological phase transition: $S_{\text{civ}}(\text{Collectivist}) - S_{\text{civ}}(\text{Individualist}) \ge 0.450$ under identical philosophical agent compositions.
- **C4 (Permutation Topology Null):** Randomizing network edges while preserving degree distribution abolishes the collectivist survival advantage ($p_{\text{perm}} \le 0.001$ under $B = 2,000$ permutations).

**Compound Verdict Rule:** PASS requires all four criteria (C1, C2, C3, C4) satisfied simultaneously. Any failure is reported as frozen without adjustment.
