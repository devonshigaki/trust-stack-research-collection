#!/usr/bin/env python3
"""
Manuscript Version, Bibliography, & Portable-Path Integrity Linter
Verifies:
1. Uniform Version 4.5 headers across all 6 *.tex and *.md manuscripts.
2. Zero placeholder DOIs ('OSF.IO/TBD') and zero un-retracted Brain-IT metrics ('0.7723').
3. Complete bibliography inclusion (\\nocite{*} + \\bibliography) across all BibTeX-backed *.tex manuscripts.
4. Zero personal machine paths (/Users/...) or deleted experiments/ paths in code/, formal/, figures/ Python scripts.
"""

import json
import os
import pathlib
import re
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
MANUSCRIPTS_DIR = os.path.join(BASE_DIR, "manuscripts")
TEX_FILES = [
    "collection/collection.tex",
    "value_of_trust/value_of_trust.tex",
    "gtt/gtt.tex",
    "tdf/tdf.tex",
    "tfp/tfp.tex",
    "whitepaper/whitepaper.tex",
]
BIBTEX_TEX = [
    "gtt/gtt.tex",
    "tdf/tdf.tex",
    "tfp/tfp.tex",
    "whitepaper/whitepaper.tex",
]
MD_HEADER_FILES = [
    "collection/collection.md",
    "value_of_trust/value_of_trust.md",
]
ALL_MD_FILES = [
    "collection/collection.md",
    "value_of_trust/value_of_trust.md",
    "gtt/gtt.md",
    "tdf/tdf.md",
    "tfp/tfp.md",
    "whitepaper/whitepaper.md",
]


def main():
    print("=" * 75)
    print("MANUSCRIPT VERSION, BIBLIOGRAPHY & PORTABLE-PATH AUDIT")
    print("=" * 75)
    errors = []
    for fn in TEX_FILES:
        base = os.path.basename(fn)
        path = os.path.join(MANUSCRIPTS_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        if "Version 4.5 --- November 2026" not in txt:
            errors.append(f"{fn}: Missing 'Version 4.5 --- November 2026' marker")
        if "OSF.IO/TBD" in txt:
            errors.append(f"{fn}: Contains placeholder 'OSF.IO/TBD'")
        if base == "tdf.tex" and "0.7723" in txt:
            errors.append(f"{fn}: Still contains withdrawn leaked Brain-IT metric 0.7723")
        if base in ("gtt.tex", "tdf.tex", "tfp.tex", "value_of_trust.tex") and "Supporting Document and Technical Appendix are in preparation" in txt:
            errors.append(f"{fn}: Contains stale 'Supporting Document and Technical Appendix are in preparation' disclaimer")
        if base in ("gtt.tex", "tdf.tex", "tfp.tex", "value_of_trust.tex"):
            brand_re = re.compile(r"\b(?:freshcredit|turso|plaid|stripe|entra|coinbase)\b", re.IGNORECASE)
            m_brand = brand_re.search(txt)
            if m_brand:
                errors.append(f"{fn}: Academic clean-room violation — commercial brand '{m_brand.group(0)}' is forbidden outside whitepaper")
        if base == "gtt.tex" and ("v4.12.0" in txt or "36 theorems" not in txt):
            errors.append(f"{fn}: Lean formalization section out of sync with Lean 4.35.0 (36 theorems)")
        if base == "whitepaper.tex" and ("OpenML 42477" not in txt or "Sim W8" not in txt or "Sim W9" not in txt):
            errors.append(f"{fn}: Missing OpenML 42477 or Sim W8/W9 parity coverage")
        if base == "tfp.tex" and ("ZK-STP v8" not in txt or "4{,}748{,}555" not in txt or "24/24" not in txt):
            errors.append(f"{fn}: Missing ZK-STP v8 (24/24) or TLA+ 4,748,555-distinct-state verification coverage")
        if fn in BIBTEX_TEX and "\\nocite{*}" not in txt:
            errors.append(f"{fn}: Missing \\nocite{{*}} (silently drops plain-text .bib references)")
        print(f"  ✓ Checked {fn}")

    for fn in ALL_MD_FILES:
        path = os.path.join(MANUSCRIPTS_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        if fn in MD_HEADER_FILES and "Version 4.5 — November 2026" not in txt:
            errors.append(f"{fn}: Missing 'Version 4.5 — November 2026' header")
        for stale in ("Release v4.3", "releases/tag/v4.3", "1,343 verified assets", "26-task", "24-task"):
            if stale in txt:
                errors.append(f"{fn}: Contains stale v4.3/1,343/26-task marker '{stale}'")
        if fn in ("gtt/gtt.md", "tdf/tdf.md", "tfp/tfp.md", "value_of_trust/value_of_trust.md"):
            brand_re = re.compile(r"\b(?:freshcredit|turso|plaid|stripe|entra|coinbase)\b", re.IGNORECASE)
            m_brand = brand_re.search(txt)
            if m_brand:
                errors.append(f"{fn}: Academic clean-room violation — commercial brand '{m_brand.group(0)}' is forbidden outside whitepaper")
        print(f"  ✓ Checked {fn}")

    root = pathlib.Path(BASE_DIR)
    bad_path_re = re.compile(
        r"/Users/" + r"devonshigaki|experiments/(?:simulations|brainit|simh1)"
        r"|/home/" + r"kimi|/mnt/" + r"agents|/private/" + r"home/"
    )
    secret_re = re.compile(
        r"(?:TOKEN|token|API_KEY|api_key)\s*=\s*['\"][0-9a-fA-F]{24,}['\"]"
        r"|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_\-]{30,}"
    )
    py_targets = (
        list(root.glob("code/**/*.py"))
        + list(root.glob("formal/**/*.py"))
        + list(root.glob("figures/**/*.py"))
        + list(root.glob("manuscripts/**/*.py"))
    )
    for p in sorted(py_targets):
        if ".venv" in str(p) or p.name == "check_manuscript_sync.py":
            continue
        txt = p.read_text(errors="ignore")
        if bad_path_re.search(txt):
            errors.append(f"{p.relative_to(root)}: Contains hardcoded personal or sandbox path")
        if secret_re.search(txt):
            errors.append(f"{p.relative_to(root)}: Contains hardcoded credential/bearer token")
    print("  ✓ Checked all Python files in code/, formal/, figures/, manuscripts/ for zero secrets or sandbox paths")

    # 5. Automated JSON-to-collection.tex verdict sync check (prevents inverted PASS/FAIL tables)
    if (root / "results").exists():
        errors.append("Repository root contains stray results/ directory (relative CWD write leak)")

    col_tex = (root / "manuscripts" / "collection" / "collection.tex").read_text(encoding="utf-8")
    col_md = (root / "manuscripts" / "collection" / "collection.md").read_text(encoding="utf-8")

    def _pf(b: bool) -> str:
        return "PASS" if b else "FAIL"

    verdict_checks = [
        ("Sim META (META-1--3)", "code/simulations/repair_era/meta_simulation/sim_meta_results.json",
         lambda d: f"{_pf(d['META1_affective_derivatives']['pass'])} / {_pf(d['META2_cross_scale_coherence']['pass'])} / {_pf(d['META3_universal_contraction']['pass'])}"),
        ("Sim K (K1 / K2 / K3)", "code/simulations/repair_era/genealogy/sim_k_results.json",
         lambda d: f"{_pf(d['K1_heritability_calibration']['pass'])} / {_pf(d['K2_tmrca_acceleration']['pass'])} / {_pf(d['K3_genetic_stratification']['pass'])}"),
        ("Sim B (B1 / B2 / B3)", "code/simulations/repair_era/basal_cognition/sim_b_results.json",
         lambda d: f"{_pf(d['B1_barrier_circumvention']['pass'])} / {_pf(d['B2_stress_steering']['pass'])} / {_pf(d['B3_trajectory_recall']['pass'])}"),
        ("Sim X (X1 / X2 / X3)", "code/simulations/repair_era/cross_substrate/sim_x_results.json",
         lambda d: f"{_pf(d['X1_lyapunov_invariance']['pass'])} / {_pf(d['X2_permutation_recurrence']['pass'])} / {_pf(d['X3_buckingham_pi_scaling']['pass'])}"),
        ("Sim DMN (DMN-1--3)", "code/simulations/repair_era/dmn/sim_dmn_results.json",
         lambda d: f"{_pf(d['DMN1_deception_suppression']['pass'])} / {_pf(d['DMN2_standing_advantage']['pass'])} / {_pf(d['DMN3_diminishing_returns']['pass'])}"),
        ("Sim B1 (B1-1--2)", "code/simulations/repair_era/tribe_bayes/results/b1_results.json",
         lambda d: f"{_pf(d['C1_pass'])} / {_pf(d['C2_pass'])}"),
    ]
    for label, rel_json, fmt_fn in verdict_checks:
        jpath = root / rel_json
        if not jpath.exists():
            errors.append(f"Missing results JSON for sync audit: {rel_json}")
            continue
        expected_v = fmt_fn(json.loads(jpath.read_text(encoding="utf-8")))
        for fname, content in [("collection.tex", col_tex), ("collection.md", col_md)]:
            lbl = label if fname == "collection.tex" else label.replace("--", "–")
            row = next((ln for ln in content.splitlines() if lbl in ln), "")
            if expected_v not in row:
                errors.append(f"{fname}: '{lbl}' row '{row.strip()}' does not match JSON verdict '{expected_v}'")
    print("  ✓ Checked JSON-to-manuscript verdict parity across Sim META, K, B, X, DMN, B1")

    # 6. Verify VERIFICATION_AXIOMS.txt matches Check.lean theorem count (no stale axiom deposit)
    ax_txt = (root / "formal" / "lean" / "VERIFICATION_AXIOMS.txt").read_text(encoding="utf-8")
    chk_txt = (root / "formal" / "lean" / "Check.lean").read_text(encoding="utf-8")
    n_check = sum(1 for ln in chk_txt.splitlines() if ln.strip().startswith("#print axioms"))
    n_ax = sum(1 for ln in ax_txt.splitlines() if "depends on axioms:" in ln)
    if n_check != n_ax or n_check < 36:
        errors.append(f"VERIFICATION_AXIOMS.txt out of sync with Check.lean ({n_ax} vs {n_check})")

    if errors:
        for e in errors:
            print(f"  ✗ ERROR: {e}")
        return 1
    print("\n✓ ALL MANUSCRIPTS, BIBLIOGRAPHIES & PORTABLE PATHS PASS AUDIT!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
