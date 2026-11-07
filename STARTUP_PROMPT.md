# TRUST STACK RESEARCH AGENT: BOOTSTRAP & GROUND-TRUTH DIRECTIVE

**To any AI Agent entering this workspace:**
You are entering the **Trust Stack (Version 4.0 / 4.2)** research environment developed by Devon Shigaki (ORCID: [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)).

## 1. Ground-Truth Source Hierarchy (STRICT PRECEDENCE)
1. **Canonical Living Manuscripts (`Desktop/Research/papers/*.md`):**
   - `whitepaper.md` (FreshCredit financial application, Version 4.0)
   - `docas.md` / `tdf.pdf` (DOCAS neuromodulatory biological architecture, Version 4.0)
   - `gtt.md` (General Theory of Trust mathematical foundations, Version 4.0)
   - `tfp.md` (The Fresh Protocol decentralized architecture, Version 4.0)
   - `the_value_of_trust.md` (Philosophical grounding)
   - `collection.md` (Research collection index)
   *MANDATE:* These files are the single source of truth. If a statement in a review or note contradicts `papers/*.md`, the manuscript governs.

2. **Historical Review Artifacts (`Desktop/Research/reviews/*`):**
   - **WARNING:** Several files in `reviews/` (e.g. `ARGON4_SCHOLARPEER_REVIEW.md`) were generated against early truncated drafts. Do NOT cite historical review critiques as active deficits without verifying against `papers/*.md`.

3. **Simulation & Invariant Ledgers:**
   - `Desktop/Research/SIMULATION_ACCOUNTING.md` (Comprehensive index of all simulations through Version 4.2).
   - `Desktop/Research/VERSIONS.md` (Version changelog).
   - `Desktop/Research/formal-verification/FORMAL_VERIFICATION_REPORT.md` (Lean 4, Z3, SymPy, TLA+ certificates).

## 2. Core Resolved Archival Landmarks
- **The Sequestration Wall (`whitepaper.md` §3.2):** Credit scoring is strictly cash-flow only. Physiological data has zero schema path to credit decisions. Checked via on-chain hashed weight checkpoints.
- **The Biophysical Eligibility Trace (`docas.md` §5.32, Sim S1):** MSN dendritic eligibility traces $c(t)$ ($\tau_c = 100\text{ms}$) integrated with phasic dopamine RPE bursts $D(t)$ recover the macroscopic Master Stability Law at $r = 1.0000$.
- **PDE4B Status (`docas.md` §4.2, §4.4, §5.14):** PDE4B is NOT proven; it failed the UK Biobank replication gate ($p = .18$) and is a labeled hypothesis. The apparent schizophrenia downregulation contradiction is resolved via the **Arnsten inverted-U model of prefrontal cortical cAMP signaling** (excessive cAMP opens HCN1 channels, causing supercritical noise $\nu > 1$ that blocks sensory validation, forcing compensatory paranoid priors).
- **Anti-Collusion Entropy Gate (`tfp.md` §3.7, Sim P8c):** Parallel-provider collusion is defeated by scaling effective time accumulation with provider signature Shannon entropy: $\Delta t_{\mathrm{eff}} = \Delta t_{\mathrm{wall}} \cdot [1 - \exp(-H(\mathbf{w}))]$.
- **Temporal SHAP Recourse (`whitepaper.md` §5, Sim W8):** ECOA/Reg B adverse action notices are generated with machine-precision Shapley efficiency ($1.39 \times 10^{-17}$) providing exact counterfactual edit targets.
- **Fisher-Rao Regularity (`gtt.md` §3.1, Theorems FR-1–FR-4):** Epsilon regularization $\tilde{\theta}_i = (\theta_i + \epsilon)/(1+5\epsilon)$ strictly eliminates boundary metric singularities ($p_i \to 0$) and guarantees Lipschitz-bounded kinetic energy in Z3 and SymPy.

## 3. How to Run Verifications
- To run all newly added Tier 1 & Tier 2 tests:
  `/Users/devonshigaki/Desktop/Research/.venv/bin/python3 /Users/devonshigaki/Desktop/Research/run_tier1_tier2_suite.py`
- To run the full local simulation battery:
  `/Users/devonshigaki/Desktop/Research/.venv/bin/python3 /Users/devonshigaki/Desktop/Research/run_all_sims_local.py`
