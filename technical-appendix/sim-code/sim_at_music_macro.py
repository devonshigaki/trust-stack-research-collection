#!/usr/bin/env python3
import os
import json
import numpy as np
import matplotlib.pyplot as plt

def lzw_compress(uncompressed):
    """Lempel-Ziv-Welch (LZW) dictionary compression baseline."""
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return dict_size

def repair_compress(sequence):
    """
    Simplified Re-Pair (Recursive Pairing) algorithm to approximate 
    the Assembly Index (ASI) of a 1D string.
    Finds the most frequent digram and replaces it with a new non-terminal.
    Returns the number of joining rules (ASI proxy).
    """
    seq = list(sequence)
    rules = 0
    next_symbol_id = 256
    
    while len(seq) > 1:
        # Count digram frequencies
        digrams = {}
        for i in range(len(seq) - 1):
            pair = (seq[i], seq[i+1])
            digrams[pair] = digrams.get(pair, 0) + 1
            
        # Find most frequent digram
        best_pair = None
        max_count = 0
        for pair, count in digrams.items():
            if count > max_count:
                max_count = count
                best_pair = pair
                
        # If no digram repeats, we are done
        if max_count < 2:
            break
            
        # Create new rule and replace
        rules += 1
        new_seq = []
        i = 0
        while i < len(seq):
            if i < len(seq) - 1 and (seq[i], seq[i+1]) == best_pair:
                new_seq.append(chr(next_symbol_id))
                i += 2
            else:
                new_seq.append(seq[i])
                i += 1
        
        seq = new_seq
        next_symbol_id += 1
        
    return rules

def run_sim_at_music(seed=42):
    rng = np.random.default_rng(seed)
    timesteps = 5000
    
    alphabet = [chr(i) for i in range(65, 65+12)] # A-L representing 12 pitch classes
    
    # 1. Null Regime: Random String
    null_seq = "".join(rng.choice(alphabet, size=timesteps))
    
    # 2. GTT Regime: Causal Memory Maker
    # A motif survives if the rhythmic expectation (E) matches environmental validation (V)
    # Delta S = lambda * (V - E)
    gtt_seq = ""
    lam = 0.5
    S_t = 0.5
    current_motif = ""
    
    # We create a periodic target metric structure
    metric_target = [1.0, 0.5, 0.8, 0.5] # Strong downbeat, weak upbeat, etc.
    
    for t in range(timesteps):
        # Generate candidate note
        note = rng.choice(alphabet)
        current_motif += note
        
        # Environmental validation
        V_t = metric_target[t % 4] + rng.normal(0, 0.1)
        # Internal expectation
        E_t = 0.75 
        
        eps = V_t - E_t
        S_t += lam * eps
        
        # Selection filter
        if S_t > 0:
            # Bond survives, append to macro structure
            if len(current_motif) >= 4:
                # When a full motif successfully forms, it is locked into memory
                gtt_seq += current_motif
                current_motif = "" # Reset for next motif
                S_t = 0.5 # Reset baseline trust for new motif
        else:
            # Bond shatters under noise (Amnesia)
            current_motif = "" 
            S_t = 0.5
            
    # Calculate Assembly Index proxies
    asi_null = repair_compress(null_seq)
    asi_gtt = repair_compress(gtt_seq)
    
    lzw_null = lzw_compress(null_seq)
    lzw_gtt = lzw_compress(gtt_seq)
    
    # Evaluate Hypotheses
    
    # AT-M1: Macro-Complexity Acceleration
    asi_ratio = asi_gtt / max(asi_null, 1)
    atm1_pass = asi_ratio >= 3.0
    
    # AT-M2: Selection Phase Transition
    atm2_pass = asi_gtt > 15
    
    # AT-M3: Algorithmic Divergence (Hierarchical motifs vs pure noise)
    atm3_pass = asi_gtt < lzw_gtt
    
    compound_pass = atm1_pass and atm2_pass and atm3_pass
    verdict = "COMPOUND PASS (3/3)" if compound_pass else "FAIL as frozen"
    
    # Output and plotting
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures", exist_ok=True)
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers", exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    labels = ['Null (Random)', 'GTT (Causal Memory)']
    asi_vals = [asi_null, asi_gtt]
    lzw_vals = [lzw_null, lzw_gtt]
    
    x = np.arange(len(labels))
    width = 0.35
    
    axes[0].bar(x - width/2, asi_vals, width, label='Assembly Index (Re-Pair)')
    axes[0].bar(x + width/2, lzw_vals, width, label='Algorithmic LZW Dict Size')
    axes[0].set_ylabel('Index / Dictionary Size')
    axes[0].set_title('Macro-Assembly vs Kolmogorov Complexity')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].legend()
    
    # Plot the difference showing divergence
    diffs = [lzw_null - asi_null, lzw_gtt - asi_gtt]
    axes[1].bar(labels, diffs, color=['gray', 'purple'])
    axes[1].set_title('Algorithmic Divergence (LZW - ASI)')
    axes[1].set_ylabel('Divergence Magnitude')
    
    plt.tight_layout()
    plt.savefig("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures/fig_sim_at_music_macro.png", dpi=300)
    
    out = {
        "timestamp": "2026-11-01",
        "seed": seed,
        "compound_verdict": verdict,
        "atm1_macro_complexity": {
            "asi_gtt": asi_gtt,
            "asi_null": asi_null,
            "ratio": asi_ratio,
            "pass": bool(atm1_pass)
        },
        "atm2_phase_transition": {
            "asi_gtt": asi_gtt,
            "threshold": 15,
            "pass": bool(atm2_pass)
        },
        "atm3_divergence": {
            "asi_gtt": asi_gtt,
            "lzw_gtt": lzw_gtt,
            "pass": bool(atm3_pass)
        }
    }
    
    with open("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers/sim_at_music_results.json", "w") as f:
        json.dump(out, f, indent=2)
        
    print(f"AT-M1 Complexity Ratio: {asi_ratio:.2f} (>= 3.0) -> {atm1_pass}")
    print(f"AT-M2 Phase Transition: ASI = {asi_gtt} (> 15) -> {atm2_pass}")
    print(f"AT-M3 Algorithmic Divergence: ASI {asi_gtt} < LZW {lzw_gtt} -> {atm3_pass}")
    print(f"Verdict: {verdict}")

if __name__ == "__main__":
    run_sim_at_music()
