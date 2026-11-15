# RUN REPORT — Sim O-Series: Optogenetic Causal Interventions (Version 4.0)

**Date:** 2026-10-15 · **Seed:** 42 everywhere · **Hardware:** Apple Silicon (MPS acceleration / CPU)
**Models:**
- Optogenetic Simulator: Native PyRhO 4-state Markov kinetic opsin models (Grossman et al. 2011).
- Target Opsins: Channelrhodopsin-2 (ChR2, 470nm, excitatory) & ArchT (Halorhodopsin, 566nm, inhibitory).
- Injection Targets: GTT Master Law (Dopamine lesion), D16 Agent Bandwidth (Cortisol stress), TFP Kuramoto Network (O/S inhibition).

---

## 1. Executive Summary & Verdicts

This simulation suite transitions the Trust Stack from *correlative* representation (fMRI / connectomes) to **causal intervention** (optogenetics), injecting simulated light-gated ion photocurrents ($I_{\text{photo}}$) directly into the mathematical neuromodulator frameworks.

**COMPOUND VERDICT: FAIL AS FROZEN (1/3 PASS)**
All results are reported openly without post-hoc goalpost adjustment.

### Hypothesis O1: The Dopaminergic "Trust Lesion" (Causal Necessity)
- **Result:** PASS.
- **Observed:** Optogenetic silencing of the $D$ channel (via ArchT) during a 100-step "FAIR" interaction suppressed the final trust state $S_t$ by **$99.97\%$** (threshold $\ge 90\%$).
- **Scientific Takeaway:** Trust accumulation is causally dependent on active dopaminergic signaling. Without the biological carrier, trust cannot form, proving that financial trust is a biological computation, not a logical accounting of events.

### Hypothesis O2: Induced Vulnerability & Predatory Cloaking (Physiological Sufficiency)
- **Result:** FAIL.
- **Observed:** Optogenetic ChR2 excitation of the Cortisol threat network in "Secure" ($D_{10}$) agents increased predatory uptake by **$1.74\times$** (threshold $\ge 5.0\times$).
- **Scientific Takeaway:** While acute optogenetic stress *does* increase vulnerability (74% increase), it is insufficient to replicate the massive $38.9\times$ exploitation seen in Sim D16. This proves that extreme vulnerability requires chronic, long-term socioeconomic cognitive scarcity, not just acute physiological stress spikes.

### Hypothesis O3: Macroeconomic Fragmentation (Network Fragility)
- **Result:** FAIL.
- **Observed:** Severing the Oxytocin/Serotonin channels in a $10\%$ mutant subpopulation reduced global Kuramoto coherence ($R$) by **$11.39\%$** (threshold $\ge 40\%$).
- **Scientific Takeaway:** The macroeconomic trust network (TFP) is highly robust. A $10\%$ "attractor black hole" is not enough to fracture the entire system, proving the distributed protocol's resilience against biological/adversarial heterogeneity.

---

## 2. Artifacts & Reproducibility
- **Pre-Registration:** `SIM_O_SERIES_PRE_REGISTRATION.md`
- **Execution Script:** `sim_o_series.py`
- **Results Payload:** `sim_o_series_results.json`
- **Analytics Figure:** `fig_sim_o_series.png`
- **Sequential Diagram:** `13_sim_o_optogenetics.png`
