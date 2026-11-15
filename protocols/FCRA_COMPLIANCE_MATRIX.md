# FreshCredit FCRA, Regulation V & ECOA Statutory Compliance Matrix
**Status:** HARDENED REGULATORY ENGINEERING SPECIFICATION (v4.5.0)

## Overview
FreshCredit operates a continuous, dynamic Trust Capital ($S_t$) engine based on the Master Stability Law ($\Delta S = \lambda(V - E)$). Deploying this in US consumer finance requires navigating four distinct federal statutory regimes:
1. **Fair Credit Reporting Act (FCRA, `15 U.S.C. § 1681` et seq.)** and **Regulation V (`12 C.F.R. Part 1022`)**
2. **Equal Credit Opportunity Act (ECOA, `15 U.S.C. § 1691`)** and **Regulation B (`12 C.F.R. Part 1002`)**
3. **CFPB Personal Financial Data Rights Rule (`12 C.F.R. Part 1033`, Dodd-Frank § 1033)**
4. **Medical Information Prohibition (`15 U.S.C. § 1681b(g)` / `12 C.F.R. § 1022.30`)**

---

## 1. FCRA CRA Definition (`15 U.S.C. § 1681a(d),(f)`) & Risk-Based Pricing (`12 C.F.R. § 1022.72`)
*Correction from earlier draft:* Simply structuring a score as a "Yield-Bump / Rate-Reduction Overlay" does **not** exempt a third-party furnisher from FCRA coverage. Under **FCRA § 603(d)(1)** and **§ 615(h)** (**`12 C.F.R. § 1022.72(a)`**, CFPB Risk-Based Pricing Rule), if a creditor obtains a third-party consumer report or score and grants materially less favorable terms (e.g., standard APR vs. discounted APR) to consumers who fail to qualify for the discount, the creditor must issue a **Risk-Based Pricing Notice (`§ 1022.72`)** or **Credit Score Exception Notice (`§ 1022.74(d)`)**, and any third-party entity assembling/evaluating consumer information for that purpose is a **Consumer Reporting Agency (CRA)** subject to §§ 607, 609, 611, and 615.

**The Architectural Compliance Path:**
* **Path A (First-Party Creditor Edge Evaluation under 12 C.F.R. Part 1033):** The consumer holds their own libSQL database-per-tenant state and authorizes direct Open Banking data transmission (`12 C.F.R. Part 1033`) to the *creditor itself*. Because the **creditor computes its own underwriting/pricing model on consumer-permissioned first-party transaction records** rather than purchasing a third-party score from FreshCredit Inc., FreshCredit acts strictly as open-source/client-side software infrastructure (`CFPB Advisory Opinion` on software tool providers vs. CRAs).
* **Path B (Registered CRA Mode):** If FreshCredit ever hosts or transmits third-party-derived $S_t$ scores across lenders for eligibility or pricing, that deployment must register and operate as a full **FCRA-compliant CRA** (30-day reinvestigation under § 611, full file disclosure under § 609, Adverse Action reason codes under § 615(a) + Reg B `12 C.F.R. § 1002.9`, and Risk-Based Pricing notices under `12 C.F.R. § 1022.72`).

---

## 2. Non-Waivable Medical Information Prohibition (`15 U.S.C. § 1681b(g)` / `12 C.F.R. § 1022.30`)
Under **FCRA § 604(g)(2) (`15 U.S.C. § 1681b(g)(2)`)** and **Regulation V Subpart D (`12 C.F.R. § 1022.30(b)`)**, a creditor is **strictly prohibited** from obtaining or using medical information (including physiological, neurobiological, wearable HRV/EEG/fNIRS, or stress biomarkers) in connection with any determination of eligibility, or continued eligibility, for credit.
* **Non-Waivable by Boilerplate Consent (`12 C.F.R. § 1022.30(e)(1)(v)`):** Unlike general data privacy regimes, consumer opt-in or boilerplate authorization inside a credit application **cannot** legalize using physiological/wearable biomarkers in credit underwriting or APR pricing.
* **Physical & Crate-Level Air-Gap Mandate:** Therefore, the DOCAS biological/wearable measurement stack (`code/simulations/wearables_pipeline/`, `protocols/ios_research_kiosk/`) is **strictly confined to IRB-governed non-commercial research** and must remain physically and cryptographically air-gapped from any commercial FCRA credit-scoring crate (`engine-ports` / `sim-core`). Financial scoring relies exclusively on verified financial/contractual cash-flow attestations.

---

## 3. ECOA / Regulation B (`12 C.F.R. § 1002.9`) & Disparate Impact Auditing
ECOA prohibits discrimination on a prohibited basis across all aspects of a credit transaction.
* **Exact Principal Adverse-Action Reasons (`12 C.F.R. § 1002.9(b)(2)`):** Any denial or adverse pricing decision must surface specific, concrete principal reasons (e.g., `Sim W8` exact coalitional Shapley attributions over cash-flow buffer, NSF frequency, obligation payment ratio, and deposit persistence—audited in `code/simulations/repair_era/whitepaper/sim_shap_adverse_action.py`).
* **Adverse Impact Ratio (AIR $\ge 0.80$ Four-Fifths Benchmark):** Continuous fairness auditing on real longitudinal panels (`validate_master_law_credit_panel.py`: OpenML 42477, $N=30{,}000$, measured `AIR = 0.9477`) verifies that asymmetric loss sensitivity ($\lambda^- > \lambda^+$) does not induce prohibited disparate impact, while avoiding non-financial behavioral proxies.

---

## 4. CFPB Section 1033 (`12 C.F.R. Part 1033` Open Banking)
The TFP database-per-tenant architecture aligns with `12 C.F.R. Part 1033` data-portability and consumer-permissioned access: the consumer holds the cryptographic state root of their local ledger and selectively shares verified financial attestations via SD-JWTs or Pedersen/Schnorr NIZKs (`formal/zk_master_law_stp.py`) without centralized bureau aggregation.
