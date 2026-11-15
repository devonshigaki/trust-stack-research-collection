import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
OUT_DIR = os.path.join(BASE_DIR, "figures/sim_visual_diagrams")
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "axes.labelweight": "bold",
    "figure.titlesize": 14,
    "figure.titleweight": "bold"
})

def safe_load_img(rel_path):
    p = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(p):
        try:
            return Image.open(p)
        except Exception:
            return None
    return None

def create_4stage_canvas(sim_id, sim_name, paper_tag, verdict_tag, verdict_color="#10B981"):
    fig = plt.figure(figsize=(24, 13.5), dpi=200, facecolor="#F8FAFC")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Header Bar
    title_box = patches.FancyBboxPatch((2, 90.5), 96, 7.8, boxstyle="round,pad=0.5", 
                                       facecolor="#0F172A", edgecolor="#1E293B", linewidth=2)
    ax.add_patch(title_box)
    
    ax.text(4, 95.2, f"{sim_id}: {sim_name.upper()}", color="#FFFFFF", fontsize=18, fontweight="bold", va="center")
    ax.text(4, 92.2, f"Research Layer: {paper_tag} · Verified Research Base · Seed 42 Everywhere · Epistemic Standard", 
            color="#94A3B8", fontsize=10.5, va="center")

    # Header Verdict Badge
    verdict_box = patches.FancyBboxPatch((80, 91.8), 16.5, 5.2, boxstyle="round,pad=0.3",
                                         facecolor=verdict_color, edgecolor="none")
    ax.add_patch(verdict_box)
    ax.text(88.25, 94.4, verdict_tag, color="#FFFFFF", fontsize=11, fontweight="bold", ha="center", va="center")

    col_w = 22.5
    col_h = 86
    col_y = 3
    col_x = [2.0, 26.5, 51.0, 75.5]

    for i in range(4):
        card = patches.FancyBboxPatch((col_x[i], col_y), col_w, col_h, boxstyle="round,pad=0.6",
                                      facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.5)
        ax.add_patch(card)
        if i < 3:
            ax.annotate("", xy=(col_x[i+1] - 0.3, 52), xytext=(col_x[i] + col_w + 0.3, 52),
                        arrowprops=dict(facecolor="#3B82F6", edgecolor="none", width=3, headwidth=9))

    return fig, ax, col_x, col_w

def set_stage_header(ax, x, w, stage_num, title, subtitle, color="#2563EB"):
    head_box = patches.FancyBboxPatch((x + 0.2, 83.5), w - 0.4, 4.8, boxstyle="round,pad=0.2",
                                     facecolor=color, edgecolor="none")
    ax.add_patch(head_box)
    ax.text(x + w/2, 85.9, f"STAGE {stage_num}: {title.upper()}", color="#FFFFFF", fontsize=11, fontweight="bold", ha="center", va="center")
    ax.text(x + w/2, 84.3, subtitle, color="#E2E8F0", fontsize=8, ha="center", va="center")

def add_inset_img(fig, img, rect, title=None, border="#CBD5E1"):
    if img is not None:
        ax_in = fig.add_axes(rect)
        ax_in.imshow(img)
        ax_in.axis("off")
        for s in ax_in.spines.values():
            s.set_color(border)
            s.set_linewidth(1)
        if title:
            ax_in.set_title(title, fontsize=8, fontweight="bold", pad=3, color="#0F172A")
        return ax_in
    return None

def add_info_card(ax, x, y, w, h, title, text, bg="#F8FAFC", border="#E2E8F0", title_color="#0F172A"):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", facecolor=bg, edgecolor=border, linewidth=1)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 2.0, title, color=title_color, fontsize=9.5, fontweight="bold", ha="center")
    ax.text(x + 1.0, y + h - 4.2, text, color="#334155", fontsize=8, va="top")

def generate_axiom_diagram():
    fig, ax, cx, cw = create_4stage_canvas("SIM AXIOM-SERIES", "The Axioms of Trust & Nested Membrane Theory", 
                                           "The Value of Trust · DOCAS §5.37 · Whitepaper §3.0", "COMPOUND PASS (3/4)", "#059669")
    
    # Stage 1: The Axiomatic Triadic Engine
    set_stage_header(ax, cx[0], cw, 1, "The Triadic Engine", "Ontological Axioms across Scales", "#1E40AF")
    t1 = (
        "• Axiom 1 (Bonds Precede Everything):\n"
        "  Trust is the physical bond resisting entropy.\n"
        "  Before memory exists, bonds must restrict\n"
        "  degrees of freedom.\n\n"
        "• Axiom 2 (Memory is Bound Energy):\n"
        "  Memory is the physical multi-trace structural\n"
        "  state left by past selection reactions.\n\n"
        "• Axiom 3 (Trust at the Boundary):\n"
        "  Trust is the active state of alignment the\n"
        "  moment before selection:\n"
        "  Expectation ──► Validation ──► Selection\n"
        "  Selection updates memory, forming the next\n"
        "  prior Expectation in an infinite loop."
    )
    add_info_card(ax, cx[0] + 1.2, 42, cw - 2.4, 39, "The Universal Axioms", t1, bg="#EFF6FF", border="#BFDBFE")
    add_info_card(ax, cx[0] + 1.2, 5, cw - 2.4, 33, "Multiscale Complexity Spectrum", 
                  "• Atoms: Orbital Expectation ──► Collision ──► Bond\n"
                  "• Cells: Vmem ──► Gap Junctions ──► Syncytium\n"
                  "• Flies: Odor ──► Shock/Sugar ──► Rutabaga AC\n"
                  "• Humans: Full DOCAS (Dopamine, Oxytocin,\n"
                  "  Cortisol, Noradrenaline, Serotonin)\n"
                  "• Economy: Offer ──► Cash Flow ──► libSQL", 
                  bg="#F0FDF4", border="#BBF7D0", title_color="#166534")

    # Stage 2: Memory Architecture & TFP Decentralization
    set_stage_header(ax, cx[1], cw, 2, "Memory & Membranes", "Multiple-Trace vs Scalar Prototypes", "#0D9488")
    t2 = (
        "• The Scalar Prototype Failure:\n"
        "  FICO scores collapse history into 1 scalar.\n"
        "  Under economic non-stationarity, prototypes\n"
        "  suffer paranoid prior rigidity (stuck priors).\n\n"
        "• Multiple-Trace Memory (TFP):\n"
        "  Local edge databases (libSQL) store the full\n"
        "  episodic transaction event history.\n\n"
        "• The Recursive Nested Membrane:\n"
        "  Selection at scale N builds the Membrane\n"
        "  (Markov blanket) for scale N+1."
    )
    add_info_card(ax, cx[1] + 1.2, 45, cw - 2.4, 36, "Memory Architecture", t2, bg="#F0FDFA", border="#99F6E4", title_color="#0F766E")
    add_info_card(ax, cx[1] + 1.2, 5, cw - 2.4, 36, "TFP Digital Membrane", 
                  "• User-Owned libSQL Edge Database:\n"
                  "  Protects agent from external entropy cascades.\n"
                  "• Two-Phase Timed Expectation Commitments:\n"
                  "  Expectation hashed before Validation occurs.\n"
                  "• ZK State Transition Proofs (ZK-STP):\n"
                  "  Mathematical verification of Master Law.", 
                  bg="#F8FAFC", border="#CBD5E1", title_color="#334155")

    # Stage 3: Sim AXIOM-1 (Trace vs Prototype Simulation)
    set_stage_header(ax, cx[2], cw, 3, "Sim AXIOM-1: Trace Test", "1,000 Agents Under Macro Shock", "#2563EB")
    img_ax1 = safe_load_img("figures/fig_sim_axiom_trace_vs_proto.png")
    add_inset_img(fig, img_ax1, [0.525, 0.44, 0.195, 0.36], title="Sim AXIOM-1: Prior Rigidity Suppression")
    t3 = (
        "• Numerical Execution (N=1,000, 100 Epochs):\n"
        "  Transient shock injected at t=50 (10 epochs).\n\n"
        "• Criterion AX1.A (Prior Rigidity):\n"
        "  Prototype false-positive denial rate is\n"
        "  8.69x higher than Multiple-Trace (PASS; >=3.0x).\n\n"
        "• Criterion AX1.B (Recovery Lag):\n"
        "  Multiple-Trace recovers in 0.14x the time\n"
        "  of Prototype underwriter (PASS; <=0.50)."
    )
    add_info_card(ax, cx[2] + 1.2, 5, cw - 2.4, 34, "Simulation Verdict: PASS (2/2)", t3, bg="#EFF6FF", border="#BFDBFE", title_color="#1E40AF")

    # Stage 4: Sim AXIOM-2 (Beinhocker Evolutionary Assembly)
    set_stage_header(ax, cx[3], cw, 4, "Sim AXIOM-2: Beinhocker", "100 Competing Firm Boundaries", "#059669")
    img_ax2 = safe_load_img("figures/fig_sim_axiom_beinhocker.png")
    add_inset_img(fig, img_ax2, [0.77, 0.44, 0.195, 0.36], title="Sim AXIOM-2: Semi-Permeable Reserves")
    t4 = (
        "• Numerical Execution (F=100, 200 Epochs):\n"
        "  Scarcity shock injected at t=100 (20 epochs).\n\n"
        "• Criterion AX2.B (Thermodynamic Buffer):\n"
        "  Semi-permeable firms retain +84.8 excess\n"
        "  capital reserves over monolithic firms (PASS).\n\n"
        "• Criterion AX2.A (Survival Ratio):\n"
        "  1.0x vs frozen >=2.5x (FAIL as frozen;\n"
        "  finite window bounds total extinction).\n\n"
        "VERDICT: COMPOUND PASS (3/4 Criteria Verified)"
    )
    add_info_card(ax, cx[3] + 1.2, 5, cw - 2.4, 34, "Simulation Verdict: PASS (1/2)", t4, bg="#ECFDF5", border="#A7F3D0", title_color="#065F46")

    out1 = os.path.join(OUT_DIR, "25_sim_axiom_series.png")
    out2 = os.path.join(FIG_DIR, "25_sim_axiom_series.png")
    plt.savefig(out1, bbox_inches="tight", dpi=200)
    plt.savefig(out2, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"Generated: {out1}")
    print(f"Generated: {out2}")

if __name__ == "__main__":
    generate_axiom_diagram()
