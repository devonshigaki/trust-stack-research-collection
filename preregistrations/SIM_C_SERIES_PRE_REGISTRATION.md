# PRE-REGISTRATION — Sim C-Series: Choice Architecture, Default Nudges & Asymmetric Loss Framing

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** GTT §1.2b / TFP §3.7 (Sim P7) / DOCAS §2.3  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Thaler & Sunstein (2008) Nudge Architecture; Kahneman & Tversky (1979) Prospect Theory; Johnson & Goldstein (2003) Defaults; TFP $\lambda^- = 4 \lambda^+$ break/build asymmetry.

---

## 1. Domain Hypotheses & Theoretical Motivation

The production simulator exposes a "Choice Architecture" toggle (`mech-choice` in Layer 5: Psychology), backed by `crates/sim-core/src/choice_architecture.rs` (`NudgeConfig`, `FrameType`, `NudgeType`). In GTT §1.2b and TFP §3.7, we established that boundedly rational agents make distorted decisions when deferred costs are non-salient, and that framing differentially engages the Master Stability Law's break/build asymmetry ($\lambda^- > \lambda^+$).

Here, we systematically evaluate how choice architecture parameters (Defaults, Loss vs Gain Framing, and Cognitive Friction) alter agent contract choices and trust updates across 1,000 simulated financial interactions.

---

### Hypothesis C1: Default Nudge Adherence
When a cooperative agreement is presented as the pre-selected default (`DefaultBias`, $+70\%$ weight), agent contract adherence will surge by at least $+25.0\%$ above the neutral $50.0\%$ baseline (reaching $\ge 75.0\%$ adherence, $p < 0.001$).
* **Criterion C1:** Adherence rate $\ge 75.0\%$ under default nudging.

---

### Hypothesis C2: Loss Framing Asymmetry Ratio
Under Loss Framing ("you will lose $X$ standing if you defect"), agent compliance resistance is amplified by at least $3.0\times$ relative to Gain Framing ("you will gain $X$ standing if you cooperate"), confirming that loss framing operationalizes the TFP Master Law's $4.0\times$ break/build asymmetry ($\lambda^- = 0.02$ vs $\lambda^+ = 0.005$):
$$\frac{\text{Compliance}_{\text{loss}}}{\text{Compliance}_{\text{gain}}} \ge 3.0$$
* **Criterion C2:** Compliance ratio $\ge 3.0\times$.

---

### Hypothesis C3: Cognitive Friction Damping
Adding cognitive friction units (delay steps and confirmation barriers) suppresses opt-out transitions by at least $50.0\%$ relative to frictionless choice menus:
$$\frac{\text{OptOut}_{\text{friction}}}{\text{OptOut}_{\text{frictionless}}} \le 0.50$$
* **Criterion C3:** Opt-out ratio $\le 0.50$ ($\ge 50.0\%$ suppression).

---

## 2. Experimental Parameters

- Population: $N = 1,000$ present-biased agents ($\beta \sim U(0.4, 0.9)$, $\delta \sim U(0.95, 0.99)$).
- Master Law presets: $\lambda^+ = 0.005$, $\lambda^- = 0.02$ (4:1 asymmetry).
- Default boost: $+70\%$; Friction penalty: $-20\%$ per unit; Salience boost: $+35\%$.
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria (C1, C2, C3) met.
- **FAIL:** Any criterion fails as frozen.
