# SIM-R2 — Robustness Batteries 3–7: Results

**Agent:** SIM-R2. **Environment:** numpy 2.2.5 / scipy 1.16.2 / matplotlib 3.10.3 / statsmodels 0.14.5, **seed 42** throughout.
**Sources read first:** `work/math/math_repairs.md` (§M4 master law, §M6 stage-activity simplex, §M7 stereographic map), `work/sims/sim_results_B.md`, `revised/gtt_revised.md` §3.1/§3.4, `revised/whitepaper_revised.md` §4.7 (+§1.1–1.2, §2.1–2.3, §4.5), `figures/docas/numbers_docas.md`, `revised/docas_revised.md` §2.9/§4.6/§5.2.
**Data:** CLICS 4.0 CLDF edge list (`colexifications.csv`, 51,562 edges / 1,725 concept nodes — matches the paper's re-run-verified counts exactly) + `languages.csv` (Glottolog macroarea/family metadata), fetched raw from github.com/clics/clics4 this session (full-repo clone blocked by a 100 MB download cap; the precomputed CLDF edge list and language metadata suffice and are the paper's own data source).

---

## BATTERY 3 — â_i reference-scale sensitivity of the Fisher–Rao simplex (GTT §3.1)

**Disclosure first:** the papers mandate "pre-registered reference scales â_i" (GTT §3.1; §M6.2) but **never print their values anywhere in the stack**. The nominal set used here is therefore a *disclosed reconstruction choice*, not a recovered registration: â = (1.0, 0.7, 0.5, 0.5, λ·0.5 = 0.175) for (D, O, C, A, S) = (Π, γ_O, C, g_A·f, λr) — mid-range operating values of each channel.

**Model (DOCAS preset of the master law, §M4; operators per DOCAS §2.9; reconstruction disclosed).** T = 400 steps; validation stream V_t = γ_O,t·s_t with s_t AR(1) (ρ = 0.9, σ = 0.3); a betrayal shock of −1.5/−3/−6 at t = 200 defines three conditions (8 episodes each, 24 total). Operators: E_{t+1} = E_t + α_D Π_t ε_t (α_D = 0.3, Π_t = 1/running-var(ε) clipped to [0.25, 4]); γ_O,t slow OU around 0.7 (σ = 0.02, clipped [0,1]); C_t = logistic(4·(|ε_t|−0.5)), r_t = C_t; A_t = g_A·C_t|ε_t| (g_A = 1); S_{t+1} = S_t + λr_t ε_t − δ_S(S_t−S_base) (λ = 0.35, δ_S = 0.01, S_base = 0.5). All stage activities non-negative by construction (verified min = 0).

**Perturbation.** θ_i = ã_i/Σã_j, ã_i = a_i/â_i, under: (i) the full grid â_i ∈ {0.5, 1, 2}×nominal per channel (3⁵ = 243 settings); (ii) 50 random log-normal perturbations, log(â_i/â_i⁰) ~ N(0, (ln 2)²) (±2× at 1σ per channel).

**Measurements.** Episode stage-mix profile = time-mean of θ(t) (a simplex point); pairwise FR distances d = 2 arccos Σ√(θθ′) between the 24 episodes; Spearman ρ between pairwise-distance vectors across â settings; dispersion = within-condition mean pairwise FR; NN-clustering = fraction of episodes whose FR-nearest neighbor shares their shock condition.

**Results.**
- Pairwise FR-distance correlation vs baseline, full grid: **min ρ = 0.940, median 0.993**; log-normal draws: **min 0.952, median 0.994**. Worst-case pairwise setting-pair ρ in the 21-setting heatmap subset: 0.955.
- **Qualitative conclusions are 100% robust:** the dispersion ordering mild < moderate < severe holds in **243/243 grid settings and 50/50 log-normal draws**; NN same-condition clustering varies only 0.583–0.667 (baseline 0.667) across the grid.
- **Absolute metric values are NOT scale-invariant (as they cannot be):** mean pairwise FR ranges 0.118–0.217 across the grid (1.83× spread; baseline 0.166). Channel influence ranking: D and O rescalings move the geometry most (mean-D swing ±0.02, ρ down to 0.987); C, A, S rescaling is nearly inert (ρ ≥ 0.9995) — because C, A, S activities co-vary (all are monotone in |ε|), rescaling one mostly rescales a shared direction.
- **Verdict:** any *relational* conclusion of the §3.1 geometry (which states are closer, dispersion orderings, clustering) is robust to defensible â choice; any *absolute* FR distance, Cramér–Rao bound value, or dispersion magnitude must be quoted with its â. The stack currently prints no â, so no printed absolute number exists to be at risk — but the registration gap is real and should be closed by the writers.

**Figure:** `figR2_B3_fr_ahat_heatmap.png` — (a) 21-setting Spearman-ρ heatmap; (b) baseline vs worst-case pairwise distances; (c) per-condition dispersion across all 243 settings (ordering never inverts); (d) ρ distributions.

---

## BATTERY 4 — sparse/weighted-network Kuramoto sensitivity

**Protocol (matches Sim-B Study 1 exactly, then varies topology).** N = 500, ω ~ Cauchy(0,1), init θ = 2 arctan(ε̃), ε̃ ~ Cauchy(0,1) (uniform phases, §M7.2); Euler dt = 0.05, burn-in 100 t.u. + measurement 200 t.u.; K grid 0–8 (17 pts); 2 graph realizations × 2 ω/init seeds (42/1042) per topology. Degree-normalized coupling dθ_i = ω_i + (K/k_i)Σ_j A_ij sin(θ_j−θ_i), making K comparable across topologies (disclosed choice; isolates uncoupled).

**Topologies:** all-to-all (reference); Erdős–Rényi p ∈ {0.05, 0.1, 0.2, 0.5} (⟨k⟩ ≈ 25/49/100/249); Barabási–Albert m = 2 (⟨k⟩ ≈ 4) and m = 12 (⟨k⟩ ≈ 24); all-to-all with symmetric log-normal(0, 0.5) weights rescaled to mean 1.

**Validation:** the all-to-all arm reproduces Sim-B's operating point: R(K=4.5) = **0.710 ± 0.029** vs Sim-B's 0.709 — the pipeline is consistent with the published battery.

**R(K=4.5) by topology (mean ± sd over 4 runs):**

| topology | ⟨k⟩ | R(K=4.5) | R > 0.7? | R(K=8) |
|---|---|---|---|---|
| all-to-all | 499 | 0.710 ± 0.029 | marginal pass (as Sim-B found) | 0.851 |
| ER p = 0.50 | 249 | 0.709 ± 0.031 | marginal pass | 0.850 |
| ER p = 0.20 | 100 | 0.705 ± 0.029 | borderline | 0.848 |
| ER p = 0.10 | 49 | 0.700 ± 0.032 | **borderline fail** | 0.847 |
| ER p = 0.05 | 25 | 0.684 ± 0.036 | **fail** | 0.843 |
| BA m = 12 | 24 | 0.687 ± 0.024 | **fail** | 0.840 |
| BA m = 2 | 4 | 0.416 ± 0.061 | **collapse** | 0.660 |
| weighted log-normal | 500 | 0.710 ± 0.030 | marginal pass | 0.851 |

**Findings.**
1. **R > 0.7 at K = 4.5 does not survive sparsity.** It holds only at ⟨k⟩ ≳ 100 (ER p ≥ 0.2, within seed noise at p = 0.1); at ⟨k⟩ ≈ 25 (ER p = 0.05, BA m = 12) R falls to ≈ 0.68–0.69 — below target, though within ~1 sd of it; at ⟨k⟩ = 4 (BA m = 2) coherence collapses to 0.42 and never recovers above 0.7 even at K = 8.
2. **Weight heterogeneity is benign:** log-normal K_ij on the full graph leaves R(K) indistinguishable from all-to-all (0.710 vs 0.710 at K = 4.5). The threat to the claim is *missing edges*, not uneven edge weights.
3. **The functional form is robust; the threshold is not.** Every topology shows the same continuous onset at K ≈ 2 (the mean-field K_c = 2 for Cauchy(0,1) survives on all graphs tested, because degree normalization keeps the effective coupling scale) — what shifts is the *asymptote level* and the margin above threshold. This is exactly the posture GTT §3.4's repaired text adopts ("functional form of the hypothesis, not a numerical prediction"); the battery confirms that repair was necessary and sufficient.
4. **Product reading for TFP/whitepaper:** the already-fragile ℓ-band at K = 4.5 (Sim-B: ℓ* ≲ 0.02–0.10) is further compressed on sparse networks — a real trust network with effective degree ~25 sits *below* the R = 0.7 line even at zero leakage. The honest claim needs K ≥ 6–8 **and** ⟨k⟩ ≳ 25.

**Figure:** `figR2_B4_kuramoto_topologies.png` — R(K) curves per topology with seed-sd bands, R = 0.7 target, 1/√N floor, K = 4.5 operating point.

---

## BATTERY 5 — family-wise multiplicity analysis

**Family assembled** from `numbers_docas.md` (SIM-D re-run values) and `docas_revised.md` §4.6/§5.2: the stack's permutation-test results named in the battery spec. m = 24 tests with p-values. Excluded from the correction (listed for completeness): **N.4 CLICS4 overlap** (descriptive shortest-path matrix, no p-value reported) and the N.3/D12 negative controls (null-confirming checks, not hypothesis tests). D11's two arms are reported only as "p > 0.5" with negative r; they enter at the conservative bound p = 1.0. All p = 0.0005 values are resolution-limited (2,000 permutations; read as p ≤ 0.0005).

**Multiplicity table** (α = 0.05; Bonferroni threshold 0.05/24 = 0.00208):

| # | Test | p | Bonferroni | BH | Post-hoc flag |
|---|---|---|---|---|---|
| 1 | CLICS C Recognition density (fam≥3) | 0.0005 | **PASS** | **PASS** | — |
| 2 | CLICS D Expectation density | 0.0075 | fail | **PASS** | — |
| 3 | CLICS O Validation density | 0.0005 | **PASS** | **PASS** | — |
| 4 | CLICS A Activation density | 0.0005 | **PASS** | **PASS** | — (concept list truncated in print) |
| 5 | CLICS S Stabilization density | 1.0 | fail (NULL) | fail (NULL) | — |
| 6 | CLICS C + mismatch-augmented density | 0.0005 | **PASS** | **PASS** | **POST-HOC** (assembled after first analysis; paper discloses) |
| 7 | CLICS adjacent/non-adjacent ratio | 0.061 | fail | fail | **POST-HOC**-ish (derived follow-up; "weakly present" ceiling correct) |
| 8 | N.3 ridge encoding (mean vertex r) | 0.0005 | **PASS** | **PASS** | — |
| 9 | N.3 exact retrieval (top-1) | 1.0 | fail (NULL) | fail (NULL) | — |
| 10 | N.3 Procrustes alignment | 0.769 | fail (NULL) | fail (NULL) | — |
| 11 | N.3 category LOO decode | 0.0005 | **PASS** | **PASS** | — **but ARTIFACT** (templatic lexicon; semantic-only control also 1.000) |
| 12 | D8 EN paraphrase LOO | 0.046 | fail | fail | — (pre-registered; marginal) |
| 13 | D8 EN×PAR geometry Mantel | 0.006 | fail | **PASS** | — |
| 14 | D8 ES arm | 0.174 | fail (NULL) | fail (NULL) | — (pre-registered) |
| 15 | D8 JA arm | 0.053 | fail (NULL) | fail (NULL) | — (pre-registered) |
| 16 | D9 second-encoder category decode | 0.190 | fail (NULL) | fail (NULL) | — (pre-registered) |
| 17 | D9 TRIBE×Tuckute Mantel | 0.0996 | fail (NULL) | fail (NULL) | — (pre-registered) |
| 18 | D11 cortical Mantel (single-word) | 1.0 (conservative; reported >0.5) | fail (NULL) | fail (NULL) | — (pre-registered) |
| 19 | D11 embedding Mantel (single-word) | 1.0 (conservative; reported >0.5) | fail (NULL) | fail (NULL) | — (pre-registered) |
| 20 | D13 cortical Mantel (definition sentences) | 0.0095 | fail | **PASS** | **POST-HOC** (stimulus-class correction after D11 null; disclosed fork) |
| 21 | D13 embedding Mantel (definition sentences) | 0.0035 | fail | **PASS** | **POST-HOC** (same fork) |
| 22 | Bridge LLaMA→eng1000 held-out (random-pairing perm) | 0.0005 | **PASS** | **PASS** | **POST-HOC** (round S, assembled after first analyses) |
| 23 | Bridge translated-vs-true cosine (battery) | 0.0005 | **PASS** | **PASS** | **POST-HOC** (round S) |
| 24 | Bridge RDM Mantel (battery) | 0.0005 | **PASS** | **PASS** | **POST-HOC** (round S) |

**Verdicts.**
- **Bonferroni: 9/24 survive** — all at the resolution-limited p = 0.0005 (C, O, A, C+mismatch, N.3 encode, N.3 category-LOO, bridge ×3). **D Expectation (0.0075) fails Bonferroni**; D8 EN×PAR (0.006) and both D13 arms fail Bonferroni.
- **BH: 13/24 survive** — adds D Expectation, D8 EN×PAR Mantel, D13 cortical, D13 embedding.
- **Adjacency (0.061) and D8 EN paraphrase (0.046) fail even BH** — the papers' own wording ("weakly present" / "marginal") is already correct and must not be upgraded.
- **Honest-structure notes:** (i) 5 of the 13 BH survivors are post-hoc assemblies (C+mismatch, D13 ×2, bridge ×2 — or 6 of 13 counting the bridge as one post-hoc program); the papers disclose each, and the disclosures are what make the correction interpretable — post-hoc tests that survive Bonferroni are still post-hoc for *hypothesis-generation* weight. (ii) N.3 category-LOO survives every correction while being a **known artifact** (semantic-only control also decodes at 1.000): multiplicity correction controls false-positive rate, not construct validity — the paper's artifact label must stay attached wherever the number travels. (iii) Treating the four CLICS channel tests as their own pre-registered sub-family (as §4.6 presents them) changes nothing qualitatively: C/O/A survive Bonferroni at m = 5 (threshold 0.01), D at 0.0075 passes, S null. (iv) All "surviving" p = 0.0005 values are permutation-resolution-limited; they survive any m ≤ 100 under Bonferroni, so the conclusion is insensitive to family-boundary choices.

---

## BATTERY 6 — NNT benefit-side ledger (complement to whitepaper §4.7)

Same discipline as the NNH side: each channel priced separately, incommensurate units, **no composed single NNT asserted**. Every input is a figure printed in the papers; every assumption is stated; anything not quantifiable from printed numbers is declared non-quantifiable rather than invented.

**Channel 1 — error correction (incumbent's measured error base: FTC 2013).**
Assumptions: (a) FTC population rates transfer to FreshCredit's target population; (b) a correction succeeds with probability q; (c) "benefit" = consumer moved to the correct (better) risk tier. Measured inputs: P(material error) = 0.26; P(tier-relevant | error) = 5.2%/26% = 0.20. Benefit rate per onboarded consumer = 0.26 × 0.20 × q:

| q anchor | benefit rate | NNT (per tier-correction benefit) |
|---|---|---|
| q = 0.37 (FTC 2015: share of disputants receiving *all* requested modifications — the adversarial-status-quo rate) | 1.92% | **52** |
| q = 0.80 (FTC 2015: share receiving *some* modification) | 4.16% | **24** |
| q = 1.00 (ceiling: user-owned record corrects every correctable error) | 5.20% | **19** |

Interpretation: the channel's theoretical ceiling is exactly the incumbent's measured harm rate (5.2% tier misplacement); FreshCredit cannot beat NNT = 19 on this channel and achieves it only if user-owned correction is perfect. **Not quantifiable without new data:** whether a user-owned, annotation-bearing correction loop actually achieves q ≥ the incumbent's dispute rates — no measured q exists; this is a pilot measurable, stated as such. Dollar value of a tier correction: not priced in the papers → not priced here.

**Channel 2 — cost savings per verification decision (paper's like-for-like marginal discipline, §4.5).**
Inputs: incumbent marginal verification = one pull at $50–$110+ (CFPB 2024 RFI), amortized $510–$725 per closed loan (CHLA 2024); FreshCredit marginal = local read + ~$0.001/event settlement; lifetime anchoring of a 10-unit competitive history (1,005 events at the battery's measured 100.5 events/unit) = **$1.01 unrolled / $0.0001 rolled up**.
Benefit per decision: each reuse of an anchored identity avoids one pull → **$50–$110 avoided per verification read**; a 3-pull mortgage shop avoids ~$150–$330 against a one-time $1.01 anchoring cost. Break-even: the one-time anchoring cost is recovered at the *first* avoided pull (NNT-analog "number needed to reuse" = 1). Attestation offset (from §4.7's own harm ledger, mandatory for honesty): Sybil attestation at multiplier m = 10/100/1000 costs $10.05/$100.50/$1,005 per 10-unit history → net benefit vs a 3-pull decision is **+$140 to +$320 (m = 10), +$50 to +$230 (m = 100), −$855 to −$675 (m = 1000, net negative)**. The cost channel's benefit is real at low attestation multipliers and is *eaten entirely* by the attestation harm channel at m = 1000 — the two ledger sides share one parameter.
Caveats carried from the paper: marginal-vs-marginal only (no comparison against the full-service tri-merge product price); CAC excluded (paper's own discipline); volumes assume honest-user event rates.

**Channel 3 — inclusion (population: CFPB-corrected 7.0M invisible + 25.3M thin/stale = 32.3M adults).**
- Only measured conversion anchors available: Upstart NAL (regulator-supervised): +27% approvals vs traditional model → number-needed-to-evaluate NNE = 1/0.27 ≈ **3.7 previously-rejected applicants evaluated per additional approval** — a third-party effect, projected, not a FreshCredit measurement. Livble (vendor, single deployment): ~3× approvals at equal default rate → at an assumed 10% baseline approval, NNE = **5** (baseline assumption explicit; vendor figure uncontrolled).
- Experian Boost (>10k newly scoreable/month): the denominator (connected base × time) is not stated in the papers → **NNT not computable honestly**; declared, not estimated.
- **Binding constraint from the harm side (§4.7 channel 4):** the inclusion NNT is **infinite** for unseeded thin-file users at organic floors ≲ 0.01 events/day (never converges); the benefit channels only exist downstream of the seeded 2-events/day × 30-day onboarding floor (decisionable at day 72). The benefit ledger inherits the harm ledger's single most consequential requirement.
- Global inclusion (6.7B people < $30/day; registry coverage 64% OECD vs 7% Sub-Saharan Africa): not quantifiable without deployment data — declared.

**Ledger summary (incommensurate units, like §4.7):** error correction NNT 19–52 per tier-fix (q-dependent, q unmeasured); cost benefit $50–$110 per avoided pull, net-of-attestation positive only for m ≲ 100; inclusion NNE ≈ 3.7–5 per additional approval (third-party effects, projected), gated by the cold-start seeding requirement. Against the harm side's headline (NNH ≈ 1.03 wrongful flags per flag at 1% prevalence), the honest reading is: **the misclassification channel dominates all benefit channels at low prevalence unless prevalence-aware thresholds land first** — the benefit side does not offset §4.7 channel 5; it coexists with it pending that mitigation.

---

## BATTERY 7 — CLICS4 per-macroarea subgroups (Simpson check)

**Method.** Real CLICS4 edge list (51,562 edges; 1,725 concept nodes — paper counts verified). Concept sets exactly as the paper/SIM-D used (gloss mappings: KNOW→KNOW (SOMETHING), CORRECT→CORRECT (RIGHT), FEAR→FEAR (BE AFRAID), CALM→CALM (OF SEA), SURPRISE→SURPRISED); A-channel set = the 7 printed concepts (printed list truncated — disclosed in numbers_docas.md). Per Glottolog macroarea (languages.csv metadata): an edge counts if supported by ≥ 1 language in the area; primary filter = **≥ 3 distinct families among the area's supporting languages** (the paper's ≥3-family filter applied within the subgroup — disclosed design choice); sensitivity panel = unfiltered (any-support) edges. Permutation tests: 2,000 random same-size concept sets from all 1,725 nodes, p = (1+k)/2001, seed 42. Aggregate reproduced **exactly** before subgrouping (C 11/21 = 0.5238; D 1/3; O 5/15; A 3/21; S 0/15; C+mismatch 12/45 — identical to SIM-D).

**Subgroup table (within-area fam≥3 density, hits/pairs, permutation p):**

| Macroarea (fam≥3 edges) | C | D | O | A | S | C+mismatch |
|---|---|---|---|---|---|---|
| Africa (355) | 0.048 (1/21) p=0.0065 | 0 (0/3) p=1.0 | 0 (0/15) p=1.0 | 0.048 (1/21) p=0.0060 | 0 (0/15) p=1.0 | 0.022 (1/45) p=0.0145 |
| Australia (62) | 0 (0/21) p=1.0 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 |
| Eurasia (1,577) | 0.238 (5/21) p=0.0005 | 0 (0/3) p=1.0 | 0.200 (3/15) p=0.0005 | 0.143 (3/21) p=0.0005 | 0 (0/15) p=1.0 | 0.133 (6/45) p=0.0005 |
| North America (333) | 0.095 (2/21) p=0.0005 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 | 0.044 (2/45) p=0.0005 |
| Papunesia (263) | 0.143 (3/21) p=0.0005 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 | 0 p=1.0 | 0.067 (3/45) p=0.0005 |
| South America (1,306) | 0.333 (7/21) p=0.0005 | 0 (0/3) p=1.0 | 0.133 (2/15) p=0.0005 | 0.048 (1/21) p=0.0150 | 0 (0/15) p=1.0 | 0.178 (8/45) p=0.0005 |

(Unfiltered any-support panel on the figure shows the same qualitative pattern at higher densities.)

**Verdict on Simpson-type reversal: NONE.**
1. **S is null in every macroarea** — 0/15 under the fam≥3 filter in all six areas, and near-zero unfiltered (≤ 2/15). The aggregate S null is not masking a subgroup positive; the paper's corrected "no detectable S lexical attractor" is subgroup-stable.
2. **C is positive wherever the subgroup has data** — significant in 5/6 areas; the single null (Australia) sits in the smallest edge base (62 fam≥3 edges in the entire area; unfiltered background 0.0008) and is a power limitation, not a reversal: C's unfiltered Australia density (2/21) still exceeds its background. The C result is *not* a Eurasia-only artifact, though Eurasia carries the most edges.
3. **A reverses *upward*, not the aggregate's direction:** significant in Africa (p = 0.006) and South America (p = 0.015) under the strict filter — the aggregate's weakest-looking channel is subgroup-positive where threat/flight lexicons are phylogenetically diverse. No subgroup shows A below background.
4. **D (3 concepts) and O are underpowered per area:** D has 3 pairs total; O significant in Eurasia and South America only. Neither can reverse (0 hits is the null, not a negative effect).
5. Caveats: within-area fam≥3 is strict (62–1,577 edges per area vs 3,986 globally); macroarea subgrouping is itself a **post-hoc robustness check**, not pre-registered; density *levels* are not comparable across areas (different family diversities) — only significance patterns are compared. Simpson's paradox in the strict sense (aggregate direction opposite to all subgroups) is impossible here for S (0 everywhere) and does not occur for C.

**Figure:** `figR2_B7_macroarea_subgroups.png` — (a) fam≥3 density heatmap with hits/pairs and p-values; (b) unfiltered any-support panel.

---

## Honest nulls and disclosures (all batteries)

1. **B3:** the "pre-registered reference scales â_i" the simplex construction requires are **not printed anywhere in the stack** — flagged to writers. Absolute FR magnitudes move 1.83× across the defensible grid (metric-sensitive statistics must carry their â).
2. **B4:** R > 0.7 at K = 4.5 **fails** on sparse graphs (ER p = 0.05: 0.684; BA m = 12: 0.687; BA m = 2: 0.416) — only the all-to-all and weighted variants (marginally) pass. The quantitative population claim needs K ≥ 6 **and** mean degree ≳ 25.
3. **B5:** D (0.0075), D8 EN×PAR (0.006), D13 (0.0095/0.0035) **fail Bonferroni** across the 24-test family (they survive BH); D8 EN paraphrase (0.046) and adjacency (0.061) fail both. N.3 category-LOO survives all corrections while being a disclosed artifact — multiplicity correction ≠ construct validity. 6 of 13 BH survivors are post-hoc assemblies (disclosed in the papers).
4. **B6:** error-correction NNT ceiling is 19 (= the incumbent's measured 5.2% harm rate); the attestation multiplier that prices the Sybil harm also prices the cost benefit — at m = 1000 the cost channel is net *negative*; Boost-based inclusion NNT and the global-inclusion benefit are **not computable without new data** (declared, not estimated).
5. **B7:** no Simpson reversal; S null in all six macroareas; C significant in 5/6 (Australia null = power, not reversal); A subgroup-positive in Africa/South America.

## Figure index (all 150 dpi, captioned on-figure)
- `figR2_B3_fr_ahat_heatmap.png` — Battery 3: FR-geometry correlation across â settings.
- `figR2_B4_kuramoto_topologies.png` — Battery 4: R(K) per topology vs all-to-all reference.
- `figR2_B7_macroarea_subgroups.png` — Battery 7: per-macroarea channel density heatmaps.

Data artifacts: `b4_results.json` (B4 curves), `b3_ahat.py` (B3 code, deterministic reproduction of all B3 numbers), `b4_kuramoto.py` (B4 code). CLICS4 sources: `/mnt/agents/output/clics_graph/colexifications.csv`, `/mnt/agents/output/languages.csv`.
