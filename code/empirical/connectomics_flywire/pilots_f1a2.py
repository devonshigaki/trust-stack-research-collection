import importlib.util, numpy as np
spec = importlib.util.spec_from_file_location('f1','/tmp/run_f1a.py')
f1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f1)
from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, Hz
P = f1.P
DL3PN = np.array([k for k in f1.POPS['uniPN']], dtype=np.int64)
# identify DL3 PNs: uniPNs that receive ORN_DL3 input
m = np.isin(f1.li, f1.ORN) & np.isin(f1.lj, f1.POPS['uniPN'])
DL3PN = np.unique(f1.lj[m])
print('DL3-receiving PNs:', len(DL3PN), flush=True)

def pilot(drive_pop, label, readouts):
    neu = NeuronGroup(f1.N, model=P['eqs'], method='linear', threshold=P['eq_th'],
                      reset=P['eq_rst'], refractory='rfc', namespace=P)
    neu.v = P['v_0']; neu.g = 0; neu.rfc = P['t_rfc']
    syn = Synapses(neu, neu, 'w : volt', on_pre='g += w', delay=P['t_dly'])
    syn.connect(i=f1.li, j=f1.lj); syn.w = f1.lw * P['w_syn']
    spk = SpikeMonitor(neu)
    pg = PoissonGroup(len(drive_pop), rates=150*Hz)
    s_in = Synapses(pg, neu, on_pre='v += wd', namespace={'wd': P['w_syn']*P['f_poi']})
    s_in.connect(i=np.arange(len(drive_pop)), j=drive_pop)
    for k in drive_pop: neu[k].rfc = 0*ms
    net = Network(neu, syn, spk, pg, s_in)
    net.run(1000*ms)
    tr = spk.spike_trains()
    out = [label]
    for nm, pop in readouts:
        cnts = np.array([len(tr.get(int(k),[])) for k in pop])
        out.append(f'{nm} {int((cnts>0).sum())}/{len(pop)} act mean{cnts.mean():.1f}Hz')
    print(' | '.join(out), flush=True)

pilot(DL3PN, 'A: drive DL3 PNs direct', [('KC', f1.KC), ('MBON', f1.MBON)])
pilot(f1.POPS['uniPN'], 'B: drive all 264 PNs', [('KC', f1.KC), ('MBON', f1.MBON)])
pilot(f1.POPS['sugar'], 'C: drive 20 sugar GRNs', [('OA', f1.OA), ('PAM', f1.PAM), ('MBON', f1.MBON)])
