# SIM-R1 — Robustness Batteries: Structural Misspecification & Closure Sensitivity

**Code:** `simR1_battery1.py`, `simR1_battery1_figs.py`, `simR1_battery2.py` (same directory). numpy/scipy/matplotlib only, seed 42 (generator streams offset per arm: +1000…+5000), runtime < 2 min total.
**Figures (150 dpi, captioned):** `figR1_error_distributions.png`, `figR1_scatter_adaptive.png`, `figR2_closure_sensitivity.png`.
**Machine-readable stats:** `simR1_battery1_stats.json`, `simR1_battery2_stats.json`, `simR1_battery1_rows.npz`.

---

## BATTERY 1 — Does the certified constant-λ estimator survive adaptive-λ ground truth?

### Setup (exact forms)

**Generative law (master law, GTT preset r=1, δ_S=0).** Per event: `S_{t+1} = S_t + λ_t ε_t` (symmetric arms) or `S_{t+1} = S_t + λ⁺_t·max(ε,0) + λ⁻_t·min(ε,0)` (asymmetric arm), `ε = V − E` stack convention.

**Adaptive gain (Behrens-style volatility link).**
```
ν_t  = (1−β) ν_{t−1} + β (|ε_t|/m_a − 1),   β = 0.10, ν_0 = 0
λ_t  = clip( λ0 · (1 + c ν_t),  0.02, 1.5 )
```
ν_t is a centered, dimensionless EWMA of recent |ε| relative to the user's own stream mean m_a = E|ε| (computed analytically per user from the mixture below). The gain rises after large mismatches — the change-point-flavored response of Behrens et al. (2007). E[λ_t] = λ0 exactly when the clip does not bind; verified: at c = 1.5 the clip binds for **0.0%** of events and realized mean λ_t / λ0 = 1.0010 (at c = 3.0: 3.9% of events clipped, ratio 1.0055).

**Cadence/noise — matched to the prior battery's spec (whitepaper §3.4, Fig. 8):** N = 300 users; per-user rate ~ U[0.3, 3.0]/day over 365 days, event count Poisson(365·rate) — realized median **595.5** events/user, range 116–1093 (prior battery: median 569, range 112–1100). Mixed-sign ε̃ streams: p_neg ~ U[0.12, 0.15]; positives ~ Gamma(k=1.5, θ=0.4) (E|ε|=0.6, Eε²=0.6); betrayals ~ −0.8·|t₃| (E|ε|=0.882, Eε²=1.92 — heavier-tailed, 3.2× the second moment). Observation: ΔH_t = ΔS_t + u_t, u ~ t₄ scaled to sd σ_u = 0.10 (calibrated so the constant-λ control arm reproduces the prior battery's error scale; see caveat 1). λ0 ~ U[0.15, 0.55] → population time-average **λ̄ = 0.355** ≈ 0.35 as required.

**Estimator (the stack's constant-λ Kalman/EM).** Constant-gain state-space model: scalar state λ with process variance Q = 0 (the constant-λ restriction), observation ΔH_t = λ·ε_t + u_t with u Gaussian N(0,R) — deliberately misspecified against the t₄ truth, exactly as the prior battery. E-step = scalar Kalman filter (diffuse prior P₀=10⁶, λ₀=0.3), M-step closed form. With Q = 0 and ΔH observations this is exactly Gaussian-MLE regression of ΔH on ε; verified numerically: closed form vs explicit KF recursion vs OLS agree to **2.6e−9** (25-user check). Two-gain variant: ΔH = λ⁺ε⁺ + λ⁻ε⁻ + u (orthogonal regressors).

### Results

**Arm A — constant-λ truth (replication control).** |λ̂ − λ|: mean **0.0042**, p95 **0.0119**, max **0.0208**, 0/300 users outside 0.15; population mean λ̂ = 0.3571 vs true 0.3570. Same order as the prior battery (0.0074 / 0.0215 / 0.0343) — slightly tighter because σ_u = 0.10 is a touch kinder than the prior noise setting; the *spec* (cadence, signs, tails, misspecified Gaussian fit) is matched, and the replication confirms the estimator performs as certified **when the truth shares its structure**.

**Arm B — adaptive-λ truth (c = 1.5), the misspecification arm.**
- Against the **time-average** gain λ̄: |λ̂ − λ̄| mean **0.1169**, p95 **0.2550**, max **0.5562**; **65 of 300 users (21.7%) outside the 0.15 corridor**. Signed error is systematically positive (mean **+0.117**, figR1b) — an *upward* bias, because the gain is high precisely when |ε| is large.
- Against the **ε²-weighted** gain λ̄_w = Σλ_tε_t²/Σε_t²: |λ̂ − λ̄_w| mean **0.0041**, p95 0.0108, max 0.0283, 0/300 outside corridor — statistically indistinguishable from the constant-truth arm.
- **This is the whole story, and it is exact, not numerical:** a constant-gain least-squares/Kalman fit identifies the ε²-weighted mean gain, λ̂ → Σλ_tε_t²/Σε_t², not the time average. Under a volatility-linked gain, λ_t and ε_t² are positively correlated, so the estimator recovers an inflated gain with essentially its certified precision. The estimator's arithmetic is fine; the *target* is misspecified. Error correlates with per-user gain dispersion (r = 0.68), not with 1/n (r = −0.02) — more data does not fix it.
- Population level: mean λ̂ = **0.472** vs true time-average 0.355 (+0.117). Corrosive corollary for GTT §6 H2: **0.472 lies INSIDE the pre-registered corridor [0.46, 0.76] while the adaptive truth (0.355) lies OUTSIDE it.** A volatility-linked learner with time-average gain 0.35 would *corroborate* the 0.61 corridor under the constant-λ estimator. Corridor corroboration under structural misspecification is therefore achievable purely by weighting bias — strengthening the paper's own statement that H2 corroboration is weak evidence and that the Behrens model comparison is the primary test.
- **Answer to the registered question:** NO — the constant-λ estimator does not recover λ̄ within the 0.15 corridor under adaptive truth (21.7% of users outside; population mean biased +0.117 ≈ 0.78 corridor-widths). It recovers λ̄_w within tolerance everywhere.

**c-sensitivity (volatility coupling).** Population bias / fraction of users outside corridor: c=0.75 → +0.060 / 3.7%; c=1.5 → +0.117 / 21.7%; c=3.0 → +0.211 / 66.7%. Bias is linear in c; even mild volatility linking (c=0.75) breaks per-user corridor certification for the tail.

**Arm C — asymmetric truth (λ⁻_t = 2λ⁺_t, both volatility-linked), two-gain estimator.**
- Direction: asymmetry detected — λ̂⁻/λ̂⁺ ratio mean **2.84** [p05 2.00, p95 4.57], vs 1.41 under symmetric control (below); AUC vs the symmetric-adaptive control = **0.968**.
- Magnitude: inflated. True ratio of time averages = 2.00; recovered 2.84. Cause, again exact: the estimator recovers the channel-wise ε²-weighted gains, and the ε²-weighting distortion is stronger on the heavier-tailed betrayal channel, so the true *weighted* ratio is 2.845 — the estimator nails it (err vs weighted targets: λ⁺ mean 0.0048/max 0.023; λ⁻ mean 0.0068/max 0.030, 0/300 outside corridor) and the 2.0 structural reading is the artifact.
- Versus time-average targets: λ̂⁺ err mean 0.059 (0% outside corridor); λ̂⁻ err mean **0.446**, p95 1.20, max 2.03 — **88% of users outside corridor**.

**Arm D — symmetric adaptive truth, two-gain estimator (the honest null that matters).** Recovered ratio mean **1.41**, sd 0.44, p95 **2.23**; 46.7% of users have |ratio−1| > 0.3. **A symmetric-but-volatility-linked learner masquerades as a break/build-asymmetric learner** under the two-gain estimator, because betrayals are heavier-tailed and pull their channel's ε²-weighted gain up more. Consequence: an estimated λ⁻ > λ⁺ asymmetry cannot, by itself, distinguish TFP's structural break/build asymmetry (M4.2/T8) from symmetric adaptive gain — the ratio distributions overlap (C down to 2.00, D up to 2.23; 3.2% misclassification at the AUC-optimal split).

**Arm E — planted λ = 0 negative control.** max |λ̂| = **0.0272**, mean |λ̂| = 0.0042 — no phantom sensitivity (prior battery: 0.0092; the difference tracks the σ_u calibration, caveat 1, and stays 5× below tolerance).

### Battery 1 verdict

The prior certification was circular in exactly the registered way: the constant-λ estimator passes its own 0.15 tolerance only when the truth shares the constant-λ structure. Under a Behrens-style adaptive truth with the *same* average gain (λ̄ ≈ 0.35), per-user recovery breaches the corridor for ~22% of users (c=1.5) with a systematic **upward** bias that would push a 0.35-truth population to λ̂ ≈ 0.47 — spuriously inside the H2 corridor [0.46, 0.76]. The failure is a target failure, not an arithmetic failure: the estimator recovers the ε²-weighted gain λ̄_w to within its certified error (max 0.028). The two-gain variant identifies asymmetry direction reliably (AUC 0.97) but inflates its magnitude (2.84 vs 2.0) and reports spurious asymmetry (ratio up to 2.2) under symmetric adaptive truth. **Whitepaper §3.4's caveat ("structural misspecification of the update law itself is not covered") is confirmed as a live failure mode, and the Behrens model comparison (GTT §6 criterion iii) is load-bearing, not optional.**

---

## BATTERY 2 — Is the ≈7.2-step ringing signature robust to the loop closure?

### Setup

Dynamics (GTT preset): `S_{t+1} = S_t + λ(V − E_t)`, x_t = E_t − V, **λ = 0.61** (the H2 target; reference closure E_{t+1} = S_t gives x_{t+2} = x_{t+1} − λx_t, period 2π/atan(√(4λ−1)) = **7.17** steps, envelope √λ = 0.78/step — Sim G8's in-silico 7.15). Impulse: unit displacement released at t = 0, deterministic, 200 steps; periods from positive-peak spacing (scipy find_peaks) checked against the analytic root angles (agreement ≤ 0.5 step, peak-spacing quantization only).

**Closures and exact characteristic equations:**
1. **Exponential smoothing**, E_{t+1} = αS_t + (1−α)E_t: with y = S − V, x' = αy + (1−α)x, y' = y − λx → **z² − (2−α)z + (1 − α(1−λ)) = 0**. Complex roots (ringing) iff **λ > α/4**; |z| = √(1−α(1−λ)); period = 2π/atan2(√(4αλ−α²), 2−α). Jury: stable for all 0 < α ≤ 1, 0 < λ < 1.
2. **Zero delay**, E_t = S_t: x_{t+1} = (1−λ)x_t — first order, monotone for λ < 1. **No ringing is possible.**
3. **Two-step delay**, E_{t+1} = S_{t−1}: y_{t+1} = y_t − λy_{t−2} → **z³ − z² + λ = 0**. Jury/bisection stability boundary **λ < (√5−1)/2 = 0.618034** (numeric boundary confirmed to machine precision: 0.6180339887498942 vs 1/φ = 0.6180339887498949).

### Results (λ = 0.61)

| Closure | Period (theory) | Period (sim) | Envelope /step | Visible cycles* | vs 7.17 reference |
|---|---|---|---|---|---|
| α = 1.0 (minimal, reference) | 7.17 | 7.0 | 0.781 | 1.7 | = reference |
| α = 0.8 | 8.24 | 8.5 | 0.829 | 1.9 | +15% |
| α = 0.6 | 9.76 | 9.7 | 0.875 | 2.3 | +36% |
| α = 0.4 | 12.22 | 12.25 | 0.919 | 2.9 | +70% |
| α = 0.2 | 17.65 | 17.5 | 0.960 | 4.2 | +146% |
| zero delay E_t = S_t | — | none | 0.39 (monotone) | 0 | **signature destroyed** |
| two-step delay | 10.04 | 10.06 | 0.9962 | 78.6 | +40%, near-marginal |

\* steps for envelope to decay to 5%, divided by period.

**Closure range over which the signature survives:**
- Smoothing closure: ringing survives at **every α ∈ (0, 1]** at λ = 0.61 (condition λ > α/4); the qualitative overshoot-and-ring is robust, and smoothing makes the ringing *more persistent* (envelope 0.78 → 0.96/step, visible cycles 1.7 → 4.2). But the **period is not robust**: it drifts smoothly from 7.17 to 17.6 steps — the registered formula P(λ̂) = 2π/atan(√(4λ̂−1)) is the α = 1 member of a family P(λ, α) (figR2b); testing the formula without verifying the closure tests the wrong curve.
- Zero-delay closure: the signature **vanishes entirely** (monotone return, 0.39/step). The ringing is a delay artifact in the precise sense that it requires the one-step expectation lag; remove the lag and there is nothing to detect.
- Two-step delay: ringing persists at period 10.04 but the system sits **1.30% below the stability boundary λ = 1/φ = 0.618** — the H2 target λ = 0.61 under a two-step closure is nearly undamped (envelope 0.9962/step, ~79 visible cycles), and λ = 0.63 would diverge. The closed-loop stability margin claimed for the target ((0,1), M5.4) shrinks to (0, 0.618) under this closure.

### Battery 2 verdict

**Qualitatively robust, quantitatively closure-fragile.** The underdamped/overshoot property survives exponential-smoothing closures for all α ∈ (0,1] at λ = 0.61 (and the general condition λ > α/4 is derivable), and survives a two-step delay — but it is destroyed by the zero-delay closure, so the signature is a property of the *lagged* closure, not of the update law alone. The specific 7.17-step period holds only for the minimal closure E_{t+1} = S_t; across the tested family the period ranges 7.2–17.6 steps (smoothing) and 10.0 (two-step delay), and the stability boundary itself moves (1 → 1/φ). For GTT §6: the falsifiable content "period set by λ̂ via the stated formula" is true *conditional on the minimal closure*; an empirical test must either verify the closure (estimate the E-mapping) or register the family P(λ, α) and joint-fit (λ, α). An observed failure of the 7.17 period would not discriminate "wrong λ" from "wrong closure."

---

## Caveats / failures reported

1. **σ_u calibration.** The prior battery's exact noise scale and ε-mixture are not stated in the briefs; I set σ_u = 0.10 (t₄), Gamma(1.5, 0.4)/−0.8·|t₃| mixture, matching the *published spec* (cadence, 12–15% negatives, heavier-tailed betrayals, median event count 596 vs 569). My constant-truth control reproduces the prior error scale at the right order (0.0042/0.0119/0.0208 vs 0.0074/0.0215/0.0343) but ~40% tighter — the adaptive-truth bias numbers (which are 10–50× larger than either noise floor) are insensitive to this gap; the λ=0 control differs accordingly (0.0272 vs 0.0092).
2. **The Kalman/EM is a regression here.** With ΔH observations and Q = 0, the constant-gain Kalman/EM reduces exactly to Gaussian-MLE of ΔH ~ ε (verified to 2.6e−9). Nothing about the misspecification result depends on filtering subtleties — which is itself the point: the bias is analytic (λ̂ → Σλ_tε_t²/Σε_t²), not an estimator artifact.
3. **Adaptive-λ form choice.** The volatility link λ_t = λ₀(1 + cν_t) with centered EWMA ν_t (β = 0.1) is one member of the registered Behrens-style family; the upward-bias sign is generic for any gain positively correlated with |ε| (including change-point-flavored gains), the magnitude scales with c (scanned: 0.75/1.5/3.0). A gain linked to *signed* surprise rather than volatility could bias differently in sign; not scanned.
4. **Battery 2 is deterministic** (impulse response, no observation noise): periods are exact root-angle computations with simulation as check. Detectability under realistic cadence/noise is the registered power-analysis question (GTT §6) and is not re-done here; note though that smoothing closures *increase* ring persistence (more visible cycles), so closure uncertainty is not purely bad news for detection — it is bad news for the *period formula*.
5. No failures of the planned runs occurred; all arms, controls, and verifications completed (AUC, clip diagnostics, KF-equivalence, Jury boundary to machine precision).

## Figure index

- **figR1_error_distributions.png** — (a) |λ̂−λ_target| under constant truth (mean 0.0042), adaptive truth vs time-average (mean 0.117, 21.7% > 0.15), adaptive truth vs ε²-weighted (mean 0.0041); (b) signed error showing +0.117 upward bias; (c) bias and corridor-breach fraction vs volatility coupling c ∈ {0.75, 1.5, 3.0}. Params: N=300, Poisson 0.3–3/day × 365 d (median 596 events), t₄ noise σ=0.10, λ₀~U[0.15,0.55], β=0.1, c=1.5, seed 42.
- **figR1_scatter_adaptive.png** — (a) λ̂ vs time-average λ̄ and vs ε²-weighted λ̄_w with ±0.15 corridor; population mean λ̂ = 0.472 vs λ̄ = 0.355; (b) two-gain scatter: asymmetric truth λ⁻=2λ⁺ (recovered ratio 2.84, weighted-truth ratio 2.845) vs symmetric-adaptive control (spurious ratio 1.41, p95 2.23), AUC 0.968.
- **figR2_closure_sensitivity.png** — (a) ringing period vs smoothing α at λ = 0.61 (theory curve + simulation points, 7.17 reference); (b) period-vs-λ registered relation for α ∈ {1.0, 0.8, 0.6, 0.4}; (c) impulse responses for all 7 closures with period, envelope |z|, visible-cycle annotations; zero-delay panel shows monotone decay (no ringing); two-step-delay panel shows near-undamped ringing at period 10.04 (λ = 0.61 is 1.30% below the 1/φ stability boundary).
