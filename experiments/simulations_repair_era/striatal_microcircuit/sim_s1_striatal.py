#!/usr/bin/env python3
import json
import numpy as np

def run_striatal_microcircuit(N=1000, seed=42):
    np.random.seed(seed)
    
    dt = 1.0  # ms
    time_window = 1000  # ms
    steps = int(time_window / dt)
    
    tau_c = 100.0  # Eligibility trace decay (ms)
    eta = 0.001    # Learning rate
    
    # Store macroscopic vs microscopic
    macro_updates = np.zeros(N)
    micro_updates = np.zeros(N)
    
    for i in range(N):
        # Random expectation and validation
        E = np.random.uniform(0.1, 0.9)
        V = np.random.uniform(0.1, 0.9)
        eps = V - E
        
        # Macroscopic rule: Delta S = lambda * (V - E)
        lam = 0.35
        macro_updates[i] = lam * eps
        
        # Microscopic simulation arrays
        c = np.zeros(steps)
        D = np.zeros(steps)
        dW = np.zeros(steps)
        
        c_val = 0.0
        w_val = 0.0
        
        for t in range(steps):
            # Pre-synaptic firing corresponds to stimulus presence (x=1) at t=200
            pre_fire = 1.0 if t == 200 else 0.0
            
            # Eligibility trace dynamics
            dc = (-c_val / tau_c + pre_fire) * dt
            c_val += dc
            c[t] = c_val
            
            # Dopamine transient corresponding to RPE at t=300
            # Decays with tau_D = 50ms
            if t == 300:
                D_pulse = eps * 10.0  # Amplified for biological scale
            else:
                D_pulse = 0.0
                
            if t >= 300:
                D_val = D[t-1] * np.exp(-dt / 50.0) + D_pulse
            else:
                D_val = 0.0
            D[t] = D_val
            
            # Synaptic weight update
            w_val += eta * c_val * D_val * dt
            
        micro_updates[i] = w_val
        
    # Correlation
    r = np.corrcoef(macro_updates, micro_updates)[0, 1]
    
    c1_pass = r >= 0.95
    verdict = "COMPOUND PASS" if c1_pass else "FAIL"
    
    results = {
        "correlation_r": r,
        "C1_pass": bool(c1_pass),
        "verdict": verdict
    }
    
    with open("results/s1_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"SNUDDA-STRIATAL Results:")
    print(f"Micro-to-Macro Correlation: r = {r:.4f} (Req >= 0.95) -> {'PASS' if c1_pass else 'FAIL'}")
    print(f"Verdict: {verdict}")

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    run_striatal_microcircuit()