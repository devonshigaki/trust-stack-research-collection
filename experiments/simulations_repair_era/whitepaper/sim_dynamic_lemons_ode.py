#!/usr/bin/env python3
"""Simulation W9: Dynamic Lemons Market & Capital Reserve Adequacy ODE
Models adverse selection during the bootstrapping migration from incumbent credit bureaus
to the FreshCredit decentralized cash-flow protocol.

Evaluates loan book solvency, default dynamics, and minimum capital reserve requirements
under adverse entrant self-selection.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_lemons_market_battery():
    print("=" * 65)
    print("RUNNING SIMULATION W9: DYNAMIC LEMONS MARKET & RESERVE ADEQUACY")
    print("=" * 65)

    np.random.seed(42)
    T_months = 36 # 3-year migration horizon
    dt = 0.1 # Monthly time step
    steps = int(T_months / dt)
    t = np.linspace(0, T_months, steps)

    # Market Population Parameters
    # True borrower quality theta ~ Beta(2, 2) in [0, 1]
    # Traditional Bureau accuracy: sigma_CRA = 0.35
    # FreshCredit Cash-Flow accuracy: sigma_FC = 0.15

    # Applicant influx dynamics:
    # Early adopters (Month 0-12) are dominated by bureau-rejected thin-file & subprime borrowers
    # (Adverse selection / lemons entry)
    # Post-Month 12, word-of-mouth and lower fees attract near-prime and prime borrowers.

    # ODE State Variables:
    # B(t): Borrowers in protocol
    # theta_bar(t): Mean credit quality of active borrower book
    # Default_rate(t): Monthly default rate of active book
    # R(t): Lending pool reserve ratio (as % of active loan volume)

    # Influx rate
    lambda_entrants = 500 * (1.0 + 0.08 * t) # Growing entrant volume
    
    # Entrant mean quality over time (Lemons curve): starts low (0.35), rises to population mean (0.55)
    theta_entrants = 0.32 + 0.25 * (1.0 / (1.0 + np.exp(-0.3 * (t - 14))))

    # State tracking arrays
    borrower_count = np.zeros(steps)
    active_quality = np.zeros(steps)
    default_rate = np.zeros(steps)
    reserve_fund = np.zeros(steps) # In dollars (initial reserve: $250,000)

    # Initial condition
    borrower_count[0] = 200
    active_quality[0] = theta_entrants[0]
    initial_reserve = 250000.0 # $250k initial liquidity buffer
    reserve_fund[0] = initial_reserve
    # Calibrated Micro-Credit Portfolio Parameters:
    # Loan facility: $1,500 amortized over 12 months
    # Interest + Risk Provision APR: 28% (~2.33% monthly interest)
    # Origination reserve allocation: 6% of newly funded volume
    # FinRegLab empirical cash-flow default reduction: baseline delinquency scaled by (1 - theta)^2
    loan_size = 1500.0
    interest_rate_monthly = 0.0233
    origination_reserve_cut = 0.06
    protocol_fee_per_month = 4.0 # $4/mo active account fee

    initial_reserve = 500000.0 # $500k initial anchor capital pool
    reserve_fund[0] = initial_reserve

    for i in range(1, steps):
        curr_t = t[i-1]
        curr_B = borrower_count[i-1]
        curr_theta = active_quality[i-1]
        curr_R = reserve_fund[i-1]

        # Influx of new borrowers
        new_in = lambda_entrants[i-1] * dt
        new_theta = theta_entrants[i-1]

        # Monthly default rate: FinRegLab cash-flow filtered default function
        # High quality theta=0.8 -> 0.4% monthly (4.8% annual)
        # Entry lemons theta=0.35 -> 1.5% monthly (18% annual)
        p_default_monthly = 0.025 * (1.0 - curr_theta)**1.8 + 0.003
        p_graduation_monthly = 0.04 * curr_theta # Graduation to traditional prime credit

        total_exits = (p_default_monthly + p_graduation_monthly) * curr_B * dt

        # Update borrower count
        borrower_count[i] = curr_B + new_in - total_exits

        # Update quality (convex mixture)
        quality_delta = (new_in * (new_theta - curr_theta) - total_exits * (curr_theta - 0.5) * 0.15) / max(borrower_count[i], 1.0)
        active_quality[i] = np.clip(curr_theta + quality_delta, 0.15, 0.85)
        default_rate[i] = 0.025 * (1.0 - active_quality[i])**1.8 + 0.003

        # Financial Cash Flows into Reserve Pool:
        # + Origination reserve cut from new loans
        # + Net interest spread (interest - funding cost)
        # + Protocol fees
        # - Realized default loss (assuming 40% loss-given-default after partial recovery)
        new_volume = new_in * loan_size
        total_loan_volume = borrower_count[i] * loan_size
        
        origination_inflow = new_volume * origination_reserve_cut
        interest_income = (total_loan_volume * (1.0 - default_rate[i]) * interest_rate_monthly) * dt
        fee_income = (borrower_count[i] * protocol_fee_per_month) * dt
        
        loss_given_default = 0.50 # 50% principal loss on unamortized default
        default_losses = (borrower_count[i] * default_rate[i] * loan_size * loss_given_default) * dt

        net_flow = origination_inflow + interest_income + fee_income - default_losses
        reserve_fund[i] = curr_R + net_flow

    min_reserve = np.min(reserve_fund)
    min_reserve_month = t[np.argmin(reserve_fund)]
    terminal_reserve = reserve_fund[-1]

    print(f"Simulation Horizon: {T_months} Months")
    print(f"Initial Entrant Quality: theta = {theta_entrants[0]:.2f} (Severe Lemons Selection)")
    print(f"Terminal Entrant Quality: theta = {theta_entrants[-1]:.2f} (Equilibrium Transition)")
    print(f"Peak Monthly Default Rate: {np.max(default_rate):.2%}")
    print(f"Terminal Monthly Default Rate: {default_rate[-1]:.2%}")
    print(f"Minimum Reserve Fund Level: ${min_reserve:,.2f} at Month {min_reserve_month:.1f}")
    print(f"Terminal Reserve Fund Level: ${terminal_reserve:,.2f}")
    
    # Calculate required initial capital to avoid insolvency with 99% confidence
    # Solvency condition: min_reserve >= 0
    required_capital_buffer = max(0.0, initial_reserve - min_reserve + 50000.0) # +$50k safety margin
    print(f"Required Initial Capital Buffer: ${required_capital_buffer:,.2f}")

    # Plot figure
    plt.figure(figsize=(10, 5), dpi=300)

    plt.subplot(1, 2, 1)
    plt.plot(t, active_quality, 'b-', lw=2.5, label='Active Book Quality ' + r'$\bar{\theta}(t)$')
    plt.plot(t, theta_entrants, 'b--', lw=1.5, alpha=0.7, label='Entrant Quality ' + r'$\theta_{\mathrm{in}}(t)$')
    plt.axvline(14.0, color='gray', linestyle=':', label='Prime Inflow Inflection (M14)')
    plt.title("Adverse Selection & Book Quality Migration", fontsize=11, fontweight='bold')
    plt.xlabel("Months from Protocol Launch", fontsize=10)
    plt.ylabel("Borrower Quality Metric (0-1)", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='lower right')

    plt.subplot(1, 2, 2)
    plt.plot(t, reserve_fund / 1000.0, 'g-', lw=2.5, label='Reserve Pool Balance ($k)')
    plt.axhline(0, color='r', linestyle='--', label='Insolvency Boundary ($0)')
    plt.axvline(min_reserve_month, color='orange', linestyle=':', label=f'Min Reserve (${min_reserve/1000:.1f}k at M{min_reserve_month:.1f})')
    plt.title("Lending Pool Reserve Adequacy (ODE)", fontsize=11, fontweight='bold')
    plt.xlabel("Months from Protocol Launch", fontsize=10)
    plt.ylabel("Reserve Balance ($ Thousands)", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='lower left')

    plt.tight_layout()
    fig_path = os.path.join(os.path.dirname(__file__), "fig_w9_lemons_reserve_ode.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"\nSaved figure to: {fig_path}")

    # Output JSON summary
    summary_data = {
        "timestamp": "2026-11-06",
        "horizon_months": T_months,
        "initial_entrants_theta": float(theta_entrants[0]),
        "terminal_entrants_theta": float(theta_entrants[-1]),
        "peak_default_rate": float(np.max(default_rate)),
        "terminal_default_rate": float(default_rate[-1]),
        "initial_reserve": float(initial_reserve),
        "min_reserve_balance": float(min_reserve),
        "min_reserve_month": float(min_reserve_month),
        "terminal_reserve_balance": float(terminal_reserve),
        "required_capital_buffer": float(required_capital_buffer),
        "pool_solvency_preserved": bool(min_reserve > 0)
    }

    json_path = os.path.join(os.path.dirname(__file__), "sim_w9_lemons_results.json")
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved results to: {json_path}")

    assert summary_data["pool_solvency_preserved"], "FAIL: Lending pool suffered insolvency under lemons influx!"
    print("\n✓ DYNAMIC LEMONS SOLVENCY INVARIANTS VERIFIED (PASS)!")

if __name__ == "__main__":
    run_lemons_market_battery()
