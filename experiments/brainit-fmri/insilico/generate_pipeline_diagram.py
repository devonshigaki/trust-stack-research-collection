"""
Pipeline Architecture Infographic Generator.
Composes real visual stimuli, 3D cortical surface maps, Brain-IT decoded images,
and Sim D16 behavioral exploitation curves into an end-to-end scientific pipeline diagram.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def build_pipeline_diagram(output_path="results/pipeline_architecture_diagram.png"):
    base_dir = "/Users/devonshigaki/Desktop/research"
    results_dir = os.path.join(base_dir, "brainit-fmri/results")

    # Load actual assets
    img_pred = Image.open(os.path.join(results_dir, "stimuli/PREDATORY_1.png"))
    img_fair = Image.open(os.path.join(results_dir, "stimuli/FAIR_1.png"))
    
    # Brain assets
    img_brain_surf = Image.open(os.path.join(base_dir, "figures/docas/fig2_contrast_threat_minus_fair.png"))
    img_yeo7 = Image.open(os.path.join(base_dir, "figures/docas/fig4_yeo7_network_contrast.png"))
    
    # Decoded images
    gallant_recons = np.load(os.path.join(results_dir, "gallant_recons.npy"))
    struct_recons = np.load(os.path.join(results_dir, "brainit_structural_recons.npy"))
    dual_recons = np.load(os.path.join(results_dir, "brainit_dual_recons.npy"))
    # Index 5 is PREDATORY_1
    pred_idx = 5
    img_gal = gallant_recons[pred_idx]
    img_str = struct_recons[pred_idx]
    img_dua = dual_recons[pred_idx]

    # Sim D16 figure
    img_d16_full = Image.open(os.path.join(results_dir, "fig_sim_d16_cloaking.png"))
    # Crop Panel (c) Vulnerability Gradient from the 2x2 grid (bottom-left quadrant)
    w_d16, h_d16 = img_d16_full.size
    img_d16_curve = img_d16_full.crop((0, int(h_d16 * 0.48), int(w_d16 * 0.52), h_d16))

    # Create figure canvas (24x13.5 inches at 200 dpi)
    fig = plt.figure(figsize=(24, 13.5), dpi=200, facecolor="#F8FAFC")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # --- Title Banner ---
    title_box = patches.FancyBboxPatch((2, 90.5), 96, 7.8, boxstyle="round,pad=0.5", 
                                       facecolor="#0F172A", edgecolor="#1E293B", linewidth=2)
    ax.add_patch(title_box)
    ax.text(50, 95.2, "THE CLOSED-LOOP IN-SILICO NEUROMORPHIC RESEARCH PIPELINE", 
            color="#FFFFFF", fontsize=20, fontweight="bold", ha="center", va="center")
    ax.text(50, 92.2, "From Visual Contract Design → Cortical BOLD Encoding (TRIBE v2) → Dual-Branch Decoding (Brain-IT) → Behavioral Exploitation Gating (Sim D16)", 
            color="#94A3B8", fontsize=11, fontweight="medium", ha="center", va="center")

    # Column container dimensions
    col_w = 22.5
    col_h = 86
    col_y = 3

    # =========================================================================
    # STAGE 1: Visual Stimulus Design (Col 1: x = 2 to 24.5)
    # =========================================================================
    s1_bg = patches.FancyBboxPatch((2, col_y), col_w, col_h, boxstyle="round,pad=0.6",
                                   facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(s1_bg)
    s1_head = patches.FancyBboxPatch((2.2, 83.5), col_w - 0.4, 4.8, boxstyle="round,pad=0.2",
                                    facecolor="#EF4444", edgecolor="none")
    ax.add_patch(s1_head)
    ax.text(2 + col_w/2, 85.9, "STAGE 1: INPUT STIMULI", color="#FFFFFF", fontsize=12, fontweight="bold", ha="center", va="center")
    ax.text(2 + col_w/2, 84.3, "Visual Financial Agreements (27 Conditions)", color="#FEE2E2", fontsize=8.5, ha="center", va="center")

    # Inset stimulus images
    # Predatory image
    ax_p = fig.add_axes([0.035, 0.58, 0.085, 0.17])
    ax_p.imshow(img_pred)
    ax_p.axis("off")
    ax.text(7.75, 76.5, "Predatory Offer Display", color="#991B1B", fontsize=9, fontweight="bold", ha="center")
    ax.text(7.75, 56.2, "[High Promo Headline: 0% APR*]", color="#DC2626", fontsize=7.5, ha="center")

    # Fair image
    ax_f = fig.add_axes([0.135, 0.58, 0.085, 0.17])
    ax_f.imshow(img_fair)
    ax_f.axis("off")
    ax.text(17.75, 76.5, "Fair Offer Display", color="#1E40AF", fontsize=9, fontweight="bold", ha="center")
    ax.text(17.75, 56.2, "[Balanced Schedule: 9.0% Fixed]", color="#2563EB", fontsize=7.5, ha="center")

    # Visual Cloaking Mechanism Callout Box
    cloaking_box = patches.FancyBboxPatch((3.5, 28), 19.5, 24, boxstyle="round,pad=0.4",
                                          facecolor="#FEF2F2", edgecolor="#FECACA", linewidth=1)
    ax.add_patch(cloaking_box)
    ax.text(13.25, 49.5, "Perceptual Cloaking Architecture", color="#991B1B", fontsize=10, fontweight="bold", ha="center")
    
    body_s1 = (
        "• Asymmetric Visual Salience:\n"
        "  Promotional header: High-contrast,\n"
        "  large stroke, bold urgency ('ACT NOW').\n\n"
        "• Fine-Print Disclaimer:\n"
        "  Buries 390% APR rollover penalty\n"
        "  in low-contrast, microscopic footer.\n\n"
        "• Visual Cloaking Ratio (χ):\n"
        "  χ = E_promo / (E_disc + ε)\n"
        "  Predatory: High header energy\n"
        "  Fair: Isomorphic balanced layout"
    )
    ax.text(4.5, 47, body_s1, color="#334155", fontsize=8.5, va="top")

    # Battery badge
    bat_badge = patches.FancyBboxPatch((3.5, 6), 19.5, 18, boxstyle="round,pad=0.4",
                                       facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(bat_badge)
    ax.text(13.25, 21.5, "27-Stimulus DOCAS Battery", color="#0F172A", fontsize=9.5, fontweight="bold", ha="center")
    ax.text(13.25, 18.5, "• 5 FAIR Credit Disclosures", color="#475569", fontsize=8, ha="center")
    ax.text(13.25, 16.0, "• 5 PREDATORY Fast Cash Offers", color="#475569", fontsize=8, ha="center")
    ax.text(13.25, 13.5, "• 5 TEASER Promotional Cards", color="#475569", fontsize=8, ha="center")
    ax.text(13.25, 11.0, "• 5 TRUST_SIGNAL Insured Cards", color="#475569", fontsize=8, ha="center")
    ax.text(13.25, 8.5, "• 5 THREAT Arrears Notices", color="#475569", fontsize=8, ha="center")
    ax.text(13.25, 6.0, "• 2 CONTROL Natural Scenes", color="#475569", fontsize=8, ha="center")

    # Arrow S1 -> S2
    ax.annotate("", xy=(26.2, 52), xytext=(24.2, 52),
                arrowprops=dict(facecolor="#3B82F6", edgecolor="none", width=3, headwidth=9))

    # =========================================================================
    # STAGE 2: Biological Brain Encoding (Col 2: x = 26.5 to 49)
    # =========================================================================
    s2_bg = patches.FancyBboxPatch((26.5, col_y), col_w, col_h, boxstyle="round,pad=0.6",
                                   facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(s2_bg)
    s2_head = patches.FancyBboxPatch((26.7, 83.5), col_w - 0.4, 4.8, boxstyle="round,pad=0.2",
                                    facecolor="#2563EB", edgecolor="none")
    ax.add_patch(s2_head)
    ax.text(26.5 + col_w/2, 85.9, "STAGE 2: BRAIN ENCODING", color="#FFFFFF", fontsize=12, fontweight="bold", ha="center", va="center")
    ax.text(26.5 + col_w/2, 84.3, "Meta TRIBE v2 Multimodal Cortex Model", color="#DBEAFE", fontsize=8.5, ha="center", va="center")

    # Inset 3D Brain Surface Map
    ax_b = fig.add_axes([0.28, 0.57, 0.19, 0.19])
    ax_b.imshow(img_brain_surf)
    ax_b.axis("off")
    ax.text(37.75, 77.2, "Simulated 3D Cortical BOLD Response", color="#1E3A8A", fontsize=9.5, fontweight="bold", ha="center")
    ax.text(37.75, 56.2, "fsaverage5 Cortical Mesh (20,484 Vertices)", color="#3B82F6", fontsize=8, ha="center")

    # Brain Network Dissociation Box
    brain_box = patches.FancyBboxPatch((28, 30), 19.5, 23, boxstyle="round,pad=0.4",
                                       facecolor="#EFF6FF", edgecolor="#BFDBFE", linewidth=1)
    ax.add_patch(brain_box)
    ax.text(37.75, 50.5, "Cortical Network Dissociation (H1)", color="#1E40AF", fontsize=9.5, fontweight="bold", ha="center")
    
    body_s2 = (
        "• Early Sensory Stream (V1–V4):\n"
        "  Preserves typographical edges, borders,\n"
        "  and layout geometry invariantly\n"
        "  across all offer conditions (SSIM Δ < 0.10).\n\n"
        "• Associative Valuation Networks:\n"
        "  THREAT and PREDATORY stimuli induce\n"
        "  selective functional displacement in\n"
        "  Default Mode (pCunPCC) and\n"
        "  Frontoparietal Control networks."
    )
    ax.text(29, 48.5, body_s2, color="#1E293B", fontsize=8.2, va="top")

    # Inset Yeo-7 Network Graph
    ax_y = fig.add_axes([0.285, 0.08, 0.18, 0.15])
    ax_y.imshow(img_yeo7)
    ax_y.axis("off")
    ax.text(37.75, 24.2, "Yeo-7 Functional Network Contrasts", color="#0F172A", fontsize=8.5, fontweight="bold", ha="center")

    # Arrow S2 -> S3
    ax.annotate("", xy=(50.7, 52), xytext=(48.7, 52),
                arrowprops=dict(facecolor="#10B981", edgecolor="none", width=3, headwidth=9))

    # =========================================================================
    # STAGE 3: Decoding & Brain-IT Resolution (Col 3: x = 51 to 73.5)
    # =========================================================================
    s3_bg = patches.FancyBboxPatch((51, col_y), col_w, col_h, boxstyle="round,pad=0.6",
                                   facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(s3_bg)
    s3_head = patches.FancyBboxPatch((51.2, 83.5), col_w - 0.4, 4.8, boxstyle="round,pad=0.2",
                                    facecolor="#059669", edgecolor="none")
    ax.add_patch(s3_head)
    ax.text(51 + col_w/2, 85.9, "STAGE 3: DUAL-BRANCH DECODING", color="#FFFFFF", fontsize=12, fontweight="bold", ha="center", va="center")
    ax.text(51 + col_w/2, 84.3, "Weizmann Institute Brain-IT (ICLR 2026)", color="#D1FAE5", fontsize=8.5, ha="center", va="center")

    # 3-Panel Visual Reconstruction Comparison
    # Gallant (Old)
    ax_g = fig.add_axes([0.522, 0.61, 0.065, 0.13])
    ax_g.imshow(img_gal)
    ax_g.axis("off")
    ax.text(55.4, 75.2, "Legacy Gallant", color="#64748B", fontsize=8, fontweight="bold", ha="center")
    ax.text(55.4, 59.5, "SSIM: 0.327\nBlurred Candidate Avg", color="#94A3B8", fontsize=6.5, ha="center")

    # Brain-IT Structural (Branch A)
    ax_st = fig.add_axes([0.595, 0.61, 0.065, 0.13])
    ax_st.imshow(img_str)
    ax_st.axis("off")
    ax.text(62.7, 75.2, "Brain-IT Branch A", color="#2563EB", fontsize=8, fontweight="bold", ha="center")
    ax.text(62.7, 59.5, "VGG Contrastive\nLayout & Margins", color="#3B82F6", fontsize=6.5, ha="center")

    # Brain-IT Dual-Branch (Branch B)
    ax_du = fig.add_axes([0.668, 0.61, 0.065, 0.13])
    ax_du.imshow(img_dua)
    ax_du.axis("off")
    ax.text(70.0, 75.2, "Brain-IT Dual-Branch", color="#059669", fontsize=8, fontweight="bold", ha="center")
    ax.text(70.0, 59.5, "SSIM: 0.748\nSharp Dual-Branch", color="#10B981", fontsize=6.5, ha="center")

    # Resolution Breakthrough Metrics Box
    res_box = patches.FancyBboxPatch((52.5, 23), 19.5, 33, boxstyle="round,pad=0.4",
                                     facecolor="#F0FDF4", edgecolor="#BBF7D0", linewidth=1)
    ax.add_patch(res_box)
    ax.text(62.25, 53.5, "Instrument Resolution Leap (H2)", color="#166534", fontsize=10, fontweight="bold", ha="center")
    
    body_s3 = (
        "• Eliminating the Retrieval Null:\n"
        "  Legacy Gallant decoder suffered from\n"
        "  spatial blur & chance retrieval (3.7%).\n"
        "  Brain-IT elevates Top-1 retrieval to\n"
        "  51.9% (14/27 correct, p = 0.0005).\n\n"
        "• Quantitative Quality Leap:\n"
        "  - SSIM: 0.7723 vs 0.3612 (+41.1% gain)\n"
        "  - LPIPS: 0.1539 vs 0.4310 (-64.3% error)\n"
        "  - CLIP Cosine: 0.9301 (high semantic match)\n\n"
        "• Strong Platonic Representation (H3):\n"
        "  Cross-encoder manifold correlation\n"
        "  Mantel r = 0.9923 (p < 0.0001)."
    )
    ax.text(53.5, 51.5, body_s3, color="#064E3B", fontsize=8.2, va="top")

    # GMM Cluster Graph Callout
    gmm_badge = patches.FancyBboxPatch((52.5, 6), 19.5, 14, boxstyle="round,pad=0.3",
                                       facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1)
    ax.add_patch(gmm_badge)
    ax.text(62.25, 17.5, "128 GMM Cluster Spatial Graph", color="#0F172A", fontsize=9, fontweight="bold", ha="center")
    ax.text(62.25, 14.5, "v2c_128_mapping_gmm_v2.npy", color="#475569", fontsize=7.5, ha="center")
    ax.text(62.25, 11.5, "Coupled to TransformerConv Graph Neural Net", color="#64748B", fontsize=7.5, ha="center")
    ax.text(62.25, 8.5, "Dual Output: 7,190 VGG + 256 CLIP Tokens", color="#059669", fontsize=7.5, fontweight="bold", ha="center")

    # Arrow S3 -> S4
    ax.annotate("", xy=(75.2, 52), xytext=(73.2, 52),
                arrowprops=dict(facecolor="#8B5CF6", edgecolor="none", width=3, headwidth=9))

    # =========================================================================
    # STAGE 4: Behavioral Exploitation Gating (Col 4: x = 75.5 to 98)
    # =========================================================================
    s4_bg = patches.FancyBboxPatch((75.5, col_y), col_w, col_h, boxstyle="round,pad=0.6",
                                   facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(s4_bg)
    s4_head = patches.FancyBboxPatch((75.7, 83.5), col_w - 0.4, 4.8, boxstyle="round,pad=0.2",
                                    facecolor="#7C3AED", edgecolor="none")
    ax.add_patch(s4_head)
    ax.text(75.5 + col_w/2, 85.9, "STAGE 4: COGNITIVE EXPLOITATION", color="#FFFFFF", fontsize=12, fontweight="bold", ha="center", va="center")
    ax.text(75.5 + col_w/2, 84.3, "Sim D16: 1,000 Heterogeneous Agents", color="#EDE9FE", fontsize=8.5, ha="center", va="center")

    # Inset Decile Vulnerability Curve
    ax_d = fig.add_axes([0.768, 0.54, 0.205, 0.22])
    ax_d.imshow(img_d16_curve)
    ax_d.axis("off")
    ax.text(86.75, 77.2, "Cognitive Vulnerability Gradient (C3)", color="#5B21B6", fontsize=9.5, fontweight="bold", ha="center")

    # 38.9x Exploitation Banner
    harm_box = patches.FancyBboxPatch((77, 34), 19.5, 17, boxstyle="round,pad=0.4",
                                      facecolor="#FAF5FF", edgecolor="#DDD6FE", linewidth=1)
    ax.add_patch(harm_box)
    ax.text(86.75, 48.5, "CORE EMPIRICAL FINDING", color="#6D28D9", fontsize=9.5, fontweight="bold", ha="center")
    ax.text(86.75, 43.5, "38.9× Odds Ratio", color="#DC2626", fontsize=16, fontweight="bold", ha="center")
    ax.text(86.75, 39.5, "Exploitation Concentration in Lowest Decile", color="#7C3AED", fontsize=8.2, fontweight="bold", ha="center")
    ax.text(86.75, 36.5, "Stressed (D1) vs Secure (D10) Consumers", color="#64748B", fontsize=7.5, ha="center")

    # Dual-Branch Decision Rule Box
    rule_box = patches.FancyBboxPatch((77, 6), 19.5, 25, boxstyle="round,pad=0.4",
                                      facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(rule_box)
    ax.text(86.75, 28.5, "Dual-Branch Decision Model", color="#0F172A", fontsize=9.5, fontweight="bold", ha="center")
    
    body_s4 = (
        "• Attention Discovery Filter:\n"
        "  P_disc = σ( γ · ( κ_i / χ  -  τ ) )\n"
        "  κ_i: Agent cognitive bandwidth\n"
        "  χ: Visual cloaking ratio (promo/disc)\n\n"
        "• Bounded Rationality Takeaway:\n"
        "  Consumers are not 'irrational' —\n"
        "  predatory graphic design hijacks human\n"
        "  visual bandwidth during financial distress.\n\n"
        "• Regulatory Policy Standard:\n"
        "  Mandating typographic contrast &\n"
        "  isomorphic font sizing abolishes the trap."
    )
    ax.text(78, 26.5, body_s4, color="#334155", fontsize=7.8, va="top")

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"[Diagram Complete] Successfully rendered pipeline architecture infographic to: {output_path}")

if __name__ == "__main__":
    build_pipeline_diagram()
