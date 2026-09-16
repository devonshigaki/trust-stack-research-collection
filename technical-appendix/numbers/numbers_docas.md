# DOCAS Simulation Battery — Re-run Numbers (SIM-D)

**Re-run agent:** SIM-D. **Environment:** numpy 2.2.5 / scipy 1.16.2 / matplotlib 3.10.3, **seed 42** throughout.
**Sources:** revised paper `/mnt/agents/output/revised/docas_revised.md` (§2.9 operators, §5, Sims D1–D13);
master law preset `/mnt/agents/work/math/math_repairs.md` §M4; prior runs `/mnt/agents/work/sims/sim_results_A.md`.
**Data:** CLICS 4.0 CLDF cloned from github.com/clics/clics4 (this session); 1,730 concepts, 51,562 colexification edges — counts match the paper exactly.
**Honesty note:** the original Sim D1–D13 code is not in the workspace; all loops/decoders are faithful reconstructions from the printed §2.9/§5 specs. Where the original's internal settings (noise levels, episode shapes, full A-concept list) are not printed, reconstruction choices are disclosed. All deviations below are attributed to reconstruction details unless stated.

---

## Row-by-row: claim vs re-run

| # | Claim (revised paper) | Re-run result (seed 42) | Verdict |
|---|---|---|---|
| **1. Operator composition** | D/O/C/A/S operators compose into the master law DOCAS preset (§2.9) | Composed loop vs direct ML (S += λ r ε − δ_S(S−S_base)), same realization: **max |ΔS| = 4.4e-16** over 2000 steps | **PASS** (exact, as claimed "identical by construction") |
| **1b. Proven limit** | GTT preset recovered as δ_S→0, r→1 (proven, not constructed) | Forcing r≡1 (θ_C→−∞) and scanning δ_S ∈ {0.2…0.001, 0}: max deviation from GTT trajectory decreases monotonically to **exactly 0 at δ_S=0**; approach is sublinear in max-norm at small δ_S (leak-free limit is an unbounded random walk, so errors accumulate — stated honestly) | **PASS** (figD_operators_masterlaw.png) |
| **2. Sim D1 H4 (decodability)** | r = 0.947 (per-channel 0.946–0.947), σ_obs=0.1, threshold r ≥ 0.7 | r = **0.917** (per-channel 0.916–0.920), 200 episodes | **PASS on criterion; DEVIATION on value** (−0.03; original generative details — bump widths/amplitudes/episode length — not printed) |
| **2b. Sim D1 H5 (ordering)** | 100% exact order, mean Kendall τ = 1.0, thresholds ≥70% / τ ≥ 0.7 | **100%** exact, **τ = 1.0000** | **PASS (exact)** |
| **2c. Sim D1 H6 (minority robustness)** | doubled minority U(0.1,0.3): r = 0.936 | r = **0.902** | **PASS on criterion; DEVIATION on value** (same reconstruction gap) |
| **2d. Noise sweep** | r = 0.99/0.95/0.83/0.59 at σ = 0.05/0.1/0.2/0.4 | r = **0.977/0.917/0.757/0.503** | **PASS qualitatively** (graceful degradation, above threshold to σ≈0.2); DEVIATION on values, monotone ordering preserved |
| **2e. Honest null (added)** | chance r ≈ 0 | shuffled mixing matrix: ch-D r = **0.054** | **PASS** (null behaves) |
| **3. Sim D10 E2 (lesions, FROZEN criterion)** | Frozen criterion (each lesion degrades own metric ≥2× any other) **FAILED** originally: O ratio 1.01, C ratio 0.72 | Re-run: **FAILS honestly.** Ratios: D 233.0, A 7.91, S ∞ (dissociate); **O 0.50 FAIL** (collapses expectation-tracking D metric more than its own — loop edge O→D); **C −0.01 FAIL** (own detector metric untouched while downstream channels move) | **FAIL reproduced (as frozen)** — same two violating channels as the original; quantitative ratios differ (reconstructed metrics/lesion implementations differ; disclosed) |
| **3b. Cascade signature (POST-HOC)** | Violating edges = loop edges O→D, C→S; hypothesis generation only | POST-HOC, labeled: O lesion's largest cross-channel displacement is on **O→D (confirmed)**. C-lesion displacement propagates downstream (A 0.82, S 0.55 normalized) but largest is **C→A, not C→S** in this reconstruction; D/A lesions' largest downstream displacement lands on **S (the loop's integrator)** | **PARTIALLY CONSISTENT — POST-HOC ONLY, no evidential weight** (figD_lesions.png) |
| **4. Sim D10 E1 (planted λ)** | slope 0.348 vs planted λ=0.35, R²=0.970 | slope = **0.3502**, R² = **0.975** (40 replicas × 2000 steps, state noise σ_S=0.01 chosen to match the original's R² regime; σ_S=0.02 → R²=0.907, σ_S=0.005 → 0.994) | **PASS** (figD_lambda_recovery.png) |
| **4b. Sim D10 E3 (negative control)** | shuffle destroys law in 200/200 replicates | **200/200 destroyed** (max R²=0.0060, max |slope|=0.028) | **PASS (exact)** |
| **4c. Sim D12 (spiking/eligibility)** | slope 0.174, R²=0.664, pre-registered eligibility rescaling; 100/100 control nulls | Brian 2 NOT available → **numpy three-factor eligibility-trace stand-in (disclosed, not Brian 2)**. Planted λ=0.174 (pre-registered rescaling, not a λ estimate): slope = **0.1743**, R² = **0.874**; controls **100/100** null (max R² 0.006) | **PASS on slope + controls; DEVIATION on R²** (0.874 vs 0.664 — expected: rate-based stand-in ≠ spiking Brian 2 network) |
| **5. CLICS4: C Recognition set** | density 0.524 (15× bg), p=0.0005 | Under Family≥3 filter: **0.5238 (11/21 pairs), p=0.0005** — EXACT. Named edges verified: KNOW–UNDERSTAND 27 families ✓, HEAR–UNDERSTAND 29 ✓, SEE–FIND 25 ✓ | **PASS (exact)** — but this is the known perception→cognition universal, not novel evidence (per paper's own repositioning) |
| **5b. D Expectation** | 0.333, p=0.008 | **0.3333 (1/3), p=0.0075** | **PASS (exact)** |
| **5c. O Validation** | 0.333, p=0.0005 | **0.3333 (5/15), p=0.0005** | **PASS (exact)** |
| **5d. A Activation** | 0.061, p=0.0005 | printed list truncated ("…") — with the 7 printed concepts: **0.1429 (3/21), p=0.0005**; full graph 0.3333 | **DEVIATION — printed list is incomplete (truncated in the paper); printed density 0.061 implies a larger set than printed. Cannot reproduce exactly from the printed set. FLAGGED to writer.** |
| **5e. S Stabilization** | 0.048, p=0.054 (marginal) | With the 6 printed concepts under Family≥3: **0.000 (0/15 edges), p = 1.0 — NULL**; under full graph: 0.200, p=0.029 | **DEVIATION — honest NULL under the paper's own stated filter.** Printed 0.048 ≈ 1/21 implies a 7-concept set (list truncated). As printed, S has NO ≥3-family edges — weaker than the paper's "marginal." FLAGGED. |
| **5f. C + mismatch (SURPRISED/MISTAKE/WRONG)** — the set the paper names as "the real test" | not run in paper (registered follow-up) | **NEW RESULT:** Family≥3: density **0.2667 (12/45), p = 0.0005**; full graph: 0.3556, p=0.0005 | **PASS (significant)** — the mismatch-augmented Recognition set IS a significant lexical attractor; supports registering it as the follow-up |
| **5g. Background density** | "whole-graph background density 0.034" | Full graph: 0.0345 ✓ matches. **But under the paper's own stated ≥3-family filter the background is 0.0027** — the printed "0.034" is the UNFILTERED density while the printed within-set densities match the FILTERED graph | **INTERNAL INCONSISTENCY in the paper's method sentence — FLAGGED to writer.** (C's "15× background" becomes 196× under consistent filtering; the significance verdicts are unchanged.) |
| **5h. Adjacent vs non-adjacent channel pairs** | adjacent colexify at 2.4× non-adjacent (0.026 vs 0.011) | Family≥3: **0.0258 vs 0.0119, ratio 2.17×** (close); permutation test on the ratio (2000 label shuffles): **p = 0.061 — marginal**; full graph: ratio 1.09× (absent) | **DEVIATION/WEAKENED: ratio reproduces but is marginal (p=0.061), not clearly significant. "Weakly present" wording is correct; must not be upgraded.** |
| **5i. Gloss-mapping choices (disclosed)** | — | KNOW→KNOW (SOMETHING); CORRECT→CORRECT (RIGHT); FEAR→FEAR (BE AFRAID); CALM→CALM (OF SEA) [only gloss]; SURPRISE→SURPRISED [nearest]. Sensitivity: FEAR (FRIGHT) → A density 0.1905 (fam≥3); SLEEP (STATE) → S still 0.000 | Disclosed; conclusions unchanged |
| **6. TRIBE v2 fMRI runs (Sims D8/D9/D11/D13, §5.2 batteries)** | external model weights | **EXTERNAL-MODEL — NOT re-run.** Requires released TRIBE v2 checkpoint + tribev2-rs; no substitute simulated (per instructions, simulating a substitute would fabricate) | **EXTERNAL-MODEL** |

---

## Figures (all 150 dpi, captioned on-figure)

- `figD_operators_masterlaw.png` — Item 1: operator composition = master law (identity 4.4e-16); trajectories → GTT limit; convergence vs δ_S.
- `figD_lambda_recovery.png` — Item 4: E1 planted-λ regression; E3 shuffle controls; D12 eligibility stand-in.
- `figD_lesions.png` — Item 3: metric-drop matrix and frozen-criterion ratios; FAIL labeled on-figure; post-hoc cascade labeled.
- `figD_decoder_selfconsistency.png` — Item 2: H4/H6 decodability, noise sweep, H5 ordering + shuffled-mixing null; SELF-CONSISTENCY and planted-structure disclosure on-figure.
- `figD_clics_colexification.png` — Item 5: within-set densities under both filters with permutation p-values; background-inconsistency and known-universal caveats on-figure.

## Items marked

- **DATA-REQUIRED:** none — CLICS4 download succeeded and the analysis ran on the real data.
- **EXTERNAL-MODEL:** TRIBE v2 fMRI runs (Sims D8, D9, D11, D13 and §5.2 rounds M/N) — not re-runnable here; no substitute simulated.

## Headline deviations for the lead

1. Frozen double-dissociation **FAILS in the re-run too** (O ratio 0.50, C ratio −0.01) — the paper's honest-failure posture is corroborated; the post-hoc cascade signature is only partially consistent in this reconstruction (O→D confirmed; C's largest downstream hit is A, not S).
2. CLICS: printed C/D/O densities and p-values reproduce **exactly** on real CLICS4 data under the ≥3-family filter; **S is a full null (p=1.0) as printed** (worse than the paper's "marginal 0.054" — printed S list appears truncated); **A cannot be reproduced from the truncated printed list**; the paper's "background 0.034" is the unfiltered density — internally inconsistent with its own stated filter (verdicts unchanged).
3. The mismatch-augmented Recognition set (the paper's named "real test") **passes strongly** (p=0.0005, both filters) — new result supporting the registered follow-up.
4. Adjacency ordering 2.4× reproduces as 2.17× but is **marginal (perm p=0.061)** — keep "weakly present."
5. Sim D1 decoder: all thresholds pass; absolute r values ~0.03 below the originals (reconstruction gap; original generative settings not printed).
