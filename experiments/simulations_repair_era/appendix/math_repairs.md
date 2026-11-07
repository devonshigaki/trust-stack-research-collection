# M1 — Mathematical Repairs for the GTT Stack

**Scope.** Repairs to `/papers/gtt.txt` (GTT), with consequences for `docas.txt` (DOCAS), `tfp.txt` (TFP), and `whitepaper.txt`. Every repair below is either (A) a pure narrowing — deleting or downgrading a claim that the stated mathematics does not support — or (B) a new derivation, verified symbolically or numerically (Python checks quoted inline). Exact replacement text is given in `REPLACE WITH:` blocks; text to be removed in `DELETE:` blocks. Equation numbers refer to GTT as written.

**Sign convention adopted for the whole stack (Repair 4):** `ε_t = V_t − E_t` (validation minus expectation; positive ε = confirmation). This is the DOCAS §2.9 convention. GTT currently uses the negative of this; the find–replace map is in §M4.4.

---

## M1. κ repair: the divergence is a constant, not an order parameter

### M1.1 The claim as written

- Def. 3 (§2.2): "κ = ∇·T … At perfect alignment E = V the flow is divergence-free: κ = 0."
- H1 (§1.1): "…a critical point at κ = 0, separating coherent meaning (κ < 0) from entropic chaos (κ > 0)."
- Abstract: "…system curvature κ = ∇·T vanishing at the E = V fixed point."
- Figure 1(a) caption: "…the fixed point E = V is divergence-free."

### M1.2 Two defects, one fatal

**Defect 1 (type error).** `T = [D,O,C,A,S]` is a single vector (a point in ℝ⁵), not a vector field on a state space. "∇·T" is only defined for a field T(x) over a coordinate space x; the divergence of one vector is undefined. Def. 3 does not say what the independent coordinates are. The only flow the paper actually defines is the (S, ε) system of §3.2, Eq. (4):

```
dS/dt = −λε,        dε/dt = −με + ξ(t),        μ > 0.
```

**Defect 2 (fatal).** Even granting the charitable reading κ = ∇·F of *that* flow, with F(S,ε) = (−λε, −με):

```
κ = ∂(−λε)/∂S + ∂(−με)/∂ε = 0 − μ = −μ.
```

**κ = −μ everywhere in state space, in particular at alignment ε = 0.** Verified symbolically (SymPy): `divergence of (S,eps) flow: -mu; at alignment eps=0: -mu`. Consequences:

1. κ never vanishes (μ > 0). The claimed "divergence-free fixed point" does not exist.
2. κ never changes sign. There is no surface κ = 0, so there is no "critical point separating coherent meaning (κ<0) from entropic chaos (κ>0)". H1 as stated is *mathematically false*, not merely unproven.
3. The true statement is the standard one for linear dissipative systems (Liouville's formula): phase volumes contract uniformly at the constant exponential rate μ. The Jacobian has eigenvalues {0, −μ}: a *line* of fixed points (ε = 0, S arbitrary), with transverse contraction at rate μ. Numerically confirmed: `eigvals = [0, −μ]`.
4. No bifurcation is possible in this system. It is linear with constant coefficients; its divergence is constant; its only parameter-dependent quantity is the contraction *rate*, which is positive for every μ > 0. A saddle-node or pitchfork requires a state-dependent nonlinearity that no axiom of the paper supplies. Retrofitting one (e.g., μ(ε) or S-dependent feedback) would be a new mechanism, not a repair — and the paper's own labeling discipline ([DERIVED] means "follows from stated assumptions") forbids it.

### M1.3 Decision: Option (A) — pure narrowing. Option (B) considered and rejected.

I considered (B), a minimal nonlinear extension producing a genuine bifurcation, and reject it for this paper: every candidate requires an axiom the paper does not state (state-dependent corrective bandwidth, or closure of S onto E), i.e. it invents mechanism rather than repairing mathematics. The honest bifurcation structure of the *closed-loop* system (S feeds tomorrow's E, per DOCAS §2.9) does exist but is an *overdamped/underdamped* transition, not a void/chaos transition; it is derived in §M5.4 as part of the λ-scale analysis, where it belongs.

**What survives of the author's intuition.** "Divergence then convergence" is not realizable: contraction is uniform, at rate μ, at every point, from the first instant. What *is* true and worth saying: with the stochastic forcing of §3.3 retained (ξ = σ dW), the flow contracts phase volume at rate μ *toward a non-degenerate stationary Gaussian* p_stat(ε) with variance σ²/2μ, not toward a point. The attractor is a fluctuation distribution around alignment — the system "maintains alignment without collapsing to a point" — and σ²/2μ is the honest, derived replacement for the "void/chaos" dialectic: small stationary variance = tight alignment maintenance; large stationary variance = noisy, poorly-corrected alignment. Neither pole is a bifurcation.

### M1.4 Exact replacement text

**DELETE (Def. 3, §2.2):** the entire current Definition 3 ("𝜅 = ∇ ⋅ 𝑇 … rests on the alignment manifold.").

**REPLACE WITH:**

> **Definition 3 (Contraction rate).** The trust flow of §3.2 is the map F(S, ε) = (−λε, −με) on the state space (S, ε) ∈ ℝ². Its divergence is ∇·F = −μ, a negative constant independent of state. By Liouville's formula, phase volumes contract uniformly at the exponential rate μ: any set of initial conditions of area A₀ occupies area A₀e^(−μt) at time t. The corrective bandwidth μ is therefore the theory's contraction rate: high-μ environments (fast, honest feedback) erase the memory of mismatches quickly; low-μ environments retain them. There is no state at which the flow is divergence-free, and no sign change of the divergence; the theory posits no divergence-based critical point. The symbol κ is retired to avoid confusion with the curvature and coupling uses of κ elsewhere in the stack.

**Abstract — DELETE:** "with system curvature 𝜅 = ∇ ⋅ 𝑇 vanishing at the 𝐸 = 𝑉 fixed point." **REPLACE WITH:** "with the alignment state E = V a Lyapunov-stable line of fixed points whose transverse contraction rate is the corrective bandwidth μ (phase volumes contract uniformly at rate μ; no divergence-based critical point is posited)."

**H1 (§1.1) — DELETE:** "Trust is a vector field 𝑇 on Δ4 that obeys a stability law with a critical point at 𝜅 = 0, separating coherent meaning (𝜅 < 0) from entropic chaos (𝜅 > 0)." **REPLACE WITH:** "Trust is a vector field on the trust state space that obeys a stability law with a globally attracting alignment manifold (E = V), uniform phase-volume contraction at rate μ, and — under stochastic forcing — a non-degenerate stationary fluctuation distribution of variance σ²/2μ around alignment. Collective trust transitions in networks are hypothesized to have Kuramoto bifurcation form (§3.4, [ANALOGY]); no critical point is claimed for the single-agent dynamics."

**H0 (§1.1)** — replace "no critical bifurcation" with "no stability law and no attracting alignment manifold" (so H0 remains the negation of the repaired H1).

**Figure 1(a) caption — DELETE:** "the fixed point 𝐸 = 𝑉 is divergence-free." **REPLACE WITH:** "alignment E = V is an attracting line of fixed points; phase volumes contract uniformly at rate μ (§3.2)."

**Claims table (§7):** there is currently no row for the κ claim — H1's bifurcation language lives in §1.1 only. Add one line to "What the theory does not claim": "No divergence-based critical point, phase transition, or void/chaos dichotomy is claimed for the single-agent dynamics (the divergence of the §3.2 flow is the constant −μ; §2.2, Def. 3)." In §7 "What the theory claims," delete nothing else; the surviving sentence "its collective behavior has the bifurcation structure of coupled phase oscillators" is the §3.4 analogy and is repaired separately in §M7.

**Verification record:** divergence computation by SymPy (`diff(−λε,S)+diff(−με,ε) = −μ`); Jacobian eigenvalues {0, −μ} by NumPy. Classification: **(A) pure narrowing.**

---

## M2. The "field equation": deletion, and a fully defined ψ

### M2.1 The object as written

§3.3 displays, once:

```
∇·T(t) + ψ·H(T(t)) = χ(S(t) ⊗ E(t))
```

with H, χ, ψ undefined, ⊗ undefined (S and E are scalars, so S ⊗ E can at most be the scalar product S·E), and — per M1.2 — ∇·T undefined for a point vector T. This equation is not derivable from anything else in the paper and cannot be repaired by definition alone: its left-hand side has no state space to live on. **It must be deleted.** What *can* and should be saved is the sentence that follows it, which contains the paper's only real measurement-dynamics idea: that the effective dissipation of the mismatch process is measurement-dependent. I define that properly below. This is Option "define ψ precisely, delete the continuum equation" — a narrowing of §3.3 to what is derivable from Eq. (5).

### M2.2 The defined replacement: observation-dependent dissipation

**State space.** The mismatch ε ∈ ℝ (dimensionless after Repair M8), driven by the OU process of §3.3: `dε = −μ_eff ε dt + σ dW_t`.

**Definition (measurement salience).** Let m_t ≥ 0 be the *measurement-salience functional* of the observation regime at time t: a dimensionless scalar increasing in (i) the subject's awareness of being measured, (ii) the audience/persistence of the measurement record, and (iii) the stakes attached to the record; m_t = 0 for measurement that is local, consent-bearing, ephemeral, and accountable (the TFP design point). m is a property of the observation channel, not of the trust state.

**Definition (ψ).** The observation-dissipation coefficient is a function ψ : ℝ≥0 → ℝ with units of 1/time (same as μ), C¹, satisfying:

- ψ(0) = 0 — unobserved (or non-saliently observed) dynamics reduce to the unperturbed OU process;
- ψ(m) ≥ −μ for all m — total dissipation stays non-negative (no anti-damping);
- sign(ψ) encodes direction: ψ > 0 = thixotropic regime (sustained salient observation *raises* dissipation — habituation); ψ < 0 = rheopectic regime (salient observation *lowers* dissipation — hypervigilance/chilling).

**Dynamics.** `dε = −(μ + ψ(m_t)) ε dt + σ dW_t`, with Ṡ = λε (stack convention, §M4). This is Eq. (5) with a slowly modulated drift coefficient — standard, simulable, estimable (ψ enters the stationary variance below).

**Derived observable consequences** (from Eq. (7), which is exact for constant m):

- Stationary variance: `Var_stat(ε) = σ² / (2(μ + ψ(m)))`.
- Autocorrelation time: `τ_c = 1/(μ + ψ(m))`.
- **Critical slowing as ψ → −μ⁺:** variance and autocorrelation time both diverge as (μ + ψ)^(−1). Hypervigilant regimes are therefore identifiable by rising variance *and* rising lag-1 autocorrelation of the mismatch stream — a standard early-warning statistic, and a falsifiable form of GTT's H4 (§6) and TFP's chilling-effects argument.
- **ψ → 0 conditions (needed by TFP):** ψ → 0 as m → 0, i.e. when observation is (i) local-first (no shared custodial record), (ii) consent-bearing (query initiated against the participant's own store), (iii) accountable (user-visible access logs), and (iv) minimized (selective disclosure — predicates, not records). These are exactly TFP §4's four architectural responses; under them the measurement approaches non-invasive measurement and the dynamics approach the ψ = 0 OU process.

**Regularity.** ε, S ∈ ℝ; σ ≥ 0 constant; m_t piecewise continuous; ψ C¹ with ψ(0)=0, ψ ≥ −μ. Nothing else is assumed.

### M2.3 Exact replacement text

**DELETE (§3.3, final paragraph):** the sentence "The non-Newtonian stress coefficient 𝜓 appearing in the field equation ∇ ⋅ 𝑇 (𝑡) + 𝜓 ⋅ 𝐻(𝑇 (𝑡)) = 𝜒 (𝑆(𝑡) ⊗ 𝐸(𝑡)) is here identified concretely: …" and the two following sentences on Navier–Stokes. **REPLACE WITH:**

> **Observation-dependent dissipation.** The act of measurement enters the dynamics as a state modulation of the dissipation rate. Let m_t ≥ 0 be the salience of the observation regime (0 = local, consent-bearing, ephemeral, accountable measurement; increasing in awareness, audience, persistence, and stakes), and let ψ : ℝ≥0 → ℝ be C¹ with ψ(0) = 0 and ψ ≥ −μ. The mismatch process becomes
>
>     dε = −(μ + ψ(m_t)) ε dt + σ dW_t .
>
> Sustained salient observation with ψ < 0 (hypervigilance/chilling) lowers effective dissipation: stationary variance σ²/(2(μ+ψ)) and autocorrelation time 1/(μ+ψ) both rise, diverging as ψ → −μ⁺ — critical slowing is the theory's measurable signature of surveillance-driven distortion. Sustained ψ > 0 is habituation. When measurement is non-salient (m → 0), ψ → 0 and the dynamics reduce to the unperturbed OU process; engineering m → 0 is the design problem addressed by The Fresh Protocol (TFP §4). No continuum field equation on ℝ⁵ is defined or needed: the theory's dynamics live on the (S, ε) state space, and measurement dependence is fully expressed through the scalar coefficient ψ.

**Claims table row G5 — REPLACE WITH:** "Measurement changes trust dynamics through the observation-dependent dissipation ψ(m) — [DERIVED] for the OU case (stationary variance σ²/(2(μ+ψ)), critical slowing as ψ → −μ⁺); [HOMOLOGY] for the decoherence correspondence of §3.5; empirical anchor in the chilling-effects literature."

### M2.4 Where TFP legitimately uses ψ

- **TFP §1.2** ("GTT formalizes through the state-dependent dissipation coefficient ψ: the act of measuring degrades the measured quantity") — legitimate as written once ψ is defined as in M2.2; "degrades" should be sharpened to "lengthens the memory of mismatch (autocorrelation time 1/(μ+ψ)) and inflates its stationary variance."
- **TFP §4** (four architectural responses) — these are precisely the conditions under which m → 0 and hence ψ → 0; the section can now cite the derived limits (stationary variance, autocorrelation time) as the quantities the architecture minimizes.
- **TFP §1.4 H1's shared-vs-isolated database contrast** is a manipulation of m (shared custodial record = high salience/persistence); the simulated R-decay target is the collective-scale projection of ψ-driven variance inflation, through the coupling-identification of §M7.

Classification: deletion of the field equation is **(A) pure narrowing**; the ψ model with its derived variance/autocorrelation limits and critical-slowing signature is **(B) a new derivation** (it follows from Eq. (5) + the stated modulation; SymPy/NumPy checks: OU stationary variance σ²/2μ_eff standard; divergence of the (S,ε) flow under ψ is −(μ+ψ), still constant — no bifurcation reintroduced, consistent with M1).

---

## M3. The EU bridge: type-correct trust-weighted expected utility

### M3.1 The defect

Eq. (2): `EU(a|T) = Σ_o T · P(o|a) · U(o)`. T ∈ ℝ⁵ while P(o|a) and U(o) are scalars. "T·P(o|a)" is a 5-vector; multiplying by scalar U(o) and summing over o yields a 5-vector, not a scalar utility; and T·P(o|a) is not a probability distortion in any reading (components of T are not per-outcome weights — they are stages of one measurement process). The claimed reduction "trust modulates the subjective probability assigned to outcomes" is not implemented by the equation. Type-correct repairs:

### M3.2 Option 1 (recommended): exponential tilt of outcome probabilities

Define the scalar **trust index** τ(T) = tanh(w·T̃) ∈ (−1, +1), where T̃ is the component-wise-normalized trust vector (per-channel reference scales, §M8) and w ∈ ℝ⁵, Σ|wᵢ| = 1, are pre-registered stage weights (default: w concentrated on S, w = e₅, since S is the stabilized baseline; other choices are empirical). Define the tilted outcome probabilities

```
P̃(o|a,T) = P(o|a) · exp(γ τ(T) û(o)) / Z(a,T),   Z(a,T) = Σ_o' P(o'|a) exp(γ τ(T) û(o')),
```

where û(o) = (U(o) − Ū_a)/sd_a(U) is the within-action standardized utility and γ ≥ 0 is a pre-registered distortion amplitude (dimensionless). Then

```
EU(a|T) = Σ_o P̃(o|a,T) · U(o).
```

**Properties (all verified).**
1. P̃ is a probability vector: P̃(o) > 0, Σ_o P̃(o) = 1 (by construction of Z).
2. **Neutral reduction:** τ = 0 ⇒ P̃ = P ⇒ EU(a|T) = Σ_o P(o|a)U(o), exactly standard EU. (NumPy: `P_tilde(P,û,γ,0) == P`, EU = 4.6 both ways.)
3. **Monotone optimism:** dEU/dτ ≥ 0, strictly > 0 when U varies across the support (exponential tilts are monotone in the tilting parameter; NumPy: EU(τ) = [−1.11, 1.57, 4.6, 7.02, 8.48] on τ ∈ [−1,1] for a 3-outcome example — mass shifts toward high-U outcomes as τ rises).
4. **Bounded distortion:** |log(P̃(o)/P(o))| ≤ γ max|û| — trust can reweight but never create or destroy outcomes; no zero-probability outcome ever becomes attainable under any trust state. This is the correct formal expression of "trust is a weighting of evidence, not a source of evidence."
5. Standard object: this is an Esscher/exponential tilt, the form used in risk-sensitive control and robust decision theory; γτ plays the role of a risk-sensitivity parameter with sign set by trust.

### M3.3 Option 2 (alternative): rank-dependent probability weighting

Keep P objective and distort the decision weights: EU(a|T) = Σ_o U(o_(i)) · [w(Σ_{j≤i} P(o_(j)); τ(T)) − w(Σ_{j<i} P(o_(j)); τ(T))] with outcomes ordered by U and w(p; τ) a Prelec-type weighting function whose elevation parameter depends on τ. This is closer to cumulative prospect theory and handles rank effects, at the cost of two extra functions, no closed form for the neutral limit beyond w(p;0) = p, and more pre-registration surface. It is legitimate but heavier.

**Recommendation: Option 1.** One new scalar (τ), one amplitude (γ), exact neutral reduction, bounded distortion, monotone behavior, and it composes with the dimensionless mismatch of §M8. Option 2 is retained as a robustness extension for the empirical program.

### M3.4 Exact replacement text (§2.3, Eq. (2))

**DELETE:** Eq. (2) and the sentence "in which the trust vector modulates the subjective probability assigned to outcomes." **REPLACE WITH:**

> For decision-making under a trust state, define the scalar trust index τ(T) = tanh(w·T̃) ∈ (−1,1), with T̃ the trust vector normalized component-wise by its domain reference scales (§2.1; §M8 of the repairs) and w a pre-registered weight vector (default w = e_S). Trust distorts outcome probabilities by an exponential tilt,
>
>     P̃(o|a,T) = P(o|a) exp(γ τ(T) û(o)) / Σ_o' P(o'|a) exp(γ τ(T) û(o')),
>
> with û the within-action standardized utility and γ ≥ 0 a pre-registered amplitude, and actions are evaluated by
>
>     EU(a | T) = Σ_o P̃(o|a,T) · U(o).        (2)
>
> At neutral trust (τ = 0), P̃ = P and (2) is exactly standard expected utility. Positive trust shifts subjective probability toward favorable outcomes; negative trust toward unfavorable ones; the distortion is bounded (|log P̃/P| ≤ γ max|û|), so trust reweights evidence but never manufactures outcomes. Equation (2) is the decision-theoretic bridge between the stability law (1) and observable choice behavior in economic games and financial decisions; (τ, γ, w) are identified from choice data, not from the dynamics.

Also update **whitepaper line 363** ("trust-weighted utility EU(a | T) = …") to quote this Eq. (2).

Classification: **(B) new derivation** (type repair + stated function with proven properties), replacing **(A)-worthy** deletion of the ill-typed equation.

---

## M4. The update-law hierarchy: one master law, three named layers

### M4.1 Master law

```
S_{t+1} = S_t + λ⁺·max(ε_t, 0)·r_t + λ⁻·min(ε_t, 0)·r_t − δ_S·(S_t − S_b)      (ML)
```

with the stack-wide convention **ε_t = V_t − E_t** (positive = confirmation), λ⁺, λ⁻ ≥ 0 the confirmation/betrayal sensitivities, r_t ∈ [0,1] the recognition gate (the fraction of the mismatch registered by the C stage), δ_S ≥ 0 the retention leak (per-step, dimensionless), and S_b the baseline toward which stabilization decays. All quantities dimensionless after §M8 normalization.

### M4.2 Named limits — proofs

**GTT physics layer (r_t ≡ 1, δ_S = 0, λ⁺ = λ⁻ = λ).** Then λ⁺max(ε,0) + λ⁻min(ε,0) = λε for all ε, so (ML) gives

```
S_{t+1} = S_t + λε_t = S_t + λ(V_t − E_t) = S_t − λ(E_t − V_t),
```

which is GTT Eq. (1) verbatim once GTT's ε_GTT = E − V is substituted (§M4.4). Reduction: **exact, proven.** Continuous-time form Ṡ = λε as used in §3.2 follows by the same substitution.

**DOCAS biological layer (λ⁺ = λ⁻ = λ, r_t ∈ [0,1], δ_S > 0, S_b = 0).** (ML) gives

```
S_{t+1} = S_t + λ r_t ε_t − δ_S S_t,
```

which is DOCAS §2.9's S-operator verbatim (with δ_S = 1/τ_S, τ_S the serotonergic retention horizon). Reduction: **exact, proven.** The DOCAS claim "the biological layer reduces to the physics layer by construction" is then literally true in both directions: set r = 1, δ_S = 0.

**TFP protocol layer (λ⁻ > λ⁺, r_t ≡ 1, δ_S ≥ 0).** (ML) gives the asymmetric law

```
S_{t+1} = S_t + λ⁺ ε_t⁺ + λ⁻ ε_t⁻ − δ_S (S_t − S_b),   ε⁺ = max(ε,0), ε⁻ = min(ε,0), λ⁻ > λ⁺.
```

This is the first *exact* statement of TFP's "break/build asymmetry (betrayal updates faster than confirmation accrues)" (TFP §3.6, T8). **Admission required:** the present TFP text asserts the asymmetry only in prose; the protocol's update rule as simulated must be checked against (ML) with λ⁻ > λ⁺, and if the simulation used symmetric λ, T8's deterrence claim needs a re-run under the asymmetric law. The master law makes the asymmetry an explicit, estimable extension: two parameters instead of one, identified separately from positive- and negative-ε subsamples.

### M4.3 What is NOT reducible — exact admission text

The following reductions are **not** true and must not be claimed:

1. GTT's Lyapunov analysis (§3.2) assumes λ⁺ = λ⁻ = λ constant, r = 1, δ_S = 0. With λ⁻ ≠ λ⁺ the flow is piecewise linear (still globally stable — each branch is contracting — but the single-Lyapunov-function proof needs the obvious two-branch extension). **Insert into GTT §7 "Principal limitations":** "(iv) The stability law (1) is the symmetric member of a family: confirmation and betrayal sensitivities (λ⁺, λ⁻) can differ (the break/build asymmetry used at the protocol layer), recognition gates the update (r_t < 1 at the biological layer), and stabilization leaks toward baseline (δ_S > 0). All three extensions preserve global stability of alignment (each branch of the piecewise-linear flow is contracting), but the closed-form quantities of §3.2 — in particular S∞ = S₀ + (λ/μ)ε₀ — hold only in the symmetric, ungated, leak-free limit."
2. DOCAS's composed law "ΔS_t = λ r_t ε_t − δ_S S_t … identical under either sign [of ε]" is true only because λ⁺ = λ⁻ there; under the TFP asymmetry the sign convention matters and must be fixed (done in §M4.4).

### M4.4 Sign convention: ε_t = V_t − E_t, and the GTT find–replace map

Rationale: DOCAS already uses ε = V − E and argues "positive ε is a confirmation" is the natural reading for the leak/gating layers; the stack should not carry two conventions joined by a sign flip. Adopt **ε_t = V_t − E_t everywhere**. In GTT the replacement is purely cosmetic *if applied consistently* (the dynamics are symmetric in ε's sign: both Ṡ and ε̇ are linear in ε):

| GTT location | Current text | Replacement |
|---|---|---|
| Def. 2 (§2.1) | "𝜀𝑡 = 𝐸𝑡 − 𝑉𝑡" | "ε_t = V_t − E_t (validation minus expectation; positive ε is a confirmation)" |
| Stability law (§2.2), Eq. (1) | "Δ𝑆𝑡 = −𝜆 (𝐸𝑡 − 𝑉𝑡) = −𝜆 𝜀𝑡" | "ΔS_t = λ(V_t − E_t) = λε_t" |
| §2.2 text | "the rate at which mismatches degrade (or confirmations restore) stability" | unchanged (signs now read directly off ε) |
| §3.2, Eq. (4) | "d𝑆/d𝑡 = −𝜆 𝜀" | "dS/dt = λε" (the ε-equation dε/dt = −με + ξ is unchanged) |
| §3.2, Prop. 2 derivation | "𝑆∞ = 𝑆0 − (𝜆/𝜇) 𝜀0" | "S∞ = S₀ + (λ/μ)ε₀" |
| §3.2 interpretation | "total stability cost of a perturbation 𝜀0 is (𝜆/𝜇) 𝜀0" | "the total stability displacement from a perturbation ε₀ is (λ/μ)ε₀ — a gain under confirmation (ε₀ > 0), a cost under mismatch (ε₀ < 0)" |
| §6, H1 state equation | "State: 𝑆𝑡 = 𝑆𝑡−1 − 𝜆 𝜀(𝑡 − 1) + 𝜂𝑡" | "State: S_t = S_{t−1} + λ ε(t−1) + η_t" |
| §6, H1 observation equation | "Δ𝐻𝑡 = 𝜆𝐻 𝜀(𝑡) + 𝑢𝑡" | unchanged in form (ε now in the V−E convention) |
| §5 manifestation chain | "𝜀 = 𝐸 − 𝑉 has a common currency" | "ε = V − E has a common currency (§M8 normalization)" |
| §8 conclusion | "Δ𝑆𝑡 = −𝜆 (𝐸𝑡 −𝑉𝑡 )" | "ΔS_t = λ(V_t − E_t)" |
| TFP §2 principle 1 | "Δ𝑆 = −𝜆 (𝐸 − 𝑉 )" | "ΔS = λ(V − E)" |
| whitepaper l.363 | "ΔS = −𝜆(E − V)" | "ΔS = λ(V − E)" |
| DOCAS §2.9 | "the negative of the GTT convention … identical under either sign" | "GTT now uses the same convention; the composed law is identical by construction" |

Classification: the master law and its two exact reductions are **(B) new derivations** (trivial algebra, but new to the stack and load-bearing for cross-paper consistency); the sign-convention unification and limitation admissions are **(A) pure narrowing**.

---

## M5. λ treatment: demoting 0.61, and what scale arguments actually give

### M5.1 The defect

GTT §6 H2: "𝜆 ≈ 0.61 — advanced as a point prediction derived from the theory's internal consistency requirements." There is no derivation of 0.61 anywhere in the stack; "internal consistency requirements" names no argument. The same paragraph correctly states falsification criteria (posterior exclusion, cross-domain invariance failure, adaptive-λ model comparison) — those survive; the derivation claim does not. Meanwhile the stack's text elsewhere uses the phrase "a universal constant claims universality" — that framing must go: a dimensionless population mean of a behavioral coefficient is not a constant of nature, and claiming it invites the correct objection that λ varies with temperament, history, and culture (the paper itself says so: §4.2 on Henrich et al., §2.2 on observer-specific priors).

### M5.2 Exact replacement text for GTT §6 H2

**DELETE:** "H2 (Target coeﬀicient). The population mean trust-sensitivity will lie near 𝜆 ≈ 0.61 — advanced as a point prediction derived from the theory's internal consistency requirements, to be confirmed or refuted. The value is a hypothesis, not an estimate, and no ± interval is asserted."

**REPLACE WITH:**

> **H2 (Target coefficient).** The population mean trust-sensitivity is pre-registered as the target μ_λ = 0.61 with an equivalence corridor [0.46, 0.76]. The point value 0.61 is a target hypothesis, not an estimate and not a derived quantity: no derivation of its value from the theory is claimed. The corridor half-width 0.15 is set by the measurement system's certified recovery tolerance — the stack's estimator pipeline (companion whitepaper, estimator-validation run) recovers planted λ with error ≤ 0.024 against a pre-registered acceptance threshold of 0.15; a prediction stated more finely than the instrument's certified resolution would be untestable, so 0.15 is adopted as the smallest effect size of interest. H2 is corroborated if the hierarchical posterior for μ_λ concentrates inside the corridor at the pre-registered credible level; it is refuted by any of: (i) the posterior excludes [0.46, 0.76]; (ii) cross-domain measurement invariance fails — financial, social, and physiological streams returning population means that differ by more than the corridor width after per-domain normalization (§M8), showing 0.61 to be a property of one instrument; (iii) the constant-λ state equation fails posterior predictive checks against an adaptive-λ extension. **Invariance hypotheses (replacing "universal constant"):** H2a — *measurement invariance*: λ̂ is equal across domains after dimensionless normalization, up to the corridor; H2b — *rank-order stability*: the ordering of individuals' λ_i is stable across domains and across repeated measurement windows, even if levels drift. H2a/H2b, not point equality across settings, are the theory's consistency claims.

**DELETE (§6, final sentence of the H2 identification plan):** "a deliberately narrow corridor, since a universal constant claims universality." **REPLACE WITH:** "a corridor set by instrument resolution, since a target hypothesis must be stated no more finely than the estimator can certify."

**§7 "What the theory does not claim" — REPLACE** "The value 𝜆 ≈ 0.61 is a prediction, not a finding." **WITH:** "The value λ ≈ 0.61 is a pre-registered population-mean target with corridor [0.46, 0.76], not a finding and not a derived constant; the theory's consistency claims are cross-domain measurement invariance and rank-order stability of λ (H2a, H2b), not universality of any point value."

**Claims table G10 — REPLACE WITH:** "μ_λ = 0.61 ∈ corridor [0.46, 0.76] is the pre-registered population-mean target for trust-sensitivity, with invariance hypotheses H2a/H2b — [HYPOTHESIS] — §6 H2; corridor width set by estimator recovery tolerance (whitepaper); falsification criteria stated."

### M5.3 The planted values: explicit statement (insert into GTT §3.6 preamble)

> The parameter values appearing in the stack's simulations — λ = 0.35 (Sim 1, Sim 6, and the DOCAS operator-recovery test, recovered slope 0.348, R² = 0.970), the regression slope 0.174 reported in DOCAS §5.3 (G1, an eligibility-rescaled estimator check, not a λ estimate), and λ = 0.02 (TFP T8, the threshold below which on-off attacks go net-negative under immediate feedback) — are **simulation parameters and recovery checks, not predictions or estimates of any population quantity**. The only prospective empirical claim about λ's value is H2.

### M5.4 A principled characteristic λ scale (sketch, assumptions labeled)

No derivation of 0.61 exists and I do not invent one. What *is* derivable is the natural dimensionless scale of λ in the closed loop — and it lands at order-unity values, which at least shows the target is in the mathematically distinguished regime rather than arbitrary:

**Assumptions (all explicit):** (i) the stack convention ε = V − E; (ii) DOCAS §2.9's loop closure, "S feeds tomorrow's E," in its minimal form E_{t+1} = S_t; (iii) exogenous, slowly varying V (held constant over the transient); (iv) r_t = 1, δ_S = 0, λ⁺ = λ⁻ = λ; (v) unit time step.

**Derivation.** From (ML) with these restrictions, S_{t+1} = S_t + λ(V − E_t) and E_{t+1} = S_t. Eliminating S: writing x_t = E_t − V,

```
x_{t+2} = x_{t+1} − λ x_t,   characteristic equation z² − z + λ = 0,   z = (1 ± √(1 − 4λ))/2.
```

Jury stability conditions for z² − z + λ: λ > 0 and 1 − λ > 0. Hence:

- **Stability boundary λ = 1:** the closed loop is asymptotically stable iff 0 < λ < 1. λ thereby acquires a dimensionless natural range (0,1) — a consistency scale, not a constant.
- **Critical damping λ* = 1/4** (discriminant zero): for λ < 1/4 the return to alignment is monotone; for λ > 1/4 the return *overshoots and rings* with complex roots |z| = √λ and period 2π/atan(√(4λ−1)).
- With the DOCAS leak restored (x_{t+2} = (1−δ_S)x_{t+1} − λx_t) the boundary moves to λ < 1 unchanged at leading Jury order and critical damping becomes λ* = (1−δ_S)²/4.

**Numerical verification (NumPy, direct simulation of the closed loop):** stable for λ ∈ {0.10, 0.25, 0.61, 0.90}, marginal oscillation at λ = 1.0, divergence at λ = 1.10; the overshoot/ringing transition occurs exactly at λ = 1/4; at λ = 0.61 the predicted ringing period 2π/atan(√1.44) ≈ 7.2 steps matches the observed peak spacing (7–8 steps), with envelope decay √λ ≈ 0.78 per step.

**What this gives the paper, honestly:** (a) λ is dimensionless with natural scale 1 — the stack's planted (0.35, 0.02) and target (0.61) values all lie inside the stable range; (b) the target 0.61, being > 1/4, predicts *underdamped* trust dynamics — a falsifiable consequence (overshoot-and-ring after betrayal events with a period set by λ, damping envelope √λ per step) that the empirical program can test independently of the point value; (c) it does **not** single out 0.61. Any text implying otherwise is dishonest.

Classification: H2 rewrite and planted-value disclosure are **(A) pure narrowing**; the closed-loop scale analysis is **(B) a new derivation** (verified), offered as the only principled λ-scale statement the current axioms support.

---

## M6. Fisher–Rao positivity repair: what actually lives on Δ⁴

### M6.1 The defect

§3.1 defines θ_i = T_i/Σ_j T_j and asserts θ ∈ Δ⁴ (the open simplex, θ_i > 0). But T's components are signed: ε (hence the Recognition/Activation readouts and ΔS) can be negative, S drifts sign, and Σ_j T_j can vanish or go negative, making θ_i negative, > 1, or undefined. Every subsequent use — Proposition 1, the Hellinger distance, Sim 1/Sim 6's "random initial conditions on Δ⁴" — silently assumes a non-negative vector the theory never supplies. Two honest fixes:

### M6.2 Option (i) (recommended): the simplex of normalized stage activities

The non-negative object the stack already possesses is DOCAS §2.9's gain/state vector. Define the **stage-activity vector**

```
a(t) = ( Π_t ,  κ_t ,  C_t ,  g_A·f(Δτ_t) ,  λ r_t )   ≥ 0  componentwise,
```

where Π_t > 0 is the error-channel precision (D), κ_t ∈ [0,1] the social-channel coupling (O), C_t = σ(β_C(|ε_t| − θ_C)) ∈ (0,1) the recognition-salience readout (C), g_A·f(Δτ_t) ≥ 0 the activation gain (A), and λ r_t ≥ 0 the gated stabilization throughput (S). Each component is non-negative *by construction* (precisions, couplings, logistic outputs, gains). Normalizing each channel by its pre-registered reference scale â_i (making components dimensionless and commensurable, §M8) and then by the sum,

```
θ_i(t) = ã_i(t) / Σ_j ã_j(t),   ã_i = a_i/â_i,   ⇒  θ ∈ Δ⁴,
```

gives a genuine point of the open simplex whenever all stages are active, and of the closed simplex otherwise. **Interpretation:** θ is the *stage-mix profile* — the distribution of current processing share across the five functional stages — and the Fisher–Rao metric on θ measures the statistical distinguishability of two stage-mix profiles, i.e. how many independent stage-resolved observations are needed to tell two trust states apart. This is exactly what the theory needs: a canonical geometry for comparing trust states and a Cramér–Rao precision limit for estimating them. Proposition 1 and its consequences then go through verbatim, with θ now well-defined.

### M6.3 Option (ii) (alternative): amplitude map θ = x²

Map the signed state to the unit 4-sphere x = T/‖T‖₂ and set θ_i = x_i². Then θ_i ≥ 0, Σθ_i = 1 automatically, and (θ ↦ 2√θ) is the standard identification of the Fisher–Rao simplex with the positive orthant of S⁴ (the paper's own Hellinger distance 2 arccos Σ√(θ_iθ'_i) is the sphere's geodesic distance). Cost: the map is many-to-one (each orthant of S⁴ maps to the same θ), so component *signs* are discarded — the geometry cannot distinguish +C from −C, i.e. mismatch salience from its mirror. Acceptable for geometry, wrong for dynamics. Retained as a fallback if stage activities prove unmeasurable.

**Recommendation: Option (i).** It uses objects DOCAS already defines, keeps sign information in the dynamics (where it belongs, in (S, ε)), and gives Δ⁴ a measurement interpretation.

### M6.4 Exact replacement text (§3.1, opening paragraph and licensing sentence)

**DELETE:** "Normalize the trust state by writing 𝜃𝑖 = 𝑇𝑖 / ∑𝑗 𝑇𝑗 , so 𝜃 ∈ Δ4 …" through "…resolves into one stage." **REPLACE WITH:**

> The signed trust vector T does not itself lie on a simplex; its components can be negative and their sum can vanish. The simplex coordinate is defined instead on the **stage-activity vector** a(t) = (Π_t, κ_t, C_t, g_A f(Δτ_t), λ r_t) ≥ 0, whose components — error-channel precision, social coupling, recognition salience, activation gain, gated stabilization throughput — are non-negative by construction (DOCAS §2.9). Normalize per channel by pre-registered reference scales (ã_i = a_i/â_i) and write θ_i = ã_i/Σ_j ã_j, so θ ∈ Δ⁴ whenever all stages are active. Treat θ as the parameter of a categorical distribution over the five stages: the stage-mix profile according to which a single stage-resolved observation of the trust process resolves into one stage. The Fisher–Rao metric below is therefore a geometry **for comparing stage-mix profiles and bounding the precision with which they can be estimated** — nothing more; it confers no dynamics and no dimensional normalization by itself.

**DELETE (§1.1 proof obligation (2)):** "components are non-dimensionalized via the Fisher metric (§3.1)." **REPLACE WITH:** "components are non-dimensionalized by per-domain reference scales (Def. 2a, §2.1; repairs §M8); the Fisher metric then supplies a canonical geometry on the normalized stage-mix profiles."

**Delete** the parallel false claim wherever it recurs ("non-dimensionalized via the Fisher metric"): it confuses a Riemannian metric on a probability simplex with unit normalization; the two operations are independent and both are needed.

**Simulation note for the stack's writers:** Sim 1/Sim 6's "random initial conditions on Δ⁴" are unaffected in code (they sampled simplex points directly) but their *interpretation* changes: trajectories are stage-mix profiles θ(t), and the stability law acts on the underlying (S, ε) with θ a derived readout. One sentence to that effect should be added to §3.6.

Classification: **(B) new derivation** (the activity simplex construction), plus **(A) narrowing** of the licensing claims.

---

## M7. PAS phase fix: full-circle phases from normalized mismatch

### M7.1 The defect

Def. 4 assigns θ_k ∝ atan(ε_k) ∈ (−π/2, π/2). Two failures: (i) phases occupy only half the circle, so the Kuramoto order parameter computed from them is biased upward even at zero coupling — NumPy check: with normalized mismatches drawn from a standard Cauchy (heavy-tailed, per TFP T5b's own stylized fact), atan-assignment gives R = 0.63 at K = 0, i.e. the "incoherent control" would report strong coherence; (ii) K_c = 2/(πg(0)) is the mean-field threshold for oscillators distributed around the full circle with a unimodal symmetric natural-frequency density — assumptions the half-circle assignment violates. (TFP's reported isolated control R = 0.032 must therefore have used raw uniform phases, not the atan map; if so, Def. 4's assignment has never actually been exercised, which should be said.)

### M7.2 The repair: stereographic (wrapped-Cauchy) assignment

```
θ_k = 2 arctan( ε̃_k )  ∈ (−π, π],     ε̃_k = (V_k − E_k)/s_k   (dimensionless, §M8).
```

Properties (verified): (i) full circle: θ covers (−π, π), with θ = 0 at perfect alignment (ε̃ = 0) and θ → ±π as mismatch saturates — "maximally distrusting" and "maximally over-validated" meet at the antipode, which is the correct topology for a *circular* alignment variable; (ii) **exact distribution identity:** if ε̃ ~ Cauchy(0, 1), then θ is *uniform* on (−π, π) (the stereographic projection of the Cauchy law; KS test on N = 2000 draws: stat 0.028, p = 0.088 — consistent with uniform), so a population of unaligned nodes with heavy-tailed normalized mismatches has R ≈ 1/√N ≈ 0 at K = 0 — the incoherent baseline the Kuramoto analysis requires (NumPy: R = 0.026 at N = 2000, matching the finite-size floor 1/√N = 0.022); (iii) if ε̃ ~ Cauchy(0, s′) with s′ ≠ 1, θ is wrapped-Cauchy with mean resultant length ρ = |1 − s′|/(1 + s′), interpolating smoothly between concentrated-at-zero (s′ → 0, aligned population) and uniform (s′ = 1) — so population alignment maps onto the standard wrapped-Cauchy concentration parameter, giving PAS a principled null model.

### M7.3 Restating K_c

K_c = 2/(πg(0)) is a **mean-field reference value**, valid under: all-to-all coupling, N → ∞, time-stationary unimodal symmetric g(ω), and full-circle phases. The paper already concedes the network correction (§7, limitation (ii)); what must change is the claim that the formula yields "a falsifiable form of prediction." Exact replacement:

**DELETE (Def. 4):** "with phase assigned from each node's residual mismatch, 𝜃𝑘 ∝ atan(𝜀𝑘 )." **REPLACE WITH:** "with phase assigned from each node's normalized residual mismatch by the stereographic map θ_k = 2 arctan(ε̃_k), ε̃_k = (V_k − E_k)/s_k, covering the full circle with θ = 0 at alignment; under heavy-tailed (Cauchy) normalized mismatches the unaligned population is uniform on the circle, giving R ≈ 1/√N at zero coupling — the correct incoherent baseline."

**DELETE (§3.4):** "Equation (10) then yields a falsifiable form of prediction: trust networks should exhibit a threshold…". **REPLACE WITH:** "Equation (10) is a mean-field reference value under all-to-all coupling, N → ∞, unimodal symmetric g(ω), and full-circle phases; on sparse weighted trust networks the true threshold will differ by network corrections, so (10) supplies the *functional form* of the hypothesis (a continuous onset of PAS coherence at a critical feedback quality), not a numerical prediction."

Classification: **(B) new derivation** (stereographic assignment + distributional identity, verified numerically), plus **(A) narrowing** of the K_c claim.

---

## M8. Dimensional analysis: the dimensionless mismatch and the common currency

### M8.1 Construction

For each measurement domain d (financial, social, physiological), define the **domain scale** s_d = RMSE of the expectation distribution — concretely, s_d² = E_t[(V_t − E_t)²] estimated on a pre-registered calibration window (rolling or held-out). Then

```
ε̃_t = (V_t − E_t)/s_d ,   S̃_t = S_t/s_d ,   ε̃, S̃ dimensionless.
```

The master law (ML) in dimensionless form:

```
S̃_{t+1} = S̃_t + λ⁺ max(ε̃,0) r_t + λ⁻ min(ε̃,0) r_t − δ_S (S̃_t − S̃_b),
```

with **λ⁺, λ⁻, r_t, δ_S all dimensionless** (δ_S per unit step; in continuous time δ_S has units 1/time and the law is divided by the step). λ is thereby dimensionless and cross-domain comparable — which is exactly what makes the invariance hypotheses H2a/H2b (§M5) well-posed: without this normalization, "the same λ across domains" would be comparing dollars-per-dollar-mismatch to seconds-per-second-mismatch, a category error.

### M8.2 Unit check across the three layers

| Layer | Equation | Units check |
|---|---|---|
| GTT physics (r=1, δ_S=0, λ⁺=λ⁻=λ) | ΔS̃ = λε̃ | [dimensionless] = [–]·[–] ✓; λ dimensionless |
| GTT continuous (§3.2) | dε̃/dt = −με̃ | μ has units 1/time ✓; Var_stat(ε̃) = σ̃²/2μ dimensionless with σ̃² in 1/time ✓ |
| ψ model (M2) | dε̃ = −(μ+ψ(m))ε̃ dt + σ̃ dW | ψ : 1/time, m dimensionless ✓ |
| DOCAS biological | S̃_{t+1} = S̃_t + λ r_t ε̃_t − δ_S S̃_t | r_t, δ_S dimensionless per step; τ_S = 1/δ_S in steps ✓ |
| TFP protocol | λ⁻ > λ⁺ asymmetric, per event | per-event step; λ's dimensionless, comparable to GTT's only after matching the observation cadence (events vs. fixed windows) — a pre-registration obligation, stated below |

**Cadence caveat (must be stated):** a per-event λ (TFP) and a per-unit-time λ (GTT Kalman form) are the same parameter only if event rates are stationary and stated; the pre-registration must fix the observation cadence per domain so the dimensionless λ's are commensurable.

### M8.3 Exact replacement text (Def. 2's "common currency" passage)

**DELETE (Def. 2, §2.1):** "…expressed in a common currency (probability, utility, or monetary value — in financial contexts, 'a dollar is a dollar' supplies the shared baseline)." **REPLACE WITH:**

> expressed in the domain's own outcome units and then made dimensionless: **Definition 2a (normalized mismatch).** For each domain d with expectation distribution's root-mean-square scale s_d (estimated on a pre-registered calibration window), ε̃_t = (V_t − E_t)/s_d. The normalized mismatch is dimensionless, so the trust-sensitivity λ multiplying it is dimensionless and comparable across domains — this normalization, not any natural identity of units, is what 'common currency' means in this theory. In the financial application s_d is the dollar-RMSE of the predicted outcome distribution: a dollar mismatch is compared to the dollar scale of what was predictable, and only that ratio enters the dynamics. Cross-domain equality of λ is then an empirical hypothesis (H2a, §6), not a definitional convenience.

**DELETE (§5):** "the shared value baseline is objective — a dollar is a dollar, so 𝜀 = 𝐸 − 𝑉 has a common currency in the literal sense." **REPLACE WITH:** "outcomes are recorded in dollars with an estimable expectation scale, so the normalized mismatch ε̃ = (V − E)/s_fin is directly and objectively computable — finance is the domain where the Definition 2a normalization is least contestable, which is the principled reason it is the first application."

Classification: **(B) new derivation** (the normalization construction and the cross-layer unit audit), replacing the hand-wave — effectively also a narrowing of the "common currency" rhetoric.

---

## M9. Summary of classifications, and what could NOT be honestly repaired

| # | Repair | Class | Core content |
|---|---|---|---|
| M1 | κ / Def. 3 / H1 | **A (narrowing)** | Divergence of the stated flow is the constant −μ (proven); bifurcation/void–chaos claims deleted; κ retired; replacement text for abstract, H1, H0, Def. 3, Fig. 1(a), §7 |
| M2 | Field equation | **A (deletion) + B (ψ model)** | Continuum equation deleted; ψ defined as observation-salience-dependent dissipation with units, regularity, ψ→0 conditions, and derived signatures (Var σ²/(2(μ+ψ)), critical slowing as ψ→−μ⁺); TFP §1.2/§4 uses ratified |
| M3 | EU bridge | **B (new derivation)** | Exponential-tilt P̃(o|a,T) with proven properties (neutral reduction, monotonicity, bounded distortion); rank-dependent alternative stated; tilt recommended |
| M4 | Update-law hierarchy | **B (master law) + A (admissions)** | Master law (ML); GTT and DOCAS reductions proven exact; TFP asymmetry made explicit with a re-run caveat; sign convention ε = V − E fixed stack-wide with a find–replace table |
| M5 | λ = 0.61 | **A (demotion) + B (scale sketch)** | H2 rewritten as corridor target [0.46, 0.76] with width tied to the estimator's certified 0.15 recovery tolerance; "universal constant" replaced by invariance hypotheses H2a/H2b; planted values 0.35/0.174/0.02 disclosed as simulation parameters; closed-loop analysis gives λ's natural range (0,1) and critical damping at 1/4 (Jury + simulation verified) — explicitly **not** a derivation of 0.61 |
| M6 | Fisher–Rao positivity | **B (construction) + A (licensing)** | Stage-activity simplex θ from DOCAS's non-negative gains (recommended); amplitude map θ = x² as fallback; §3.1 licensing rewritten (metric = distinguishability of stage-mix profiles); "non-dimensionalized via the Fisher metric" corrected |
| M7 | PAS phase | **B (new derivation) + A (K_c narrowing)** | θ = 2 arctan(ε̃) covers the full circle; Cauchy→uniform identity verified (KS p = 0.088); R(K=0) drops from 0.63 (broken atan) to ≈ 1/√N; K_c restated as mean-field reference value with assumptions |
| M8 | Dimensional analysis | **B (construction)** | ε̃ = (V−E)/s_d with s_d = expectation RMSE; λ dimensionless; unit audit across all three layers; Def. 2a replaces "a dollar is a dollar"; cadence-commensurability caveat added |

### Things I could not repair honestly

1. **No bifurcation in the single-agent dynamics.** No definition or minimal extension consistent with the paper's stated axioms produces the claimed κ-sign-change critical point. The author's "divergence then convergence" intuition is not realizable in the stated dynamics (contraction is uniform at rate μ). The only genuine transition available — overdamped vs. underdamped return in the closed loop (M5.4) — is a *qualitative change of approach to* the attractor, not a void/chaos boundary, and I have placed it at λ-scale analysis where it belongs rather than dressing it as H1.
2. **No derivation of 0.61.** None exists in the stack and none was constructible. The corridor target + invariance hypotheses (M5.2) is the strongest defensible statement; the closed-loop scale argument shows the target lies in the underdamped regime (a falsifiable consequence) but does not select its value.
3. **The field equation ∇·T + ψ·H(T) = χ(S ⊗ E).** Not definable on the theory's state space; deleted, with its one salvageable idea (ψ) rebuilt from the OU dynamics.
4. **∇·T on the five-vector T.** Type-ill-defined throughout (M1.2, Defect 1); retired everywhere.
5. **TFP T8's asymmetry provenance.** The master law can express the break/build asymmetry, but whether TFP's *reported simulations* actually implemented λ⁻ > λ⁺ cannot be settled from the paper text; flagged for the simulation agent to check and re-run if needed (M4.2, M4.3).

### Cross-agent handoffs (for the lead)

- **Wave-2 simulation agent:** implement (ML) of §M4.1 with named layer presets; phase assignment θ = 2 arctan(ε̃) (§M7.2) — and re-baseline the isolated control (the atan map inflates R at K = 0 to ≈ 0.63); OU-with-ψ dynamics for the chilling/critical-slowing battery (Var, lag-1 autocorrelation vs. m); closed-loop λ-scan to exhibit the 1/4 critical-damping boundary and the √λ ringing envelope (§M5.4); verify TFP T8 under explicit λ⁻ > λ⁺.
- **GTT writer:** paste blocks at Def. 2/2a, Def. 3, Eq. (1)–(2), §3.1 opening, §3.2 (S∞ sign + interpretation), §3.3 final paragraph, §3.4 Def. 4 + K_c paragraph, §6 H1–H2, §7 (limitations (iv), "does not claim" bullets, claims rows G5, G10), §8 conclusion, Figs. 1(a) caption; sign-convention table §M4.4.
- **DOCAS writer:** one-line change in §2.9 (conventions now identical); add "stage-activity vector" terminology pointer to §M6.2.
- **TFP writer:** §1.2 ψ sentence sharpened per §M2.4; §2 principle 1 sign; state whether T8 simulations used λ⁻ > λ⁺ (per §M4.3).
- **Whitepaper writer:** line 363 updates (sign + EU form); the λ̂-recovery tolerance 0.15 is now load-bearing for the H2 corridor — keep the certified value versioned.
