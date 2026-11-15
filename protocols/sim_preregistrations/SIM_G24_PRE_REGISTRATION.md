# PRE-REGISTRATION — Sim G24: Perceptual Genomics, Bioelectric Gap-Junction Epistasis & Reality Threshold Collapse

**Date:** 2026-10-29 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §4.2, §4.4, §5.10, §5.13 / GTT §3 / Sim L-Series / Sim D19  
**Random Seed:** 42 everywhere  
**Theoretical Anchors:**  
- Arnsten, A. F. T. (2009). "Stress signalling pathways that impair prefrontal cortex structure and function." *Nature Reviews Neuroscience*, 10(6), 410–422. [DOI: 10.1038/nrn2648](https://doi.org/10.1038/nrn2648)  
- Wang, M., et al., & Arnsten, A. F. T. (2007). "Alpha2A-adrenoceptors strengthen, while dopamine D1 receptors weaken, network firing through cAMP-HCN channel gating." *Nature*, 448(7150), 203–207.  
- Shreesha, L., & Levin, M. (2024). "Stress sharing as cognitive glue for collective intelligences: A computational model of stress as a coordinator for morphogenesis." *Biochem Biophys Res Commun*, 710, 149868.  
- Cheng, J., et al. (2023). "Accurate proteome-wide missense variant effect prediction with AlphaMissense." *Science*, 381(6664), eadg7492.  
- Dijkstra, N., & Fleming, S. M. (2023). "Subjective signal strength distinguishes reality from imagination." *Nature Communications*, 14, 1627.

---

## 1. Domain Hypotheses & Theoretical Motivation

Historical attempts to locate a single behavioral "trust gene" failed because macro-level social trust is an emergent dynamical property of multi-timescale active inference, not a primary protein product. Consequently, behavioral GWAS for candidate genes (e.g., *OXTR*, *AVPR1A*, *PDE4B*) either yielded nulls or failed independent replication.

However, the **cellular hardware that executes reality monitoring and stress sharing is directly encoded by structural genes.**

### The Biochemical & Biophysical Signalplex
1. **The Intracellular cAMP Brake (*PDE4B*):** Phosphodiesterase 4B hydrolyzes cyclic AMP (cAMP) within dendritic spines of prefrontal cortical Layer III pyramidal neurons. 
2. **The Molecular Shunt (*HCN1* Channels):** Elevated cAMP directly binds to the cyclic nucleotide-binding domain (CNBD) of hyperpolarization-activated cyclic nucleotide-gated (*HCN1*) channels, driving channel opening ($P_{\text{open}}$). Open HCN1 channels leak potassium/sodium ions ($I_h$ shunting), disconnecting pyramidal dendritic spines and silencing the recurrent "mental sketch pad."
3. **The Intercellular Syncytial Buffer (*GJA1* / Connexin 43):** Gap junctions allow direct intercellular diffusion of cAMP across neighboring cells (the DOCAS Oxytocin/Coupling channel $\gamma_O$). In healthy tissue, gap junctions dilute local metabolic stress, preventing runaway cAMP accumulation.
4. **The Perceptual Reality-Monitoring Interface (Sim D19):** Sensory gain $\alpha_i$ and internal observation noise $\sigma_i$ are direct functions of HCN1 channel open probability ($P_{\text{open}}$):
   $$\alpha_i = \alpha_0 \cdot (1 - 0.85 P_{\text{open}}), \quad \sigma_i = \sigma_0 \cdot (1 + 2.5 P_{\text{open}})$$
   When $P_{\text{open}} \to 1$, sensory evidence ($X$) is shunted ($\alpha_i \to 0$), and chaotic internal noise explodes ($\sigma_i \to \infty$).

### Resolution of the Schizophrenia/Paranoia Paradox
This cellular biophysics resolves the directional paradox of Section 4.2:
- **Moderate cAMP ($\nu \approx 1$):** Flexible learning, near-critical updating, intact reality testing ($T_{\text{reality}} = 2.5$).
- **Severe PDE4B Loss ($\nu > 1$):** Runaway cAMP locks HCN1 channels open, disconnecting the prefrontal cortex. The resulting sensory void and supercritical noise flood the reality filter with false positives ($m \gg T_{\text{reality}}$).
- **Compensatory Rigidity:** To prevent total cognitive dissolution, the organism collapses plasticity ($\lambda \to 0$) and locks in rigid, un-updatable top-down paranoid priors ($E$). Thus, severe PDE4B deficiency causes **low trust** through noise-induced compensatory paranoia, rather than high trust through linear updating.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

All four quantitative criteria are strictly frozen prior to simulation execution.

### Hypothesis G24.1: The Inverted-U Reality-Testing Gate
* **Criterion C1:** Reality-monitoring fidelity ($F_{\text{RM}} = 1 - \text{Error Rate}$) must follow an inverted-U profile with respect to PDE4B catalytic rate ($k_{\text{cat}}$). Severe PDE4B catalytic impairment ($k_{\text{cat}} \le 0.30$, AlphaMissense score $\ge 0.80$) must drop reality-monitoring fidelity by at least 40.0 percentage points compared to wild-type ($k_{\text{cat}} = 1.0$):
  $$\Delta F_{\text{RM}} = F_{\text{RM}}(\text{WildType}) - F_{\text{RM}}(\text{Null}_{\text{PDE4B}}) \ge 0.400$$

### Hypothesis G24.2: GJA1 Gap-Junctional Rescue of High-Burden Missense Variants
* **Criterion C2:** In microcircuits carrying deleterious PDE4B missense variants (AlphaMissense score $\ge 0.80$), restoring intact Connexin 43 gap junctions ($G_{\text{GJA1}} \ge 0.50$) must dilute local cAMP into syncytial neighbors, reducing dendritic HCN1 open probability by at least 35.0% relative to isolated cells ($G_{\text{GJA1}} = 0.0$):
  $$\frac{P_{\text{open}}(G_{\text{GJA1}} = 0.50) - P_{\text{open}}(G_{\text{GJA1}} = 0.0)}{P_{\text{open}}(G_{\text{GJA1}} = 0.0)} \le -0.350$$

### Hypothesis G24.3: Double-Hit Epistatic Catastrophe
* **Criterion C3:** Co-occurring high-burden missense variants in both *PDE4B* and *GJA1* (AlphaMissense pathogenicity $\ge 0.70$ on both loci) must produce a multiplicative surge in catastrophic reality-monitoring failure (hallucination rate $P(\text{Hallucination}) > 0.50$) of at least $5.00\times$ compared to single-hit mutants:
  $$\text{Risk Ratio}_{\text{DoubleHit}/\text{SingleHit}} = \frac{P(\text{Fail} \mid \text{DoubleHit})}{P(\text{Fail} \mid \text{SingleHit})} \ge 5.00\times$$

### Hypothesis G24.4: Compensatory Paranoid Rigidity Transition
* **Criterion C4:** Microcircuits in chronic HCN1 shunting states ($P_{\text{open}} \ge 0.75$) undergo an epistemic phase transition: the effective update gain collapses ($\lambda_{\text{eff}} \le 0.05 \lambda_0$). When subjected to 100 consecutive rounds of positive confirming validation ($\varepsilon = +1.0$), terminal steady-state trust remains locked in a low-trust attractor ($S_{100} \le 0.250$) in at least $80.0\%$ of severe-burden agents:
  $$\text{Rigidity Rate} = \mathbb{E}[\mathbb{I}(S_{100} \le 0.250)] \ge 0.800$$

**Compound Verdict Rule:**  
- **PASS:** All four criteria (C1, C2, C3, C4) satisfied simultaneously.  
- **FAIL:** Any criterion fails as frozen. Results will be reported transparently without post-hoc threshold adjustment.

---

## 3. Mathematical Model & Experimental Architecture

### Population & Lattice Parameters:
- Heterogeneous population: $N = 1,000$ microcircuits.
- Cellular syncytium: $10 \times 10 = 100$ coupled pyramidal compartments per microcircuit.
- AlphaMissense pathogenicity distributions:
  - $B_{\text{PDE4B}} \sim \operatorname{Beta}(2, 3)$ (calibrated to Q07343 missense burden).
  - $B_{\text{GJA1}} \sim \operatorname{Beta}(2, 2)$ (calibrated to P17302 missense burden).
  - $B_{\text{HCN1}} \sim \operatorname{Beta}(1.5, 3)$ (calibrated to O60741 pore-domain burden).
- Random seed: 42 everywhere.

### Coupled Biochemical Equations:
1. **cAMP Synthesis and Hydrolysis:**
   $$\frac{d[\text{cAMP}]_i}{dt} = k_{\text{syn}} - k_{\text{cat}}(\text{PDE4B}_i) [\text{cAMP}]_i + D_{\text{GJA1}, i} \sum_{j \in \mathcal{N}(i)} ([\text{cAMP}]_j - [\text{cAMP}]_i) + \xi_{\text{cAMP}}$$
   where $k_{\text{cat}} = k_0 (1 - 0.85 B_{\text{PDE4B}})$ and $D_{\text{GJA1}} = D_0 (1 - 0.90 B_{\text{GJA1}})$.
2. **HCN1 Channel Gating:**
   $$P_{\text{open}, i} = \frac{1}{1 + \exp\left(-\frac{[\text{cAMP}]_i - \theta_{\text{HCN1}}(B_{\text{HCN1}})}{\beta_{\text{HCN1}}}\right)}$$
3. **Perceptual Reality-Monitoring Interface:**
   $$\alpha_i = \alpha_0 (1 - 0.85 P_{\text{open}, i}), \quad \sigma_i = \sigma_0 (1 + 2.5 P_{\text{open}, i})$$
   $$m_i = \alpha_i X + V_i + \epsilon_i, \quad \epsilon_i \sim \mathcal{N}(0, \sigma_i^2)$$
   Decision rule: Conscious perception $\iff m_i > T_{\text{reality}} = 2.5$.
4. **Compensatory Bayesian Updating:**
   $$\lambda_{\text{eff}, i} = \lambda_0 \cdot \exp(-4.5 \cdot P_{\text{open}, i})$$
   $$\Delta S_{t} = \lambda_{\text{eff}, i} (V_t - E_t) - \delta_S (S_t - S_{\text{base}})$$

---

## 4. Expected Deliverables & Artifacts
- Frozen Pre-registration: `technical-appendix/SIM_G24_PRE_REGISTRATION.md`
- Simulation Implementation: `experiments/brainit-fmri/insilico/sim_g24_perceptual_genomics.py`
- Statistical Results: `experiments/brainit-fmri/results/sim_g24_results.json`
- 4-Panel Publication Diagram: `figures/docas/pipeline/fig_sim_g24_perceptual_genomics.png`
- Accounting Audit Trail: Updated `SIMULATION_ACCOUNTING.md` and `VERSIONS.md`
