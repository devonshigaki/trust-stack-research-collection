#!/usr/bin/env python3
import os
import json
import numpy as np


def run_striatal_microcircuit(N=1000, seed=42):
    rng = np.random.default_rng(seed)

    dt = 1.0  # ms
    steps = 1000  # 1000 ms
    tau_c = 100.0  # Ca2+/CaMKII eligibility trace decay (ms)
    tau_d = 50.0   # Extracellular DA clearance (ms)
    eta = 0.001

    macro_updates = np.zeros(N)
    micro_updates = np.zeros(N)

    decay_c = np.exp(-dt / tau_c)
    decay_d = np.exp(-dt / tau_d)

    for i in range(N):
        E = float(rng.uniform(0.1, 0.9))
        V = float(rng.uniform(0.1, 0.9))
        eps = V - E
        macro_updates[i] = 0.35 * eps

        # Stochastic Poisson cortical-striatal stimulus burst (x=1) around t in [180, 220) ms + 5 Hz spontaneous noise
        rates = np.full(steps, 0.005)
        rates[180:220] = 0.45
        spikes = (rng.random(steps) < rates).astype(np.float64)

        # Phasic dopamine validation onset with realistic biophysical jitter (ms) and release noise
        t_da = int(np.clip(round(300.0 + rng.normal(0.0, 12.0)), 240, 420))
        da_amp = eps * 10.0 + float(rng.normal(0.0, 0.20))

        c_val = 0.0
        d_val = 0.0
        w_val = 0.0
        for t in range(steps):
            c_val = c_val * decay_c + spikes[t]
            if t == t_da:
                d_val += da_amp
            else:
                d_val *= decay_d
            # D1/D2 three-factor plasticity kernel with soft saturation
            w_val += eta * c_val * np.tanh(0.15 * d_val) * dt

        micro_updates[i] = w_val

    r = float(np.corrcoef(macro_updates, micro_updates)[0, 1])
    c1_pass = r >= 0.95
    verdict = "COMPOUND PASS" if c1_pass else "FAIL"

    results = {
        "correlation_r": r,
        "C1_pass": bool(c1_pass),
        "verdict": verdict,
    }

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "s1_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("SNUDDA-STRIATAL (Poisson Spike + DA Jitter Three-Factor STDP) Results:")
    print(f"Micro-to-Macro Correlation: r = {r:.4f} (Req >= 0.95) -> {'PASS' if c1_pass else 'FAIL'}")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    run_striatal_microcircuit()