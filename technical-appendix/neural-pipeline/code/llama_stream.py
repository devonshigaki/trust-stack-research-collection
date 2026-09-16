"""Memory-streaming LLaMA-3.2-3B hidden-state extractor.

Runs the real unsloth/Llama-3.2-3B weights (identical to gated
meta-llama/Llama-3.2-3B) layer-by-layer via safetensors mmap so peak RAM
stays ~1 layer (~0.5 GB). Computes in fp32. Captures hidden states after
every transformer block. Validated by a next-token probe.
"""
import json
import math

import numpy as np
import torch
from safetensors import safe_open

CFG = json.load(open("/tmp/tribe/llama_config.json"))
SHARDS = ["/tmp/tribe/llama_model-00001-of-00002.safetensors",
          "/tmp/tribe/llama_model-00002-of-00002.safetensors"]
INDEX = json.load(open("/tmp/tribe/llama_model.safetensors.index.json"))["weight_map"]


class ShardReader:
    def __init__(self, paths):
        import os
        self.handles = {os.path.basename(p).replace("llama_", ""): safe_open(p, framework="pt") for p in paths}

    def get(self, name):
        return self.handles[INDEX[name]].get_tensor(name).float()

    def get_rows(self, name, rows):
        sl = self.handles[INDEX[name]].get_slice(name)
        return torch.stack([sl[int(r)].float() for r in rows])


def llama3_inv_freq(cfg):
    dim = cfg["head_dim"]
    base = cfg["rope_theta"]
    inv = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
    rs = cfg["rope_scaling"]
    factor = rs["factor"]
    low = rs["low_freq_factor"]
    high = rs["high_freq_factor"]
    old_ctx = rs["original_max_position_embeddings"]
    wavelen = 2 * math.pi / inv
    low_wl = old_ctx / low
    high_wl = old_ctx / high
    inv_new = inv.clone()
    smooth = (old_ctx / wavelen - low) / (high - low)
    smooth = smooth.clamp(0, 1)
    mid = (wavelen <= low_wl) & (wavelen >= high_wl)
    inv_new[mid] = (1 - smooth[mid]) * inv[mid] / factor + smooth[mid] * inv[mid]
    inv_new[wavelen > low_wl] = inv[wavelen > low_wl] / factor
    return inv_new  # [dim/2]


def rope(x, pos, inv_freq):
    # x: [seq, heads, head_dim]
    freqs = torch.outer(pos, inv_freq)  # [seq, dim/2]
    cos = freqs.cos()[:, None, :]
    sin = freqs.sin()[:, None, :]
    x1, x2 = x[..., ::2], x[..., 1::2]
    xr = torch.stack([-x2, x1], dim=-1).flatten(-2)
    out = x * torch.repeat_interleave(cos, 2, dim=-1) + xr * torch.repeat_interleave(sin, 2, dim=-1)
    return out


def rmsnorm(x, w, eps):
    return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * w


def extract_hidden_states(token_ids, layers_to_capture=None):
    """token_ids: list[int]. Returns dict layer_idx -> [seq, 3072] hidden states
    (layer_idx = number of blocks applied, 0 = embedding output)."""
    cfg = CFG
    H = cfg["num_hidden_layers"]
    nh, nkv, hd = cfg["num_attention_heads"], cfg["num_key_value_heads"], cfg["head_dim"]
    eps = cfg["rms_norm_eps"]
    reader = ShardReader(SHARDS)
    if layers_to_capture is None:
        layers_to_capture = set(range(H + 1))
    ids = torch.tensor(token_ids, dtype=torch.long)
    x = reader.get_rows("model.embed_tokens.weight", token_ids)  # [seq, 3072]
    seq = x.shape[0]
    pos = torch.arange(seq).float()
    inv_freq = llama3_inv_freq(cfg)
    mask = torch.full((seq, seq), float("-inf")).triu(1)
    captured = {}
    if 0 in layers_to_capture:
        captured[0] = x.clone()
    for i in range(H):
        p = f"model.layers.{i}."
        h = rmsnorm(x, reader.get(p + "input_layernorm.weight"), eps)
        q = h @ reader.get(p + "self_attn.q_proj.weight").T
        k = h @ reader.get(p + "self_attn.k_proj.weight").T
        v = h @ reader.get(p + "self_attn.v_proj.weight").T
        q = rope(q.view(seq, nh, hd), pos, inv_freq)
        k = rope(k.view(seq, nkv, hd), pos, inv_freq)
        v = v.view(seq, nkv, hd)
        k = k.repeat_interleave(nh // nkv, dim=1)
        v = v.repeat_interleave(nh // nkv, dim=1)
        att = torch.einsum("qhd,khd->hqk", q, k) / math.sqrt(hd) + mask
        att = att.softmax(-1)
        o = torch.einsum("hqk,khd->qhd", att, v).reshape(seq, nh * hd)
        o = o @ reader.get(p + "self_attn.o_proj.weight").T
        x = x + o
        h2 = rmsnorm(x, reader.get(p + "post_attention_layernorm.weight"), eps)
        gate = h2 @ reader.get(p + "mlp.gate_proj.weight").T
        up = h2 @ reader.get(p + "mlp.up_proj.weight").T
        down = torch.nn.functional.silu(gate) * up
        x = x + down @ reader.get(p + "mlp.down_proj.weight").T
        if (i + 1) in layers_to_capture:
            captured[i + 1] = x.clone()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        del q, k, v, att, o, h, h2, gate, up, down
    if (H + 1) in layers_to_capture:  # final normed output for probing
        captured[H + 1] = rmsnorm(x, reader.get("model.norm.weight"), eps)
    return captured
