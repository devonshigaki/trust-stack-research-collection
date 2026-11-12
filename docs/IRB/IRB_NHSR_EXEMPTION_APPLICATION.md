# INSTITUTIONAL REVIEW BOARD (IRB) NOT HUMAN SUBJECTS RESEARCH (NHSR) / EXEMPTION DETERMINATION REQUEST

**Project Title:** DOCAS-PILOT-1: Multimodal 180-Day In-Vivo Continuous Phenotyping of the Master Stability Law  
**Principal Investigator:** Devon Shigaki (ORCID: 0009-0003-8977-8010)  
**Sponsor:** The FreshCredit Lab (Independent Research)  
**Submission Date:** November 2026  
**Protocol Version:** V4.5 (OSF Pre-Registered)  

---

## 1. Request for Exemption or NHSR Determination
This submission requests a formal determination from the Institutional Review Board (e.g., WCG IRB) that the proposed protocol qualifies as **Not Human Subjects Research (NHSR)** or is otherwise **Exempt from ongoing IRB review** under 45 CFR § 46.104.

### Primary Regulatory Justification (Self-Experimentation):
This protocol involves an $N=1$ longitudinal study where the Principal Investigator (Devon Shigaki) is the **sole participant and sole researcher**. 
Under OHRP (Office for Human Research Protections) guidance and standard institutional policies, research involving only the investigator conducting self-experimentation often does not meet the definition of "human subjects research" requiring full IRB oversight, provided the research does not involve FDA-regulated products (e.g., IND/IDE). 

*All sensors utilized in this protocol (Dexcom Stelo, Apple Watch, Muse S, Aktiia) are FDA-cleared or FDA-exempt Class I/II devices utilized strictly within their intended use parameters as over-the-counter (OTC) wellness or general physiological monitors.*

## 2. Ethical Safeguards & Independent Monitoring ("Kill Switch")
While self-experimentation may be legally exempt, ethical integrity under the **WMA Declaration of Helsinki (2024 revision)** demands objective safety limits to prevent investigator bias from compromising physical or psychological safety during an intensive 180-day protocol.

**The N=1 Data and Safety Monitoring Board (DSMB):**
1.  **Trusted Third-Party Monitor:** A qualified, independent medical or bioethical professional is appointed as the external monitor.
2.  **Bayesian Stopping Rules:** The local ingestion pipeline calculates rolling averages of critical safety parameters (e.g., sustained RMSSD suppression $> 30\%$, acute sleep deprivation, or severe hypoglycemic excursions $< 55\text{ mg/dL}$ over consecutive days). 
3.  **Absolute Kill Switch Authority:** If Bayesian stopping thresholds are breached, the independent monitor holds absolute, non-negotiable authority to suspend the 180-day pilot immediately. The investigator forfeits the right to override the monitor.

## 3. Data Privacy and Regulatory Sequestration (ECOA/FCRA)
To ensure the empirical research does not violate federal lending regulations (Equal Credit Opportunity Act / Regulation B, 12 C.F.R. § 1002; Fair Credit Reporting Act, 15 U.S.C. § 1681):
*   **The Sequestration Wall:** All physiological, biometric, and multimodal telemetry (fNIRS, EEG, ECG, CGM, Spirometry, Hair Metabolomics, Music, Reading logs) are collected strictly as *scientific correlation signals* stored in a local encrypted edge database (`trust_wearables_edge.db`).
*   **Non-Interference:** These streams possess **ZERO** schema paths and zero integration into the financial credit scoring, underwriting, or adverse-action systems. 

## 4. Ecological Momentary Assessment (EMA) & Fatigue Mitigation
An intense 180-day protocol carries a severe risk of participant fatigue.
*   **Micro-Randomized Trial (MRT) Design:** Instead of random or static hourly surveys, EMA triggers are governed by Just-In-Time Adaptive Interventions (JITAI). 
*   **Physiological Triggering:** Psychological self-assessments (e.g., Affect circumplex) are dynamically triggered by the Apple Watch only upon detecting a $> 15\%$ acute shift in autonomic vagal tone, minimizing survey fatigue while capturing critical state transitions.
*   **Data Provenance:** All self-reported data is captured via a localized, 21 CFR Part 11 compliant instance of REDCap to guarantee non-repudiation and immutable audit trails.

## 5. Conclusion
By securing this formal NHSR/Exemption letter, the resulting 180-day dataset is fully cleared for publication in Tier-1 scientific journals (e.g., *Nature*, *Science*), satisfying peer-review editorial policies regarding ethical oversight without violating federal regulations.