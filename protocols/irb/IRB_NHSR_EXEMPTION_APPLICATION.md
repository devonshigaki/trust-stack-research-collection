# INSTITUTIONAL REVIEW BOARD (IRB) NOT HUMAN SUBJECTS RESEARCH (NHSR) / EXEMPTION DETERMINATION REQUEST

**Project Title:** DOCAS-PILOT-1: Multimodal 180-Day In-Vivo Continuous Phenotyping of the Master Stability Law  
**Principal Investigator:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Sponsor:** The FreshCredit Lab (Independent Research)  
**Submission Date:** November 2026  
**Protocol Version:** V4.5 (OSF Pre-Registered)  

---

## 1. Scope of Determination: Stage 1 ($N=1$) vs. Stages 2–4 ($N=43$)
This submission requests a formal, **prospective written determination** from an accredited external Institutional Review Board (e.g., WCG IRB) **prior to Day 1 of Stage 1 data collection** so that Stage 1 ($N = 1$ PI-only self-experimentation) is independently adjudicated under **45 C.F.R. § 46.102(e)** (Not Human Subjects Research: *"no intervention or interaction with any external living individual"*), or—if the reviewing IRB or target journal classifies structured self-experimentation as Human Subjects Research—under **45 C.F.R. § 46.104(d)(3)** (benign behavioral/sensor interaction exemption) and **45 C.F.R. § 46.110 / 63 FR 60364 Expedited Category 4** (non-invasive external sensors applied within consumer labeling). Post-hoc IRB determinations do not satisfy ICMJE or *Nature Portfolio* human-subjects editorial policies and will not be relied upon.

### Regulatory Separation of Stages 2–4:
*   **Stage 1 ($N = 1$ Self-Experimentation — Scope of This Filing):** The Principal Investigator (Devon Shigaki) is the sole participant and sole researcher, utilizing non-invasive OTC consumer wearables (Apple Watch Series 8, Muse S Athena, Dexcom Stelo OTC iCGM) strictly within consumer labeling. Note: CE-marked non-US-OTC devices (e.g., Aktiia/Hilo cuffless BP), spirometry/breath assays, hair biospecimen metabolomics, and clinical phlebotomy/WGS are **excluded from Stage 1 and from NHSR self-exemption claims** unless cleared or conducted under prospective clinical IRB supervision.
*   **Stages 2–4 ($N = 43$ External Human Subjects — Separate Full/Expedited IRB Gating):** Any enrollment of external human participants ($N = 43$), venous blood draws, scalp hair specimen harvesting, spirometry, 30x Whole Genome Sequencing (requiring GINA / 45 C.F.R. § 46 protections), or investigational device evaluations (21 C.F.R. § 812 IDE check) is **strictly gated behind a separate, prospective Full/Expedited IRB Protocol and Informed Consent approval** prior to recruiting any external participant.

## 2. Ethical Safeguards & Independent Monitoring ("Kill Switch")
While self-experimentation may be legally exempt, ethical integrity under the **WMA Declaration of Helsinki (2024 revision)** demands objective safety limits to prevent investigator bias from compromising physical or psychological safety during an intensive 180-day protocol.

**The N=1 Data and Safety Monitoring Board (DSMB):**
1.  **Trusted Third-Party Monitor:** A qualified, independent medical or bioethical professional is appointed as the external monitor.
2.  **Bayesian Stopping Rules:** The local ingestion pipeline calculates rolling averages of critical safety parameters (e.g., sustained RMSSD suppression $> 30\%$, acute sleep deprivation, or severe hypoglycemic excursions $< 55\text{ mg/dL}$ over consecutive days). 
3.  **Absolute Kill Switch Authority:** If Bayesian stopping thresholds are breached, the independent monitor holds absolute, non-negotiable authority to suspend the 180-day pilot immediately. The investigator forfeits the right to override the monitor.

## 3. Data Privacy and Regulatory Sequestration (ECOA/FCRA)
To ensure the empirical research does not violate federal lending regulations (Equal Credit Opportunity Act / Regulation B, 12 C.F.R. § 1002; Fair Credit Reporting Act, 15 U.S.C. § 1681):
*   **The Sequestration Wall:** All Stage 1 non-invasive physiological, biometric, and multimodal telemetry (fNIRS, EEG, ECG, OTC iCGM, Music, Reading logs) are collected strictly as *scientific correlation signals* stored in a local encrypted edge database (`trust_wearables_edge.db`). Biospecimen assays (hair metabolomics, phlebotomy, WGS) and spirometry are deferred exclusively to IRB-approved Stages 2–4.
*   **Non-Interference:** These streams possess **ZERO** schema paths and zero integration into the financial credit scoring, underwriting, or adverse-action systems. 

## 4. Ecological Momentary Assessment (EMA) & Fatigue Mitigation
An intense 180-day protocol carries a severe risk of participant fatigue.
*   **Micro-Randomized Trial (MRT) Design:** Instead of random or static hourly surveys, EMA triggers are governed by Just-In-Time Adaptive Interventions (JITAI). 
*   **Physiological Triggering:** Psychological self-assessments (e.g., Affect circumplex) are dynamically triggered by the Apple Watch only upon detecting a $> 15\%$ acute shift in autonomic vagal tone, minimizing survey fatigue while capturing critical state transitions.
*   **Data Provenance:** All self-reported data is captured via a localized, 21 CFR Part 11 compliant instance of REDCap to guarantee non-repudiation and immutable audit trails.

## 5. Conclusion
By securing this formal NHSR/Exemption letter, the resulting 180-day dataset is fully cleared for publication in Tier-1 scientific journals (e.g., *Nature*, *Science*), satisfying peer-review editorial policies regarding ethical oversight without violating federal regulations.