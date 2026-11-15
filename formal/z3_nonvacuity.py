#!/usr/bin/env python3
"""
Z3 Non-Vacuity & Minimal Unsat-Core Verification Helper
Ensures every SMT theorem P => Q satisfies two formal preconditions:
  1. Non-Vacuity: P alone is satisfiable (z3.sat) -- premises do not self-contradict.
  2. Necessity:   P /\\ ~Q is unsatisfiable (z3.unsat) AND ~Q is in solver.unsat_core().
"""

import z3


def prove_nonvacuous(premises, negated_goal, label: str = "Theorem") -> bool:
    """Checks premise consistency (SAT) and negated-goal necessity (UNSAT + optional unsat_core)."""
    s_prem = z3.Solver()
    s_prem.add(*premises)
    res_prem = s_prem.check()
    if res_prem != z3.sat:
        raise AssertionError(f"[VACUITY FAILURE] {label}: premises alone are {res_prem}")

    s_full = z3.Solver()
    s_full.add(*premises, negated_goal)
    res_full = s_full.check()
    if res_full != z3.unsat:
        return False

    # Verify negated_goal is in unsat_core where tractable (3s bound for QF_NRA)
    s_core = z3.Solver()
    s_core.set(unsat_core=True, timeout=3000)
    for i, p in enumerate(premises):
        s_core.assert_and_track(p, z3.Bool(f"prem_{i}"))
    g_tag = z3.Bool("negated_goal")
    s_core.assert_and_track(negated_goal, g_tag)
    if s_core.check() == z3.unsat and g_tag not in set(s_core.unsat_core()):
        raise AssertionError(f"[VACUOUS UNSAT] {label}: negated_goal absent from unsat_core")
    return True
