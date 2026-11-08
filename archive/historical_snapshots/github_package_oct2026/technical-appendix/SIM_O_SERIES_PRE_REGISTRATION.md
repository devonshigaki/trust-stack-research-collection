# PRE-REGISTRATION — Sim O-Series: Optogenetic Causal Interventions

**Date:** 2026-10-15 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §6 / TFP §5 (Version 4.0 additions)  
**Random Seed:** 42 everywhere

---

## 1. Domain Hypotheses & Theoretical Motivation

To date, the Trust Stack has established functional recurrence (connectome simulations), architectural convergence (Kuramoto synchronization), and in-silico representational fidelity (Brain-IT decoding). However, these measurements are fundamentally *correlative* or *observational*. 

In Version 4.0, we transition to causal interventions using simulated optogenetics (via PyRhO multi-state kinetic models). By simulating light-gated ion channels (e.g., Channelrhodopsin-2 for excitation, ArchT/Halorhodopsin for inhibition) injected directly into the GTT mean-field differential equations and TFP multi-agent frameworks, we can prove causality.

### Hypothesis O1: The Dopaminergic "Trust Lesion" (Causal Necessity)
**Hypothesis:** Trust accumulation is causally dependent on active dopaminergic ($D$) signaling. Optogenetic silencing of the $D$ channel (via simulated yellow light on ArchT) during highly beneficial ("FAIR") financial interactions will completely block positive prediction error updates ($\lambda^+$), inducing a catastrophic decay to baseline despite positive economic stimuli.
**Criterion C1 (Abolition):** In a simulated 100-step "FAIR" interaction, optogenetic inhibition of $D$ must suppress final trust state $S_t$ by $\ge 90\%$ compared to an uninhibited control. 

### Hypothesis O2: Induced Vulnerability & Predatory Cloaking (Physiological Sufficiency)
**Hypothesis:** Predatory visual design targets transient physiological vulnerabilities. Optogenetically exciting the Cortisol ($C$) threat network (via blue light on ChR2) immediately prior to evaluating visually cloaked predatory contracts (Sim D16) will compress cognitive bandwidth, forcing "Secure" ($D_{10}$) agents to exhibit the exploitation rates of "Stressed" ($D_1$) agents.
**Criterion C2 (Vulnerability Induction):** Optogenetic stress induction must increase the uptake of predatory contracts in the top quartile of agents by $\ge 500\%$ (a $5.0\times$ relative risk increase).

### Hypothesis O3: Macroeconomic Fragmentation (Network Fragility)
**Hypothesis:** Global market synchronization (Kuramoto coherence $K_c$ in TFP) is fragile to biological heterogeneity. Continuous optogenetic inhibition of Oxytocin ($O$, validation) and Serotonin ($S$, stability) in a small mutant subpopulation ($10\%$ of agents) will act as an attractor black hole, preventing the remaining $90\%$ of healthy agents from achieving global synchronization.
**Criterion C3 (Synchronization Collapse):** A $10\%$ inhibited subpopulation must reduce the terminal global Kuramoto order parameter $R$ by $\ge 40\%$ compared to a homogeneous healthy network.

---

## 2. Methodology & Software Substrate

- **Optogenetic Simulator:** `PyRhO` (Evans et al., 2016) integrated with `Brian2` or standard NumPy solvers.
- **Opsin Models:** 4-state Markov kinetic models for ChR2 (excitation, 470nm) and ArchT (inhibition, 566nm).
- **Injection:** The generated photocurrents ($I_{\text{photo}}$) will be linearly coupled into the respective neuromodulatory differential equations established in DOCAS Sim D10.

**Compound Verdict Rule:**  
- **PASS:** All 3 criteria (C1–C3) met.  
- **FAIL:** Any criterion fails as frozen. All results reported openly without post-hoc goalpost adjustment.
