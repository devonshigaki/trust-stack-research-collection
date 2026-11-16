# INSTITUTIONAL REVIEW BOARD (IRB) NOT HUMAN SUBJECTS RESEARCH (NHSR) / EXEMPTION DETERMINATION REQUEST

**Project Title:** DOCAS-PILOT-1: Multimodal 180-Day In-Vivo Continuous Phenotyping of the Master Stability Law  
**Principal Investigator:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Sponsor:** The FreshCredit Lab (Independent Research)  
**Submission Date:** November 2026  
**Protocol Version:** V4.5 (OSF Pre-Registered)  

---

## 1. Scope of Determination: Stage 1 ($N=1$) vs. Stages 2–4 ($N=43$)
This submission requests a formal, **prospective written determination** from an accredited external Institutional Review Board (e.g., WCG IRB) **prior to Day 1 of Stage 1 data collection** so that Stage 1 ($N = 1$ PI-only self-experimentation) is independently adjudicated under **45 C.F.R. § 46.102(e)** (Not Human Subjects Research: *"no intervention or interaction with any external living individual"*), or—if the reviewing IRB or target journal classifies structured self-experimentation as Human Subjects Research—under **45 C.F.R. § 46.104(d)(3)** (benign behavioral/sensor interaction exemption) and **45 C.F.R. § 46.110 / 63 FR 60364 Expedited Category 4** (non-invasive external sensors applied within consumer labeling). Post-hoc IRB determinations do not satisfy ICMJE or *Nature Portfolio* human-subjects editorial policies and will not be relied upon.

### Regulatory Separation of Stages 2–4 & Stage 1 Tiering:
*   **Stage 1 ($N = 1$ PI Self-Tracking & Personal Wellness Records — Scope of This Filing):** The Principal Investigator (Devon Shigaki) is the sole participant and sole researcher. To maintain strict regulatory clarity prior to Day 1, Stage 1 cleanly partitions:
    1. *Tier 1A (Non-Invasive Consumer Wearables & Ambient Sensors within Consumer Labeling):* Apple Watch Series 8 (`TimeInDaylight`, PPG HRV, wrist temperature), Muse S Athena (fNIRS/EEG), Dexcom Stelo OTC iCGM, Aranet4 ($\mathrm{CO}_2$, Temp, RH) + optional public EPA/PurpleAir outdoor $\mathrm{PM}_{2.5}$, Philips Hue pre-bed lux, wired USB Akai MPK Mini cognitive battery (PVT-B, Go/No-Go, 2-Back, Stroop), **Airofit Pro** respiratory muscle trainer (`MIP`/`MEP`/`VC`), Throne smart toilet, Fitindex scale, Logitech Circle View, and Brio 4K / Yeti Nano (**feature-only extraction; raw audio/video purged or air-gapped; strict minor/multi-speaker exclusion gate**).
    2. *Tier 1B (PI Self-Ordered Clinical/Wellness Records & Personal Device Logs):* Hilo/Aktiia cuffless BP (calibrated against oscillometric cuff), 6 monthly CLIA-certified venous blood panels (Quest/Labcorp), and 1x air-gapped 30x Whole Genome Sequencing (`PGS`/`CYP2C9`/`CYP1A2`/`FAAH`/`COMT` secondary covariates) are conducted under standard consumer/clinical ordering and ingested strictly post-collection as secondary $N=1$ personal covariates—or covered under a unified prospective IRB Expedited Review determination (45 C.F.R. § 46.110 Categories 2 & 4) prior to Day 1.
*   **Stages 2–4 ($N = 43$ External Human Subjects — Separate Full/Expedited IRB Gating):** Any enrollment of external human participants ($N = 43$), venous blood draws, scalp hair specimen harvesting, medical spirometry, or Whole Genome Sequencing (GINA / 45 C.F.R. § 46 protections) in external volunteers is **strictly gated behind a separate, prospective Full/Expedited IRB Protocol and Informed Consent approval** prior to recruiting any external participant. **Minors & Non-Enrolled Household Members:** Strictly excluded from all data collection (`speaker_count == 1` automated filter).

## 2. Ethical Safeguards & Independent Monitoring ("Kill Switch")
While self-experimentation may be legally exempt, ethical integrity under the **WMA Declaration of Helsinki (2024 revision)** demands objective safety limits to prevent investigator bias from compromising physical or psychological safety during an intensive 180-day protocol.

**The N=1 Data and Safety Monitoring Board (DSMB):**
1.  **Trusted Third-Party Monitor:** A qualified, independent medical or bioethical professional is appointed as the external monitor.
2.  **Bayesian Stopping Rules:** The local ingestion pipeline calculates rolling averages of critical safety parameters (e.g., sustained RMSSD suppression $> 30\%$, acute sleep deprivation, or sustained Dexcom Stelo OTC `"Below 70 mg/dL"` / `"Above 250 mg/dL"` flags or fingerstick-confirmed $< 70\text{ mg/dL}$ excursions over consecutive days — reflecting FDA `K234077` Stelo reporting bounds of $70\text{--}250\text{ mg/dL}$). 
3.  **Absolute Kill Switch Authority:** If Bayesian stopping thresholds are breached, the independent monitor holds absolute, non-negotiable authority to suspend the 180-day pilot immediately. The investigator forfeits the right to override the monitor.

## 3. Data Privacy and Regulatory Sequestration (ECOA/FCRA)
To ensure the empirical research does not violate federal lending regulations (Equal Credit Opportunity Act / Regulation B, 12 C.F.R. § 1002; Fair Credit Reporting Act, 15 U.S.C. § 1681):
*   **The Sequestration Wall:** All Stage 1 physiological, biometric, cognitive, acoustic-feature, and environmental telemetry (fNIRS, EEG, PPG, OTC iCGM, Airofit, Aranet4, PVT-B/2-Back/Stroop, Reading logs, and secondary clinical covariates) are collected strictly as *scientific correlation signals* stored in a local encrypted edge database (`trust_wearables_edge.db`). Hair metabolomics and external-volunteer biospecimens are deferred exclusively to IRB-approved Stages 2–4. Raw audio, raw 4K video, and raw WGS `.FASTQ`/`.BAM` files are never retained in shared/analytical datasets (feature-only extraction; minor/household voices and faces auto-purged).
*   **Non-Interference:** These streams possess **ZERO** schema paths and zero integration into the financial credit scoring, underwriting, or adverse-action systems. 

## 4. Ecological Momentary Assessment (EMA) & Fatigue Mitigation
An intense 180-day protocol carries a severe risk of participant fatigue.
*   **Micro-Randomized Trial (MRT) Design:** Instead of random or static hourly surveys, EMA triggers are governed by Just-In-Time Adaptive Interventions (JITAI). 
*   **Physiological Triggering:** Psychological self-assessments (e.g., Affect circumplex) are dynamically triggered by the Apple Watch only upon detecting a $> 15\%$ acute shift in autonomic vagal tone, minimizing survey fatigue while capturing critical state transitions.
*   **Data Provenance:** All self-reported data is captured via a localized, 21 CFR Part 11 compliant instance of REDCap to guarantee non-repudiation and immutable audit trails.

## 5. Conclusion
By securing this formal NHSR/Exemption letter, the resulting 180-day dataset is fully cleared for publication in Tier-1 scientific journals (e.g., *Nature*, *Science*), satisfying peer-review editorial policies regarding ethical oversight without violating federal regulations.