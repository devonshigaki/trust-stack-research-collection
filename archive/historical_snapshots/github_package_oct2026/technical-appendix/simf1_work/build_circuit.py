"""Extract frozen F1a circuit from v783: populations per Design Addendum A,
induced subgraph, local index remap, plastic-synapse (KC->MBON) map."""
import json
import numpy as np
import pandas as pd

REPO = '/tmp/Drosophila_brain_model-main'
ANN = '/tmp/flywire_annotations-main/supplemental_files/Supplemental_file1_neuron_annotations.tsv'
OUT = '/mnt/agents/output/simf1_work'

comp = pd.read_csv(f'{REPO}/Completeness_783.csv', index_col=0)
roster = comp.index.to_numpy()
in_roster = set(roster.tolist())

ann = pd.read_csv(ANN, sep='\t', low_memory=False,
                  usecols=['root_id', 'cell_class', 'cell_type'])
ann = ann[ann.root_id.isin(in_roster)]

ct = ann.cell_type.fillna('')
cc = ann.cell_class.fillna('')
pops = {
    'ORN_DL3': ann[ct == 'ORN_DL3'].root_id.to_numpy(),
    'uniPN':   ann[ct.str.contains('_adPN|_lPN', regex=True)].root_id.to_numpy(),
    'KC':      ann[cc == 'Kenyon_Cell'].root_id.to_numpy(),
    'MBON':    ann[ct.str.match(r'^MBON')].root_id.to_numpy(),
    'PPL1':    ann[ct.str.match(r'^PPL1')].root_id.to_numpy(),
    'PAM':     ann[ct.str.match(r'^PAM')].root_id.to_numpy(),
    'OA':      ann[ct.str.match(r'^OA-')].root_id.to_numpy(),
    'APL':     ann[ct == 'APL'].root_id.to_numpy(),
    'DPM':     ann[ct == 'DPM'].root_id.to_numpy(),
}
SUGAR = [720575940624963786,720575940630233916,720575940637568838,720575940638202345,
         720575940617000768,720575940630797113,720575940632889389,720575940621754367,
         720575940621502051,720575940640649691,720575940639332736,720575940616885538,
         720575940639198653,720575940620900446,720575940617937543,720575940632425919,
         720575940633143833,720575940612670570,720575940628853239,720575940629176663,
         720575940611875570]
pops['sugar'] = np.array([s for s in SUGAR if s in in_roster])

counts = {k: int(len(v)) for k, v in pops.items()}
print('population counts (in v783):', counts)

circuit_ids = np.unique(np.concatenate(list(pops.values())))
cid_set = set(circuit_ids.tolist())
print('circuit neurons:', len(circuit_ids))

g = np.load('/tmp/graph783.npz')
ei, ej, ew = g['i'], g['j'], g['w']
pre_root = roster[ei]; post_root = roster[ej]
mask = np.isin(pre_root, circuit_ids) & np.isin(post_root, circuit_ids)
ci_pre, ci_post, ci_w = pre_root[mask], post_root[mask], ew[mask]
print('circuit edges:', int(mask.sum()))

local = {r: k for k, r in enumerate(circuit_ids.tolist())}
li = np.array([local[r] for r in ci_pre], dtype=np.int32)
lj = np.array([local[r] for r in ci_post], dtype=np.int32)

pop_local = {k: np.array([local[r] for r in v], dtype=np.int32)
             for k, v in pops.items()}

# plastic synapses: KC -> MBON
kc_set = set(pops['KC'].tolist()); mbon_set = set(pops['MBON'].tolist())
plastic_mask = np.isin(ci_pre, list(kc_set)) & np.isin(ci_post, list(mbon_set))
plastic_edges = np.where(plastic_mask)[0].astype(np.int64)
print('KC->MBON plastic edges:', len(plastic_edges))
# group plastic edge positions by presynaptic KC local index
kc_to_edges = {}
for e in plastic_edges:
    kc_to_edges.setdefault(int(li[e]), []).append(int(e))

np.savez('/tmp/circuit_f1.npz', i=li, j=lj, w=ci_w,
         roots=circuit_ids, plastic_edges=plastic_edges)
with open('/tmp/kc_to_edges.json', 'w') as f:
    json.dump(kc_to_edges, f)
with open(f'{OUT}/circuit_f1_populations.json', 'w') as f:
    json.dump({'counts': counts, 'circuit_size': int(len(circuit_ids)),
               'circuit_edges': int(len(li)),
               'plastic_edges_kc_mbon': int(len(plastic_edges)),
               'pop_root_ids': {k: [int(x) for x in v] for k, v in pops.items()}},
              f, indent=1)
np.savez('/tmp/circuit_pops.npz', **pop_local)
print('saved circuit_f1.npz, circuit_pops.npz, kc_to_edges.json')
