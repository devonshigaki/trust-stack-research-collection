# Sim F1a2 — Pre-registration (FROZEN 2026-09-12, before any F1a2 conditioning data)
Governs the re-operationalized circuit-scale conditioning test. Extends
SIM_F1_PRE_REGISTRATION.md and SIM_F1_DESIGN_ADDENDUM_A.md. All plasticity
constants, protocol phases, thresholds, and criteria forms are UNCHANGED from
Addendum A unless an explicit amendment is frozen here. Nothing below was
chosen after seeing conditioning data; pilot measurements used to fix the
instrument are disclosed verbatim in §2.

## 1. Status of F1a
- Reference gate (whole-brain v783, Shiu-model default parameters): **PASS** —
  repo sugar-GRN drive (20/21 IDs present in v783) → MN9 (720575940660219265)
  fired 86/73/82/86 spikes per 1 s trial (n_run=4); frozen shuffled-connectivity
  control (partners permuted, weights preserved, seed 42): 0/0/0/0;
  supplementary random-drive descriptive control: 0/0/0/0.
- F1a conditioning battery: **INDETERMINATE (instrument)** — the frozen CS
  operationalization (ORN_DL3 drive, n=79, default r_poi/w_syn) evokes ZERO
  Kenyon-cell spikes and ZERO MBON spikes in the frozen circuit subgraph, so
  B0 = 0 and every R-based criterion is undefined. No criterion was violated;
  none could be evaluated. Diagnosis (layer-resolved, recorded in
  f1a_instrument_diagnosis.txt): ORN→PN propagates (10/10 DL3 PNs fire),
  PN→KC fails for a single glomerulus; KC→MBON and full-PN→KC→MBON stages
  work. This is a property of the published model's weight calibration
  (validated on strong multi-channel SEZ drives), not of the DOCAS overlay.

## 2. Disclosed pilots (used to fix the instrument; all numbers recorded)
- Pilot A — drive the 20 DL3-receiving uniPNs directly, 150 Hz, 1 s:
  62/5,177 KCs active (mean 0.0 Hz), 0/96 MBONs → still no baseline.
- Pilot B — drive all 264 uniglomerular PNs, 150 Hz, 1 s:
  3,610/5,177 KCs active (mean 21.6 Hz), 63/96 MBONs active (mean 70.3 Hz)
  → measurable baseline. Chosen as the F1a2 CS.
- Pilot C — drive 20 repo sugar GRNs (frozen appetitive US): 0/43 OA,
  0/307 PAM → frozen appetitive routing fails inside the frozen subgraph
  (SEZ relay neurons are outside the Addendum-A population set; the path is
  physically cut).
- Pilot D — drive all 43 OA neurons directly, 150 Hz, 1 s: 0/307 PAM.
  OA→PAM edges exist (n=50, all excitatory-signed) but mean connectivity is
  1.06 synapses — physiologically negligible at the frozen w_syn = 0.275 mV.
- Sign census (recorded): KC→MBON 62,261/62,261 excitatory; PPL1→MBON 281
  excitatory; PPL1→KC 10,720 excitatory; PAM→MBON 1,709 excitatory;
  sugar→OA 3 excitatory; OA→PAM 50 excitatory.

## 3. Frozen amendments to the operationalization (only these)
- **CS**: drive all 264 uniglomerular PNs (`_adPN|_lPN`, Addendum-A set) at
  the default 150 Hz. Functionally a strong broad-spectrum odor; the single
  CS used throughout. ORN stage bypassed because pilot A shows even direct
  single-glomerulus PN drive yields no MBON baseline.
- **Appetitive US**: drive all 307 PAM neurons directly at 150 Hz (symmetric
  to the aversive PPL1 drive). The Addendum-A routing (sugar→SEZ→OA→PAM)
  cannot carry drive to PAM in this substrate (pilots C, D); this is an
  instrument limitation, recorded as such.
- **Aversive US**: unchanged (drive all 16 PPL1 at 150 Hz).
- Arms (n_run = 4 each; n_run for arms was unspecified in Addendum A and is
  frozen here to match the gate): intact-aversive, D-ablated aversive
  (eta = 0), S-ablated aversive (tau_S = 3), shuffle aversive (within-circuit
  partner permutation, weights preserved, seed 42), intact-appetitive,
  OA-ablated appetitive (OA outputs zeroed).

## 4. Frozen scoring of criteria (thresholds unchanged from Addendum A)
- (1) intact-aversive acquisition: Spearman rho(trial, R) <= -0.8 AND
  R_final <= 0.70. Aggregation (locked): run-mean curve primary; per-run
  curves reported.
- (2) D-ablation: R_final > 0.95.
- (3a) intact-appetitive acquisition: same numeric form as (1).
- (3b) OA-dissociation leg: **INDETERMINATE (instrument) by construction** —
  with the PAM-direct appetitive US, silencing OA cannot abolish acquisition,
  so the Addendum-A dissociation question is not evaluable in this substrate.
  The OA-ablated arm is still run and its curve reported; the leg is scored
  INDETERMINATE, never silently dropped. Deferred to a whole-brain/SEZ-intact
  substrate (F1b).
- (4) S-ablation recovery: Addendum-A form assumes both arms recover inside
  the 8-probe extinction window. Frozen contingency: if intact recovery to
  R >= 0.90 is right-censored at 8 probes (expected: tau_S = 12 implies
  ~26-probe recovery), criterion (4) is scored PASS iff the S-ablated arm
  reaches R >= 0.90 within the 8-probe window AND the intact arm has not
  reached R >= 0.90 within the same window (the directional dissociation the
  criterion operationalizes); FAIL if S-ablated does not recover or recovers
  no faster than intact; the censoring is reported either way.
- (5) shuffle: R_final > 0.95. Frozen contingency: if the shuffled circuit
  yields B0 < 1 Hz (R undefined), criterion (5) is scored PASS-by-structure
  iff the shuffle arm's final-probe absolute MBON rate is <= 5% of the
  intact B0 AND its acquisition-probe sequence shows |Spearman rho| < 0.5
  vs trial index; otherwise FAIL.
- PASS = (1), (2), (3a), (4), (5) met. FAIL = any of them violated.
  (3b) INDETERMINATE is reported alongside and does not count as FAIL.
- Permitted paper action: NONE automatic (per SIM_F1_PRE_REGISTRATION.md).

## 5. Non-commercial note
FlyWire data are CC BY-NC 4.0: usable in the research papers, never in
FreshCredit commercial materials.
