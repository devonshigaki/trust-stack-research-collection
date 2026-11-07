"""DOCAS x TRIBE v2 minimal real run.

Real artifacts: facebook/tribev2 best.ckpt (708,856,138 B, 108 tensors)
+ unsloth/Llama-3.2-3B weights (= gated meta-llama/Llama-3.2-3B, bf16).
Text features: hidden states of LLaMA blocks 14-20 (group 1) and 21-28
(group 2), group_mean exactly as neuralset HuggingFaceMixin does for
layers=[0.5, 0.75, 1.0] on the 28-layer model (latents[14:21], latents[21:29]).
Words laid out at 0.4 s intervals, 2 Hz feature frames, TRIBE v2 pools to
100 TRs x 20,484 fsaverage5 vertices. Audio/video inputs are zero (modality
dropout design allows text-only; same convention as the Rust port's zeros).
"""
import json
import sys
import time

import numpy as np
import torch
import yaml

sys.path.insert(0, "/tmp/tribe/tribev2")
sys.path.insert(0, "/tmp/tribe")

from transformers import AutoTokenizer
from llama_stream import extract_hidden_states
from tribev2.model import FmriEncoder

torch.manual_seed(0)
np.random.seed(0)


def tokens_to_words(text, words, offsets):
    word_spans, pos = [], 0
    for w in words:
        i = text.find(w, pos); word_spans.append((i, i + len(w))); pos = i + len(w)
    tok2word = []
    for (s, e) in offsets:
        if s == e:
            tok2word.append(None); continue
        while s < e and text[s] == " ":
            s += 1
        widx = next((j for j, (ws, we) in enumerate(word_spans) if s >= ws and e <= we), None)
        tok2word.append(widx)
    return word_spans, tok2word

OUT = "/tmp/tribe/results"
import os
os.makedirs(OUT, exist_ok=True)

# ---------- load TRIBE v2 ----------
ck = torch.load("/tmp/tribe/best.ckpt", map_location="cpu", weights_only=False)
sd = ck["state_dict"]
cfg_full = yaml.load(open("/tmp/tribe/config.yaml"), Loader=yaml.UnsafeLoader)
bmc = cfg_full["brain_model_config"]
enc_cfg = FmriEncoder(**bmc)
enc_cfg.subject_layers.average_subjects = True
enc_cfg.subject_layers.n_subjects = 0
model = enc_cfg.build(feature_dims=ck["model_build_args"]["feature_dims"],
                      n_outputs=20484, n_output_timesteps=100)
model.load_state_dict({k[len("model."):]: v for k, v in sd.items()}, strict=True)
model.eval()
del sd, ck
print("TRIBE v2 loaded", flush=True)

tok = AutoTokenizer.from_pretrained("/tmp/tribe/llama_tok")
stimuli = {k: v for k, v in json.load(open("/tmp/tribe/stimuli.json")).items()
           if not k.startswith("_")}

WORD_DUR = 0.4  # s per word, uniform schedule
FEAT_HZ = 2.0

class Batch:
    def __init__(self, data):
        self.data = data

results = {}
for name, text in stimuli.items():
    words = text.split()
    # tokenize whole text once with offsets (full context, like neuralset contextualized=True)
    enc = tok(text, return_offsets_mapping=True, add_special_tokens=True)
    ids = enc["input_ids"]
    offsets = enc["offset_mapping"]
    t0 = time.time()
    hid = extract_hidden_states(ids, layers_to_capture=set(range(14, 29)))
    # groups per neuralset group_mean: latents[14:21] and latents[21:29]
    g1 = torch.stack([hid[i] for i in range(14, 21)]).mean(0)  # [seq, 3072]
    g2 = torch.stack([hid[i] for i in range(21, 29)]).mean(0)
    feats_tok = torch.cat([g1, g2], dim=-1)  # [seq, 6144]
    word_spans, tok2word = tokens_to_words(text, words, offsets)
    word_feats = np.zeros((len(words), 6144), dtype=np.float32)
    for j in range(len(words)):
        rows = [k for k, w in enumerate(tok2word) if w == j]
        word_feats[j] = feats_tok[rows].mean(0).numpy()
    # 2 Hz timeline
    duration = len(words) * WORD_DUR
    T = max(int(np.ceil(duration * FEAT_HZ)), 4)
    timeline = np.zeros((T, 6144), dtype=np.float32)
    for j in range(len(words)):
        f = int((j * WORD_DUR) * FEAT_HZ)
        if f < T:
            timeline[f] += word_feats[j]  # aggregation: sum (config)
    x = torch.from_numpy(timeline).T[None, None, :, :]  # [1, 1, 6144, T]
    x = x.view(1, 2, 3072, T)  # [B, L, D, T]  (layer_aggregation: cat -> same thing)
    with torch.no_grad():
        out = model(Batch({"text": x}))  # [1, 20484, 100]
    out = out[0].numpy()  # [20484, 100]
    results[name] = out
    print(f"{name}: {len(words)} words, seq={len(ids)}, T={T}, "
          f"out mean={out.mean():.4f} std={out.std():.4f} ({time.time()-t0:.0f}s)", flush=True)

np.savez_compressed(f"{OUT}/tribe_preds.npz", **results)

# ---------- determinism check on one stimulus ----------
text = stimuli["FAIR"]
words = text.split()
enc = tok(text, return_offsets_mapping=True, add_special_tokens=True)
hid = extract_hidden_states(enc["input_ids"], layers_to_capture=set(range(14, 29)))
g1 = torch.stack([hid[i] for i in range(14, 21)]).mean(0)
g2 = torch.stack([hid[i] for i in range(21, 29)]).mean(0)
feats_tok = torch.cat([g1, g2], -1)
offsets = enc["offset_mapping"]
word_spans, tok2word = tokens_to_words(text, words, offsets)
word_feats = np.zeros((len(words), 6144), dtype=np.float32)
for j in range(len(words)):
    rows = [k for k, w in enumerate(tok2word) if w == j]
    word_feats[j] = feats_tok[rows].mean(0).numpy()
T = max(int(np.ceil(len(words) * WORD_DUR * FEAT_HZ)), 4)
timeline = np.zeros((T, 6144), dtype=np.float32)
for j in range(len(words)):
    f = int((j * WORD_DUR) * FEAT_HZ)
    if f < T:
        timeline[f] += word_feats[j]
x = torch.from_numpy(timeline).T[None].view(1, 2, 3072, T)
with torch.no_grad():
    out2 = model(Batch({"text": x}))[0].numpy()
dmax = float(np.abs(out2 - results["FAIR"]).max())
print(f"determinism: max|delta| = {dmax}")
json.dump({"max_abs_delta": dmax}, open(f"{OUT}/determinism.json", "w"))

# ---------- separability: pairwise Pearson of TR-mean maps ----------
names = list(results)
mean_maps = {n: results[n].mean(1) for n in names}
import itertools
pairs = {}
for a, b in itertools.combinations(names, 2):
    r = float(np.corrcoef(mean_maps[a], mean_maps[b])[0, 1])
    pairs[f"{a}|{b}"] = r
    print(f"pearson({a},{b}) = {r:.4f}")
json.dump(pairs, open(f"{OUT}/separability.json", "w"), indent=1)
print("DONE")
