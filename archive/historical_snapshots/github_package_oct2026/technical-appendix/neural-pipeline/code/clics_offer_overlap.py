"""DOCAS N.4: CLICS4 colexification overlap for the reconstructed offer battery.

- Extracts content-word vocabulary from battery27_reconstructed.json
  (lowercase, alpha tokens, minus a small embedded stopword list and the
  amount/number tokens that are crossed by design).
- Maps words -> Concepticon nodes via exact Concepticon_Gloss match
  (concepts.csv). Unmapped words are reported, not silently dropped.
- Builds the CLICS4 colexification graph from colexifications.csv
  (unfiltered: 51,562 edges / 1,730 concepts; see RUN_REPORT.md sec.6 for the
  paper's density inconsistency). Sensitivity: Family_Count>=3 subgraph.
- Defines five channel lexicons = per-category content words (union over the
  category's stimuli, minus words shared with >=2 other categories) plus a
  CONTROL lexicon.
- Computes shortest-path distances: for every mapped vocabulary node, the min
  graph distance to each channel lexicon; plus category-level mean distances.
Outputs: results/clics_offer_overlap_results.json, figure data table csv.
Reconstruction caveat: the paper's own channel-concept lists live in the absent
Supporting Document; these lexicons are derived from the reconstructed battery.
"""
import csv
import json
import sys

csv.field_size_limit(10_000_000)
import re
from collections import defaultdict

import networkx as nx
import numpy as np

BASE = "/tmp/tribe"
CLDF = "/tmp/clics4/cldf"

STOP = set("""a an and are as at be because been before but by can do does for
from has have if in into is it its may no not of on or our so than that the
their then there these this to up we will with without you your after once
""".split())
# numbers/amount tokens are crossed by design -> excluded from vocabulary
NUM = re.compile(r"^[\d,.$%]+$")

battery = json.load(open(f"{BASE}/battery27_reconstructed.json"))["stimuli"]


def content_words(text):
    toks = re.findall(r"[A-Za-z][a-z'-]*|\$?[\d,]+(?:\.\d+)?%?", text.lower())
    return [t for t in toks if t not in STOP and not NUM.match(t) and len(t) > 1]


cat_words = defaultdict(set)
for s in battery:
    cat_words[s["category"]] |= set(content_words(s["text"]))

VOCAB = sorted(set().union(*cat_words.values()))

# ---------- Concepticon mapping ----------
gloss2node = {}
node_meta = {}
with open(f"{CLDF}/concepts.csv") as f:
    for row in csv.DictReader(f):
        g = (row["Concepticon_Gloss"] or "").strip().lower()
        if g:
            gloss2node[g] = row["Concepticon_ID"]
            node_meta[row["Concepticon_ID"]] = row["Concepticon_Gloss"]

# Analyst synonym map for domain terms with no Concepticon gloss (documented
# judgment calls; Concepticon is basic vocabulary and lacks most finance terms).
SYNONYMS = {
    "payment": "pay", "payments": "pay", "repay": "pay", "repayment": "pay",
    "prepayment": "pay", "payoff": "pay", "wage": "pay", "wages": "pay",
    "fee": "price", "fees": "price", "charge": "price", "charges": "price",
    "cost": "price", "cash": "money", "dollar": "money", "dollars": "money",
    "bills": "bill", "loan": "borrow", "credit": "lend", "balance": "debt",
    "penalty": "punishment", "garnishment": "seize", "levy": "seize",
    "seizure": "seize", "lawsuit": "court", "legal": "law",
    "proceedings": "court", "damage": "destroy", "harm": "bad",
    "hidden": "secret", "private": "secret", "guarantee": "promise",
    "guaranteed": "promise", "trust": "truth", "disclose": "show",
    "disclosed": "show", "report": "tell", "progress": "grow",
    "expires": "finish", "ends": "finish", "closes": "finish",
    "tonight": "night", "midnight": "night", "weekdays": "week",
    "weekends": "week", "community": "people", "members": "people",
    "library": "book", "books": "book", "rooms": "room", "plots": "land",
    "shed": "house", "reserve": "keep", "stored": "keep",
    "prohibited": "forbid", "introductory": "first", "little": "small",
    "page": "paper",
}


def morph_candidates(w):
    c = [w]
    if w.endswith("ies"):
        c.append(w[:-3] + "y")
    if w.endswith("es"):
        c.append(w[:-2])
    if w.endswith("s"):
        c.append(w[:-1])
    if w.endswith("ing"):
        c.append(w[:-3])
    if w.endswith("ed"):
        c.append(w[:-2])
    return c


mapped, unmapped, map_tier = {}, [], {}
for w in VOCAB:
    hit = None
    if w in gloss2node:
        hit, tier = w, "exact"
    else:
        for c in morph_candidates(w)[1:]:
            if c in gloss2node:
                hit, tier = c, "morphological"
                break
        if hit is None and w in SYNONYMS and SYNONYMS[w] in gloss2node:
            hit, tier = SYNONYMS[w], "synonym"
    if hit:
        mapped[w] = gloss2node[hit]
        map_tier[w] = f"{tier}:{hit}"
    else:
        unmapped.append(w)

# ---------- graph ----------
def build_graph(min_family=1):
    G = nx.Graph()
    g2id = gloss2node
    with open(f"{CLDF}/colexifications.csv") as f:
        for row in csv.DictReader(f):
            if int(row["Family_Count"]) < min_family:
                continue
            a = g2id.get(row["Source_Concept"].strip().lower())
            b = g2id.get(row["Target_Concept"].strip().lower())
            if a and b and a != b:
                G.add_edge(a, b)
    return G

G_full = build_graph(1)
G_fam3 = build_graph(3)

# ---------- channel lexicons ----------
cats = ["FAIR", "PREDATORY", "TEASER", "TRUST_SIGNAL", "THREAT", "CONTROL"]
lexicons = {}
for c in cats:
    others = set().union(*[cat_words[o] for o in cats if o != c])
    lex = {w for w in cat_words[c] if sum(w in cat_words[o] for o in cats if o != c) <= 1}
    lexicons[c] = {w: mapped[w] for w in lex if w in mapped}

# ---------- distances ----------
def dist_table(G):
    lex_nodes = {c: set(lx.values()) & set(G.nodes) for c, lx in lexicons.items()}
    table = {}
    for w, node in mapped.items():
        if node not in G:
            continue
        lengths = nx.single_source_shortest_path_length(G, node)
        row = {}
        for c in cats:
            d = min((lengths[n] for n in lex_nodes[c] if n in lengths), default=None)
            row[c] = d
        table[w] = row
    return table

dist_full = dist_table(G_full)
dist_fam3 = dist_table(G_fam3)

def category_means(table):
    out = {}
    for cat in cats:
        words = [w for w in cat_words[cat] if w in table]
        row = {}
        for ch in cats:
            ds = [table[w][ch] for w in words if table[w][ch] is not None]
            row[ch] = float(np.mean(ds)) if ds else None
        out[cat] = row
    return out

res = {
    "_provenance": "reconstruction-from-spec battery; CLICS4 real data (clics/clics4 CLDF)",
    "graph": {
        "full": {"nodes": G_full.number_of_nodes(), "edges": G_full.number_of_edges(),
                 "density": nx.density(G_full)},
        "family_ge3": {"nodes": G_fam3.number_of_nodes(), "edges": G_fam3.number_of_edges(),
                       "density": nx.density(G_fam3)},
    },
    "vocabulary": {"n_content_words": len(VOCAB), "n_mapped": len(mapped),
                   "n_unmapped": len(unmapped), "unmapped": unmapped,
                   "mapping_tiers": map_tier},
    "lexicons": {c: sorted(lx) for c, lx in lexicons.items()},
    "word_channel_distances_full": dist_full,
    "word_channel_distances_family_ge3": dist_fam3,
    "category_mean_distances_full": category_means(dist_full),
    "category_mean_distances_family_ge3": category_means(dist_fam3),
}
json.dump(res, open(f"{BASE}/results/clics_offer_overlap_results.json", "w"), indent=1)

print("graph full:", res["graph"]["full"])
print("graph fam>=3:", res["graph"]["family_ge3"])
print(f"vocab {len(VOCAB)} mapped {len(mapped)} unmapped {len(unmapped)}")
print("unmapped:", unmapped)
print("\ncategory mean distances (full graph):")
hdr = "from\\to      " + "".join(f"{c[:9]:>10}" for c in cats)
print(hdr)
for cat in cats:
    row = res["category_mean_distances_full"][cat]
    print(f"{cat[:12]:<13}" + "".join(f"{row[c]:>10.2f}" if row[c] is not None else f"{'--':>10}" for c in cats))
