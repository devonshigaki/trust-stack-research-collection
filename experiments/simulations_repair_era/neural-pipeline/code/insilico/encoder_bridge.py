"""
Biological Brain Encoder & Spatial Tensor Bridge (TRIBE v2 -> Brain-IT).
Simulates cortical BOLD activation tensors (~15,724 - 70,000 voxels) across the 27 experimental conditions
and bridges the representations into Brain-IT's 128 GMM cluster space using v2c_128_mapping_gmm_v2.npy.
"""

import os
import sys
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import models, transforms

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.datasets import EmbedGraphDataset

class CorticalEncoderBridge:
    def __init__(self, v2c_path="data/derived_data/v2c_128_mapping_gmm_v2.npy", num_voxels=15724, seed=42):
        self.num_voxels = num_voxels
        self.seed = seed
        np.random.seed(seed)
        torch.manual_seed(seed)
        
        # Load GMM mapping
        self.v2c_mapping = np.load(v2c_path)
        print(f"[CorticalEncoderBridge] Loaded GMM mapping from {v2c_path}, shape: {self.v2c_mapping.shape}")

        # VGG visual feature extractor representing hierarchical ventral visual stream (V1, V2, V4, IT)
        self.visual_extractor = models.vgg16(weights=models.VGG16_Weights.DEFAULT).features.eval()
        
        # Anatomical parcel assignment for simulated voxels:
        # 40% Early Visual (V1-V3), 30% Ventral Temporal / LOC (V4, IT), 15% Control / Salience, 15% Default Mode (DMN)
        self.voxel_regions = np.zeros(num_voxels, dtype=int)
        n_ev = int(0.40 * num_voxels)
        n_vt = int(0.30 * num_voxels)
        n_cont = int(0.15 * num_voxels)
        n_dmn = num_voxels - (n_ev + n_vt + n_cont)
        self.voxel_regions[:n_ev] = 0           # Early Visual
        self.voxel_regions[n_ev:n_ev+n_vt] = 1   # Ventral Temporal / Object
        self.voxel_regions[n_ev+n_vt:n_ev+n_vt+n_cont] = 2  # Control / Attention
        self.voxel_regions[n_ev+n_vt+n_cont:] = 3 # Default Mode / Valuation

        # Precompute projection matrices for spatial realism
        rng = np.random.RandomState(seed)
        self.W_ev = rng.randn(64 * 14 * 14, n_ev).astype(np.float32) / np.sqrt(64 * 14 * 14)
        self.W_vt = rng.randn(256 * 7 * 7, n_vt).astype(np.float32) / np.sqrt(256 * 7 * 7)

    def extract_visual_hierarchy(self, img_tensor):
        """Extract multi-scale hierarchical visual representations from stimuli."""
        # Normalize with ImageNet stats
        mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
        x = (img_tensor - mean) / std

        feats_ev = None
        feats_vt = None
        with torch.no_grad():
            for idx, layer in enumerate(self.visual_extractor):
                x = layer(x)
                if idx == 4: # early conv (V1/V2 layout & edges)
                    # Downsample to 14x14 for projection
                    feats_ev = F.adaptive_avg_pool2d(x, (14, 14)).reshape(x.shape[0], -1)
                elif idx == 16: # mid/late conv (object/typography)
                    feats_vt = F.adaptive_avg_pool2d(x, (7, 7)).reshape(x.shape[0], -1)
                    break
        return feats_ev.numpy(), feats_vt.numpy()

    def simulate_cortical_bold(self, images_np, metadata):
        """
        Simulate whole-cortex BOLD activation tensors across all 27 stimuli.
        Incorporate DOCAS §5.2 empirical cortical contrasts:
        - THREAT vs FAIR concentrates in Control and DMN parcels.
        - PREDATORY induces high early visual contrast and ventral attention.
        """
        N = len(images_np)
        img_tensor = torch.from_numpy(images_np).permute(0, 3, 1, 2).float() / 255.0
        feats_ev, feats_vt = self.extract_visual_hierarchy(img_tensor)

        voxel_acts = np.zeros((N, self.num_voxels), dtype=np.float32)

        n_ev = int(0.40 * self.num_voxels)
        n_vt = int(0.30 * self.num_voxels)
        n_cont = int(0.15 * self.num_voxels)
        
        # Early visual voxels driven by low-level image layout
        voxel_acts[:, :n_ev] = np.dot(feats_ev, self.W_ev)
        # Ventral temporal voxels driven by object and text shapes
        voxel_acts[:, n_ev:n_ev+n_vt] = np.dot(feats_vt, self.W_vt)

        # Higher-order Control & DMN modulation based on DOCAS §5.2 category effects
        rng = np.random.RandomState(self.seed + 10)
        for i, meta in enumerate(metadata):
            cat = meta["category"]
            amt_raw = meta.get("amount_usd")
            amt = (float(amt_raw) / 20000.0) if amt_raw is not None else 0.2

            if cat == "FAIR":
                # Balanced cognitive control, baseline DMN
                cont_mod = 0.05 + 0.02 * amt + 0.03 * rng.randn(n_cont)
                dmn_mod = -0.02 + 0.02 * rng.randn(self.num_voxels - (n_ev + n_vt + n_cont))
            elif cat == "PREDATORY":
                # High ventral attention & salience, elevated warning
                cont_mod = 0.12 + 0.05 * amt + 0.04 * rng.randn(n_cont)
                dmn_mod = 0.08 + 0.03 * rng.randn(self.num_voxels - (n_ev + n_vt + n_cont))
            elif cat == "TEASER":
                # Reward/control tension
                cont_mod = 0.08 + 0.03 * amt + 0.03 * rng.randn(n_cont)
                dmn_mod = 0.04 + 0.02 * rng.randn(self.num_voxels - (n_ev + n_vt + n_cont))
            elif cat == "TRUST_SIGNAL":
                # Enhanced ventral integration, positive social alignment
                cont_mod = 0.03 + 0.02 * rng.randn(n_cont)
                dmn_mod = -0.05 + 0.02 * rng.randn(self.num_voxels - (n_ev + n_vt + n_cont))
            elif cat == "THREAT":
                # Peak Control & DMN contrast (matching DOCAS THREAT - FAIR finding)
                cont_mod = 0.22 + 0.08 * amt + 0.04 * rng.randn(n_cont)
                dmn_mod = 0.28 + 0.09 * amt + 0.04 * rng.randn(self.num_voxels - (n_ev + n_vt + n_cont))
            else: # CONTROL
                # Minimal cognitive control, peaceful default mode
                cont_mod = -0.05 + 0.02 * rng.randn(n_cont)
                dmn_mod = -0.08 + 0.02 * rng.randn(self.num_voxels - (n_ev + n_vt + n_cont))

            voxel_acts[i, n_ev+n_vt:n_ev+n_vt+n_cont] = cont_mod
            voxel_acts[i, n_ev+n_vt+n_cont:] = dmn_mod

        # Standardize across voxels (zero mean, unit variance per stimulus)
        voxel_acts = (voxel_acts - voxel_acts.mean(axis=1, keepdims=True)) / (voxel_acts.std(axis=1, keepdims=True) + 1e-8)
        print(f"[CorticalEncoderBridge] Simulated BOLD activations for {N} stimuli. Matrix shape: {voxel_acts.shape}")
        return voxel_acts

    def create_graph_dataset(self, voxel_acts):
        """Wrap simulated BOLD activations into Brain-IT's EmbedGraphDataset."""
        N = voxel_acts.shape[0]
        sub_vector = np.zeros(N, dtype=int) # Subject 0
        Y_placeholder = np.zeros((N, 1))
        sub_num_voxels = np.array([self.num_voxels])

        dataset = EmbedGraphDataset(
            voxel_acts,
            Y_placeholder,
            self.v2c_mapping,
            sub_vector,
            sub_num_voxels=sub_num_voxels,
            sample=False,
            num_centers=128
        )
        return dataset
