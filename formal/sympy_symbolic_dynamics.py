#!/usr/bin/env python3
"""
Formal Symbolic Computer Algebra Verification of Trust Stack Dynamics
Engine: SymPy (Symbolic Python)
"""

import sys
import sympy as sp

def print_banner(title):
    print("=" * 70)
    print(f" SYMPY CAS VERIFICATION: {title}")
    print("=" * 70)

def verify_continuous_lyapunov():
    print_banner("Theorem 1: Continuous-Time Lyapunov Asymptotic Stability")
    print("Proving: Candidate Lyapunov function V(S) = (1/2)*(S - S*)^2 satisfies")
    print("dV/dt = -lambda * (S - S*)^2 < 0 for all lam > 0 and S != S*.\n")

    S, S_star = sp.symbols('S S_star', real=True)
    lam = sp.symbols('lam', positive=True)
    delta_s = sp.symbols('delta_s', real=True, nonzero=True)

    V = sp.Rational(1, 2) * (S - S_star)**2
    S_dot = -lam * (S - S_star)
    V_dot = sp.simplify(sp.diff(V, S) * S_dot)
    expected_V_dot = -lam * (S - S_star)**2

    is_identical = (sp.simplify(V_dot - expected_V_dot) == 0)
    universally_neg = bool(sp.ask(sp.Q.negative(V_dot.subs(S - S_star, delta_s))))
    print(f"Symbolic V(S)  = {V}")
    print(f"Symbolic dV/dt = {V_dot} (universal negative for lam>0, S!=S*: {universally_neg})")

    if is_identical and universally_neg:
        print("\n[VERIFIED] Universal symbolic dV/dt < 0 proven via sp.Q.negative without point substitution.")
        return True
    print("\n[FAILED] Verification failed.")
    return False

def verify_ornstein_uhlenbeck_tradeoff():
    print_banner("Theorem 2: Ornstein-Uhlenbeck Observation Drift Trade-off")
    print("Proving: Steady-state variance Sigma = sigma^2 / (2*(mu + psi(m)))")
    print("satisfies dSigma/dm = -sigma^2 * psi'(m) / (2*(mu + psi(m))^2) < 0 universally.\n")

    sigma, mu, m, psi_val, dpsi_dm = sp.symbols('sigma mu m psi_val dpsi_dm', positive=True)
    psi = sp.Function('psi')(m)

    Sigma = sigma**2 / (2 * (mu + psi))
    dSigma_dm = sp.simplify(sp.diff(Sigma, m))
    expected_form = -(sigma**2) * sp.Derivative(psi, m) / (2 * (mu + psi)**2)
    is_identical = (sp.simplify(dSigma_dm - expected_form) == 0)

    dSigma_sym = dSigma_dm.subs({sp.Derivative(psi, m): dpsi_dm, psi: psi_val})
    universally_neg = bool(sp.ask(sp.Q.negative(dSigma_sym)))

    print(f"Symbolic dSigma/dm = {dSigma_dm} (universal negative for positive sigma, mu, psi, psi': {universally_neg})")
    if is_identical and universally_neg:
        print("\n[VERIFIED] Universal analytical derivative < 0 proven symbolically.")
        return True
    print("\n[FAILED] Derivative verification failed.")
    return False

def verify_kuramoto_jacobian_spectrum():
    print_banner("Theorem 3: Kuramoto Synchronized Manifold Stability")
    print("Proving: Linearized Jacobian around phase-locked state (theta_i = theta_j)")
    print("has non-zero eigenvalues equal to -K, ensuring exponential phase-locking.\n")
    
    K = sp.symbols('K', real=True, positive=True)
    
    # 3-oscillator system around synchronized state theta_1 = theta_2 = theta_3 = 0
    # dot(theta_i) = omega_i + (K/N) sum_j sin(theta_j - theta_i)
    # J_ij = (K/N) * cos(theta_j - theta_i) = K/3 for i != j
    # J_ii = -(K/N) * sum_{j != i} cos(theta_j - theta_i) = -2*K/3
    
    J = sp.Matrix([
        [-2*K/3,   K/3,   K/3],
        [  K/3, -2*K/3,   K/3],
        [  K/3,   K/3, -2*K/3]
    ])
    
    print("Symbolic 3-Oscillator Jacobian Matrix J:")
    sp.pprint(J)
    
    eigenvals = J.eigenvals()
    print(f"\nSymbolic Eigenvalues & Multiplicities: {eigenvals}")
    
    # Expected: eigenvalue 0 with multiplicity 1 (phase shift symmetry)
    # and eigenvalue -K with multiplicity 2 (transversal contraction)
    has_zero = (0 in eigenvals) and (eigenvals[0] == 1)
    has_minus_K = (-K in eigenvals) and (eigenvals[-K] == 2)
    
    if has_zero and has_minus_K:
        print("\n[VERIFIED] Eigenvalues are exactly {0: 1, -K: N-1}.")
        print("=> Transversal contraction rate is strictly -K < 0.")
        print("=> The synchronized phase-locked manifold is exponentially stable.")
        return True
    else:
        print("\n[FAILED] Eigenvalue structure failed.")
        return False

def verify_monotone_optimism_gradient():
    print_banner("Theorem 4: Monotone Optimism of the Trust-Tilted Utility")
    print("Proving: d/diota EU(iota) = gamma * Var_P_tilde(U) > 0 universally for all iota in R, p_i > 0, u1 != u2.\n")

    u1, u2, iota = sp.symbols('u1 u2 iota', real=True)
    gamma, p1, p2, du = sp.symbols('gamma p1 p2 du', positive=True)

    w1 = p1 * sp.exp(gamma * iota * u1)
    w2 = p2 * sp.exp(gamma * iota * u2)
    Z = w1 + w2
    EU = (w1 * u1 + w2 * u2) / Z

    dEU_diota = sp.simplify(sp.diff(EU, iota))
    # Exact algebraic variance identity: gamma * p1 * p2 * exp(gamma*iota*(u1+u2)) * (u2 - u1)^2 / Z^2
    var_identity = gamma * w1 * w2 * (u2 - u1)**2 / (Z**2)
    is_identical = (sp.simplify(dEU_diota - var_identity) == 0)
    universally_pos = bool(sp.ask(sp.Q.positive(var_identity.subs(u2 - u1, du))))

    print(f"Symbolic dEU/diota = {dEU_diota}")
    print(f"Exact Var_P_tilde identity holds={is_identical}, universal positivity={universally_pos}")

    if is_identical and universally_pos:
        print("[VERIFIED] Trust-weighted utility is strictly increasing for all iota in R and non-uniform priors p1, p2 > 0.")
        return True
    print("\n[FAILED] Gradient positivity check failed.")
    return False

def main():
    print("\n" + "#" * 70)
    print(" STARTING SYMPY SYMBOLIC COMPUTER ALGEBRA VERIFICATION SUITE")
    print(" Research Suite: Trust Stack Dynamics")
    print("#" * 70 + "\n")
    
    results = [
        verify_continuous_lyapunov(),
        verify_ornstein_uhlenbeck_tradeoff(),
        verify_kuramoto_jacobian_spectrum(),
        verify_monotone_optimism_gradient()
    ]
    
    print("\n" + "=" * 70)
    print(f" SYMPY VERIFICATION SUMMARY: {sum(results)}/{len(results)} THEOREMS SYMBOLICALLY VERIFIED")
    print("=" * 70 + "\n")
    
    if all(results):
        print("VERDICT: ALL SYMBOLIC MATHEMATICAL CLAIMS VERIFIED.")
        return 0
    else:
        print("VERDICT: SYMPIC VERIFICATION FAILED.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
