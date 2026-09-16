#!/usr/bin/env python3
"""Sim D15 frozen-rule application. Reads SIM_D15_raw_slice.csv (raw GTEx_V8
brain cis-eQTL rows, retrieved read-only) and applies the pre-registered
criterion VERBATIM:

  Target variants: rs7528604 + 23 frozen EUR r2>=0.8 proxies (positions/
  rsids from SIM_D14_variant_list.csv).
  Gene: PDE4B (ENSG00000184588, version suffix tolerated).
  Tissues: 13 GTEx_V8 brain tissues fetched.
  PASS = (q<=0.05 in >=1 brain tissue) OR (nominal p<1e-4 in >=1 brain tissue).
         [The imported full summary statistics carry no q-values; the
         portal's significant-pairs lists are unreachable from this sandbox,
         so the q-branch is unevaluated; the nominal branch is decisive:
         p<1e-4 anywhere => PASS; min p everywhere >= 1e-4 => the nominal
         branch fails.]
  FAIL = variants present in panel, no variant meets the above.
  INDETERMINATE = lead variant AND all proxies absent from panel.

No thresholds or sets are modified here. Output: SIM_D15_results.txt + CSVs.
"""
import pandas as pd

PDE4B = "ENSG00000184588"
HEADER = ["variant","r2","pvalue","molecular_trait_object_id","molecular_trait_id",
          "maf","gene_id","median_tpm","beta","se","an","ac","chromosome","position",
          "ref","alt","type","rsid"]

vlist = pd.read_csv("/mnt/agents/output/osf_deposit/technical-appendix/simD14/SIM_D14_variant_list.csv")
frozen_rsids = set(vlist["rsid"])
frozen_pos = set(vlist["pos_GRCh38"].astype(int))

df = pd.read_csv("SIM_D15_raw_slice.csv", sep="\t", header=None,
                 names=["tissue"] + HEADER, dtype={"chromosome": str})
df["position"] = pd.to_numeric(df["position"], errors="coerce").astype("Int64")
df["pvalue"] = pd.to_numeric(df["pvalue"], errors="coerce")
df["beta"] = pd.to_numeric(df["beta"], errors="coerce")

out = []
def say(s=""):
    print(s); out.append(str(s))

say(f"raw rows: {len(df)}, tissues: {df['tissue'].nunique()}")

# --- which frozen variants are present in the panel (any gene) ---
present = df[df["position"].isin(frozen_pos) | df["rsid"].isin(frozen_rsids)]
present_variants = sorted(set(present["rsid"].dropna()) | {f"pos:{p}" for p in present["position"].dropna().unique()})
per_tissue_presence = present.groupby("tissue")["position"].nunique()
say(f"frozen variants present in panel (union across tissues): {present['position'].nunique()}/24 positions")
say(f"missing positions: {sorted(frozen_pos - set(present['position'].dropna().unique()))}")

# --- restrict to PDE4B associations ---
pde = present[present["gene_id"].astype(str).str.startswith(PDE4B)]
say(f"\nrows for frozen variants x PDE4B: {len(pde)} across {pde['tissue'].nunique()} tissues")

if len(pde) == 0:
    # check whether PDE4B appears at all in the window
    anyp = df[df["gene_id"].astype(str).str.startswith(PDE4B)]
    say(f"(any PDE4B rows in window regardless of variant: {len(anyp)})")
    say("\nVERDICT: INDETERMINATE — frozen variants absent from PDE4B association panel")
else:
    g = pde.groupby(["tissue","rsid","position"], dropna=False).agg(
        min_p=("pvalue","min"), beta=("beta","first"), maf=("maf","first")).reset_index()
    g = g.sort_values("min_p")
    say("\nPer variant-tissue minimum p for PDE4B (sorted, top 40):")
    say(g.head(40).to_string(index=False))
    best = g.iloc[0]
    say(f"\nBEST: tissue={best['tissue']} rsid={best['rsid']} pos={best['position']} "
        f"p={best['min_p']:.3e} beta={best['beta']} maf={best['maf']}")
    g.to_csv("SIM_D15_pde4b_variant_tissue_minp.csv", index=False)
    pde.to_csv("SIM_D15_pde4b_rows.csv", index=False)
    hits = g[g["min_p"] < 1e-4]
    say(f"\nfrozen nominal threshold p<1e-4: {len(hits)} variant-tissue combos pass")
    if len(hits):
        say(hits.to_string(index=False))
        say("\nVERDICT: PASS (nominal p<1e-4 branch, frozen a priori)")
    else:
        say("\nVERDICT on nominal branch: FAIL (min p across all brain tissues >= 1e-4)")

with open("SIM_D15_results.txt", "w") as f:
    f.write("\n".join(out) + "\n")
