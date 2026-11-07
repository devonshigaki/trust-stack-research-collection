"""Fly reference for Sim H1 (descriptive, registration section 5):
KC->MBON share of MBON input budget in FlyWire v783 (whole brain, Shiu repo
tables), plus full class composition of MBON inputs. One streaming pass."""
import json, time
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = '/tmp/Drosophila_brain_model-main'
ANN = '/tmp/ann.tsv'
OUT = '/mnt/agents/output/simh1_work/fly_mbon_budget.json'

comp = pd.read_csv(f'{REPO}/Completeness_783.csv', index_col=0)
roster = comp.index.to_numpy()
in_roster = set(roster.tolist())

ann = pd.read_csv(ANN, sep='\t', low_memory=False,
                  usecols=['root_id', 'cell_class', 'cell_type'])
ann = ann[ann.root_id.isin(in_roster)]
root2class = dict(zip(ann.root_id, ann.cell_class.fillna('unannotated')))
root2type = dict(zip(ann.root_id, ann.cell_type.fillna('')))
mbon = set(ann[ann.cell_type.fillna('').str.match(r'^MBON')].root_id.tolist())
kc = set(ann[ann.cell_class == 'Kenyon_Cell'].root_id.tolist())

# map roster index -> class for fast lookup during streaming
cls_arr = np.array([root2class.get(int(r), 'unannotated') for r in roster])
idx_mbon = set(np.where(np.isin(roster, list(mbon)))[0].tolist())

tot_by_class = {}
tot = 0.0
t0 = time.time()
pf = pq.ParquetFile(f'{REPO}/Connectivity_783.parquet')
for batch in pf.iter_batches(batch_size=2_000_000,
                             columns=['Presynaptic_Index', 'Postsynaptic_Index',
                                      'Excitatory x Connectivity']):
    d = batch.to_pydict()
    i = np.asarray(d['Presynaptic_Index']); j = np.asarray(d['Postsynaptic_Index'])
    w = np.asarray(d['Excitatory x Connectivity'], dtype=np.float64)
    m = np.isin(j, list(idx_mbon))
    if not m.any():
        continue
    for cls in np.unique(cls_arr[i[m]]):
        sel = m & (cls_arr[i] == cls)
        tot_by_class[cls] = tot_by_class.get(cls, 0.0) + float(w[sel].sum())
    tot += float(w[m].sum())

share = {k: v / tot for k, v in sorted(tot_by_class.items(), key=lambda x: -x[1])}
res = {'substrate': 'FlyWire v783 whole brain (Shiu repo Connectivity_783.parquet)',
       'mbon_cells': len(mbon), 'kc_cells': len(kc),
       'total_synapse_weight_onto_MBON': tot,
       'class_composition_of_MBON_input': share,
       'KC_share_of_MBON_input_budget': share.get('Kenyon_Cell', 0.0),
       'wall_s': round(time.time() - t0, 1)}
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res, indent=1)[:1500])
print('DONE_MARKER')
