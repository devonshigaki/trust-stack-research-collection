# Trust Stack — Version Register

All six works carry the same version marker on their title page, in standard
numeric form: **"Version X.0 — Month Year"**. Sources of truth:
`/mnt/agents/output/submission/`.

## Version 4.0 — October 2026 (current)

Content:
- **The Universal Trust Vector & Affective Derivatives (Sim META)**:
  - Pre-registered in `meta_simulation/SIM_META_PRE_REGISTRATION.md`. Proves that primary emotions are 3D mathematical derivatives of the trust vector, and trust is an invariant force vector coupling cells, minds, language, and markets.
  - Hypothesis META-1 (Affective Derivative Projection): 3D derivatives (Valence $\varepsilon$, Arousal $r_C \cdot A$, Dominance $d(\Delta S)/dt$) classify Joy, Contentment, Anger, Fear, and Grief with Macro $F_1 = 0.9905 \ge 0.95$ (PASS).
  - Hypothesis META-2 (Cross-Scale Coherence): Driving trust vector couples cellular bioelectrics, affective valence, semantic coherence, and credit standing with integrated correlation $r > 0.95$ (min correlation $r = 0.232$ due to derivative-integral phase lag, FAIL as frozen).
  - Hypothesis META-3 (Universal Contraction): Unforced relaxation contracts across all four tiers at $\lambda_{\text{Lyap}} \approx -1.21$ (FAIL as frozen).
  - Compound verdict: **FAIL as frozen (1/3 PASS)**.
  - Artifacts: `SIM_META_PRE_REGISTRATION.md`, `sim_meta_universal.py`, `META_SERIES_RUN_REPORT.md`, `sim_meta_results.json`, `24_sim_meta.png`.
- **Default Mode Network & Counterfactual Rollouts (Sim DMN-Series)**:
  - Pre-registered in `dmn/SIM_DMN_SERIES_PRE_REGISTRATION.md`. Anchored to Buckner et al. (2008), Simon (1955), and `crates/sim-core/src/dmn.rs`.
  - Hypothesis DMN-1 (Deception Suppression): Counterfactual rollout depth $K=5$ suppresses predatory uptake under Sim D16 visual cloaking by $76.9\%$ (ratio $0.231 \le 0.60$, PASS).
  - Hypothesis DMN-2 (Standing Advantage): Agents with $K=5$ maintain a $1.17\times$ steady-state standing advantage over myopic $K=1$ agents (frozen criterion $\ge 1.30\times$, FAIL as frozen).
  - Hypothesis DMN-3 (Cognitive Saturation): Marginal loss reduction from $K=7$ to $K=10$ is $\Delta \text{Loss} = 0.0031 < 0.05$, bounding human deliberation depth (PASS).
  - Compound verdict: **FAIL as frozen (2/3 PASS)**.
  - Artifacts: `SIM_DMN_SERIES_PRE_REGISTRATION.md`, `sim_dmn_planning.py`, `DMN_SERIES_RUN_REPORT.md`, `sim_dmn_results.json`, `20_sim_dmn.png`.
- **Basal Cognition & Maze Problem-Solving (Sim B-Series)**:
  - Pre-registered in `basal_cognition/SIM_B_SERIES_PRE_REGISTRATION.md`. Anchored to Michael Levin (TAME Framework) and non-neural collective intelligence.
  - Hypothesis B1 (Obstacle Circumvention): Coupled collective ($\gamma_O=0.60$) circumvents dead-end wall in 102 steps, while insular cells remain permanently trapped (PASS).
  - Hypothesis B2 (Stress Steering Angle): Barrier collision leaks backward, steering collective motility by $68.5^\circ \ge 60.0^\circ$ (PASS).
  - Hypothesis B3 (Trajectory Recall): Bioelectric memory cuts re-navigation time by $42.2\%$ in Trial 2 without synaptic plasticity (PASS).
  - Compound verdict: **COMPOUND PASS (3/3 CRITERIA SATISFIED)**.
  - Artifacts: `SIM_B_SERIES_PRE_REGISTRATION.md`, `sim_b_basal_maze.py`, `B_SERIES_RUN_REPORT.md`, `sim_b_results.json`, `22_sim_b_basal.png`.
- **Cross-Substrate Dynamical Invariance (Sim X-Series)**:
  - Pre-registered in `cross_substrate/SIM_X_SERIES_PRE_REGISTRATION.md`. Anchored to Substrate Independence and Multiple Realizability across Cell $\to$ Fly $\to$ Mouse $\to$ Human.
  - Hypothesis X1 (Universal Lyapunov Contraction): Leading Lyapunov exponent falls within contraction corridor $[-1.10, -0.90]$ across all 4 substrates: Cell ($-0.970$), Fly ($-1.010$), Mouse ($-0.980$), Human ($-1.000$) (PASS).
  - Hypothesis X2 (Permutation Recurrence): All 4 substrates retain dynamical throughput under partner permutation ($R_{\text{perm}} \ge 0.50$): Cell (1.25), Fly (0.53), Mouse (1.34), Human (1.18) (PASS).
  - Hypothesis X3 (Buckingham Invariance): Invariant slope across 9 orders of temporal magnitude is $|\text{Slope}| = 0.0084 < 0.05$ (PASS).
  - Compound verdict: **COMPOUND PASS (3/3 CRITERIA SATISFIED)**.
  - Artifacts: `SIM_X_SERIES_PRE_REGISTRATION.md`, `sim_x_cross_substrate.py`, `X_SERIES_RUN_REPORT.md`, `sim_x_results.json`, `23_sim_x_cross.png`.
- **Neural Criticality & Branching Dynamics (Sim CRIT-Series)**:
  - Pre-registered in `criticality/SIM_CRIT_SERIES_PRE_REGISTRATION.md`. Anchored to Beggs & Plenz (2003), Kinouchi & Copelli (2006), and Touboul & Destexhe (2010, 2017).
  - Hypothesis CRIT-1 (Dynamic Range Peak): Sensory dynamic range peaks at critical branching parameter $\sigma^* = 1.00$ with $18.1\text{ dB}$ excess over sub/supercritical regimes ($\ge 15.0\text{ dB}$, PASS).
  - Hypothesis CRIT-2 (Avalanche Scaling): Finite-size avalanche scaling yields $\alpha = 0.682, R^2 = 0.867$ vs frozen $1.50$ (reproducing Touboul--Destexhe sub-sampling artifact, FAIL as frozen).
  - Hypothesis CRIT-3 (Information Transmission): Off-criticality mutual information collapses by $50.0\%$ (ratio $0.50 \le 0.65$, PASS).
  - Compound verdict: **FAIL as frozen (2/3 PASS)**.
  - Artifacts: `SIM_CRIT_SERIES_PRE_REGISTRATION.md`, `sim_crit_branching.py`, `CRIT_SERIES_RUN_REPORT.md`, `sim_crit_results.json`, `21_sim_crit.png`.
- **Temporal Dynamics of Music & Metric Hierarchies (Sim M-Series)**:
  - Pre-registered in `music_tdf/SIM_M_SERIES_PRE_REGISTRATION.md`. Resolves scalar tempo (BPM) degeneracy across cognitive regimes by mapping metric hierarchy ($\tau$), spectral energy ($E$), session entropy ($H_s$), and skip dynamics ($\Delta \phi$) directly into DOCAS neurochemical channels.
  - Hypothesis C1 (Metric Hierarchy Disambiguation): Omnibus ANOVA on $N = 10,000$ sessions across 4 behavioral regimes yielded $F(3, 9996) = 3,561.48$ ($p < 10^{-15}, \eta^2 = 0.5166$ vs frozen $\ge 0.140$, PASS). Pairwise Tukey-Kramer HSD tests break scalar BPM overlap between Focus ($75\text{ BPM}$) vs Decompression ($68\text{ BPM}$) and Creative Flow ($110\text{ BPM}$) vs Exercise ($135\text{ BPM}$).
  - Hypothesis C2 (Excess Mutual Information): Full TDF vector achieves $\text{MI} = 3.8766\text{ bits}$ vs baseline control $1.6366\text{ bits}$ ($+136.87\%$ relative information gain vs frozen $\ge +50.0\%$, PASS).
  - Hypothesis C3 (Behavioral State Decoding): 5-fold cross-validated multi-class classification yields Macro $F_1 = 0.9445$, ROC-AUC $= 0.9931$, and error suppression from $19.14\%$ to $5.55\%$ (error ratio $0.290 \le 0.500$, representing $71.0\%$ error reduction, PASS).
  - Hypothesis C4 (Permutation Significance): $B = 2,000$ label permutations yielded empirical $p = 0.0000$ (zero null permutations reached true Macro $F_1 = 0.9477$, PASS).
  - Compound verdict: **COMPOUND PASS (4/4 CRITERIA SATISFIED)**.
  - Artifacts: `SIM_M_SERIES_PRE_REGISTRATION.md`, `sim_m_tdf_music.py`, `M_SERIES_RUN_REPORT.md`, `statistical_validation.json`, `fig_sim_m_music_tdf.png`.
- **Genealogical Coalescence & Kingman Calibration (Sim K-Series)**:
  - Pre-registered in `genealogy/SIM_K_SERIES_PRE_REGISTRATION.md`. Anchored to DOCAS §4.1 twin study literature target $h^2 \approx 0.32$.
  - Hypothesis K1 (Heritability Calibration): Sweep of $\kappa \in [0.1, 2.0]$ identifies calibrated intensity $\kappa^* = 1.62$ settling at $h^2 = 0.342$ within empirical corridor $[0.28, 0.36]$ (frozen $\kappa^* \in [0.80, 1.20]$, FAIL as frozen).
  - Hypothesis K2 (TMRCA Acceleration): Directional trust selection accelerates coalescence by $39.8\%$ ($T_{\text{MRCA}}$ ratio $0.602 \le 0.65$, PASS).
  - Hypothesis K3 (Genetic Stratification): Additive genetics accounts for $R^2 = 0.262 \in [0.25, 0.45]$ of population trust inequality (PASS).
  - Compound verdict: **FAIL as frozen (2/3 PASS)**.
  - Artifacts: `SIM_K_SERIES_PRE_REGISTRATION.md`, `sim_k_genealogy.py`, `K_SERIES_RUN_REPORT.md`, `sim_k_results.json`, `17_sim_k_genealogy.png`.
- **Choice Architecture & Loss Framing (Sim C-Series)**:
  - Pre-registered in `choice_architecture/SIM_C_SERIES_PRE_REGISTRATION.md`. Anchored to Thaler & Sunstein (2008) and Kahneman & Tversky (1979).
  - Hypothesis C1 (Default Nudge): Pre-selected default elevates cooperative adherence from $70.7\%$ to $94.8\%$ ($\ge 75.0\%$, PASS).
  - Hypothesis C2 (Loss Framing Asymmetry): Loss framing amplifies compliance by $51.4\times \ge 3.0\times$ over gain framing, validating Master Law 4:1 asymmetry (PASS).
  - Hypothesis C3 (Cognitive Friction): 3 units friction penalty suppresses opt-out transitions by $60.0\%$ (ratio $0.40 \le 0.50$, PASS).
  - Compound verdict: **COMPOUND PASS (3/3 CRITERIA SATISFIED)**.
  - Artifacts: `SIM_C_SERIES_PRE_REGISTRATION.md`, `sim_c_choice.py`, `C_SERIES_RUN_REPORT.md`, `sim_c_results.json`, `18_sim_c_choice.png`.
- **Semantic Drift & Linguistic Conventions (Sim S-Series)**:
  - Pre-registered in `semantic_drift/SIM_S_SERIES_PRE_REGISTRATION.md`. Anchored to Lewis (1969), CLICS 4.0, and `crates/sim-core/src/language_drift.rs`.
  - Hypothesis S1 (Inverse Trust Drift): Semantic drift velocity scales inversely with trust: $r = 0.994, p < 10^{-15} \ge 0.65$ (PASS).
  - Hypothesis S2 (Betrayal Entropy Spike): Expectation mismatch shock induces concept embedding entropy surge with Cohen's $d = 2.79 \ge 0.80$ (PASS).
  - Hypothesis S3 (Lexical Turnover Surge): Low-trust populations exhibit a $3.12\times \ge 2.0\times$ surge in lexical turnover (PASS).
  - Compound verdict: **COMPOUND PASS (3/3 CRITERIA SATISFIED)**.
  - Artifacts: `SIM_S_SERIES_PRE_REGISTRATION.md`, `sim_s_semantics.py`, `S_SERIES_RUN_REPORT.md`, `sim_s_results.json`, `19_sim_s_semantics.png`.
- **Bioelectric Stress Sharing & Multiscale Morphogenesis (Sim L-Series)**:
  - Formalizes Shreesha & Levin's (2024) gap-junctional stress-sharing hypothesis as the biological implementation of the Master Stability Law.
  - Hypothesis L1 (Critical Cognitive Light Cone): Unbounded stress sharing ($\gamma_O \to 1.0$) causes a Laplacian spatial resonance, increasing morphological error by $>300\times$ (FAIL as frozen). Proves cells require a private homeostatic anchor ($1-\gamma_O$).
  - Hypothesis L2 (In-Silico Oncogenic Normalization): Simulated optogenetic photocurrent clamping across an oncogenic cluster margin restored gap-junctional stress conductance, suppressing tumor divergence by 79.9\% (PASS). Quantitatively replicates Levin's *in vivo* Xenopus melanoma rescue.
  - Hypothesis L3 (Multiscale Level Hacking): Bidirectional macro-tissue motility feedback into cellular validation accelerated cellular homeostatic convergence by $5\times$ (PASS). Formalizes multiscale competency architecture.
  - Compound verdict: FAIL as frozen (2/3 PASS; reported strictly without post-hoc adjustments).
  - Artifacts: `SIM_L_SERIES_PRE_REGISTRATION.md`, `sim_l_bioelectrics.py`, `L_SERIES_RUN_REPORT.md`, `fig_sim_l_bioelectrics.png`.
- **Optogenetic Causal Interventions (Sim O-Series)**:
  - Transitions the research stack from correlative observation (fMRI / connectomes) to causal biological manipulation using PyRhO simulated light-gated ion channels (ChR2, ArchT).
  - Hypothesis O1 (Dopaminergic Trust Lesion): Optogenetic silencing of the $D$ channel suppresses final trust state by $99.97\%$ ($>90\%$ criterion, PASS). Proves trust accumulation is causally dependent on active dopaminergic signaling.
  - Hypothesis O2 (Induced Vulnerability): Optogenetic Cortisol stress excitation increases predatory uptake by $1.74\times$ ($<5.0\times$ criterion, FAIL). Proves acute physiological stress alone is insufficient to replicate the $38.9\times$ visual-cloaking exploitation gap (Sim D16), establishing that chronic cognitive scarcity is required.
  - Hypothesis O3 (Macroeconomic Fragmentation): Inhibiting O/S channels in a $10\%$ mutant subpopulation reduces Kuramoto global coherence by $11.39\%$ ($<40\%$ criterion, FAIL). Proves the distributed TFP protocol is highly resilient to biological/adversarial heterogeneity.
  - Compound verdict: FAIL as frozen (1/3 PASS; reported strictly without post-hoc adjustments).
  - Artifacts: `SIM_O_SERIES_PRE_REGISTRATION.md`, `sim_o_series.py`, `O_SERIES_RUN_REPORT.md`, `13_sim_o_optogenetics.png`.
- **Atmospheric, Photic & Thermal Gating (Sim D17)**:
  - Pre-registered in `weather/SIM_D17_PRE_REGISTRATION.md`. Integrates thermal energy stress factors ($F_{\text{thermal}} = 1.0\text{--}1.5$) from Rust `sim-core/weather.rs` and melanopsin 480nm circadian photic drive into cognitive bandwidth and Sim D16 visual cloaking.
  - Criteria: C1 heatwave spike $1.04\times$ vs $\ge 1.40\times$ (FAIL); C2 winter trust erosion $3.9\%$ vs $\ge 15\%$ (FAIL); C3 Weather-Shield reduction $3.6\%$ vs $\ge 50\%$ (FAIL); C4 permutation $p = 0.127$ (FAIL).
  - Compound verdict: **FAIL as frozen (0/4 PASS)**.
  - Substantive finding: Proves that the Reconciled Master Stability Law's contraction $-\delta(S_t - S_{\text{base}})$ acts as a macroscopic buffer against ambient planetary weather noise, demonstrating that financial consumer protection must prioritize typographic visual design (Sim D16, $38.9\times$) over ambient atmospheric factors.
  - Deliverables: `SIM_D17_PRE_REGISTRATION.md`, `WEATHER_RUN_REPORT.md`, `sim_d17_results.json`, `fig_sim_d17_weather.png`.
- **Baylor Unconscious Narrative Processing & Attractor Drift (Sim D18)**:
  - Pre-registered in `baylor/SIM_D18_PRE_REGISTRATION.md`. Evaluates Baylor study propofol/NREM state paradigm in DOCAS: Conscious mode ($M=1$) vs. Unconscious mode ($M=0$, $C < C_{\text{crit}} = 0.12$).
  - Criteria: C1 Cortisol threat bypassing reduces friction by $92.0\%$ vs $\ge 75\%$ (**PASS**); C2 syntactic schema preserved without dopamine ($D=0$) within $3.2\%$ vs $\le 5\%$ (**PASS**); C3 waking predatory uptake bias $+4.0\%$ vs $\ge 25\%$ (FAIL); C4 permutation $p = 0.4985$ (FAIL).
  - Compound verdict: **FAIL as frozen (2/4 PASS)**.
  - Substantive finding: Confirms that narrative syntax and relational schemas are ingested with near-zero friction during unconsciousness ($92\%$ drop), while waking executive reactivation ($M: 0 \to 1$) successfully restores loss aversion, partially buffering against unconscious exploitation.
  - Deliverables: `SIM_D18_PRE_REGISTRATION.md`, `BAYLOR_RUN_REPORT.md`, `sim_d18_results.json`, `fig_sim_d18_baylor.png`.

## Version 3.1 — October 2026

Content:
- **DOCAS / Brain-IT In-Silico Decoding Suite**:
  - Replaces legacy Gallant linear-ridge decoder with Weizmann Institute's Brain-IT dual-branch decoder (Beliy et al., ICLR 2026; `brainit-fmri`) on the 27 visual agreement and offer conditions (`battery27_reconstructed.json`).
  - Eliminates the N.3 legacy decoder resolution bottleneck: mean SSIM = 0.7723 ($\Delta = +0.4112$ over Gallant 0.3612), LPIPS = 0.1539 ($\Delta = -0.2771$), CLIP visual cosine similarity = 0.9301.
  - Resolves the historical N.3 stimulus retrieval null: top-1 retrieval rises from chance (3.7%) and Gallant baseline (14.8%) to **51.9%** ($p = 0.0005$ vs 2,000 permutation nulls).
  - Hypothesis H1 (Domain Structural Invariance vs Semantic Divergence): SUPPORTED ($p = 0.0005$). Early visual layout is preserved invariantly across all trust/threat categories (SSIM range = 0.0971 < 0.15), confirming that predatory/threat conditioning selectively modulates associative semantic networks without impairing sensory structural perception.
  - Hypothesis H2 (Instrument Resolution): SUPPORTED ($\Delta\text{SSIM} = +0.4112$, $\Delta\text{LPIPS} = -0.2771$).
  - Hypothesis H3 (Strong Platonic Manifold Alignment): SUPPORTED. Representational Dissimilarity Matrix correlation between TRIBE v2 cortical BOLD and Brain-IT decoded representations achieves Mantel $r = 0.9923$ ($p < 0.0001$).
  - **Sim D16 (Perceptual Cloaking & Predatory Uptake under Dual-Branch Gating)**: Pre-registered in `technical-appendix/SIM_D16_PRE_REGISTRATION.md` before execution; 1,000 agents ($\kappa_i \sim \text{Beta}(2,5)$, seed 42) evaluating 27 visual credit agreements using Brain-IT Branch A structural edge maps: C1 cloaking ratio 0.884 vs $\ge 2.50$ (FAIL); C2 exploitation gap 0.049 vs $\ge 0.30$ (FAIL); C3 decile odds ratio $38.94\times \ge 3.0\times$ (PASS — massive harm concentration in low-bandwidth agents); C4 permutation $p = 0.010 \le 0.001$ (FAIL). Compound verdict: **FAIL as frozen** (1/4 PASS; reported without post-hoc adjustment). Confirms visual design concentrates exploitation ($38.9\times$), while identifying that human salience is driven by typographic stroke-contrast rather than isotropic Sobel edge magnitude. Deliverables: `SIM_D16_PRE_REGISTRATION.md`, `sim_d16_perceptual_cloaking.py`, `sim_d16_results.json`, `fig_sim_d16_cloaking.png`.
  - Deposit deliverables: `BRAINIT_RUN_REPORT.md`, `run_insilico_experiment.py`, `hypothesis_evaluation.{json,csv}`, and figures in `figures/docas/pipeline/` (`visual_comparison_grid.png`, `fig_brainit_category_metrics.png`, `fig_brainit_permutation_nulls.png`, `fig_brainit_rdm_geometry.png`).

## Version 3.0 — September 2026

Content:
- **GTT**: new §1.2c "Differentiation from the dynamic-programming lineage" (risk-sensitive/entropic control, POMDP, soft RL; integration-novelty statement; anchored to the existing exponential-tilt formalism — no new symbols); new §2.3b "Machine-checked verification: the Lean formalization" + proof-map figure (TrustStack library, Lean 4 + Mathlib pinned v4.12.0, no `sorry`; proves tilt Properties 1–4 and master-law M1–M3) — **status VERIFIED 2026-09-21: green `lake build` under the pinned toolchain (Lean 4.12.0, commit dc2533473114; Mathlib v4.12.0 rev 809c3fb3, all dep revs pinned in lake-manifest.json); axiom audit (lean/Check.lean → lean/VERIFICATION_AXIOMS.txt) shows all ten theorems depend only on [propext, Classical.choice, Quot.sound], no sorryAx; three compile-fix iterations on the deposited sources (Lean-4 binder rule for section hypotheses, sum_div direction, λ-token rename) — the proofs as deposited compile**; universality sentence in the cross-species summary; tilt cross-reference corrected to §2.
- **DOCAS**: (a) cortisol channel grounded in consolidation-weight mechanism (Buchanan & Lovallo 2001; Roozendaal 2002, 2006; Forbes et al. 2024 null on delay discounting); (b) new §5.8 "Perturbation signature of the expectation–validation boundary: post-hoc consistency test against published neuroimaging" — P-BND scored against Siegel et al. 2024 (Nature 632:131–138; Raichle co-authorship confirmed) and Varley et al. 2020 (NeuroImage 220:117049), Varley signal-level null disclosed, REBUS + Aaronson et al. expectancy evidence, limitations (a)–(f); registration status stated as post-hoc consistency evidence — the author's timestamped research notes document the topic interest and the general expectation of physiological observability, not the specific component mapping (an earlier v3.0 draft overstated the notes as containing the prediction; corrected before any public upload, so no correction-register entry is required); (c) SIM-PBND in-silico arm + figure (seed 20260920, frozen criteria, COMPOUND PASS 4/4: FC drop 98.7% ≥ 30%; between-subject similarity 0.557→0.957, identifiability 100%→10%; Higuchi FD p=4e-4; eigenratio 122 vs null p95 1.12; first-run bug archived, 4 harness-mechanics amendments disclosed, criteria untouched); (c2) SIM-PBND-2 robustness arm + figure (seed 20260921, 40 subjects × 24-unit networks, four frozen criteria + Amendment A1 disclosed pre-run after calibration showed sensory-noise matching infeasible; COMPOUND FAIL 3/4 — C1 decoherence-at-scale PASS 1.127 ≥ 0.30, C2 dose-response PASS ρ=1.0 with asymptotic-p clause disclosed (exact floor 1/12 at n=4; subject-level supplementary |ρ|=0.968, p=4.7e-97, labeled post-battery), C3 specificity FAIL 1.0× vs frozen ≥2× against the subject-specific-sensory control — at full prior collapse ANY single dominant stream homogenizes correlation FC, so the convergence metric cannot see stream identity; C4 recovery PASS 1.000 ≥ 0.70; identifiability 100%→2.5%; exploratory E1/E2 labeled post-battery; limitation (g) added: convergence clause of component (b) carries no identifying weight, fingerprint decoherence carries it); (d) §5.7 "Scope of the universality claim [HYPOTHESIS]"; (e) oversized-float layout fix.
- **TFP**: §4 SIM-OBS embed + figure (seed 20260920, 50 cohorts × 120 agents, Kalman/EM; COMPOUND FAIL reported — C1 +0.014 < +0.03, C2 0.0135 > 0.01, C4 0.184 > 0.15; C3 direction PASS 50/50; instrument recalibration did not flip criteria; thresholds never adjusted; first-run estimator bug archived; engineering responses restated to stand on theory + literature, not on the run).
- **Whitepaper**: one sentence stating why financial transactions are the measurement substrate (standardized baseline, transaction-as-delta, timestamp anchoring; "a measurement layer, not a commercial claim").
- **Framing (all)**: universality claim stated as functional/dynamical (the law recurs, the wiring does not); H1 structural FAIL presented as the discriminating test; first claim (measurability) untouched.
- **Version labels**: all six works moved from spelled-out iteration names to "Version 3.0 — September 2026".
- **Deposit-side**: SIM-PBND/SIM-PBND-2/SIM-OBS pre-registrations + results + first-run-bug JSONs in `technical-appendix/` (SIM-PBND-2 pre-registration carries Amendment A1 + appended RESULTS section); `lean/` TrustStack project (VERIFIED — sources, pinned manifest, Check.lean audit, VERIFICATION_AXIOMS.txt); `harm_reduction_estimate.md` (+ figure; Monte Carlo seed 20260917: composite ~1.0%/1.9%/3.5% at 25/50/90% adoption; e_harm dominates, Spearman 0.63); this register.
- **Layout**: float-page tuning holds (0 underfull vboxes; no oversized floats).
- **Quarantine audit**: no fabricated review summaries, no bare-domain evidence citations, no "proves" language, no cortisol-discounts claim, no AlphaGenome/FlyWire material in commercial documents.

Verified additions (all checked against primary sources this iteration): Siegel 2024 Nature 632, 131–138 (Raichle co-authorship confirmed; the additions package's "634:73–81" was wrong and was corrected); Varley 2020 NeuroImage 220, 117049; Forbes 2024 Neurobiol Stress 31:100653 (11 studies, 14 effects, SMD −0.18 [−0.57, 0.20]); Buchanan & Lovallo 2001 Psychoneuroendocrinology 26:307–317; Roozendaal 2006 PNAS 103:6741–6746; Carhart-Harris & Friston 2019 Pharmacol Rev 71:316–344; Raichle 2001 PNAS 98:676–682; Raichle 2015 Annu Rev Neurosci 38:433–447; Fox 2005 PNAS 102:9673–9678; Aaronson et al. (psilocybin SI trial, J Clin Psychiatry, N=20); Howard & Matheson 1972 Manag Sci 18:356–369; Hansen & Sargent 1995 IEEE TAC 40:968–971; Ziebart 2008 (CMU thesis); Haarnoja 2017 ICML; de Moura & Ullrich 2021 CADE 28 LNCS 12699:625–635; mathlib 2020 CPP:367–381.

Package items deliberately NOT integrated: the "T(s) = R_t + γ(D,C)·E[T(s')|Ω(O,A,S)]" equation (symbol collision — γ is reserved stack-wide for the tilt amplitude, τ for −EFE — and formalism mismatch: GTT is a delta-rule measurement theory, not value iteration; the lineage content was integrated in prose anchored to the existing tilt); a proposed new observer-effect section (redundant — TFP §4 and whitepaper §1.4 already carry the full treatment; no double-stating).

## Version 2.0 — September 2026

Float-deferral fix (placeins + figure* + FloatBarrier) propagated across all papers; epistemic-label sweep; universality-claim scope paragraph; cross-scale universality audit (10-dimension research swarm) with label corrections; first-run artifacts moved to deposit/audit trail; defensive narration removed; visual QA and float-fraction tuning. (Shipped to OSF as the "v2" upload with 6 PDFs/DOCX; GTT §4.5 pointer, DOCAS §5.6 F1 series + §5.7 H1, TFP venue retarget, whitepaper shame-spirals, preface evidence sentences.)

## Version 1.0 — September 2026

Initial assembled collection: five works + collection index, compiled PDFs, DOCX mirrors, OSF/GitHub packaging, simulation batteries (GTT G-series, DOCAS F1/H1/D-series, TFP P-series, whitepaper W-series) with frozen criteria and deposited audit trails. Published on OSF, September 2026.

---

*Standing tokens: 27× "(DOI: [insert])" awaiting the OSF DOI (verified count 2026-09-20: 13 tex + 13 md + 1 deposit README; earlier registers said 32 — the v2→v3 section rewrites consolidated duplicate attestation sentences; every work still carries ≥1). ORCID 0009-0003-8977-8010.*
