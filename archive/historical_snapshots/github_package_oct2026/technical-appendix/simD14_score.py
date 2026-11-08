#!/usr/bin/env python3
"""Sim D14 — PDE4B locus regulatory-plausibility scoring (AlphaGenome).
Frozen criterion: SIM_D14_PRE_REGISTRATION.md (frozen BEFORE any score was inspected).
Input:  SIM_D14_variant_list.csv  (lead variant + 23 EUR LD proxies, r2>=0.8)
Output: simD14_scores.csv  ->  verdict PASS / FAIL per the frozen rule.

Setup (one time, ~5 min):
  1. Get a free non-commercial API key: https://www.alphagenomedocs.com/ (Google account)
  2. pip install alphagenome
  3. export ALPHAGENOME_API_KEY=your_key
Run: python3 simD14_score.py
"""
import csv, os, sys
from alphagenome.data import genome
from alphagenome.models import dna_client

API_KEY = os.environ.get("ALPHAGENOME_API_KEY")
if not API_KEY:
    sys.exit("Set ALPHAGENOME_API_KEY (free non-commercial key from alphagenomedocs.com)")

model = dna_client.create(API_KEY)

# Brain-relevant ontologies (UBERON): brain + cerebral cortex
BRAIN = ["UBERON:0000955", "UBERON:0000956"]
OUTPUTS = [dna_client.OutputType.RNA_SEQ, dna_client.OutputType.SPLICE_SITES,
           dna_client.OutputType.ATAC, dna_client.OutputType.DNASE]

results = []
with open("SIM_D14_variant_list.csv") as f:
    for row in csv.DictReader(f):
        alleles = row["alleles_ref_alt"].split("/")
        ref, alts = alleles[0], alleles[1:]
        pos = int(row["pos_GRCh38"])
        for alt in alts:
            if alt == ref: continue
            variant = genome.Variant(chromosome="chr"+row["chr"], position=pos,
                                     reference_bases=ref, alternate_bases=alt)
            interval = genome.Interval(chromosome="chr"+row["chr"],
                                       start=pos-2**18, end=pos+2**18)  # 512 kb window
            try:
                # Atlas precomputed score (higher query rate, single call)
                out = model.predict_variant(interval=interval, variant=variant,
                                            ontology_terms=BRAIN, requested_outputs=OUTPUTS)
                # aggregate per-modality max abs log2 fold change in brain tracks
                scores = {}
                alt_t, ref_t = out.alternate, out.reference
                for name, a, r in [("RNA_SEQ", alt_t.rna_seq, ref_t.rna_seq),
                                   ("SPLICE", alt_t.splice_sites, ref_t.splice_sites),
                                   ("ATAC", alt_t.atac, ref_t.atac),
                                   ("DNASE", alt_t.dnase, ref_t.dnase)]:
                    try:
                        import numpy as np
                        scores[name] = float(np.max(np.abs(a.values - r.values)))
                    except Exception:
                        scores[name] = None
                results.append({"rsid": row["rsid"], "variant": f"{pos}{ref}>{alt}",
                                "r2": row["r2_with_rs7528604_EUR"], **scores})
                print("scored", row["rsid"], f"{ref}>{alt}")
            except Exception as e:
                print("FAILED", row["rsid"], alt, "->", e)

with open("simD14_scores.csv", "w", newline="") as f:
    if results:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(results)

# --- Frozen verdict rule (do not edit after first run) ---
# PASS: lead variant or any proxy reaches the top-5% impact band for common SNVs
#       (moderate-to-high predicted effect on PDE4B expression/splicing/chromatin
#        in brain context). Calibrate the band against a background sample of
#       common intronic SNVs scored identically (background_snps.csv).
# FAIL: no variant at the locus reaches the band.
# INDETERMINATE: scores unavailable (report as INDETERMINATE; never drop silently).
print("Done. Apply the frozen rule in SIM_D14_PRE_REGISTRATION.md to simD14_scores.csv")
