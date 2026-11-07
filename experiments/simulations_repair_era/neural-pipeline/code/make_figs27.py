"""DOCAS N.1 analyses + all pipeline figures for the reconstructed battery27.

Figures (150-200 dpi, honest captions carrying the reconstruction label):
  fig_n1_separability_matrix.png   27x27 pairwise Pearson, sorted by category
  fig_n1_category_contrasts.png    per-category minus CONTROL cortical maps
  fig_n1_category_contrast_matrix.png  category-level mean-map correlations
  fig_n3_decode_bars.png           LOO decode accuracy by category + null CI
  fig_n4_clics_heatmap.png         CLICS category->channel distance heatmap
Outputs also: results/battery27_separability.json, results/battery27_contrasts.json
All TRIBE predictions are model outputs on fabricated reconstructed texts.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = "/tmp/tribe"
FIG = "/tmp/agents_fig"  # overridden below
import sys
FIGDIR = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tribe/figs27"
os.makedirs(FIGDIR, exist_ok=True)

LABEL = ("reconstruction-from-spec, pending bit-identity check vs "
         "battery27_manifest.json")

preds = np.load(f"{BASE}/results/battery27_preds.npz")
battery = json.load(open(f"{BASE}/battery27_reconstructed.json"))["stimuli"]
ids = [s["id"] for s in battery]
cats = [s["category"] for s in battery]
order = sorted(range(len(ids)), key=lambda i: (cats[i], ids[i]))
ids_o = [ids[i] for i in order]
cats_o = [cats[i] for i in order]
n = len(ids)
mean_maps = np.stack([preds[i].mean(1) for i in ids_o])  # [27, 20484]

CATS = ["FAIR", "PREDATORY", "TEASER", "TRUST_SIGNAL", "THREAT", "CONTROL"]

# ---------- separability ----------
Bz = (mean_maps - mean_maps.mean(1, keepdims=True)) / mean_maps.std(1, keepdims=True)
S = Bz @ Bz.T / mean_maps.shape[1]
pairs = {}
for i in range(n):
    for j in range(i + 1, n):
        pairs[f"{ids_o[i]}|{ids_o[j]}"] = float(S[i, j])
within = [float(S[i, j]) for i in range(n) for j in range(i + 1, n)
          if cats_o[i] == cats_o[j]]
between = [float(S[i, j]) for i in range(n) for j in range(i + 1, n)
           if cats_o[i] != cats_o[j]]
sep = {"pairwise": pairs,
       "within_category_mean_r": float(np.mean(within)),
       "between_category_mean_r": float(np.mean(between)),
       "min_r": float(S[np.triu_indices(n, 1)].min()),
       "max_r_offdiag": float(S[np.triu_indices(n, 1)].max()),
       "_label": LABEL}
json.dump(sep, open(f"{BASE}/results/battery27_separability.json", "w"), indent=1)
print(f"within r={np.mean(within):.3f} between r={np.mean(between):.3f}")

fig, ax = plt.subplots(figsize=(8.5, 7))
im = ax.imshow(S, cmap="viridis", vmin=-0.5, vmax=1)
ax.set_xticks(range(n)); ax.set_xticklabels(ids_o, rotation=90, fontsize=5.5)
ax.set_yticks(range(n)); ax.set_yticklabels(ids_o, fontsize=5.5)
# category boundary lines
bounds = [i for i in range(1, n) if cats_o[i] != cats_o[i - 1]]
for b in bounds:
    ax.axhline(b - 0.5, color="w", lw=1.2)
    ax.axvline(b - 0.5, color="w", lw=1.2)
fig.colorbar(im, label="Pearson r (TR-mean cortical patterns)", shrink=0.8)
ax.set_title("Battery-27 separability — TRIBE v2 predicted fMRI (real checkpoint)\n"
             f"stimuli: {LABEL}", fontsize=9)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/fig_n1_separability_matrix.png", dpi=180)
plt.close(fig)

# ---------- category contrasts vs CONTROL ----------
cat_mean = {c: np.stack([preds[i].mean(1) for i, cc in zip(ids, cats)
                         if cc == c]).mean(0) for c in CATS}
contrasts = {f"{c}_minus_CONTROL": (cat_mean[c] - cat_mean["CONTROL"]).tolist()
             for c in CATS if c != "CONTROL"}
json.dump({"_label": LABEL,
           "note": "lists truncated in JSON; see figure",
           "summary": {k: {"mean_abs": float(np.mean(np.abs(v))),
                           "max_abs": float(np.max(np.abs(v)))}
                       for k, v in ((k, np.array(v)) for k, v in contrasts.items())}},
          open(f"{BASE}/results/battery27_contrasts.json", "w"), indent=1)

# category-level correlation matrix (6x6)
C = np.ones((6, 6))
for i, a in enumerate(CATS):
    for j, b in enumerate(CATS):
        C[i, j] = np.corrcoef(cat_mean[a], cat_mean[b])[0, 1]
fig, ax = plt.subplots(figsize=(5.6, 4.6))
im = ax.imshow(C, cmap="viridis", vmin=-0.4, vmax=1)
ax.set_xticks(range(6)); ax.set_xticklabels(CATS, rotation=45, ha="right", fontsize=8)
ax.set_yticks(range(6)); ax.set_yticklabels(CATS, fontsize=8)
for i in range(6):
    for j in range(6):
        ax.text(j, i, f"{C[i, j]:.2f}", ha="center", va="center",
                fontsize=8, color="w" if C[i, j] < 0.6 else "k")
fig.colorbar(im, label="Pearson r (category mean maps)", shrink=0.85)
ax.set_title("Category-level cortical pattern correlations\n"
             f"({LABEL})", fontsize=9)
fig.tight_layout()
fig.savefig(f"{FIGDIR}/fig_n1_category_contrast_matrix.png", dpi=180)
plt.close(fig)

# ---------- surface contrast maps ----------
# (Layout repaired: colorbars previously drawn inside the 3D axes collided
# with the row titles; they now live in dedicated slim axes rows.)
try:
    from nilearn import datasets, plotting
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable
    fs = datasets.fetch_surf_fsaverage("fsaverage5")
    NL = 10242
    n_con = len(CATS) - 1
    fig = plt.figure(figsize=(7, 2.9 * n_con))
    gs = fig.add_gridspec(2 * n_con, 2, height_ratios=[1.0, 0.045] * n_con,
                          hspace=0.9, wspace=0.05,
                          left=0.06, right=0.94, top=0.92, bottom=0.02)
    for i, c in enumerate([c for c in CATS if c != "CONTROL"]):
        con = cat_mean[c] - cat_mean["CONTROL"]
        vm = np.percentile(np.abs(con), 99)
        for j, (mesh, hemi, data, tag) in enumerate([
                (fs.pial_left, "left", con[:NL], "LH"),
                (fs.pial_right, "right", con[NL:], "RH")]):
            ax = fig.add_subplot(gs[2 * i, j], projection="3d")
            plotting.plot_surf(mesh, data, hemi=hemi, view="lateral",
                               cmap="RdBu_r", vmin=-vm, vmax=vm, axes=ax,
                               bg_map=fs.sulc_left if hemi == "left" else fs.sulc_right,
                               colorbar=False)
            ax.set_title(f"{c} - CONTROL {tag}", fontsize=8, pad=2)
            ax.set_box_aspect(None, zoom=1.25)
        cax = fig.add_subplot(gs[2 * i + 1, :])
        fig.colorbar(ScalarMappable(Normalize(-vm, vm), cmap="RdBu_r"),
                     cax=cax, orientation="horizontal")
        cax.tick_params(labelsize=6)
    fig.suptitle("Per-category cortical contrasts vs CONTROL (TRIBE v2 predictions)\n"
                 f"({LABEL})\n"
                 "model predictions on fabricated texts, not human data",
                 fontsize=8.5)
    fig.savefig(f"{FIGDIR}/fig_n1_category_contrasts.png", dpi=170)
    plt.close(fig)
    print("surface fig done ->", FIGDIR)
except Exception as e:
    print("surface figure failed:", e)


# ---------- N.3 decode bars ----------
gd_path = f"{BASE}/results/gallant_decode_results.json"
if os.path.exists(gd_path):
    gd = json.load(open(gd_path))
    per = gd["category_loo_decode"]["per_category"]
    null_ci = gd["category_loo_decode"]["null_ci95"]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    xs = list(per)
    ax.bar(xs, [per[c] for c in xs], color="#4c72b0",
           label="LOO accuracy (brain patterns)")
    ax.axhline(gd["category_loo_decode"]["accuracy"], color="#c44e52", lw=1.5,
               label=f"overall acc = {gd['category_loo_decode']['accuracy']:.2f}")
    ax.axhspan(null_ci[0], null_ci[1], color="gray", alpha=0.3,
               label=f"perm null 95% CI [{null_ci[0]:.2f}, {null_ci[1]:.2f}]")
    ax.axhline(gd["category_loo_decode"]["chance"], color="k", ls="--", lw=1,
               label=f"chance = {gd['category_loo_decode']['chance']:.2f}")
    ax.set_ylabel("accuracy")
    ax.legend(fontsize=7)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right", fontsize=8)
    ax.set_title(f"N.3 category LOO decode by category — p={gd['category_loo_decode']['p_perm']:.3f} "
                 f"({gd['n_permutations']} perms, seed {gd['seed']})\n{LABEL}", fontsize=9)
    fig.tight_layout()
    fig.savefig(f"{FIGDIR}/fig_n3_decode_bars.png", dpi=180)
    plt.close(fig)
    print("decode fig done")

# ---------- N.4 CLICS heatmap ----------
cl_path = f"{BASE}/results/clics_offer_overlap_results.json"
if os.path.exists(cl_path):
    cl = json.load(open(cl_path))
    Dm = cl["category_mean_distances_full"]
    D = np.array([[Dm[a][b] if Dm[a][b] is not None else np.nan
                   for b in CATS] for a in CATS])
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(D, cmap="magma_r", vmin=0, vmax=np.nanmax(D))
    ax.set_xticks(range(6)); ax.set_xticklabels(CATS, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(6)); ax.set_yticklabels(CATS, fontsize=8)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, f"{D[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color="w" if D[i, j] > 0.8 else "k")
    ax.set_xlabel("channel lexicon (target)")
    ax.set_ylabel("category vocabulary (source)")
    fig.colorbar(im, label="mean CLICS4 shortest-path distance", shrink=0.85)
    ax.set_title("N.4 CLICS4 colexification distances: category vocabulary -> channel lexicons\n"
                 f"(real CLICS4 graph, 51,562 edges; {LABEL})", fontsize=9)
    fig.tight_layout()
    fig.savefig(f"{FIGDIR}/fig_n4_clics_heatmap.png", dpi=180)
    plt.close(fig)
    print("clics fig done")

print("ALL FIGS DONE ->", FIGDIR)
