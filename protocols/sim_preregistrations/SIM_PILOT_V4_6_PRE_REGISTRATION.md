# Pre-Registration: Sim PILOT-V4.6 (180-Day N=1 Dense Phenotype — 100% Stream-to-Hypothesis Bijection)

- **Document ID:** `SIM_PILOT_V4_6_PRE_REGISTRATION.md`
- **Target Protocol:** `DOCAS_PILOT_1_HUMAN_PROTOCOL.md` (Version 4.6)
- **Simulation Script:** `code/simulations/wearables_pipeline/simulate_180day_dense_pilot.py`
- **Results Artifact:** `code/simulations/wearables_pipeline/sim_pilot2_results.json`
- **Freeze Timestamp:** 2026-11-15 (Pre-Collection Simulation & Criterion Freeze)
- **Deterministic Seed:** `42` (plus AR(1) null-calibration Monte Carlo ensemble `B = 200`, seeds `100..299`)

## 1. Study Design & Phase Partitioning (Days 1–180)
1. **Days 1–14 (Phase 0 — Habituation & Practice-Curve Burn-In):** Excluded from steady-state estimation; fits exponential learning curve $RT(d) = RT_\infty + a \cdot e^{-d/\tau_{\text{learn}}}$ across PVT-B, 2-Back, Go/No-Go, Stroop, and Akai MPK Mini tapping.
2. **Days 15–42 (Phase 1 — 4-Week Observational Baseline & Pharmacokinetic/Washout Calibration):** Establishes passive/active baseline alongside timestamped Cannabis (`THC`/`CBD` mg) and Caffeine (`mg`) PK logging.
3. **Days 43–180 (Phase 2 — Longitudinal Ecological Contrasts):** Evaluates within-subject ARIMAX / DSEM ($AR(1)$ residualized) trust-shock coupling across all hardware streams.

## 2. 100% Stream-to-Hypothesis Bijection
Every physical device and active log in Stage 1 maps 1-to-1 to a simulated synthetic channel and pre-registered hypothesis (`PILOT-H1`..`PILOT-H12`, zero unmapped streams):
- Muse S Athena fNIRS/EEG (`PILOT-H1`, `PILOT-H8`)
- Apple Watch S8 HRV RMSSD, Wrist Temp, Sleep Stages, `TimeInDaylight` (`PILOT-H2`, `PILOT-H3`, `PILOT-H5`, `PILOT-H10`)
- Dexcom Stelo CGM (`PILOT-H12`)
- Hilo/Aktiia Cuffless BP & Throne Smart Toilet (`PILOT-H6`)
- Wired 1000 Hz Akai MPK Mini (Circumplex, Tapping, PVT-B, Go/No-Go, 2-Back, Stroop; `PILOT-H7`, `PILOT-H8`)
- Airofit Pro (`MIP`, `MEP`, `VC`; `PILOT-H9`)
- Aranet4 ($\mathrm{CO}_2$, Temp, RH) + Outdoor $\mathrm{PM}_{2.5}$ + Philips Hue Pre-Bed Lux (`PILOT-H10`)
- Cannabis & Caffeine PK logs, Manual Reading OCR/NLP, CoreMotion Workout Power, Apple Music DSP, Studio Acoustic eGeMAPS (`PILOT-H5`, `PILOT-H11`)
- 6 Monthly Venous Blood Panels (`hs-CRP`, Cortisol, $\text{HbA1c}$, ApoB), 1x 30x WGS PGS/PGx (`CYP2C9`, `CYP1A2`, `FAAH`, `COMT`), Fitindex Smart Scale, Circle View PIR (`PILOT-H12`)

## 3. Frozen Falsification Criteria (C1–C9)
- **C1 (Exertion & Pharmacological Confounder Residualization):** After subtracting CoreMotion mechanical power and Caffeine/Cannabis PK kernels, residual variance explained by workout wattage is $R^2_{\text{resid}} \le 0.0200$.
- **C2 (Master Law Parameter Recovery on Days 15–180):** DSEM/Kalman estimator recovers $\hat{\lambda}$ within $|\hat{\lambda} - \lambda_{\text{true}}| \le 0.0200$.
- **C3 (Serotonergic Multi-Day Relaxation Recovery):** Estimated $\hat{\tau}_{\text{relax}} \in [2.0, 4.0]\text{ days}$.
- **C4 (Benjamini-Yekutieli FDR under AR(1) Prewhitening):** Across all 12 stream hypotheses (`PILOT-H1`..`PILOT-H12`, after AR(1) prewhitening and Days 1–14 practice detrending), maximum BY-adjusted $q_{\max} \le 0.0500$.
- **C5 (Endocrine / Blood Panel Allostatic AUC Concordance):** 6 monthly blood panels ($hs\text{-CRP}$ + morning cortisol) and retrospective endocrine AUC correlate with cumulative CGM/BP allostatic load at $r \ge 0.40, p < 0.01$.
- **C6 (Airofit MIP/MEP/VC & Aranet4 CO₂ / TimeInDaylight Coupling):** AR(1)-prewhitened Airofit MIP positively tracks next-night vagal RMSSD ($r \ge 0.20, p < 0.01$) and Aranet4 $\mathrm{CO}_2$ positively tracks practice-detrended PVT-B latency ($r \ge 0.25, p < 0.001$).
- **C7 (Practice-Curve Detrending Fidelity):** Cognitive battery exponential learning fit recovers $\tau_{\text{learn}}$ on Days 1–14 without attenuating Phase 2 shock sensitivity (post-detrending shock Cohen's $d \ge 0.50$).
- **C8 (AR(1) Null-Calibration / Type-I Error Guard):** Under synthetic AR(1) null series with realistic physiological autocorrelation ($\rho_1 = 0.72$) and zero true shock effect ($B = 400$ Monte Carlo runs), empirical false-positive rate of the prewhitened DSEM/ARIMAX test at $\alpha = 0.05$ is bounded by $\mathrm{FPR}_{\mathrm{null}} \le 0.08$, while un-prewhitened naive $t$-tests inflate $\mathrm{FPR}_{\mathrm{naive}} > 0.20$ (demonstrating why AR(1) prewhitening is mandatory).
- **C9 (Blind 12-Draw Simulation-Based Calibration / Zero Oracle Leakage):** Under 12 random parameter/loading draws $(\lambda^* \sim U[0.14, 0.34], \tau_{\text{relax}}^* \sim U[2.0, 4.0], c_f^*, c_e^*, c_r^*)$ using a blind profile-likelihood estimator that breaks the bilinear $c_k \lambda = \text{const}$ scale degeneracy solely via the unit-anchored $[0, 1]$ daily Task 1 behavioral probe ($c_{\text{probe}} \equiv 1$, all physiological $c_k$ estimated free with **zero** oracle constants or `S_true`), blind recovery satisfies $\mathrm{MAE}(\hat{\lambda} - \lambda^*) \le 0.020$ and $\mathrm{MAE}(\hat{\tau} - \tau^*) \le 0.30\text{ days}$.
