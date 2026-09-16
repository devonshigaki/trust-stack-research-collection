"""DOCAS N.1: run the reconstructed 27-stimulus battery through the manifest's
canonical per-stimulus pipeline:

  1. tokenize with LLaMA-3 BPE, NO BOS (add_special_tokens=False)
  2. LLaMA-3.2-3B forward (real unsloth mirror weights, fp32 compute);
     tap hidden states at layers 17 and 24 (manifest stand-ins for the released
     model's group-mean over layer ranges [(0.5,0.75),(0.75,1.0)])
  3. uniformly resample token sequence to 100 TRs:
     idx = min(arange(100) * seq // 100, seq - 1)
  4. features as f32 [2, 3072, 100]
  5. TRIBE v2 forward (real best.ckpt, 708,856,138 B, strict load) ->
     [20484, 100] fsaverage5 predictions per stimulus

Battery: battery27_reconstructed.json (reconstruction-from-spec label inside).
Output: results/battery27_preds.npz  + results/battery27_meta.json
"""
import json
import os
import time

import numpy as np
import torch
import yaml

sys_paths = ["/tmp/tribe/tribev2", "/tmp/tribe"]
import sys
for p in sys_paths:
    sys.path.insert(0, p)

from transformers import AutoTokenizer
from llama_stream import extract_hidden_states
from tribev2.model import FmriEncoder

torch.manual_seed(0)
np.random.seed(0)

OUT = "/tmp/tribe/results"
os.makedirs(OUT, exist_ok=True)

# ---------- TRIBE v2 ----------
ck = torch.load("/tmp/tribe/best.ckpt", map_location="cpu", weights_only=False)
sd = ck["state_dict"]
cfg_full = yaml.load(open("/tmp/tribe/config.yaml"), Loader=yaml.UnsafeLoader)
enc_cfg = FmriEncoder(**cfg_full["brain_model_config"])
enc_cfg.subject_layers.average_subjects = True
enc_cfg.subject_layers.n_subjects = 0
model = enc_cfg.build(feature_dims=ck["model_build_args"]["feature_dims"],
                      n_outputs=20484, n_output_timesteps=100)
model.load_state_dict({k[len("model."):]: v for k, v in sd.items()}, strict=True)
model.eval()
del sd, ck
print("TRIBE v2 loaded", flush=True)

tok = AutoTokenizer.from_pretrained("/tmp/tribe/llama_tok")

battery = json.load(open("/tmp/tribe/battery27_reconstructed.json"))["stimuli"]

class Batch:
    def __init__(self, data):
        self.data = data

def tribe_forward(text):
    ids = tok(text, add_special_tokens=False)["input_ids"]  # no BOS
    hid = extract_hidden_states(ids, layers_to_capture={17, 24})
    h17 = hid[17].numpy().astype(np.float32)  # [seq, 3072]
    h24 = hid[24].numpy().astype(np.float32)
    seq = h17.shape[0]
    idx = np.minimum(np.arange(100) * seq // 100, seq - 1)  # manifest resample
    feats = np.stack([h17[idx], h24[idx]], axis=0)  # [2, 100, 3072]
    feats = feats.transpose(0, 2, 1).copy()  # [2, 3072, 100] f32
    x = torch.from_numpy(feats)[None]  # [1, 2, 3072, 100]
    with torch.no_grad():
        out = model(Batch({"text": x}))  # [1, 20484, 100]
    return out[0].numpy(), seq

results, meta = {}, []
for stim in battery:
    t0 = time.time()
    out, seq = tribe_forward(stim["text"])
    results[stim["id"]] = out
    meta.append({**{k: stim[k] for k in ("id", "category", "item", "amount_usd",
                                         "verbatim_from_manifest")},
                 "n_tokens": seq,
                 "pred_mean": float(out.mean()), "pred_std": float(out.std())})
    print(f"{stim['id']}: seq={seq} mean={out.mean():.4f} std={out.std():.4f} "
          f"({time.time()-t0:.0f}s)", flush=True)

np.savez_compressed(f"{OUT}/battery27_preds.npz", **results)
json.dump({"_provenance": battery and json.load(open("/tmp/tribe/battery27_reconstructed.json"))["_provenance"],
           "pipeline": "no-BOS tokenize -> LLaMA-3.2-3B layers 17&24 -> token resample to 100 TRs -> f32 [2,3072,100] -> TRIBE v2 -> [20484,100]",
           "stimuli": meta}, open(f"{OUT}/battery27_meta.json", "w"), indent=1)

# ---------- determinism re-check on one stimulus ----------
out2, _ = tribe_forward(battery[0]["text"])
dmax = float(np.abs(out2 - results[battery[0]["id"]]).max())
print(f"determinism re-check ({battery[0]['id']}): max|delta| = {dmax}")
json.dump({"stimulus": battery[0]["id"], "max_abs_delta": dmax},
          open(f"{OUT}/battery27_determinism.json", "w"))
print("DONE")
