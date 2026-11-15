# Sim F1a2 — Amendment 1 (FROZEN 2026-09-12, before any shuffle-v2 data)

## What happened
The F1a2 battery (24 runs, 6 arms x n_run=4) is complete and evaluated against
the frozen criteria. Results are final and remain on the record unchanged:

- (1) intact-aversive: rho = -1.000, R_final = 0.401  -> MET
- (2) D-ablation:      R_final = 1.015 (flat, rho = -0.071) -> MET
- (3a) appetitive:     rho = -1.000, R_final = 0.399 -> MET
- (3b) OA-dissociation: INDETERMINATE (instrument), as pre-scored
- (4) S-ablation:      recovers R >= 0.90 at probe 5; intact censored (0.741
                       at probe 8) -> MET per frozen contingency
- (5) shuffle (as run): B0 = 141.1 Hz, rho = -0.976, R_final = 0.873
  -> NOT MET (required > 0.95). As-run F1a2 verdict: FAIL on criterion (5).

## The ambiguity this amendment resolves
Design Addendum A froze: "Plastic synapses: all KC -> MBON synapses" and
"Shuffle control: within-circuit connectivity randomly permuted (weights
preserved, partners permuted; fixed seed 42)." It did not specify how the
plastic set is defined ON the permuted graph. The as-run implementation
depressed the intact-graph KC->MBON edge POSITIONS; after permutation those
positions connect random partners, so ~1.6% still terminate on MBONs and most
land on KC->KC pairs — producing a weak partial MBON decline (R_final 0.873)
that is an implementation artifact of position-based targeting, not a property
of the circuit rule.

The frozen text defines plasticity by neuron CLASS ("all KC -> MBON
synapses"). The class-faithful reading on a permuted graph: the plastic set is
the KC -> MBON edges OF the permuted graph.

## Frozen amendment (before shuffle-v2 data)
- Shuffle-v2 arm: identical permutation (seed 42), plastic set re-derived as
  KC -> MBON edges of the permuted graph; eligibility/trigger/update/leak
  constants unchanged; n_run = 4.
- Scoring (frozen now): criterion (5) is reported for BOTH variants. The
  class-faithful variant is the primary control (natural reading of the frozen
  text); the position-based variant stands as a reported secondary. If they
  disagree, that disagreement is itself reported as a control-sensitivity
  finding. The as-run FAIL is never removed from the record.
- Disclosure: this amendment is written after seeing the position-based
  shuffle outcome (0.873). It is justified by the frozen text, not by the
  outcome; both numbers are published regardless of the shuffle-v2 result.
