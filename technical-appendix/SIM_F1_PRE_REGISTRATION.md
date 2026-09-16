# Sim F1 — Pre-Registered Criterion (FROZEN BEFORE ANY FLY DATA ACCESS)
# Frozen: 2026-09-12 UTC — before any FlyWire data or model code was downloaded
# or executed. Feasibility-only checks performed pre-freeze: endpoint
# reachability (codex.flywire.ai/api/download HTTP 200; philshiu/
# Drosophila_brain_model HTTP 200; eonsystemspbc/fly-brain HTTP 200;
# BANC Dataverse DOI resolves) and published model specifications.
#
# Question: does the DOCAS/GTT trust-measurement architecture — five parallel
# neuromodulatory channels carrying Expectation, Validation, Recognition,
# Activation, Stabilization — survive cross-species translation? Specifically:
# when a connectome-constrained Drosophila model is given a channel-structured
# modulatory overlay, does it reproduce published real-fly learning behavior,
# and do channel ablations degrade behavior along the predicted lines?
#
# THEORY NOTE (frozen): the channels are functional ROLES, not molecules.
# Drosophila lacks oxytocin and cortisol, yet flies demonstrably form
# associative memories lasting days — so Validation and Recognition functions
# must exist with different carriers. Pre-committed carrier map:
#   D (Expectation)  -> dopamine (PPL1/PAM DANs; direct analog; canonical)
#   A (Activation)   -> octopamine (insect noradrenaline analog; canonical)
#   S (Stabilization)-> serotonin (present; weakest mechanistic anchoring)
#   O (Validation)   -> inotocin (insect oxytocin/vasopressin ortholog)
#                       [in the MB circuit, US-representation is carried by
#                        DANs (aversive) / octopamine (appetitive); frozen]
#   C (Recognition)  -> corazonin + DH44/DH31 axis (CRF/CGRP-related;
#                       ancient stress-peptide system; Kubrak 2016 et al.)
# O and C legs are EXPLORATORY (outside the PASS gate) because their fly
# carrier evidence is thinner; D, A, S legs constitute the gate.

## Substrate (all public)
- FlyWire whole-brain connectome, snapshot v783 (138,639 neurons; CC BY-NC 4.0
  — research use only; outputs may NOT enter FreshCredit commercial materials)
- LIF dynamics per Shiu et al. 2024 (Nature 634:210-219), Brian2;
  code: philshiu/Drosophila_brain_model (MIT); neurotransmitter identity per
  Eckstein et al. 2024 predictions.
- Reference reproduction gate (INDETERMINATE trigger): sugar-GRN drive at
  10-200 Hz must elicit left MN9 firing, and the shuffled-connectivity control
  must not (per Shiu et al. Fig 1-2 and independent reproductions).

## Stage F1a (gated experiment; circuit-scale with whole-brain propagation)
Protocol: in-silico olfactory associative conditioning.
  CS = odor-channel activation (projection-neuron drive to mushroom body);
  US = shock-like (aversive) or sugar-like (appetitive) reinforcement drive
  routed to the corresponding DAN/octopamine populations.
DOCAS overlay (the only addition to the substrate; frozen here):
  D: dopamine-gated plasticity at KC->MBON synapses (eligibility x DAN signal)
  A/O: appetitive US gating via octopamine pathway; aversive via PPL1-DANs
  S: plasticity leak term setting retention horizon (extinction rate)
  (C/O exploratory overlays logged but not gated)

## Benchmarks (named sources frozen here; numeric bands extracted verbatim
## from these papers' published curves/tables at build time, before any run)
- Tully & Quinn 1985: aversive acquisition rises with trials to asymptote;
  retention decays over hours
- Schwaerzel et al. 2003 (J Neurosci): dopamine required for aversive,
  octopamine for appetitive memory (double dissociation)
- Burke et al. 2012: appetitive LTM requires octopamine
- Aso et al. 2014/2016; Hige et al. 2015: DAN-driven KC->MBON plasticity rules

## Frozen PASS / FAIL / INDETERMINATE
PASS requires ALL of:
  (1) aversive acquisition curve monotonic to asymptote within the extracted
      band;
  (2) D-ablation abolishes aversive learning (performance statistically
      indistinguishable from untrained control);
  (3) OA-ablation abolishes appetitive but not aversive learning
      (Schwaerzel dissociation);
  (4) S-ablation increases extinction rate vs intact model (directional);
  (5) shuffled-connectivity control destroys (1)-(4).
FAIL: any of (1)-(3) violated, OR intact model indistinguishable from shuffle.
INDETERMINATE: reference reproduction gate fails (substrate not runnable in
this environment) — reported as INDETERMINATE, never silently dropped; the
package then goes to a local agent per the Sim D14 handoff pattern.
Exploratory (never gated): inotocin (O) and corazonin (C) carrier overlays;
whole-brain closed-loop behavior (Stage F1b) — logged, reported as exploratory.

## Permitted paper action
NONE automatic. Sim F1 is a new study: results (pass, fail, or indeterminate)
go to a new manuscript or a future versioned revision — never retrofitted into
any frozen battery, table, or section of the existing five works.

## Compute plan
Circuit-scale trials on CPU are feasible (published reproduction: ~40 s wall
per 300 ms brain-time per run, one core). Multi-trial conditioning with
plasticity = F1a target. Whole-brain closed-loop (F1b) likely requires
GPU/Brian2CUDA (Eon repo) or local-agent execution.
