# The Trust Stack — Research Collection: Public Review & Reproducibility Package

**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010) · The FreshCredit Lab — Independent Research  
**Release:** **Version 4.5 — November 2026**  
**Repository:** [github.com/devonshigaki/trust-stack-research-collection](https://github.com/devonshigaki/trust-stack-research-collection)

---

## Overview

This repository contains the reproducible research base of **The Trust Stack**, a six-work research collection investigating whether trust can be formalized and measured as the dynamical relationship between an agent's expectations ($E_t$) and the validations ($V_t$) returned by its environment ($\varepsilon_t = V_t - E_t$), without relying on centralized behavioral surveillance.

### The Six Works (`manuscripts/`)

| Work | Epistemic Role | Canonical Files |
| :--- | :--- | :--- |
| **The Value of Trust** (Preface) | `[OBSERVATION]` — Philosophical & ethical grounding of trust measurement | `manuscripts/value_of_trust/{value_of_trust.md,value_of_trust.tex,value_of_trust.pdf}` |
| **Collection Index & Correction Register** | `[INDEX]` — Stack-wide symbol registry, epistemic labels, 34-item correction register | `manuscripts/collection/{collection.md,collection.tex,collection.pdf}` |
| **The General Theory of Trust (GTT)** | `[THEORY]` — Five-channel state vector $T=[D,O,C,A,S]$, Master Stability Law, Esscher probability tilt, regularized Fisher–Rao geometry | `manuscripts/gtt/{gtt.md,gtt.tex,gtt.bib,gtt.pdf}` |
| **The DOCAS / TDF Framework** | `[MODEL / HYPOTHESIS]` — Multi-timescale neuromodulatory instantiation, connectomics (FlyWire, MICrONS), CLICS³ colexification, Brain-IT decoding audit | `manuscripts/tdf/{tdf.md,tdf.tex,tdf.bib,tdf.pdf}` |
| **The Fresh Protocol (TFP)** | `[PROTOCOL SPEC]` — Domain-agnostic decentralized measurement architecture (W3C DIDs, RFC 9901 SD-JWT, secp256k1 NIZK `ZK-STP v8`, sovereign per-tenant stores) | `manuscripts/tfp/{tfp.md,tfp.tex,tfp.bib,tfp.pdf}` |
| **FreshCredit Whitepaper** | `[APPLICATION]` — Consumer-permissioned cash-flow underwriting, OpenML 42477 ($N=30{,}000$) empirical validation, statutory biometric Sequestration Wall | `manuscripts/whitepaper/{whitepaper.md,whitepaper.tex,whitepaper.bib,whitepaper.pdf}` |

---

## Repository Architecture

```text
manuscripts/    Per-manuscript directories ({collection,value_of_trust,gtt,tdf,tfp,whitepaper}/) with .md, .tex, .bib, compiled .pdf, and figures/ symlinks
figures/        Single canonical figure store (symlinked cleanly into manuscripts/*/figures)
formal/         Lean 4.35 + Mathlib (32 theorems, leanchecker), Z3 SMT, SymPy CAS, secp256k1 NIZK (ZK-STP v8), TLA+ TLC
protocols/      Pre-registrations, amendments, pilot protocols, IRB exemption, FCRA matrix
code/
  ├── empirical/    Real external-data pipelines (OpenML 42477 30k credit, CLICS-3, simD14 AlphaGenome, simD15 GTEx, FlyWire, MICrONS)
  ├── simulations/  In-silico dynamical, neural, wearable, and protocol models
  └── tools/        57-task CI suite runner, Thresholdout autoresearch, SHA-256 manifest (--verify)
docs/           RUNBOOK.md, PATTERNS.md, SIMULATION_ACCOUNTING.md, VERSIONS.md, notes & indexes
```

---

## Reproducing Verifications & Simulations

```bash
# Run formal proofs (Lean 4.35, TLC, Z3, SymPy, secp256k1 NIZK), citation/sync checks, 45-task suite, and seal SHA-256 manifest
make check

# Or run targets individually:
make formal      # Z3 SMT, SymPy CAS, TLA+ TLC model checker, Lean 4 leanchecker, secp256k1 Pedersen/Schnorr/Tuple-OR NIZK
make test        # 57-task Tier 1 & Tier 2 suite
make sims        # Core local simulation reproduction suite
make osf-deposit # Build reproducible OSF zip bundle in dist/
```

---

## Licensing & Competing Interests

- **Papers, figures, and original code:** **CC BY 4.0** (`LICENSE`).
- **FlyWire-derived and AlphaGenome-derived artifacts:** **CC BY-NC 4.0** — non-commercial research use only (`LICENSE-NC`).
- **Competing Interests:** D.S. is the founder of FreshCredit Inc. and The FreshCredit Lab. FreshCredit Inc. holds US utility patents (`US 12,236,480 B2`, `US 12,293,410 B2`, `US 12,307,515 B2`, `US 12,293,411 B2`).
