# PRE-REGISTRATION — Sim D18: Unconscious Narrative Processing, Cortisol Suppression, and Waking Attractor Drift

**Date:** 2026-10-15 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §4 (Consciousness Mode Gating) / GTT §3 (Reconciled Attractor Drift) / FreshCredit Whitepaper §3.4 (Nocturnal Exploitation)  
**Random Seed:** 42 everywhere

---

## 1. Domain Hypotheses & Theoretical Motivation

Drawing upon the Baylor College of Medicine studies on narrative and syntactic processing during propofol anesthesia and unconscious states, this simulation investigates the boundary between conscious executive evaluation ($M=1$) and passive unconscious schema ingestion ($M=0$).

1. **Claim A (Cortisol Suppression Threshold & Executive Bypassing):**  
   In conscious mode ($M=1$), incoming financial narratives must pass an executive threat-monitoring gate $E(t)$ modulated by Cortisol ($C$). When $C < C_{\text{crit}} \approx 0.12$ (anesthesia or deep sleep), the executive gate deactivates ($E(t) = 0$), collapsing loss aversion ($\lambda^- \to 0$) and eliminating cognitive friction.
2. **Claim B (Dopamine Decoupling in Syntax Preservation):**  
   High-order syntactic schema and narrative structure formation do not require active phasic dopamine reward signaling ($D_t = 0$). The hippocampal narrative intake array maintains grammatical structure through background priors (analogous to Brain-IT Branch A structural layout invariance).
3. **Claim C (Oxytocin / Serotonin Implicit Tagging & Waking Attractor Drift):**  
   Unconscious inputs ($M=0$) tagged with relational safety ($O$) and stability ($S$) bypass conscious scrutiny and shift the baseline trust attractor:
   $$\Delta S_{\text{base}} = \eta_O O_t + \eta_S S_t$$
   Upon waking reactivation ($M: 0 \to 1$), the agent evaluates new contracts starting from this modified baseline, inducing an unconscious acceptance bias even on predatory agreements.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

All criteria are frozen before executing the simulation script.

* **Criterion C1 (Cortisol Gate Bypassing & Friction Reduction):**  
  In unconscious mode ($M=0$, $C < C_{\text{crit}}$), narrative processing friction (cognitive resistance / loss aversion weighting) must decrease by at least $75\%$ ($\ge 0.75$ friction reduction) compared to conscious baseline ($M=1$).
* **Criterion C2 (Dopamine-Decoupled Structural Schema Preservation):**  
  Under total dopaminergic silencing ($D_t = 0$), sequence prediction entropy / structural perplexity on narrative streams must remain within $5\%$ of the active-reward baseline ($D_t > 0$):
  $$\frac{|\text{Perplexity}_{D=0} - \text{Perplexity}_{D>0}|}{\text{Perplexity}_{D>0}} \le 0.05$$
* **Criterion C3 (Waking Attractor Exploitation Bias):**  
  Agents exposed to $O/S$-tagged narratives during unconscious mode ($M=0$) will exhibit at least a $25\%$ increase in predatory contract acceptance upon waking ($M: 0 \to 1$) relative to unexposed controls:
  $$\Delta\text{Uptake}_{\text{waking}} \ge 0.25$$
* **Criterion C4 (Permutation Significance):**  
  Shuffling narrative presentation across sleep/wake state timestamps must abolish the waking acceptance bias ($p \le 0.001$ under 2,000 permutations).

**Compound Verdict Rule:**  
- **PASS:** All 4 criteria (C1–C4) met.  
- **FAIL:** Any criterion fails as frozen. All results reported openly without post-hoc goalpost adjustment.
