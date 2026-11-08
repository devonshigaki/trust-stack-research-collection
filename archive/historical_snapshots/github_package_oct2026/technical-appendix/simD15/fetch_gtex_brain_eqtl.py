#!/usr/bin/env python3
"""Sim D15 data acquisition: slice GTEx_V8 brain-tissue cis-eQTL summary
statistics (eQTL Catalogue imported files, tabix-indexed) for the frozen
Sim D15 locus window chr1:65,926,722-66,013,157 (GRCh38).

Read-only data retrieval. No criterion logic here beyond retrieval and a
column dump; the frozen rule is applied by a separate step against the
saved raw rows (SIM_D15_raw_slice.csv).
"""
import time
import sys
import pysam

BASE = "https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/imported/GTEx_V8/ge/{tissue}.tsv.gz"
TISSUES = [
    "Brain_Amygdala",
    "Brain_Anterior_cingulate_cortex_BA24",
    "Brain_Caudate_basal_ganglia",
    "Brain_Cerebellar_Hemisphere",
    "Brain_Cerebellum",
    "Brain_Cortex",
    "Brain_Frontal_Cortex_BA9",
    "Brain_Hippocampus",
    "Brain_Hypothalamus",
    "Brain_Nucleus_accumbens_basal_ganglia",
    "Brain_Putamen_basal_ganglia",
    "Brain_Spinal_cord_cervical_c-1",
    "Brain_Substantia_nigra",
]
CHROM, START, END = "1", 65926722, 66013157  # frozen 24-variant window
PAD = 5000

out_path = sys.argv[1] if len(sys.argv) > 1 else "SIM_D15_raw_slice.csv"
log = open("SIM_D15_fetch_log.txt", "w")

def say(msg):
    print(msg, flush=True)
    log.write(msg + "\n"); log.flush()

header = None
n_total = 0
with open(out_path, "w") as out:
    for t in TISSUES:
        url = BASE.format(tissue=t)
        say(f"--- {t} ---")
        try:
            tb = pysam.TabixFile(url)
            contigs = list(tb.contigs)
            say(f"contigs sample: {contigs[:3]}")
            c = CHROM if CHROM in contigs else ("chr" + CHROM if "chr" + CHROM in contigs else None)
            if c is None:
                say(f"!! no matching contig for chr{CHROM}; skipping")
                continue
            rows = 0
            for i, line in enumerate(tb.fetch(c, START - PAD, END + PAD)):
                if header is None:
                    # pysam TabixFile has no header API; header captured separately
                    pass
                out.write(t + "\t" + line + "\n")
                rows += 1
            say(f"rows in window: {rows}")
            n_total += rows
            tb.close()
        except Exception as e:
            say(f"ERROR {t}: {type(e).__name__}: {e}")
        time.sleep(2.5)  # be gentle; EBI firewall blacklists frequent slices
say(f"TOTAL rows: {n_total}")
log.close()
