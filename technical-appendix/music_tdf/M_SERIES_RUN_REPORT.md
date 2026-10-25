# Sim M-Series Run Report: Temporal Dynamics of Music (TDF), Metric Hierarchies & Auditory State Gating in DOCAS

**Date:** 2026-10-24 · **Status:** EXECUTED AS FROZEN (Seed = 42, N = 10,000)  
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §2 / GTT §3 / TFP §5 (Version 4.1 additions)  
**Compound Verdict:** **COMPOUND PASS (4/4 CRITERIA SATISFIED)**

---

## 1. Summary of Pre-Registered Results

| Hypothesis | Test Description | Frozen Criterion | Observed Metric | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Metric Hierarchy Disambiguation** | One-Way ANOVA across 4 behavioral regimes for $\tau$ ($3/4$ triple simple $0.0$ vs $4/4$ duple $0.5$ vs $6/8$ compound $1.0$) | $F \ge 1,000.0$, $p < 0.001$, $\eta^2 \ge 0.140$ (large effect) | **$F = 3,561.5$, $p < 10^{-15}$, $\eta^2 = 0.517$** | **PASS** |
| **M2: Multidimensional TDF Information Gain** | Mutual Information $I(\text{Target State}; \vec{M}_{\text{TDF}})$ vs Baseline (BPM + Genre) | $\text{MI} \ge 1.00\text{ bits}$, $\Delta I_{\text{rel}} \ge +50.0\%$ | **$\text{MI} = 3.877\text{ bits}$, $\Delta I_{\text{rel}} = +136.9\%$** | **PASS** |
| **M3: Behavioral State Decoding & Misclassification Collapse** | 5-Fold Cross-Validated multi-class classification across 4 behavioral regimes | Macro $F_1 \ge 0.850$, ROC-AUC $\ge 0.950$, $\Delta F_1 \ge +0.100$, Error Ratio $\le 0.500$ | **Macro $F_1 = 0.944$, AUC $= 0.993$, $\Delta F_1 = +0.136$, Error Ratio $= 0.290$** ($71.0\%$ error reduction) | **PASS** |
| **M4: Permutation Significance under Shuffled Null** | $B = 2,000$ label permutations of empirical null distribution | Empirical $p_{\text{perm}} < 0.001$ | **$p_{\text{perm}} = 0.0000$** (True $F_1 = 0.948$ vs Null Mean $0.252$, Max $0.271$) | **PASS** |

---

## 2. Quantitative Findings & Statistical Breakdown

### A. Omnibus Analysis of Variance (ANOVA) Across Features
Across $N = 10,000$ listening sessions evenly stratified across `Focus/Work`, `Physical Exercise`, `Creative Flow`, and `Decompression`:

1. **Metric Hierarchy Ratio ($\tau$):**
   - $F(3, 9996) = 3,561.48, \quad p < 10^{-300}, \quad \eta^2 = 0.5166, \quad \omega^2 = 0.5164$
   - Group Means: Focus $= 0.375 \pm 0.220$, Exercise $= 0.540 \pm 0.142$, Creative $= 0.775 \pm 0.339$, Decomp $= 0.090 \pm 0.187$.
   - **Post-Hoc Tukey-Kramer HSD:** All pairwise comparisons are significant at $p < 0.0001$. $\tau$ unequivocally disambiguates the scalar tempo overlap between Focus ($75\text{ BPM}$) and Decompression ($68\text{ BPM}$) ($q = 44.8, p < 0.0001$), and between Creative Flow ($110\text{ BPM}$) and Exercise ($135\text{ BPM}$) ($q = 36.9, p < 0.0001$).
2. **Session Entropy ($H_s$):**
   - $F(3, 9996) = 22,231.95, \quad p < 10^{-300}, \quad \eta^2 = 0.8697$
   - Creative Flow exhibits high exploratory entropy ($2.75 \pm 0.35\text{ bits}$), while Focus enforces tight repeat predictability ($1.05 \pm 0.22\text{ bits}$).
3. **Spectral Energy / Loudness ($E$):**
   - $F(3, 9996) = 35,468.61, \quad p < 10^{-300}, \quad \eta^2 = 0.9142$
   - Drives sympathetic arousal segregation: Exercise ($0.85 \pm 0.07$) vs Decompression ($0.22 \pm 0.06$).
4. **Skip Dynamics ($\Delta \phi$):**
   - $F(3, 9996) = 17,214.39, \quad p < 10^{-300}, \quad \eta^2 = 0.8377$
   - Captures active curation prediction errors: Creative Flow ($0.24 \pm 0.06$) vs Focus ($0.05 \pm 0.02$).
5. **Scalar Tempo (BPM):**
   - $F(3, 9996) = 6,707.87, \quad p < 10^{-300}, \quad \eta^2 = 0.6681$
   - While overall tempo varies, scalar BPM exhibits complete confusion between Focus and Decompression (pairwise overlap $> 68\%$).

### B. Mutual Information Escalation
- **Baseline Feature Set (BPM + Genre One-Hot):** $I(\text{Target State}; \vec{M}_{\text{Baseline}}) = 1.6366\text{ bits}$
- **Enhanced TDF Vector ($\vec{M}_{\text{TDF}}$):** $I(\text{Target State}; \vec{M}_{\text{TDF}}) = 3.8766\text{ bits}$
- **Relative Information Gain:** $+136.87\%$ ($> 2.36\times$ total information capacity).
- Individual feature mutual information:
  - $\tau$ (Metric Hierarchy): $0.5186\text{ bits}$
  - $H_s$ (Session Entropy): $0.9482\text{ bits}$
  - $E$ (Spectral Energy): $1.0924\text{ bits}$
  - $\Delta \phi$ (Skip Dynamics): $0.7842\text{ bits}$
  - BPM (Scalar Tempo): $0.5332\text{ bits}$

### C. Predictive State Decoding & Confusion Collapse
In stratified 5-fold cross-validation:
- **Baseline Classifier (Random Forest on BPM + Genre):**
  - Accuracy: $80.86\% \pm 0.52\%$
  - Macro $F_1$: $0.8086 \pm 0.0052$
  - One-vs-Rest ROC-AUC: $0.9579 \pm 0.0018$
  - Confusion: High cross-contamination between Focus and Decompression (14.2% of Focus sessions misclassified as Decompression; 18.6% of Decompression misclassified as Focus).
- **Enhanced TDF Classifier (Random Forest on $\vec{M}_{\text{TDF}}$):**
  - Accuracy: $94.45\% \pm 0.28\%$
  - Macro $F_1$: $0.9445 \pm 0.0028$
  - One-vs-Rest ROC-AUC: $0.9931 \pm 0.0006$
  - Confusion: Focus/Decompression confusion collapses from $18.6\%$ down to $1.8\%$, driven by the metric hierarchy ratio $\tau$ and skip dynamics $\Delta \phi$.
  - Error rate drops from $19.14\%$ to $5.55\%$ (Error Ratio $= 0.290$, a $71.0\%$ reduction in error).

---

## 3. Theoretical Grounding within GTT & DOCAS

1. **Oxytocinergic Phase Entrainment ($O \leftrightarrow \tau$):** In the Master Stability Law $\Delta S_t = \lambda(V_t - E_t)$, rhythmic entrainment governs the phase coupling parameter $\gamma_O$. In compound duple meters ($\tau = 1.0$, $6/8$), dual-frequency Kuramoto entrainment expands the cognitive synchronization cone, fostering divergent exploratory processing (Creative Flow). Simple triple meter ($\tau = 0.0$, $3/4$) provides smooth rotational dissipation suitable for parasympathetic restoration (Decompression).
2. **Cortisol Uncertainty Gating ($C \leftrightarrow H_s$):** High session entropy directly triggers the allostatic recognition gate $r_t = \operatorname{logistic}(\beta_C(\|\varepsilon_t\| - \theta_C))$. When users repeatedly skip and shift styles, allostatic load rises, opening the gate for active behavioral realignment.
3. **Dopaminergic Structural Prediction Error ($D \leftrightarrow \Delta \phi$):** Skips occurring out-of-phase with hypermetric phrasing indicate violation of temporal expectations ($E_t$), signaling cognitive restlessness.

---

## 4. Deposited Artifacts

- **Pre-Registration:** `experiments/simulations_repair_era/music_tdf/SIM_M_SERIES_PRE_REGISTRATION.md`
- **Simulation Script:** `experiments/simulations_repair_era/music_tdf/sim_m_tdf_music.py`
- **Statistical Results:** `experiments/simulations_repair_era/music_tdf/results/statistical_validation.json` & `results/statistical_validation.json`
- **Diagnostic Plots:**
  - `results/plots/metric_distribution_anova.png` (Boxplots & omnibus ANOVA summary)
  - `results/plots/feature_effect_sizes.png` (Eta-squared effect sizes and mutual information escalation)
  - `results/plots/state_space_manifold.png` (Tempo vs $\tau$ phase manifold demonstrating degeneracy resolution)
  - `results/plots/confusion_matrices_comparison.png` (Cross-validated confusion matrices)
  - `results/plots/roc_curves_comparison.png` (One-vs-Rest ROC curves per behavioral state)
- **Downstream Coding Agent Hand-off:** `CODING_AGENT_INTEGRATION_PROMPT.md`
