# OSF Deposit Package — The Trust Stack Research Collection (Repair-Era Audit Surface)

This package is the repair-era audit surface for the trust research collection: *The Value of Trust* (preface), *GTT* (theory), *DOCAS* (neurochemical framework), *TFP* (protocol), and the *FreshCredit* whitepaper (application). It contains the technical appendix (math repairs, simulation briefs, neural-pipeline run reports, frozen numbers files), all simulation and analysis figures, the simulation and neural-pipeline code produced in this workflow, and four pre-registration documents (one complete registered protocol, three skeleton drafts ready to file).

It is designed to be uploaded to OSF per the companion **OSF_GUIDE.md** (included at this root), using the post-phaseout surfaces: Research Materials for files, Registries for the pre-registrations, Preprints for the papers.

## New since the original upload

Everything below was produced after the first deposit and is included here in full:

- **Sim D14** (AlphaGenome variant battery, DOCAS) and **Sim D15** — complete packages (registrations, data, code, results). AlphaGenome outputs appear in research materials only.
- **S-channel descriptive note** + paired figure.
- **F1 series** (`simf1_work/`) — pre-registered connectome simulations on FlyWire v783 (*Drosophila* mushroom body). Verdicts: reference gate **PASS**; F1a **INDETERMINATE** (instrument); F1a2 **FAIL** (control-shuffle criterion: position-based 0.873, class-faithful 0.680, vs frozen > 0.95); F1b compartment-resolved DAN gating **PASS (7/7 as frozen; criteria 6–7 met at a floor-saturation calibration artifact, evidential weight on 1–5)**. Reference measurement: Kenyon cells supply 98.2% of the MBON input budget. Reported in the DOCAS paper (F1-series subsection) and summarized in the collection index.
- **Simulation H1** (`simh1_work/`) — pre-registered cross-species replication on MICrONS mouse cortex (`minnie65_public` materialization 1822). Verdicts: H1-A structural dominance **FAIL** (median 0.313 vs 0.50 criterion); A2 availability-tracking **MET** (8/11 classes); H1-B dynamical permutation robustness **MET** (R_perm = 1.340 ≥ 0.50, gate 4/4). **Compound verdict FAIL** — global partner permutation fails to abolish function in both species, on different metrics and criteria (the fly's abolition index vs. a cortical throughput ratio), not a matched quantitative replication; the single-class structural basis does not transfer. Reported in the DOCAS paper (§5.7, Figure 25).
- **Simulation H01** (human cortex) — pre-registered under the same frozen criteria; **in progress** at deposit time. Raw H01 shard parts are withheld from this package (see `simh1_work/H01_PARTS_WITHHELD.md`); the worker state and aggregation code are included.
- **Sim G6-M1 manifold render** — the GTT "trust manifold" (Sim G6-M1, §3.6) rendered from an **independent re-implementation** (seed 20260908, 60 uniform-random initial conditions on Δ⁴, discrete law λ = 0.35 planted): `technical-appendix/sim-code/g6_m1_manifold_figure.py`, `technical-appendix/numbers/g6_m1_reimplementation_results.json`, and three figures in `figures/gtt/` (wide 2-panel, column version printed in GTT as Figure SR5, self-contained interactive HTML). The structural claim replicates in full — every trajectory inside the d < 0.05 band, mean distance 0.288 → 0.013 at step 7, dispersion ratio 0.047 (95% bootstrap CI [0.0447, 0.0473]) vs the printed 0.295 → 0.016, ratio 0.053 [0.0475, 0.0594]. The re-implementation shows the printed absolute distances to be on the √θ-sphere **chord (Hellinger) convention**; the Fisher–Rao arc is a monotone reparameterization and the dispersion ratio is near-identical under either. **Pending bit-identity against the original `simulations/` battery** (uploaded separately).
- **Sim G22 reality-monitoring battery** — pre-registered frozen criteria (C1–C6) before data; source-mixing model (Dijkstra & Fleming 2023 formalism) grafted onto the G6-M1 trust-stage dynamics (seed 20260913; 60 ICs on Δ⁴; λ = 0.35 planted; Hellinger-chord distances): `technical-appendix/SIM_G22_PRE_REGISTRATION.md`, `technical-appendix/SIM_G22_CLOSURE.md`, `technical-appendix/sim-code/g22_reality_monitoring.py`, `technical-appendix/numbers/g22_results.json`, the disclosed `g22_firstrun_bug.json` audit artifact, and two figures in `figures/gtt/` (wide 2-panel; column version printed in GTT as Figure SR6). Verdicts: C1–C4, C6 **PASS**; C5 **FAIL** (aggregation attenuates ≈2.9× but does not restore the convergence band; shared expectations — the formalized collective illusion — collapse the rescue); **compound FAIL, reported**. The C1 instrument gate caught a first-run off-manifold implementation fault; the buggy run is preserved and disclosed, the frozen spec was not altered. Reported in GTT §4.6 (Figure SR6) and the collection index.

## Folder map

```
osf_deposit/
├── README.md                        ← this file
├── OSF_GUIDE.md                     ← step-by-step deposit instructions (copy for convenience)
├── preregistrations/
│   ├── DOCAS-GATE-1.md              ← COMPLETE registered protocol: pharmacological-perturbation
│   │                                  gate for the DOCAS exact-form claim + independent-rater
│   │                                  protocol for CLICS concept sets / offer-stimulus categories
│   │                                  (source: CARRIER_GATE.md, retitled, content unchanged)
│   ├── GTT-EMPIRICAL-PROGRAM.md     ← skeleton draft from GTT §6: λ estimation, R1, H2 corridor
│   │                                  [0.46, 0.76] around target μ_λ = 0.61, H0a lumpability,
│   │                                  H3 Kuramoto-form threshold, H4 observer effect, model
│   │                                  comparison vs. Behrens-style adaptive-λ rival
│   ├── TFP-PILOT.md                 ← skeleton draft from TFP §1.4/§5: H0/H1 three legs
│   │                                  (coupling→coherence, leakage→decoherence, edge cost),
│   │                                  fragility band ℓ* ∈ [0.02, 0.10] honest null
│   └── WHITEPAPER-EVAL.md           ← skeleton draft from whitepaper §4 (+§3.4/§4.7): concordance
│                                      pilot P1–P3 (Mantel/partial Mantel), harm/benefit ledger
│                                      endpoints (NNH ≈ 1.03 at 1% prevalence; NNT 19–52; NNE 3.7–5)
├── technical-appendix/
│   ├── math_repairs.md              ← the math repair log (M1–M7) the papers were patched against
│   ├── sim_results_A.md             ← Sim-Battery A brief: long-run laws, cold start, breach
│   │                                  expected-loss, Sybil cost (fig1–fig5)
│   ├── sim_results_B.md             ← Sim-Battery B brief: leakage-graded Kuramoto H1 test,
│   │                                  closed-loop λ battery, ψ-OU battery, phase-map artifact
│   │                                  control (figB1–figB4)
│   ├── sim-code/                    ← ALL simulation code produced in this workflow
│   │   ├── robustness/              ← SIM-R1/SIM-R2 batteries: simR1_battery1.py (adaptive-λ
│   │   │                              misspecification arm), simR1_battery1_figs.py,
│   │   │                              simR1_battery2.py (closure-sensitivity scan),
│   │   │                              b3_ahat.py (â_i Fisher–Rao sensitivity),
│   │   │                              b4_kuramoto.py (sparse/weighted-network Kuramoto)
│   │   │   ├── tfp/sim_p1_p1b.py        ← TFP Sim P1/P1b leakage-graded coherence
│   │   ├── g6_m1_manifold_figure.py ← G6-M1 manifold render: independent re-implementation
│   │                                  (seed 20260908, 60 ICs on Δ⁴, λ = 0.35 planted) +
│   │                                  figure generation; status: pending bit-identity
│   └── g22_reality_monitoring.py  ← Sim G22 reality-monitoring battery (seed 20260913,
│                                       frozen criteria C1–C6; arms 0/A/B/C/D) per
│                                       SIM_G22_PRE_REGISTRATION.md / SIM_G22_CLOSURE.md
│   ├── SIM_D14_PRE_REGISTRATION.md / simD14/ / SIM_D14_variant_list.csv / simD14_score.py
│   │                                ← Sim D14 (DOCAS AlphaGenome variant battery): complete
│   │                                  package — pre-registration, variant list, scoring code,
│   │                                  results
│   ├── SIM_D15_PRE_REGISTRATION.md / simD15/
│   │                                ← Sim D15 (DOCAS follow-up): complete package
│   ├── SIM_F1_PRE_REGISTRATION.md   ← F1-series registration (top-level copy)
│   ├── SIM_G22_PRE_REGISTRATION.md / SIM_G22_CLOSURE.md
│   │                                ← Sim G22 (GTT reality-monitoring battery): frozen
│   │                                  criteria C1–C6 registered before data; closure with
│   │                                  full audit trail incl. the preserved first-run bug
│   │                                  (C1–C4, C6 PASS; C5 FAIL; compound FAIL)
│   ├── S_CHANNEL_DESCRIPTIVE_NOTE.md← S-channel descriptive note (paired figure in figures/)
│   ├── simf1_work/                  ← F1 SERIES (FlyWire v783 Drosophila mushroom body):
│   │                                  complete working archive — registrations (F1, F1a2 +
│   │                                  Amendment 1, F1b), design addendum A, closures
│   │                                  (SIM_F1_CLOSURE.md, SIM_F1B_CLOSURE.md), final
│   │                                  evaluation JSONs (gate, f1a2, f1b), probe readout CSVs,
│   │                                  run logs, all run code, sha256 file manifest.
│   │                                  Verdicts: gate PASS; F1a INDETERMINATE-instrument;
│   │                                  F1a2 FAIL (control-shuffle criterion 5: 0.873 / 0.680
│   │                                  vs > 0.95); F1b PASS (7/7 as frozen, 6–7 at floor-saturation
│   │                                  artifact). FlyWire data CC BY-NC 4.0.
│   └── simh1_work/                  ← SIMULATION H1 (MICrONS mouse cortex, minnie65_public
│                                      materialization 1822): complete working archive —
│                                      registration, four disclosed amendments
│                                      (SIM_H1_AMENDMENTS.md), closure (SIM_H1_CLOSURE.md),
│                                      H1-A/H1-B result JSONs, frozen seed-45 sample,
│                                      rebuilt cell-type map + superseded artifact retained,
│                                      pull/eval/sim code, H01 human-replication worker state
│                                      (H01 raw shard parts withheld; see H01_PARTS_WITHHELD.md),
│                                      sha256 manifest (297 entries). Verdict: compound FAIL
│                                      (A1 FAIL median dominance 0.313; A2 MET 8/11; B2 MET
│                                      R_perm = 1.340).
│   ├── neural-pipeline/
│   │   ├── RUN_REPORT.md            ← TRIBE v2 real-checkpoint run (byte-exact, bit-exact
│   │   │                              determinism; 27-stimulus battery leg 1)
│   │   ├── RUN_REPORT_2.md          ← round-2 report: Gallant eng1000 decode (real Huth model),
│   │   │                              vec2vec bridge (real v1.0.0 release), CLICS overlap
│   │   ├── BRIDGE_REPORT.md         ← LLaMA↔eng1000 bridge results
│   │   └── code/                    ← the full neural-pipeline code set (llama_stream.py,
│   │                                  run_pipeline.py, run_battery27.py, gallant_decode.py,
│   │                                  vec2vec_demo.py, clics_offer_overlap.py, make_figs*.py,
│   │                                  chunk_dl.py, config.yaml, stimuli.json) plus:
│   │       battery27_reconstructed.py / .json   ← RECONSTRUCTION-FROM-SPEC, LABELED:
│   │                                  "reconstruction-from-spec, pending bit-identity vs
│   │                                  battery27_manifest.json". Item-1 texts verbatim from the
│   │                                  Master Reproduction Manifest; items 2–5 faithful to the
│   │                                  stated design. Do NOT report original headline numbers
│   │                                  from this reconstruction.
│   └── numbers/                     ← frozen numbers files backing the papers' printed values
│       ├── numbers_gtt.md
│       ├── numbers_docas.md
│       ├── numbers_tfp.md
│       ├── numbers_whitepaper.md
│       ├── g6_m1_reimplementation_results.json  ← G6-M1 re-implementation vs printed values
│       │                                        (chord-vs-arc convention check, bootstrap CI)
│       ├── g22_results.json                 ← Sim G22 repaired-run results (arm grid, CIs,
│       │                                        verdicts per frozen criteria)
│       └── g22_firstrun_bug.json            ← disclosed audit artifact: the off-manifold
│                                               first run the C1 instrument gate caught
│                                               (spec unchanged; code repaired to spec)
└── figures/                         ← all figures, subfolder structure preserved
    ├── fig1_trajectories.png … fig5_sybil.png          (Sim-Battery A, sims root)
    ├── figB1_R_surface.png … figB4_psi_battery.png     (Sim-Battery B, sims root)
    ├── gtt/                       (14 files: convergence, spectral, heavy-tail, long-run,
    │                              λ/ψ batteries, Kuramoto threshold, phase-map control, numbers,
    │                              G6-M1 manifold renders — wide 2-panel, column (GTT Figure SR5),
    │                              interactive HTML — plus G22 reality-monitoring renders,
    │                              wide 2-panel and column (GTT Figure SR6))
    ├── docas/                     (12 files: surface means, contrasts, parcels, Yeo-7 networks,
    │                              similarity, GFP, figD series)
    │   └── pipeline/              (9 files: round-N/bridge figures — category contrasts,
    │                              separability, decode bars, CLICS heatmap, bridge a–d)
    ├── tfp/                       (11 files: coherence, R surface, transfer entropy, Sybil
    │                              deterrence, adoption, cold start, expected loss, storage refit)
    ├── whitepaper/                (8 files: estimator validation, PPV/base-rate, cold start,
    │                              adoption compounding, cost accounting, NNH harm, R surface)
    ├── robustness/                (SIM-R1/R2 figures + scripts + results JSONs/MDs)
    ├── arch/                      (architecture diagrams for TFP/whitepaper + captions.md)
    ├── figF1_series_verdicts.png  (F1-series verdict figure, printed in DOCAS)
    └── figH1_microns_budget.png   (Simulation H1 verdict figure, printed in DOCAS as Figure 25)
```

## Relationship to the author's original `simulations/` folder

**This package does not contain, and does not replace, the author's original `simulations/` folder** (the original scripts, result JSONs, `run_full_pipeline.sh`, `battery27_manifest.json`, `sim13_manifest.json`, `concepts.json`, `clics_dist.npy`, and the `*_firstrun_bug.json` audit-trail files). The author uploads that folder **separately and unchanged** — it is the material for the **bit-identity acceptance test**: once uploaded, every number in this repair-era package and in the papers can be checked bit-for-bit against the original shipped JSONs.

Everything here is a *re-implementation / re-run* of the same designs (all seeded), produced during the repair workflow, plus new repair studies the originals did not contain. Where original generative settings were not archived, exact-value deviations are expected, were measured, and were patched into the papers (see the deviation register in `SIMULATION_ACCOUNTING.md`, companion output). Reconstructed artifacts carry explicit labels — most importantly `battery27_reconstructed.{py,json}`: **reconstruction-from-spec, pending bit-identity vs `battery27_manifest.json`**.

## Reconstruction labels (read before citing numbers)

- `technical-appendix/neural-pipeline/code/battery27_reconstructed.{py,json}` — 27-stimulus battery reconstructed from the Master Reproduction Manifest spec (item-1 texts verbatim; items 2–5 and CONTROL_2 faithful reconstructions; amount-crossing order a reconstruction choice). **Pending bit-identity check against `simulations/battery27_manifest.json` (not yet uploaded). Do not report original headline numbers from this reconstruction.**
- The category-decode results from the reconstruction battery (LOO 1.000) are flagged in the papers as lexically driven (semantic-only control also 1.000) and explicitly *not* the original 0.40; the paraphrase-controlled arm (Sim D8, original battery) is the load-bearing result.
- Sim 12's spiking replication used a disclosed numpy three-factor stand-in (Brian2 unavailable); the real spiking version can be run on request.

## License

- **Documents** (all Markdown, figures, and reports in this package): **CC-BY 4.0**.
- **Code** (all `.py` files): **Apache-2.0**.
- Third-party materials referenced but not included (TRIBE v2 checkpoint, Huth eng1000 model, vec2vec release, CLICS4 data) retain their own licenses; see the run reports for provenance.
- **Data-use terms applying to derived artifacts in this package:** `simf1_work/` contains artifacts derived from the FlyWire connectome (**CC BY-NC 4.0** — non-commercial use only); these materials are part of non-commercial research outputs and must not be reused in commercial materials. `simh1_work/` contains artifacts derived from the MICrONS `minnie65_public` release (used under its public-data terms; attribution: MICrONS Consortium, materialization 1822). H01 human-connectome derived data are withheld from this package pending the replication's completion (CC BY 4.0 with attribution once deposited).

## The "deposit replaces the self-attestation caveat" note

The papers currently carry the honesty sentence that, until the OSF deposits exist, all pre-registration and frozen-criteria claims are **self-attested**. This package — once uploaded and timestamped on OSF, and once the registrations in `preregistrations/` plus the seven simulation pre-registrations (D14, D15, F1, F1a2, F1b, H1, G22) are filed in OSF Registries (each yields a DOI) — is what retires that caveat. After deposit, the DOIs replace the `deposited at OSF (DOI: [insert])` placeholders in the papers (33 occurrences across the collection, including two brace-wrapped heading variants), and the self-attestation sentence is removed because it is no longer true. Until those steps are completed, the caveat stands.
