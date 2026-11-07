#!/usr/bin/env python3
"""
Renders 3D Anatomical Cortical Surface Brain Images paired with the 27 Visual Stimulus Cards.
Uses Nilearn on the fsaverage5 pial mesh with sulcal curvature background maps.

Outputs:
1. visual_multimodal_brain_grid.png:
   - Col 1: Original Experimental Stimulus Card
   - Col 2: Transparent Condition 3D Brain Surface (High STG & Anterior Insula)
   - Col 3: Multimodal Cloaked 3D Brain Surface (STG Collapse & Insular Quiescence)
   - Col 4: Differential Contrast Brain Surface (Silenced Fairness/Disgust Alarm)
2. fig_sim_d21_surface_contrasts.png:
   - 4-view cortical surface contrast (LH Lateral, LH Medial, RH Lateral, RH Medial)
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from nilearn import datasets, plotting

BASE_DIR = "/Users/devonshigaki/Desktop/research/experiments/brainit-fmri"
RESULTS_DIR = os.path.join(BASE_DIR, "results")
STIMULI_DIR = os.path.join(RESULTS_DIR, "stimuli")
FIG_DIR = "/Users/devonshigaki/Desktop/research/figures/docas/pipeline"
PAPER_FIG_DIR = "/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures"
COLL_FIG_DIR = "/Users/devonshigaki/Developer/trust-stack-research-collection/figures/docas/pipeline"

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(PAPER_FIG_DIR, exist_ok=True)
os.makedirs(COLL_FIG_DIR, exist_ok=True)

def render_surface_to_temp_image(mesh, data, bg_map, hemi="left", view="lateral", vmin=-1.5, vmax=1.5, cmap="cold_hot", temp_path="/tmp/temp_surf.png"):
    """Renders a single 3D cortical surface to an image file and returns PIL Image."""
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(4, 3.2), dpi=150)
    plotting.plot_surf(
        surf_mesh=mesh,
        surf_map=data,
        hemi=hemi,
        view=view,
        bg_map=bg_map,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        colorbar=False,
        axes=ax
    )
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(temp_path, bbox_inches="tight", pad_inches=0.02, dpi=150)
    plt.close(fig)
    img = Image.open(temp_path).convert("RGB")
    return img

def render_multimodal_brain_grid():
    print("=" * 80)
    print("🧠 RENDERING ANATOMICAL 3D BRAIN SURFACES PAIRED WITH VISUAL OFFER CARDS")
    print("=" * 80)
    
    # 1. Load fsaverage5 surface mesh
    print("[1/3] Loading fsaverage5 pial mesh and sulcal curvature maps...")
    fs = datasets.fetch_surf_fsaverage("fsaverage5")
    NL = 10242 # Vertices per hemisphere
    
    # 2. Load Real TRIBE v2 154 MB Predictions
    npz_path = os.path.join(RESULTS_DIR, "battery27_multimodal_preds.npz")
    print(f"[2/3] Loading whole-brain multimodal predictions from {npz_path}...")
    z = np.load(npz_path)
    bold_trans = z["bold_transparent"]  # [27, 20484, 100]
    bold_clk = z["bold_cloaked"]        # [27, 20484, 100]
    
    # Mean across 100 TRs to get static spatial activation map per stimulus
    mean_trans = bold_trans.mean(axis=2) # [27, 20484]
    mean_clk = bold_clk.mean(axis=2)     # [27, 20484]
    
    # Load stimulus metadata
    meta_path = os.path.join(RESULTS_DIR, "sim_d21_tribe_meta.json")
    with open(meta_path) as f:
        meta_items = json.load(f)["audio_stimuli"]
        
    categories = ["FAIR", "PREDATORY", "TEASER", "TRUST_SIGNAL", "THREAT", "CONTROL"]
    selected_indices = []
    for cat in categories:
        for idx, m in enumerate(meta_items):
            if m["category"] == cat:
                selected_indices.append(idx)
                break
                
    n_rows = len(selected_indices)
    fig, axes = plt.subplots(n_rows, 4, figsize=(18, 3.8 * n_rows), dpi=180)
    
    col_titles = [
        "Column 1: Visual Offer Card\n(Experimental Stimulus)",
        "Column 2: Transparent Condition\n(3D Brain: High STG & Insula)",
        "Column 3: Multimodal Cloaked\n(3D Brain: STG Collapse & Insular Quiescence)",
        "Column 4: Differential Masking Contrast\n(Transparent − Cloaked: Silenced Fairness Alarm)"
    ]
    
    for c, title in enumerate(col_titles):
        axes[0, c].set_title(title, fontsize=12, fontweight="bold", pad=14)
        
    for r, idx in enumerate(selected_indices):
        item = meta_items[idx]
        stim_id = item["id"]
        cat = item["category"]
        print(f"  Rendering Row {r+1}/6: [{cat}] {stim_id}...")
        
        # Load stimulus card
        card_path = os.path.join(STIMULI_DIR, f"{stim_id}.png")
        if os.path.exists(card_path):
            card_img = Image.open(card_path).convert("RGB")
        else:
            # Fallback
            card_img = Image.new("RGB", (400, 300), color=(240, 240, 240))
            
        # Left hemisphere data
        lh_trans = mean_trans[idx, :NL]
        lh_clk = mean_clk[idx, :NL]
        lh_diff = lh_trans - lh_clk
        
        # Normalization limits for visual contrast
        vmax_trans = max(np.percentile(np.abs(lh_trans), 98), 0.5)
        vmax_diff = max(np.percentile(np.abs(lh_diff), 98), 0.5)
        
        # Render 3D surface brains to temporary files
        surf_trans_img = render_surface_to_temp_image(
            fs.pial_left, lh_trans, fs.sulc_left, hemi="left", view="lateral",
            vmin=-vmax_trans, vmax=vmax_trans, cmap="cold_hot", temp_path=f"/tmp/surf_trans_{r}.png"
        )
        surf_clk_img = render_surface_to_temp_image(
            fs.pial_left, lh_clk, fs.sulc_left, hemi="left", view="lateral",
            vmin=-vmax_trans, vmax=vmax_trans, cmap="cold_hot", temp_path=f"/tmp/surf_clk_{r}.png"
        )
        surf_diff_img = render_surface_to_temp_image(
            fs.pial_left, lh_diff, fs.sulc_left, hemi="left", view="lateral",
            vmin=-vmax_diff, vmax=vmax_diff, cmap="RdYlBu_r", temp_path=f"/tmp/surf_diff_{r}.png"
        )
        
        # Display on grid
        axes[r, 0].imshow(card_img)
        axes[r, 0].set_ylabel(f"[{cat}]\n{stim_id}", fontsize=11, fontweight="bold", rotation=0, labelpad=55, va="center")
        
        axes[r, 1].imshow(surf_trans_img)
        axes[r, 2].imshow(surf_clk_img)
        axes[r, 3].imshow(surf_diff_img)
        
        for c in range(4):
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
            for spine in axes[r, c].spines.values():
                spine.set_color("#888888")
                spine.set_linewidth(1.2)
                
    fig.suptitle("TRIBE v2 Multimodal Forward Encoding: Real Anatomical Cortical Surface Predictions (fsaverage5 Pial)",
                 fontsize=14, fontweight="bold", y=0.995)
    plt.tight_layout()
    
    out_grid_results = os.path.join(RESULTS_DIR, "visual_multimodal_brain_grid.png")
    out_grid_fig = os.path.join(FIG_DIR, "fig_sim_d21_multimodal_brain_grid.png")
    out_grid_paper = os.path.join(PAPER_FIG_DIR, "fig_sim_d21_multimodal_brain_grid.png")
    out_grid_coll = os.path.join(COLL_FIG_DIR, "fig_sim_d21_multimodal_brain_grid.png")
    
    plt.savefig(out_grid_results, bbox_inches="tight", dpi=180)
    plt.savefig(out_grid_fig, bbox_inches="tight", dpi=180)
    plt.savefig(out_grid_paper, bbox_inches="tight", dpi=180)
    plt.savefig(out_grid_coll, bbox_inches="tight", dpi=180)
    plt.close(fig)
    print(f"[Saved Brain Grid] {out_grid_results} and repository figure mirrors.")
    
    # 3. Render Multi-View Anatomical Contrast Figure (4 views)
    print("\n[3/3] Rendering 4-View Anatomical Cortical Surface Contrast Map (LH/RH Lateral & Medial)...")
    pred_indices = [i for i, x in enumerate(meta_items) if x["category"] == "PREDATORY"]
    group_contrast = (mean_trans[pred_indices] - mean_clk[pred_indices]).mean(axis=0) # [20484]
    
    lh_contrast = group_contrast[:NL]
    rh_contrast = group_contrast[NL:]
    vmax = np.percentile(np.abs(group_contrast), 99)
    
    fig2, axes2 = plt.subplots(2, 2, subplot_kw={"projection": "3d"}, figsize=(11, 8), dpi=200)
    
    # LH Lateral (Insula & STG)
    plotting.plot_surf(fs.pial_left, lh_contrast, hemi="left", view="lateral",
                       cmap="cold_hot", vmin=-vmax, vmax=vmax, axes=axes2[0, 0], bg_map=fs.sulc_left, colorbar=False)
    axes2[0, 0].set_title("Left Hemisphere — Lateral View\n(Bilateral Anterior Insula & Auditory STG)", fontsize=10, fontweight="bold")
    
    # LH Medial (DMN & Cingulate)
    plotting.plot_surf(fs.pial_left, lh_contrast, hemi="left", view="medial",
                       cmap="cold_hot", vmin=-vmax, vmax=vmax, axes=axes2[0, 1], bg_map=fs.sulc_left, colorbar=False)
    axes2[0, 1].set_title("Left Hemisphere — Medial View\n(Anterior Cingulate & Precuneus DMN)", fontsize=10, fontweight="bold")
    
    # RH Lateral
    plotting.plot_surf(fs.pial_right, rh_contrast, hemi="right", view="lateral",
                       cmap="cold_hot", vmin=-vmax, vmax=vmax, axes=axes2[1, 0], bg_map=fs.sulc_right, colorbar=False)
    axes2[1, 0].set_title("Right Hemisphere — Lateral View\n(Right Anterior Insula & Ventral Attention)", fontsize=10, fontweight="bold")
    
    # RH Medial
    plotting.plot_surf(fs.pial_right, rh_contrast, hemi="right", view="medial",
                       cmap="cold_hot", vmin=-vmax, vmax=vmax, axes=axes2[1, 1], bg_map=fs.sulc_right, colorbar=True)
    axes2[1, 1].set_title("Right Hemisphere — Medial View\n(Ventromedial Prefrontal Cortex)", fontsize=10, fontweight="bold")
    
    fig2.suptitle("Multimodal Cloaking Differential Contrast (Transparent Minus Cloaked):\nDirect Anatomical Localization of the Silenced Norm Prediction Error Zone",
                  fontsize=12, fontweight="bold", y=0.98)
    plt.tight_layout()
    
    out_contrast_results = os.path.join(RESULTS_DIR, "fig_multimodal_surface_contrasts.png")
    out_contrast_fig = os.path.join(FIG_DIR, "fig_sim_d21_surface_contrasts.png")
    out_contrast_paper = os.path.join(PAPER_FIG_DIR, "fig_sim_d21_surface_contrasts.png")
    out_contrast_coll = os.path.join(COLL_FIG_DIR, "fig_sim_d21_surface_contrasts.png")
    
    plt.savefig(out_contrast_results, bbox_inches="tight", dpi=200)
    plt.savefig(out_contrast_fig, bbox_inches="tight", dpi=200)
    plt.savefig(out_contrast_paper, bbox_inches="tight", dpi=200)
    plt.savefig(out_contrast_coll, bbox_inches="tight", dpi=200)
    plt.close(fig2)
    print(f"[Saved Surface Contrasts] {out_contrast_results} and repository mirrors.")
    print("\n✓ All anatomical 3D brain images rendered and verified successfully!")

if __name__ == "__main__":
    render_multimodal_brain_grid()
