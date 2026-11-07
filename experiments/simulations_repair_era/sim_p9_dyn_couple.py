import numpy as np
import json
import time
import networkx as nx

def er_graph(n, p, seed):
    r = np.random.default_rng(seed)
    A = np.triu(r.random((n, n)) < p, 1)
    A = A + A.T
    return A.astype(float)

def rownorm(A):
    d = A.sum(1)
    d[d == 0] = 1.0
    return A / d[:, None]

def run_dyn_couple():
    N = 500
    K = 4.5
    dt = 0.05
    burn_steps = 2000
    meas_steps = 4000
    
    seed = 42
    r = np.random.default_rng(seed)
    
    # Sparse graph (ER p=0.05, mean deg ~25)
    A = er_graph(N, 0.05, seed)
    An = rownorm(A)
    
    # Master law params
    lambda_param = 0.35
    
    # Master Law state initialization
    S = r.uniform(0.2, 0.8, N)
    E = S.copy()
    
    # Initialize phases via stereographic projection of initial mismatch
    initial_eps = r.standard_cauchy(N)
    Th_dyn = 2 * np.arctan(initial_eps)
    
    acc = 0.0
    
    # Burn-in
    for t in range(burn_steps):
        # Validation event (Cauchy noise)
        V = E + r.standard_cauchy(N)
        eps = V - E
        dS = lambda_param * eps
        S = S + dS * dt
        E = S
        
        # Coupled natural frequency
        OM = dS
        
        C, Sin = np.cos(Th_dyn), np.sin(Th_dyn)
        Zr, Zi = C @ An.T, Sin @ An.T
        Th_dyn += dt * (OM + K * (Zi * C - Zr * Sin))
        Th_dyn = (Th_dyn + np.pi) % (2 * np.pi) - np.pi

    # Measurement
    for t in range(meas_steps):
        V = E + r.standard_cauchy(N)
        eps = V - E
        dS = lambda_param * eps
        S = S + dS * dt
        E = S
        
        OM = dS
        
        C, Sin = np.cos(Th_dyn), np.sin(Th_dyn)
        Zr, Zi = C @ An.T, Sin @ An.T
        Th_dyn += dt * (OM + K * (Zi * C - Zr * Sin))
        Th_dyn = (Th_dyn + np.pi) % (2 * np.pi) - np.pi
        
        Zm = np.exp(1j * Th_dyn).mean()
        acc += np.abs(Zm)
        
    R = acc / meas_steps
    return R

if __name__ == "__main__":
    R_dyn = run_dyn_couple()
    print(f"Dynamic Coupling R: {R_dyn:.3f}")
