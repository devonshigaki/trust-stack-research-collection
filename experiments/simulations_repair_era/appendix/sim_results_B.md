# Simulation Results Brief — Batch B (SIM-B)

All simulations: numpy/matplotlib/scipy, base seed 42, runtime < 5 min total. Figures in `/mnt/agents/work/sims/` (PNG, 150 dpi). Implements the repaired math of `/mnt/agents/work/math/math_repairs.md` (§M2 ψ-model, §M5.4 closed-loop λ, §M7 stereographic phase map).

---

## Study 1 — The REAL TFP H1 test: leakage-graded coherence (figB1, figB2)

**Model.** Kuramoto population, N = 500, natural frequencies ω ~ Cauchy(0,1), initialized by the repaired stereographic map θ_k = 2 arctan(ε̃_k) with ε̃ ~ Cauchy(0,1) (→ uniform phases, per §M7.2). Euler integration, dt = 0.05, burn-in 100 t.u. + measurement 200 t.u., 2 seeds (42/1042) averaged per grid point.

**Leakage operationalization (exact, for the paper).** The observation-leakage parameter ℓ ∈ [0,1] degrades the feedback channel in two compounding ways:
1. **Coupling attenuation:** K_eff = K(1−ℓ) — a fraction ℓ of the feedback signal never reaches the population.
2. **Observation noise:** each agent's phase as observed by the others is θ̂_j = θ_j + η_j, η_j ~ N(0, σ_η²), **σ_η = (π/2)·ℓ**, redrawn independently every timestep. At ℓ = 0.9, σ_η ≈ 1.41 rad — the observed phase is nearly uncorrelated with the true phase.

Dynamics: θ̇_i = ω_i + K_eff·Im(Z_obs e^{−iθ_i}), Z_obs = (1/N)Σ_j e^{iθ̂_j}. Both channels compound; this is the strongest reasonable leakage model — reported thresholds are therefore conservative (real leakage may degrade R less).

**Sweep:** K ∈ [0, 8] (17 pts) × ℓ ∈ [0, 0.9] (10 pts).

**Findings.**
- **(a) R(K, ℓ) surface (figB1a).** R rises smoothly from the 1/√N floor at K ≲ 2 (consistent with the mean-field K_c = 2 for Cauchy(0,1)) to R ≈ 0.85 at K = 8, ℓ = 0. Leakage compresses the entire surface: the R = 0.7 contour retreats from K ≈ 4.4 (ℓ = 0) to K ≈ 5.5 (ℓ = 0.1), K ≈ 7 (ℓ = 0.2), and off-grid (K > 8) for ℓ ≳ 0.25.
- **(b) H1 mechanism confirmed:** R decays monotonically with ℓ at every fixed K (figB1b). At K = 4.5: R = 0.709 (ℓ=0) → 0.663 (ℓ=0.1) → 0.474 (ℓ=0.3) → 0.071 (ℓ=0.5) → 0.041 (ℓ=0.9, at the incoherent floor 0.045).
- **(c) Collapse threshold at the operating point K = 4.5 (fine scan, 3 seeds):** R falls below 0.7 at **ℓ* ≈ 0.02** (R = 0.705 at ℓ=0.01, 0.701 at 0.02, 0.698 at 0.03). R falls below 0.5 near ℓ ≈ 0.3 and below 0.1 near ℓ ≈ 0.5.
- **(d) Honest framing guidance — this is a demanding requirement, not a soft one.** At K = 4.5 the zero-leakage coherence is only R ≈ 0.71, *marginally* above the 0.7 target. So "non-expropriative measurement keeps ℓ low" must mean **ℓ ≲ 0.02** — leakage of only a few percent already breaks the R > 0.7 claim at this operating point. If the paper wants a robust claim, it must either (i) raise the operating coupling (at K = 6, R > 0.7 survives to ℓ ≈ 0.15; at K = 8, to ℓ ≈ 0.25 — read off figB1a contours), or (ii) lower the coherence target. **The qualitative mechanism (leakage erodes coherence) is robust; the quantitative threshold at K = 4.5 is fragile.** The paper should say this.
- **Artifact correction (figB2).** OLD broken map θ = atan(ε̃), ε̃ ~ Cauchy(0,1), at K = 0: **R = 0.648** (seed 42, N = 500); ensemble of 200 seeds: **R = 0.635 ± 0.014** — confirms the §M7.1 prediction of R ≈ 0.63 inflation (an "incoherent control" reporting strong coherence). NEW stereographic map: R = 0.081 (seed 42); ensemble **R = 0.040 ± 0.021**, at the finite-size floor 1/√500 = 0.045. Raw uniform phases give 0.039 ± 0.020 — matching **TFP T1's reported isolated control R = 0.032**, confirming §M7.1's inference that T1 used raw uniform phases and the broken Def.-4 map was never actually exercised. **The corrected control baseline is ≈ 0.03–0.05, not 0.63.** Any old figure showing R(K=0) ≈ 0.6 as a "control" is an artifact and must be re-baselined.

---

## Study 2 — Closed-loop λ behavior battery (figB3)

**Model (§M5.4).** Closed loop E_{t+1} = S_t with master law (GTT preset r=1, δ_S=0, λ±=λ) reduces to x_{t+2} = x_{t+1} − λx_t, x = E − V, released from unit displacement (x₀ = x₁ = 1), deterministic, 20,000 steps. Scan λ ∈ [0.02, 1.19] (118 pts).

**Verifications.**
- **Stability boundary (Jury: 0 < λ < 1).** |x| after 2000 steps: λ=0.10 → 1.8e−104, λ=0.61 → 2.8e−215, λ=0.90 → 2.1e−46 (stable); **λ=1.00 → 1.0 exactly (marginal oscillation)**; λ=1.10 → 2.4e+41 (divergent). Boundary confirmed at λ = 1 to machine behavior.
- **Critical damping λ* = 1/4.** Settling time (entry into |x| < 0.01 band, permanent) has its minimum at λ = 0.25 (figB3a): theory ln(0.01)/ln|z|_max matches simulation within ±1 step across the scan; the overdamped→underdamped transition is exactly where predicted (monotone return for λ < 1/4, overshoot/ringing for λ > 1/4).
- **Ringing period at λ = 0.61 — the falsifiable consequence for GTT §6.** Theory: 2π/atan(√(4λ−1)) = **7.17 steps**. Simulation: positive-peak spacings over the first 200 steps are [7,7,7,7,8,...], mean **7.15 steps**; regression-based period estimate over the full decay = 7.15. Envelope decays at √λ = 0.78/step as predicted. **The ≈7.2-step ringing period is confirmed and is printable.** Predicted settling 18.6 steps vs simulated 20.
- **Honest null: λ = 0.61 is NOT special.** Period and settling time vary smoothly through λ = 0.61 (periods at λ = 0.59/0.60/0.61/0.62/0.63: 7.30/7.23/7.15/7.10/7.00; settling flat at ≈ 17–20 steps). No feature, extremum, or transition exists at 0.61 — it is merely a point on the underdamped branch (period declines monotonically from ∞ at λ→1/4⁺ to 6.0 at λ=1). This supports §M5's demotion of 0.61 to a pre-registered target with corridor [0.46, 0.76], not a derived constant.

---

## Study 3 — ψ chilling-effects battery (figB4)

**Model (§M2.2, sign convention as repaired).** dε = −(μ + ψ)ε dt + σ dW, μ = σ = 1. Convention: **ψ > 0 = habituation** (observation ADDS dissipation, faster error decay); **ψ < 0 = hypervigilance/chilling** (observation REMOVES dissipation — the distortion regime TFP cares about); constraint ψ ≥ −μ. Exact OU discretization (x' = e^{−μ_eff dt}x + σ√((1−e^{−2μ_eff dt})/2μ_eff)·ξ — zero discretization bias), dt = 0.01, 64 parallel chains × 100k–300k steps (≥ 30 autocorrelation times per run), seed 42. ψ/μ scanned over [−0.95, +1.00] (11 pts).

**Verifications (figB4).**
- **Stationary variance σ²/(2(μ+ψ))** — simulated/theory ratio ∈ [0.996, 1.008] across all 11 points (max deviation 0.8%, at the deepest-chilling point). At ψ = −0.95μ: Var = 9.99 vs theory 10.00.
- **Autocorrelation.** ρ(lag 1 t.u.) matches e^{−(μ+ψ)} within ±0.002 at every point; implied τ_c = 1/(μ+ψ) verified (e.g., ψ=−0.95μ: ρ = 0.9512 vs e^{−0.05} = 0.9512; τ_c = 20 t.u.).
- **Critical slowing as ψ → −μ⁺ is real and printable:** variance and memory both diverge ∝ (μ+ψ)^{−1}. Distortion inflation factors vs the unobserved baseline: ψ = −0.2μ → ×1.25; ψ = −0.5μ → ×2.0; ψ = −0.9μ → ×10. Rising variance AND rising lag-1 autocorrelation jointly = the early-warning signature (TFP chilling-effects argument, falsifiable form).
- **Habituation branch (ψ > 0) verified too:** ψ = +1.0μ → Var = 0.249 vs theory 0.250, ρ = 0.137 vs 0.135.
- **Honest statement for TFP §4 (must be printed).** Measurement distortion is a *parameter shift* μ → μ + ψ(m), fully quantified: at residual salience the shift is small but nonzero. User-owned measurement (TFP's four architectural responses: local-first, consent-bearing, accountable, minimized) drives salience m → m_min > 0, hence **ψ → ψ(m_min) < 0, not 0 — TFP's own measurement still distorts.** Illustratively (green band in figB4), at residual ψ_min = −0.05μ the mismatch variance and memory are still inflated ×1.05. The architecture minimizes, but does not eliminate, observation-driven distortion. The paper must not claim ψ = 0 is achievable.

---

## Nulls / artifact corrections reported prominently
1. **Broken atan phase map inflates K=0 coherence to R = 0.635 ± 0.014** (200 seeds) — corrected stereographic map gives 0.040 ± 0.021 ≈ 1/√N, matching TFP T1's R = 0.032 (T1 evidently used raw uniform phases; the old Def.-4 map was never actually run).
2. **R > 0.7 at K = 4.5 requires ℓ ≲ 0.02** — the H1 quantitative threshold is fragile at the paper's operating point; only the qualitative mechanism is robust. Robust claims need K ≥ 6 or a lower coherence target.
3. **λ = 0.61 has no distinguishing dynamical feature** — smooth period/settling curves through it; only the underdamped-branch membership (ringing period 7.17 steps, confirmed at 7.15) is falsifiable.
4. **TFP's own measurement still distorts** (ψ(m_min) < 0): distortion is minimized, not zeroed — ×1.05 inflation even at illustrative residual salience ψ = −0.05μ.

## Figure index
- **figB1_R_surface.png** — (a) R(K, ℓ) heatmap with R = 0.3/0.5/0.7 contours and the K = 4.5 operating point; (b) R vs K at ℓ = 0/0.1/0.3/0.5/0.9. Params: N=500, ω~Cauchy(0,1), stereographic init, K_eff = K(1−ℓ), σ_η = πℓ/2, dt=0.05, 2 seeds.
- **figB2_phasemap_control.png** — (a) phase densities old vs new map; (b) K=0 control R boxplots (200 seeds): old 0.635±0.014, new 0.040±0.021, raw uniform 0.039±0.020, vs T1's 0.032 and the 1/√N floor.
- **figB3_lambda_battery.png** — (a) settling time vs λ with theory ln(0.01)/ln|z|; (b) ringing period vs λ with theory 2π/atan(√(4λ−1)); critical damping λ*=1/4, stability boundary λ=1, λ=0.61 marked as unremarkable. Deterministic recurrence, 118 λ values, 20k steps.
- **figB4_psi_battery.png** — (a) stationary variance vs ψ/μ (log), theory σ²/(2(μ+ψ)) + sim (ratio ≤ 1.008); (b) autocorrelation time vs ψ/μ (log), theory 1/(μ+ψ) + sim from ρ(1 t.u.); critical-slowing asymptote ψ→−μ⁺; TFP residual-salience band. μ=σ=1, exact OU step, 64 chains, seed 42.
