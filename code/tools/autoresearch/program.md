# Trust Stack `autoresearch` Program (Apple Silicon M4 / Thresholdout Edition)

Adapted from Andrej Karpathy's `autoresearch` (`prepare.py` / mutable file / `program.md` / `results.tsv`)
with two mandatory scientific & security upgrades:
1. **Out-of-Process Evaluation:** `candidate_estimator.py` runs in a stripped child subprocess and never sees ground-truth `lam_t` or held-out targets.
2. **Dwork's Thresholdout + One-Shot Sealed Vault:** Validation queries use Thresholdout (`tau = 0.004`, Laplace noise) to prevent adaptive overfitting; the sealed `N = 600` vault split is unlocked **once** (`--unlock-vault`) at the end of the branch.

## Research Objective
Solve **SIM-R1 (Collection Correction Register #5)**: discover a concise (`<= 45` AST nodes inside `estimate_gains`), heavy-tailed-robust online adaptive-$\lambda_t$ estimator that:
- Recovers time-average sensitivity $\bar{\lambda}$ within $\pm 0.15$ across Behrens volatility-linked users (reducing baseline `21.7%` failure rate below `5%`),
- Eliminates spurious break/build asymmetry on symmetric adaptive truth (p95 false ratio `< 1.30` vs baseline `2.23`),
- Preserves true `2x` asymmetric separation (`CD_ratio_AUC >= 0.96`).

## Rules
- **DO NOT MODIFY** `prepare.py`.
- **ONLY EDIT** `candidate_estimator.py`.
- **SIMPLICITY CRITERION:** Lower `val_score` wins; if complexity increases materially for `< 0.005` gain, discard and `git reset`.
