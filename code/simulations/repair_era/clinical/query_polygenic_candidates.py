#!/usr/bin/env python3
"""
Empirical Candidate Locus & Pathway Audit
Queries Open Targets Platform GraphQL API for the core biological pathway candidates
governing the five DOCAS functions:
  - ADCY5 (Master striatal cAMP coincidence engine)
  - DRD2 (Striatal Dopamine D2 RPE gate)
  - FKBP5 (Glucocorticoid receptor allostatic negative feedback)
  - ADRA2A (Locus coeruleus noradrenaline gain control)
  - HTR1A / HTR2A (Serotonergic patience & prior-relaxation switch)
"""

import os
import json
import requests

OT_URL = "https://api.platform.opentargets.org/api/v4/graphql"

CANDIDATES = [
    {"symbol": "ADCY5",  "ensembl_id": "ENSG00000173175", "channel": "Gain Integrator (cAMP Engine)"},
    {"symbol": "DRD2",   "ensembl_id": "ENSG00000149295", "channel": "Expectation (Dopamine RPE)"},
    {"symbol": "FKBP5",  "ensembl_id": "ENSG00000096060", "channel": "Recognition (Cortisol HPA Gate)"},
    {"symbol": "ADRA2A", "ensembl_id": "ENSG00000150594", "channel": "Activation (Noradrenaline Gain)"},
    {"symbol": "HTR1A",  "ensembl_id": "ENSG00000178394", "channel": "Stabilization (Serotonergic Patience)"},
    {"symbol": "HTR2A",  "ensembl_id": "ENSG00000102468", "channel": "Stabilization (Prior Relaxation)"}
]

QUERY = """
query getTargetProfile($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    approvedName
    geneticConstraint {
      constraintType
      score
    }
    associatedDiseases(page: {size: 8, index: 0}) {
      count
      rows {
        disease {
          id
          name
        }
        score
        datatypeScores {
          id
          score
        }
      }
    }
  }
}
"""

def audit_candidates():
    print("=" * 70)
    print("EMPIRICAL GENOMIC AUDIT: CORE NEUROMODULATORY CANDIDATE PANEL")
    print("=" * 70)

    results = {}

    for cand in CANDIDATES:
        sym = cand["symbol"]
        ens = cand["ensembl_id"]
        ch = cand["channel"]

        print(f"\nQuerying Open Targets for {sym} ({ens}) — [{ch}]...")
        
        try:
            r = requests.post(OT_URL, json={"query": QUERY, "variables": {"ensemblId": ens}}, timeout=15)
            if r.status_code != 200:
                print(f"  HTTP Error {r.status_code}")
                continue
                
            data = r.json().get("data", {}).get("target", {})
            if not data:
                print(f"  No data returned for {sym}")
                continue

            constraints = {c["constraintType"]: c["score"] for c in data.get("geneticConstraint", [])}
            lof_score = constraints.get("lof", "N/A")
            mis_score = constraints.get("mis", "N/A")

            diseases = data.get("associatedDiseases", {}).get("rows", [])
            top_traits = []
            for row in diseases:
                d_name = row.get("disease", {}).get("name")
                score = row.get("score")
                # find genetic association component
                gen_score = 0.0
                for dt in row.get("datatypeScores", []):
                    if dt.get("id") == "genetic_association":
                        gen_score = dt.get("score", 0.0)
                top_traits.append({"trait": d_name, "overall_score": score, "genetic_score": gen_score})

            results[sym] = {
                "ensembl_id": ens,
                "approved_name": data.get("approvedName"),
                "functional_channel": ch,
                "loss_of_function_constraint": lof_score,
                "missense_constraint": mis_score,
                "total_associated_traits": data.get("associatedDiseases", {}).get("count", 0),
                "top_associated_traits": top_traits[:5]
            }

            print(f"  Approved Name: {data.get('approvedName')}")
            print(f"  gnomAD LoF Constraint: {lof_score}")
            print(f"  Top Associated Phenotypes (by genetic score):")
            for t in top_traits[:3]:
                print(f"    • {t['trait']}: Overall = {t['overall_score']:.3f} (Genetic = {t['genetic_score']:.3f})")

        except Exception as e:
            print(f"  Exception querying {sym}: {e}")

    out_file = os.path.join(os.path.dirname(__file__), "polygenic_candidate_audit.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved empirical candidate audit to: {out_file}")

if __name__ == "__main__":
    audit_candidates()
