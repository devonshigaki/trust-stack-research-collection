"""Stream Connectivity_783.parquet -> compact int32/float32 npz (RAM-safe)."""
import numpy as np, pyarrow.parquet as pq, resource, time

t0 = time.time()
pf = pq.ParquetFile('/tmp/Drosophila_brain_model-main/Connectivity_783.parquet')
i_l, j_l, w_l = [], [], []
for batch in pf.iter_batches(batch_size=2_000_000,
                             columns=['Presynaptic_Index', 'Postsynaptic_Index',
                                      'Excitatory x Connectivity']):
    d = batch.to_pydict()
    i_l.append(np.asarray(d['Presynaptic_Index'], dtype=np.int32))
    j_l.append(np.asarray(d['Postsynaptic_Index'], dtype=np.int32))
    w_l.append(np.asarray(d['Excitatory x Connectivity'], dtype=np.float32))
i = np.concatenate(i_l); j = np.concatenate(j_l); w = np.concatenate(w_l)
np.savez('/tmp/graph783.npz', i=i, j=j, w=w)
print('edges:', len(i), '| nnz weight:', int((w != 0).sum()),
      '| min/max w:', w.min(), w.max())
print(f'{time.time()-t0:.0f}s | peak RSS MB:',
      resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024)
