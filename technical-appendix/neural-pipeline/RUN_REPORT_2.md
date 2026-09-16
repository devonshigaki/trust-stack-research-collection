# DOCAS x TRIBE v2 — Engineering Run Report 2 (ENG-2)

**Date:** 2026-09-07 (sandbox clock) · **Agent:** ENG-2 · **Scope:** complete the DOCAS
neural pipeline for real on the full 27-stimulus battery: battery reconstruction,
27 TRIBE v2 forward passes, Gallant-style decode (N.3), vec2vec bridge, CLICS4
overlap (N.4), figures. Builds on ENG-1's RUN_REPORT.md (6-stimulus round M).

## 0. Verdict (one line)

The full round-N backbone runs end-to-end on real artifacts — reconstructed
battery27 → LLaMA-3.2-3B (real weights) → TRIBE v2 (real checkpoint) → 27 ×
[100 × 20,484] predictions with bit-exact determinism — and both previously
BLOCKED links were unblocked: Gallant decode uses the **real** Huth-lab
english1000 985-dim semantic model (found on OpenNeuro ds003020, not a
substitute), and vec2vec's **released pretrained translators** were downloaded
and run on CPU. Retrieval and Procrustes alignment are NULLs (consistent with
the paper's own nulls); category LOO decode on our reconstruction is perfect
(1.00) — a property of the reconstruction's templatic lexicon, explicitly NOT
the paper's 0.40.

## 1. Honesty constraints (read first)

- **All 27 stimulus texts are labeled "reconstruction-from-spec, pending
  bit-identity check against `simulations/battery27_manifest.json`"** (that file
  was NOT uploaded). Item 1 of each category is a verbatim quote from the Master
  Reproduction Manifest; items 2–5 (+ CONTROL_2) were written to the manifest's
  stated design intents; the amount-crossing order (item1=$4,000 forced by the
  quotes; items 2–5 = $2,500/$7,500/$12,000/$20,000) is a reconstruction choice.
  FAIR monthly payments were computed for 9% APR/60 mo — the formula reproduces
  the verbatim item-1 "$83" exactly.
- **No original headline numbers are claimed.** Where the manifest quotes
  originals (EN LOO decode 0.40 p=0.032; retrieval/alignment nulls), they are
  cited as reference-only.

## 2. Sandbox / assets (all restored after sandbox reset wiped /tmp)

| Asset | Bytes (verified) | Source |
|---|---|---|
| TRIBE v2 `best.ckpt` | 708,856,138 (exact) | hf-mirror.com/facebook/tribev2 |
| LLaMA-3.2-3B safetensors shards | 4,965,799,096 + 1,459,729,952 (exact) | hf-mirror.com/unsloth/Llama-3.2-3B |
| english1000sm.hf5 (985 × 10,470 words) | 82,673,264 | OpenNeuro ds003020 snapshot 4.0.0 `derivatives/english1000sm.hf5` (LeBel et al. 2023; same matrix as Huth et al. 2016) |
| vec2vec v1.0.0 `final_model_release.zip` | 1,162,524,881 | github.com/rjha18/vec2vec releases |
| CLICS4 CLDF (`colexifications.csv`, `concepts.csv`) | — | github.com/clics/clics4 |
| gte-base / gtr-t5-base encoders | — | hf-mirror (thenlper/gte-base, sentence-transformers/gtr-t5-base) |
| fsaverage5 + Schaefer-400/Yeo-7 | — | nilearn datasets |

Env: CPU-only, 4 GB RAM, torch 2.8.0; tribev2 deps pinned per its pyproject
(neuralset==0.0.2, neuraltrain==0.0.2, exca==0.5.20, x_transformers==1.27.20).

## 3. What was run

### N.1 — battery27 pipeline (RUN-OK)
Manifest-canonical per-stimulus chain in `code/run_battery27.py`: no-BOS LLaMA
tokenize → hidden states at **layers 17 & 24** (manifest stand-ins for the
group-mean ranges) → uniform token resample to 100 TRs
(`idx=min(arange(100)*seq//100, seq-1)`) → f32 [2,3072,100] → TRIBE v2 forward
→ [20484,100] per stimulus. 27/27 stimuli, ~38 s each.
- **Determinism: max |Δ| = 0.0** on full independent re-run of FAIR_1
  (`results/battery27_determinism.json`).
- **Separability:** within-category mean r = 0.991, between = 0.908, min pair
  r = 0.708 (`results/battery27_separability.json`). All 351 pairs distinct
  (max off-diagonal 0.998 < 1). NOTE: within-category correlations are higher
  than round M's 6-stimulus set because the reconstructed battery uses one
  template per category — a reconstruction property, not a model property.
- Category contrasts vs CONTROL: PREDATORY largest (mean |Δ| 0.070, max 0.349),
  then FAIR (0.053), TEASER (0.050), TRUST_SIGNAL (0.030), THREAT (0.026)
  (`results/battery27_contrasts.json`).
- Full time series: `/tmp/tribe/results/battery27_preds.npz` (204 MB, sha256
  2e1b09ee…1cd9); TR-mean maps hash-verified copy at
  `results/battery27_meanmaps.npz` (the 204 MB file exceeds the /mnt/agents
  portal-mount transfer limit — copy failed with EIO, as ENG-1 warned).

### N.3 — Gallant decode (RUN-OK, real semantic model)
`code/gallant_decode.py`, seed 20260905, 2,000 permutations per null,
leave-8-out folds (8/8/8/3, seeded assignment). Semantic features = mean of
real eng1000 vectors over in-vocab words (coverage 0.78–0.97 per stimulus).
Ridge α=1e3 fixed (RidgeCV on full data independently selects 1e1–1e3 range;
reported in JSON).

| Test | Observed | Null (2,000 perm) | p | Verdict |
|---|---|---|---|---|
| Ridge encoding, mean vertex corr | 0.181 | 0.000 ± ~0.01 | 0.0005 | PASS |
| Stimulus retrieval top-1 (of 27) | 0.037 (1/27) | 0.037 | 1.000 | **NULL** |
| Procrustes alignment (PCA-18) | r = −0.058 | −0.007 | 0.769 | **NULL** |
| Category LOO decode | **1.000** | 95% CI [0.00, 0.37] | 0.0005 | PASS |

Retrieval and alignment nulls reproduce the *pattern* of the paper's reported
nulls (reference only). The perfect LOO decode is driven by the
reconstruction's within-category lexical homogeneity — the semantic-only
control decodes at 1.000 too, so the brain patterns inherit a trivially
separable input. The original 0.40 implies the true battery had much higher
within-category lexical diversity. Documented speed compromises (fixed α in
null loop via algebraically identical precomputed ridge maps; null encoding
evaluated on every 20th vertex; Procrustes in train-fold PCA-18 space) are in
the script docstring.

### vec2vec bridge (RUN-OK tool-level; DOCAS bridge TRAINING-REQUIRED)
Cloned rjha18/vec2vec; downloaded the real v1.0.0 release (15 pretrained
translator pairs over gte/gtr/e5/stella/clip/granite). None cover LLaMA hidden
states or eng1000, so the DOCAS-specific bridge is **TRAINING-REQUIRED**:
`python train.py configs/unsupervised.toml --unsup_emb <llama_extractor>
--sup_emb <eng1000_extractor> --num_points 1000000 --epochs 2000` (GPU-scale;
repo warns GAN training is unstable across seeds). What WAS run for real on
CPU (`code/vec2vec_demo.py`): loaded `gte_gtr/model.pt` with the repo's own
builder (state dict strict=False: 0 missing / 0 unexpected), embedded the 27
battery texts with real gte-base and gtr-t5-base, translated gte→gtr:
**mean cosine to true gtr = 0.703 (range 0.627–0.802); top-1 retrieval of the
correct text among 27 = 44.4% vs 3.7% chance** (shuffle-null mean 0.0375).
(`results/vec2vec_bridge_results.json`.)

### N.4 — CLICS4 overlap (RUN-OK)
`code/clics_offer_overlap.py` on real CLICS4 CLDF: graph verified at 1,725
nodes / 51,562 edges (density 0.0347; family≥3 sensitivity: 1,386/3,986).
196 content words extracted from the battery; **114 mapped** to Concepticon
nodes (52 exact gloss, 19 morphological, 43 via an explicit documented synonym
table, e.g. payment→PAY, garnishment→SEIZE, penalty→PUNISHMENT, trust→TRUTH;
82 unmapped, mostly finance jargon with no Concepticon gloss — listed in the
JSON). Category-vocabulary → channel-lexicon mean shortest-path matrix: every
category sits at distance ~0 from its own channel lexicon and ≥0.5 from all
others; CONTROL is the farthest from every offer category (1.08–1.48). The
paper's own channel-concept lists are in the absent Supporting Document, so the
lexicons are battery-derived — labeled as such. ENG-1's density inconsistency
finding (0.034 matches only the unfiltered graph) stands.
(`results/clics_offer_overlap_results.json`.)

## 4. Pipeline-link status table

| Link | Status | Notes |
|---|---|---|
| battery27 stimulus texts | **PARTIAL (reconstruction)** | item-1s verbatim from manifest; rest faithful-from-spec; pending bit-identity vs `battery27_manifest.json` |
| LLaMA-3.2-3B features | RUN-OK (with substitution) | unsloth mirror weights (bf16), ENG-1 streaming forward, layers 17/24 per manifest |
| TRIBE v2 forward | RUN-OK | real ckpt, strict load, bit-exact determinism re-verified on battery27 |
| N.1 battery expansion | RUN-OK | 27/27, separability + contrasts + determinism |
| N.3 Gallant decode | RUN-OK | **real** eng1000 (OpenNeuro); encoding PASS, LOO decode PASS (trivially, see §3), retrieval NULL, alignment NULL |
| vec2vec | PARTIAL | released translators load & translate on CPU (real demo metrics); LLaMA↔eng1000 bridge TRAINING-REQUIRED, exact command documented |
| N.4 CLICS overlap | RUN-OK | real CLICS4 graph; tiered Concepticon mapping fully logged |

## 5. Figures (all in /mnt/agents/output/figures/docas/pipeline/, 170–180 dpi,
honest captions carrying the reconstruction label)

- `fig_n1_separability_matrix.png` — 27×27 pairwise Pearson, category blocks
- `fig_n1_category_contrast_matrix.png` — 6×6 category mean-map correlations
- `fig_n1_category_contrasts.png` — per-category − CONTROL surface maps (real fsaverage5 pial)
- `fig_n3_decode_bars.png` — LOO decode by category + permutation-null 95% CI + chance
- `fig_n4_clics_heatmap.png` — CLICS category→channel distance heatmap

## 6. Exact commands

```bash
# assets (chunked downloader code/chunk_dl.py; sizes verified)
python3 chunk_dl.py https://hf-mirror.com/facebook/tribev2/resolve/main/best.ckpt best.ckpt 708856138
python3 chunk_dl.py https://hf-mirror.com/unsloth/Llama-3.2-3B/resolve/main/model-00001-of-00002.safetensors llama_model-00001-of-00002.safetensors 4965799096
python3 chunk_dl.py https://hf-mirror.com/unsloth/Llama-3.2-3B/resolve/main/model-00002-of-00002.safetensors llama_model-00002-of-00002.safetensors 1459729952
# english1000sm.hf5: HEAD https://openneuro.org/crn/datasets/ds003020/snapshots/4.0.0/files/derivatives:english1000sm.hf5 -> S3 redirect; curl -C - resume (openneuro 500s on Range)
git clone --depth 1 https://github.com/clics/clics4 && git clone --depth 1 https://github.com/rjha18/vec2vec
curl -L -C - -o vec2vec_models.zip https://github.com/rjha18/vec2vec/releases/download/v1.0.0/final_model_release.zip
pip install "neuralset==0.0.2" "neuraltrain==0.0.2" "exca==0.5.20" "x_transformers==1.27.20" einops \
    safetensors "transformers<6" nilearn nibabel h5py sentence-transformers toml diffusers
# runs (all in /mnt/agents/work/tribe/code/)
python3 battery27_reconstructed.py     # writes battery27_reconstructed.json
python3 run_battery27.py               # ~18 min; battery27_preds.npz + determinism
python3 gallant_decode.py              # ~15 min; 2,000 perms x 3 nulls, seed 20260905
python3 clics_offer_overlap.py         # ~2 min
python3 vec2vec_demo.py                # ~5 min CPU
python3 make_figs27.py <figdir>        # all figures
```

## 7. Deviations & residual risks

1. Stimuli reconstructed (§1) — every neural number will move with the true
   battery; the scripts are drop-in rerunnable.
2. LLaMA bf16 mirror vs paper's F16 GGUF; streaming fp32 forward (RAM) —
   unchanged from ENG-1, validated there by next-token probe.
3. N.3 protocol gaps vs the (absent) original `gallant_decode.py`: fold
   structure implemented as 8/8/8/3 seeded split; fixed ridge α; PCA-18
   Procrustes. All documented in-code.
4. N.4 channel lexicons are battery-derived, not the paper's (absent
   Supporting Document).
5. LOO decode = 1.00 is a reconstruction artifact (templatic categories);
   do not cite as the paper's 0.40.
6. Full [20484×100] prediction tensor lives in /tmp only (204 MB > portal-mount
   limit); TR-mean maps (what all analyses use) are hash-verified in
   results/battery27_meanmaps.npz.
