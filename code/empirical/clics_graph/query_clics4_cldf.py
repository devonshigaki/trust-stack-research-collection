#!/usr/bin/env python3
"""CLICS 4.0 Empirical Colexification Graph Verification
Verifies the cross-linguistic concept graph structure, family filtering (Family_Count >= 3),
and runs Monte Carlo permutation tests on channel-concept sets (DOCAS §4.6 & Table 3).
"""

import os
import sys
import csv
import json
import numpy as np
import networkx as nx

csv.field_size_limit(10_000_000)

def verify_clics():
    print("=" * 65)
    print("EMPIRICAL VERIFICATION: CLICS 4.0 CROSS-LINGUISTIC GRAPH")
    print("=" * 65)

    csv_path = os.path.join(os.path.dirname(__file__), "colexifications.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    print(f"Loading CLICS 4.0 colexifications from: {csv_path}...")
    
    G_unfiltered = nx.Graph()
    G_fam3 = nx.Graph()

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row.get("Source_Concept")
            v = row.get("Target_Concept")
            if not u or not v or u == v:
                continue
            
            fam_cnt = int(row.get("Family_Count", 1))
            weight = int(row.get("Language_Count", 1))
            
            G_unfiltered.add_edge(u, v, weight=weight, family_count=fam_cnt)
            if fam_cnt >= 3:
                G_fam3.add_edge(u, v, weight=weight, family_count=fam_cnt)

    n_nodes_raw = G_unfiltered.number_of_nodes()
    n_edges_raw = G_unfiltered.number_of_edges()
    n_nodes_f3 = G_fam3.number_of_nodes()
    n_edges_f3 = G_fam3.number_of_edges()

    print(f"\nUnfiltered Graph: {n_nodes_raw:,} concepts, {n_edges_raw:,} colexification edges")
    print(f"Family>=3 Filtered: {n_nodes_f3:,} concepts, {n_edges_f3:,} colexification edges")

    # Background densities
    bg_unfiltered = n_edges_raw / (n_nodes_raw * (n_nodes_raw - 1) / 2)
    bg_fam3 = n_edges_f3 / (n_nodes_f3 * (n_nodes_f3 - 1) / 2) if n_nodes_f3 > 1 else 0

    print(f"Background Density (Unfiltered): {bg_unfiltered:.4f}")
    print(f"Background Density (Family>=3):   {bg_fam3:.4f}")

    # DOCAS Core Channel Concept Sets
    channels = {
        "Recognition (C)": ["KNOW", "UNDERSTAND", "SEE", "HEAR", "LEARN", "FIND", "SEEM"],
        "Validation (O)": ["TRUE", "TRUTH", "BELIEVE", "ANSWER", "RIGHT", "CORRECT"],
        "Expectation (D)": ["HOPE", "WANT", "WAIT (FOR)"],
        "Stabilization (S)": ["REST", "SLEEP", "CALM", "PEACE", "QUIET", "STABLE"]
    }

    results = {}
    np.random.seed(42)
    n_perms = 2000
    all_nodes_f3 = list(G_fam3.nodes())
    node_degrees = np.array([G_fam3.degree(u) for u in all_nodes_f3])
    decile_edges = np.quantile(node_degrees, np.linspace(0.0, 1.0, 11))
    node_bins = np.clip(np.digitize(node_degrees, decile_edges[1:-1]), 0, 9)
    bin_to_nodes = {b: [all_nodes_f3[i] for i in range(len(all_nodes_f3)) if node_bins[i] == b] for b in range(10)}
    node_to_bin = {all_nodes_f3[i]: int(node_bins[i]) for i in range(len(all_nodes_f3))}

    print("\n--- Within-Channel Density & 2,000-Permutation Tests (Uniform + Degree-Stratified, Family>=3) ---")

    for ch_name, concepts in channels.items():
        present_nodes = [c for c in concepts if c in G_fam3]
        k = len(present_nodes)
        if k < 2:
            print(f"{ch_name}: Insufficient concepts present ({k}/{len(concepts)})")
            continue

        sub = G_fam3.subgraph(present_nodes)
        actual_edges = sub.number_of_edges()
        max_edges = k * (k - 1) // 2
        actual_density = actual_edges / max_edges if max_edges > 0 else 0

        # 1. Uniform permutation null
        perm_counts = []
        # 2. Degree-stratified permutation null (controls for hub-degree confounding)
        target_bins = [node_to_bin[c] for c in present_nodes]
        deg_perm_counts = []
        for _ in range(n_perms):
            sample = np.random.choice(all_nodes_f3, size=k, replace=False)
            perm_counts.append(G_fam3.subgraph(sample).number_of_edges())
            deg_sample = []
            for b in target_bins:
                pool = [u for u in bin_to_nodes[b] if u not in deg_sample]
                if not pool:
                    pool = [u for u in all_nodes_f3 if u not in deg_sample]
                deg_sample.append(np.random.choice(pool))
            deg_perm_counts.append(G_fam3.subgraph(deg_sample).number_of_edges())

        perm_counts = np.array(perm_counts)
        deg_perm_counts = np.array(deg_perm_counts)
        p_val = (np.sum(perm_counts >= actual_edges) + 1.0) / (n_perms + 1.0)
        p_deg = (np.sum(deg_perm_counts >= actual_edges) + 1.0) / (n_perms + 1.0)

        results[ch_name] = {
            "concepts_tested": present_nodes,
            "present_count": k,
            "actual_edges": int(actual_edges),
            "max_possible_edges": int(max_edges),
            "density": float(actual_density),
            "fold_enrichment": float(actual_density / bg_fam3) if bg_fam3 > 0 else 0,
            "permutation_p": float(p_val),
            "degree_stratified_p": float(p_deg),
            "status": "PASS (p <= 0.05)" if p_val <= 0.05 else "NULL"
        }

        print(f"[{results[ch_name]['status']}] {ch_name}:")
        print(f"  Concepts: {present_nodes}")
        print(f"  Edges: {actual_edges}/{max_edges} | Density: {actual_density:.3f} ({results[ch_name]['fold_enrichment']:.1f}x bg)")
        print(f"  Uniform p: {p_val:.4f} | Degree-Stratified p: {p_deg:.4f}\n")

    out_json = os.path.join(os.path.dirname(__file__), "clics_permutation_verified.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to: {out_json}")

    # Confirm key empirical landmarks:
    # 1. Recognition is statistically significant (p < 0.01)
    assert results["Recognition (C)"]["permutation_p"] < 0.01, "FAIL: Recognition channel not significant!"
    # 2. Validation is statistically significant (p < 0.01)
    assert results["Validation (O)"]["permutation_p"] < 0.01, "FAIL: Validation channel not significant!"
    # 3. Stabilization is confirmed as a null (p > 0.05) under Family>=3 as reported in Table 3
    assert results["Stabilization (S)"]["status"] == "NULL", "FAIL: Stabilization channel null was not confirmed!"
    print("✓ ALL CLICS 4.0 CROSS-LINGUISTIC LANDMARKS VERIFIED (PASS)!")

if __name__ == "__main__":
    verify_clics()
