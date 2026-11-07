# VIZ REPORT — visualization agent (VIZ), seed 42

**Deliverables:** `/mnt/agents/output/figures/docas/viz/` — 6 PNG figures (170–180 dpi) + 2 supporting
`.npy` tables. Every figure was rendered from real artifacts on disk (listed per figure below); no map,
network, or scatter was fabricated. Rendering stack: **matplotlib + nilearn 0.14.1** (freshly installed);
**pycortex was attempted first and failed to build** (`pip install pycortex` → wheel-build step dies with
`Permission denied` writing to a cython share dir), so all cortical surfaces use nilearn `plot_surf` on the
real fsaverage5 pial mesh — labeled as such on each figure.

## Figure inventory

### Task 1 — cortical-tile / surface visuals (from real TRIBE v2 predictions; nothing recomputed, nothing invented)

The per-vertex predictions already existed: `/mnt/agents/work/tribe/results/battery27_meanmaps.npz`
(27 × [20,484] TR-mean fsaverage5 maps, hash-verified by ENG-2 from the real TRIBE v2 forward passes on the
reconstructed battery27). No recompute was needed; none was done.

- **viz1a_category_mean_maps.png** — 6 rows × 4 views (LH lat/med, RH med/lat): per-category mean predicted
  TRIBE v2 cortical response (5 items/category; CONTROL n=2), shared symmetric color scale (±98th percentile,
  RdBu_r). *Provenance:* model predictions on reconstruction-from-spec stimuli; no measured neurophysiology.
  Supports docas.md §5.2 ("every offer produces a distinct predicted cortical pattern").
- **viz1b_contrast_threat_minus_fair.png** — vertex-wise THREAT−FAIR category-mean contrast, 4 views,
  ±99th-percentile scale. *Provenance:* as above; explicitly labeled "descriptive contrast, not an inferential
  statistic" per the §5.2 effect-size correction.
- **viz1c_yeo7_network_summary.png** — network-level aggregation. Real Schaefer-400/Yeo-7 atlas
  (nilearn `fetch_atlas_schaefer_2018`) projected to fsaverage5 with `vol_to_surf` (radius 3 mm,
  `nearest_most_frequent`; 17,997/20,484 vertices labeled). Panel (a): 5×7 heatmap of category−CONTROL mean
  Δ per Yeo-7 network (values annotated); panel (b): THREAT−FAIR network bars, mean ± SEM over parcels —
  Cont (largest negative, −0.045), DorsAttn (−0.032), SalVentAttn (−0.024) negative, Vis positive (+0.017),
  consistent with §5.2's control/dorsal-attention/DMN localization claim. Supporting array:
  `viz1c_yeo7_contrast_table.npy`.

### Task 2 — bridge shared-latent visualization (real bridge results)

- **viz2a_bridge_geometry_pca.png** — joint PCA (fit on the 54 stacked vectors) of true eng1000 battery
  features (●) vs ridge-translated LLaMA features (×), colored by battery category, grey pairing lines;
  header carries Mantel r = 0.805, p = 0.0005. The translated cloud shrinks toward the centroid (ridge
  regression-to-mean) while category structure is preserved — exactly what the Mantel number quantifies.
- **viz2b_bridge_retrieval_summary.png** — retrieval-quality panel: (a) held-out cosine histogram (128 NQ
  pairs, mean 0.965) against the random-pairing null (mean 0.866/p95 0.874) — the anisotropy caveat is stated
  on the figure; (b) top-1/5/10 retrieval (0.40/0.71/0.82) vs chance; (c) battery27 per-item cosine by
  category vs pairing null; (d) Mantel geometry match: bridge-translated r = 0.805 vs raw-LLaMA r = 0.362 vs
  null |r| p95 = 0.315.
- **Data honesty note:** the true battery eng1000 features were *not* archived by EXEC (only the translated
  ones were). I re-downloaded the real `english1000sm.hf5` (OpenNeuro ds003020 snapshot 4.0.0; **exactly
  82,673,264 bytes**, matching ENG-2's verified size) and recomputed the true features with EXEC's exact
  code path (`embed_eng1000.py`). Validation: recomputed per-item translated-vs-true cosines match the
  archived `battery_bridge_results.json` to **max |Δ| = 1.2e-9** — a functional bit-check of the whole
  chain. Recomputed features saved as `eng_battery27_true.npy` for reuse.

### Task 3 — CLICS network tiling (real CLICS4 data)

- **viz3_clics_channel_network.png** — spring layout (seed 42) of the colexification neighborhoods of the
  six channel lexicons. Source: real CLICS4 CLDF (`/mnt/agents/output/clics_graph/colexifications.csv` +
  `clics4-main/cldf/concepts.csv.zip`). Filter: Family_Count ≥ 3 (1,386 concepts / 3,986 edges — re-verified,
  matches ENG-2's sensitivity row; the 51,562-edge unfiltered graph is too dense to render honestly).
  Shown: 75 mapped lexicon concept nodes (colored by channel; squares = nodes shared by ≥2 channels) + their
  1-hop colexification neighbors (grey), 393 nodes / 1,196 edges. Lexicon membership and the exact/
  morphological/synonym Concepticon mapping tiers are taken from the archived
  `clics_offer_overlap_results.json` (battery-derived lexicons — labeled on the figure, since the paper's own
  channel lists are in the absent Supporting Document). Style after Jackson et al. 2019 language-family
  networks, as requested.

## Skips / deviations

1. **pycortex: SKIPPED (build failure)** — `pip install pycortex` fails at wheel build (Permission denied in
   sandbox). nilearn used instead and labeled on every surface figure, per the task's fallback instruction.
2. **No recompute of TRIBE v2 predictions** — real per-vertex predictions existed on disk
   (`battery27_meanmaps.npz`); recomputing would have duplicated verified work.
3. **Huth et al. 2016 semantic-tiling *reference* map** (the gallantlab atlas itself) — not renderable: the
   lab's model weights are an external research-data download and the paper itself leaves this obligation
   open (RUN_REPORT §4). What exists instead is the eng1000 feature-space geometry in viz2a/viz2b, computed
   from the real eng1000 matrix.
4. Round-M 6-stimulus figures already exist at `/mnt/agents/work/tribe/fig*.png` and pipeline figures at
   `/mnt/agents/output/figures/docas/pipeline/`; this set complements rather than duplicates them (battery27
   category means + new bridge/CLICS figures).

## Reproduction notes

Environment: python 3.12, numpy 2.2.5, matplotlib 3.10.3, networkx 3.5, scikit-learn 1.7.2, nilearn 0.14.1
(pip-installed this session), h5py (pip-installed this session). Seed 42 for PCA and the spring layout.
fsaverage5 and Schaefer-400/Yeo-7 fetched via nilearn from their real public sources (nilearn_data cache).
Palette: muted green/red/ochre/slate/mauve/olive channel colors; RdBu_r diverging for cortical contrasts
(no blue-purple sequential gradients anywhere).
