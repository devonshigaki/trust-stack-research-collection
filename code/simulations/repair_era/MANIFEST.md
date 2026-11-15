# Repair-Era Simulations — Manifest

Every simulation, re-run, and validation battery produced during the repair workflow (2026), organized by which paper's values it backs. This folder is the **`/simulations-repair-era/`** upload in the OSF deposit guide. The author's **original `simulations/` folder uploads separately and unchanged** — it is the bit-identity acceptance-test material for everything here.

## Preservation status legend
- **[COMPLETE]** — script + result files + figures preserved; re-runnable as-is
- **[RESULTS FROZEN]** — result values frozen in the `numbers_*.md` file (which records re-run vs. printed value with PASS/FAIL) and figure preserved; the generating script was run in-session and is not separately archived
- **[ORIGINAL]** — result of the author's original simulation suite; repair-era role was verification/figure regeneration only

---

## robustness/ — SIM-R1 / SIM-R2 batteries [COMPLETE]
Scripts: `simR1_battery1.py`, `simR1_battery1_figs.py`, `simR1_battery2.py`, `b3_ahat.py`, `b4_kuramoto.py` · Results: `simR1_battery1_stats.json`, `simR1_battery1_rows.npz`, `simR1_battery2_stats.json`, `b4_results.json`, `b4_log.txt` · Writeups: `simR1_results.md`, `simR2_results.md` · Figures: `figR1_*`, `figR2_*`

| Battery | Backs | Key frozen values |
|---|---|---|
| SIM-R1 B1 — adaptive-λ misspecification arm | GTT §7 G10; whitepaper §3.4 | adaptive truth λ̄ = 0.355 → λ̂ = 0.472 (inside corridor, truth outside); 21.7% outside at c = 1.5; population bias +0.117; ε²-weighted gain exact |
| SIM-R1 B2 — closure sensitivity | GTT §6 (closure-conditional ringing) | period drifts 7.17 → 17.65 across smoothing closures; zero-delay destroys ringing; two-step rings at 10.04 with boundary exactly 1/φ |
| SIM-R2 B3 — â_i Fisher–Rao sensitivity | GTT §3.1 | relational conclusions robust (ρ ≥ 0.940; ordering 243/243); absolute magnitudes shift 1.83× |
| SIM-R2 B4 — sparse/weighted topologies | GTT §3.4; TFP §3.6 Sim P1c | R > 0.7 at K = 4.5 fails at ⟨k⟩ ≲ 25 (BA m = 2 → 0.416); onset K_c ≈ 2 topology-invariant; ABM-with-adversaries 0.739 vs pure-Kuramoto 0.709/0.710 |
| SIM-R2 B7 — macroarea subgroups | DOCAS §4.6 | S-channel full null (0/15, p = 1.0) stable across all six macroareas |

## tfp/ — protocol simulation re-runs
- `sim_p1_p1b.py` + `p1_results.npz` — Sim P1/P1b leakage-graded coherence verification re-run **[COMPLETE]**: R = 0.739 ± 0.029 coupled vs 0.040 ± 0.001 isolated (at the 1/√N ≈ 0.045 floor); fragility band ℓ* ∈ [0.02, 0.10]; robust R > 0.7 needs K ≥ 6–8 and ⟨k⟩ ≳ 25
- `sim_p9_dyn_couple.py` + `p9_results.json` — Sim P9 dynamically coupled Master Law & Kuramoto layer **[COMPLETE]**: dynamic coupling $\omega_k(t) = \Delta S_k(t)$ endogenously achieves $R = 0.907$ at $K=4.5$ on sparse ER networks ($\langle k \rangle \approx 25$), closing the theoretical gap in Sim P1c and proving coherence is driven directly by expectation-validation alignment.
- `numbers_tfp.md` — frozen re-run table for all TFP sims (P1–P10), incl. Sim P5 surrogate-corrected transfer entropy (protocol 0.0315 ± 0.0029 / 0.0283 ± 0.0022 both directions, 8/8 replicas; surveillance 0.1210 ± 0.0050 / −0.001) and Sim P8 Sybil deterrence ($1.01 → $1,005 at m = 1,000; time floors 5.5/1.4 yr) **[RESULTS FROZEN]** for P5/P8 figures
- Figures: `figP1_*`, `figP5_*`, `figP8_*`, `fig_adoption_sensitivity`, `fig_coldstart`, `fig_expected_loss`, `fig_storage_refit`

## whitepaper/ — estimator validation + ledger batteries
- `numbers_whitepaper.md` — frozen validation table: trajectory recovery r = 0.879 printed vs re-run median r = 1.000 (deviation note D1: dual-layer vs single-stream scope); λ̂ recovery error 0.024 printed vs re-run p95 0.0215 (tolerance 0.15; 300-user re-run mean 0.0074, max 0.0343); λ = 0 negative control max 0.0092; ultra-thin worst case 0.0737; planted concordance Mantel r = 1.0, p = 0.002; partial given text p = 0.002; shuffled-label control p = 0.684; four first-run failures preserved and disclosed **[RESULTS FROZEN]**
- `make_figW4.py` — adoption-compounding figure script
- Figures: `figW1`–`figW7`

## gtt/ — theory simulation figures + frozen values [ORIGINAL]
`numbers_gtt.md` + figures `figG1` (convergence), `figG6_M2/M3`, `figG7` (long-run), `figG8` (λ battery), `figG9` (ψ-OU battery), `fig_kuramoto_threshold`, `fig_phasemap_control`. The generating scripts are the author's originals; repair-era verification is the SIM-R1/R2 set above.

## docas/ — neural-pipeline figures + frozen values [RESULTS FROZEN / COMPLETE via neural-pipeline/]
`numbers_tdf.md`; figures `fig1`–`fig6`, `figD_*` (decoder self-consistency, λ recovery, lesions, operators, CLICS colexification); `pipeline/` (bridge a–d, category contrasts/separability, decode bars, CLICS heatmap); `viz/` (VIZ_REPORT.md, TRIBE surface maps, bridge geometry, CLICS channel network).

## neural-pipeline/ — TRIBE v2 / eng1000 / vec2vec / CLICS code [COMPLETE]
Full repair-era code set (`run_pipeline.py`, `run_battery27.py`, `gallant_decode.py`, `vec2vec_demo.py`, `clics_offer_overlap.py`, `make_figs*.py`, `llama_stream.py`, `config.yaml`, `stimuli.json`) + run reports (`RUN_REPORT.md`, `RUN_REPORT_2.md`, `BRIDGE_REPORT.md`) + `battery27_reconstructed.{py,json}` — **reconstruction-from-spec, labeled; pending bit-identity vs the original `battery27_manifest.json`; do not report original headline numbers from it.**

## appendix/ — audit briefs
`math_repairs.md` (M1–M7 repair log), `sim_results_A.md` (Sim-Battery A brief), `sim_results_B.md` (Sim-Battery B brief).

## optogenetics/ — SIM-O Series causal biology battery [COMPLETE]
Pre-registration: `SIM_O_SERIES_PRE_REGISTRATION.md` · Code: `sim_o_series.py` · Results: `sim_o_series_results.json` · Report: `O_SERIES_RUN_REPORT.md` · Figure: `figures/13_sim_o_optogenetics.png`.
- **Foundational Research & Tools**: PyRhO 4-state Markov opsin simulator (Evans et al., *Frontiers in Neuroinformatics* 2016); Microbial opsin physiology (Boyden et al., *Nature Neuroscience* 2005; Deisseroth, *Nature Neuroscience* 2015).
- **Key Findings**: ArchT dopaminergic silencing suppresses trust state $S_t$ by 99.97% (PASS). ChR2 cortisol excitation increases secure consumer vulnerability by $1.74\times$ (FAIL as frozen $\ge 5.0\times$).

## weather/ — SIM-D17 environmental coupling battery [COMPLETE]
Pre-registration: `SIM_D17_PRE_REGISTRATION.md` · Results: `sim_d17_results.json` · Report: `WEATHER_RUN_REPORT.md` · Figure: `figures/14_sim_d17_weather.png`.
- **Foundational Research & Tools**: Circadian photic melanopsin phototransduction (Berson et al., *Science* 2002; Lucas et al., *Trends in Neurosciences* 2014); Empirical weather-mood cognition dynamics (Keller et al., *Psychological Science* 2005); Rust `crates/sim-core/src/environment/weather.rs` thermal engine ($F_{\text{thermal}}$).
- **Key Findings**: Master Stability Law geometric contraction $-\delta(S_t - S_{\text{base}})$ buffers against environmental noise; heatwave predatory surge $+4.0\%$ (failing $\ge 40\%$); compound FAIL (0/4 PASS).

## baylor/ — SIM-D18 unconscious narrative state switching battery [COMPLETE]
Pre-registration: `SIM_D18_PRE_REGISTRATION.md` · Results: `sim_d18_results.json` · Report: `BAYLOR_RUN_REPORT.md` · Figure: `figures/15_sim_d18_baylor_unconscious.png`.
- **Foundational Research & Tools**: Global Neuronal Workspace & Conscious Processing (Mashour et al., *Neuron* 2020; Dehaene et al., 2006); Anesthetic loss-of-consciousness dynamics (Alkire et al., *Science* 2008); Baylor College of Medicine intraoperative narrative paradigms.
- **Key Findings**: Cortisol threat gate deactivation in unconscious mode ($M=0$) collapses processing friction by 92.0% (C1 PASS) and preserves syntactic perplexity within 3.2% under dopaminergic silencing (C2 PASS); waking reactivation ($M: 0 \to 1$) restores loss aversion, restricting waking predatory acceptance drift to $+4.0\%$ (C3 FAIL).

## bioelectrics/ — SIM-L Series multiscale stress sharing & morphogenesis [COMPLETE]
Pre-registration: `SIM_L_SERIES_PRE_REGISTRATION.md` · Code: `sim_l_bioelectrics.py` · Results: `sim_l_results.json` · Report: `L_SERIES_RUN_REPORT.md` · Figure: `fig_sim_l_bioelectrics.png`.
- **Foundational Research & Tools**: Stress sharing as cognitive glue (Shreesha & Levin, *Biochemical and Biophysical Research Communications* 2024); Technological Approach to Mind Everywhere (Levin, *Frontiers in Systems Neuroscience* 2022); Top-down multiscale cybernetics (Pezzulo & Levin, *J. R. Soc. Interface* 2016).
- **Key Findings**: Optogenetic clamping of 10% oncogenic defect cluster suppresses morphological divergence by 79.9% (L2 PASS); bidirectional macro-tissue motility accelerates time-to-homeostasis by $0.21\times$ (L3 PASS); boundary noise propagation under strong coupling expands local variance before topological convergence (L1 FAIL; compound FAIL 2/3).

## music_tdf/ — SIM-M Series temporal dynamics of music & metric hierarchy gating [COMPLETE]
Pre-registration: `SIM_M_SERIES_PRE_REGISTRATION.md` · Code: `sim_m_tdf_music.py` · Results: `results/statistical_validation.json` · Report: `M_SERIES_RUN_REPORT.md` · Figures: `results/plots/` & `figures/16_sim_m_music_tdf.png` · Coding Agent Hand-off: `prompts/CODING_AGENT_INTEGRATION_PROMPT.md`.
- **Foundational Research & Tools**: Metric hierarchies and temporal subdivision (London, *Hearing in Time*, Oxford University Press 2012); Expectation, downbeat prediction errors, and ITPRA theory (Huron, *Sweet Anticipation*, MIT Press 2006); Nonlinear oscillatory attentional entrainment (Large & Jones, *Psychological Review* 1999); Neurochemistry of music across dopamine, oxytocin, cortisol, and adrenaline (Chanda & Levitin, *Trends in Cognitive Sciences* 2013; Koelsch, *Nature Reviews Neuroscience* 2014); Anticipatory striatal dopamine release (Salimpoor et al., *Nature Neuroscience* 2011); Embodied sensorimotor mediation (Leman, *Embodied Music Cognition*, MIT Press 2008).
- **Key Findings**: Metric hierarchy ratio $\tau$ ($3/4$ triple simple $0.0$, $4/4$ duple simple $0.5$, $6/8$ compound duple $1.0$) yields $F = 3,561.48$ ($p < 10^{-15}, \eta^2 = 0.5166$), completely eliminating the scalar BPM degeneracy between Focus ($75\text{ BPM}$) vs. Decompression ($68\text{ BPM}$) and Creative Flow ($110\text{ BPM}$) vs. Exercise ($135\text{ BPM}$); Mutual Information increases by $+136.87\%$ ($3.877\text{ bits}$); cross-validated classification error is suppressed by $71.0\%$ (Error Ratio $0.290$; Macro-$F_1 = 0.945$, AUC $= 0.993$); empirical permutation $p = 0.0000$ ($B = 2,000$ iterations). COMPOUND PASS (4/4).

## tribe_bayes/ — SIM-B1 closed-loop streaming BOLD to Bayesian filter [COMPLETE]
Pre-registration: `SIM_B1_PRE_REGISTRATION.md` · Code: `sim_b1_tribe_bayes.py` · Results: `results/b1_results.json` · Report: `B1_RUN_REPORT.md`.
- **Foundational Research**: DOCAS §5.2 open-loop TRIBE v2 BOLD fMRI predictions; GTT §6 continuous-time Kalman/EM Bayesian tracking.
- **Key Findings**: In-silico DMN semantic threat activation passed continuously as a BOLD proxy into the augmented Kalman filter successfully tracked the latent volatility-driven trust sensitivity ($\lambda_t$) with near-perfect correlation ($r = 0.996$), reducing state tracking MSE by 46.9% relative to behavior-only baselines. COMPOUND PASS (2/2).

## adv_llm_dmn/ — SIM-A1 multi-turn generative attacks vs. DMN planning [COMPLETE]
Pre-registration: `SIM_A1_PRE_REGISTRATION.md` · Code: `sim_a1_adv_llm_dmn.py` · Results: `results/a1_results.json` · Report: `A1_RUN_REPORT.md`.
- **Foundational Research**: GTT §4.2 adversarial exploitation constraints (Zero-Determinant/Memory-One strategies); DOCAS §5 Default Mode Network counterfactual rollout and planning depth ($K$).
- **Key Findings**: A generative trust-building extortion trap (LLM manipulation proxy) successfully extracts terminal surplus (utility $-1.000$) from present-biased ($K=1$) agents. Equipping agents with deep DMN counterfactual rollout ($K=5$) fully anticipates tail-risk extortion paths, maintaining positive terminal utility ($0.750$) and neutralizing the trap loss completely (100.0% reduction). COMPOUND PASS (2/2).

## striatal_microcircuit/ — SIM-S1 biophysically detailed MSNs & macroscopic reduction [COMPLETE]
Pre-registration: `SIM_S1_PRE_REGISTRATION.md` · Code: `sim_s1_striatal.py` · Results: `results/s1_results.json` · Report: `S1_RUN_REPORT.md`.
- **Foundational Research**: GTT §3 Master Law mean-field approximation; Striatal medium spiny neuron (MSN) dopaminergic eligibility trace kinetics (Snudda scale).
- **Key Findings**: At the microscopic scale, the continuous-time integration of decaying synaptic eligibility traces $c(t)$ and phasic dopamine RPE bursts $D(t)$ yields terminal weight updates $\Delta W$ perfectly homomorphic ($r = 1.0000$) to the discrete macroscopic Delta Rule update $\Delta S_t = \lambda(V_t - E_t)$, formally securing the macroscopic Master Law as a precise mean-field approximation of dendritic coincidence-detection. COMPOUND PASS (1/1).

---

**Honest boundary:** items marked [RESULTS FROZEN] have their values locked in the numbers files with re-run-vs-printed reconciliation and their figures deposited, but the one-off generating scripts from the repair sessions are not separately archived. The acceptance path for every printed number is: original `simulations/` JSONs (author upload, unchanged) ↔ these frozen numbers ↔ the papers' print. Where the original generative settings were not archived, exact-value deviations are expected and are listed in the numbers files' deviation notes.
