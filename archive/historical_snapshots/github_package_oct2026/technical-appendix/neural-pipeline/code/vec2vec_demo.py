"""DOCAS N-bridge: vec2vec (rjha18/vec2vec) with REAL released pretrained
translator weights (v1.0.0, final_model_release.zip, 1,162,524,881 B).

What this script does:
- Loads the released gte<->gtr translator (gte_gtr/model.pt) with the repo's
  own builder (utils.load_n_translator + config.toml), strict=False as in
  eval.py.
- Embeds the 27 reconstructed battery texts with the REAL encoders
  (thenlper/gte-base and sentence-transformers/gtr-t5-base, via hf-mirror,
  normalized embeddings as in the training config).
- Translates gte -> gtr and reports reconstruction metrics: cosine similarity
  to the true gtr embedding, and top-1 retrieval of the correct text's gtr
  embedding among all 27 (plus a shuffled control).

What this does NOT do (honest scope): no released pair includes LLaMA-3.2-3B
hidden states or the eng1000 space, so the DOCAS-specific bridge
(LLaMA text features <-> Gallant/eng1000 semantics) still requires TRAINING a
new translator. Exact training command is printed at the end and recorded in
the results JSON as TRAINING-REQUIRED.
"""
import json
import os
import sys
from types import SimpleNamespace

import numpy as np
import torch

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["TOKENIZERS_PARALLELISM"] = "0"

V2V = "/tmp/vec2vec"
sys.path.insert(0, V2V)
# vec2text is only needed for inversion models (not translation); stub it out
import types
for m in ("vec2text", "vec2text.models"):
    sys.modules[m] = types.ModuleType(m)
sys.modules["vec2text.models"].InversionModel = object
import toml
from utils.utils import load_n_translator

BASE = "/tmp/tribe"
MODELDIR = f"{BASE}/vec2vec_models/final_model_release/gte_gtr"

cfg = SimpleNamespace(**toml.load(f"{MODELDIR}/config.toml"))
translator = load_n_translator(cfg, {"gte": 768, "gtr": 768})
sd = torch.load(f"{MODELDIR}/model.pt", map_location="cpu")
missing, unexpected = translator.load_state_dict(sd, strict=False)
translator.eval()
print(f"translator loaded: missing={len(missing)} unexpected={len(unexpected)}")

battery = json.load(open(f"{BASE}/battery27_reconstructed.json"))["stimuli"]
texts = [s["text"] for s in battery]
ids = [s["id"] for s in battery]

embs = {}
for flag, mname in [("gte", "thenlper/gte-base"),
                    ("gtr", "sentence-transformers/gtr-t5-base")]:
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer(mname, device="cpu")
    e = enc.encode(texts, normalize_embeddings=True, convert_to_numpy=True,
                   batch_size=8, show_progress_bar=False)
    embs[flag] = torch.tensor(e, dtype=torch.float32)
    print(flag, mname, e.shape, flush=True)
    del enc

with torch.no_grad():
    trans = translator.translate_embeddings(embs["gte"], "gte", "gtr")

tgt = embs["gtr"]
cos = torch.nn.functional.cosine_similarity(trans, tgt, dim=1).numpy()
sim = (trans @ tgt.T).numpy()  # both normalized
ranks = np.array([int(np.sum(sim[i] > sim[i, i]) + 1) for i in range(len(ids))])

rng = np.random.default_rng(20260905)
null_top1 = []
for _ in range(2000):
    pp = rng.permutation(len(ids))
    null_top1.append(float(np.mean(np.argmax(sim[pp], axis=1) == np.arange(len(ids)))))

res = {
    "_scope": ("vec2vec released gte->gtr translator on the reconstructed "
               "battery27 texts; NOT the DOCAS LLaMA<->eng1000 bridge"),
    "weights": "vec2vec v1.0.0 final_model_release/gte_gtr/model.pt (real)",
    "state_dict_load": {"missing": missing, "unexpected": unexpected},
    "gte_to_gtr_cosine": {"mean": float(cos.mean()), "min": float(cos.min()),
                          "max": float(cos.max())},
    "retrieval_top1_of_27": float(np.mean(ranks == 1)),
    "retrieval_mean_rank": float(ranks.mean()),
    "null_top1_mean": float(np.mean(null_top1)),
    "chance_top1": 1 / len(ids),
    "per_text": {i: {"cos": float(c), "rank": int(r)}
                 for i, c, r in zip(ids, cos, ranks)},
    "docas_bridge_status": "TRAINING-REQUIRED",
    "docas_bridge_training_command": (
        "python train.py configs/unsupervised.toml "
        "--unsup_emb <llama_hidden_extractor> --sup_emb <eng1000_extractor> "
        "--num_points 1000000 --epochs 2000  # GPU-scale; see vec2vec README: "
        "'GAN training is very unstable; try multiple seeds'. No released "
        "checkpoint covers LLaMA-3.2-3B hidden states or eng1000."),
}
json.dump(res, open(f"{BASE}/results/vec2vec_bridge_results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items()
                  if k not in ("per_text", "state_dict_load")}, indent=1))
