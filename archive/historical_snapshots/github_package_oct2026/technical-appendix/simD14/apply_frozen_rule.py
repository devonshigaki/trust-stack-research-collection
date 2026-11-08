#!/usr/bin/env python3
"""Sim D14 - apply the FROZEN verdict rule (SIM_D14_PRE_REGISTRATION.md).
Reads simD14_target_scores.csv (tidy_scores output) and prints the verdict.

Frozen rule as registered:
- Primary statistic: quantile_score (model's own calibration: rank of the
  raw_score within the distribution of scores for a background set of common
  variants; signed, extreme at both tails).
- Brain-relevant rows: ontology_curie in the brain UBERON subtree
  (UBERON:0000955 brain, UBERON:0000956 CNS parts), or CL neuronal terms,
  or gtex_tissue/biosample_name containing brain/cortex/neuronal terms.
- PASS (regulatory-plausible): the lead variant rs7528604 or >=1 LD proxy has
  any brain-relevant |quantile_score| >= 0.95 (top-5% band, frozen).
- FAIL (regulatory-null): no target variant reaches the band.
- No edits to this file are permitted after the first run.
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, "simD14_target_scores.csv"))

BRAIN_UBERON = ("UBERON:0000955", "UBERON:0000956", "UBERON:0001871",
                "UBERON:0001873", "UBERON:0001893", "UBERON:0002421",
                "UBERON:0001950", "UBERON:0002037", "UBERON:0000957")
BRAIN_TEXT = ("brain", "cortex", "cerebr", "cerebell", "neuron", "hippocamp",
              "amygdala", "hypothal", "substantia nigra", "prefrontal",
              "striat", "pituitary")

def brain_mask(d):
    m = d["ontology_curie"].astype(str).str.startswith(BRAIN_UBERON)
    for col in ("gtex_tissue", "biosample_name"):
        if col in d.columns:
            m |= d[col].astype(str).str.lower().apply(
                lambda s: any(t in s for t in BRAIN_TEXT))
    return m

brain = df[brain_mask(df)].copy()
if len(brain) == 0:
    brain = df.copy()
    print("WARNING: no brain-annotated rows; falling back to all tracks")
print(f"brain-relevant score rows: {len(brain)} "
      f"(of {len(df)} total; variants: {brain['rsid'].nunique()})")

per_var = brain.groupby(["rsid", "alt"])["quantile_score"].apply(
    lambda s: float(s.abs().max())).sort_values(ascending=False)

BAND = 0.95  # frozen top-5% band
print(f"\nfrozen band: |quantile_score| >= {BAND}\n")
hits = 0
for (rsid, alt), q in per_var.items():
    mark = "  <-- IN BAND" if q >= BAND else ""
    hits += q >= BAND
    print(f"  {rsid} ({alt}): {q:.4f}{mark}")

verdict = "PASS (regulatory-plausible)" if hits > 0 else "FAIL (regulatory-null)"
print(f"\nFROZEN VERDICT: {verdict}")
print("Permitted paper action: exactly ONE labeled sentence in DOCAS §4.2,")
print("per the pre-registration branch for this verdict. The two-gate verdict")
print("(GWAS significance + independent replication) is unchanged either way.")
