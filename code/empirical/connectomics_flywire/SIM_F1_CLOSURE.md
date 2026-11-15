# Sim F1 — CLOSURE (2026-09-12)
Governing documents: SIM_F1_PRE_REGISTRATION.md (frozen before data),
SIM_F1_DESIGN_ADDENDUM_A.md (frozen), SIM_F1A2_PRE_REGISTRATION.md (frozen
before F1a2 data), SIM_F1A2_AMENDMENT_1.md (frozen before shuffle-v2 data).

## Reference gate (whole-brain v783, Shiu et al. 2024 model, default params):
PASS
- Sugar-GRN drive (20/21 repo IDs present in v783) -> MN9 (720575940660219265)
  fired 86 / 73 / 82 / 86 spikes per 1 s trial (n_run = 4).
- Frozen control (partners permuted, weights preserved, seed 42):
  0 / 0 / 0 / 0. Supplementary random-drive control: 0 / 0 / 0 / 0.
- Files: gate_f1_results.json, gate_f1_shuffled_connectivity.json,
  gate_f1.log, gate_f1_control.log.

## F1a (frozen circuit battery): INDETERMINATE (instrument)
Frozen CS (ORN_DL3 drive @150 Hz) evokes zero KC and zero MBON spikes in the
frozen circuit subgraph -> B0 = 0 -> all R-based criteria undefined. No
criterion violated; none evaluable. Cause localized layer-by-layer
(f1a_instrument_diagnosis.txt): single-glomerulus drive (10 DL3 PNs) cannot
recruit KCs at the published default w_syn; the PN->KC->MBON chain itself
works under full-PN drive. Property of the published model calibration, not of
the DOCAS overlay. Gate PASS means F1 overall is NOT INDETERMINATE-by-gate.

## F1a2 (frozen amendments: CS = 264-uniPN drive; appetitive US = PAM-direct):
6 arms x n_run = 4 (+4 shuffle-v2 runs), run-mean curves (aggregation locked
before data):

| criterion | result | numbers |
|---|---|---|
| (1) intact-aversive acquisition | MET | rho = -1.000; R_final = 0.401 (need <= -0.8 and <= 0.70) |
| (2) D-ablation (eta = 0) | MET | R_final = 1.015, flat curve (need > 0.95) |
| (3a) intact-appetitive acquisition | MET | rho = -1.000; R_final = 0.399 |
| (3b) OA-dissociation | INDETERMINATE (instrument, pre-scored) | OA_abl R_final = 0.399 (PAM-direct US bypasses OA; OA->PAM mean 1.06 synapses cannot carry drive) |
| (4) S-ablation (tau_S = 3 vs 12) | MET (frozen contingency) | S_abl recovers R >= 0.90 at probe 5; intact censored (0.741 at probe 8 of 8) |
| (5) shuffle, position-based (as run) | NOT MET | R_final = 0.873, rho = -0.976 (need > 0.95) |
| (5) shuffle, class-faithful (Amendment 1) | NOT MET | R_final = 0.680 (need > 0.95) |

### VERDICT: F1a2 = FAIL on criterion (5) under both control readings.
(1), (2), (3a), (4) MET; (3b) INDETERMINATE-instrument. The as-run FAIL stands
on the record; Amendment 1's class-faithful control also fails the threshold.

## Interpretation (descriptive, not part of the frozen scoring)
- The DOCAS overlay on the real v783 connectome produces robust associative
  acquisition (R collapses to ~0.40 over 12 pairings), correct ablation
  dissociations (no acquisition without the dopamine trigger; fast recovery
  with a shortened retention horizon), for both aversive (PPL1) and
  appetitive (PAM) US channels.
- But acquisition is not strictly topology-specific at this operationalization:
  partner-permuted circuits still show partial acquisition (0.87 / 0.68),
  because KCs dominate the MBON input budget by class, and the frozen
  eligibility rule acts at class level. Intact topology acquires most
  (0.40), so topology modulates strength, but the frozen > 0.95 null-control
  threshold is not met.
- Biological reading: in real flies, associative specificity comes from
  compartment-specific DAN innervation of MBON lobes (Aso 2014; Hige 2015),
  which the frozen global-DAN trigger does not model. This is the concrete
  refinement target: F1b = compartment-resolved DAN gating on a whole-brain
  (SEZ-intact) substrate, which would also restore the OA appetitive
  dissociation leg. New pre-registration required before any F1b data.

## Resource/model notes for the record
- One repo sugar ID (of 21) absent from v783 roster; the present 20 were
  driven. Recorded here and in gate outputs.
- MN9 ID 720575940660219265 annotates as CB0701, brain_motor_neuron, right in
  v783 (Schlegel et al. 2024 file); the repo example targets it as MN9.
  Discrepancy recorded in Addendum A; the ID is the published target.
- Sandbox build note: pandas/parquet whole-brain load OOM-killed at 4 GB;
  replaced by streamed int32/float32 arrays (graph783.npz; prep_graph.py).
  Model mechanics, parameters, and equations unchanged from the repo.
- KC top_nt annotation reads 'dopamine' for 5,172/5,177 KCs in the Schlegel
  file (classifier artifact; KC->MBON edges are excitatory-signed in the
  connectivity table, which is what the model uses). Recorded.
- FlyWire data CC BY-NC 4.0: research use only; never in FreshCredit
  commercial materials.

## Permitted paper action
NONE automatic (per SIM_F1_PRE_REGISTRATION.md). No manuscript edits were
made from F1.
