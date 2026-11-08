# Simulation Results Brief — Batch A (SIM-A)

All simulations: numpy, seed 42, runtime < 1 min. Figures in `/mnt/agents/work/sims/` (PNG, 150 dpi).
Shared parameters unless stated: λ⁺ = 0.005, λ⁻ = 0.02 (4× break/build asymmetry), δ = 0.01/event, S_base = 0.5, S₀ = 0.5.

---

## Study 1 — Long-run dynamics & cold start

**Laws implemented**
- GTT leak-free: `S += λ⁺ε (ε≥0) / λ⁻ε (ε<0)` — no decay term.
- DOCAS leak: GTT + `−δ·S` — decays toward 0.
- Reconciled: `S += λ⁺max(ε,0) + λ⁻min(ε,0) − δ(S − S_base)` — leak pulls toward a homeostatic baseline S_base (justification: absent new evidence, trust should revert to a prior, not to zero — a no-information state, not a distrust state; this also preserves TFP asymmetry λ⁻ > λ⁺).

**Findings (fig1_trajectories.png)**

1. **GTT accumulates unbounded values.** Under a stationary honest stream (90% good +1 / 10% bad −1, mean drift +0.0025/event), GTT reaches S = 249 after 10⁵ events — off-scale in fig1b (zoomed to [−2, 30]). Trust inflates without bound; any cross-user comparability is lost. A betrayal shock leaves a **permanent** scar: after a −5 shock followed by silence, S stays at 10.400 forever (fig1a). GTT's "permanent scar" claim is confirmed, but the flip side — unbounded *positive* drift — is also a pathology the GTT framing ignores.
2. **DOCAS leak decays trust to zero without events.** Half-life = ln2/δ = **69.3 events (theory) / 69 events (empirical)**. In wall-clock: at 1 event/day that's ~69 days; a thin-file user who goes quiet for a quarter loses half their trust, and after ~7 half-lives (~16 months) is back at zero — indistinguishable from a Sybil fresh account. This punishes exactly the low-activity users the cold-start story cares about. Stationary honest asymptote S* = drift/δ = 0.25.
3. **Reconciled law avoids both pathologies.** Same shock-and-silence test: S recovers to within 10% of S_base in **206 events** and converges to S_base = 0.5 exactly (fig1a). Honest-stream asymptote = S_base + drift/δ = 0.75 (empirical 0.733 after shock+regime-change, fig1b). Under a mid-stream regime change to 50% bad events it re-settles at −0.25 (bounded), then would recover if honesty resumes.

**Recovery dynamics (fig2_recovery.png).** Recovery is exponential, S(t) = S_base + (S_post − S_base)(1−δ)^t; simulated time-to-recover matches theory `ln(0.1·S_base/λ⁻|ε|)/ln(1−δ)` at every shock size tested. Numbers: shock −5 → 69 events; −10 → 138; −20 → 207. Shocks with λ⁻|ε| < 0.05 (i.e. |ε| ≲ 2.5) never push S outside the ±10% band — **honest null: small betrayals are absorbed, not scarred**, which is arguably desired behavior but contradicts a strong reading of GTT's "permanent scar" claim.

**Cold start (fig3_coldstart.png)**
- From S₀ = 0 on an honest stream, the reconciled law stabilizes within 10% of asymptote in **200 events** (theory: −ln(0.1)/δ = 230, stream-independent to first order); DOCAS takes 64 events but converges to the lower 0.25 asymptote. In wall-clock: at 5 events/day ≈ 40 days; at 0.5 events/day ≈ 400 days.
- **Cold-start trap is REAL.** With rate feedback (event rate = r_floor + 5·S per day, Poisson), r_floor = 0 → **never converges**: no history → no validations → no score, permanently. Any nonzero organic floor escapes: r_floor = 0.01/day → day 562; 0.05 → day 143; 0.1 → 139; 0.5 → 119; 1 → 71; 5 → 23 (fig3b). Implication: the product **must** seed a score-independent event floor (e.g. provider-initiated onboarding events) or thin-file users are trapped. This is a design requirement, not a tunable parameter.

---

## Study 2 — Breach expected-loss model (fig4_breakeven.png)

Model: N_all = 3×10⁸ records; n_devices = 3×10⁸ (one endpoint per tenant record).
E_C = p_org·N_all; E_T = n_devices·p_device·1 + p_commonmode·N_all. **Break-even reduces exactly to p_device + p_commonmode < p_org.**

Parameter anchors: p_org ∈ {0.02, 0.03, 0.05, 0.10}/yr (DBIR-class organizational breach base rates for bureau-scale honeypots); p_device ∈ [0.001, 0.10]/yr (per-endpoint phishing/malware compromise range); p_commonmode ∈ [10⁻⁴, 10⁻²]/yr (shared client/supply-chain vulnerability in the per-tenant stack).

**Numbers:**
- Centralized expected exposure: 6M (p_org=0.02), 9M (0.03), 15M (0.05), 30M (0.10) records/yr.
- Per-tenant wins e.g. p_device=0.005, p_cm=0.001 → E_T = 1.8M vs 15M (**8× better** than p_org=0.05 centralized).
- Per-tenant loses when endpoint multiplication dominates: p_device=0.06, p_cm=0.001 → E_T = 18.3M > 15M. At p_device=0.10, E_T = 30M+ regardless of p_cm.
- The break-even boundary is a straight line p_device = p_org − p_cm on log axes (fig4a). The entire defensible region depends on per-endpoint compromise staying well below the organizational breach rate — plausible (endpoints hold one record, not 300M, so attacker ROI per endpoint is low) but this is an assumption, not a measurement.
- **Key/guardian-loss channel (separate term, access-loss not attacker exposure):** p_key = 0.001/0.005/0.01 → +0.3M / +1.5M / +3.0M records/yr. **Honest null:** at baseline p_key = 0.005 the key-loss channel (1.5M/yr) is the same order as the entire per-tenant attacker-exposure win (1.8M/yr in the favorable example). Per-tenant's security advantage on expected *attacker-exposed* records is real in the favorable region, but it is substantially offset by self-inflicted availability loss unless guardian recovery is much better than 0.5%/yr.

---

## Study 3 — Sybil / manufactured-history cost (fig5_sybil.png)

Stack's own figure: 100.5 events per unit of standing; c = $0.001/event (x402-class). Target: a competitive synthetic history of S* = 10 units = 1,005 events.

- **Without attestation:** $0.1005/unit → **$1.01 for 10 units**. Trivially fakeable; the "costly to fake" claim is false without attestation.
- **With provider attestation (cost multiplier m):** m=10 → $10.05; m=100 → $100.50; m=1000 → $1,005 for 10 units. Linear scaling; cost alone is a weak deterrent at m ≤ 10.
- **Time floor (the real defense):** attested events must occur in wall-clock time and cannot be compressed. At a max plausible validation rate of 0.5/1/2/5 events/day, manufacturing 10 units takes **5.5 / 2.8 / 1.4 / 0.6 years minimum**. This is what restores "costly to fake because faking requires living it" — the cost multiplier m is secondary.
- **Block rollups (K events/anchor, $0.001/anchor):** on-chain cost per event falls from $0.001 (K=1) to $10⁻⁷ (K=10,000); honest user's lifetime 1,005-event cost falls from $1.005 to **$0.0001** — a 10⁴× honest-user discount that does **not** touch the Sybil time floor (fig5b). Rollups are unambiguously good: they decouple honest cost from Sybil cost.
- **Caveat:** the time floor assumes providers refuse to backdate signatures and that one Sybil cannot contract many providers in parallel. Parallel-provider collusion divides the time floor by the number of colluding providers — m and T_min must therefore be paired with a provider-diversity requirement (not modeled here).

---

## Pathologies / nulls reported prominently
1. GTT trust inflates without bound under honest streams (S=249 @ 10⁵ events) — not just "permanent scars."
2. DOCAS zero-leak erases inactive thin-file users (69-event half-life) — punishes the exact users cold-start cares about.
3. Cold-start trap is real under pure score-proportional event rates: r_floor=0 → never converges. Requires a seeded event floor.
4. Reconciled law absorbs small betrayals (|ε| ≲ 2.5) — no permanent scar for small events; papers should not overclaim scar permanence.
5. Key/guardian loss (~1.5M records/yr at p_key=0.005) is the same order as the per-tenant security win in favorable regions.
6. Sybil cost multiplier alone (m≤10) is a weak deterrent; the wall-clock time floor is the actual defense, and it degrades with parallel provider collusion.

## Figure index
- fig1_trajectories.png — (a) shock-then-silence under 3 laws (shock ε=−5 @ event 2000); (b) 10⁵-event horizon with shock @5000, regime change @50000.
- fig2_recovery.png — recovery trajectories and time-to-recover vs shock size; theory overlay.
- fig3_coldstart.png — cold-start from S₀=0; trap scan over organic floor rate.
- fig4_breakeven.png — log10(E_T/E_C) heatmap with break-even contour; expected-loss curves.
- fig5_sybil.png — Sybil cost vs attestation multiplier with rollup baselines; time floor vs plausible event rate.
