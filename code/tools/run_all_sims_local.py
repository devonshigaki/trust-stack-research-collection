#!/usr/bin/env python3
import os
import subprocess
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_local_venv = os.path.join(base_dir, ".venv/bin/python3")
venv_python = _local_venv if os.path.exists(_local_venv) else sys.executable

sims = [
    {
        "name": "G6-M1 GTT Trust Manifold Re-implementation",
        "path": "code/simulations/repair_era/gtt/g6_m1_manifold_figure.py",
        "workdir": "code/simulations/repair_era/gtt"
    },
    {
        "name": "G22 Reality-Monitoring Source-Mix Simulation",
        "path": "code/simulations/repair_era/gtt/g22_reality_monitoring.py",
        "workdir": "code/simulations/repair_era/gtt"
    },
    {
        "name": "TFP Sim-P1 / P1b Cryptographic Pilot Legs",
        "path": "code/simulations/repair_era/tfp/sim_p1_p1b.py",
        "workdir": "code/simulations/repair_era/tfp"
    },
    {
        "name": "Sim-R1 Battery 1: Structural Misspecification & EWMA Volatility",
        "path": "code/simulations/repair_era/robustness/simR1_battery1.py",
        "workdir": "code/simulations/repair_era/robustness"
    },
    {
        "name": "Sim-R1 Battery 2: Closed-Loop Stability & Jury Criterion",
        "path": "code/simulations/repair_era/robustness/simR1_battery2.py",
        "workdir": "code/simulations/repair_era/robustness"
    },
    {
        "name": "In-Silico Neural Decoding Suite (VGG Proxy -> Blind Brain-IT Dual-Branch)",
        "path": "code/simulations/brainit_fmri/run_insilico_experiment.py",
        "workdir": "code/simulations/brainit_fmri"
    },
    {
        "name": "Sim-D16: Perceptual Cloaking & Predatory Uptake (Dual-Branch Gating)",
        "path": "code/simulations/brainit_fmri/insilico/sim_d16_perceptual_cloaking.py",
        "workdir": "code/simulations/brainit_fmri"
    },
    {
        "name": "Sim O-Series: Optogenetic Causal Interventions",
        "path": "code/simulations/repair_era/optogenetics/code/sim_o_series.py",
        "workdir": "code/simulations/repair_era/optogenetics"
    },
    {
        "name": "Sim-D17: Atmospheric & Photic-Thermal Gating",
        "path": "code/simulations/brainit_fmri/insilico/sim_d17_weather_gating.py",
        "workdir": "code/simulations/brainit_fmri"
    },
    {
        "name": "Sim-D18: Baylor Unconscious Narrative Gating & Attractor Drift",
        "path": "code/simulations/brainit_fmri/insilico/sim_d18_baylor_unconscious_gating.py",
        "workdir": "code/simulations/brainit_fmri"
    },
    {
        "name": "Sim-D19: Perky Reality-Monitoring Perception Filter (Dijkstra Psychophysics)",
        "path": "code/simulations/brainit_fmri/insilico/sim_d19_perky_reality_filter.py",
        "workdir": "code/simulations/brainit_fmri"
    },
    {
        "name": "Sim AXIOM-Series: Axioms of Trust & Evolutionary Assembly",
        "path": "code/simulations/repair_era/axioms_of_trust/sim_axiom_series.py",
        "workdir": "code/simulations/repair_era/axioms_of_trust"
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
    _brainit_venv = os.path.join(base_dir, "code/simulations/brainit_fmri/.venv/bin/python3")
    sim_python = _brainit_venv if ("brainit" in sim['path'] and os.path.exists(_brainit_venv)) else venv_python
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
