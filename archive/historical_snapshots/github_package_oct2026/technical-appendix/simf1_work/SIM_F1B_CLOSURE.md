# Sim F1b — Closure (2026-09-12)
Registration: SIM_F1B_PRE_REGISTRATION.md (frozen before any F1b conditioning
data). Driver: run_f1b.py. Raw readouts: f1b_probe_readouts_set1.csv,
f1b_probe_readouts_set2.csv (7 arms × 4 runs × 19 probes each).
Evaluation: f1b_final_evaluation.json. Logs: f1b_set1.log, f1b_set2.log,
f1b_smoke.log.

## Verdict: PASS — 7/7 frozen criteria MET

| # | Criterion (frozen) | Result | Verdict |
|---|---|---|---|
| 1 | intact_av: rho ≤ −0.8 AND R_cond_final ≤ 0.70 | rho = −1.000; R_cond_final = 0.451 (per-run 0.442–0.464) | MET |
| 2 | specificity: R_noncond_final > 0.95 | 0.963 | MET |
| 3 | D_abl: R_cond_final > 0.95 | 0.990 | MET |
| 4 | S_abl recovers ≥0.90 within 8 ext probes AND intact does not | recovers at probe 4 (final 0.995); intact in-window max 0.817 | MET |
| 5 | gateshuf_av: R_cond_final > 0.95 | 1.119 | MET |
| 6 | intact_app: rho ≤ −0.8 AND R_cond_final ≤ 0.70 | rho = −0.994; R_cond_final = 0.000 | MET |
| 7 | gateshuf_app: R_cond_final > 0.95 | 0.996 | MET |

## Interpretation
1. **Compartment gating produces compartment-LOCALIZED learning.** With
   plasticity restricted to the literature-verified PPL1 compartment set,
   the conditioned MBON population falls to 0.451 of baseline while the
   51 non-conditioned MBONs stay at 0.963 — the localization F1a2's
   population-wide readout could not express.
2. **The gate map, not merely the cell classes, carries the effect.** The
   F1a2 FAIL showed partner-permuted circuits still acquire because KCs
   dominate MBON input by class. F1b's gate-map shuffle (same cells, same
   classes, plasticity re-routed to equally many random non-conditioned
   MBONs) abolishes acquisition on the conditioned compartment (1.119 av,
   0.996 app) — the conditioned readout is flat or slightly facilitated.
   A gating theory therefore needs the correct gating MAP, and this map —
   Aso 2014 / Li 2020 compartment assignments — is sufficient.
3. **Ablation dissociations preserved:** D-ablation blocks acquisition
   (0.990); S-ablation acquires normally then recovers fast (probe 4),
   while intact stays depressed (0.817 max in-window).
4. **Appetitive channel works through the PAM–MBON-α1 compartment.**
   MBON07 acquisition rho = −0.994. Honest calibration note: the curve
   saturates to the floor (R = 0.000) — all 3,719 KC→MBON07 edges are
   eligible, so η = 0.25 compounds to silence within ~6 trials. The frozen
   criterion is formally MET; the saturation is reported as a model
   calibration observation (single-compartment readout + full eligibility),
   not hidden.
5. **Descriptive (no PASS leg):** partner-shuffle with compartment gating
   still yields partial acquisition (0.681 vs intact 0.451 — attenuated
   ~2× relative to F1a2's 0.873 position-based shuffle but not abolished).
   KC-class dominance still carries partial acquisition under full partner
   permutation; the gate-map control is the appropriate topology test for
   a gating theory and it passes.

## What this closes and what it opens
- F1 series scientific arc: gate PASS → F1a INDETERMINATE-instrument
  (single-glomerulus drive below threshold) → F1a2 FAIL on topology
  specificity (criterion 5) → F1b PASS with compartment-resolved gating.
- The DOCAS channel overlay on the real v783 connectome now reproduces,
  with frozen criteria: robust acquisition, compartment localization,
  DAN-dependence, eligibility-trace persistence (S-ablation), and
  gate-map specificity, in both aversive (PPL1) and appetitive (PAM)
  channels.
- Open items for the paper's simulation appendix: (a) appetitive
  saturation calibration; (b) partner-permutation residual acquisition
  (class-dominance) — candidate refinement: KC->MBON weight heterogeneity
  or APL feedback; (c) gustatory->DAN reinforcement below threshold in
  this calibration (f1b_appetitive_probe.json) — OA-relay dissociation
  remains untestable in this substrate.
- Permitted paper action per registration: NONE automatic. All paper
  edits await explicit user instruction.
- Non-commercial note: FlyWire data CC BY-NC 4.0 — research use only;
  never in FreshCredit commercial materials.
