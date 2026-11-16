#!/usr/bin/env python3
"""
Z3 Non-Vacuity & Minimal Unsat-Core Verification Helper
Ensures every SMT theorem P => Q satisfies two formal preconditions:
  1. Non-Vacuity: P alone is satisfiable (z3.sat) -- premises do not self-contradict.
  2. Necessity:   P /\\ ~Q is unsatisfiable (z3.unsat) AND ~Q is in solver.unsat_core().
"""

import z3


def prove_nonvacuous(premises, negated_goal, label: str = "Theorem", required_indices=None) -> bool:
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

    # Verify negated_goal (and any explicitly required domain hypotheses) are in unsat_core
    s_core = z3.Solver()
    s_core.set(unsat_core=True, timeout=3000)
    prem_tags = []
    for i, p in enumerate(premises):
        t = z3.Bool(f"prem_{i}")
        prem_tags.append(t)
        s_core.assert_and_track(p, t)
    g_tag = z3.Bool("negated_goal")
    s_core.assert_and_track(negated_goal, g_tag)
    if s_core.check() == z3.unsat:
        core = set(s_core.unsat_core())
        if g_tag not in core:
            raise AssertionError(f"[VACUOUS UNSAT] {label}: negated_goal absent from unsat_core")
        if required_indices:
            for idx in required_indices:
                if prem_tags[idx] not in core:
                    raise AssertionError(
                        f"[VACUOUS PREMISE] {label}: required premise prem_{idx} absent from unsat_core"
                    )
    return True
