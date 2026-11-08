"""DOCAS round-N.1 canonical 27-stimulus battery — RECONSTRUCTION FROM SPEC.

PROVENANCE LABEL: reconstruction-from-spec, pending bit-identity check against
the user's simulations/battery27_manifest.json (NOT uploaded to this workspace).

What is verbatim vs reconstructed:
- Item 1 of every category is QUOTED VERBATIM from the Master Reproduction
  Manifest ("Simulation Suite — Master Reproduction Manifest.md", battery table,
  "Example (item 1 of each)" column).
- Items 2-5 of each offer category and CONTROL item 2 are newly written to be
  faithful to the manifest's stated design intents, crossed with the five
  principal amounts ($2,500 / $4,000 / $7,500 / $12,000 / $20,000).
- Crossing ORDER is a reconstruction choice: item 1 = $4,000 (forced by the
  verbatim quotes); items 2-5 take $2,500, $7,500, $12,000, $20,000.
- FAIR monthly payments are computed for 9% fixed APR, 60 months
  (r = 0.0075/mo): $2,500->$52, $4,000->$83, $7,500->$156, $12,000->$249,
  $20,000->$415 (item 1's "$83" matches this exactly, validating the formula).

Any single-character difference from the true battery27_manifest.json changes
every downstream neural number. Do not report original headline numbers from
this reconstruction.
"""
import json
import os

AMOUNTS_ORDER = {1: 4000, 2: 2500, 3: 7500, 4: 12000, 5: 20000}

BATTERY = {
    "FAIR": {
        1: "You are approved for a $4,000 personal loan at 9 percent fixed APR. Your payment is $83 per month for 60 months. No hidden fees, and early repayment is free.",
        2: "You are approved for a $2,500 personal loan at 9 percent fixed APR. Your payment is $52 per month for 60 months. The full fee schedule is on page one, and you can repay early at any time without charge.",
        3: "You are approved for a $7,500 personal loan at 9 percent fixed APR. Your payment is $156 per month for 60 months. Every cost is disclosed before you sign, and there is never a prepayment penalty.",
        4: "You are approved for a $12,000 personal loan at 9 percent fixed APR. Your payment is $249 per month for 60 months. The rate is fixed for the life of the loan, and extra payments go straight to principal.",
        5: "You are approved for a $20,000 personal loan at 9 percent fixed APR. Your payment is $415 per month for 60 months. All fees are listed in plain language, and you can pay off the balance early for free.",
    },
    "PREDATORY": {
        1: "Congratulations, you are pre-approved for $4,000 in cash today. Only $69 per month. Act now, this exclusive offer expires at midnight. Fees may apply. Approval not guaranteed.",
        2: "Congratulations, you are pre-approved for $2,500 in cash today. Only $43 per month. This private invitation closes tonight at midnight, so call now. Additional charges may apply. Terms subject to change without notice.",
        3: "Congratulations, you are pre-approved for $7,500 in cash today. Only $129 per month. Supplies are limited and this offer expires within hours. Act fast. Processing fees may apply. Approval not guaranteed.",
        4: "Congratulations, you are pre-approved for $12,000 in cash today. Only $207 per month. This once-only opportunity expires at midnight, do not delay. Certain fees and conditions may apply. Not everyone will qualify.",
        5: "Congratulations, you are pre-approved for $20,000 in cash today. Only $345 per month. Act immediately, this exclusive window closes tonight. Administrative fees may apply. Offer void where prohibited.",
    },
    "TEASER": {
        1: "Get $4,000 at only 2.9 percent APR for the first 6 months. After that a variable rate applies, up to 28.9 percent. Keep payments low with our minimum-payment option.",
        2: "Get $2,500 at only 1.9 percent APR for the first 12 months. After the introductory period a variable rate applies, up to 27.9 percent. Minimum payments keep your monthly cost low.",
        3: "Get $7,500 at only 3.9 percent APR for the first 9 months. Once the promotional period ends a variable rate applies, up to 29.9 percent. Choose our minimum-payment plan to keep bills small.",
        4: "Get $12,000 at only 2.49 percent APR for the first 6 months. After that a variable rate applies, up to 26.9 percent. Pay as little as the minimum each month and keep cash on hand.",
        5: "Get $20,000 at only 3.49 percent APR for the first 18 months. After the introductory window a variable rate applies, up to 30.9 percent. Our minimum-payment option keeps monthly payments low.",
    },
    "TRUST_SIGNAL": {
        1: "Build your credit with every on-time payment. We report to all three bureaus, show your progress each month, and never charge surprise fees. Borrow $4,000 at 13 percent APR.",
        2: "Build your credit with every on-time payment. We report to all three bureaus, send you a monthly progress statement, and disclose every fee up front. Borrow $2,500 at 13 percent APR.",
        3: "Build your credit with every on-time payment. We report to all three bureaus, let you track your score in the app, and never add hidden charges. Borrow $7,500 at 13 percent APR.",
        4: "Build your credit with every on-time payment. We report to all three bureaus, review your progress with you twice a year, and list all fees on one page. Borrow $12,000 at 13 percent APR.",
        5: "Build your credit with every on-time payment. We report to all three bureaus, show your payoff progress in real time, and guarantee no surprise fees. Borrow $20,000 at 13 percent APR.",
    },
    "THREAT": {
        1: "Final notice. Your $4,000 balance is past due. Pay now to avoid legal action, wage garnishment, and serious damage to your credit score.",
        2: "Final notice. Your $2,500 balance is past due. Pay immediately or face referral to collections, court action, and long-lasting damage to your credit report.",
        3: "Final notice. Your $7,500 balance is past due. Pay now to avoid a lawsuit, garnishment of your wages, and severe harm to your credit standing.",
        4: "Final notice. Your $12,000 balance is past due. Pay within ten days to avoid legal proceedings, bank account levy, and lasting damage to your credit score.",
        5: "Final notice. Your $20,000 balance is past due. Pay at once to avoid asset seizure, wage garnishment, and permanent damage to your credit history.",
    },
    "CONTROL": {
        1: "The community garden opens at eight in the morning on weekends. Members can reserve one of twenty plots for the season. Tools are stored in the shared shed.",
        2: "The public library opens at nine in the morning on weekdays. Visitors can borrow up to five books for three weeks. Reading rooms are located on the second floor.",
    },
}

VERBATIM = {f"{c}_1" for c in BATTERY}  # all item-1s incl. CONTROL_1


def iter_stimuli():
    for cat, items in BATTERY.items():
        for idx, text in items.items():
            yield {
                "id": f"{cat}_{idx}",
                "category": cat,
                "item": idx,
                "amount_usd": AMOUNTS_ORDER[idx] if cat != "CONTROL" else None,
                "text": text,
                "verbatim_from_manifest": f"{cat}_{idx}" in VERBATIM,
            }


if __name__ == "__main__":
    out = {
        "_provenance": (
            "reconstruction-from-spec, pending bit-identity check against "
            "simulations/battery27_manifest.json (not uploaded). Item-1 texts "
            "are verbatim quotes from the Master Reproduction Manifest; items "
            "2-5 (and CONTROL_2) are faithful reconstructions of the stated "
            "design intents; amount crossing order is a reconstruction choice. "
            "Do NOT report original headline numbers from this battery."
        ),
        "_crossing": "5 offer categories x 5 amounts ($2,500/$4,000/$7,500/$12,000/$20,000) + 2 CONTROL = 27",
        "stimuli": list(iter_stimuli()),
    }
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "battery27_reconstructed.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    n = len(out["stimuli"])
    assert n == 27, n
    cats = {}
    for s in out["stimuli"]:
        cats.setdefault(s["category"], []).append(s["amount_usd"])
    print(f"wrote {path}: {n} stimuli")
    for c, a in cats.items():
        print(f"  {c}: n={len(a)} amounts={a}")
