# PRE-REGISTRATION — Sim M-Series: Temporal Dynamics of Music (TDF), Metric Hierarchies & Auditory State Gating in DOCAS

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §2 / GTT §3 / TFP §5 (Version 4.1 additions)  
**Random Seed:** 42 everywhere  
**Theoretical Anchor:** London (2012, *Hearing in Time: Psychological Aspects of Musical Meter*); Huron (2006, *Sweet Anticipation: Music and the Psychology of Expectation*); General Theory of Trust (GTT) Master Stability Law $\Delta S_t = \lambda(V_t - E_t)$; Kuramoto Phase Synchrony & Rhythmic Entrainment (§3.4); Shreesha & Levin (2024, stress sharing and multiscale behavioral feedback).

---

## 1. Domain Hypotheses & Theoretical Motivation

A pervasive limitation of existing commercial and algorithmic music interfaces (such as legacy Spotify and Apple Music recommendation heuristics) is their reliance on **scalar tempo (BPM)** and static genre taxonomy. In dynamical systems and computational cognitive neuroscience, scalar tempo is severely under-determined: a $3/4$ triple simple meter (e.g., Brahms waltz, $72\text{ BPM}$) and a $6/8$ compound duple meter (e.g., African/Celtic polyrhythmic jig, $72\text{ BPM}$) share identical scalar tempo representations, but elicit fundamentally distinct motor-corticostriatal entrainment patterns, oxytocinergic phase coherence, and autonomic arousal states.

Within the **General Theory of Trust (GTT)** and the **DOCAS Framework**, human cognitive and behavioral states operate as dynamic attractors on the Riemannian manifold $\mathring{\Delta}^4$. We establish a formal mathematical isomorphism between the acoustic/auditory feature space and the five neurochemical channels of DOCAS:
1. **Dopamine ($D$, Forward Drive & Anticipatory Prediction Error):** Mapped to **Phase / Skip Dynamics ($\Delta \phi$)**, measuring user skip, scrub, and pause events relative to musical structural boundaries (downbeats, hypermetric phrases). Skips at non-structural boundaries reflect acute prediction error mismatch ($V_t \neq E_t$).
2. **Oxytocin ($O$, Rhythmic Synchrony & Collective Entrainment):** Mapped to the **Metric Hierarchy Ratio ($\tau$)**, capturing the subdivision architecture:
   - $\tau = 0.0$: Simple triple meter ($3/4$), characterized by asymmetric rotational momentum and introspective stabilization.
   - $\tau = 0.5$: Simple duple/quadruple meter ($4/4$), standard symmetric locomotor synchronization.
   - $\tau = 1.0$: Compound duple meter ($6/8$), dual-level hierarchical subdivision inducing multi-frequency phase-locking in Kuramoto oscillators ($\gamma_O \gg 0$).
3. **Cortisol ($C$, Stress & Allostatic Uncertainty Gating):** Mapped to **Session Entropy ($H_s$)**, calculated over rolling 30-minute windows:
   $$H_s = -\sum_{k} p_k \log_2 p_k$$
   where high entropy indicates erratic acoustic switching, high uncertainty, and active cognitive exploration/stress, triggering the allostatic recognition gate $r_t$.
4. **Adrenaline ($A$, Sympathetic Activation & Motor Dissipation):** Mapped to **Spectral Energy / Loudness ($E \in [0, 1]$)**, setting the corrective dissipation bandwidth $\mu$.
5. **Serotonin ($S$, Steady-State Homeostasis & Attractor Stabilization):** Mapped to **Ground Tempo / Pacing ($\text{BPM}$)** and steady-state behavioral state retention across extended listening sessions.

This yields the complete 5-dimensional **TDF (The DOCAS Framework) state vector**:
$$\vec{M}_{\text{TDF}} = \begin{bmatrix} 
\text{Tempo (BPM)} \\ 
\text{Metric Hierarchy Ratio } (\tau) \\ 
\text{Spectral Energy / Loudness } (E) \\ 
\text{Session Entropy } (H_s) \\ 
\text{Phase / Skip Dynamics } (\Delta \phi) 
\end{bmatrix} \in \mathbb{R}^5$$

We contrast this against the **Baseline Control Feature Set**:
$$\vec{M}_{\text{Baseline}} = \begin{bmatrix} 
\text{Tempo (BPM)} \\ 
\text{Primary Genre (Categorical One-Hot)} 
\end{bmatrix}$$

---

## 2. Frozen Hypotheses & Quantitative Criteria

We pre-register four quantitative hypotheses before running simulation scripts:

### Hypothesis M1: Metric Hierarchy Disambiguation over Scalar BPM
**Hypothesis:** The metric hierarchy ratio $\tau$ resolves the scalar tempo degeneracy across distinct behavioral regimes (Focus/Work, Physical Exercise, Creative Flow, Decompression). Specifically, while scalar BPM fails to distinguish Focus ($60\text{--}90\text{ BPM}$) from Decompression ($50\text{--}80\text{ BPM}$), or Creative Flow ($90\text{--}130\text{ BPM}$) from Physical Exercise ($120\text{--}150\text{ BPM}$), metric hierarchy $\tau$ will account for massive, statistically significant between-group variance.
* **Criterion C1 (Metric Hierarchy Variance Explanation):** In a one-way analysis of variance (ANOVA) across the 4 target behavioral states on $N = 10,000$ simulated sessions, the metric hierarchy ratio $\tau$ must yield:
  $$F \ge 1,000.0, \quad p < 0.001, \quad \eta^2 \ge 0.140 \quad (\text{large effect size})$$

### Hypothesis M2: Multidimensional TDF Information Gain
**Hypothesis:** The full 5-channel TDF state vector $\vec{M}_{\text{TDF}}$ provides synergistic mutual information regarding the underlying user cognitive state that significantly exceeds the information contained in scalar tempo and genre tags alone.
* **Criterion C2 (Excess Mutual Information & Relative Gain):** The mutual information $I(\text{Target State}; \vec{M}_{\text{TDF}})$ must satisfy:
  $$I(\text{Target State}; \vec{M}_{\text{TDF}}) \ge 1.00\text{ bits}$$
  and the relative information gain over the baseline control must exceed $50.0\%$:
  $$\Delta I_{\text{rel}} = \frac{I(\text{Target State}; \vec{M}_{\text{TDF}}) - I(\text{Target State}; \vec{M}_{\text{Baseline}})}{I(\text{Target State}; \vec{M}_{\text{Baseline}})} \ge 0.500$$

### Hypothesis M3: Behavioral State Decoding & Misclassification Collapse
**Hypothesis:** Incorporating metric hierarchy ($\tau$), spectral energy ($E$), session entropy ($H_s$), and skip dynamics ($\Delta \phi$) enables high-fidelity state classification across the 4 behavioral regimes, eliminating the high-error classification boundaries observed under scalar tempo baselines.
* **Criterion C3 (Classification Performance & Error Reduction):** In a 5-fold cross-validated multi-class evaluation, the enhanced TDF model must achieve:
  $$\text{Macro } F_1 \ge 0.850, \quad \text{One-vs-Rest ROC-AUC} \ge 0.950, \quad \Delta F_1 = F_{1,\text{TDF}} - F_{1,\text{Baseline}} \ge +0.100$$
  and suppress classification error rate by $\ge 50.0\%$:
  $$\frac{1 - F_{1,\text{TDF}}}{1 - F_{1,\text{Baseline}}} \le 0.500$$

### Hypothesis M4: Permutation Significance under Shuffled Null
**Hypothesis:** The observed state discrimination is non-spurious and invariant to generative noise artifacts.
* **Criterion C4 (Shuffled Label Permutation Test):** Under $B = 2,000$ label permutations, the empirical $p$-value for the omnibus test statistic must satisfy:
  $$p_{\text{perm}} < 0.001 \quad (\text{zero permutation scores exceed the true test statistic})$$

---

## 3. Experimental Parameters & Methodology

- **Sample Size:** $N = 10,000$ total sessions ($n = 2,500$ sessions per behavioral state).
- **Target Behavioral States:**
  1. `Focus/Work`: Moderate pacing ($60\text{--}90\text{ BPM}$), simple duple or triple ambient structure ($\tau \approx 0.35$), low spectral energy ($E \in [0.20, 0.50]$), low session entropy ($H_s \in [0.60, 1.40]$: high repeat consistency), minimal skip dynamics ($\Delta \phi \le 0.08$).
  2. `Physical Exercise`: High pacing ($120\text{--}155\text{ BPM}$), driving simple duple meter ($\tau \approx 0.50$), high spectral energy ($E \in [0.70, 0.98]$), moderate entropy ($H_s \in [1.20, 2.20]$), low skip dynamics ($\Delta \phi \le 0.10$).
  3. `Creative Flow`: Broad pacing ($85\text{--}130\text{ BPM}$), rich compound and polyrhythmic meter ($\tau \approx 0.85$, high $6/8$ prevalence), moderate-high spectral energy ($E \in [0.45, 0.80]$), high session entropy ($H_s \in [2.00, 3.50]$: eclectic genre exploration), elevated exploratory skip dynamics ($\Delta \phi \in [0.15, 0.35]$).
  4. `Decompression`: Slow pacing ($50\text{--}80\text{ BPM}$), gentle simple triple and floating meter ($\tau \approx 0.15$), low spectral energy ($E \in [0.10, 0.35]$), low-to-moderate session entropy ($H_s \in [0.70, 1.60]$), minimal skip dynamics ($\Delta \phi \le 0.06$).
- **Statistical Tests:**
  - One-Way ANOVA and Repeated-Measures ANOVA across states for each feature.
  - Tukey-Kramer Honestly Significant Difference (HSD) post-hoc pairwise tests with family-wise error rate $\alpha = 0.05$.
  - Effect size calculations: Eta-squared ($\eta^2$), Omega-squared ($\omega^2$), and pairwise Cohen's $d$.
  - Mutual information estimation via $k$-nearest neighbors (Kraskov-Stögbauer-Grassberger) and binned estimators.
  - Multi-class Logistic Regression & Random Forest classifiers evaluated via stratified 5-fold cross-validation.
  - Permutation test ($B = 2,000$ iterations) shuffling state labels.
- **Random Seed:** Strict `seed=42`.

---

## 4. Compound Verdict Rule

- **COMPOUND PASS:** All 4 pre-registered criteria (C1, C2, C3, C4) met under frozen thresholds.
- **COMPOUND FAIL:** Any criterion fails under frozen thresholds. All observed values must be reported honestly without post-hoc threshold adjustment.
