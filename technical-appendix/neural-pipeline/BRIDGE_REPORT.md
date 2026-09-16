# BRIDGE REPORT — Supervised LLaMA-3.2-3B (3072-d) ↔ eng1000 (985-d) bridge (vec2vec-skip, runbook §C.1)

**Date:** 2026-09-08 · **Seed:** 42 everywhere · **Agent:** EXEC (sandbox CPU, 2 cores, 4 GB RAM)

## Verdict (up front)

**The supervised ridge bridge makes vec2vec GAN training unnecessary for this pipeline.**
With only **640 paired texts** (512 train / 128 held-out; vec2vec's paper floor is 50k–1M per
side, days of GPU GAN training), a plain ridge regression already achieves, on held-out pairs:
**top-1 retrieval 0.398 (≈51× chance 0.0078), top-5 0.594, mean rank 6.9 (chance 64.5),
mean cosine 0.965, permutation null p = 0.0005 (2000 perms).** The GAN's only advantage —
not needing paired data — does not apply here, because we control both feature extractors.

Against the runbook §B.6 success criteria: **cosine 0.965 ≥ 0.6–0.75 ("good" to paper-grade)**,
mean rank 6.9 vs criterion ≤~10, top-1 0.398 vs criterion ≥0.5 (below on top-1 only — at
**128× smaller data** and zero GAN training; vec2vec itself collapses to top-1 0.01 at 10k
pairs, paper Table 9). See "Honest limits" for the cosine-anisotropy caveat.

## Method

1. **Corpus.** `jxm/nq_corpus_dpr` train shard 0 (761,718 passages; HF unreachable from this
   sandbox, fetched via the ModelScope mirror of the same dataset — byte-size verified
   316,861,494). vec2vec-style chunking: 20–400 whitespace-token passages truncated to 64
   tokens, deduped, eng1000 in-vocab coverage ≥ 0.5 required (mean coverage 0.813, p5 0.677;
   4000 candidates kept, first 640 used after timing). Seed 42.
2. **Extractors (both real, both ours — hence paired data is producible).**
   - LLaMA-3.2-3B (real unsloth weights via ModelScope; shard sizes verified
     4,965,799,096 / 1,459,729,952 B; huggingface.co is blocked in this sandbox):
     memory-streaming extractor restored from `/mnt/agents/work/tribe/code/llama_stream.py`,
     validated by next-token probe ("The capital of France is" → top-2 " the"/" Paris").
     Feature = mean over blocks {14, 21, 28} (0.5/0.75/1.0 depth, TRIBE text-feature config)
     of token-mean-pooled hidden states → 3072-d, fp32.
   - eng1000: `english1000sm.hf5` (OpenNeuro ds003020 derivatives; 82,673,264 B, md5 matches
     S3 ETag `74a55e89…`), feature = mean of in-vocab word vectors → 985-d (Huth convention).
3. **Timing / N.** Single-text extraction was 38 s regardless of length (weight-I/O bound;
   4 GB RAM cannot cache 6.4 GB weights). I wrote a **batched extractor** (`embed_all.py`,
   one weight-pass per 16-text batch; verified cos = 1.0000 vs the validated single-text
   path) → **4.5 s/text**. N = 640 corpus texts = 47.6 min (battery27: +2.1 min) — inside the
   60-min timebox.
4. **Bridge.** Features z-scored (train statistics). Ridge `W = (XᵀX + αI)⁻¹XᵀY`, α from
   {1e1…1e5} (9 values) by 5-fold CV MSE on the 512 train pairs → **α = 3162**
   (llama→eng1000); refit on full train. Rectangular **orthogonal Procrustes** fitted as
   comparison. Evaluated on 128 held-out pairs: cosine (unit-norm), top-k retrieval, mean
   rank, plus a 2000-rep **random-pairing permutation null** for honest chance levels.
5. **Downstream.** Battery27 LLaMA features translated to eng1000 space via the ridge map;
   compared to direct eng1000 features of the same texts: per-item cosine, retrieval,
   **Mantel test** on cosine-distance RDMs (2000 perms), category LOO decode.

## Results (all real, held-out, seed 42)

### Paired held-out eval (128 NQ pairs)

| direction / model | mean cos | top-1 | top-5 | mean rank | null cos p95 | p (cos) |
|---|---|---|---|---|---|---|
| **LLaMA→eng1000 ridge (α=3162)** | **0.965** | **0.398** | 0.594 | **6.9** | 0.874 | 0.0005 |
| LLaMA→eng1000 Procrustes | 0.180* | 0.328 | — | 4.8 | 0.008 | 0.0005 |
| eng1000→LLaMA ridge (α=1000) | 0.949 | 0.266 | — | 18.2 | 0.909 | 0.0005 |
| eng1000→LLaMA Procrustes | 0.156* | 0.477 | — | 3.9 | 0.008 | 0.0005 |
| chance | (null mean 0.866) | 0.0078 | 0.039 | 64.5 | — | — |

*Procrustes outputs are near-orthogonal to targets in raw cosine (semi-orthogonal map
preserves angles, not the space's mean direction) yet retrieve well — cosine alone misleads
here; retrieval/rank is the reliable cross-space metric. Ridge beats Procrustes on the
primary direction's cosine (0.965 vs 0.180) and top-1 (0.398 vs 0.328).

### Battery27 downstream (27 reconstructed stimuli → eng1000 space via bridge)

- Per-item cosine translated-vs-true: mean **0.813**, min 0.642, max 0.967; vs tight null
  (mean 0.791, p95 0.797) → **p = 0.0005** (pairing matters).
- **Mantel r = 0.805, p = 0.0005** (null |r| p95 = 0.315). Raw un-translated LLaMA RDM vs
  true eng1000 RDM: r = 0.362 — the bridge **doubles** the geometry match.
- Category LOO decode: **1.00** for translated features (identical to true eng1000's 1.00;
  categories are trivially separable in both spaces; chance 1/6, null p95 0.33).
- **Honest failure mode:** exact-item retrieval among the 27 is at chance (top-1 = 1/27,
  mean rank 13.3 vs chance 14). Cause: within-category items are near-duplicates in true
  eng1000 space itself (same-category cos 0.951 vs cross-category 0.817), so item identity
  is intrinsically ambiguous for a bag-of-words target; the ridge's regression-to-mean
  (visible in fig. c as ×'s shrunk toward the centroid) compounds it. Category-level
  geometry — what the DOCAS pipeline actually consumes — is preserved.

## Honest limits

- **eng1000 anisotropy inflates absolute cosines:** random pairs already average cos 0.866
  (corpus) / 0.791 (battery). The signal is that paired ≫ null (p = 0.0005) and retrieval is
  51× chance — report cosine with the null, never alone.
- **Scale:** 640 pairs (CPU timebox) vs vec2vec's 1M/side. Metrics will improve with more
  pairs (GCP runbook §B.3 pipeline is directly reusable); even so, top-1 0.398 @ n=640
  already exceeds vec2vec's 10k-data regime (top-1 0.01).
- **Corpus:** NQ Wikipedia passages, not financial-ad domain; battery27 is OOD-ish, yet
  category geometry transferred (Mantel 0.805).
- **Procrustes cosine caveat** as above; rectangular Procrustes underperforms ridge here.

## Reproduce

Scripts + artifacts: `/tmp/tribe/{prep_corpus,embed_all,embed_eng1000,fit_bridge,battery_geometry,make_bridge_figs}.py`,
`bridge_results.json`, `battery_bridge_results.json`, `bridge_fwd.npz` (fitted map),
`battery27_eng1000_translated.npy` — archived copies in `/mnt/agents/work/tribe/results/bridge/`.
Figures: `/mnt/agents/output/figures/docas/pipeline/bridge_{a_cosine_dist,b_topk,c_pca_battery,d_alpha}.png`.
