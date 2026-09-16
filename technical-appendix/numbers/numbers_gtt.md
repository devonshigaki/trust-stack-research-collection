# numbers_gtt.md — SIM-G full GTT re-run under repaired conventions

Re-run of the GTT simulation battery against `/mnt/agents/output/revised/gtt_revised.md`
(claims G1–G21, §3.6 Sims G1–G9) per `/mnt/agents/work/math/math_repairs.md`.
All runs: numpy/scipy/matplotlib, seed 42 (Sim G8 is deterministic, seed-free), honest nulls
retained. Figures in this directory (PNG, 150 dpi, captioned, axis labels).

Conventions implemented: ε = V − E (positive = confirmation); master law
S_{t+1} = S_t + λ⁺max(ε,0)r + λ⁻min(ε,0)r − δ_S(S−S_base); GTT preset r=1, δ_S=0, λ⁺=λ⁻=λ;
stereographic phase map θ = 2 arctan(ε̃).

## Claim vs re-run table

| # | Printed claim | Re-run value | Verdict |
|---|---|---|---|
| G12 / Sim G1(a) | all 200 ICs on Δ⁴ converge to alignment fixed point; final Fisher–Rao distance 0.0; median 10 steps to d < 0.01 (λ=0.35 planted) | final d = 0.0 for all 200 (float saturation by step 200); median 10 steps, mean 10.2 (median initial d = 0.82) | PASS |
| G1(c) | Langevin noise floor d̄ ≈ 3.3σ over σ∈[0.01,0.5] | NOT RE-RUN — not in delegated battery list | — |
| G13 / Sim G1(b) | R < 0.3 everywhere below K_c = 2 | max R = 0.079 for K < 2; R(K=2) = 0.195 | PASS |
| G13 | transition band R: 0.25 → 0.75 over K ∈ [2, 4.5] | R: 0.195 → 0.732 over K ∈ [2, 4.5] | PASS (band endpoints ~0.02–0.05 lower; same shape) |
| G13 | PAS coherence R > 0.7 by K = 4.5 | R(4.5) = 0.732 | PASS |
| G13 | R = 0.89 at K = 10 | R(10) = 0.880 (seed-mean of 42/1042) | PASS |
| G13 | finite-size scaling (N=500/2000/5000) confirms R=0.7 crossing | NOT RE-RUN — not in delegated battery list | — |
| G16 / Sim G6-M2 | per-trajectory S(t) spectral-centroid separation stable vs volatile, median ratio 8.2×, BCa 95% CI [6.86, 9.28] | ratio 3.48×, BCa 95% CI [3.04, 3.69] (AR(1) φ=0.99 stable vs power-matched iid volatile, 40 replicas, λ=0.35, post-transient Welch) | DEVIATION — see note M2 below |
| G16 | Mann–Whitney U = 1600/1600, p = 7.2×10⁻¹⁵ | U = 1600/1600, p = 7.18×10⁻¹⁵ (complete separation) | PASS |
| G16 | 10,000-replicate label-swap permutation p = 1×10⁻⁴ (resolution-limited) | p = 1×10⁻⁴ (0 exceedances + 1 convention) | PASS |
| G16 | Hedges g = 7.4 [6.2, 8.6] on log-centroids | g = 8.78 | PASS (same order, very large effect) |
| G16 | both groups Gaussian-plausible by Shapiro–Wilk at n = 40 | stable p = 0.385; volatile p = 0.027 | PARTIAL — volatile log-centroids marginally non-Gaussian |
| G17 / Sim G6-M3 | UCI credit cohort payment-amount-increment excess kurtosis 575.4 | 575.43 (150,000 increments, 30,000 borrowers; exact re-download of UCI 00350) | PASS |
| G17 | credit-limit excess kurtosis 0.54 (right-heavy-tailed) | 0.536 | PASS |
| G17 | model side ≈ 1.9; magnitudes disagree by ~2 orders; sign-level concordance only | calibrated two-regime Gaussian mixture (p=0.95, σ₂=2.34) gives simulated 2.00 (theory 1.9); data/model gap 575.4 vs ~1.9 confirmed | PASS (TFP T5b's exact 1.9 generator not in scope; mixture demonstrates order-1 model kurtosis) |
| G18 / Sim G7 | GTT leak-free unbounded: S = 249 after 10⁵ honest events (90% +1 / 10% −1, λ⁺=0.005, λ⁻=0.02) | S = 249.4 | PASS |
| G18 | shock-then-silence: S pinned at 10.4 forever | S = 10.400, constant for all post-shock events (pure +1 build-up to 10.5 at event 2000, ε=−5 shock, then ε=0 stream) | PASS |
| G18 | zero-ward leak half-life: theory ln2/δ = 69.3, empirical 69 events | theory 69.3, empirical 69 events | PASS |
| G18 | reconciled law recovers to within 10% of S_base in 206 events "after the same shock" (ε=−5) | after ε=−5 from baseline: 69 events (theory 69.0). The −20-shock value is 207 (theory 206.9) | DEVIATION — paper text appears to quote the −20-shock number for the −5 shock; per-shock values below replicate exactly |
| G18 (lead spec) | recovery in 69 / 138 / 207 events after −5 / −10 / −20 shocks | 69 / 138 / 207 events; matches closed form ln(0.1·S_base/λ⁻|ε|)/ln(1−δ) at every shock size | PASS |
| G18 | honest null: |ε| ≲ 2.5 absorbed without leaving 10% band | ε=−1.0: min S = 0.480; ε=−2.5: min S = 0.450 (band edge); never outside band | PASS |
| G18 | reconciled converges to S_base exactly; honest-stream asymptote S_base + drift/δ = 0.75 | post-shock S(6000) = 0.5000; 10⁵-event honest final 0.733 (asymptote 0.75, still converging after drift noise) | PASS |
| G18 | DOCAS honest asymptote drift/δ = 0.25 | 0.233 at 10⁵ events (stationary mean 0.25, seed realization) | PASS |
| G18 | cold start from S₀=0: reconciled stabilizes within 10% of asymptote in 200 events | 201 events (theory 230) | PASS |
| G18 | (Batch A) DOCAS cold start 64 events | 82 events (noise-dependent entry into ±10% band of 0.25 asymptote) | DEVIATION (minor; same order, criterion-sensitive) |
| G18 | cold-start trap: r_floor=0 never converges; 0.01→562, 0.05→143, 0.1→139, 0.5→119, 1→71, 5→23 days | r_floor=0: no events ever, S=0 permanently (trap confirmed); 0.01→563, 0.05→144, 0.1→140, 0.5→120, 1→72, 5→24 days | PASS (uniformly +1 day = day-indexing convention) |
| G19 / Sim G8 | closed loop x_{t+2}=x_{t+1}−λx_t asymptotically stable iff 0<λ<1; marginal oscillation at λ=1.00, divergence at λ=1.10 | max|x| over final 2000 steps: λ=0.10→1.5e−323, 0.25→4.9e−324, 0.61→4.9e−324, 0.90→2.5e−323 (stable); λ=1.00→1.0 exactly (marginal); λ=1.10→overflow (divergent) | PASS |
| G19 | critical damping λ*=1/4; settling time minimal at λ=0.25; theory ln(0.01)/ln|z| matches sim within ±1 step across the scan | sim settling minimum at λ∈[0.25,0.29] plateau (11/10/9/8/7 steps at 0.25–0.29); near the double root the theory curve underestimates by up to ~4 steps (polynomial prefactor (1+t)2⁻ᵗ not in ln-formula); elsewhere ±1–2 steps | PARTIAL — qualitative claim (minimum at critical damping) holds; ±1-step agreement fails at the double root |
| G19 | ringing period at λ=0.61: theory 7.17, sim 7.15 | theory 2π/atan(√(4λ−1)) = 7.17; sim positive-peak spacing 7.15 | PASS |
| G19 | envelope decay √λ ≈ 0.78/step at λ=0.61 | √0.61 = 0.781; predicted settling 18.6 vs simulated 20 | PASS |
| G19 | honest null: λ=0.61 unremarkable; periods 7.30/7.23/7.15/7.10/7.00 at λ=0.59/0.60/0.61/0.62/0.63 | 7.27/7.23/7.15/7.12/7.04; no feature at 0.61 | PASS (±0.08, peak-quantization level) |
| G20 / Sim G9 | stationary variance tracks σ²/2(μ+ψ), sim/theory ratio ∈ [0.996, 1.008] | ratio ∈ [0.992, 1.004] across ψ/μ ∈ [−0.95, +1.00] (64–256 chains × 150k–800k steps, ≥150 autocorr times at deep chilling) | PASS (structural); prior's tighter band not reproducible at comparable compute — deepest-chilling point carries ~1% sampling error |
| G20 | lag-1 autocorrelation matches e^(−(μ+ψ)) within ±0.002 at every point | max abs error 0.0057 (at ψ=+0.61μ, small-ρ point); ≤0.002 at 8/11 points; e.g. ψ=−0.95μ: 0.9513 vs 0.9512 | PASS (structural); ±0.002 tolerance not met at 3/11 points |
| G20 | ψ=−0.95μ: Var 9.99 vs theory 10.00 | Var 10.01 vs 10.00; τ_c 20.0 vs 20.0 | PASS |
| G20 | inflation ×1.25 / ×2 / ×10 at ψ = −0.2 / −0.5 / −0.9μ (variance and memory) | exact by construction of theory curve; sim at ψ=−0.9μ region: Var 2.03 vs theory 2.04 (ψ=−0.75 grid point) and 10.01/10.00 at −0.95; ratios 1.25/2.0/10.0 confirmed on curve | PASS |
| G20 | habituation branch ψ=+μ: Var 0.249 vs 0.250; ρ 0.137 vs 0.135 | Var 0.250 vs 0.250; ρ 0.137 vs 0.135 | PASS |
| G20 | residual distortion ×1.05 at ψ=−0.05μ | theory ×1.0526 (not a Monte-Carlo quantity; curve value) | PASS |
| G21 | old atan map: R(K=0) = 0.635 ± 0.014 over 200 seeds (N=500, Cauchy(0,1)) | 0.636 ± 0.014 (seed-42 single value 0.648, matching Batch B) | PASS |
| G21 | corrected stereographic map: 0.040 ± 0.021 | 0.041 ± 0.022 (seed-42 single 0.081, matching Batch B) | PASS |
| G21 | raw uniform phases 0.039 ± 0.020; finite-size floor 1/√500 = 0.045 | 0.042 ± 0.021; floor 0.045 | PASS |
| G21 | matches TFP Sim P1 isolated control R = 0.032 | consistent (re-run distribution contains 0.032); P1 itself NOT RE-RUN here (TFP battery, outside scope) | PASS (consistency) |

## Non-simulation claims (not re-runnable by this battery)

G1 (Fisher–Rao geometry, textbook), G2 (Lyapunov stability, proven), G3 (OU/Fokker–Planck,
textbook), G4 (Kuramoto analogy status), G5's homology leg, G6–G9 (literature: behavioral
genetics, evolutionary game theory, predictive processing, economic evidence), G7b, G10/G10b's
prospective-corridor content, G11 (prospective network hypothesis). These are proofs, citations,
or pre-registered hypotheses — nothing to simulate. G10b's in silico leg is covered by Sim G8 above.

## Simulation claims not re-run in this delegated battery

- Sim G1(c) Langevin noise floor d̄ ≈ 3.3σ (not in the lead's battery list).
- Sim G1(b) finite-size scaling at N=2000/5000 (not in the battery list).
- Sim G6-M1 manifold contraction, 60 ICs, dispersion ratio 0.053 [0.0475, 0.0594] (not in list).
- DOCAS operator-recovery slope 0.348, R²=0.970 (DOCAS battery, outside scope).
- TFP leakage-graded R(K,ℓ) surface / ℓ* ≈ 0.02 fragility (Batch B Study 1; TFP battery, outside scope).
- TFP T5b's exact 1.9-kurtosis generator (spec not available; a calibrated mixture shows the model
  side is order-1, which is all M3 needs).

## Notes on deviations

- **M2 centroid ratio (8.2× → 3.5×).** With S(t) the output of the pure integrator (λ=0.35) driven by
  power-matched streams, the 1/f² integration filter caps the stable/volatile S-centroid ratio at ≈3.7
  for any stable-stream persistence φ (verified φ ∈ {0.99, 0.995, 0.999, 0.9995} → 3.48–3.65). The
  printed 8.2× is not reachable under this implementation. Centroids of the raw mismatch streams
  (before integration) do reach the printed magnitude (9.5× at φ=0.95, 24.8× at φ=0.99), so the prior
  number likely used stream (not S) centroids or unmatched power. Separation itself is total
  (U=1600/1600, p=7.2×10⁻¹⁵) under any of these variants; the reframed claim (a definitional
  consistency check, not external evidence) stands, but the point value 8.2× and its CI should be
  re-derived or the operationalization stated explicitly.
- **Sim G7 "206 events" for the ε=−5 shock.** §3.2 and G18 say the reconciled law recovers from "the
  same shock" (−5) in ~206 events. Re-run: −5 recovers in 69 events; 207 (≈206) is the −20-shock
  value. The paper text conflates the two rows of its own recovery table; 69/138/207 for −5/−10/−20
  replicate exactly.
- **Sim G8 theory-vs-sim settling near λ*=1/4.** The ln(0.01)/ln|z| formula misses the (1+t)0.5ᵗ
  polynomial prefactor at the defective double root, underestimating settling by up to ~4 steps in
  λ∈[0.25, 0.30]; simulated argmin settling is λ=0.29 (7 steps), not exactly 0.25. The "minimum at
  critical damping" claim survives only as a plateau statement.
- **Sim G9 tolerances.** At disclosed compute (64–256 chains, ≥150 autocorrelation times per point)
  the variance ratio band is [0.992, 1.004] and max autocorr error 0.006, versus printed [0.996, 1.008]
  and ±0.002. Structural agreement is exact; the printed tolerances imply ~5× more sampling than
  stated (or a favorable seed). Recommend widening printed tolerances or disclosing the larger ensemble.

## Figure index

- `figG1_convergence.png` — Sim G1(a): distance trajectories + convergence-time histogram.
- `fig_kuramoto_threshold.png` — Sim G1(b): R vs K, K_c=2, floor 1/√N, operating point K=4.5.
- `figG6_M2_spectral.png` — M2 consistency check: median output spectra + per-trajectory centroids.
- `figG6_M3_heavytail.png` — M3: UCI increment histogram vs model mixture histogram.
- `figG8_lambda_battery.png` — Sim G8: settling time and dominant period vs λ.
- `figG9_psi_battery.png` — Sim G9: stationary variance and autocorrelation time vs ψ/μ.
- `fig_phasemap_control.png` — phase-map artifact correction (maps + K=0 control boxplots).
- `figG7_longrun.png` — Sim G7: shock-then-silence, 10⁵-event horizons, recovery curves, cold-start scan.
