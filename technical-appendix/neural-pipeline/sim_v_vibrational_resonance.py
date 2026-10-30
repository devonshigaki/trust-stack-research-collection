#!/usr/bin/env python3
"""
Sim V-Series: Sub-Cellular 1D Vibrational Resonance & Acoustic Trust Fatigue
Implements the pre-registered protocol in SIM_V_PRE_REGISTRATION.md.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_sim_v(n_steps=1000, seed=42):
    rng = np.random.RandomState(seed)
    
    T_REALITY = 0.25 # Macro reality threshold
    CRITICAL_YIELD = 100.0 # Cumulative energy threshold for collapse
    
    # We test multiple frequencies
    frequencies = np.linspace(10, 200, 20)
    t_collapse = []
    
    # Store one trace for plotting (e.g., 100Hz)
    macro_s_trace = None
    vib_energy_trace = None
    
    for f in frequencies:
        dt = 0.001
        
        # 1D Harmonic Oscillator (Expectation binding)
        x = 0.0 # displacement
        v = 0.0 # velocity
        m = 1.0 # mass
        k = 50.0 # stiffness
        c = 2.0 # damping
        
        cumulative_energy = 0.0
        S_conscious = 0.80 # Start with high trust
        collapsed = False
        collapse_time = n_steps * dt
        
        s_hist = []
        e_hist = []
        
        for t_idx in range(n_steps):
            t = t_idx * dt
            # Sub-threshold high-frequency perturbation (micro-betrayal)
            # Amplitude is < T_REALITY/10
            amp = T_REALITY / 15.0
            force = amp * np.sin(2 * np.pi * f * t)
            
            # Physics update (Verlet/Euler)
            a = (force - k*x - c*v) / m
            v += a * dt
            x += v * dt
            
            # Energy accumulates (kinetic + potential)
            energy = 0.5 * m * v**2 + 0.5 * k * x**2
            cumulative_energy += energy * dt
            
            # Macroscopic perception (Low-pass filtered / Reality Threshold)
            # Because amplitude is small, conscious trust is unperturbed unless collapse happens
            if not collapsed:
                if np.abs(force) > T_REALITY:
                    S_conscious -= 0.1 # Should not happen here
                S_conscious = np.clip(S_conscious + rng.normal(0, 0.001), 0, 1)
            
            # Acoustic Fatigue Failure
            if cumulative_energy > CRITICAL_YIELD and not collapsed:
                collapsed = True
                S_conscious = 0.0 # Catastrophic phase transition
                collapse_time = t
                
            s_hist.append(S_conscious)
            e_hist.append(cumulative_energy)
            
        t_collapse.append(collapse_time)
        
        if int(f) == 100:
            macro_s_trace = s_hist
            vib_energy_trace = e_hist
            
    t_collapse = np.array(t_collapse)
    
    # --- C1: Sub-Threshold Invisibility ---
    # For f=100Hz, S_conscious remains > 0.75 for first 80% of time before collapse
    collapse_idx = np.argmin(np.array(macro_s_trace) > 0.0)
    if collapse_idx == 0: collapse_idx = n_steps # Didn't collapse
    # Check if drift <= 0.05 in the 80% window before collapse
    check_window = int(collapse_idx * 0.80)
    drift = np.max(macro_s_trace[:check_window]) - np.min(macro_s_trace[:check_window])
    c1_pass = drift <= 0.05
    
    # --- C2: Acoustic Trust Fatigue ---
    # Collapsed in >= 95% of high frequency trials (f > 50)
    high_f_mask = frequencies > 50
    collapse_rate = np.mean(t_collapse[high_f_mask] < (n_steps * 0.001))
    c2_pass = collapse_rate >= 0.95
    
    # --- C3: Logarithmic Resonance Signature ---
    # t_collapse scales with ln(f)
    mask = t_collapse < (n_steps * 0.001) # only those that collapsed
    if np.sum(mask) > 3:
        r_pearson = np.corrcoef(t_collapse[mask], np.log(frequencies[mask]))[0, 1]
    else:
        r_pearson = 0.0
    c3_pass = np.abs(r_pearson) >= 0.90 # Absolute correlation magnitude
    
    compound_pass = c1_pass and c2_pass and c3_pass
    
    results = {
        "experiment": "Sim V-Series: 1D Vibrational Resonance",
        "criteria": {
            "C1_sub_threshold_invisibility": {
                "drift": float(drift),
                "frozen_threshold": "<= 0.05",
                "verdict": "PASS" if c1_pass else "FAIL"
            },
            "C2_acoustic_fatigue": {
                "collapse_rate": float(collapse_rate),
                "frozen_threshold": ">= 0.95",
                "verdict": "PASS" if c2_pass else "FAIL"
            },
            "C3_logarithmic_resonance": {
                "r_pearson": float(r_pearson),
                "frozen_threshold": "|r| >= 0.90",
                "verdict": "PASS" if c3_pass else "FAIL"
            }
        },
        "compound_verdict": "PASS" if compound_pass else "FAIL",
        "data": {
            "frequencies": frequencies.tolist(),
            "t_collapse": t_collapse.tolist(),
            "macro_s_trace": macro_s_trace,
            "vib_energy_trace": vib_energy_trace
        }
    }
    return results

def plot_sim_v(results, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # C1 & C2 Trace
    t = np.arange(len(results["data"]["macro_s_trace"])) * 0.001
    axes[0].plot(t, results["data"]["macro_s_trace"], color="black", lw=2)
    axes[0].set_title("(a) Conscious Trust ($S_t$) Catastrophic Collapse")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Macroscopic Trust")
    
    # Energy accumulation
    axes[1].plot(t, results["data"]["vib_energy_trace"], color="orange", lw=2)
    axes[1].axhline(100.0, color="red", linestyle="--", label="Critical Yield")
    axes[1].set_title("(b) 1D Sub-Cellular Vibrational Energy")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Cumulative Allostatic Load")
    axes[1].legend()
    
    # C3
    f = np.array(results["data"]["frequencies"])
    tc = np.array(results["data"]["t_collapse"])
    axes[2].scatter(np.log(f), tc, color="purple")
    axes[2].set_title("(c) Logarithmic Resonance Signature")
    axes[2].set_xlabel("ln(Frequency of Micro-Betrayals)")
    axes[2].set_ylabel("Time to Failure ($t_{collapse}$)")
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    results = run_sim_v()
    base_dir = "/Users/devonshigaki/Desktop/research"
    results_path = os.path.join(base_dir, "experiments/brainit-fmri/results/sim_v_results.json")
    fig_path = os.path.join(base_dir, "figures/docas/pipeline/fig_sim_v_vibrational.png")
    
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
        
    plot_sim_v(results, fig_path)
    print("Sim V Complete. Verdict:", results["compound_verdict"])
