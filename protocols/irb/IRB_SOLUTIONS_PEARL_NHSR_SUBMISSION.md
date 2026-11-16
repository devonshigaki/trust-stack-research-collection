# Solutions / Pearl IRB: Not Human Subjects Research (NHSR) Determination Submission ($N = 1$ Self-Experimentation)

**Document ID:** `IRB_SOLUTIONS_PEARL_NHSR_SUBMISSION.md`  
**Target Boards:** Solutions IRB (`solutionsirb.com`) / Pearl IRB (`pearlirb.com`) / WCG IRB  
**Regulatory Basis:** 45 C.F.R. § 46.102(e) (Not Human Subjects Research / Sole-Investigator Self-Experimentation)  
**Sponsoring Organization:** FreshCredit Org (501(c)(3) Nonprofit Research Organization)  
**Study Window:** 180 Days / 6 Months Prospective (December 1, 2026 – May 30, 2027) + De-Identified Retrospective Archive  

---

## 1. Five Structural Rules Preserving NHSR Status

1. **Strict $N = 1$ Exclusivity:** The Principal Investigator is the sole observed individual. Future multi-participant validation ($N \ge 30$ Spoke cohort) is explicitly excluded and gated behind a separate prospective Full/Expedited IRB protocol prior to recruitment.
2. **Autonomous Lifestyle Choice (Zero Experimental Intervention):** Personal cessation of cannabis (and pre-Day-0 cessation of exogenous melatonin, with no GLP-1 RA initiation) is an autonomous lifestyle decision—not a protocol-assigned drug trial or clinical intervention.
3. **Zero Third-Party Subject Capture (`chat.db` & Solo-Room Enforcement):** Local messaging SQLite databases (`chat.db`) execute **100% locally** filtering `is_from_me = 1` and outputting only sender-side aggregate metrics (timestamps, word counts, response latency, lexical/sentiment scores) while **permanently stripping all third-party names, phone numbers, handles, and raw text**. Audio (`48 kHz`) and video tasks run strictly alone (`speaker_count == 1`; raw media purged post-feature extraction).
4. **FDA-Cleared & Consumer-Wellness Device Scope:** Every sensor is a commercial wellness device or FDA-cleared device used strictly within its OTC/clinical labeling (Dexcom CGM, Hilo/Aktiia BP). Venous blood draws (Quest) and CLIA cellular panels are standard outpatient wellness orders.
5. **De-Identified Retrospective Archive:** Historical archives belong solely to the investigator and are stripped of direct personal identifiers prior to analysis.


---

## 2. Copy-Paste Ready IRB Portal Summary

> **PROTOCOL TITLE:** Multimodal Longitudinal Dense Phenotyping of Autonomic, Neurovascular, Metabolic, and Financial Prediction-Error Dynamics ($N = 1$ Self-Experimentation Calibration Hub)  
> **SPONSORING ORGANIZATION:** FreshCredit Org (501(c)(3) Nonprofit Research Organization)  
> **PRINCIPAL INVESTIGATOR & SOLE PARTICIPANT:** Principal Investigator, FreshCredit Org  
> **STUDY DURATION:** 180 Days / 6 Months Prospective (December 1, 2026 – May 30, 2027) + De-Identified Retrospective Archive  
> **DETERMINATION REQUESTED:** Written Determination of **Not Human Subjects Research (NHSR) / Self-Experimentation** pursuant to **45 C.F.R. § 46.102(e)**.
>
> ### 1. Purpose & Scientific Background
> This $N = 1$ observational self-study establishes a high-resolution physiological and behavioral baseline ("The Fresh Protocol Hub") across 180 continuous days (Phase 1: Days 1–90 post-cessation physiological resynchronization [Dec 1, 2026 – Feb 28, 2027]; Phase 2: Days 91–180 clean steady-state baseline [Mar 1 – May 30, 2027]) to quantify coupling between objective financial prediction errors ($\varepsilon_t = V_t - E_t$) and autonomic, metabolic, neurovascular, and neuromotor dynamics, and to derive a minimal wrist-plus-ledger transfer function for a separate, future IRB-approved multi-participant study.
>
> ### 2. Study Population & Scope ($N = 1$ Exclusivity)
> $N = 1$. The Principal Investigator is the sole subject of observation. No external human participants will be recruited, enrolled, consented, or observed under this protocol. Any future multi-subject Spoke cohort ($N \ge 30$) will be submitted independently for prospective IRB review prior to enrollment.
>
> ### 3. Itemized Data Streams & Procedures (30 Streams)
> 1. **Consumer & FDA-Cleared Wearables / Home Sensors:** Apple Watch (PPG HR, HRV, $\mathrm{SpO}_2$, respiratory rate, sleep, ambient/headphone dB), Hilo/Aktiia cuffless BP (FDA-cleared), Dexcom CGM (FDA-cleared), Muse S Athena (EEG/fNIRS; worn overnight + weekly 5-min baseline; docked 5–7 AM & 5–7 PM), Airofit Pro (weekly pre-yoga MIP/MEP/VLC), Throne Science (passive Bristol/hydration), FITINDEX smart scale, Aranet4 ($\mathrm{CO}_2$, temp, RH, pressure), Philips Hue circadian lighting, and Logitech Circle overnight IR camera (solo bedroom boundary).
> 2. **Daily Behavioral, Cognitive & Solo Audio-Visual Tasks:** iPad cognitive battery (Creyos/PsyToolkit; 3 pre-Day-0 practice runs), wired USB Akai MPK Mini (CoreMIDI + 48 kHz onset sync, $\ge 30\text{–}45\text{ min}$ forearm rest post-pull-ups), standardized daily calisthenics/PPL/yoga/nutrition logs (11 MyFitnessPal Saved Meals, Write-Only HealthKit), Blue Yeti 48 kHz & Logitech Brio 4K feature-only check-in (solo closed room; raw media purged).
> 3. **De-Identified Digital, Environmental & Financial Logs:** Personal transaction ledgers ($\varepsilon_t$), itemized retail order history, Apple Music history, reading/journal logs, Screen Time/Notes/Calendar metadata, local sender-only messaging metadata (`chat.db` with third-party handles/text permanently stripped), and hourly local meteorological/photoperiod station data.
> 4. **Standard Outpatient Clinical & Biological Anchors:** Monthly fasted 8:00–8:30 AM Quest blood panels (Days 0, 30, 60, 90, 120, 150, 180; 72-hour Biotin/multi hold), CLIA-certified cellular semen analyses (Days 0, 90, 180; 48–72 h abstinence), Sequencing.com 30x WGS (air-gapped local NAS), de-identified historical outpatient EHRs, and Day 0 foil-wrapped root/tip virgin hair lock.
>
> ### 4. Privacy & Minimal-Risk Safeguards
> All devices operate strictly within labeled consumer/FDA parameters. Messaging, notes, and EHRs are processed locally on AES-256 encrypted storage (`FileVault` + `AES-256-GCM`) with all third-party identifiers and raw text/media permanently purged prior to statistical analysis. Strict record-only blinding is enforced through Month 6, with an independent clinical monitor overseeing out-of-band safety alerts.
>
> ### 5. Conclusion Requested
> FreshCredit Org requests a written determination that this $N = 1$ activity constitutes **Not Human Subjects Research (NHSR) / Self-Experimentation** under **45 C.F.R. § 46.102(e)**.

---

## 3. Pre-Launch Execution Checklist (Nov 16 – Nov 30, 2026)

1. Submit portal application to **Solutions IRB** (`solutionsirb.com`) or **Pearl IRB** (`pearlirb.com`) prior to **Nov 24**; attach PI CV and FreshCredit Org 501(c)(3) letter if requested.
2. Save signed determination letter locally (`IRB_NHSR_Determination_Nov2026.pdf`) and cite Protocol Reference Number inside frozen OSF Registration before **Dec 1, 2026**.
3. Complete **3 cognitive practice runs**, Day 0 baseline CLIA cellular panel (48–72 h abstinence), Day 0 fasted Quest draw (8:00–8:30 AM; 72 h Biotin hold), Nov 30 virgin hair lock (`ROOT`/`TIP` marked in foil), and `/retrospective_archive/` read-only lock.
