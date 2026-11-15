#!/usr/bin/env python3
"""
Deterministic Empirical Connectomics Readout Verifier (FlyWire F1a2/F1b + MICrONS H1a)
Re-computes frozen pre-registered verdicts directly from raw CSV and NPZ synapse artifacts
without calling external container paths.
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import scipy.stats as stats

FLY_DIR = os.path.dirname(os.path.abspath(__file__))
MIC_DIR = os.path.abspath(os.path.join(FLY_DIR, "../connectomics_microns"))


def main():
    print("=" * 75)
    print("EMPIRICAL CONNECTOMICS READOUT VERIFICATION (FLYWIRE F1 & MICRONS H1)")
    print("=" * 75)

    # 1. FlyWire F1b (Mushroom body compartment-resolved acquisition, 7/7 PASS)
    df_b1 = pd.read_csv(os.path.join(FLY_DIR, "f1b_probe_readouts_set1.csv"))
    df_b2 = pd.read_csv(os.path.join(FLY_DIR, "f1b_probe_readouts_set2.csv"))
    df_b = pd.concat([df_b1, df_b2], ignore_index=True)

    intact_acq = df_b[(df_b["arm"] == "intact_av") & (df_b["phase"] == "acq")]
    mean_curve = intact_acq.groupby("after_trial")["R_cond"].mean()
    rho_av = float(stats.spearmanr(mean_curve.index, mean_curve.values).statistic)
    r_cond_final = float(mean_curve.loc[8])
    r_noncond_final = float(intact_acq[intact_acq["after_trial"] == 8]["R_noncond"].mean())
    d_abl_final = float(df_b[(df_b["arm"] == "D_abl") & (df_b["phase"] == "acq") & (df_b["after_trial"] == 8)]["R_cond"].mean())
    gshuf_av = float(df_b[(df_b["arm"] == "gateshuf_av") & (df_b["phase"] == "acq") & (df_b["after_trial"] == 8)]["R_cond"].mean())

    print(f"FlyWire F1b intact_av:  rho={rho_av:.3f}, R_cond={r_cond_final:.3f} (<=0.70), R_noncond={r_noncond_final:.3f} (>0.95)")
    print(f"FlyWire F1b controls:   D_abl={d_abl_final:.3f} (>0.95), gateshuf_av={gshuf_av:.3f} (>0.95)")
    assert rho_av <= -0.80 and r_cond_final <= 0.70
    assert r_noncond_final > 0.95 and d_abl_final > 0.95 and gshuf_av > 0.95

    # 2. FlyWire F1a2 (Whole-brain partner-permutation failure reported honestly)
    df_a = pd.concat([
        pd.read_csv(os.path.join(FLY_DIR, "f1a2_probe_readouts_set1.csv")),
        pd.read_csv(os.path.join(FLY_DIR, "f1a2_probe_readouts_set2.csv")),
        pd.read_csv(os.path.join(FLY_DIR, "f1a2_probe_readouts_shufflev2.csv")),
    ], ignore_index=True)
    shuf_pos = float(df_a[(df_a["arm"] == "shuffle") & (df_a["phase"] == "acq") & (df_a["after_trial"] == 8)]["R"].mean())
    shuf_cls = float(df_a[(df_a["arm"] == "shuffle_v2") & (df_a["phase"] == "acq") & (df_a["after_trial"] == 8)]["R"].mean())
    print(f"FlyWire F1a2 controls:  shuffle_pos={shuf_pos:.3f}, shuffle_classfaithful={shuf_cls:.3f} (FAIL <0.95 as reported)")
    assert shuf_pos < 0.95 and shuf_cls < 0.95

    # 3. MICrONS H1a (722,253 synapses onto 8,256 typed neuronal posts -> median class dominance < 0.50 FAIL)
    g = np.load(os.path.join(MIC_DIR, "graph_h1b_microns.npz"))
    w, cq, cp = g["w"], g["cls_post"], g["cls_pre"]
    classes = np.unique(cq)
    dom_vals = []
    for c_post in classes:
        mask_post = (cq == c_post)
        tot_post = float(w[mask_post].sum())
        max_share = max(float(w[mask_post & (cp == c_pre)].sum()) / tot_post for c_pre in classes)
        dom_vals.append(max_share)
    med_dom = float(np.median(dom_vals))
    print(f"MICrONS H1a (722k pairs): median single-class dominance={med_dom:.3f} (FAIL <0.50 as reported)")
    assert abs(med_dom - 0.313) < 0.02 and med_dom < 0.50

    print("\n✓ ALL FLYWIRE F1a2/F1b & MICRONS H1a EMPIRICAL READOUTS VERIFIED (PASS)!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
