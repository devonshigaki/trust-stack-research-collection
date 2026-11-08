# OSF DEPOSIT GUIDE — step by step (written for the post-phaseout OSF)

Your screenshot shows OSF is phasing out OSF Projects starting **November 16, 2026**. So the workflow below uses the surfaces that survive: **Research Materials** (files/data), **Registries / Study Plans** (pre-registrations), and **Preprints** (the papers). Do this today; everything below is ordered so each step unblocks the next.

## What you need on your machine
1. Your originals: the `simulations/` folder (all scripts, result JSONs, `run_full_pipeline.sh`, `battery27_manifest.json`, `sim13_manifest.json`, `concepts.json`, `clics_dist.npy`, the `*_firstrun_bug.json` audit-trail files), `Supporting Document — Statistical Verification and Significance Appendix.md`, `Simulation Pipeline — Replication and Build Guide.md`, and the three pre-registration documents.
2. Our repair-era package (download these from this session's outputs): the Technical Appendix bundle + all figures + the `osf_deposit` package we assembled (see the file list at the end).

## Step 1 — Create the Research Materials space (the file store)
1. From your OSF home (the page in your screenshot), click **"Store Research Materials"** (or go to My OSF → new).
2. Name it: **"The Trust Stack — Research Collection"**.
3. Description (paste): "Open research collection: The Value of Trust (preface); GTT (theory); DOCAS (neurochemical framework); TFP (protocol); FreshCredit whitepaper (application); Supporting Document; Technical Appendix; simulation suite. License: CC-BY 4.0 for documents; Apache-2.0 for code."
4. Set it **Public** (or private until submission, then flip public — your call; public is what makes the audit claims verifiable).

## Step 2 — Upload the materials (the audit surface)
Create this folder structure and upload:
- `/papers/` — the 6 PDFs (value_of_trust, gtt, docas, tfp, whitepaper, collection).
- `/supporting/` — your Supporting Document + Build Guide.
- `/technical-appendix/` — our assembled Technical Appendix package (math repairs, simulation briefs, run reports, numbers files).
- `/simulations/` — your original scripts + JSONs **unchanged** (this is the bit-identity acceptance test material).
- `/simulations-repair-era/` — our re-run code, figures, results JSONs, manifests (including the reconstructed battery27 manifest, clearly labeled as reconstruction-from-spec).
- `/figures/` — all figure PNGs (36+ from the sims + 9 architecture diagrams + 4 bridge figures + 5 pipeline figures).
- Every upload page gives you a per-file link — those links are what replace the `[to be deposited: OSF DOI pending]` placeholders in the papers.

## Step 3 — Register the pre-registrations (Registries)
1. Left sidebar → **Registries** → New registration → use the "OSF-Standard Pre-Data Collection Registration" template (or the closest current equivalent — OSF renamed some templates in the transition).
2. One registration per study: (a) the GTT empirical program (λ estimation, R1, H2 corridor, H0a lumpability test, H3, H4); (b) the DOCAS five-channel protocol + the carrier-gate perturbation study (we drafted this fully — see CARRIER_GATE.md); (c) TFP's pilot program; (d) the whitepaper's evaluation program.
3. Fill from your existing pre-registration documents. Where the papers' text was repaired after the fact (TFP's H1 inversion, DOCAS's frozen-criterion failure), register the CURRENT text and keep the correction history in the paper — the papers already disclose this.
4. Each registration gets a DOI on completion. Those DOIs replace the registration placeholders in the papers.

## Step 4 — Post the preprints (optional but recommended)
Left sidebar → **Preprints** → Add Preprint → one per paper (or one combined collection PDF). This gives each work a citable DOI immediately, independent of journal submission.

## Step 5 — Close the loop in the papers
1. Collect the DOIs/links from Steps 2–4.
2. Send them back here — we will replace every `(DOI: [insert])` token with the real identifiers in all 6 documents (md + tex + pdf + docx) and rebuild.
3. The papers' self-attestation clause ("until they are deposited, the frozen-criteria and protocol claims that cite them are self-attested") refers to the Supporting Document and Technical Appendix; once those two are deposited too, the clause is removed in the same rebuild.

## Time and cost
About 60–90 minutes total if your files are gathered. OSF is free. Do Steps 1–3 today while your account is open; Step 5 is ours.

## Notes specific to your account state
- Your screenshot shows zero existing projects — you're starting clean, which is ideal (no migration needed before the November 16, 2026 Projects phaseout).
- If the "Research Materials" surface asks for a "project" parent during the transition, create one named "The Trust Stack" and ignore the phaseout warning — contents migrate automatically per OSF's notice; Registries and Preprints are unaffected.
