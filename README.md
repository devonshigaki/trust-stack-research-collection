# The Value of Trust — Research Collection: Public Review Package

**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010) · The FreshCredit Lab — Independent Research
**Deposit:** all artifacts are mirrored at OSF (DOI: [insert on publication])
**Date of this package:** 2026-09-13

This repository contains the complete, reproducible research base of the
five-work trust-measurement collection: every simulation script, every
pre-computed result, every pre-registration, amendment, and closure document,
every figure (and its rendering code), and the papers themselves.

**You do not need to re-run anything to review this work.** Every simulation
ships with its pre-computed outputs (JSON/CSV/logs) exactly as reported in
the papers. Re-running is optional — `docs/RUNBOOK.md` gives per-simulation
instructions, dependency tiers, expected outputs, and runtimes.

## The collection

| Work | Role | Directory |
|---|---|---|
| The Value of Trust (preface) | OBSERVATION — why trust measurement matters | `papers/` |
| Can trust be measured? (research program) | HYPOTHESIS — measurement and distortion | throughout |
| The General Theory of Trust (GTT) | THEORY — vector state, update law, manifold, Sim G1–G22 | `papers/`, `technical-appendix/sim-code/`, `figures/gtt/` |
| The DOCAS Framework | MODEL — five-carrier neuromodulatory instantiation; Sim F1 (fly), Sim H1 (mouse), Sim D14/D15 (genetics), H01 (human, in progress) | `papers/`, `technical-appendix/simf1_work/`, `simh1_work/`, `simD14/`, `simD15/` |
| The Fresh Protocol (TFP) | APPLICATION — domain-agnostic measurement architecture; Sim P1–P8 | `papers/`, `technical-appendix/sim-code/tfp/` |
| FreshCredit (whitepaper) | APPLICANTS — the financial instantiation, control group, ICP; Sim W-series + robustness batteries | `papers/`, `figures/robustness/` |

## Repository layout

```
papers/               the five works + collection index (PDF + LaTeX source)
figures/              every figure PNG, organized by paper, plus rendering code
preregistrations/     OSF registration documents
technical-appendix/   simulation code, pre-computed results, logs,
                      pre-registrations/amendments/closures per simulation,
                      verification reports, and the numbers ledger
docs/                 RUNBOOK.md (reproduce everything), PATTERNS.md
                      (cross-simulation meta-analysis), deposit README/guide
```

## Research discipline (read this first)

Every quantitative claim in the papers is bounded by **criteria frozen before
data contact**: PASS / FAIL / INDETERMINATE, with INDETERMINATE outcomes
reported, never dropped. Amendments are disclosed with justification before
the amended analysis runs. Buggy first runs are preserved as audit artifacts
(`*_firstrun_bug.json`). FAILs are published as FAILs — see, e.g., Sim F1a2,
Sim H1 (compound FAIL), and `docs/PATTERNS.md` for the full ledger.

## Licensing

- Papers, figures, and original code: **CC BY 4.0** (see LICENSE).
- Materials derived from **FlyWire** data and **AlphaGenome** outputs:
  **CC BY-NC 4.0** — research use only, no commercial use (see LICENSE-NC).
- The H01 dataset is CC BY 4.0 (Allen Institute).
- The Shiu et al. (2024) Drosophila brain model is MIT-licensed
  (`philshiu/Drosophila_brain_model`); a frozen snapshot of the exact
  parameters used is included (`technical-appendix/simh1_work/shiu_model_default_params_snapshot.py`).

## Citation

See `CITATION.cff`. If you use the simulations or data, please cite the
collection and the OSF deposit.

## Competing interests

D.S. is the founder and a beneficiary of FreshCredit Inc. and the founder of
The FreshCredit Lab. FreshCredit Inc holds granted US utility patents
(US 12,236,480 B2; US 12,293,410 B2; US 12,307,515 B2; US 12,293,411 B2).
The underlying protocol is otherwise open; the theoretical results and the
patented methods overlap in composition, and this overlap is disclosed
explicitly in each paper.
