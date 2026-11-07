# Battery 4 — sparse/weighted-network Kuramoto sensitivity (SIM-R2, seed 42)
# Reference protocol (Sim-B Study 1): N=500, omega~Cauchy(0,1), theta0 = 2 arctan(Cauchy(0,1)),
# Euler dt=0.05, burn-in 100 t.u. + measurement 200 t.u., K grid 0..8 (17 pts), seeds 42/1042.
# Networks: all-to-all; ER G(N,p) p in {0.05,0.1,0.2,0.5}; Barabasi-Albert m=2 and m=12;
# weighted all-to-all with symmetric log-normal(0,0.5) weights rescaled to mean 1.
# Coupling: dth_i = omega_i + (K/k_i) * sum_j A_ij sin(th_j - th_i)  (degree-normalized, K comparable
# across topologies). R = time-mean of |mean(e^{i th})| over the measurement window.
# Implementation: all K values and both omega seeds batched as rows; dense matmul per step.
import numpy as np, json, time

N = 500
dt = 0.05
burn_steps, meas_steps = 2000, 4000
Ks = np.linspace(0, 8, 17)
seeds = [42, 1042]

def er_graph(n, p, r):
    A = np.triu(r.random((n, n)) < p, 1); A = A + A.T
    return A.astype(float)

def ba_graph(n, m, r):
    A = np.zeros((n, n))
    for i in range(m+1):
        for j in range(i+1, m+1): A[i, j] = A[j, i] = 1.0
    deg = A.sum(1)
    for new in range(m+1, n):
        probs = deg[:new]/deg[:new].sum()
        for t in r.choice(new, size=m, replace=False, p=probs): A[new, t] = A[t, new] = 1.0
        deg = A.sum(1)
    return A

def rownorm(A):
    d = A.sum(1); d[d == 0] = 1.0
    return A/d[:, None]

def run_block(An, Om, Th0):
    # Om, Th0: (B, N); Ks column-batched
    B = Om.shape[0]
    Th = np.tile(Th0, (len(Ks), 1))          # (len(Ks)*B? no:) -> handle: we batch (K x seed) jointly
    return None

t0 = time.time()
# batch rows: for each omega seed s -> 17 rows (one per K)
om = {s: np.random.default_rng(s).standard_cauchy(N) for s in seeds}
th0 = {s: 2*np.arctan(np.random.default_rng(s+7).standard_cauchy(N)) for s in seeds}
B = len(Ks)*len(seeds)
OM = np.array([om[s] for k in Ks for s in seeds])                            # (34, N)
TH0 = np.array([th0[s] for k in Ks for s in seeds])                          # (34, N)
KVEC = np.array([[k] for k in Ks for s in seeds])                            # (34,1)

def run(An):
    Th = TH0.copy()
    for _ in range(burn_steps):
        C, S = np.cos(Th), np.sin(Th)
        Zr, Zi = C @ An.T, S @ An.T
        Th += dt*(OM + KVEC*(Zi*C - Zr*S))
        Th = (Th+np.pi) % (2*np.pi) - np.pi
    acc = np.zeros(Th.shape[0])
    for _ in range(meas_steps):
        C, S = np.cos(Th), np.sin(Th)
        Zr, Zi = C @ An.T, S @ An.T
        Th += dt*(OM + KVEC*(Zi*C - Zr*S))
        Zm = np.exp(1j*Th).mean(1)
        acc += np.abs(Zm)
    R = acc/meas_steps                       # (34,)
    out = {}
    for i, k in enumerate(Ks):
        out[float(k)] = [float(R[i*len(seeds)+j]) for j in range(len(seeds))]
    return out

results = {}
for gseed in seeds:
    r = np.random.default_rng(gseed)
    W = np.triu(r.lognormal(0, 0.5, (N, N)), 1); W = W + W.T; W = W/W.mean()
    graphs = {
        'alltoall': np.ones((N, N))-np.eye(N),
        'ER_p0.05': er_graph(N, 0.05, r), 'ER_p0.10': er_graph(N, 0.10, r),
        'ER_p0.20': er_graph(N, 0.20, r), 'ER_p0.50': er_graph(N, 0.50, r),
        'BA_m2': ba_graph(N, 2, r), 'BA_m12': ba_graph(N, 12, r),
        'weighted_lognorm': W,
    }
    for name, A in graphs.items():
        meandeg = A.sum(1).mean()
        res = run(rownorm(A))
        results.setdefault(name, {})[f'g{gseed}'] = {'meandeg': float(meandeg), 'R': res}
        r45 = res[4.5]
        print(f"{name} g{gseed} meandeg={meandeg:.1f} R(K=4.5)={r45} ({time.time()-t0:.0f}s)", flush=True)

json.dump({'Ks': Ks.tolist(), 'results': results},
          open('/mnt/agents/output/figures/robustness/b4_results.json', 'w'))
print("ALL DONE", time.time()-t0)
