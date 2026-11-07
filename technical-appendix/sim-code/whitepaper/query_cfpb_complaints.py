#!/usr/bin/env python3
"""Live CFPB API Empirical Verification
Queries the Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database API
to verify the 2024 credit reporting complaint volume and issue decomposition.

Direct Source: https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/
"""

import json
import requests

def verify_cfpb_live_data():
    print("=" * 65)
    print("EMPIRICAL VERIFICATION: CFPB CONSUMER COMPLAINT DATABASE (LIVE API)")
    print("=" * 65)

    url = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/'
    base_params = {
        'product': 'Credit reporting or other personal consumer reports',
        'date_received_min': '2024-01-01',
        'date_received_max': '2024-12-31',
        'size': 0
    }

    # 1. Total 2024 Credit Reporting Complaints
    print("Querying total 2024 credit reporting complaints...")
    r_total = requests.get(url, params=base_params, timeout=20).json()
    total_count = r_total.get('hits', {}).get('total', {}).get('value', 0)
    print(f"Total 2024 Published Complaints: {total_count:,}")

    # 2. Issue: Incorrect Information
    p_incorrect = base_params.copy()
    p_incorrect['issue'] = 'Incorrect information on your report'
    r_inc = requests.get(url, params=p_incorrect, timeout=20).json()
    incorrect_count = r_inc.get('hits', {}).get('total', {}).get('value', 0)
    incorrect_share = incorrect_count / total_count

    # 3. Issue: Problem with Investigation
    p_inv = base_params.copy()
    p_inv['issue'] = "Problem with a company's investigation into an existing problem"
    r_inv = requests.get(url, params=p_inv, timeout=20).json()
    inv_count = r_inv.get('hits', {}).get('total', {}).get('value', 0)
    inv_share = inv_count / total_count

    combined_count = incorrect_count + inv_count
    combined_share = combined_count / total_count

    print(f"\nIssue Decomposition:")
    print(f"  1. 'Incorrect information on your report': {incorrect_count:,} ({incorrect_share:.2%})")
    print(f"  2. 'Problem with investigation':          {inv_count:,} ({inv_share:.2%})")
    print(f"  Combined Error/Investigation Failures:    {combined_count:,} ({combined_share:.2%})")

    # Audit against Whitepaper §1.2 & §3.0 claims
    expected_total = 2365586
    expected_incorrect = 1175009
    expected_inv = 455637

    diff_total = abs(total_count - expected_total)
    diff_incorrect = abs(incorrect_count - expected_incorrect)
    diff_inv = abs(inv_count - expected_inv)

    print(f"\nIntegrity Audit against Manuscript:")
    print(f"  Delta Total:     {diff_total} (Exact Match: {diff_total == 0})")
    print(f"  Delta Incorrect: {diff_incorrect} (Exact Match: {diff_incorrect == 0})")
    print(f"  Delta Inv:       {diff_inv} (Exact Match: {diff_inv == 0})")

    results = {
        "timestamp": "2026-11-06",
        "api_endpoint": url,
        "query_product": base_params['product'],
        "date_range": "2024-01-01 to 2024-12-31",
        "total_complaints": total_count,
        "incorrect_info_complaints": incorrect_count,
        "investigation_problem_complaints": inv_count,
        "combined_error_complaints": combined_count,
        "combined_share": float(combined_share),
        "exact_match_verified": bool(diff_total == 0 and diff_incorrect == 0 and diff_inv == 0)
    }

    import os
    out_path = os.path.join(os.path.dirname(__file__), "cfpb_verified_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to: {out_path}")

    assert results["exact_match_verified"], "FAIL: CFPB live counts diverged from manuscript snapshot!"
    print("\n✓ ALL CFPB EMPIRICAL GROUNDING INVARIANTS 100% BIT-EXACT VERIFIED!")

if __name__ == "__main__":
    verify_cfpb_live_data()
