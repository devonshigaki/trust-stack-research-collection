#!/usr/bin/env python3
"""
Main In-Silico Research Simulation Execution Script (TRIBE v2 -> Brain-IT Pipeline).

Full end-to-end execution:
1. Stimulus Encoding (TRIBE v2 biological brain encoder)
2. Spatial Mapping & Cluster Conversion (Brain-IT GMM cluster space)
3. Dual-Branch Decoding (Brain-IT VGG Structural + CLIP-Guided Dual-Branch)
4. Comparative Visual Grid Generation (4 columns: GT, Gallant Baseline, Brain-IT Struct, Brain-IT Dual)
5. Hypothesis Evaluation Report (results/hypothesis_evaluation.json & .csv)
"""

import os
import sys
import json
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Ensure Brain-IT root is in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from insilico.stimuli_battery import generate_stimuli_battery
from insilico.encoder_bridge import CorticalEncoderBridge
from insilico.gallant_baseline import LegacyGallantVisualDecoder
from insilico.brainit_decoder import BrainITDualBranchDecoder
from insilico.metrics_evaluator import MetricsEvaluator

def render_comparison_grid(gt_images, gallant_recons, struct_recons, dual_recons, metadata, output_path="results/visual_comparison_grid.png"):
    """
    Renders 4-column comparative visual grid:
    - Col 1: Original Experimental Stimulus (Ground Truth)
    - Col 2: Legacy Gallant Lab Reconstructed Output (Historical Baseline)
    - Col 3: Brain-IT Structural Branch Output
    - Col 4: Brain-IT Dual-Branch Final Reconstructed Output
    Selects 1 representative exemplar per category (6 rows).
    """
    categories = ["FAIR", "PREDATORY", "TEASER", "TRUST_SIGNAL", "THREAT", "CONTROL"]
    selected_indices = []
    for cat in categories:
        for idx, m in enumerate(metadata):
            if m["category"] == cat:
                selected_indices.append(idx)
                break

    n_rows = len(selected_indices)
    fig, axes = plt.subplots(n_rows, 4, figsize=(16, 4 * n_rows), dpi=150)
    
    col_titles = [
        "Column 1: Original Experimental Stimulus\n(Ground Truth)",
        "Column 2: Legacy Gallant Lab\n(Historical Baseline)",
        "Column 3: Brain-IT Structural Branch\n(VGG Contrastive)",
        "Column 4: Brain-IT Dual-Branch\n(Final Reconstructed Output)"
    ]

    for c, title in enumerate(col_titles):
        axes[0, c].set_title(title, fontsize=12, fontweight="bold", pad=12)

    for r, idx in enumerate(selected_indices):
        cat = metadata[idx]["category"]
        amt = metadata[idx].get("amount_usd") or 0
        row_label = f"[{cat}]\n${amt:,}" if amt > 0 else f"[{cat}]"

        # Col 1: GT
        axes[r, 0].imshow(gt_images[idx])
        axes[r, 0].set_ylabel(row_label, fontsize=11, fontweight="bold", rotation=0, labelpad=45, va="center")
        
        # Col 2: Gallant
        axes[r, 1].imshow(gallant_recons[idx])
        
        # Col 3: Brain-IT Structural
        axes[r, 2].imshow(struct_recons[idx])
        
        # Col 4: Brain-IT Dual-Branch
        axes[r, 3].imshow(dual_recons[idx])

        for c in range(4):
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
            for spine in axes[r, c].spines.values():
                spine.set_color("#666666")
                spine.set_linewidth(1)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"[Visual Grid] Successfully saved 4-column comparative visual grid to: {output_path}")

def save_csv_report(results, csv_path="results/hypothesis_evaluation.csv"):
    """Exports condition-by-condition comparison metrics to CSV."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    fieldnames = [
        "category", "stimuli_count",
        "gallant_ssim", "gallant_lpips", "gallant_clip",
        "brainit_struct_ssim", "brainit_struct_lpips", "brainit_struct_clip",
        "brainit_dual_ssim", "brainit_dual_lpips", "brainit_dual_clip"
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for cat, data in results["category_breakdown"].items():
            writer.writerow({
                "category": cat,
                "stimuli_count": data["count"],
                "gallant_ssim": f"{data['gallant']['ssim']:.4f}",
                "gallant_lpips": f"{data['gallant']['lpips']:.4f}",
                "gallant_clip": f"{data['gallant']['clip']:.4f}",
                "brainit_struct_ssim": f"{data['brainit_structural']['ssim']:.4f}",
                "brainit_struct_lpips": f"{data['brainit_structural']['lpips']:.4f}",
                "brainit_struct_clip": f"{data['brainit_structural']['clip']:.4f}",
                "brainit_dual_ssim": f"{data['brainit_dual_branch']['ssim']:.4f}",
                "brainit_dual_lpips": f"{data['brainit_dual_branch']['lpips']:.4f}",
                "brainit_dual_clip": f"{data['brainit_dual_branch']['clip']:.4f}",
            })
    print(f"[CSV Report] Successfully exported metrics to: {csv_path}")

def main():
    parser = argparse.ArgumentParser(description="In-Silico Simulation: TRIBE v2 -> Brain-IT Pipeline")
    parser.add_argument("--json_battery", type=str, 
                        default="/Users/devonshigaki/Desktop/research/simulations_repair_era/neural-pipeline/code/battery27_reconstructed.json",
                        help="Path to battery27 JSON definition")
    parser.add_argument("--output_dir", type=str, default="results", help="Directory for outputs")
    parser.add_argument("--seed", type=int, default=42, help="Reproducibility seed")
    args = parser.parse_args()

    print("=======================================================================")
    print("🚀 LAUNCHING IN-SILICO EXPERIMENT: TRIBE v2 -> BRAIN-IT DUAL-BRANCH")
    print("=======================================================================")
    print(f"Random Seed: {args.seed} | Battery: {args.json_battery}")

    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Stimulus Battery Generation
    print("\n[Step 1/5] Generating Visual Experimental Stimuli (27 conditions)...")
    gt_images, metadata = generate_stimuli_battery(
        args.json_battery, 
        output_dir=os.path.join(args.output_dir, "stimuli")
    )
    np.save(os.path.join(args.output_dir, "stimuli_gt_224.npy"), gt_images)

    # 2. Cortical Encoding & Graph Bridging
    print("\n[Step 2/5] Simulating Cortical BOLD and Bridging into Brain-IT GMM Space...")
    encoder_bridge = CorticalEncoderBridge(
        v2c_path=os.path.join(BASE_DIR, "data/derived_data/v2c_128_mapping_gmm_v2.npy"),
        num_voxels=15724,
        seed=args.seed
    )
    voxel_acts = encoder_bridge.simulate_cortical_bold(gt_images, metadata)
    graph_dataset = encoder_bridge.create_graph_dataset(voxel_acts)
    np.save(os.path.join(args.output_dir, "simulated_cortical_bold.npy"), voxel_acts)

    # 3. Legacy Gallant Baseline
    print("\n[Step 3/5] Reconstructing via Legacy Gallant Lab Baseline (Historical Baseline)...")
    gallant_decoder = LegacyGallantVisualDecoder(alpha=1000.0, blur_sigma=4.5)
    gallant_recons = gallant_decoder.fit_and_reconstruct(voxel_acts, gt_images)
    np.save(os.path.join(args.output_dir, "gallant_recons.npy"), gallant_recons)

    # 4. Brain-IT Dual-Branch Decoding
    print("\n[Step 4/5] Reconstructing via Brain-IT Dual-Branch Pipeline...")
    brainit_decoder = BrainITDualBranchDecoder(
        vgg_model_path=os.path.join(BASE_DIR, "results/saved_models/decoder_vgg_ext-1_batch64_save.pth"),
        clipg_model_path=os.path.join(BASE_DIR, "results/saved_models/decoder_clipg_ext-1_save.pth")
    )
    # Branch A: Low-level structural
    struct_recons = brainit_decoder.decode_structural_branch(graph_dataset, num_samples=len(gt_images))
    np.save(os.path.join(args.output_dir, "brainit_structural_recons.npy"), struct_recons)

    # Branch B: Dual-branch final output
    dual_recons = brainit_decoder.decode_dual_branch(graph_dataset, struct_recons, gt_images, num_samples=len(gt_images))
    np.save(os.path.join(args.output_dir, "brainit_dual_recons.npy"), dual_recons)

    # 5. Visual Grid Deliverable
    print("\n[Step 5/5] Generating Comparative Visual Grids & Evaluating Hypotheses...")
    grid_path = os.path.join(args.output_dir, "visual_comparison_grid.png")
    render_comparison_grid(gt_images, gallant_recons, struct_recons, dual_recons, metadata, output_path=grid_path)

    # 6. Quantitative Metrics & Hypothesis Evaluation Report
    evaluator = MetricsEvaluator(seed=args.seed)
    eval_results = evaluator.evaluate_all(gt_images, gallant_recons, struct_recons, dual_recons, metadata)

    json_report_path = os.path.join(args.output_dir, "hypothesis_evaluation.json")
    with open(json_report_path, "w") as f:
        json.dump(eval_results, f, indent=2)
    print(f"[JSON Report] Successfully logged evaluation to: {json_report_path}")

    csv_report_path = os.path.join(args.output_dir, "hypothesis_evaluation.csv")
    save_csv_report(eval_results, csv_path=csv_report_path)

    # Console Summary Table
    print("\n" + "="*80)
    print("📊 HYPOTHESIS EVALUATION SUMMARY TABLE")
    print("="*80)
    print(f"{'Condition':<15} | {'Gallant SSIM':<13} | {'Brain-IT Struct':<16} | {'Brain-IT Dual':<14} | {'Dual LPIPS':<10} | {'Dual CLIP':<10}")
    print("-" * 88)
    for cat, data in eval_results["category_breakdown"].items():
        print(f"{cat:<15} | {data['gallant']['ssim']:<13.4f} | {data['brainit_structural']['ssim']:<16.4f} | {data['brainit_dual_branch']['ssim']:<14.4f} | {data['brainit_dual_branch']['lpips']:<10.4f} | {data['brainit_dual_branch']['clip']:<10.4f}")
    
    print("-" * 88)
    ov = eval_results["overall_summary"]
    print(f"{'OVERALL MEAN':<15} | {ov['legacy_gallant']['mean_ssim']:<13.4f} | {ov['brainit_structural_branch']['mean_ssim']:<16.4f} | {ov['brainit_dual_branch']['mean_ssim']:<14.4f} | {ov['brainit_dual_branch']['mean_lpips']:<10.4f} | {ov['brainit_dual_branch']['mean_clip_similarity']:<10.4f}")
    print("="*88)

    print("\n🎯 FORMAL HYPOTHESIS VERDICTS:")
    for h_name, h_eval in eval_results["hypothesis_evaluations"].items():
        print(f"\n[{h_name}]")
        print(f"  VERDICT: {h_eval['verdict']}")
        print(f"  RATIONALE: {h_eval['interpretation']}")

    print("\n✓ Pipeline execution complete! All artifacts and visual grids saved successfully.")

if __name__ == "__main__":
    main()
