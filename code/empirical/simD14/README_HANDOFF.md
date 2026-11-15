# Sim D14 — Local Execution Handoff (read me first)

**What this is:** a pre-registered, frozen in-silico study. Your job is
execution only — the criterion, scripts, and verdict rule are frozen. Do not
edit any file except to set the API key environment variable.

## Files in this package (all required)
| File | Role |
|---|---|
| `run_d14.py` | Scores all target variants via AlphaGenome `score_variant` (official quick-start API: `RECOMMENDED_VARIANT_SCORERS` + `tidy_scores(match_gene_strand=True)`) |
| `apply_frozen_rule.py` | Applies the frozen PASS/FAIL rule to the scores. Prints the verdict. |
| `SIM_D14_variant_list.csv` | 24 target variants: rs7528604 (lead, PDE4B intron, GRCh38 chr1:65,941,669 G>A) + 23 EUR LD proxies (r2 >= 0.8, 1000 Genomes Phase 3) |
| `background_snps.csv` | 35 common intronic background SNVs (optional sanity set; NOT required for the verdict — the model's quantile_score is already calibrated against common variants) |
| `SIM_D14_PRE_REGISTRATION.md` | The frozen criterion and what each verdict permits. Context only — do not edit. |

## Exact commands
```bash
pip install alphagenome pandas
export ALPHAGENOME_API_KEY=<the free non-commercial key>
cd <this folder>
python3 run_d14.py            # ~15-25 min: 24 variants, prints "ok rs..." per variant
python3 apply_frozen_rule.py  # prints the frozen verdict
```

## What success looks like
- `run_d14.py` ends with `DONE targets: 24 scored, 0 failed` (a few failures are
  acceptable; they are logged to `simD14_failures.csv` and reported as
  INDETERMINATE rows, never silently dropped)
- Two new files exist: `simD14_target_scores.csv`, and if any, `simD14_failures.csv`
- `apply_frozen_rule.py` prints `FROZEN VERDICT: PASS ...` or `FAIL ...`

## Return these files
1. `simD14_target_scores.csv` (required)
2. `simD14_failures.csv` (if created)
3. The full terminal output of both scripts (copy-paste is fine)

Do NOT interpret the results, do NOT run additional analyses, do NOT modify the
scripts. The verdict and any paper text are decided elsewhere under the
pre-registration.

## Notes
- API: official quick start — https://www.alphagenomedocs.com/colabs/quick_start.html
- The verdict uses `quantile_score`: the model's own rank of each raw score
  within a background distribution of common variants (signed; extreme at both
  tails). Frozen band: |quantile_score| >= 0.95 in any brain-relevant track.
- Free API key: https://www.alphagenomedocs.com/ (Google account; non-commercial
  research use). Expected runtime well within free daily quota.
