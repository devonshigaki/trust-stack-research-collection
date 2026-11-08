#!/usr/bin/env python3
"""Sim D14 - PDE4B locus regulatory-plausibility scoring (AlphaGenome).
Matches the official quick-start: score_variant + RECOMMENDED_VARIANT_SCORERS
+ tidy_scores(match_gene_strand=True). Frozen criterion:
SIM_D14_PRE_REGISTRATION.md (frozen BEFORE any score was inspected).

Input:  SIM_D14_variant_list.csv (same folder): lead variant + 23 EUR LD proxies
Output: simD14_target_scores.csv

Setup:  pip install alphagenome
        export ALPHAGENOME_API_KEY=<your free key>
Run:    python3 run_d14.py
"""
import csv, os, sys, time
import pandas as pd
from alphagenome.data import genome
from alphagenome.models import dna_client, variant_scorers

HERE = os.path.dirname(os.path.abspath(__file__))
model = dna_client.create(os.environ["ALPHAGENOME_API_KEY"], timeout=600)

# All recommended gene-mask scorers (RNA_SEQ, ATAC, CAGE, DNASE, CHIP_*, PROCAP,
# SPLICE_*, CONTACT_MAPS as available in this SDK version)
try:
    SCORERS = list(variant_scorers.RECOMMENDED_VARIANT_SCORERS.values())
except AttributeError:
    from alphagenome.models.dna_model import Organism
    SCORERS = variant_scorers.get_recommended_scorers(Organism.HOMO_SAPIENS)
print(f"{len(SCORERS)} variant scorers loaded", flush=True)

rows, failures = [], []
with open(os.path.join(HERE, "SIM_D14_variant_list.csv")) as f:
    variants = list(csv.DictReader(f))

for r in variants:
    ref = r["alleles_ref_alt"].split("/")[0]
    alts = [a for a in r["alleles_ref_alt"].split("/")[1:] if a != ref and a in "ACGT"]
    for alt in alts:
        v = genome.Variant(chromosome=f"chr{r['chr']}", position=int(r["pos_GRCh38"]),
                           reference_bases=ref, alternate_bases=alt)
        interval = v.reference_interval.resize(dna_client.SEQUENCE_LENGTH_1MB)
        try:
            out = model.score_variant(interval=interval, variant=v, variant_scorers=SCORERS)
            df = variant_scorers.tidy_scores(out, match_gene_strand=True)
            df.insert(0, "rsid", r["rsid"]); df.insert(1, "alt", alt)
            df["r2_with_rs7528604_EUR"] = r.get("r2_with_rs7528604_EUR", "")
            rows.append(df)
            print(f"ok {r['rsid']} {ref}>{alt} rows={len(df)}", flush=True)
        except Exception as e:
            failures.append({"rsid": r["rsid"], "alt": alt, "error": str(e)[:300]})
            print(f"FAIL {r['rsid']} {ref}>{alt}: {str(e)[:150]}", flush=True)
        time.sleep(2)

if rows:
    pd.concat(rows, ignore_index=True).to_csv(os.path.join(HERE, "simD14_target_scores.csv"), index=False)
if failures:
    pd.DataFrame(failures).to_csv(os.path.join(HERE, "simD14_failures.csv"), index=False)
print(f"DONE targets: {len(rows)} scored, {len(failures)} failed", flush=True)
print("Next: python3 apply_frozen_rule.py", flush=True)
