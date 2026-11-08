"""Honest visualizations of the real TRIBE v2 predictions.

- Surface renders via nilearn plot_surf on the bundled fsaverage5 pial mesh
- Schaefer-400/Yeo-7 parcel labels via nilearn (vol_to_surf, radius=3 mm,
  matching TRIBE's TribeSurfaceProjector config)
- No fabricated anatomy: labels come from the real downloaded atlas.
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import nibabel
from nilearn import datasets, plotting, surface

OUT = "/tmp/tribe/figs"
import os
os.makedirs(OUT, exist_ok=True)

z = np.load("/tmp/tribe/results/tribe_preds.npz")
names = ["FAIR", "PREDATORY", "TEASER", "TRUST_SIGNAL", "THREAT", "CONTROL"]
preds = {n: z[n] for n in names}  # [20484, 100]
mean_maps = {n: preds[n].mean(1) for n in names}

fs = datasets.fetch_surf_fsaverage("fsaverage5")
NL = 10242
lh = {n: mean_maps[n][:NL] for n in names}
rh = {n: mean_maps[n][NL:] for n in names}

# --- Fig 1: mean predicted response per stimulus, lateral views ---
fig, axes = plt.subplots(6, 2, subplot_kw={"projection": "3d"}, figsize=(7, 13))
for i, n in enumerate(names):
    plotting.plot_surf(fs.pial_left, lh[n], hemi="left", view="lateral",
                       cmap="RdBu_r", vmin=-0.197, vmax=0.197, axes=axes[i, 0],
                       colorbar=False, bg_map=fs.sulc_left)
    axes[i, 0].set_title(f"{n} LH", fontsize=8)
    plotting.plot_surf(fs.pial_right, rh[n], hemi="right", view="lateral",
                       cmap="RdBu_r", vmin=-0.197, vmax=0.197, axes=axes[i, 1],
                       colorbar=False, bg_map=fs.sulc_right)
    axes[i, 1].set_title(f"{n} RH", fontsize=8)
fig.suptitle("TRIBE v2 predicted fMRI (real best.ckpt), TR-mean, fsaverage5 pial", fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/fig1_surface_means.png", dpi=80)
plt.close(fig)

# --- Fig 2: THREAT - FAIR vertex-wise contrast on surface ---
contrast = mean_maps["THREAT"] - mean_maps["FAIR"]
vmax = np.percentile(np.abs(contrast), 99)
fig, axes = plt.subplots(2, 2, subplot_kw={"projection": "3d"}, figsize=(9, 6))
plotting.plot_surf(fs.pial_left, contrast[:NL], hemi="left", view="lateral",
                   cmap="RdBu_r", vmin=-vmax, vmax=vmax, axes=axes[0, 0], bg_map=fs.sulc_left)
axes[0, 0].set_title("LH lateral", fontsize=8)
plotting.plot_surf(fs.pial_left, contrast[:NL], hemi="left", view="medial",
                   cmap="RdBu_r", vmin=-vmax, vmax=vmax, axes=axes[0, 1], bg_map=fs.sulc_left)
axes[0, 1].set_title("LH medial", fontsize=8)
plotting.plot_surf(fs.pial_right, contrast[NL:], hemi="right", view="lateral",
                   cmap="RdBu_r", vmin=-vmax, vmax=vmax, axes=axes[1, 0], bg_map=fs.sulc_right)
axes[1, 0].set_title("RH lateral", fontsize=8)
plotting.plot_surf(fs.pial_right, contrast[NL:], hemi="right", view="medial",
                   cmap="RdBu_r", vmin=-vmax, vmax=vmax, axes=axes[1, 1], bg_map=fs.sulc_right)
axes[1, 1].set_title("RH medial", fontsize=8)
fig.suptitle("THREAT minus FAIR predicted cortical contrast (real TRIBE v2 weights)", fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/fig2_contrast_threat_minus_fair.png", dpi=80)
plt.close(fig)

# --- Schaefer-400/Yeo-7 parcel mapping ---
sch = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7)
img = nibabel.load(sch.maps)
labels_txt = [l.decode() if isinstance(l, bytes) else str(l) for l in sch.labels]

def surf_labels(mesh):
    vals = surface.vol_to_surf(img, mesh, interpolation="nearest_most_frequent", radius=3.0)
    return np.round(vals).astype(int)

lab_l = surf_labels(fs.pial_left)
lab_r = surf_labels(fs.pial_right)
labels_all = np.concatenate([lab_l, lab_r])
print("unlabeled vertices:", int((labels_all == 0).sum()))

# parcel means of the THREAT-FAIR contrast
parcel_vals = {}
for p in range(1, 401):
    m = labels_all == p
    if m.sum() > 0:
        parcel_vals[p] = float(contrast[m].mean())
order = sorted(parcel_vals, key=lambda p: abs(parcel_vals[p]), reverse=True)[:20]
fig, ax = plt.subplots(figsize=(8, 6))
vals = [parcel_vals[p] for p in order][::-1]
labs = [labels_txt[p].replace("7Networks_", "") for p in order][::-1]
ax.barh(range(len(vals)), vals, color=["#b2182b" if v > 0 else "#2166ac" for v in vals])
ax.set_yticks(range(len(vals)))
ax.set_yticklabels(labs, fontsize=7)
ax.axvline(0, color="k", lw=0.5)
ax.set_xlabel("mean predicted-response contrast (a.u.)")
ax.set_title("THREAT - FAIR: top-20 Schaefer-400/Yeo-7 parcels by |contrast|\n"
             "(real TRIBE v2 predictions; atlas: nilearn fetch_atlas_schaefer_2018)", fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/fig3_parcel_bars_threat_minus_fair.png", dpi=90)
plt.close(fig)

# Yeo-7 network-level summary
net_names = ["Vis", "SomMot", "DorsAttn", "SalVentAttn", "Limbic", "Cont", "Default"]
net_contrast = {k: [] for k in net_names}
for p, v in parcel_vals.items():
    lab = labels_txt[p]
    for k in net_names:
        if f"_{k}_" in lab:
            net_contrast[k].append(v)
fig, ax = plt.subplots(figsize=(6, 4))
ms = [np.mean(net_contrast[k]) for k in net_names]
ss = [np.std(net_contrast[k]) / np.sqrt(len(net_contrast[k])) for k in net_names]
ax.bar(net_names, ms, yerr=ss, color="#7570b3")
ax.axhline(0, color="k", lw=0.5)
ax.set_ylabel("mean parcel contrast (a.u.)")
ax.set_title("THREAT - FAIR by Yeo-7 network (mean +/- SEM over parcels)", fontsize=9)
plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
fig.tight_layout()
fig.savefig(f"{OUT}/fig4_yeo7_network_contrast.png", dpi=90)
plt.close(fig)

# --- Fig 5: pairwise Pearson similarity matrix ---
S = np.ones((6, 6))
for i, a in enumerate(names):
    for j, b in enumerate(names):
        S[i, j] = np.corrcoef(mean_maps[a], mean_maps[b])[0, 1]
fig, ax = plt.subplots(figsize=(5.2, 4.2))
im = ax.imshow(S, cmap="viridis", vmin=-0.4, vmax=1)
ax.set_xticks(range(6)); ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
ax.set_yticks(range(6)); ax.set_yticklabels(names, fontsize=8)
for i in range(6):
    for j in range(6):
        ax.text(j, i, f"{S[i, j]:.2f}", ha="center", va="center",
                fontsize=7, color="w" if S[i, j] < 0.6 else "k")
fig.colorbar(im, label="Pearson r (TR-mean cortical patterns)")
ax.set_title("Separability: pairwise pattern correlations\n(real TRIBE v2, 6 reconstructed stimuli)", fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/fig5_similarity_matrix.png", dpi=90)
plt.close(fig)

# --- Fig 6: global field power timecourses ---
fig, ax = plt.subplots(figsize=(8, 4))
for n in names:
    gfp = preds[n].std(0)
    ax.plot(gfp, label=n, lw=1)
ax.set_xlabel("TR (model output, 100 pooled TRs)")
ax.set_ylabel("GFP = std across 20,484 vertices")
ax.legend(fontsize=7, ncol=2)
ax.set_title("Predicted global field power per stimulus (real TRIBE v2)", fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/fig6_gfp_timeseries.png", dpi=90)
plt.close(fig)

# save parcel table
with open(f"{OUT}/parcel_contrast_table.json", "w") as f:
    json.dump({labels_txt[p]: parcel_vals[p] for p in parcel_vals}, f, indent=1)
with open(f"{OUT}/yeo7_network_summary.json", "w") as f:
    json.dump({k: {"mean": float(np.mean(net_contrast[k])),
                   "n_parcels": len(net_contrast[k])} for k in net_names}, f, indent=1)
print("figs done")
