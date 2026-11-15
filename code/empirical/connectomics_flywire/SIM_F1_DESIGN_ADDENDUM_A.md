# Sim F1 — Design Addendum A (operationalization; FROZEN 2026-09-12 before any
# experimental run; extends SIM_F1_PRE_REGISTRATION.md, which governs)

## Graph & annotations
- Connectivity: FlyWire FAFB v783 (`Connectivity_783.parquet`, shipped with
  philshiu/Drosophila_brain_model); roster `Completeness_783.csv`
  (138,639 neurons).
- Annotations: Schlegel et al. 2024 Supplemental_file1 (v783 root IDs).

## Populations (selection rules frozen here, applied programmatically)
- CS drive: all neurons cell_type == ORN_DL3 (n=79; odor channel, both
  antennae). Signal propagates through AL PNs to Kenyon cells.
- Aversive US: all cell_type matching ^PPL1 (n=16).
- Appetitive US: sugar GRN set = the 21 published repo IDs (Shiu et al.
  model repo), of which 20 annotate as LB3 gustatory sensory neurons (left)
  in v783; drive propagates SEZ -> OA -> PAM.
- OA relay: cell_type matching ^OA- (n=43).
- Circuit neurons (simulated): ORN_DL3 + all uniglomerular PNs (cell_type
  matching `_adPN|_lPN`, n=264) + cell_class=='Kenyon cell' (n=5,177) +
  ^MBON (n=96) + ^PPL1 + ^PAM (n=307) + ^OA- + APL + DPM (n=2+2).
  Induced subgraph: all v783 edges within this set.

## Plasticity overlay (the only addition; per pre-registration)
- Plastic synapses: all KC -> MBON synapses.
- Eligibility: KC spiked during CS window.
- Trigger: mean rate of the relevant DAN population during the pairing window
  exceeds frozen threshold theta = 20 Hz (aversive: PPL1; appetitive: PAM).
- Update per pairing trial: w <- w * (1 - eta), eta = 0.25 (frozen).
- Retention (S channel): between CS-only probes, w recovers toward baseline
  w0: w <- w + (w0 - w)/tau_S, tau_S = 12 probes (frozen); S-ablation: tau_S = 3.
- D-ablation: eta = 0. OA-ablation: OA neurons silenced (syn weights out = 0),
  so sugar drive cannot reach PAM (tests US routing + dissociation).
- Shuffle control: within-circuit connectivity randomly permuted (weights
  preserved, partners permuted; fixed seed 42).

## Protocol (frozen)
- Probe = 1.0 s CS-only trial; readout = mean spike rate of all 96 MBONs
  during the final 700 ms.
- Baseline: 3 probes (mean = B0).
- Acquisition: 12 pairing trials (CS 900 ms; US co-drive during final 700 ms),
  probe after trials 1,2,3,4,6,8,10,12 (8 probes).
- Extinction: 8 consecutive probes with leak applied between.
- Arms: (i) intact-aversive; (ii) D-ablated aversive; (iii) intact-appetitive;
  (iv) OA-ablated appetitive; (v) shuffle intact-aversive.

## Operationalized frozen criteria (mapping to pre-registration 1-5)
Let R_k = probe response as fraction of B0.
  (1) acquisition: Spearman rho(trial, R) <= -0.8 AND R_final <= 0.70.
  (2) D-ablation: R_final > 0.95 (no acquisition).
  (3) OA-ablation: appetitive R_final > 0.95 AND intact aversive passes (1).
  (4) S-ablation: recovery to R >= 0.90 in <= half the probes required by the
      intact arm.
  (5) shuffle: R_final > 0.95.
PASS = (1)-(5) all met. FAIL = any of (1)-(3) or (5) violated, or intact
indistinguishable from shuffle. INDETERMINATE = reference gate fails.

## Reference gate (per pre-registration; implementation detail frozen here)
Whole-brain v783 graph; drive = 21-ID sugar set at default 150 Hz; measure
firing of repo MN9 ID 720575940660219265 (annotated in v783 as CB0701,
brain_motor_neuron, right side — annotation discrepancy recorded here; the ID
is the published reproduction target); control = shuffled connectivity.
Gate PASSES if the neuron fires under drive and is silent/near-silent under
shuffle. n_run = 4 per condition (2-core sandbox budget; documented here).
