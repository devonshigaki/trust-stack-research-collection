"""SIM-P re-run: P1 (corrected coherence) + P1b (leakage-graded surface).
Conventions per sim_results_B.md Study 1: N=500, omega ~ Cauchy(0,1),
stereographic init theta = 2 arctan(eps_tilde), eps_tilde ~ Cauchy(0,1),
Euler dt=0.05, burn-in 100 t.u. + measurement 200 t.u.
Leakage: K_eff = K(1-l), observed phases theta_hat = theta + eta,
eta ~ N(0, (pi*l/2)^2) redrawn every timestep. Seed base 42.
"""
import numpy as np

N = 500
DT = 0.05
BURN = int(100 / DT)   # 2000 steps
MEAS = int(200 / DT)   # 4000 steps


def kuramoto_R(K, leak, seed, phase_map="stereo"):
    rng = np.random.default_rng(seed)
    omega = rng.standard_cauchy(N)
    eps = rng.standard_cauchy(N)
    if phase_map == "stereo":
        theta = 2.0 * np.arctan(eps)
    elif phase_map == "atan":
        theta = np.arctan(eps)
    elif phase_map == "uniform":
        theta = rng.uniform(-np.pi, np.pi, N)
    Keff = K * (1.0 - leak)
    sig_eta = 0.5 * np.pi * leak
    Rs = []
    for step in range(BURN + MEAS):
        th_obs = theta + (rng.normal(0.0, sig_eta, N) if sig_eta > 0 else 0.0)
        Z = np.exp(1j * th_obs).mean()
        theta = theta + DT * (omega + Keff * np.imag(Z * np.exp(-1j * theta)))
        if step >= BURN:
            Rs.append(np.abs(np.exp(1j * theta).mean()))
    return float(np.mean(Rs))


if __name__ == "__main__":
    # ---- P1: coupled vs isolated, 8 replicas ----
    reps = [42 + 1000 * i for i in range(8)]
    R_c = [kuramoto_R(4.5, 0.0, s) for s in reps]
    R_i = [kuramoto_R(0.0, 0.0, s) for s in reps]
    print("P1 coupled K=4.5 :", np.round(R_c, 4), "mean %.4f sd %.4f" % (np.mean(R_c), np.std(R_c, ddof=1)))
    print("P1 isolated K=0  :", np.round(R_i, 4), "mean %.4f sd %.4f" % (np.mean(R_i), np.std(R_i, ddof=1)))

    # ---- artifact: old atan map at K=0, 200-seed ensemble ----
    R_old = [kuramoto_R(0.0, 0.0, 7000 + i, "atan") for i in range(200)]
    R_new = [kuramoto_R(0.0, 0.0, 9000 + i, "stereo") for i in range(200)]
    R_uni = [kuramoto_R(0.0, 0.0, 11000 + i, "uniform") for i in range(200)]
    print("atan K=0   : %.4f ± %.4f" % (np.mean(R_old), np.std(R_old, ddof=1)))
    print("stereo K=0 : %.4f ± %.4f" % (np.mean(R_new), np.std(R_new, ddof=1)))
    print("uniform K=0: %.4f ± %.4f" % (np.mean(R_uni), np.std(R_uni, ddof=1)))
    np.savez("/mnt/agents/output/figures/tfp/p1_results.npz",
             R_c=R_c, R_i=R_i, R_old=R_old, R_new=R_new, R_uni=R_uni)
