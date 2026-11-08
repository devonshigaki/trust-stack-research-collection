# Sim D15 — Pre-Registered Criterion (FROZEN BEFORE DATA ACCESS)
# Frozen: 2026-09-10T20:39:04.285787+00:00 UTC — before any GTEx data was inspected.
# Question: does the PDE4B-locus lead variant rs7528604 (or an r2>=0.8 EUR proxy)
# associate with PDE4B expression/splicing in measured human brain tissue (GTEx)?
# Status: public-data lookup. Hypothesis-generating only; cannot alter the
# two-gate verdict of DOCAS §4.2 regardless of outcome.

## Target
- Lead: rs7528604 (GRCh38 chr1:65,941,669 G>A/C)
- Proxies: the 23-variant EUR r2>=0.8 set frozen in Sim D14 (SIM_D14_variant_list.csv)
- Gene: PDE4B (GENCODE ENSG00000184588)
- Resource: GTEx Portal API v2, single-tissue cis-eQTL / cis-sQTL associations
  (adult postmortem brain tissues; all brain tissues queried, cortex primary)

## Frozen PASS / FAIL criterion
- PASS (real-data regulatory leg): rs7528604 OR >=1 frozen proxy shows a
  significant cis-eQTL or cis-sQTL for PDE4B in >=1 GTEx brain tissue at the
  portal's own significance threshold (q-value <= 0.05), OR a nominal
  association p < 1e-4 in a brain tissue (threshold frozen here a priori).
- FAIL (no measurable expression link): no variant in the frozen set meets the
  above in any brain tissue (includes variants present in GTEx but null).
- INDETERMINATE: lead variant AND all proxies absent from GTEx reference panel
  (then reported as INDETERMINATE, never silently dropped).

## Permitted paper action (exactly one sentence, either branch)
- PASS: §4.2 gains one sentence — public postmortem brain data show a PDE4B
  cis-e/sQTL at the locus (tissue, p/q, effect direction stated); labeled
  instrument-level support for the regulatory-prior reading; two-gate verdict
  unchanged.
- FAIL: §4.2 gains one sentence — no detectable PDE4B expression/splicing link
  in GTEx brain at the frozen threshold; the regulatory-plausibility PASS from
  Sim D14 is annotation-only; hypothesis downgraded a further notch.
- One claims-table row (outside the 24-test multiplicity family; public-data
  lookup, flagged as such). No other text changes permitted.

---

# CLOSURE — appended after execution (frozen criterion above unchanged)
# Closed: 2026-09-11 UTC
# VERDICT: FAIL (no detectable PDE4B expression/splicing link at the locus in GTEx brain)
#
# Resource substitution (access-forced, recorded openly): GTEx Portal API v2 was
# unreachable from the execution environment (TLS/timeout, repeated). Identical
# underlying study data were obtained from two public mirrors of the same GTEx
# v8 release: (a) eQTL Catalogue imported GTEx_V8 full cis-eQTL summary
# statistics (tabix slices, chr1:65,921,722-66,018,157, all 13 brain tissues,
# ge quantification; 55,210 rows saved to simD15/SIM_D15_raw_slice.csv);
# (b) the GTEx project's own public GCS bucket (adult-gtex,
# bulk-qtl/v8/single-tissue-cis-qtl/, GTEx_Analysis_v8_eQTL.tar and
# GTEx_Analysis_v8_sQTL.tar): per-tissue significant variant-gene/splice pairs
# and sgenes tables for all 13 brain tissues (SHA-256 manifest:
# simD15/SIM_D15_gtex_file_manifest_sha256.csv).
#
# Panel presence: 24/24 frozen variants present in the GTEx v8 panel
# (INDETERMINATE branch not triggered).
#
# Leg-by-leg results (criterion: q<=0.05 in >=1 brain tissue OR nominal p<1e-4):
# - eQTL, q-leg (GTEx v8 official significant pairs, 13 brain tissues):
#   0 rows for any frozen variant x PDE4B; 0 rows for the frozen variants for
#   ANY gene; PDE4B has 0 significant eQTL pairs genome-wide in all 13
#   (SIM_D15_signifpairs_evidence.csv).
# - eQTL, nominal leg (full summary statistics, 13 brain tissues):
#   minimum nominal p = 1.766e-3 (proxy rs11208779, Brain - Frontal Cortex
#   BA9); lead rs7528604: p = 0.0246 (BA9), p = 0.0486 (Cortex); no
#   variant-tissue combination reaches the frozen p<1e-4 threshold
#   (SIM_D15_results.txt; SIM_D15_pde4b_variant_tissue_minp.csv; 312
#   frozen-variant x PDE4B tissue rows).
# - sQTL, q-leg (GTEx v8 official significant splice pairs, 13 brain tissues):
#   0 rows for any frozen variant x any PDE4B splice cluster; 0 rows for the
#   frozen variants for ANY phenotype; PDE4B itself is not a significant
#   sGene in any brain tissue (per-tissue best-cluster q = 0.256-0.822;
#   SIM_D15_sgenes_PDE4B_rows.csv).
# - sQTL, nominal leg: GTEx never released full per-variant sQTL summary
#   statistics; the only public per-variant sQTL data are the significant-pairs
#   files evaluated above, so this sub-leg is evaluable only down to each
#   tissue's significance threshold (all null). Recorded as a limitation; it
#   cannot rescue PASS because the criterion's OR is evaluated across legs and
#   every evaluable leg is null, and the variants are present (FAIL branch,
#   "variants present in GTEx but null", applies).
#
# Permitted action executed: exactly one FAIL-branch sentence added to DOCAS
# S4.2 plus one claims-table row flagged outside the 24-test multiplicity
# family (public-data lookup). No other text changed. Two-gate verdict of
# S4.2 unchanged (gate i passed, gate ii failed; PDE4B remains a labeled
# hypothesis, downgraded a further notch per the frozen FAIL branch).
