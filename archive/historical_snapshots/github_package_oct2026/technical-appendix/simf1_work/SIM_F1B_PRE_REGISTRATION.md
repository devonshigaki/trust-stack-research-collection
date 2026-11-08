# Sim F1b — Pre-registration (FROZEN 2026-09-12, before any F1b conditioning data)
Extends SIM_F1_PRE_REGISTRATION.md, SIM_F1_DESIGN_ADDENDUM_A.md, and
SIM_F1A2_PRE_REGISTRATION.md. Motivation: F1a2 FAILED frozen criterion (5)
(scrambled circuits partially acquire because the KC class dominates the MBON
input budget), indicating the missing ingredient is compartment-resolved
dopaminergic gating — the structure real flies use (Aso et al. 2014; Hige et
al. 2015; Li et al. 2020). F1b tests that refinement. All plasticity
constants, protocol phases, thresholds, and aggregation rules are UNCHANGED
from F1a2 unless an explicit amendment is frozen here.

## 1. Substrate (unchanged)
Frozen v783 circuit subgraph: 6,006 neurons, 555,325 edges, populations per
Design Addendum A. Plasticity constants: eta = 0.25, theta = 20 Hz,
tau_S = 12 (S-ablation 3). Protocol: 3 baseline probes; 12 acquisition trials
(200 ms CS + 700 ms CS+US), probes after trials 1,2,3,4,6,8,10,12; 8
extinction probes with leak between; n_run = 4 per arm; run-mean curve primary,
per-run reported (aggregation locked, unchanged).

## 2. Compartment map (literature-verified, sources cited; the only new element)
PPL1 cluster innervates the alpha' lobe, alpha lobe compartments 2 and 3, and
gamma lobe compartments 1 and 2 (Li et al. 2020, eLife 10:e62576, Fig. 6).
MBON dendritic compartments per Aso et al. 2014 (eLife 3:e04577, Table 1),
Li et al. 2020 (Figs. 7-8), and VFB FBbt_00049113 (MBON23 = MBON-alpha2sp).
- Conditioned-aversive set M*_av (41 cells, 15 types; holds 23,492 = 37.7% of
  the circuit's KC->MBON edges): MBON11 (gamma1pedc), 12 (gamma2alpha'1),
  13 (alpha'2), 14 (alpha3), 15 + 15-like (alpha'1), 16 (alpha'3ap),
  17 + 17-like (alpha'3m), 18 (alpha2sc), 19 (alpha2p3p), 20 (gamma1gamma2),
  23 (alpha2sp), 31 (alpha'1), 32 (gamma2).
- EXCLUDED as mixed-compartment (dendrites span PPL1 and non-PPL1
  compartments): MBON30 (gamma1gamma2gamma3), MBON33 (gamma2gamma3).
- EXCLUDED as ambiguous/unverified: MBON25, MBON28, MBON35, MBON34 (gamma2,
  but FlyWire annotation merges it with MBON25), the "MBON25,MBON34" group.
  These sit in the non-conditioned readout. Conservative direction: exclusion
  can only weaken measured compartmentalization, never inflate it.
- Conditioned-appetitive set M*_app: MBON07 (alpha1; 4 cells; 3,719 = 6.0% of
  KC->MBON edges) — the canonical PAM-alpha1 -> MBON-alpha1 appetitive
  compartment (Aso et al. 2014; Ichinose et al. 2015; Yamagata et al. 2015).
- Non-conditioned readout: the remaining 51 MBON cells.

## 3. Amendments vs F1a2 (only these)
- Plastic set = KC->MBON edges whose postsynaptic MBON is in the triggered
  cluster's compartment set (M*_av for PPL1 drive; M*_app for PAM drive).
- Readouts per probe: R_cond = conditioned-set rate / B0_cond and
  R_noncond = non-conditioned-set rate / B0_noncond (B0 from 3 baseline probes).
- New control arm (gate-map shuffle): plastic targets re-routed to
  KC->M' edges, M' = |M*| non-conditioned MBON cells (disjoint from M*),
  seed 43 (aversive) / 44 (appetitive). Trigger, eligibility, constants
  unchanged. This isolates the gating MAP — the topology test appropriate to
  a gating theory.
- Arms (7): intact_av, D_abl (eta=0), S_abl (tau_S=3), gateshuf_av,
  partnershuf_av (partner permutation seed 42; plastic = KC->M*_av edges of
  the permuted graph per Amendment 1 class-faithful reading; DESCRIPTIVE
  attenuation report only, no PASS leg — the absolute partner-permutation
  form was settled FAIL in F1a2 and is not re-litigated), intact_app,
  gateshuf_app.

## 4. Frozen criteria (thresholds unchanged in form from F1a2)
- (1) intact_av acquisition: Spearman rho(trial, R_cond) <= -0.8 AND
  R_cond_final <= 0.70.
- (2) compartment specificity: R_noncond_final > 0.95 (intact_av).
- (3) D-ablation: R_cond_final > 0.95.
- (4) S-ablation: R_cond recovers >= 0.90 within the 8-probe extinction
  window AND intact_av has not recovered >= 0.90 in-window (frozen
  contingency, same as F1a2).
- (5) gate-map shuffle (aversive): R_cond_final > 0.95.
- (6) intact_app acquisition: rho <= -0.8 AND R_cond_final <= 0.70.
- (7) gate-map shuffle (appetitive): R_cond_final > 0.95.
PASS = (1)-(7) all met. FAIL = any violated. INDETERMINATE-instrument if any
readout baseline B0 < 1 Hz (disclosed pilot: B0_cond_av = 80.0 Hz, 28/41
active; B0_cond_app = 174.6 Hz, 4/4; B0_noncond = 64.7 Hz — all viable).
Permitted paper action: NONE automatic.

## 5. Whole-brain appetitive scoping probe (descriptive, completed before
freezing; recorded here)
Driving the 20 repo sugar GRNs at 150 Hz on the WHOLE-BRAIN v783 graph
recruits 0/43 OA, 0/307 PAM, 0/16 PPL1 neurons (and 0 KCs), while the same
drive robustly fires thoracic MN9 (F1 gate). In this model's calibration,
gustatory drive reaches sensorimotor arcs but not the dopaminergic
reinforcement system; the appetitive US therefore remains direct PAM drive,
and the OA-relay dissociation remains untestable in this substrate
(f1b_appetitive_probe.json).

## 6. Non-commercial note
FlyWire data are CC BY-NC 4.0: research use only; never in FreshCredit
commercial materials.
