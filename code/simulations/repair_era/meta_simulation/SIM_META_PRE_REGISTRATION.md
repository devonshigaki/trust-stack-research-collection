# PRE-REGISTRATION — Sim META: The Universal Trust Vector & Affective Derivative Projection

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** GTT §2.1 / DOCAS §2.9 / Value of Trust (Preface) / TFP §3.2  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** Russell (1980) Circumplex Model; Barrett (2017) Constructed Emotion; Friston (2017) Free Energy Derivatives; GTT Invariant Force Vector.

---

## 1. Domain Hypotheses & Theoretical Motivation

A foundational tenet of the Trust Stack is that **trust is not an emotion, nor is it a psychological construct confined to the human head**. Trust is a universal physical force vector: the continuous, measurable alignment between an agent's expectations ($E$) and environmental validation ($V$). The primary emotions that humans experience—joy, contentment, anger, fear, grief—are not irreducible biological primitives; they are **mathematical derivatives of the trust vector** projected across three dynamic axes:
1. **Valence:** The signed prediction error mismatch $\varepsilon_t = V_t - E_t$ (positive when trust is validated, negative when trust is broken).
2. **Arousal:** Salience gating through Cortisol and Adrenergic mobilization: $r_{C,t} \cdot A_t$.
3. **Dominance / Control:** The temporal rate of mismatch resolution: $\frac{d(\Delta S_t)}{dt}$.

Here, we execute **Sim META**, a multi-scale meta-simulation demonstrating that:
(1) Primary discrete emotion categories are exact mathematical readouts of the 3D trust derivative manifold.
(2) A single perturbation sequence applied to the Master Stability Law simultaneously governs cellular bioelectrics, affective valence, linguistic consensus, and macro credit credibility across scales.

---

### Hypothesis META-1: Affective Derivative Projection
Across $N = 1,000$ expectation-validation events spanning confirmation ($\varepsilon > 0$), mild mismatch ($|\varepsilon| \le \theta_C$), and acute betrayal ($\varepsilon < -\theta_C$), the three mathematical derivatives of the trust vector:
$$\text{Valence} = \varepsilon_t, \quad \text{Arousal} = r_{C,t} \cdot A_t, \quad \text{Dominance} = \operatorname{clip}\left(\frac{\Delta S_t - \Delta S_{t-1}}{\Delta t}, -1, 1\right)$$
classify canonical discrete emotion categories (Joy/Contentment, Fear/Panic, Anger/Aggression, Grief/Depression) with 5-fold cross-validated Macro $F_1 \ge 0.95$ ($p < 0.001$), proving that discrete emotions are derivative projections of trust.
* **Criterion META-1:** Macro $F_1 \ge 0.95$ with $p < 0.001$.

---

### Hypothesis META-2: Cross-Scale Force Vector Coherence
When a standardized sequence of confirmation and betrayal shocks is applied to the Master Stability Law, the resulting state dynamics across all four emergent layers:
1. Layer 1: Cellular bioelectric resting potential ($V_{\text{mem}} \in [-70, -20]\text{ mV}$)
2. Layer 2: Psychological affective valence ($[-1.0, 1.0]$)
3. Layer 3: Semantic concept stability ($[0.0, 1.0]$)
4. Layer 4: Institutional credit standing ($S_t \in [0.0, 1.0]$)
will exhibit pairwise cross-correlation $r_{\text{cross}} \ge 0.85$ ($p < 10^{-15}$), proving that trust acts as an invariant physical force vector across biological, psychological, and institutional scales.
* **Criterion META-2:** Minimum pairwise cross-correlation $\min(r_{\text{cross}}) \ge 0.85$.

---

### Hypothesis META-3: Universal Transverse Contraction
In the absence of external driving shocks, all four layers contract toward their respective steady-state alignment manifolds at the invariant Lyapunov rate $\mu \approx -1.0$ (corridor $[-1.10, -0.90]$).
* **Criterion META-3:** Contraction rate $\lambda_{\text{Lyap}} \in [-1.10, -0.90]$ across all four tiers.

---

## 2. Experimental Parameters

- Population: $N = 1,000$ multi-tier event sequences.
- Emotion categories: Contentment ($\varepsilon > 0$, low arousal), Joy ($\varepsilon > 0$, high arousal), Anger ($\varepsilon < 0$, high arousal, high dominance), Fear ($\varepsilon < 0$, high arousal, low dominance), Grief ($\varepsilon < 0$, low arousal, zero dominance).
- Shock sequence: Alternating confirmation blocks ($T=25$) and betrayal shocks ($T=10$).
- Seed: 42.

---

## 3. Compound Verdict Rule
- **PASS:** All 3 criteria met.
- **FAIL:** Any criterion fails as frozen.
