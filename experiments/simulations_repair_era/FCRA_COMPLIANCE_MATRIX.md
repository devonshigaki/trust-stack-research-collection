# FreshCredit FCRA & ECOA Statutory Compliance Matrix
**Status:** DRAFT MEMORANDUM (Regulatory Engineering)

## Overview
FreshCredit operates a continuous, dynamic Trust Capital ($S_t$) engine based on the Master Stability Law ($\Delta S = \lambda(V - E)$). To deploy this in US consumer finance without triggering massive statutory liabilities under the Fair Credit Reporting Act (FCRA, 15 U.S.C. § 1681) and Equal Credit Opportunity Act (ECOA, Regulation B), the protocol relies on a **Dual-Score Parallel Run Architecture**.

## 1. The FCRA "Consumer Reporting Agency" (CRA) Trap
If FreshCredit directly issues a score used to deny a loan, it becomes a CRA. It must then provide:
* Section 611: Reinvestigation of disputed information within 30 days.
* Section 615: Adverse Action Notices explaining exactly why the score dropped.

**The Fix:** FreshCredit is **not** used for underwriting denial (Adverse Action). Incumbent banks continue to use FICO/VantageScore as the primary underwriting gate. FreshCredit operates strictly as a **"Yield-Bump / Rate-Reduction" Overlay**. If the consumer opts in and their $S_t$ is high, the bank *lowers* their interest rate. If they fail the FreshCredit check, they simply receive the standard FICO-approved rate. *You cannot trigger an Adverse Action notice for failing to qualify for an optional discount.*

## 2. ECOA / Regulation B (Disparate Impact)
ECOA prohibits discrimination on a prohibited basis (race, color, religion, national origin, sex, marital status, age). Machine learning models often face "disparate impact" claims if their alternative data proxies for protected classes.

**The Fix:** FreshCredit uses zero "alternative data" (no social media scraping, no zip code redlining, no browser history). The inputs to the trust vector $T$ are strictly **verified cryptographic attestations of contractual performance** (on-time payments, fulfilled promises). Because the inputs are identical in nature to tradeline data (just recorded continuously on edge nodes), they fall under established "permissible purpose" and "business necessity" defenses.

## 3. CFPB Section 1033 (Open Banking)
The CFPB's upcoming Section 1033 rules mandate that consumers have the right to access and share their financial data.
**The Fix:** The TFP protocol's database-per-tenant architecture natively complies with 1033. The consumer holds the cryptographic state root of their libSQL database. They grant read-access via SD-JWTs. It is the ultimate realization of the CFPB's open banking mandate.
