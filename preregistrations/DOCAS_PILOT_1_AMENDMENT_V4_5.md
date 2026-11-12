# DOCAS-PILOT-1: OSF FORMAL PROTOCOL AMENDMENT (VERSION 4.5)
**Document ID:** `DOCAS_PILOT_1_AMENDMENT_V4_5.md`  
**Registration Target:** Open Science Framework (OSF Pre-Registration Freeze)  
**Parent Protocol:** `DOCAS_PILOT_1_HUMAN_PROTOCOL.md` (Version 4.4)  
**Principal Investigator:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Standard Adherence:** TOP Tier 3 / CONSORT-EHEALTH / IEEE-EMBS / Cochrane RoB 2 / APA JARS-Quant  

---

## 1. Rationale for Protocol Amendment

To prevent post-hoc data dredging (HARKing / p-hacking) and ensure uncompromised scientific integrity under **TOP (Transparency and Openness Promotion) Guidelines**, this amendment formally freezes the mathematical hypotheses, data structures, and de-biasing filters for five newly integrated multimodal observation streams prior to trial data analysis:

1.  **Books Currently Reading (Kindle / E-Reader Telemetry)**
2.  **High-Frequency Workout Kinematics & Exertion (Apple Watch / CoreMotion)**
3.  **Ambient Acoustic Exposure & Music Choices (Apple Music Telemetry)**
4.  **Forced Pulmonary Mechanics & Flow-Volume Dynamics (Medical Spirometry)**
5.  **Segmental Scalp Hair Metabolomics & Trace Minerals (LC-MS/MS & ICP-MS)**

---

## 2. Acquisition Taxonomy: Active vs. Passive Telemetry

```
========================================================================================================================
                                EXPANDED DATA STREAM ACQUISITION TAXONOMY
========================================================================================================================
Stream Name               | Acquisition Modality         | Sampling Resolution  | Primary Epistemic Function
--------------------------+------------------------------+----------------------+---------------------------------------
1. Books Reading          | Passive Telemetry of an      | Millisecond event log| Cognitive fatigue, reading velocity
   (Kindle / E-Reader)    | Active Conscious Behavior    | (page-flips / dwell) | (WPM), attention span under stress
--------------------------+------------------------------+----------------------+---------------------------------------
2. Workout Dynamics       | Hybrid (Active Bout Start +  | 50 Hz – 100 Hz IMU   | Mechanical power decoupling; isolating
   (CoreMotion / Apple W) | Passive Ambient Sensors)     | 1 Hz PPG optical     | physical exertion from mental stress
--------------------------+------------------------------+----------------------+---------------------------------------
3. Apple Music Telemetry  | Passive Ambient Background   | Discrete per-track   | Acoustic arousal, tempo/valence,
   (Playback / DSP)       | Event Logging                | (ISRC / skips / DSP) | isolating insomnia from allostasis
--------------------------+------------------------------+----------------------+---------------------------------------
4. Lung Capacity          | Strictly Active Physical     | 500 Hz raw ADC       | Pulmonary boundary constraints;
   (Medical Spirometry)   | Forced Exhalation Maneuver   | differential pressure| Respiratory Sinus Arrhythmia limits
--------------------------+------------------------------+----------------------+---------------------------------------
5. Hair Metabolomics      | Active Scalp Harvest of a    | Longitudinal 90–180d | Chronic HPA-axis allostatic load,
   (LC-MS/MS & ICP-MS)    | Passive Historical Matrix    | retrospective segment| baseline cortisol/cortisone time-capsule
========================================================================================================================
```

---

## 3. Pre-Registered Hypotheses & Success Criteria

### Hypothesis H-READ (Cognitive Fatigue & Attention Gating):
*   **Hypothesis:** Sustained contractual allostatic load ($\varepsilon < 0$ financial shock) induces prefrontal executive depletion, manifested as a statistically significant drop in reading velocity ($\Delta \text{WPM} \ge 25.0\%$) and a $> 2.0\times$ increase in character dwell time dispersion during evening reading sessions.
*   **Frozen Criterion:** Permutation test $p < 0.01$ correlating evening reading velocity drops with daytime prefrontal fNIRS $\Delta [\mathrm{HbO}_2]$ attenuation in medial prefrontal cortex (BA10/BA32).

### Hypothesis H-WORKOUT (Exertion Confounder Decoupling):
*   **Hypothesis:** Convolving high-frequency workout kinematics (CoreMotion IMU mechanical power in Watts, cadence, and active METs) with an exponential cardiac recovery kernel residualizes physical exertion tachycardia, leaving unconfounded psychological vagal modulation ($O$-channel).
*   **Frozen Criterion:** Residual vagal metric $\mathrm{RMSSD}_{\text{stress}}$ exhibits zero statistical correlation ($R^2 \le 0.02, p > 0.10$) with mechanical workout power post-recovery ($\Delta t > 30\text{ min}$).

### Hypothesis H-MUSIC (Acoustic Arousal vs. Allostasis Separation):
*   **Hypothesis:** Late-night acoustic music feature vectors (tempo $> 120\text{ BPM}$, valence $< 0.35$, high spectral centroid) predict nocturnal sleeping wrist temperature elevation ($\Delta T_{\text{wrist}} \ge 0.15^\circ\text{C}$), allowing the circadian filter to isolate acute cognitive arousal from systemic allostatic cortisol elevation ($C$-channel).
*   **Frozen Criterion:** Multi-modal GLM demonstrates that acoustic tempo explains $\ge 30\%$ of nocturnal temperature variance independently of daytime financial prediction errors.

### Hypothesis H-SPIRO (Pulmonary Bounds on Vagal Brake):
*   **Hypothesis:** Individualized Forced Vital Capacity ($FVC$) and Forced Expiratory Volume in 1 second ($FEV_1$), corrected for ambient BTPS thermodynamic variables, mathematically bound the maximum dynamic range of Respiratory Sinus Arrhythmia (RSA), setting the physiological ceiling for vagal recovery ($O$- and $S$-channels).
*   **Frozen Criterion:** Normalizing high-frequency HRV by BTPS-corrected $FVC$ collapses inter-subject vagal recovery variance by $\ge 40\%$.

### Hypothesis H-HAIR (Longitudinal Endocrine Ground Truth):
*   **Hypothesis:** Scalp hair segmental cortisol and cortisone concentrations (LC-MS/MS; pg/mg) measured from proximal $3\text{ cm}$ segments correlate identically with the cumulative time-integral of 90-day daily ambulatory interstitial glycemic excursions ($dG/dt$) captured by continuous glucose monitoring.
*   **Frozen Criterion:** Pearson correlation between hair cortisol/cortisone ratio and 90-day cumulative CGM stress area-under-the-curve evaluates to $r \ge 0.80$ ($p < 0.001$).

---

## 4. Cryptographic Sequestration & Chain-of-Custody Protocols

1.  **Hair Specimen Blinding & Genomic Isolation:**
    *   Scalp cutting leaving $\ge 1.0\text{ mm}$ stubble ensures zero follicular root bulbs or diploid cells enter the specimen tube, eliminating whole-genome DNA contamination.
    *   Specimens are tracked exclusively via unforgeable, single-use, cryptographically salted pseudonymous identifiers:
        $$\text{PSID} = \mathrm{HMAC\_SHA256}(\text{MasterPrivateKey}, \text{"HAIR\_PILOT1\_BATCH"} \,||\, \text{SegmentID})[0:16]$$
    *   Laboratory requisitions are legally constrained to LC-MS/MS steroid metabolomics and ICP-MS trace elemental analysis, with explicit contractual prohibition of nucleic acid isolation.
2.  **Spirometry Direct BLE Protocol:**
    *   Direct local BLE connection using IEEE 11073-10421 driver extracts raw $500\text{ Hz}$ transducer voltages, completely bypassing third-party commercial cloud intermediaries.
3.  **The Regulatory Sequestration Wall:**
    *   All five streams are stored in local edge databases (`trust_wearables_edge.db`).
    *   **Zero-Interference Invariant:** Medical, biological, literary, musical, and workout data possess **ZERO** schema paths, zero SQL queries, and zero memory pointers into credit underwriting, scoring, or decision algorithms, ensuring complete compliance with ECOA / Regulation B (12 C.F.R. § 1002) and FCRA (15 U.S.C. § 1681).
