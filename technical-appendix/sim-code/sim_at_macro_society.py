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

def run_sim_at_macro(seed=42):
    rng = np.random.default_rng(seed)
    timesteps = 5000
    N_agents = 20 # Alphabet size 20 (A-T)
    alphabet = [chr(65 + i) for i in range(N_agents)]
    
    # Null Regime: Random Economy (High Entropy)
    null_seq = "".join(rng.choice(alphabet, size=timesteps))
    
    # GTT Regime: Trust-Bound Economy (Origin of Wealth)
    gtt_seq = ""
    lam = 0.5
    
    # Active contracts between agent i and agent j -> trust state S_ij
    # S_ij > 0 means the bond exists and they trade (which gets logged)
    trust_matrix = np.full((N_agents, N_agents), 0.5) 
    
    # Exogenous market shock cycle
    market_cycle = [1.0, 0.5, -0.2, 0.8, 1.2]
    
    for t in range(timesteps):
        # Pick a random candidate trading pair
        i, j = rng.choice(N_agents, size=2, replace=False)
        
        # Environmental validation (market conditions for this trade)
        V_t = market_cycle[t % 5] + rng.normal(0, 0.2)
        E_t = 0.5 # Expectation of standard return
        
        # GTT Update
        eps = V_t - E_t
        trust_matrix[i, j] += lam * eps
        
        # Selection filter: if trust is positive, trade executes (bond holds)
        if trust_matrix[i, j] > 0:
            # We log the participating agents as a sequence
            gtt_seq += alphabet[i] + alphabet[j]
        else:
            # Bankrupt / Defect: bond breaks, reset baseline for future
            trust_matrix[i, j] = 0.5
            
    # Subsample to keep computation time reasonable if seq is long
    if len(gtt_seq) > 5000:
        gtt_seq = gtt_seq[:5000]
        
    # Calculate Assembly Index proxies
    asi_null = repair_compress(null_seq)
    asi_gtt = repair_compress(gtt_seq)
    
    lzw_null = lzw_compress(null_seq)
    lzw_gtt = lzw_compress(gtt_seq)
    
    # Evaluate Hypotheses
    
    # AT-MAC-1: Institutional Complexity Generation
    asi_ratio = asi_gtt / max(asi_null, 1)
    atmac1_pass = asi_ratio >= 2.0
    
    # AT-MAC-2: Algorithmic Divergence (Order vs Noise)
    atmac2_pass = asi_gtt < 0.5 * lzw_gtt
    
    # AT-MAC-3: Institutional Phase Transition
    atmac3_pass = asi_gtt > 15
    
    compound_pass = atmac1_pass and atmac2_pass and atmac3_pass
    verdict = "COMPOUND PASS (3/3)" if compound_pass else "FAIL as frozen"
    
    # Output and plotting
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures", exist_ok=True)
    os.makedirs("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers", exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    labels = ['Random Economy (Null)', 'GTT Economy (Origin of Wealth)']
    asi_vals = [asi_null, asi_gtt]
    lzw_vals = [lzw_null, lzw_gtt]
    
    x = np.arange(len(labels))
    width = 0.35
    
    axes[0].bar(x - width/2, asi_vals, width, label='Assembly Index (Re-Pair)')
    axes[0].bar(x + width/2, lzw_vals, width, label='Kolmogorov Complexity (LZW)')
    axes[0].set_ylabel('Index / Dictionary Size')
    axes[0].set_title('Macro-Assembly: Order from Chaos')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].legend()
    
    # Plot divergence ratio
    div_null = asi_null / lzw_null
    div_gtt = asi_gtt / lzw_gtt
    axes[1].bar(labels, [div_null, div_gtt], color=['gray', 'purple'])
    axes[1].set_title('Assembly-to-Kolmogorov Ratio ($ASI / LZW$)')
    axes[1].set_ylabel('Ratio (Lower = More Ordered Structure)')
    axes[1].axhline(0.5, color='r', linestyle='--', label='AT-MAC-2 Threshold')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig("/Users/devonshigaki/Developer/trust-stack-research-collection/papers/source/figures/fig_sim_at_macro.png", dpi=300)
    
    out = {
        "timestamp": "2026-11-01",
        "seed": seed,
        "compound_verdict": verdict,
        "atmac1_complexity": {
            "asi_gtt": asi_gtt,
            "asi_null": asi_null,
            "ratio": asi_ratio,
            "pass": bool(atmac1_pass)
        },
        "atmac2_divergence": {
            "asi_gtt": asi_gtt,
            "lzw_gtt": lzw_gtt,
            "ratio": float(div_gtt),
            "pass": bool(atmac2_pass)
        },
        "atmac3_transition": {
            "asi_gtt": asi_gtt,
            "threshold": 15,
            "pass": bool(atmac3_pass)
        }
    }
    
    with open("/Users/devonshigaki/Developer/trust-stack-research-collection/technical-appendix/numbers/sim_at_macro_results.json", "w") as f:
        json.dump(out, f, indent=2)
        
    print(f"AT-MAC-1 Complexity Ratio: {asi_ratio:.2f} (>= 2.0) -> {atmac1_pass}")
    print(f"AT-MAC-2 Divergence Ratio (ASI/LZW): {div_gtt:.2f} (< 0.5) -> {atmac2_pass}")
    print(f"AT-MAC-3 Phase Transition: ASI = {asi_gtt} (> 15) -> {atmac3_pass}")
    print(f"Verdict: {verdict}")

if __name__ == "__main__":
    run_sim_at_macro()
