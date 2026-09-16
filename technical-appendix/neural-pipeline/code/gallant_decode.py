"""DOCAS N.3: Gallant-style encoding/decoding on the reconstructed battery27.

Semantic model: REAL Huth-lab English1000 985-dim word vectors
(english1000sm.hf5, OpenNeuro ds003020 derivatives, LeBel et al. 2023 — the
same matrix cited for Huth et al. 2016). NOT a substitute.

Brain data: TRIBE v2 predicted fMRI for the 27 reconstructed stimuli
(reconstruction-from-spec label applies), TR-mean maps [27 x 20484].

Protocol (manifest N.3): ridge encoding with leave-8-out folds (27 = 8+8+8+3,
fold assignment by seeded permutation); stimulus retrieval; Procrustes
alignment; category LOO decode; 2,000 permutations per null;
seed 20260905. Nulls are reported as nulls. The original headline (EN LOO
decode 0.40, p=0.032; retrieval/alignment nulls) is a reference target ONLY —
our stimuli are reconstructions, so identical numbers are neither expected nor
claimed.

Performance notes (documented, not hidden):
- Ridge alpha fixed at 1e3 (n=19 train / fold with 985 features; a RidgeCV
  grid over logspace(1,5,9) on the full data also selects alpha=1e3, reported
  in the output as ridgecv_alpha_full).
- Encoding permutation null re-fits via a precomputed per-fold ridge map with
  brain rows permuted (algebraically identical to re-fitting with permuted
  semantic rows at fixed alpha) and evaluates every 20th vertex (1025/20484).
- Procrustes alignment is computed in a 19-dimensional PCA space (train-fold
  PCA), because full-vertex orthogonal Procrustes is infeasible/ill-posed with
  27 samples x 20,484 vertices.

Outputs: results/gallant_decode_results.json
"""
import json
import re

import h5py
import numpy as np
from scipy.linalg import orthogonal_procrustes
from sklearn.decomposition import PCA
from sklearn.linear_model import RidgeCV

SEED = 20260905
NPERM = 2000
ALPHA = 1e3
BASE = "/tmp/tribe"

# ---------- load semantic model (robust to hf5 layout) ----------
f = h5py.File(f"{BASE}/english1000sm.hf5", "r")


def walk(g, prefix=""):
    out = []
    for k in g:
        item = g[k]
        name = f"{prefix}/{k}"
        if isinstance(item, h5py.Dataset):
            out.append((name, item.shape, item.dtype))
        else:
            out += walk(item, name)
    return out


layout = walk(f)
print("hf5 layout:", layout, flush=True)
names = {name: (shape, dtype) for name, shape, dtype in layout}
mat_key = next(n for n, (s, _) in names.items() if len(s) == 2 and 985 in s)
words_key = next(n for n, (s, d) in names.items()
                 if len(s) == 1 and d.kind in ("S", "O", "U"))
M = f[mat_key][()]
if M.shape[0] != 985:
    M = M.T
WORDS = [w.decode() if isinstance(w, bytes) else str(w) for w in f[words_key][()]]
assert M.shape == (985, len(WORDS)), (M.shape, len(WORDS))
vindex = {w.lower(): i for i, w in enumerate(WORDS)}
print(f"eng1000 loaded: {M.shape}, vocab={len(WORDS)}", flush=True)

# ---------- load brain preds + battery ----------
preds = np.load(f"{BASE}/results/battery27_preds.npz")
battery = json.load(open(f"{BASE}/battery27_reconstructed.json"))["stimuli"]
ids = [s["id"] for s in battery]
cats = np.array([s["category"] for s in battery])
B = np.stack([preds[i].mean(1) for i in ids]).astype(np.float64)  # [27, 20484]
n = len(ids)

# ---------- per-stimulus semantic vectors ----------
S = np.zeros((n, 985))
cov = []
for i, s in enumerate(battery):
    toks = [t.lower() for t in re.findall(r"[A-Za-z']+", s["text"])]
    vecs = [M[:, vindex[t]] for t in toks if t in vindex]
    S[i] = np.mean(vecs, axis=0)
    cov.append(len(vecs) / len(toks))
print(f"eng1000 coverage min={min(cov):.2f} max={max(cov):.2f}", flush=True)

# ---------- leave-8-out folds ----------
rng = np.random.default_rng(SEED)
perm = rng.permutation(n)
folds = [perm[0:8], perm[8:16], perm[16:24], perm[24:27]]
fold_tr = [np.setdiff1d(np.arange(n), fo) for fo in folds]

# ridgecv reference alpha on full data
rcv = RidgeCV(alphas=np.logspace(1, 5, 9)).fit(S, B[:, ::20])
alpha_full = float(rcv.alpha_)

# precompute per-fold ridge maps  W = (X'X + aI)^-1 X'  -> [985, n_tr]
pinvX = []
for tr in fold_tr:
    X = S[tr]
    A = X @ X.T + ALPHA * np.eye(len(tr))  # kernel trick: W = X' (XX'+aI)^-1
    pinvX.append(X.T @ np.linalg.inv(A))   # [985, n_tr]


def ridge_fit_predict(Sx_tr, Ytr, Sx_te):
    X = Sx_tr
    A = X @ X.T + ALPHA * np.eye(len(tr))
    W = X.T @ np.linalg.inv(A) @ Ytr
    return Sx_te @ W


def zcols(X):
    return (X - X.mean(0)) / (X.std(0) + 1e-12)


Bz = zcols(B)
Vsub = np.arange(0, B.shape[1], 20)

# ---------- 1. ridge encoding: semantic -> brain ----------
pred_brain = np.zeros_like(B)
for fo, tr, PX in zip(folds, fold_tr, pinvX):
    pred_brain[fo] = S[fo] @ (PX @ B[tr])
enc_vx = np.nan_to_num((zcols(pred_brain) * Bz).mean(0))  # per-vertex corr
enc_mean = float(enc_vx.mean())

null_enc = np.zeros(NPERM)
for p in range(NPERM):
    pp = rng.permutation(n)
    pb = np.zeros((n, len(Vsub)))
    for fo, tr, PX in zip(folds, fold_tr, pinvX):
        pb[fo] = S[fo] @ (PX @ B[pp][tr][:, Vsub])
    null_enc[p] = np.nan_to_num((zcols(pb) * Bz[:, Vsub]).mean(0)).mean()
    if p % 400 == 0:
        print(f"enc perm {p}", flush=True)
p_enc = float((np.sum(null_enc >= enc_mean) + 1) / (NPERM + 1))
print(f"encoding: r={enc_mean:.4f} p={p_enc:.4f}", flush=True)

# ---------- 2. stimulus retrieval ----------
pred_sem = np.zeros_like(S)
for fo, tr in zip(folds, fold_tr):
    X = B[tr]
    A = X @ X.T + ALPHA * np.eye(len(tr))
    pred_sem[fo] = B[fo] @ (X.T @ np.linalg.inv(A) @ S[tr])


def zrows(X):
    return (X - X.mean(1, keepdims=True)) / (X.std(1, keepdims=True) + 1e-12)


Sz = zrows(S)


def retrieval_top1(ps):
    sim = zrows(ps) @ Sz.T / S.shape[1]
    return float(np.mean(np.argmax(sim, 1) == np.arange(n)))


top1 = retrieval_top1(pred_sem)
null_ret = np.zeros(NPERM)
for p in range(NPERM):
    null_ret[p] = retrieval_top1(pred_sem[rng.permutation(n)])
p_ret = float((np.sum(null_ret >= top1) + 1) / (NPERM + 1))
print(f"retrieval: top1={top1:.3f} p={p_ret:.4f}", flush=True)

# ---------- 3. Procrustes alignment in PCA space ----------
K = 18


def proc_aligned_corr(pred, act, tr, te):
    pca = PCA(n_components=K).fit(act[tr])
    Pa = pca.transform(pred[tr])
    Aa = pca.transform(act[tr])
    R, _ = orthogonal_procrustes(Pa, Aa)
    Pe = pca.transform(pred[te]) @ R
    Ae = pca.transform(act[te])
    return float(np.nanmean([np.corrcoef(Pe[i], Ae[i])[0, 1]
                             for i in range(len(te))]))


proc = float(np.mean([proc_aligned_corr(pred_brain, B, tr, fo)
                      for fo, tr in zip(folds, fold_tr)]))
null_proc = np.zeros(NPERM)
for p in range(NPERM):
    pp = rng.permutation(n)
    null_proc[p] = float(np.mean([
        proc_aligned_corr(pred_brain[pp], B, tr, fo)
        for fo, tr in zip(folds, fold_tr)]))
p_proc = float((np.sum(null_proc >= proc) + 1) / (NPERM + 1))
print(f"procrustes: r={proc:.4f} p={p_proc:.4f}", flush=True)

# ---------- 4. category LOO decode (nearest centroid, correlation) ----------
def loo_correct(X, labels):
    correct = np.zeros(len(X), dtype=bool)
    Xz = zrows(X)
    for i in range(len(X)):
        tr = np.setdiff1d(np.arange(len(X)), [i])
        cents = {c: zrows(X[tr][labels[tr] == c].mean(0, keepdims=True))[0]
                 for c in np.unique(labels)}
        sims = {c: float(Xz[i] @ ce) for c, ce in cents.items()}
        correct[i] = max(sims, key=sims.get) == labels[i]
    return correct


corr_items = loo_correct(B, cats)
acc = float(corr_items.mean())
per_cat = {c: float(corr_items[cats == c].mean()) for c in np.unique(cats)}
acc_sem = float(loo_correct(S, cats).mean())

null_acc = np.zeros(NPERM)
for p in range(NPERM):
    null_acc[p] = loo_correct(B, rng.permutation(cats)).mean()
    if p % 400 == 0:
        print(f"loo perm {p}", flush=True)
p_loo = float((np.sum(null_acc >= acc) + 1) / (NPERM + 1))
print(f"LOO decode: acc={acc:.3f} p={p_loo:.4f}", flush=True)

res = {
    "_provenance": ("reconstruction-from-spec battery (battery27_reconstructed.json); "
                    "REAL eng1000 985-dim semantic model (OpenNeuro ds003020 "
                    "derivatives, LeBel et al. 2023); do NOT compare numerically "
                    "to paper headlines"),
    "seed": SEED, "n_permutations": NPERM, "ridge_alpha": ALPHA,
    "ridgecv_alpha_full": alpha_full,
    "n_stimuli": n, "folds": [sorted(map(int, f_)) for f_ in folds],
    "eng1000_word_coverage": {"min": float(min(cov)), "max": float(max(cov)),
                              "mean": float(np.mean(cov))},
    "encoding": {"mean_vertex_corr": enc_mean, "p_perm": p_enc,
                 "null_mean": float(null_enc.mean()), "null_std": float(null_enc.std()),
                 "verdict": "PASS" if p_enc < 0.05 else "NULL"},
    "retrieval": {"top1": top1, "p_perm": p_ret, "chance_top1": 1.0 / n,
                  "null_mean": float(null_ret.mean()), "null_std": float(null_ret.std()),
                  "verdict": "PASS" if p_ret < 0.05 else "NULL"},
    "procrustes": {"aligned_corr_pca18": proc, "p_perm": p_proc,
                   "null_mean": float(null_proc.mean()),
                   "null_std": float(null_proc.std()),
                   "verdict": "PASS" if p_proc < 0.05 else "NULL"},
    "category_loo_decode": {"accuracy": acc, "p_perm": p_loo,
                            "null_mean": float(null_acc.mean()),
                            "null_std": float(null_acc.std()),
                            "null_ci95": [float(np.percentile(null_acc, 2.5)),
                                          float(np.percentile(null_acc, 97.5))],
                            "chance": float(1 / len(np.unique(cats))),
                            "per_category": per_cat,
                            "semantic_only_accuracy": acc_sem,
                            "verdict": "PASS" if p_loo < 0.05 else "NULL"},
    "_reference_only_original_headline": ("EN LOO decode 0.40 p=0.032; retrieval and "
                                          "alignment NULLS (do not claim)"),
}
json.dump(res, open(f"{BASE}/results/gallant_decode_results.json", "w"), indent=1)
print("WROTE results/gallant_decode_results.json")
