# Sim H1 — Pre-registration (FROZEN 2026-09-12, before any H01 criterion-relevant data)
Question: is class-level input-budget dominance under partner permutation —
the mechanism that produced F1a2's FAIL in the fly mushroom body — also
present in a human cortical connectome? Either outcome is informative and
will be reported: presence = cross-species generality of the wiring regime
that makes compartment/gating maps necessary; absence = the fly MB regime is
special, which the collection must then state.

## 1. Data and license
H01 c3 synaptic-connections export (Google Research / Lichtman Lab, Science
2024): ~100 Avro shards at
gs://h01-release/data/20210729/c3/synapses/exported/. Cell table:
agglo_20200916c3_cell_data.json (ashapsoncoe/h01 GitHub, mirrored to
simh1_work/h01_cell_data.json): 49,377 typed cells with soma in volume.
License CC BY 4.0 (attribution required; commercial use permitted — unlike
FlyWire CC BY-NC; noted for collection records).

## 2. Disclosed instrument checks (completed before freezing; shard 0 only)
- Avro schema: pre_synaptic_site.neuron_id, post_synaptic_partner.neuron_id,
  top-level integer 'type', contact_area, confidence, location, bounding_box.
- Shard 0: 998,235 rows; top-level type values {1: 40.8%, 2: 59.2%}.
- Cell-table ID space: 49,377 records map to 45,994 unique agglo_seg IDs
  (merged-soma collisions; first record wins, collisions counted at build).
- Boundary truncation (measured, shard 0): presynaptic partner typed 0.6%,
  postsynaptic typed 17.2%, both typed 0.3%. All H1 claims are therefore
  restricted to the typed-typed subgraph; truncation is a stated limitation.
- E/I assignments: (a) cell-class level, from the H01 authors' own mapping
  (edge_list_to_graph.py): pyramidal / spiny-stellate / excitatory-spiny-
  atypical = excitatory; interneuron = inhibitory; unclassified neuron =
  unmapped. (b) Synapse-level type field: type 1 = inhibitory, type 2 =
  excitatory — INFERRED, corroborated by shard-0 targeting bias (type-1
  synapses supply 84% of AIS and 79% of soma contacts, consistent with
  GABAergic physiology; chandelier/AIS synapses are inhibitory). Frozen
  fallback: H1-B uses class-level E/I (a) only, so an error in inference (b)
  cannot affect H1-B; type-level E/I is reported descriptively only.

## 3. Graph construction (fixed)
G: nodes = typed cells; directed edge (u,v) weight w = number of export rows
with pre=u, post=v. G_N = neuronal subgraph: classes {pyramidal neuron,
interneuron, spiny stellate neuron, excitatory/spiny neuron with atypical
tree, unclassified neuron}. Build streamed shard-by-shard with checkpointed
part-files; integrity = per-shard byte size vs GCS listing + row counts.

## 4. Tests and frozen criteria
H1-A (structural, primary), on G_N:
- s_AB = synapses from class A onto class-B cells / all typed-neuron→B
  synapses; a_A = class A's share of all typed-neuron→typed-neuron synapses
  (availability). dominance_B = max_A s_AB.
- (A1) median dominance_B over neuronal postsynaptic classes >= 0.50.
- (A2) for each B's dominant presynaptic class, |s_dom,B - a_dom| <= 0.15
  for a majority of neuronal classes B.
A1 establishes single-class budget dominance; A2 establishes that dominance
tracks availability — the condition under which partner permutation
preserves class-level budgets (the F1a2 mechanism).

H1-B (dynamical, secondary): Brian2 LIF propagation on G_N, parameters per
Shiu et al. 2024 default_params for cross-study comparability (disclosed
calibration); edge signs by class-level E/I (a); w = ±0.275 mV x synapse
count. Drive = all 185 spiny stellate neurons, 150 Hz Poisson, 1000 ms
(PoissonGroup + 1:1 synapses, rfc=0 — F-series drive pattern); readout =
pyramidal neuron spikes in final 700 ms. Arms: intact vs class-faithful
global partner-permutation (postsynaptic partners permuted, weights
preserved, seed 42 — the F1a2 shuffle recipe), n_run = 4, run-mean primary.
- (B1) intact gate: pyramidal spikes > 0 in >= 3/4 runs, else
  INDETERMINATE-instrument (pre-scored, reported).
- (B2) R_perm = permuted/intact pyramidal spike count >= 0.50.
- Frozen contingency: if G_N has < 10,000 edges, H1-B is
  INDETERMINATE-instrument (reported, not dropped).

PASS = A1 AND A2 AND B2 (B1 gating). FAIL = any violated. INDETERMINATE
outcomes reported, never silently dropped.

## 5. Descriptive context (no PASS legs)
Fly reference values from the archived F-series (KC→MBON budget share; F1a2
shuffle R_final = 0.873 position-based / 0.680 class-faithful) and H01
per-post truncation factors, synapse-count-per-pair distribution (the
paper's 'powerful pairs' heavy tail), and E/I budget per postsynaptic class.

## 6. Permitted paper actions
NONE automatic. All paper edits await explicit user instruction.
Attribution per CC BY 4.0 in any use.
