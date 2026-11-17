# Pre-Registration: Sim PILOT-V4.6 (180-Day N=1 Dense Phenotype — 100% Stream-to-Hypothesis Bijection)

- **Document ID:** `SIM_PILOT_V4_6_PRE_REGISTRATION.md`
- **Target Protocol:** `DOCAS_PILOT_1_HUMAN_PROTOCOL.md` (Version 4.6)
- **Simulation Script:** `code/simulations/wearables_pipeline/simulate_180day_dense_pilot.py`
- **Results Artifact:** `code/simulations/wearables_pipeline/sim_pilot2_results.json`
- **Freeze Timestamp:** 2026-11-15 (Pre-Collection Simulation & Criterion Freeze)
- **Deterministic Seed:** `42` (plus AR(1) null-calibration Monte Carlo ensemble `B = 200`, seeds `100..299`)

## 1. Study Design, Three-Paper Cascade & Two-Phase Split (Days 1–180 | Dec 1, 2026 – May 30, 2027)
1. **Days 1–90 (Phase 1 — Cycle 1 Cessation & Network Reset; Dec 1, 2026 – Feb 28, 2027):** Tracks post-cessation cannabinoid washout and Cycle 1 cellular/neuro-endocrine resynchronization; **Days 1–14** are nested as cognitive/motor practice-curve burn-in ($RT(d) = RT_\infty + a \cdot e^{-d/\tau_{\text{learn}}}$, preceded by 3 pre-Day-0 practice runs) and excluded from steady-state cognitive parameter estimation.
2. **Days 91–180 (Phase 2 — Cycle 2 Clean Steady-State Financial Shock Baseline; Mar 1 – May 30, 2027):** Evaluates clean steady-state ARIMAX/DSEM ($AR(1)$ prewhitened) coupling between real-world financial prediction errors ($\varepsilon_t$) and all 30 streams, deriving the **Minimal-to-Deep Hub-to-Spoke Transfer Function** (`Apple HealthKit / Health Connect + Ledger ε_t` $\rightarrow$ 30-stream Hub allostatic state).
3. **Strict Self-Blinding & Retrospective Archive Lock:** Read-only `/retrospective_archive/` locked Nov 30, 2026; record-only blinding enforced until May 30, 2027 unblinding.

## 2. 100% Stream-to-Hypothesis Bijection (30 Itemized Streams)
Every physical device, clinical panel, digital archive, and active log in Stage 1 maps 1-to-1 to the pipeline (`PILOT-H1`..`PILOT-H12` + `C1`–`C10`, zero unmapped streams):
- Muse S Athena overnight + weekly 5-min baseline fNIRS/EEG (`PILOT-H1`, `PILOT-H8`)
- Apple Watch PPG HRV RMSSD, Wrist Temp, Sleep Stages, $\mathrm{SpO}_2$, Respiratory Rate, Ambient/Headphone dB, `TimeInDaylight`, 6-yr archive (`PILOT-H2`, `PILOT-H3`, `PILOT-H5`, `PILOT-H10`)
- Dexcom G7 / Stelo CGM (`PILOT-H12`) + 11 MyFitnessPal Saved Meals (Write-Only HealthKit)
- Hilo/Aktiia Cuffless BP & Throne Smart Toilet (`PILOT-H6`) + FITINDEX Fasted Mass/TBW %
- iPad Creyos/PsyToolkit + Wired 1000 Hz Akai MPK Mini (CoreMIDI + 48 kHz acoustic transient sync; $\ge 30\text{–}45\text{ min}$ forearm rest; `PILOT-H7`, `PILOT-H8`) + Solo-Room Blue Yeti / Brio 4K (feature-only; raw purged)
- Weekly Pre-Yoga Airofit Pro (`MIP`, `MEP`, `VLC`; `PILOT-H9`)
- Aranet4 ($\mathrm{CO}_2$, Temp, RH, hPa) + Local Meteorological/Photoperiod Station + Philips Hue Pre-Bed Lux + Circle View IR (`PILOT-H10`)
- Apple Music + Multi-Year Repeat Archive, Reading Logs, Journal Logs, Retail Order History, Screen/Notes/Calendar Metadata, Sender-Only Local Messaging Metadata (`is_from_me=1`, zero third-party PII), CoreMotion Exertion / GTG Calisthenics (`PILOT-H5`, `PILOT-H11`)
- **Monthly Core Labs (Every 30d, 8:00–8:30 AM Fasted, 72h Biotin Hold):** CMP, CBC w/ Differential, Lipid Panel, hs-CRP, Fasting Insulin (HOMA-IR), Morning Serum Cortisol (`PILOT-H12`)
- **Quarterly Add-Ons (Day 0, M3, M6 Only) & Biological Anchors:** HbA1c, Free/Total Testosterone + SHBG, Estradiol, TSH/Free T3/Free T4, ApoB, Ferritin, 25-OH Vitamin D, Vitamin B12; Day 0/90/180 CLIA cellular panels (48–72h abstinence); Day 0 root/tip virgin hair lock + Sequencing.com 30x WGS + de-identified historical outpatient EHRs (`PILOT-H12`)
- **Behavioral, Nutrition & Blinding Standardization:** 11 MyFitnessPal Saved Meals (Meal Timestamps ON, Write-Only HealthKit), 5–7 AM & 5–7 PM Hilo/Muse charging blocks, weekly pre-yoga Airofit, 400-rep GTG + MWF PPL + M–F Yoga, pre-Day-0 melatonin cessation, no GLP-1 RA, 3 pre-Day-0 cognitive practice runs, $\ge 30\text{–}45\text{ min}$ forearm rest before MPK Mini, and strict record-only self-blinding through Month 6 (`PILOT-H1..H12`)

## 3. Frozen Falsification Criteria (C1–C10)
- **C1 (Exertion & Pharmacological Confounder Residualization):** After subtracting CoreMotion mechanical power and Caffeine/Cannabis PK kernels, residual variance explained by workout wattage is $R^2_{\text{resid}} \le 0.0200$.
- **C2 (Asymmetric Master Law Parameter Recovery on Days 15–180 under OU Process Noise):** Triadic Instrumental-Variable EIV calibration + local shock-locked estimator recovers positive $\hat{\lambda}^+$ within $|\hat{\lambda}^+ - \lambda^+_{\text{true}}| \le 0.0250$ and strictly asymmetric $\hat{\lambda}^- > \hat{\lambda}^+$ without oracle constants or `S_true`.
- **C3 (Serotonergic Multi-Day Relaxation Recovery):** Estimated $\hat{\tau}_{\text{relax}} \in [2.0, 4.0]\text{ days}$.
- **C4 (Benjamini-Yekutieli FDR under AR(1) Prewhitening):** Across all 12 stream hypotheses (`PILOT-H1`..`PILOT-H12`, after AR(1) prewhitening and Days 1–14 practice detrending), maximum BY-adjusted $q_{\max} \le 0.0500$.
- **C5 (Endocrine / Blood Panel Allostatic AUC Concordance):** 6 monthly blood panels ($hs\text{-CRP}$ + morning cortisol) and retrospective endocrine AUC correlate with cumulative CGM/BP allostatic load at $r \ge 0.40, p < 0.01$.
- **C6 (Airofit MIP/MEP/VC & Aranet4 CO₂ / TimeInDaylight Coupling):** AR(1)-prewhitened Airofit MIP positively tracks next-night vagal RMSSD ($r \ge 0.20, p < 0.01$) and Aranet4 $\mathrm{CO}_2$ positively tracks practice-detrended PVT-B latency ($r \ge 0.25, p < 0.001$).
- **C7 (Practice-Curve Detrending Fidelity):** Cognitive battery exponential learning fit recovers $\tau_{\text{learn}}$ on Days 1–14 without attenuating Phase 2 shock sensitivity (post-detrending shock Cohen's $d \ge 0.50$).
- **C8 (AR(1) Null-Calibration / Type-I Error Guard):** Under synthetic AR(1) null series with realistic physiological autocorrelation ($\rho_1 = 0.72$) and zero true shock effect ($B = 400$ Monte Carlo runs), empirical false-positive rate of the prewhitened DSEM/ARIMAX test at $\alpha = 0.05$ is bounded by $\mathrm{FPR}_{\mathrm{null}} \le 0.08$, while un-prewhitened naive $t$-tests inflate $\mathrm{FPR}_{\mathrm{naive}} > 0.20$ (demonstrating why AR(1) prewhitening is mandatory).
- **C9 (Blind 12-Draw Simulation-Based Calibration / Zero Oracle Leakage):** Under 12 random parameter/loading draws $(\lambda^* \sim U[0.14, 0.34], \tau_{\text{relax}}^* \sim U[2.0, 4.0], c_f^*, c_e^*, c_r^*)$ using a blind profile-likelihood estimator that breaks the bilinear $c_k \lambda = \text{const}$ scale degeneracy solely via the unit-anchored $[0, 1]$ daily Task 1 behavioral probe ($c_{\text{probe}} \equiv 1$, all physiological $c_k$ estimated free with **zero** oracle constants or `S_true`), blind recovery satisfies $\mathrm{MAE}(\hat{\lambda} - \lambda^*) \le 0.020$ and $\mathrm{MAE}(\hat{\tau} - \tau^*) \le 0.30\text{ days}$.
- **C10 (Minimal-to-Deep Hub-to-Spoke Transfer Compression, Incremental Physiology & Circular-Shift Null):** Fold-isolated blocked-CV Ridge projection from disjoint minimal Spoke streams (`Watch HRV [fold-residualized] + Watch Wrist Temp + Causal Bank Ledger`) to the blind 6-sensor Hub PCA composite (`Muse fNIRS/EEG + CGM + Hilo BP + Airofit MIP + MPK PVT-B`, zero `S_true` oracle) achieves $R^2_{\text{OOS}} \ge 0.60$ in Phase 2 steady state (Days 91–180), outperforms `Ledger-only` by $\Delta R^2_{\text{physio}} \ge +0.15$ under nonzero endogenous OU process noise ($\sigma_w > 0$), and collapses under circular day-shift surrogate falsification ($\tau \in [14, 76]$ days) to median $R^2_{\text{OOS}} \le 0.05$.
