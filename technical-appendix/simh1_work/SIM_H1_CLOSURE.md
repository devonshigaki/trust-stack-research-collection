# Sim H1 — Closure (MICrONS primary test)

**Question (frozen 2026-09-12):** is class-level input-budget dominance
under partner permutation — the mechanism that produced F1a2's FAIL in the
fly mushroom body — also present in a mammalian cortical connectome?

**Verdict: FAIL on the frozen compound criterion** (PASS = A1 ∧ A2 ∧ B2).
A1 fails; A2 and B2 are met. No INDETERMINATE legs; nothing dropped.

Per the registration, FAIL is informative and is reported: the fly-MB
regime of extreme single-class budget dominance (KC share of the MBON
input budget = 0.9816, fly_mbon_budget.json) is **absent** in mouse
cortex — no presynaptic class supplies a majority of any postsynaptic
class's typed-neuron input budget (median dominant share 0.313). Yet the
dynamical robustness that dominance produced in the fly is still present
(B2: permutation *increases* readout throughput, R_perm = 1.34) — in
cortex it rests on a different structural basis: distributed budgets that
track availability, over dense convergence.

## 1. Substrate and amendments executed
- minnie65_public (MICrONS mouse visual cortex cubic millimeter),
  materialization **1822** (frozen), synapse table synapses_pni_2,
  class map aibs_metamodel_celltypes_v661 — rebuilt first-wins by
  ascending annotation id from the complete 94,014-row pull
  (Amendment 4; the earlier artifact map was irreconcilable with the
  v1822 table and was replaced before any criterion quantity was
  computed; blind preserved throughout).
- Frozen sampling rule: seed 45, n = 12,000 posts; **8,256** are
  v661-neuronal-typed at v1822 and entered evaluation (Amendment 4 §2b).
  Every class above the Amendment-1 minimum (k ≥ 8): 23P 2,193; 4P 1,677;
  6P-IT 1,351; 5P-IT 955; 6P-CT 732; BC 364; MC 292; 5P-ET 277;
  BPC 215; 5P-NP 123; NGC 77.
- Pull: 120 batches × 100 posts, complete per-post incoming typed sets
  (Amendment 3 §3 ratio estimators). 1,921,530 typed-pre synapses pulled;
  after re-filtering pres to the rebuilt neuronal map and posts to typed
  sampled cells: **722,253 pairs / 1,169,652 synapses** (graph nodes
  42,744). Two batches (39, 60) failed deterministically mid-transfer
  (IncompleteRead at fixed offsets) and were recovered by split queries
  (microns_fixer.py); integrity check: all 120 parts parse, each covers
  exactly its own 100 posts.

## 2. H1-A (structural; on the sampled-posts neuronal graph)
s_AB = typed-neuron synapses from class A onto sampled class-B posts /
all typed-neuron→sampled-B synapses; availability a_A = class-A share of
all typed-neuron→sampled-post synapses.

| Post class | Dominant pre class | s_dom | a_dom | gap | syn onto class |
|---|---|---|---|---|---|
| 23P  | BC    | 0.360 | 0.311 | 0.050 | 335,105 |
| 4P   | BC    | 0.342 | 0.311 | 0.031 | 242,795 |
| 5P-IT| BC    | 0.330 | 0.311 | 0.020 | 139,487 |
| 5P-ET| BC    | 0.317 | 0.311 | 0.007 | 94,979 |
| 5P-NP| 5P-NP | 0.231 | 0.005 | 0.225 | 4,838 |
| 6P-IT| 6P-IT | 0.348 | 0.054 | 0.294 | 93,845 |
| 6P-CT| 6P-CT | 0.238 | 0.029 | 0.209 | 51,364 |
| BC   | BC    | 0.313 | 0.311 | 0.002 | 117,007 |
| MC   | 4P    | 0.205 | 0.132 | 0.072 | 66,987 |
| BPC  | MC    | 0.225 | 0.194 | 0.032 | 17,219 |
| NGC  | MC    | 0.262 | 0.194 | 0.068 | 6,026 |

- **(A1) median dominance = 0.313 < 0.50 → FAIL.** No class approaches
  majority control of any budget (max 0.360). Contrast fly MB: 0.9816.
- **(A2) 8/11 classes within 0.15 → MET.** Where dominance exists it
  mostly tracks availability. The three exceptions are self-dominant
  recurrent classes: 6P-IT (0.348 vs availability 0.054, 6.4×),
  6P-CT (0.238 vs 0.029, 8.4×), 5P-NP (0.231 vs 0.005, 43×) — canonical
  cortical within-class recurrence, invisible to availability-matched
  permutation.

## 3. H1-B (dynamical; Brian2 LIF, Shiu et al. 2024 default_params)
Graph = 42,744 neurons / 722,253 edges; w = ±0.275 mV × synapse count,
sign by presynaptic class E/I (all 11 classes mapped). Drive = all 4P
nodes (9,310; 9,308 with out-edges) at 150 Hz / 1000 ms, PoissonGroup +
1:1, rfc = 0. Readout = non-4P excitatory nodes (28,457; 5,626 with
in-edges), spikes in final 700 ms. Arms: intact vs seed-42 global
partner-permutation (weights preserved); n_run = 4.

| arm | run spikes | mean |
|---|---|---|
| intact | 7,488 / 7,498 / 7,489 / 7,571 | 7,511.5 |
| permuted | 10,089 / 9,985 / 10,141 / 10,054 | 10,067.25 |

- **(B1) intact gate: 4/4 runs > 0 → gate open.**
- **(B2) R_perm = 1.340 ≥ 0.50 → MET.** Permutation does not degrade
  propagation — it *enhances* readout spiking by 34%, i.e. the intact
  cortical wiring suppresses drive→readout throughput relative to an
  availability-matched random partner assignment (structured selection /
  inhibitory routing removed by the shuffle). This is the opposite
  direction from a fragile-specificity regime.

## 4. Interpretation for the collection
- The F1a2 mechanism — permutation cannot hurt because one class IS the
  budget (KC 0.9816) — is **not** the cortical regime. Cortical budgets
  are distributed (top supplier ≤ 0.36).
- Permutation-robustness of drive→readout propagation **does** hold in
  cortex (B2), but its basis is different: availability-tracking
  distributed budgets over ~10³-fold convergence, not single-class
  dominance. Under the frozen compound criterion the hypotheses are
  therefore separable — and H1 separates them: A1 FAIL with B2 MET.
- Availability outliers concentrate exactly where cortical anatomy says
  they should: deep-layer self-recurrence (6P-IT, 6P-CT, 5P-NP). These
  are the loci where a permutation argument would mislead, and where
  compartment/gating maps (F1b) remain necessary.
- For DOCAS/TFP: the fly→mammal bridge claim must be stated as
  "robustness to partner permutation is conserved, its structural basis
  is not" — pending the human (H01) replication.

## 5. Limitations (stated, not silently absorbed)
- Typed-pre coverage: ~19% of incoming synapses onto sampled posts come
  from v661-neuronal-typed cells (boundary truncation — extrinsic axons
  and untyped fragments excluded by the frozen typed-typed rule; same
  convention as H01's registration §2).
- 3,744 of 12,000 sampled posts carry no v661 neuronal type at v1822 and
  are excluded from class-structured evaluation (Amendment 4; exclusion
  by the frozen typing rule, not by outcome).
- s_AB/availability are ratio estimators over uniform sampled posts with
  complete per-post in-sets (Amendment 3 §3); class minima per
  Amendment 1 all met.
- H1-B uses class-level E/I signs and the disclosed Shiu calibration;
  readout nodes without in-edges (22,831 of 28,457) are structurally
  silent and disclosed above.
- Brian2 warning on 'w' namespace shadowing is benign (the synapse
  variable is the intended target of the assignment).

## 6. Permitted paper actions
**NONE taken.** All paper edits await explicit user instruction.

## 7. H01 (human replication) status
Bulk export lane at 12/166 shards under the sustained 0.023 MB/s Google
throttle (checkpointed, still running). The identical frozen tests
(Amendment 1 substrate rule, minima k ≥ 8 / k ≥ 64) run when the export
completes or brain-wire access is approved.

## 8. Evidence manifest (simh1_work/)
SIM_H1_PRE_REGISTRATION.md; SIM_H1_AMENDMENTS.md (Amendments 1–4);
microns_sample_seed45.json (frozen sample); microns_celltypes.json
(rebuilt first-wins map) + microns_celltypes_raw.csv (94,014-row pull) +
microns_celltypes_artifact_superseded.json (audit);
microns_pull_lane_v3.py + mclaims/ + mparts/ (120 parts);
microns_fixer.py (batches 39, 60); microns_status.json;
h1a_evaluate_microns.py + h1a_results_microns.json;
graph_h1b_microns.npz + graph_h1b_microns_stats.json;
run_h1b_sim_microns.py + h1b_results_microns.json + h1b_microns.log;
shiu_model_default_params_snapshot.py (SHA-256 fc45837d7122c6ce…);
fly_mbon_budget.py/json (fly reference 0.9816);
H01 lane: h01_aggregate_worker.py, h01_done.json (12/166),
h01_worker_status.json, parts/.
