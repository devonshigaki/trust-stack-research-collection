# PRE-REGISTRATION — Sim ECOL: Ecological Carrying Capacity, Metabolic Phase Space, and Scale-Free Clustering

**Date:** 2026-10-30 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS / GTT / Complex Systems  
**Random Seed:** 42 everywhere  

**Theoretical Anchors:**  
- Epstein, J. M., & Axtell, R. (1996). *Growing Artificial Societies: Social Science from the Bottom Up*. (Sugarscape resource mechanics).  
- Bak, P., Tang, C., & Wiesenfeld, K. (1987). "Self-organized criticality: An explanation of the 1/f noise." *Physical Review Letters*, 59(4), 381–384.  
- Saltelli, A., et al. (2010). "Variance based sensitivity analysis of model output." *Computer Physics Communications*, 181(2), 259-270.

---

## 1. Domain Hypotheses & Theoretical Motivation

Simulators frequently rely on ad-hoc heuristics for background environmental scaffolding (resource regeneration, movement costs, reproduction thresholds, and stochastic weather). Without rigorous phase-space mapping, these parameters risk driving the simulation into unplannable chaotic regimes (Malthusian boom-bust cycles) or artificial rigidity.

We hypothesize that if the simulation's metabolic engine and spatial resource clustering are biologically grounded, the macroscopic population will exhibit universal hallmarks of self-organized criticality (SOC) without explicit top-down programming. Specifically, social groups forming via spatial proximity will self-organize into a scale-free (power-law) distribution, and the population's temporal fluctuations will exhibit $1/f$ (pink) noise. Furthermore, a Global Sensitivity Analysis (Sobol indices) must prove that metabolic thermodynamics (energy costs) dominate the system's variance, rather than stochastic weather noise.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

- **C1 (Malthusian Bifurcation Boundary):** Across a Quasi-Monte Carlo sweep of the parameter space, regimes with extreme metabolic cost-to-resource ratios will trigger deterministic population collapse ($N_{\text{final}} \le 0.05 N_{\text{initial}}$ in $\ge 90\%$ of extreme trials), while balanced regimes will stabilize at a homeostatic carrying capacity.
- **C2 (Global Sobol Sensitivity):** The total-order Sobol sensitivity index ($S_T$) for Metabolic Cost (Energy + Movement) must strictly dominate the variance of the carrying capacity ($S_T \ge 0.50$), while Stochastic Base Weather must act as a secondary perturbation ($S_T \le 0.15$).
- **C3 (Scale-Free Social Clustering):** In the homeostatic regime, the distribution of emergent social group sizes (clustered by spatial proximity) must follow a power-law distribution ($R^2 \ge 0.90$ on a log-log regression).
- **C4 (1/f Pink Noise Signature):** The Power Spectral Density (PSD) of the population time-series in the homeostatic regime must exhibit $1/f^\alpha$ scaling with $\alpha \in [0.5, 1.5]$ (pink noise), proving the system avoids artificial white noise and strictly periodic oscillation.

**Compound Verdict Rule:** PASS requires all four criteria (C1, C2, C3, C4) satisfied simultaneously. Any failure is reported as frozen without adjustment.
