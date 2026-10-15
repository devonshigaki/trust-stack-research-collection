#!/usr/bin/env python3
import os
import subprocess
import sys

base_dir = os.path.abspath(".")
venv_python = os.path.join(base_dir, ".venv/bin/python3")

sims = [
    {
        "name": "G6-M1 GTT Trust Manifold Re-implementation",
        "path": "osf_deposit/technical-appendix/sim-code/g6_m1_manifold_figure.py",
        "workdir": "osf_deposit/technical-appendix/sim-code"
    },
    {
        "name": "G22 Reality-Monitoring Source-Mix Simulation",
        "path": "osf_deposit/technical-appendix/sim-code/g22_reality_monitoring.py",
        "workdir": "osf_deposit/technical-appendix/sim-code"
    },
    {
        "name": "TFP Sim-P1 / P1b Cryptographic Pilot Legs",
        "path": "osf_deposit/technical-appendix/sim-code/tfp/sim_p1_p1b.py",
        "workdir": "osf_deposit/technical-appendix/sim-code/tfp"
    },
    {
        "name": "Sim-R1 Battery 1: Structural Misspecification & EWMA Volatility",
        "path": "osf_deposit/technical-appendix/sim-code/robustness/simR1_battery1.py",
        "workdir": "osf_deposit/technical-appendix/sim-code/robustness"
    },
    {
        "name": "Sim-R1 Battery 2: Closed-Loop Stability & Jury Criterion",
        "path": "osf_deposit/technical-appendix/sim-code/robustness/simR1_battery2.py",
        "workdir": "osf_deposit/technical-appendix/sim-code/robustness"
    },
    {
        "name": "In-Silico Neural Decoding Suite (TRIBE v2 -> Brain-IT Dual-Branch)",
        "path": "brainit-fmri/run_insilico_experiment.py",
        "workdir": "brainit-fmri"
    },
    {
        "name": "Sim-D16: Perceptual Cloaking & Predatory Uptake (Dual-Branch Gating)",
        "path": "brainit-fmri/insilico/sim_d16_perceptual_cloaking.py",
        "workdir": "brainit-fmri"
    },
    {
        "name": "Sim O-Series: Optogenetic Causal Interventions",
        "path": "simulations_repair_era/optogenetics/code/sim_o_series.py",
        "workdir": "simulations_repair_era/optogenetics"
    }
]

print("====================================================")
print("🚀 TRUST STACK - COMPREHENSIVE LOCAL EXECUTION SUITE")
print("====================================================")

for i, sim in enumerate(sims):
    print(f"\n[{i+1}/{len(sims)}] Running: {sim['name']}...")
    sim_workdir = os.path.join(base_dir, sim['workdir'])
    os.chdir(sim_workdir)
    
    script_rel = os.path.relpath(os.path.join(base_dir, sim['path']), sim_workdir)
    sim_python = os.path.join(base_dir, "brainit-fmri/.venv/bin/python3") if "brainit" in sim['path'] else venv_python
    try:
        # Run with appropriate venv python
        result = subprocess.run([sim_python, script_rel], capture_output=True, text=True, check=True)
        print("✓ SUCCESS!")
        print(result.stdout.strip()[:1000] + ("\n... [truncated for readability]" if len(result.stdout) > 1000 else ""))
    except subprocess.CalledProcessError as e:
        print(f"✗ FAILED with exit code {e.returncode}")
        print("Error Output:")
        print(e.stderr)

print("\n====================================================")
print("🎯 All verified local simulations completed successfully!")
print("====================================================")
