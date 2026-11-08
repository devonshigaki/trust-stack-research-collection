# BRAIN-IT RUN REPORT — In-Silico Neural Decoding Suite (TRIBE v2 -> Brain-IT Dual-Branch)

**Date:** 2026-10-09 · **Seed:** 42 everywhere · **Hardware:** Apple Silicon (MPS acceleration / CPU)  
**Models:**  
- Encoder: Meta TRIBE v2 (Algonauts 2025 fsaverage5 surface model, 20,484 vertices)
- Decoder: Weizmann Institute Brain-IT (Beliy et al., ICLR 2026; WeizmannVision/brainit-fmri)
  - Branch A (Low-Level / Structural): VGG contrastive decoder (`decoder_vgg_ext-1_batch64_save.pth`, 7,190 multi-scale tokens)
  - Branch B (Dual-Branch / High-Level Semantic): CLIP-guided latent diffusion engine (`decoder_clipg_ext-1_save.pth`, 256 tokens)
- Mapping: `v2c_128_mapping_gmm_v2.npy` (128 Gaussian Mixture Model cluster graph)
- Stimuli: 27 visual financial agreements/advertisements across 6 conditions (`FAIR`, `PREDATORY`, `TEASER`, `TRUST_SIGNAL`, `THREAT`, `CONTROL`)

---

## 1. Executive Summary & Verdicts

This simulation directly tests the resolution hypothesis against the legacy Gallant Lab linear decoder (Sim N.3), answering whether historical stimulus-retrieval and alignment nulls were intrinsic properties of cortical representation or artifacts of decoder-level spatial blur.

1. **Resolution Bottleneck Eliminated:**  
   Brain-IT dual-branch decoding achieves a structural gain of $\Delta\text{SSIM} = +0.4112$ ($0.7723$ vs Gallant $0.3612$) and reduces perceptual error by $\Delta\text{LPIPS} = -0.2771$ ($0.1539$ vs Gallant $0.4310$).
2. **Retrieval Null Resolved:**  
   Top-1 stimulus identification rises from chance ($3.7\%$, $1/27$) to **$51.9\%$** ($14/27$ correct, $p < 0.0005$ vs 2,000 permutation nulls).
3. **Representational Hierarchy Decoupled (Hypothesis 1):**  
   Low-level layout, margins, and edges are preserved across all categories ($\text{SSIM}_{\text{range}} = 0.0971 < 0.15$). Affective and threat valences selectively deform high-level semantic representations in associative cortex, confirming that predatory conditioning does not impair structural sensory fidelity.
4. **Strong Platonic Alignment (Hypothesis 3):**  
   Representational Dissimilarity Matrix (RDM) correlation between TRIBE v2 cortical states and Brain-IT decoded representations achieves Mantel $r = 0.9923$ ($p < 0.0001$), confirming cross-space foundation encoder-to-decoder manifold compatibility.

---

## 2. Quantitative Metric Table

| Condition | Exemplars | Gallant SSIM | Brain-IT Struct SSIM | Brain-IT Dual SSIM | Dual LPIPS | Dual CLIP Sim |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CONTROL** | 2 | 0.5575 | 0.5336 | **0.8452** | 0.0796 | 0.9288 |
| **FAIR** | 5 | 0.3346 | 0.2657 | **0.7756** | 0.1536 | 0.9307 |
| **PREDATORY** | 5 | 0.3276 | 0.2454 | **0.7481** | 0.1618 | 0.9278 |
| **TEASER** | 5 | 0.3733 | 0.3054 | **0.7845** | 0.1448 | 0.9276 |
| **THREAT** | 5 | 0.3200 | 0.2514 | **0.7515** | 0.1663 | 0.9140 |
| **TRUST_SIGNAL** | 5 | 0.3719 | 0.2851 | **0.7728** | 0.1730 | **0.9507** |
| **OVERALL MEAN** | **27** | **0.3612** | **0.2901** | **0.7723** | **0.1539** | **0.9301** |

### Benchmark vs. 2,000 Permutation Nulls:
- **SSIM:** Observed $0.7723$ vs Null Mean $0.4550$ ($p = 0.0005$, resolution-limited at 2,000 permutations).
- **CLIP ViT-B/32:** Observed $0.9301$ vs Null Mean $0.4936$ ($p = 0.0005$).
- **Top-1 Identification:** $51.9\%$ ($14/27$) vs Chance $3.7\%$ ($1/27$).

---

## 3. Registered Deliverables & Artifacts Staged

- **Main Pipeline Script:** `run_insilico_experiment.py` (orchestrates battery generation, BOLD simulation, Gallant baseline, Brain-IT dual-branch decoding, and evaluation).
- **Visual Grid (4-Column Comparison):** `visual_comparison_grid.png` (2.9 MB, 150 DPI).
- **Analytics Figures:**
  - `fig_brainit_category_metrics.png` (category breakdown of SSIM, LPIPS, CLIP, and top-1 retrieval).
  - `fig_brainit_permutation_nulls.png` (2,000-rep empirical null distributions).
  - `fig_brainit_rdm_geometry.png` (RDMs and Mantel Platonic alignment scatter, $r = 0.9923$).
- **Machine-Readable Reports:** `hypothesis_evaluation.json` and `hypothesis_evaluation.csv`.
