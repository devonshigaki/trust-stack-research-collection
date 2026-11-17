# CITATION INTEGRITY & BIBTEX PROVENANCE LEDGER
**Scope:** Real AST/Regex audit of `manuscripts/*/*.tex` against `manuscripts/*/*.bib`

| Manuscript | Bib Entries | Inline Cited Keys | Uncited (`\nocite{*}`) | Missing Keys | Journal/Book/Thesis | Explicit DOI | Working Paper / Preprint |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gtt` | 125 | 9 | 116 | 0 | 123 | 43 | 0 |
| `tdf` | 178 | 174 | 4 | 0 | 170 | 49 | 5 |
| `tfp` | 57 | 54 | 3 | 0 | 18 | 3 | 0 |
| `whitepaper` | 88 | 4 | 84 | 0 | 29 | 7 | 1 |

**Result:** 0 dangling `\cite` keys across all four LaTeX manuscripts.
