# Sim H1 — Amendment 4 (2026-09-12; disclosed before any criterion evaluation)
Cell-type map correction; same amendment discipline (criteria, thresholds,
sampling rule, permutation recipe, n_run, aggregation, permitted paper
actions unchanged; evaluation remains blind — no s_AB, availability,
dominance, or spiking criterion quantities computed on MICrONS data).

1. Defect found: the working cell-type map (microns_celltypes.json, built
   earlier this session) is irreconcilable with the authoritative
   aibs_metamodel_celltypes_v661 table at materialization 1822: the artifact
   carried 71,997 neuronal roots while the complete table pull (94,014 rows,
   offset-paginated, row count verified against the table's annotation
   count) yields 67,214 unique roots of which 49,621 are neuronal
   (43,965 excitatory, 5,656 inhibitory, 17,593 nonneuronal). 22,205
   artifact roots do not exist in the v661 table at v1822 — the artifact's
   provenance is unrecoverable (consistent with a pull at a different
   materialization, where root ids are different identifiers).
2. Corrective action (before any criterion quantity is computed):
   a. Class map rebuilt from the complete v661 table pull at v1822,
      deduplicated FIRST-WINS by ascending annotation id (the H01 cell-table
      precedent, matching the pre-registration's stated convention). New
      microns_celltypes.json = 67,214 roots; the superseded artifact is
      retained as microns_celltypes_artifact_superseded.json for audit.
      Raw table archived as microns_celltypes_raw.csv.
   b. Frozen sampling rule unchanged (seed 45, n = 12,000). Of the 12,000
      sampled posts, 8,256 are v661-neuronal-typed at v1822 and enter
      H1-A/H1-B. Per-class sampled-post counts: 23P 2,193; 4P 1,677;
      6P-IT 1,351; 5P-IT 955; 6P-CT 732; BC 364; MC 292; 5P-ET 277;
      BPC 215; 5P-NP 123; NGC 77 — every class above the Amendment-1
      minimum (k >= 8). The 3,744 sampled posts without v661 neuronal
      types (3,712 artifact-only roots + 32 nonneuronal) carry no
      postsynaptic class and are excluded from class-structured evaluation;
      their exclusion is by the frozen typing rule, not by outcome.
   c. Pull-lane presynaptic filter check: the running lane's typed-pre set
      is the artifact key set. Verified: 0 of the 49,621 v661-neuronal
      roots are missing from that set (it is a strict superset), so no
      neuronal-pre edge is lost in flight. Artifact-only pre roots retained
      in part files are re-filtered out at evaluation time by the rebuilt
      map (they are not v661-typed at v1822).
3. What does NOT change: the sample itself (no re-draw — avoids any
   discretion in post selection; the cost is efficiency only, since
   per-class ratio estimators remain unbiased within typed strata),
   all criteria and thresholds, and the pull-lane queue.
4. Statistical note: expected per-class sampled-post counts in Amendment 3
   section 3 were computed from the artifact map's class proportions and are
   superseded by the realized counts in 2b above.

# Sim H1 — Amendment 3 (2026-09-12; disclosed before any criterion evaluation)
Scale management for the MICrONS substrate; same amendment discipline
(criteria, thresholds, permutation recipe, n_run, aggregation, permitted
paper actions unchanged; evaluation remains blind — no s_AB, availability,
dominance, or spiking criterion quantities computed on MICrONS data).

1. Version frozen: materialization version 1822 (most recent at access
   date), datastack minnie65_public.
2. Cell-type table: aibs_metamodel_celltypes_v661 (94,014 annotations;
   completeness verified by over-limit probe). Neuronal typed set =
   classification_system in {excitatory_neuron, inhibitory_neuron}
   (72,158 cells). Class map (MICrONS aibs nomenclature):
   excitatory {23P, 4P, 5P-IT, 5P-ET, 5P-NP, 6P-IT, 6P-CT};
   inhibitory {BC (PV basket), MC (SST Martinotti), BPC (VIP bipolar),
   NGC (neurogliaform)}. E/I signs for H1-B from this class map (the
   Amendment-2 equivalent of the H01 author class mapping).
3. Sampled-posts pull (frozen sampling rule): the full typed-post synapse
   pull is ~100M rows — infeasible over the API. Instead: uniform random
   sample of n = 12,000 typed neurons (seed 45), and for each sampled cell
   its COMPLETE incoming typed synapse set. Ratio estimators (s_AB,
   availability) are unbiased under uniform postsynaptic sampling — the
   Amendment-1 argument, here exact per sampled cell (no within-cell
   thinning). Expected per-class cell counts in sample: 23P ~3,280,
   4P ~2,457, 6P-IT ~1,951, 5P-IT ~1,322, 6P-CT ~1,133, BC ~560, MC ~411,
   5P-ET ~368, BPC ~247, 5P-NP ~161, NGC ~107.
4. H1-B mapping (per Amendment 2): drive = 4P cells (the thalamorecipient
   layer-4 excitatory class) at 150 Hz / 1000 ms; readout = non-4P
   excitatory cells, spikes in final 700 ms; arms intact vs seed-42 global
   partner-permutation; B1 gate: readout spikes > 0 in >= 3/4 intact runs;
   B2: R_perm >= 0.50. Graph = sampled posts + their typed presynaptic
   cells as nodes (dense local neighborhoods: sampled cells keep their
   complete typed in-degree).
5. The H01 shard worker/lanes continue unchanged toward the human
   replication.

# Sim H1 — Amendment 2 (2026-09-12; disclosed before any criterion evaluation)
Substrate access update, same amendment discipline as Amendment 1 (criteria,
thresholds, graph construction, permutation recipe, n_run, aggregation, and
permitted paper actions all unchanged; criterion evaluation remains blind —
no MICrONS criterion quantities computed).

1. H01 bulk export remains throttled (0.023 MB/s sustained). H01's own CAVE
   instance (brain-wire.org, Harvard VCG) requires a manual Google-form
   application with ~24 h approval — outside this sandbox's control.
2. The user-provided CAVE token (global.daf-apis.com) grants access to the
   Allen/Princeton-hosted datastacks, including minnie65_public — the
   MICrONS mouse visual-cortex cubic millimeter, the field-standard
   fully-proofread mammalian cortex connectome (synapse table
   synapses_pni_2; soma table nucleus_detection_v0; local server
   minnie.microns-daf.com; ToS acceptance recorded by the user).
3. The H1 question — is class-level input-budget dominance under partner
   permutation present in MAMMALIAN cortex — is species-general by design.
   MICrONS mouse cortex is therefore a valid and better-annotated substrate
   for the primary test. H1-A and H1-B run on minnie65_public materialized
   synapses, restricted to cells with nucleus detections and cell-type
   annotations (the datastack's cell-type table), with the same class sets
   re-derived from MICrONS annotations (excitatory classes, inhibitory
   classes; the stellate-drive analogue is re-derived from the thalamorecipient
   layer-4 classes if present, else H1-B is INDETERMINATE-instrument as
   pre-scored).
4. H01 remains the human-specific extension: the bulk-export worker and
   shell lanes keep grinding (checkpointed); when the export completes or
   brain-wire access is approved, the identical frozen tests run on H01 as
   the human replication.

# Sim H1 — Amendment 1 (2026-09-12; disclosed before any criterion evaluation)
Frozen registrations may be amended only with disclosed justification before
the amended analysis is run (F1a2 Amendment 1 precedent). No criterion
thresholds change. No s_AB, availability, or dominance quantities have been
computed on partial data; the criterion evaluation remains blind.

## 1. Justification
Sandbox egress to Google Cloud Storage is throttled to a sustained
0.023 MB/s (measured 2026-09-12, kernel probe, 90 s window). The full c3
export (166 shards, 32.9 GB) would take ~16 days. Shards complete at
~1/40 min via the patient checkpointed worker. This amendment defines the
substrate rule under that constraint.

## 2. Export shards are spatially unordered (evidence)
- Shard 0's first record sits at (x 461.5k, y 196.5k nm) — the far corner of
  the volume (x range 64.7k-484.0k), inconsistent with spatial ordering.
- Typed postsynaptic cells from completed shards 0-4 span the entire volume
  footprint (shard_spread.png, produced from posttot part files + the cell
  table's soma coordinates; plotted per shard).
Therefore each shard is a ~1/166 uniform random sample of ALL synapse rows:
typed-typed pairs observed with k shards are an unbiased, volume-wide sample;
class-proportion estimators (s_AB, availability) are ratio estimators and
remain unbiased under uniform row sampling. Cost is precision and per-pair
count thinning only.

## 3. Amended substrate rule (frozen)
- Substrate at evaluation = all shards completed by then, monotone growth;
  every completed shard is included (no cherry-picking possible: inclusion
  is exhaustive and frozen).
- H1-A minimum: k >= 8 shards (~25k typed-typed pairs; standard error on a
  dominant share ~0.6 <= sqrt(0.6*0.4/25000) = 0.003, an order below the
  0.15 tolerance). If k < 8 after 72 h of worker operation, H1-A is
  evaluated at the k then available with the limitation escalated in the
  closure; if k < 4, H1-A is INDETERMINATE-instrument.
- H1-B minimum: k >= 64 shards. Justification: the typed-typed subgraph's
  mean in-degree scales as ~32 * k/166; the propagation gate requires
  driven->readout paths dense enough to test fairly (degree >= ~12). Below
  k = 64 the gate would measure sparsity, not permutation robustness, so
  H1-B is INDETERMINATE-instrument (pre-scored, reported, never dropped).
- The worker continues toward all 166 shards regardless; if throughput
  recovers, the full export is used and this amendment's minima are moot.

## 4. Disclosed instrument checks since the registration
- Partial-graph smoke (4 shards, 3,394 edges, 4,506 nodes): Brian2 signed
  LIF build OK; stellate drive fires 72/72 cells at ~148 Hz (150 Hz drive);
  pyramidal spikes = 0 at this sparsity (mean degree 0.75) — drive chain
  functional, transmission untestable on the partial graph. Not a criterion
  evaluation.
- Fly reference (registration section 5) completed on whole-brain v783:
  KC share of MBON input budget = 0.9816 (DAN 0.0584, MBON -0.0313
  inhibitory, LHCENT -0.0087; signed weights, 261,521 total weight onto 96
  MBONs; fly_mbon_budget.json). The fly MB regime is an extreme
  single-class-budget case — the benchmark H1-A compares human cortex
  against.

## 5. Unchanged
All frozen criteria (A1, A2, B1, B2), graph construction, E/I handling,
permutation recipe (seed 42), n_run = 4, aggregation, INDETERMINATE
reporting, and permitted paper actions (NONE automatic).
