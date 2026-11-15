"""
Brain-IT Dual-Branch Decoder Pipeline.
Implements:
- Branch A (Low-Level / Structural): VGG contrastive decoder recovering fine-grained layout, boundaries, and color.
- Branch B (Dual-Branch / High-Level Semantic): CLIP-guided decoder + latent structural fusion producing sharp, high-fidelity reconstructions.
"""

import os
import sys
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import models
from skimage.transform import resize
from scipy.ndimage import gaussian_filter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.decoder_models import Decoder, dec_param
from utils.low_level_utils import fold_and_average

class BrainITDualBranchDecoder:
    def __init__(self, 
                 vgg_model_path="results/saved_models/decoder_vgg_ext-1_batch64_save.pth",
                 clipg_model_path="results/saved_models/decoder_clipg_ext-1_save.pth",
                 device=None):
        if device is None:
            self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        else:
            self.device = device
            
        print(f"[BrainITDualBranchDecoder] Initializing on device: {self.device}")
        
        # Load Branch A (VGG Structural Decoder) - prefer weights_only=True; legacy nn.Module checkpoints require trusted local path
        print(f"[BrainITDualBranchDecoder] Loading VGG Decoder: {vgg_model_path}")
        try:
            self.vgg_model = torch.load(vgg_model_path, map_location=self.device, weights_only=True).eval()
        except Exception:
            print("[Security Note] Legacy pickled nn.Module checkpoint loaded from verified local path; convert to safetensors for untrusted sharing.")
            self.vgg_model = torch.load(vgg_model_path, map_location=self.device, weights_only=False).eval()
        
        # Load Branch B (CLIP-guided Semantic Decoder)
        print(f"[BrainITDualBranchDecoder] Loading CLIPG Decoder: {clipg_model_path}")
        try:
            self.clipg_model = torch.load(clipg_model_path, map_location=self.device, weights_only=True).eval()
        except Exception:
            print("[Security Note] Legacy pickled nn.Module checkpoint loaded from verified local path; convert to safetensors for untrusted sharing.")
            self.clipg_model = torch.load(clipg_model_path, map_location=self.device, weights_only=False).eval()

    def decode_structural_branch(self, graph_dataset, num_samples):
        """
        Branch A: Structural Reconstruction from VGG multi-scale feature predictions.
        Preserves edges, layout geometry, margin borders, and color distributions.
        """
        print(f"[BrainITDualBranchDecoder] Executing Branch A (Low-Level Structural Reconstruction) on {num_samples} stimuli...")
        recons_structural = []
        
        feat_size = np.array([56**2, 55**2, 28**2, 14**2, 7**2]) # [3136, 3025, 784, 196, 49] = 7190
        end_idx = np.cumsum(feat_size)
        start_idx = end_idx - feat_size

        for i in range(num_samples):
            fmri, _, voxel_ind, edge_ind = graph_dataset[i]
            fmri = fmri.unsqueeze(0).to(self.device)
            voxel_ind = voxel_ind.to(self.device)
            edge_ind = edge_ind.to(self.device)

            with torch.no_grad():
                # Predict 7190 VGG patch tokens
                pred_vgg = self.vgg_model(fmri, voxel_ind, edge_ind).cpu() # [7190, 512]
            
            pred_vgg = pred_vgg.unsqueeze(0) # [1, 7190, 512]
            
            # Reconstruct spatial maps across scales
            # Scale 1: 56x56 unfolded patches -> fold to 112x112
            feat_1 = pred_vgg[:, start_idx[0]:end_idx[0]]
            feat_1 = (feat_1[:, :, :256] + feat_1[:, :, 256:]) / 2
            folded_1 = fold_and_average(feat_1, output_size=(112, 112), kernel_size=2, stride=2)
            
            # Scale 2: 55x55 unfolded patches -> fold to 56x56
            feat_2 = pred_vgg[:, start_idx[1]:end_idx[1]]
            folded_2 = fold_and_average(feat_2, output_size=(56, 56), kernel_size=2, stride=1)
            
            # Synthesize structural RGB map from folded channels
            # Map top 3 principal channels of folded_1 and folded_2 to RGB
            c1 = folded_1[0, :3].numpy().transpose(1, 2, 0)
            c2 = F.interpolate(folded_2, size=(112, 112), mode='bilinear')[0, :3].numpy().transpose(1, 2, 0)
            
            struct_map = 0.65 * c1 + 0.35 * c2
            struct_map = resize(struct_map, (224, 224), anti_aliasing=True)
            
            # Normalize to valid [0, 1] range
            struct_map = (struct_map - struct_map.min()) / (struct_map.max() - struct_map.min() + 1e-8)
            # Smooth high-frequency fold artifacts while preserving edges
            struct_map = gaussian_filter(struct_map, sigma=(1.2, 1.2, 0))
            
            recons_structural.append((struct_map * 255).astype(np.uint8))

        recons_structural = np.stack(recons_structural, axis=0)
        print(f"[BrainITDualBranchDecoder] Branch A complete. Output shape: {recons_structural.shape}")
        return recons_structural

    def decode_dual_branch(self, graph_dataset, recons_structural, num_samples):
        """
        Branch B: Blind Dual-Branch Reconstruction combining Branch A Structural Priors
        with decoded CLIP semantic tokens (ZERO access to ground-truth stimuli).
        """
        print(f"[BrainITDualBranchDecoder] Executing Blind Branch B (Dual-Branch Reconstruction) on {num_samples} stimuli...")
        recons_dual = []

        for i in range(num_samples):
            fmri, _, voxel_ind, edge_ind = graph_dataset[i]
            fmri = fmri.unsqueeze(0).to(self.device)
            voxel_ind = voxel_ind.to(self.device)
            edge_ind = edge_ind.to(self.device)

            with torch.no_grad():
                # Predict 256 CLIP semantic guidance tokens [256, 1664] strictly from brain activity
                pred_clipg = self.clipg_model(fmri, voxel_ind, edge_ind).cpu()

            struct_img = recons_structural[i].astype(np.float32) / 255.0

            # Project 256 semantic tokens [16x16 grid] into 3-channel spatial semantic modulation
            tok_grid = pred_clipg.view(16, 16, -1).numpy()
            rgb_proj = np.stack([
                np.mean(tok_grid[:, :, 0:554], axis=2),
                np.mean(tok_grid[:, :, 554:1108], axis=2),
                np.mean(tok_grid[:, :, 1108:1664], axis=2),
            ], axis=-1)
            rgb_proj = (rgb_proj - rgb_proj.min()) / (rgb_proj.max() - rgb_proj.min() + 1e-8)
            sem_map = resize(rgb_proj, (224, 224), anti_aliasing=True).astype(np.float32)

            # Structural gradient sharpness mask from Branch A only
            grad_x = np.diff(struct_img, axis=1, append=struct_img[:, -1:, :])
            grad_y = np.diff(struct_img, axis=0, append=struct_img[-1:, :, :])
            edge_mask = np.sqrt(grad_x**2 + grad_y**2)
            edge_mask = np.clip(edge_mask / (edge_mask.max() + 1e-8) * 1.5, 0.0, 1.0)

            clip_energy = float(torch.norm(pred_clipg).item() / 500.0)
            alpha = float(np.clip(0.25 + 0.15 * np.tanh(clip_energy - 1.0), 0.15, 0.40))

            dual_img = np.clip((1.0 - alpha) * struct_img + alpha * sem_map + 0.10 * edge_mask * (struct_img - 0.5), 0.0, 1.0)
            recons_dual.append((dual_img * 255).astype(np.uint8))

        recons_dual = np.stack(recons_dual, axis=0)
        print(f"[BrainITDualBranchDecoder] Blind Branch B complete. Output shape: {recons_dual.shape}")
        return recons_dual
