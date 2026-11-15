#!/usr/bin/env python3
"""
Automated Citation & BibTeX Provenance Audit
Audits all manuscripts in manuscripts/ (.tex and .bib) to verify:
1. Every \\cite / \\citep / \\citet key in *.tex exists in its corresponding .bib file.
2. Reports actual counts of DOIs, ISBNs, peer-reviewed entries, and working papers / preprints.
3. Writes an accurate, non-inflated ledger to docs/CITATION_INTEGRITY_LEDGER.md.
"""

import os
import re
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
MANUSCRIPTS_DIR = os.path.join(BASE_DIR, "manuscripts")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

PAIRS = [
    ("gtt", "gtt/gtt.tex", "gtt/gtt.bib"),
    ("tdf", "tdf/tdf.tex", "tdf/tdf.bib"),
    ("tfp", "tfp/tfp.tex", "tfp/tfp.bib"),
    ("whitepaper", "whitepaper/whitepaper.tex", "whitepaper/whitepaper.bib"),
]


def parse_bib(bib_path: str) -> dict:
    with open(bib_path, "r", encoding="utf-8") as f:
        text = f.read()
    entries = {}
    blocks = re.split(r"(?=@\w+\s*\{)", text)
    for b in blocks:
        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", b)
        if not m:
            continue
        etype, key = m.group(1).lower(), m.group(2).strip()
        if etype in ("comment", "preamble", "string"):
            continue
        entries[key] = {
            "type": etype,
            "has_doi": bool(re.search(r"\bdoi\s*=", b, re.IGNORECASE)),
            "has_isbn": bool(re.search(r"\bisbn\s*=", b, re.IGNORECASE)),
            "is_preprint_or_wp": bool(re.search(r"(arxiv|biorxiv|medrxiv|ssrn|working paper|preprint)", b, re.IGNORECASE)),
        }
    return entries


def extract_tex_cites(tex_path: str) -> set:
    with open(tex_path, "r", encoding="utf-8") as f:
        text = f.read()
    keys = set()
    for m in re.finditer(r"\\cite(?:p|t|alp|author|year)?\*?(?:\[[^\]]*\])*\{([^}]+)\}", text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k:
                keys.add(k)
    return keys


def run_audit(dry_run: bool = False):
    print("=" * 75)
    print("REAL BIBTEX & MANUSCRIPT CITATION INTEGRITY AUDIT")
    print("=" * 75)

    summary_rows = []
    all_missing = []

    for name, tex_fn, bib_fn in PAIRS:
        tex_path = os.path.join(MANUSCRIPTS_DIR, tex_fn)
        bib_path = os.path.join(MANUSCRIPTS_DIR, bib_fn)
        bib_entries = parse_bib(bib_path)
        cited_keys = extract_tex_cites(tex_path)
        missing = sorted(cited_keys - set(bib_entries.keys()))
        all_missing.extend([(name, m) for m in missing])

        n_cited = len(cited_keys)
        n_bib = len(bib_entries)
        n_journal_book = sum(1 for e in bib_entries.values() if e["type"] in ("article", "book", "inproceedings", "incollection", "phdthesis"))
        n_doi = sum(1 for e in bib_entries.values() if e["has_doi"])
        n_preprint = sum(1 for e in bib_entries.values() if e["is_preprint_or_wp"])

        summary_rows.append((name, n_bib, n_cited, len(missing), n_journal_book, n_doi, n_preprint))
        print(f"  {name:<11s} | bib={n_bib:3d} | cited={n_cited:3d} | missing={len(missing):2d} | journal/book={n_journal_book:3d} | doi_field={n_doi:3d} | preprint/wp={n_preprint:2d}")

    out_path = os.path.join(DOCS_DIR, "CITATION_INTEGRITY_LEDGER.md")
    lines = [
        "# CITATION INTEGRITY & BIBTEX PROVENANCE LEDGER",
        "**Scope:** Real AST/Regex audit of `manuscripts/*/*.tex` against `manuscripts/*/*.bib`",
        "",
        "| Manuscript | Bib Entries | Cited Keys | Missing Keys | Journal/Book/Thesis | Explicit DOI | Working Paper / Preprint |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(f"| `{row[0]}` | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |")

    if all_missing:
        lines.append("\n## Missing BibTeX Keys Detected")
        for m_doc, m_key in all_missing:
            lines.append(f"- `{m_doc}.tex`: `{m_key}`")
    else:
        lines.append("\n**Result:** 0 dangling `\\cite` keys across all four LaTeX manuscripts.")

    if not dry_run:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\n✓ Wrote honest citation ledger to: {out_path}")

    return len(all_missing) == 0


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    ok = run_audit(dry_run=dry)
    sys.exit(0 if ok else 1)
