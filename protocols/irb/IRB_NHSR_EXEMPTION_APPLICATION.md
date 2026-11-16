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
    2. *Tier 1B (PI Self-Ordered Clinical/Wellness Records & Personal Device Logs):* Hilo/Aktiia cuffless BP (blinded monthly cuff calibration), **Quest Diagnostics monthly core venous panels** (8:00–8:30 AM fasted every 30 days: CMP, CBC w/ diff, Lipids, hs-CRP, Fasting Insulin, Morning Cortisol; with quarterly HbA1c, Free/Total Testosterone + SHBG, Estradiol, TSH/FT3/FT4, ApoB, Ferritin, 25-OH-D, B12 at Day 0/M3/M6), **1x Day 0 PI self-clipped foil-wrapped baseline hair lock**, and **1x air-gapped Sequencing.com 30x Whole Genome Sequencing** (`PGS`/`CYP1A2`/`COMT` covariates; cloud purge post-download) are conducted under standard consumer/clinical ordering and ingested strictly post-collection under record-only blinding—or covered under a unified prospective IRB Expedited Review determination (45 C.F.R. § 46.110 Categories 2 & 4) prior to Day 1.
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

## 4. Strict Record-Only Self-Blinding & Fatigue Mitigation
An intense 180-day protocol carries risks of both participant fatigue and observer-expectancy bias.
*   **Record-Only Self-Blinding (Stage 1):** All push notifications, widgets, and summary trend charts are disabled across Apple Health, Stelo, Hilo, Muse, Airofit, MyFitnessPal (Write-Only HealthKit), and Quest portals until Month 6 completion; Watch HRV-triggered EMA prompts are disabled during blinded Stage 1 to prevent dynamic unblinding. Only hardware battery %, electrode contact (`SCI >= 0.80`), and technical ingestion counts are monitored.
*   **Independent Clinical Safety Gate:** Out-of-band Quest critical lab values route exclusively to the external clinical monitor/ordering clinician (`Kill Switch` authority) without exposing routine biometric trends to the PI.
*   **Data Provenance:** All daily timestamps, GTG logs, and pre-bed cognitive runs (`iPad Creyos/PsyToolkit + wired Akai MPK Mini` with $\ge 30\text{–}45\text{ min}$ post-pull-up rest) are hashed locally into an immutable audit log (`trust_wearables_edge.db`).

## 5. Conclusion
By securing this formal NHSR/Exemption letter, the resulting 180-day dataset is fully cleared for publication in Tier-1 scientific journals (e.g., *Nature*, *Science*), satisfying peer-review editorial policies regarding ethical oversight without violating federal regulations.