#!/usr/bin/env python3
"""
Comprehensive Execution Suite: Tier 1 (Simulations & SMT Proofs) and Tier 2 (Empirical Data APIs)
Validates all newly developed components for the Trust Stack (Version 4.0).
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(BASE_DIR, ".venv/bin/python3")
desktop_venv = "/Users/devonshigaki/Desktop/Research/.venv/bin/python3"
if os.path.exists(venv_python):
    PYTHON = venv_python
elif os.path.exists(desktop_venv):
    PYTHON = desktop_venv
else:
    PYTHON = sys.executable

TASKS = [
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Fisher-Rao Boundary Regularity Proofs",
        "script": "formal-verification/z3_fisher_rao_singularity.py",
        "workdir": "formal-verification"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim P8c: Provider-Diversity Entropy Gate (Anti-Collusion)",
        "script": "experiments/simulations_repair_era/tfp/sim_p8_collusion.py",
        "workdir": "experiments/simulations_repair_era/tfp"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim P8d: Economic Collusion Auction & Nash Break-Even Model",
        "script": "experiments/simulations_repair_era/tfp/sim_collusion_economic_auction.py",
        "workdir": "experiments/simulations_repair_era/tfp"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim W8: Temporal SHAP Adverse Action & Recourse Engine",
        "script": "experiments/simulations_repair_era/whitepaper/sim_shap_adverse_action.py",
        "workdir": "experiments/simulations_repair_era/whitepaper"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim W9: Dynamic Lemons Market & Capital Solvency ODE",
        "script": "experiments/simulations_repair_era/whitepaper/sim_dynamic_lemons_ode.py",
        "workdir": "experiments/simulations_repair_era/whitepaper"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim GEN-2: Omnigenic Striatal Coincidence & p-PGS Engine",
        "script": "experiments/simulations_repair_era/clinical/sim_polygenic_coincidence.py",
        "workdir": "experiments/simulations_repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim GEN-3: 2S-MR & Colocalization (DOCAS-GATE-2 Protocol)",
        "script": "experiments/simulations_repair_era/clinical/sim_2smr_phewas_protocol.py",
        "workdir": "experiments/simulations_repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim GEN-4: ADCY Coincidence Engine eQTL & Cognitive Flexibility 2S-MR",
        "script": "experiments/simulations_repair_era/clinical/sim_adcy_coincidence_genomics.py",
        "workdir": "experiments/simulations_repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim EVOL-1: 600M-Yr Evolutionary Conservation (Drosophila rutabaga to ADCY8)",
        "script": "experiments/simulations_repair_era/clinical/sim_evol1_rutabaga_adcy8_conservation.py",
        "workdir": "experiments/simulations_repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim BIO-1: Multiscale Coincidence & Levin Bioelectrics",
        "script": "experiments/simulations_repair_era/bioelectrics/sim_cellular_coincidence_levin.py",
        "workdir": "experiments/simulations_repair_era/bioelectrics"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-2: Multiscale Assembly Index of Trust across 7 Magnitudes",
        "script": "experiments/simulations_repair_era/docas/sim_assembly_multiscale.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Multiscale Assembly Manifold Invariants (Theorems MS-1–MS-4)",
        "script": "formal-verification/z3_multiscale_assembly_manifold.py",
        "workdir": "formal-verification"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim THERMO-1: Thermodynamic Landauer Bound on Trust Erasure",
        "script": "experiments/simulations_repair_era/docas/sim_landauer_trust_thermodynamics.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim MS-1: Tandem Mass Spectrometry Fragmentation Assembly Benchmark",
        "script": "experiments/simulations_repair_era/docas/sim_tandem_ms_assembly_trees.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim PATCH-1: Multicompartmental Pyramidal Cell HCN1 Shunting Kinetics",
        "script": "experiments/simulations_repair_era/docas/sim_patch_clamp_hcn_shunting.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-3: Quantum Molecular Expectation & Active Biological Repair",
        "script": "experiments/simulations_repair_era/docas/sim_quantum_molecular_expectation.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-4: Metabolome-Wide Assembly & Allosteric Token Partition",
        "script": "experiments/simulations_repair_era/docas/sim_at4_metabolome_assembly_partition.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-5: Multi-Constraint Token Landscape & Monte Carlo Null Permutation",
        "script": "experiments/simulations_repair_era/docas/sim_at5_probabilistic_landscape.py",
        "workdir": "experiments/simulations_repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim CRIT-2: Empirical Connectome Spectral Radius & Quasicritical Corridor",
        "script": "experiments/simulations_repair_era/criticality/sim_crit2_connectome_spectral_radius.py",
        "workdir": "experiments/simulations_repair_era/criticality"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim CRIT-3: Bayes Factor Model Comparison (Quasicritical 1/f vs Non-Critical)",
        "script": "experiments/simulations_repair_era/criticality/sim_crit3_bayes_factor_comparison.py",
        "workdir": "experiments/simulations_repair_era/criticality"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Quantum-Biological Isomorphism (Theorems Q-1–Q-4)",
        "script": "formal-verification/z3_quantum_molecular_isomorphism.py",
        "workdir": "formal-verification"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Tri-Critical Invariant & Variational Extremum (Theorems E-1–E-4)",
        "script": "formal-verification/z3_information_token_extremum.py",
        "workdir": "formal-verification"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "CFPB Consumer Complaint Database (Live REST API)",
        "script": "experiments/simulations_repair_era/whitepaper/query_cfpb_complaints.py",
        "workdir": "experiments/simulations_repair_era/whitepaper"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "CLICS 4.0 Colexification Graph & Permutation Tests",
        "script": "experiments/clics_graph/query_clics4_cldf.py",
        "workdir": "experiments/clics_graph"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "Ensembl Genomic Association Audit (PDE4B rs7528604)",
        "script": "experiments/simulations_repair_era/clinical/query_gtex_v8_eqtl.py",
        "workdir": "experiments/simulations_repair_era/clinical"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "OpenNeuro ds003020 Dataset & Semantic Model Verification",
        "script": "experiments/brainit-fmri/query_openneuro_ds003020.py",
        "workdir": "experiments/brainit-fmri"
    },
    {
        "tier": "Tier 1: Scientific Integrity",
        "name": "Multi-Rubric Integrity & Standards Verification (TOP, NeurIPS, Cochrane, APA, Huff)",
        "script": "evaluations/multi_rubric_evaluator.py",
        "workdir": "."
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim WEARABLE-TRIAD: Multi-Rate Biosensor Fusion (Muse Athena, Apple Watch S8, Dexcom Stelo)",
        "script": "experiments/wearables_pipeline/sim_wearable_triad_sensor_fusion.py",
        "workdir": "experiments/wearables_pipeline"
    }
]

def main():
    print("=" * 75)
    print("🚀 TRUST STACK - COMPREHENSIVE TIER 1 & TIER 2 EXECUTION SUITE")
    print("=" * 75)

    passed = 0
    failed = 0

    for i, task in enumerate(TASKS, 1):
        print(f"\n[{i}/{len(TASKS)}] Running [{task['tier']}]: {task['name']}...")
        script_path = os.path.join(BASE_DIR, task['script'])
        work_dir = os.path.join(BASE_DIR, task['workdir'])

        try:
            res = subprocess.run(
                [PYTHON, script_path],
                cwd=work_dir,
                capture_output=True,
                text=True,
                check=True
            )
            print("✓ PASS!")
            passed += 1
        except subprocess.CalledProcessError as e:
            print(f"✗ FAIL! (Exit Code {e.returncode})")
            print("Error Output:\n", e.stderr)
            failed += 1

    print("\n" + "=" * 75)
    print(f"SUMMARY: {passed}/{len(TASKS)} Tasks Succeeded | {failed} Failed")
    print("=" * 75)

    if failed == 0:
        print("🎉 ALL TIER 1 & TIER 2 FORMAL VERIFICATIONS & DATA PIPELINES COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
