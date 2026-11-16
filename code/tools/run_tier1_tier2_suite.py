#!/usr/bin/env python3
"""
Comprehensive Execution Suite: Tier 1 (Simulations & SMT Proofs) and Tier 2 (Empirical Data APIs)
Validates all newly developed components for the Trust Stack (Version 4.0).
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
venv_python = os.path.join(BASE_DIR, ".venv/bin/python3")
PYTHON = venv_python if os.path.exists(venv_python) else sys.executable

TASKS = [
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Fisher-Rao Boundary Regularity Proofs",
        "script": "formal/z3_fisher_rao_singularity.py",
        "workdir": "formal"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 Trust vs. Selection Thermodynamic & Architectural Invariants",
        "script": "formal/z3_trust_vs_selection_thermodynamic_invariance.py",
        "workdir": "formal"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AXIOM-Series: Axioms of Trust & Evolutionary Assembly",
        "script": "code/simulations/repair_era/axioms_of_trust/sim_axiom_series.py",
        "workdir": "code/simulations/repair_era/axioms_of_trust"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim P8c: Provider-Diversity Entropy Gate (Anti-Collusion)",
        "script": "code/simulations/repair_era/tfp/sim_p8_collusion.py",
        "workdir": "code/simulations/repair_era/tfp"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim P8d: Economic Collusion Auction & Nash Break-Even Model",
        "script": "code/simulations/repair_era/tfp/sim_collusion_economic_auction.py",
        "workdir": "code/simulations/repair_era/tfp"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim W8: Temporal SHAP Adverse Action & Recourse Engine",
        "script": "code/simulations/repair_era/whitepaper/sim_shap_adverse_action.py",
        "workdir": "code/simulations/repair_era/whitepaper"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim W9: Dynamic Lemons Market & Capital Solvency ODE",
        "script": "code/simulations/repair_era/whitepaper/sim_dynamic_lemons_ode.py",
        "workdir": "code/simulations/repair_era/whitepaper"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim GEN-2: Omnigenic Striatal Coincidence & p-PGS Engine",
        "script": "code/simulations/repair_era/clinical/sim_polygenic_coincidence.py",
        "workdir": "code/simulations/repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim GEN-3: 2S-MR & Colocalization (DOCAS-GATE-2 Protocol)",
        "script": "code/simulations/repair_era/clinical/sim_2smr_phewas_protocol.py",
        "workdir": "code/simulations/repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim GEN-4: ADCY Coincidence Engine eQTL & Cognitive Flexibility 2S-MR",
        "script": "code/simulations/repair_era/clinical/sim_adcy_coincidence_genomics.py",
        "workdir": "code/simulations/repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim EVOL-1: 600M-Yr Evolutionary Conservation (Drosophila rutabaga to ADCY8)",
        "script": "code/simulations/repair_era/clinical/sim_evol1_rutabaga_adcy8_conservation.py",
        "workdir": "code/simulations/repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim BIO-1: Multiscale Coincidence & Levin Bioelectrics",
        "script": "code/simulations/repair_era/bioelectrics/sim_cellular_coincidence_levin.py",
        "workdir": "code/simulations/repair_era/bioelectrics"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-2: Multiscale Assembly Index of Trust across 7 Magnitudes",
        "script": "code/simulations/repair_era/docas/sim_assembly_multiscale.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Multiscale Assembly Manifold Invariants (Theorems MS-1–MS-4)",
        "script": "formal/z3_multiscale_assembly_manifold.py",
        "workdir": "formal"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim THERMO-1: Thermodynamic Landauer Bound on Trust Erasure",
        "script": "code/simulations/repair_era/docas/sim_landauer_trust_thermodynamics.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim MS-1: Tandem Mass Spectrometry Fragmentation Assembly Benchmark",
        "script": "code/simulations/repair_era/docas/sim_tandem_ms_assembly_trees.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim PATCH-1: Multicompartmental Pyramidal Cell HCN1 Shunting Kinetics",
        "script": "code/simulations/repair_era/docas/sim_patch_clamp_hcn_shunting.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-3: Quantum Molecular Expectation & Active Biological Repair",
        "script": "code/simulations/repair_era/docas/sim_quantum_molecular_expectation.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-4: Metabolome-Wide Assembly & Allosteric Token Partition",
        "script": "code/simulations/repair_era/docas/sim_at4_metabolome_assembly_partition.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim AT-5: Multi-Constraint Token Landscape & Monte Carlo Null Permutation",
        "script": "code/simulations/repair_era/docas/sim_at5_probabilistic_landscape.py",
        "workdir": "code/simulations/repair_era/docas"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim CRIT-2: Empirical Connectome Spectral Radius & Quasicritical Corridor",
        "script": "code/simulations/repair_era/criticality/sim_crit2_connectome_spectral_radius.py",
        "workdir": "code/simulations/repair_era/criticality"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim CRIT-3: Bayes Factor Model Comparison (Quasicritical 1/f vs Non-Critical)",
        "script": "code/simulations/repair_era/criticality/sim_crit3_bayes_factor_comparison.py",
        "workdir": "code/simulations/repair_era/criticality"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Quantum-Biological Isomorphism (Theorems Q-1–Q-4)",
        "script": "formal/z3_quantum_molecular_isomorphism.py",
        "workdir": "formal"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "Z3 & SymPy Tri-Critical Invariant & Variational Extremum (Theorems E-1–E-4)",
        "script": "formal/z3_information_token_extremum.py",
        "workdir": "formal"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "CFPB Consumer Complaint Database (Live REST API)",
        "script": "code/simulations/repair_era/whitepaper/query_cfpb_complaints.py",
        "workdir": "code/simulations/repair_era/whitepaper"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "CLICS 4.0 Colexification Graph & Permutation Tests",
        "script": "code/empirical/clics_graph/query_clics4_cldf.py",
        "workdir": "code/empirical/clics_graph"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "Ensembl Genomic Association Audit (PDE4B rs7528604)",
        "script": "code/simulations/repair_era/clinical/query_gtex_v8_eqtl.py",
        "workdir": "code/simulations/repair_era/clinical"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "OpenNeuro ds003020 Dataset & Semantic Model Verification",
        "script": "code/simulations/brainit_fmri/query_openneuro_ds003020.py",
        "workdir": "code/simulations/brainit_fmri"
    },
    {
        "tier": "Tier 1: Scientific Integrity",
        "name": "Multi-Rubric Integrity & Standards Verification (TOP, NeurIPS, Cochrane, APA, Huff)",
        "script": "code/tools/evaluations/multi_rubric_evaluator.py",
        "workdir": "."
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim WEARABLE-TRIAD: Multi-Rate Biosensor Fusion (Muse Athena, Apple Watch S8, Dexcom Stelo)",
        "script": "code/simulations/wearables_pipeline/sim_wearable_triad_sensor_fusion.py",
        "workdir": "code/simulations/wearables_pipeline"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim PERSUADE-1: Lindquist-Watson Agential Convergence & Mutual Persuasion ODE",
        "script": "code/simulations/repair_era/agency/sim_persuade1_mutual_persuasion.py",
        "workdir": "code/simulations/repair_era/agency"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim PILOT-1: End-to-End 30-Day Multimodal Pre-Flight Mock Trial Runner",
        "script": "code/simulations/wearables_pipeline/simulate_30day_dense_pilot.py",
        "workdir": "code/simulations/wearables_pipeline"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim PILOT-2: Full 180-Day 14-Stream Synthetic Benchmark (V4.5 Protocol)",
        "script": "code/simulations/wearables_pipeline/simulate_180day_dense_pilot.py",
        "workdir": "code/simulations/wearables_pipeline"
    },
    {
        "tier": "Tier 1: Formal Math",
        "name": "ZK-STP v8 secp256k1 3-Party Unlinkable Tail-Complete Verifier (23/23)",
        "script": "formal/zk_master_law_stp.py",
        "workdir": "formal"
    },
    {
        "tier": "Tier 1: Hardware Driver",
        "name": "Muse S Athena BrainFlow Driver, Channel Remapping & AES-GCM Self-Test",
        "script": "code/simulations/wearables_pipeline/stream_muse_athena.py",
        "workdir": "code/simulations/wearables_pipeline",
        "args": ["--self-test"]
    },
    {
        "tier": "Tier 1: Signal Processing",
        "name": "Prefrontal fNIRS Modified Beer-Lambert Law (MBLL) & TDDR Self-Test",
        "script": "code/simulations/wearables_pipeline/process_fnirs_mbll.py",
        "workdir": "code/simulations/wearables_pipeline",
        "args": ["--self-test"]
    },
    {
        "tier": "Tier 1: Protocol Concordance",
        "name": "DOCAS-PILOT-1 Multi-Modal Concordance, TOST & BY-FDR Self-Test",
        "script": "code/simulations/wearables_pipeline/evaluate_pilot1_concordance.py",
        "workdir": "code/simulations/wearables_pipeline",
        "args": ["--self-test"]
    },
    {
        "tier": "Tier 1: Empirical Data",
        "name": "Real 30,000-Borrower Longitudinal Credit Panel Benchmark (OpenML 42477)",
        "script": "code/empirical/credit_panel/validate_master_law_credit_panel.py",
        "workdir": "code/empirical/credit_panel"
    },
    {
        "tier": "Tier 1: Cross-Repo Parity",
        "name": "Master Law Golden-Vector Parity (Python <-> R1CS <-> Rust UniFFI)",
        "script": "code/tools/test_cross_repo_parity.py",
        "workdir": "code/tools"
    },
    {
        "tier": "Tier 1: Manuscript Integrity",
        "name": "LaTeX Version 4.5 & Claim-Sync Linter across all 6 Manuscripts",
        "script": "code/tools/check_manuscript_sync.py",
        "workdir": "code/tools"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "Sim D14: AlphaGenome Regulatory Variant Quantile Audit (PDE4B 790k Rows)",
        "script": "code/empirical/simD14/apply_frozen_rule.py",
        "workdir": "code/empirical/simD14"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "Sim D15: GTEx v8 13-Brain-Tissue PDE4B cis-eQTL Audit (Honest FAIL Reported)",
        "script": "code/empirical/simD15/apply_frozen_rule_d15.py",
        "workdir": "code/empirical/simD15"
    },
    {
        "tier": "Tier 2: Public Data",
        "name": "Connectomics Readout Verification (FlyWire F1a2/F1b + MICrONS H1a 722k Synapses)",
        "script": "code/empirical/connectomics_flywire/verify_connectomics_readouts.py",
        "workdir": "code/empirical/connectomics_flywire"
    },
    {
        "tier": "Tier 1: Formal & ML",
        "name": "Autoresearch SIM-R1 Adaptive-Lambda Estimator: Z3 Proof + N=600 Sealed Vault",
        "script": "code/tools/autoresearch/verify_discovered_estimator.py",
        "workdir": "code/tools/autoresearch"
    },
    {
        "tier": "Tier 1: Adversarial Security",
        "name": "Adversarial Autoresearch Red-Team: 200 Sybil & Cartel-Split Mutations",
        "script": "code/tools/autoresearch/redteam_sybil.py",
        "workdir": "code/tools/autoresearch"
    },
    {
        "tier": "Tier 1: Distributed Protocol",
        "name": "Sim TFP-ClockSkew: Clamped Non-Commutativity & HLC G-Set Op-Log Convergence",
        "script": "code/simulations/repair_era/protocol/sim_tfp_clock_skew.py",
        "workdir": "code/simulations/repair_era/protocol"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim CRIT-Series: Kinouchi-Copelli N=600 Criticality & CSN/Vuong Cascades",
        "script": "code/simulations/repair_era/criticality/sim_crit_branching.py",
        "workdir": "code/simulations/repair_era/criticality"
    },
    {
        "tier": "Tier 1: Clinical Design",
        "name": "DOCAS-GATE-1 Statistical Power Audit (Nominal vs. 5-Channel Holm-Bonferroni FWER)",
        "script": "code/simulations/repair_era/clinical/sim_gate1_power.py",
        "workdir": "code/simulations/repair_era/clinical"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim A1: Adversarial Grooming vs. K-Step Bayesian Bellman Rollout",
        "script": "code/simulations/repair_era/adv_llm_dmn/sim_a1_adv_llm_dmn.py",
        "workdir": "code/simulations/repair_era/adv_llm_dmn"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim DMN-Series: Selective Counterfactual Rollout Depth (K=1..10)",
        "script": "code/simulations/repair_era/dmn/sim_dmn_planning.py",
        "workdir": "code/simulations/repair_era/dmn"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim O-Series: 4-State Markov Kinetic Opsin Causal Interventions",
        "script": "code/simulations/repair_era/optogenetics/code/sim_o_series.py",
        "workdir": "code/simulations/repair_era/optogenetics"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim B-Series: 2D Bioelectric Stress-Field & Extracellular Memory Maze",
        "script": "code/simulations/repair_era/basal_cognition/sim_b_basal_maze.py",
        "workdir": "code/simulations/repair_era/basal_cognition"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim X-Series: 4-Topology Benettin Cross-Substrate Dynamical Invariance",
        "script": "code/simulations/repair_era/cross_substrate/sim_x_cross_substrate.py",
        "workdir": "code/simulations/repair_era/cross_substrate"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim S-Series: 8D Naming-Game Lexicon Drift & Betrayal Spectral Entropy",
        "script": "code/simulations/repair_era/semantic_drift/sim_s_semantics.py",
        "workdir": "code/simulations/repair_era/semantic_drift"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim K-Series: Forward Diploid Wright-Fisher Parent-Pointer TMRCA",
        "script": "code/simulations/repair_era/genealogy/sim_k_genealogy.py",
        "workdir": "code/simulations/repair_era/genealogy"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim B1: Double-Gamma BOLD HRF Deconvolution & Lag-Augmented EKF",
        "script": "code/simulations/repair_era/tribe_bayes/sim_b1_tribe_bayes.py",
        "workdir": "code/simulations/repair_era/tribe_bayes"
    },
    {
        "tier": "Tier 1: Simulation",
        "name": "Sim S1: Poisson Spike + DA Jitter D1/D2 Three-Factor Striatal STDP",
        "script": "code/simulations/repair_era/striatal_microcircuit/sim_s1_striatal.py",
        "workdir": "code/simulations/repair_era/striatal_microcircuit"
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
        cmd = [PYTHON, script_path] + task.get("args", [])

        try:
            res = subprocess.run(
                cmd,
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
