# RUNBOOK — Reproducing every simulation locally

**You do not need to re-run anything to review this work.** All results ship
pre-computed in this repository (JSON/CSV/logs) exactly as reported in the
papers. This runbook is for reviewers who want to verify by re-execution.

## 0. Environment

Python 3.10+ recommended (3.12 used for the runs). Base install:

```bash
pip install -r requirements.txt        # numpy scipy matplotlib pandas pyarrow networkx
```

Heavier tiers need extra packages, listed per-simulation below. All random
seeds are fixed in the scripts; expect exact reproduction up to floating-point
and library-version jitter (documented where it matters).

**Runtime tiers:** Tier 1 = seconds–minutes, laptop. Tier 2 = minutes–hours.
Tier 3 = hours and/or external data/credentials.

---

## 1. GTT — theory simulations (`technical-appendix/sim-code/`)

| Sim | Script | Deps | Command | Expected output | Runtime |
|---|---|---|---|---|---|
| G6-M1 manifold re-implementation | `sim-code/g6_m1_manifold_figure.py` | numpy | `python3 g6_m1_manifold_figure.py` | `numbers/g6_m1_reimplementation_results.json` (60/60 replicas, d̄₀ = 0.284) | ~minutes |
| G22 reality monitoring | `sim-code/g22_reality_monitoring.py` | numpy | `python3 g22_reality_monitoring.py` | `numbers/g22_results.json` (arm A d25T 0.2754→0.1969→0.2290 across the μ_v grid; C1–C4,C6 PASS / C5 FAIL). Compare `numbers/g22_firstrun_bug.json` (preserved buggy first run) | ~minutes |

G1–G5, G7–G21 are fixed-reference verifications whose printed values are
re-derived in the papers' Supporting Document; the reference results are in
`technical-appendix/numbers/numbers_gtt.md`. Figures: `figures/gtt/`.

## 2. TFP — protocol simulations

| Sim | Script | Deps | Notes |
|---|---|---|---|
| P1 / P1b (Kuramoto coherence; leakage surface) | `sim-code/tfp/sim_p1_p1b.py` | numpy | Produces the P1 coherence readout (coupled R = 0.739 ± 0.029 vs isolated 0.040 ± 0.001, seed 42) and the P1b R(K, ℓ) surface. Figures `figures/tfp/figP1_coherence.png`, `figP1b_surface.png`. |
| P1c / P5 / P5b / P8 / P2 / P3 / P6 / P7 | **results-only this release** | — | Printed values, protocols, and criteria are in the TFP paper §§3.6–3.7 and `technical-appendix/numbers/numbers_tfp.md`; scripts under reconstruction for a later release. |

## 3. Robustness / whitepaper batteries (`figures/robustness/` = `technical-appendix/sim-code/robustness/`)

| Battery | Script | Deps | Expected output |
|---|---|---|---|
| SIM-R1 battery 1 (estimator misspecification) | `simR1_battery1.py` (+ `_figs.py`) | numpy, matplotlib | `simR1_battery1_stats.json`, `simR1_battery1_rows.npz`, `figR1_*.png` |
| SIM-R1 battery 2 (ringing/period recovery) | `simR1_battery2.py` | numpy, scipy, matplotlib | `simR1_battery2_stats.json` |
| B3 reference-scale sensitivity (â-hat) | `b3_ahat.py` | numpy, scipy, matplotlib | heatmap `figR2_B3_fr_ahat_heatmap.png` |
| B4 Kuramoto topologies | `b4_kuramoto.py` | numpy | `b4_results.json`, `figR2_B4_kuramoto_topologies.png` |

Result summaries: `figures/robustness/simR1_results.md`, `simR2_results.md`.

## 4. DOCAS — genetics (Tier 3: external APIs/credentials)

| Sim | Scripts | Requires |
|---|---|---|
| D14 (AlphaGenome variant scoring) | `simD14/run_d14.py`, `apply_frozen_rule.py`, `simD14_score.py` | `alphagenome` package + API key (**non-commercial use**); pre-computed rows in `simD14/*.csv` |
| D15 (GTEx brain eQTL scan) | `simD15/scan_gtex_tar.py`, `fetch_gtex_brain_eqtl.py`, `apply_frozen_rule_d15.py` | `pysam`, internet access to GTEx; pre-computed `simD15/*.csv` + SHA256 manifest |

## 5. DOCAS — F1 series, fly mushroom body (Tier 2–3)

Directory `technical-appendix/simf1_work/`. Requirements: `brian2`, `pandas`,
`pyarrow`, **and `model.py` from Shiu et al. (2024), `philshiu/Drosophila_brain_model`
(MIT)** — place it on the path (a frozen snapshot of the exact parameters used
is `simh1_work/shiu_model_default_params_snapshot.py`). Connectome data:
FlyWire v783 (`codex.flywire.ai`, CC BY-NC 4.0 — research use only).

Pipeline order (see `SIM_F1_PRE_REGISTRATION.md` for criteria):
1. `prep_graph.py` → circuit parquet
2. `build_circuit.py` → `circuit_f1_populations.json`
3. `gate_f1.py` / `gate_f1_control.py` → reference gate (`gate_f1_results.json`) — logs: `gate_f1*.log`
4. `pilots_f1a2.py`, `run_f1a.py`, `run_f1a2.py` → probe readouts (`f1a2_probe_readouts_set*.csv`), `f1a2_final_evaluation.json` (FAIL on frozen criterion, reported)
5. `run_shufflev2.py` → `f1a2_probe_readouts_shufflev2.csv`
6. `run_f1b.py` → `f1b_final_evaluation.json` (PASS 7/7 as frozen; criteria 6–7 floor-saturation artifact disclosed)
Verdict figure: `figures/figF1_series_verdicts.png`. Closures: `SIM_F1_CLOSURE.md`, `SIM_F1B_CLOSURE.md`.

## 6. DOCAS — H1 (MICrONS mouse cortex) and H01 (human, in progress)

Directory `technical-appendix/simh1_work/`.

- **H1-A** (structural budget): `microns_pull_lane*.py` (requires `caveclient` + a CAVE auth token; MICrONS v1822) → `h1a_evaluate_microns.py` → `h1a_results_microns.json` (A1 FAIL; A2 MET 8/11). Pre-computed batch pulls in `mparts/`.
- **H1-B** (dynamics): `run_h1b_sim_microns.py` (brian2 + model.py) → `h1b_results_microns.json` (R_perm = 1.3402). Verdict figure: `figures/figH1_microns_budget.png`. Closure/amendments: `SIM_H1_CLOSURE.md`, `SIM_H1_AMENDMENTS.md`.
- **H01** (human cortex, pre-registered, **in progress**): `h01_shell_lane.py`, `h01_aggregate_worker.py` (H01 dataset, CC BY 4.0; `fastavro`). Status: `h01_worker_status.json`. Withheld parts documented in `H01_PARTS_WITHHELD.md`.

## 7. DOCAS — neural pipeline (TRIBE v2 / 27-stimulus battery) (Tier 3)

`technical-appendix/neural-pipeline/`: requires `torch`, `transformers`,
`tribev2` weights (released TRIBE v2), Llama weights, `nilearn`, `nibabel`,
`h5py`, `scikit-learn`, plus CLICS data for `clics_offer_overlap.py`.
Reports: `RUN_REPORT.md`, `RUN_REPORT_2.md`, `BRIDGE_REPORT.md`. These runs
are GPU-scale and artifact-heavy; review the deposited outputs unless you
specifically need re-execution.

---

## Verification conventions

- Compare your re-run against the deposited JSON/CSV of the same name.
- Logs (`*.log`) are the ground truth of what actually executed.
- `*_firstrun_bug.json` files are preserved buggy first runs (audit trail) —
  do not "fix" the record by deleting them.
- SHA256 manifests: `simf1_work/SIM_F1_file_manifest_sha256.txt`,
  `simh1_work/SHA256_MANIFEST.json`, `simD15/SIM_D15_gtex_file_manifest_sha256.csv`.
