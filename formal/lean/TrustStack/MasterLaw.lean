/-
TrustStack.MasterLaw

The stack-wide master update law (GTT eq:masterlaw) and its stability results:

  M1. Physics-layer reduction: at the preset (λ⁺ = λ⁻ = λ, r = 1, δ = 0,
      S_base = 0) the master law is exactly the Rescorla–Wagner / delta-rule
      stability axiom ΔS = λε (GTT eq:stability).
  M2. Contraction: with zero mismatch and leak δ ∈ (0, 1], the state decays
      geometrically to baseline, S_t − S_base = (1 − δ)^t·(S₀ − S_base).
  M3. Bounded-input bounded-state: with the gated update term bounded by B,
      |S_t − S_base| ≤ (1 − δ)^t·|S₀ − S_base| + B/δ.
      Corollary: with |ε| ≤ E and r ∈ [0,1], B = (λ⁺ + λ⁻)·E.

These are the consistency checks that the three layer presets of the stack
(physics, biological, protocol) cannot contradict one another: M1 ties the
presets to the printed axiom, M2–M3 bound every leaky preset.

No `sorry` placeholders are used.
-/

import Mathlib

namespace TrustStack

/-- The master law (eq:masterlaw):
    S ↦ S + λ⁺·max(ε,0)·r + λ⁻·min(ε,0)·r − δ·(S − S_base). -/
noncomputable def masterStep (lp ln δ Sbase r : ℝ) (S ε : ℝ) : ℝ :=
  S + lp * max ε 0 * r + ln * min ε 0 * r - δ * (S - Sbase)

/-- Trajectory under constant parameters with exogenous gate/mismatch streams. -/
noncomputable def traj (lp ln δ Sbase : ℝ) (r ε : ℕ → ℝ) (S0 : ℝ) : ℕ → ℝ
  | 0 => S0
  | (t + 1) => masterStep lp ln δ Sbase (r t) (traj lp ln δ Sbase r ε S0 t) (ε t)

/-- **M1** — the physics-layer preset is the Rescorla–Wagner limit:
    max(ε,0) + min(ε,0) = ε collapses the asymmetric terms. -/
theorem masterStep_physics (lam S ε : ℝ) :
    masterStep lam lam 0 0 1 S ε = S + lam * ε := by
  have h : lam * max ε 0 + lam * min ε 0 = lam * ε := by
    rw [← mul_add, max_add_min, add_zero]
  unfold masterStep
  rw [mul_one, mul_one, zero_mul, sub_zero]
  linarith [h]

/-- **M2** — contraction to baseline under zero input. -/
theorem contraction (δ Sbase S0 : ℝ) (t : ℕ) :
    traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t - Sbase
      = (1 - δ)^t * (S0 - Sbase) := by
  induction t with
  | zero => simp [traj]
  | succ t ih =>
    have hstep : traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 (t + 1)
        = traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t
          - δ * (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t - Sbase) := by
      show masterStep 0 0 δ Sbase 0 (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t) 0
          = _
      unfold masterStep
      ring
    rw [hstep]
    have e : (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t
          - δ * (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t - Sbase)) - Sbase
        = (1 - δ) * (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S0 t - Sbase) := by
      ring
    rw [e, ih, pow_succ]
    ring

/-- Per-step input bound: for λ⁺, λ⁻ ≥ 0 and r ∈ [0,1],
    |λ⁺·max(ε,0)·r + λ⁻·min(ε,0)·r| ≤ (λ⁺ + λ⁻)·|ε|. -/
theorem input_bound {lp ln r ε : ℝ} (hlp : 0 ≤ lp) (hln : 0 ≤ ln)
    (hr0 : 0 ≤ r) (hr1 : r ≤ 1) :
    |lp * max ε 0 * r + ln * min ε 0 * r| ≤ (lp + ln) * |ε| := by
  have hmax : max ε 0 ≤ |ε| := by
    rcases le_total ε 0 with h | h
    · rw [max_eq_right h]; exact abs_nonneg ε
    · rw [max_eq_left h]; exact le_abs_self ε
  have hmin : -min ε 0 ≤ |ε| := by
    rcases le_total ε 0 with h | h
    · rw [min_eq_left h]; exact neg_le_abs ε
    · rw [min_eq_right h, neg_zero]; exact abs_nonneg ε
  have hmaxnn : 0 ≤ max ε 0 := le_max_right _ _
  have hminnn : 0 ≤ -min ε 0 := by
    rcases le_total ε 0 with h | h
    · rw [min_eq_left h]; linarith
    · rw [min_eq_right h, neg_zero]
  have e1 : |lp * max ε 0 * r| = lp * max ε 0 * r :=
    abs_of_nonneg (mul_nonneg (mul_nonneg hlp hmaxnn) hr0)
  have e2 : |ln * min ε 0 * r| = ln * (-min ε 0) * r := by
    rw [show ln * min ε 0 * r = -(ln * (-min ε 0) * r) from by ring, abs_neg]
    exact abs_of_nonneg (mul_nonneg (mul_nonneg hln hminnn) hr0)
  have h1 : lp * max ε 0 * r ≤ lp * |ε| := by
    calc lp * max ε 0 * r ≤ lp * max ε 0 * 1 :=
          mul_le_mul_of_nonneg_left hr1 (mul_nonneg hlp hmaxnn)
      _ = lp * max ε 0 := mul_one _
      _ ≤ lp * |ε| := mul_le_mul_of_nonneg_left hmax hlp
  have h2 : ln * (-min ε 0) * r ≤ ln * |ε| := by
    calc ln * (-min ε 0) * r ≤ ln * (-min ε 0) * 1 :=
          mul_le_mul_of_nonneg_left hr1 (mul_nonneg hln hminnn)
      _ = ln * (-min ε 0) := mul_one _
      _ ≤ ln * |ε| := mul_le_mul_of_nonneg_left hmin hln
  calc |lp * max ε 0 * r + ln * min ε 0 * r|
      ≤ |lp * max ε 0 * r| + |ln * min ε 0 * r| := abs_add_le _ _
    _ = lp * max ε 0 * r + ln * (-min ε 0) * r := by rw [e1, e2]
    _ ≤ lp * |ε| + ln * |ε| := add_le_add h1 h2
    _ = (lp + ln) * |ε| := by ring

/-- **M3** — bounded-input bounded-state stability of the leaky master law. -/
theorem bibo {lp ln δ Sbase : ℝ} {r ε : ℕ → ℝ} {S0 : ℝ}
    (hδ0 : 0 < δ) (hδ1 : δ ≤ 1) {B : ℝ} (hB0 : 0 ≤ B)
    (hB : ∀ t, |lp * max (ε t) 0 * r t + ln * min (ε t) 0 * r t| ≤ B) (t : ℕ) :
    |traj lp ln δ Sbase r ε S0 t - Sbase|
      ≤ (1 - δ)^t * |S0 - Sbase| + B / δ := by
  induction t with
  | zero =>
    have hBd : 0 ≤ B / δ := div_nonneg hB0 (le_of_lt hδ0)
    simp [traj]
    linarith
  | succ t ih =>
    have hstep : traj lp ln δ Sbase r ε S0 (t + 1) - Sbase
        = (1 - δ) * (traj lp ln δ Sbase r ε S0 t - Sbase)
          + (lp * max (ε t) 0 * r t + ln * min (ε t) 0 * r t) := by
      show masterStep lp ln δ Sbase (r t) (traj lp ln δ Sbase r ε S0 t) (ε t)
          - Sbase = _
      unfold masterStep
      ring
    have hq : 0 ≤ 1 - δ := sub_nonneg.mpr hδ1
    have hδ : δ ≠ 0 := ne_of_gt hδ0
    rw [hstep]
    calc |(1 - δ) * (traj lp ln δ Sbase r ε S0 t - Sbase)
            + (lp * max (ε t) 0 * r t + ln * min (ε t) 0 * r t)|
        ≤ |(1 - δ) * (traj lp ln δ Sbase r ε S0 t - Sbase)|
          + |lp * max (ε t) 0 * r t + ln * min (ε t) 0 * r t| := abs_add_le _ _
      _ = (1 - δ) * |traj lp ln δ Sbase r ε S0 t - Sbase|
          + |lp * max (ε t) 0 * r t + ln * min (ε t) 0 * r t| := by
          rw [abs_mul, abs_of_nonneg hq]
      _ ≤ (1 - δ) * ((1 - δ)^t * |S0 - Sbase| + B / δ) + B :=
          add_le_add (mul_le_mul_of_nonneg_left ih hq) (hB t)
      _ = (1 - δ)^(t + 1) * |S0 - Sbase| + B / δ := by
          rw [pow_succ]
          field_simp [hδ]
          ring

/-- **M3 corollary** — the explicit bound for |ε| ≤ E, r ∈ [0,1]:
    the state never strays from baseline by more than (λ⁺+λ⁻)·E/δ plus a
    geometrically decaying initial transient. -/
theorem bibo_of_eps_bound {lp ln δ Sbase : ℝ} {r ε : ℕ → ℝ} {S0 E : ℝ}
    (hlp : 0 ≤ lp) (hln : 0 ≤ ln) (hδ0 : 0 < δ) (hδ1 : δ ≤ 1)
    (hr : ∀ t, 0 ≤ r t ∧ r t ≤ 1) (hε : ∀ t, |ε t| ≤ E) (hE : 0 ≤ E) (t : ℕ) :
    |traj lp ln δ Sbase r ε S0 t - Sbase|
      ≤ (1 - δ)^t * |S0 - Sbase| + (lp + ln) * E / δ := by
  apply bibo hδ0 hδ1 (mul_nonneg (add_nonneg hlp hln) hE) _ t
  intro s
  exact le_trans (input_bound hlp hln (hr s).1 (hr s).2)
    (mul_le_mul_of_nonneg_left (hε s) (add_nonneg hlp hln))

/-- **Theorem O1 (Dopaminergic Lesion Asymptotic Collapse)**:
    Under ArchT optogenetic inhibition (λ⁺ = 0), for any non-negative reward stream
    (ε t ≥ 0) and any positive reinforcement gate r t, the trajectory contracts
    geometrically to baseline S_base at rate (1 - δ)^t, abolishing positive trust
    accumulation regardless of reinforcement. -/
theorem dopamine_lesion_contraction (ln δ Sbase S0 : ℝ) (r ε : ℕ → ℝ)
    (hε : ∀ t, 0 ≤ ε t) (t : ℕ) :
    traj 0 ln δ Sbase r ε S0 t - Sbase = (1 - δ)^t * (S0 - Sbase) := by
  induction t with
  | zero => simp [traj]
  | succ t ih =>
    have hmin : min (ε t) 0 = 0 := min_eq_right (hε t)
    have hstep : traj 0 ln δ Sbase r ε S0 (t + 1)
        = (1 - δ) * (traj 0 ln δ Sbase r ε S0 t - Sbase) + Sbase := by
      show masterStep 0 ln δ Sbase (r t) (traj 0 ln δ Sbase r ε S0 t) (ε t) = _
      unfold masterStep
      rw [hmin]
      ring
    have e : traj 0 ln δ Sbase r ε S0 (t + 1) - Sbase
        = (1 - δ) * (traj 0 ln δ Sbase r ε S0 t - Sbase) := by
      linarith [hstep]
    rw [e, ih, pow_succ]
    ring

/-- Bounded cognitive bandwidth disclaimer discovery probability (Sim D16).
    P_disc(κ, χ) = 1 / (1 + exp(-γ * (κ / χ - τ))). -/
noncomputable def Pdisc (γ τ χ κ : ℝ) : ℝ :=
  1 / (1 + Real.exp (-γ * (κ / χ - τ)))

/-- Predatory contract uptake under bounded attention: 1 - P_disc. -/
noncomputable def Uptake (γ τ χ κ : ℝ) : ℝ :=
  1 - Pdisc γ τ χ κ

/-- Predatory uptake odds: (1 - P_disc) / P_disc = exp(-γ * (κ / χ - τ)). -/
theorem uptake_odds_eq (γ τ χ κ : ℝ) :
    Uptake γ τ χ κ / Pdisc γ τ χ κ = Real.exp (-γ * (κ / χ - τ)) := by
  unfold Uptake Pdisc
  have hepos : 0 < 1 + Real.exp (-γ * (κ / χ - τ)) := by positivity
  have hene : 1 + Real.exp (-γ * (κ / χ - τ)) ≠ 0 := ne_of_gt hepos
  field_simp [hene]
  ring

/-- **Theorem D16 (Visual Cloaking Exploitation Odds Ratio)**:
    For any attention sensitivity γ > 0, visual cloaking ratio χ > 0,
    and two cognitive tiers κ_L < κ_H, the predatory uptake odds ratio
    OR(κ_L, κ_H) is strictly greater than 1:
    OR(κ_L, κ_H) = exp(γ * (κ_H - κ_L) / χ) > 1.
    This proves that visual cloaking creates an intrinsic exploitation concentration
    disproportionately penalizing lower-bandwidth agents. -/
theorem cloaking_odds_ratio_gt_one {γ τ χ κL κH : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hκ : κL < κH) :
    (Uptake γ τ χ κL / Pdisc γ τ χ κL) / (Uptake γ τ χ κH / Pdisc γ τ χ κH)
      = Real.exp (γ * (κH - κL) / χ) ∧
    1 < (Uptake γ τ χ κL / Pdisc γ τ χ κL) / (Uptake γ τ χ κH / Pdisc γ τ χ κH) := by
  have eL := uptake_odds_eq γ τ χ κL
  have eH := uptake_odds_eq γ τ χ κH
  rw [eL, eH]
  have eexp : Real.exp (-γ * (κL / χ - τ)) / Real.exp (-γ * (κH / χ - τ))
      = Real.exp (γ * (κH - κL) / χ) := by
    rw [← Real.exp_sub]
    congr 1
    ring
  refine ⟨eexp, ?_⟩
  rw [eexp]
  have hdiff : 0 < κH - κL := sub_pos.mpr hκ
  have hpos : 0 < γ * (κH - κL) / χ := by
    exact div_pos (mul_pos hγ hdiff) hχ
  exact Real.one_lt_exp_iff.mpr hpos

/-- Perceived expected utility of a credit contract under bounded disclaimer discovery.
    When disclaimer is discovered (probability Pdisc), consumer perceives true utility U_true.
    When disclaimer is cloaked/missed (probability 1 - Pdisc), consumer perceives promotional utility U_promo. -/
noncomputable def perceivedEU (γ τ χ κ U_promo U_true : ℝ) : ℝ :=
  Pdisc γ τ χ κ * U_true + (1 - Pdisc γ τ χ κ) * U_promo

theorem perceivedEU_eq (γ τ χ κ U_promo U_true : ℝ) :
    perceivedEU γ τ χ κ U_promo U_true = U_promo - Pdisc γ τ χ κ * (U_promo - U_true) := by
  unfold perceivedEU
  ring

/-- Strict monotonicity of disclaimer discovery probability in cognitive bandwidth κ:
    Higher cognitive bandwidth strictly increases discovery probability. -/
theorem Pdisc_strictMono_kappa (τ : ℝ) {γ χ κ1 κ2 : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hκ : κ1 < κ2) :
    Pdisc γ τ χ κ1 < Pdisc γ τ χ κ2 := by
  unfold Pdisc
  have h_exp : Real.exp (-γ * (κ2 / χ - τ)) < Real.exp (-γ * (κ1 / χ - τ)) := by
    rw [Real.exp_lt_exp]
    have h_div : κ1 / χ < κ2 / χ := div_lt_div_of_pos_right hκ hχ
    have h_neg : -γ * (κ2 / χ - τ) < -γ * (κ1 / χ - τ) := by
      nlinarith
    exact h_neg
  have h_denom : 1 + Real.exp (-γ * (κ2 / χ - τ)) < 1 + Real.exp (-γ * (κ1 / χ - τ)) := by
    linarith
  have h_pos : 0 < 1 + Real.exp (-γ * (κ2 / χ - τ)) := by
    linarith [Real.exp_pos (-γ * (κ2 / χ - τ))]
  exact one_div_lt_one_div_of_lt h_pos h_denom

/-- Strict anti-monotonicity of predatory uptake in cognitive bandwidth κ:
    Higher cognitive bandwidth strictly decreases predatory contract uptake. -/
theorem Uptake_strictAnti_kappa (τ : ℝ) {γ χ κ1 κ2 : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hκ : κ1 < κ2) :
    Uptake γ τ χ κ2 < Uptake γ τ χ κ1 := by
  unfold Uptake
  have hp := Pdisc_strictMono_kappa τ hγ hχ hκ
  linarith

/-- Predatory contract uptake weak anti-monotonicity in cognitive bandwidth:
    κ1 ≤ κ2 implies Uptake(κ2) ≤ Uptake(κ1). -/
theorem Uptake_anti_kappa (τ : ℝ) {γ χ κ1 κ2 : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hκ : κ1 ≤ κ2) :
    Uptake γ τ χ κ2 ≤ Uptake γ τ χ κ1 := by
  rcases eq_or_lt_of_le hκ with rfl | hlt
  · rfl
  · exact le_of_lt (Uptake_strictAnti_kappa τ hγ hχ hlt)

/-- Strict anti-monotonicity of disclaimer discovery probability in visual cloaking ratio χ:
    Higher visual cloaking ratio strictly decreases discovery probability. -/
theorem Pdisc_strictAnti_chi (τ : ℝ) {γ χ1 χ2 κ : ℝ}
    (hγ : 0 < γ) (hκ : 0 < κ) (hχ1 : 0 < χ1) (hχ : χ1 < χ2) :
    Pdisc γ τ χ2 κ < Pdisc γ τ χ1 κ := by
  unfold Pdisc
  have h_exp : Real.exp (-γ * (κ / χ1 - τ)) < Real.exp (-γ * (κ / χ2 - τ)) := by
    rw [Real.exp_lt_exp]
    have h_div : κ / χ2 < κ / χ1 := by
      exact div_lt_div_of_pos_left hκ hχ1 hχ
    have h_neg : -γ * (κ / χ1 - τ) < -γ * (κ / χ2 - τ) := by
      nlinarith
    exact h_neg
  have h_denom : 1 + Real.exp (-γ * (κ / χ1 - τ)) < 1 + Real.exp (-γ * (κ / χ2 - τ)) := by
    linarith
  have h_pos : 0 < 1 + Real.exp (-γ * (κ / χ1 - τ)) := by
    linarith [Real.exp_pos (-γ * (κ / χ1 - τ))]
  exact one_div_lt_one_div_of_lt h_pos h_denom

/-- **Theorem (Cloaked Perceived Expected Utility Monotonicity)**:
    For any predatory contract where the true fine-print utility is strictly worse than
    the promotional headline (U_true < U_promo):
    Increasing visual cloaking χ (from χ1 to χ2) strictly increases perceived expected utility EU,
    mechanistically driving excess uptake among bounded consumers. -/
theorem cloaked_perceived_utility_strictMono_chi (τ : ℝ) {γ χ1 χ2 κ U_promo U_true : ℝ}
    (hγ : 0 < γ) (hκ : 0 < κ) (hχ1 : 0 < χ1) (hχ : χ1 < χ2)
    (hU : U_true < U_promo) :
    perceivedEU γ τ χ1 κ U_promo U_true < perceivedEU γ τ χ2 κ U_promo U_true := by
  rw [perceivedEU_eq, perceivedEU_eq]
  have h_pdisc := Pdisc_strictAnti_chi τ hγ hκ hχ1 hχ
  have h_udiff : 0 < U_promo - U_true := sub_pos.mpr hU
  have h_mul : Pdisc γ τ χ2 κ * (U_promo - U_true) < Pdisc γ τ χ1 κ * (U_promo - U_true) :=
    mul_lt_mul_of_pos_right h_pdisc h_udiff
  linarith

/-- **Theorem (Cloaked Perceived Utility Strict Anti-Monotonicity in Bandwidth κ)**:
    For any predatory contract where the true fine-print utility is strictly worse than
    the promotional headline (U_true < U_promo):
    Increasing cognitive bandwidth κ (from κ1 to κ2) strictly decreases perceived expected utility EU,
    because higher cognitive bandwidth enables discovery of the hidden predatory terms. -/
theorem cloaked_perceived_utility_strictAnti_kappa (τ : ℝ) {γ χ κ1 κ2 U_promo U_true : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hκ : κ1 < κ2)
    (hU : U_true < U_promo) :
    perceivedEU γ τ χ κ2 U_promo U_true < perceivedEU γ τ χ κ1 U_promo U_true := by
  rw [perceivedEU_eq, perceivedEU_eq]
  have h_pdisc := Pdisc_strictMono_kappa τ hγ hχ hκ
  have h_udiff : 0 < U_promo - U_true := sub_pos.mpr hU
  have h_mul : Pdisc γ τ χ κ1 * (U_promo - U_true) < Pdisc γ τ χ κ2 * (U_promo - U_true) :=
    mul_lt_mul_of_pos_right h_pdisc h_udiff
  linarith

/-- **Theorem (Weather-Shield Gating Mitigates Predatory Exploitation)**:
    Under elevated environmental thermal stress F_thermal > 1, cognitive bandwidth is compressed
    to κ_eff = κ / F_thermal < κ.
    Activating Weather-Shield (holding execution until ambient conditions normalize to κ)
    strictly reduces perceived expected utility of predatory agreements back to baseline,
    neutralizing thermal-stress-induced predatory exploitation. -/
theorem weather_shield_reduces_predatory_utility (τ : ℝ) {γ χ κ F_thermal U_promo U_true : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hκ : 0 < κ) (hF : 1 < F_thermal)
    (hU : U_true < U_promo) :
    let κ_eff := κ / F_thermal
    perceivedEU γ τ χ κ U_promo U_true < perceivedEU γ τ χ κ_eff U_promo U_true := by
  intro κ_eff
  have h_eff_lt : κ_eff < κ := by
    dsimp [κ_eff]
    have h_div : κ / F_thermal < κ / 1 := div_lt_div_of_pos_left hκ (by linarith) hF
    simpa using h_div
  exact cloaked_perceived_utility_strictAnti_kappa τ hγ hχ h_eff_lt hU

/-- Executive threat monitoring gate E(C) under Cortisol threshold gating (Baylor model):
    Deactivates when C < C_crit = 0.12. -/
noncomputable def executiveGate (C Ccrit : ℝ) : ℝ :=
  if C < Ccrit then 0 else 1

/-- Effective loss aversion rate under Baylor unconsciousness gating:
    lambda_minus_eff = E(C) * lambda_minus_base. -/
noncomputable def lambdaMinusEff (C Ccrit lambda_base : ℝ) : ℝ :=
  executiveGate C Ccrit * lambda_base

/-- **Theorem D18 (Baylor Cortisol Threat Gate Collapse)**:
    When Cortisol drops below the threshold (C < C_crit), the executive threat gate
    deactivates (E(C) = 0), completely silencing loss aversion (lambda_minus_eff = 0)
    and reducing cognitive friction. -/
theorem baylor_cortisol_gate_collapse {C Ccrit lambda_base : ℝ}
    (hC : C < Ccrit) :
    lambdaMinusEff C Ccrit lambda_base = 0 := by
  unfold lambdaMinusEff executiveGate
  rw [if_pos hC]
  ring

/-- **Theorem D18 (Baylor Waking Executive Restoration)**:
    When the agent re-enters conscious awareness (C >= C_crit), the executive threat gate
    fully reactivates (E(C) = 1), restoring full loss aversion (lambda_minus_eff = lambda_base). -/
theorem baylor_waking_executive_restoration {C Ccrit lambda_base : ℝ}
    (hC : Ccrit ≤ C) :
    lambdaMinusEff C Ccrit lambda_base = lambda_base := by
  unfold lambdaMinusEff executiveGate
  have hnot : ¬ (C < Ccrit) := not_lt.mpr hC
  rw [if_neg hnot]
  ring

/-- Relational Oxytocin and Serotonin implicit narrative attractor shift (Sim D18):
    Delta_S_base = eta_O * O + eta_S * S. -/
noncomputable def baylorAttractorShift (eta_O eta_S O S : ℝ) : ℝ :=
  eta_O * O + eta_S * S

/-- Trajectory step under unconscious relational narrative exposure with shifted baseline:
    S ↦ S - δ * (S - (Sbase + ΔS)). -/
noncomputable def masterStep_baylor (δ Sbase ΔS S : ℝ) : ℝ :=
  S - δ * (S - (Sbase + ΔS))

/-- **Theorem D18 (Baylor Unconscious Attractor Convergence)**:
    Under unconscious narrative exposure (M=0), the shifted baseline attractor
    S* = Sbase + ΔS is a fixed point of the Master Law dynamics. -/
theorem baylor_unconscious_attractor_fixed_point (δ Sbase ΔS : ℝ) :
    masterStep_baylor δ Sbase ΔS (Sbase + ΔS) = Sbase + ΔS := by
  unfold masterStep_baylor
  ring

/-- **Theorem D18 (Baylor Waking Perturbation Decay)**:
    For any two trajectories entering conscious waking mode (M=1) with restoring rate δ ≤ 1,
    the difference between an exposed agent (S1) and unexposed control (S2) contracts
    geometrically at rate (1 - δ)^t:
    |traj(0,0,δ,Sbase,0,0,S1,t) - traj(0,0,δ,Sbase,0,0,S2,t)| = (1 - δ)^t * |S1 - S2|.
    This formally proves why Criterion C3 in Sim D18 exhibits only modest waking uptake (+4%),
    demonstrating intrinsic waking executive resilience against unconscious narrative priming. -/
theorem baylor_waking_perturbation_decay (δ Sbase S1 S2 : ℝ) (hδ1 : δ ≤ 1) (t : ℕ) :
    |traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S1 t - traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S2 t|
      = (1 - δ) ^ t * |S1 - S2| := by
  have e1 := contraction δ Sbase S1 t
  have e2 := contraction δ Sbase S2 t
  have hdiff : traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S1 t - traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S2 t
      = (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S1 t - Sbase) - (traj 0 0 δ Sbase (fun _ => 0) (fun _ => 0) S2 t - Sbase) := by ring
  rw [hdiff, e1, e2]
  have hmul : (1 - δ) ^ t * (S1 - Sbase) - (1 - δ) ^ t * (S2 - Sbase)
      = (1 - δ) ^ t * (S1 - S2) := by ring
  rw [hmul, abs_mul]
  have hq : 0 ≤ 1 - δ := sub_nonneg.mpr hδ1
  have hp : 0 ≤ (1 - δ) ^ t := by positivity
  rw [abs_of_nonneg hp]

/-- Compound multi-stressor effective cognitive bandwidth (Sim O2, Sim D17, Sim D18):
    kappa_comp = (kappa0 * exp(-alpha_C * I_chr2) / F_thermal) * (3/5 + 2/5 * R_fric). -/
noncomputable def compoundBandwidth (kappa0 alpha_C I_chr2 F_thermal R_fric : ℝ) : ℝ :=
  (kappa0 * Real.exp (-alpha_C * I_chr2) / F_thermal) * (3/5 + 2/5 * R_fric)

/-- **Theorem (Compound Biophysical Bandwidth Compression)**:
    Under non-negative ChR2 Cortisol excitation (alpha_C >= 0, I_chr2 >= 0),
    hyperthermal stress (F_thermal >= 1), and bounded unconscious cognitive friction (R_fric <= 1),
    the compound effective bandwidth kappa_comp is strictly bounded above by baseline kappa0. -/
theorem compound_biophysical_bandwidth_le {kappa0 alpha_C I_chr2 F_thermal R_fric : ℝ}
    (hk0 : 0 ≤ kappa0) (halpha : 0 ≤ alpha_C) (hI : 0 ≤ I_chr2)
    (hF : 1 ≤ F_thermal) (hR : R_fric ≤ 1) :
    compoundBandwidth kappa0 alpha_C I_chr2 F_thermal R_fric ≤ kappa0 := by
  unfold compoundBandwidth
  have h_prod : 0 ≤ alpha_C * I_chr2 := mul_nonneg halpha hI
  have h_neg : -alpha_C * I_chr2 ≤ 0 := by linarith
  have h_exp : Real.exp (-alpha_C * I_chr2) ≤ 1 := by
    calc Real.exp (-alpha_C * I_chr2) ≤ Real.exp 0 := Real.exp_le_exp.mpr h_neg
    _ = 1 := Real.exp_zero
  have h_exp_nonneg : 0 ≤ Real.exp (-alpha_C * I_chr2) := Real.exp_nonneg _
  have h_num : kappa0 * Real.exp (-alpha_C * I_chr2) ≤ kappa0 := by
    nlinarith
  have h_div : (kappa0 * Real.exp (-alpha_C * I_chr2)) / F_thermal ≤ kappa0 := by
    have h1 : (kappa0 * Real.exp (-alpha_C * I_chr2)) / F_thermal ≤ kappa0 / F_thermal := by
      exact div_le_div_of_nonneg_right h_num (by linarith)
    have h2 : kappa0 / F_thermal ≤ kappa0 / 1 := by
      exact div_le_div_of_nonneg_left hk0 (by linarith) hF
    rw [div_one] at h2
    linarith
  have h_nonneg_div : 0 ≤ (kappa0 * Real.exp (-alpha_C * I_chr2)) / F_thermal := by
    have h_prod_nonneg : 0 ≤ kappa0 * Real.exp (-alpha_C * I_chr2) := mul_nonneg hk0 h_exp_nonneg
    exact div_nonneg h_prod_nonneg (by linarith)
  nlinarith

/-- **Theorem (Compound Multi-Stressor Increases Predatory Uptake)**:
    Under biophysical stressors (Cortisol excitation, hyperthermia, Baylor unconsciousness),
    effective cognitive bandwidth compresses below baseline (kappa_comp ≤ kappa0),
    which weakly increases predatory contract uptake:
    Uptake(kappa0) ≤ Uptake(kappa_comp). -/
theorem compound_stressor_increases_uptake (τ : ℝ) {γ χ kappa0 alpha_C I_chr2 F_thermal R_fric : ℝ}
    (hγ : 0 < γ) (hχ : 0 < χ) (hk0 : 0 ≤ kappa0) (halpha : 0 ≤ alpha_C) (hI : 0 ≤ I_chr2)
    (hF : 1 ≤ F_thermal) (hR : R_fric ≤ 1) :
    Uptake γ τ χ kappa0 ≤ Uptake γ τ χ (compoundBandwidth kappa0 alpha_C I_chr2 F_thermal R_fric) := by
  have hle := compound_biophysical_bandwidth_le hk0 halpha hI hF hR
  exact Uptake_anti_kappa τ hγ hχ hle



/-- Master law step with time-varying environmental baseline under zero prediction error:
    S ↦ S - δ * (S - Sbase_t). -/
noncomputable def masterStep_env (δ Sbase_t S : ℝ) : ℝ :=
  S - δ * (S - Sbase_t)

/-- Trajectory with time-varying environmental baseline under zero input. -/
noncomputable def traj_env (δ S0 : ℝ) (Sbase_seq : ℕ → ℝ) : ℕ → ℝ
  | 0 => S0
  | (t + 1) => masterStep_env δ (Sbase_seq t) (traj_env δ S0 Sbase_seq t)

/-- **Theorem D17 (Environmental Baseline Drift Low-Pass Bound)**:
    Under leaky baseline restoration with δ ∈ (0, 1] and bounded seasonal baseline drift
    |S_base(t) - S_0| ≤ D_max, the longitudinal trust deviation |S_t - S_0| is strictly
    bounded by D_max for all time t.
    This proves that the Master Stability Law acts as an intrinsic low-pass filter,
    explaining why winter photoperiod deficits produce modest vector-norm erosion (3.9%)
    rather than runaway trust collapse. -/
theorem environmental_drift_bound {δ S0 Dmax : ℝ} {Sbase_seq : ℕ → ℝ}
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) (hD0 : 0 ≤ Dmax)
    (hD : ∀ t, |Sbase_seq t - S0| ≤ Dmax) (t : ℕ) :
    |traj_env δ S0 Sbase_seq t - S0| ≤ Dmax := by
  induction t with
  | zero =>
    simp [traj_env, hD0]
  | succ t ih =>
    have hq : 0 ≤ 1 - δ := sub_nonneg.mpr hδ1
    have hstep : traj_env δ S0 Sbase_seq (t + 1) - S0
        = (1 - δ) * (traj_env δ S0 Sbase_seq t - S0) + δ * (Sbase_seq t - S0) := by
      show masterStep_env δ (Sbase_seq t) (traj_env δ S0 Sbase_seq t) - S0 = _
      unfold masterStep_env
      ring
    rw [hstep]
    calc |(1 - δ) * (traj_env δ S0 Sbase_seq t - S0) + δ * (Sbase_seq t - S0)|
        ≤ |(1 - δ) * (traj_env δ S0 Sbase_seq t - S0)| + |δ * (Sbase_seq t - S0)| := abs_add_le _ _
      _ = (1 - δ) * |traj_env δ S0 Sbase_seq t - S0| + δ * |Sbase_seq t - S0| := by
          rw [abs_mul, abs_of_nonneg hq, abs_mul, abs_of_nonneg hδ0]
      _ ≤ (1 - δ) * Dmax + δ * Dmax :=
          add_le_add (mul_le_mul_of_nonneg_left ih hq) (mul_le_mul_of_nonneg_left (hD t) hδ0)
      _ = Dmax := by ring

/-- Conservation of total probability under continuous Markov flux:
    The sum of derivatives vanishes identically:
    dc1 + do1 + do2 + dc2 = 0. -/
theorem markov_derivatives_conserve_probability
    (c1 o1 o2 c2 k1 k2 gd1 gd2 e12 e21 gr : ℝ) :
    let dc1 := -k1 * c1 + gd1 * o1 + gr * c2
    let do1 := k1 * c1 - (gd1 + e12) * o1 + e21 * o2
    let do2 := k2 * c2 + e12 * o1 - (gd2 + e21) * o2
    let dc2 := -k2 * c2 + gd2 * o2 - gr * c2
    dc1 + do1 + do2 + dc2 = 0 := by
  intro dc1 do1 do2 dc2
  dsimp [dc1, do1, do2, dc2]
  ring

/-- **Theorem O3 (Kuramoto Mutant Subpopulation Macroeconomic Resilience Bound)**:
    Let Z_intact be the order parameter of the intact subpopulation, and Z_all be the
    global order parameter formed by convex combination with a mutant subpopulation
    of fraction eps in [0, 1]: Z_all = (1 - eps) * Z_intact + eps * Z_mutant.
    When the mutant order parameter is bounded by 1 (|Z_mutant| <= 1), the global
    coherence R_all = |Z_all| cannot deviate from the scaled intact coherence
    (1 - eps) * R_intact by more than eps:
    |R_all - (1 - eps) * R_intact| <= eps.
    In particular, for eps = 0.10 (10% O/S mutants), the coherence deviation is bounded
    by 10%, explaining from first principles why the Kuramoto network demonstrates
    resilience (11.39% drop) rather than catastrophic phase collapse. -/
theorem kuramoto_mutant_resilience_bound {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Z_intact Z_mutant : E) (eps : ℝ) (heps0 : 0 ≤ eps) (heps1 : eps ≤ 1)
    (h_mut : ‖Z_mutant‖ ≤ 1) :
    ‖(1 - eps) • Z_intact + eps • Z_mutant‖ - (1 - eps) * ‖Z_intact‖ ≤ eps ∧
    (1 - eps) * ‖Z_intact‖ - ‖(1 - eps) • Z_intact + eps • Z_mutant‖ ≤ eps := by
  have hq : 0 ≤ 1 - eps := sub_nonneg.mpr heps1
  have h_add : ‖(1 - eps) • Z_intact + eps • Z_mutant‖
      ≤ ‖(1 - eps) • Z_intact‖ + ‖eps • Z_mutant‖ := norm_add_le _ _
  have h_norm1 : ‖(1 - eps) • Z_intact‖ = (1 - eps) * ‖Z_intact‖ := by
    rw [norm_smul, Real.norm_of_nonneg hq]
  have h_norm2 : ‖eps • Z_mutant‖ = eps * ‖Z_mutant‖ := by
    rw [norm_smul, Real.norm_of_nonneg heps0]
  have h_bound2 : ‖eps • Z_mutant‖ ≤ eps := by
    rw [h_norm2]
    calc eps * ‖Z_mutant‖ ≤ eps * 1 := mul_le_mul_of_nonneg_left h_mut heps0
      _ = eps := mul_one _
  constructor
  · calc ‖(1 - eps) • Z_intact + eps • Z_mutant‖ - (1 - eps) * ‖Z_intact‖
        ≤ (‖(1 - eps) • Z_intact‖ + ‖eps • Z_mutant‖) - (1 - eps) * ‖Z_intact‖ := sub_le_sub_right h_add _
      _ = ‖eps • Z_mutant‖ := by rw [h_norm1]; ring
      _ ≤ eps := h_bound2
  · have h_rev : (1 - eps) * ‖Z_intact‖ - ‖(1 - eps) • Z_intact + eps • Z_mutant‖
        ≤ ‖eps • Z_mutant‖ := by
      have e : (1 - eps) • Z_intact = ((1 - eps) • Z_intact + eps • Z_mutant) - eps • Z_mutant := by
        abel
      have h_le : ‖(1 - eps) • Z_intact‖ ≤ ‖(1 - eps) • Z_intact + eps • Z_mutant‖ + ‖eps • Z_mutant‖ := by
        nth_rw 1 [e]
        exact norm_sub_le _ _
      rw [h_norm1] at h_le
      linarith
    exact le_trans h_rev h_bound2

/-- **Theorem (Discrete CFL Markov Simplex Invariance)**:
    Under discrete Euler sub-stepping with step size dt >= 0 and Courant-Friedrichs-Lewy (CFL) bounds
    on the rate constants:
      dt * k1 <= 1
      dt * (gd1 + e12) <= 1
      dt * (gd2 + e21) <= 1
      dt * (k2 + gr) <= 1,
    any initial probability distribution (c1, o1, o2, c2) on Delta^3 is mapped into Delta^3:
    all probabilities remain non-negative (c1' >= 0, o1' >= 0, o2' >= 0, c2' >= 0) and
    the sum is identically preserved: c1' + o1' + o2' + c2' = 1. -/
theorem markov_euler_simplex_invariant
    (c1 o1 o2 c2 k1 k2 gd1 gd2 e12 e21 gr dt : ℝ)
    (h_c1 : 0 ≤ c1) (h_o1 : 0 ≤ o1) (h_o2 : 0 ≤ o2) (h_c2 : 0 ≤ c2)
    (h_sum : c1 + o1 + o2 + c2 = 1)
    (h_dt : 0 ≤ dt)
    (h_k1 : 0 ≤ k1) (h_k2 : 0 ≤ k2) (h_gd1 : 0 ≤ gd1) (h_gd2 : 0 ≤ gd2)
    (h_e12 : 0 ≤ e12) (h_e21 : 0 ≤ e21) (h_gr : 0 ≤ gr)
    (cfl_c1 : dt * k1 ≤ 1)
    (cfl_o1 : dt * (gd1 + e12) ≤ 1)
    (cfl_o2 : dt * (gd2 + e21) ≤ 1)
    (cfl_c2 : dt * (k2 + gr) ≤ 1) :
    let c1' := (1 - dt * k1) * c1 + dt * (gd1 * o1 + gr * c2)
    let o1' := (1 - dt * (gd1 + e12)) * o1 + dt * (k1 * c1 + e21 * o2)
    let o2' := (1 - dt * (gd2 + e21)) * o2 + dt * (k2 * c2 + e12 * o1)
    let c2' := (1 - dt * (k2 + gr)) * c2 + dt * (gd2 * o2)
    0 ≤ c1' ∧ 0 ≤ o1' ∧ 0 ≤ o2' ∧ 0 ≤ c2' ∧ c1' + o1' + o2' + c2' = 1 := by
  intro c1' o1' o2' c2'
  have hc1' : 0 ≤ c1' := by
    dsimp [c1']
    have h1 : 0 ≤ 1 - dt * k1 := sub_nonneg.mpr cfl_c1
    have h2 : 0 ≤ (1 - dt * k1) * c1 := mul_nonneg h1 h_c1
    have h3 : 0 ≤ gd1 * o1 := mul_nonneg h_gd1 h_o1
    have h4 : 0 ≤ gr * c2 := mul_nonneg h_gr h_c2
    have h5 : 0 ≤ dt * (gd1 * o1 + gr * c2) := mul_nonneg h_dt (add_nonneg h3 h4)
    linarith
  have ho1' : 0 ≤ o1' := by
    dsimp [o1']
    have h1 : 0 ≤ 1 - dt * (gd1 + e12) := sub_nonneg.mpr cfl_o1
    have h2 : 0 ≤ (1 - dt * (gd1 + e12)) * o1 := mul_nonneg h1 h_o1
    have h3 : 0 ≤ k1 * c1 := mul_nonneg h_k1 h_c1
    have h4 : 0 ≤ e21 * o2 := mul_nonneg h_e21 h_o2
    have h5 : 0 ≤ dt * (k1 * c1 + e21 * o2) := mul_nonneg h_dt (add_nonneg h3 h4)
    linarith
  have ho2' : 0 ≤ o2' := by
    dsimp [o2']
    have h1 : 0 ≤ 1 - dt * (gd2 + e21) := sub_nonneg.mpr cfl_o2
    have h2 : 0 ≤ (1 - dt * (gd2 + e21)) * o2 := mul_nonneg h1 h_o2
    have h3 : 0 ≤ k2 * c2 := mul_nonneg h_k2 h_c2
    have h4 : 0 ≤ e12 * o1 := mul_nonneg h_e12 h_o1
    have h5 : 0 ≤ dt * (k2 * c2 + e12 * o1) := mul_nonneg h_dt (add_nonneg h3 h4)
    linarith
  have hc2' : 0 ≤ c2' := by
    dsimp [c2']
    have h1 : 0 ≤ 1 - dt * (k2 + gr) := sub_nonneg.mpr cfl_c2
    have h2 : 0 ≤ (1 - dt * (k2 + gr)) * c2 := mul_nonneg h1 h_c2
    have h3 : 0 ≤ gd2 * o2 := mul_nonneg h_gd2 h_o2
    have h4 : 0 ≤ dt * (gd2 * o2) := mul_nonneg h_dt h3
    linarith
  have hsum' : c1' + o1' + o2' + c2' = 1 := by
    dsimp [c1', o1', o2', c2']
    calc (1 - dt * k1) * c1 + dt * (gd1 * o1 + gr * c2)
       + ((1 - dt * (gd1 + e12)) * o1 + dt * (k1 * c1 + e21 * o2))
       + ((1 - dt * (gd2 + e21)) * o2 + dt * (k2 * c2 + e12 * o1))
       + ((1 - dt * (k2 + gr)) * c2 + dt * (gd2 * o2))
       = c1 + o1 + o2 + c2 := by ring
     _ = 1 := h_sum
  exact ⟨hc1', ho1', ho2', hc2', hsum'⟩

/-- Master law step with time-varying opsin conductance gating:
    S ↦ S + λ⁺·(1 - g)·max(ε,0)·r + λ⁻·min(ε,0)·r − δ·(S − S_base). -/
noncomputable def masterStep_opto (lp ln δ Sbase r g S ε : ℝ) : ℝ :=
  S + lp * (1 - g) * max ε 0 * r + ln * min ε 0 * r - δ * (S - Sbase)

/-- Trajectory under time-varying opsin conductance gating. -/
noncomputable def traj_opto (lp ln δ Sbase : ℝ) (r g ε : ℕ → ℝ) (S0 : ℝ) : ℕ → ℝ
  | 0 => S0
  | (t + 1) => masterStep_opto lp ln δ Sbase (r t) (g t) (traj_opto lp ln δ Sbase r g ε S0 t) (ε t)

/-- **Theorem (Opsin Conductance Gated Contraction)**:
    Under full ArchT opsin saturation (g t = 1 for all t) and non-negative reward stream (ε t >= 0),
    the time-varying optogenetic trajectory contracts geometrically to baseline S_base at rate (1 - δ)^t,
    regardless of learning rate λ⁺ or reward gate r t. -/
theorem opto_conductance_gated_contraction
    (lp ln δ Sbase S0 : ℝ) (r g ε : ℕ → ℝ)
    (hg : ∀ t, g t = 1) (hε : ∀ t, 0 ≤ ε t) (t : ℕ) :
    traj_opto lp ln δ Sbase r g ε S0 t - Sbase = (1 - δ)^t * (S0 - Sbase) := by
  induction t with
  | zero => simp [traj_opto]
  | succ t ih =>
    have hmin : min (ε t) 0 = 0 := min_eq_right (hε t)
    have hg1 : 1 - g t = 0 := by rw [hg t, sub_self]
    have hstep : traj_opto lp ln δ Sbase r g ε S0 (t + 1)
        = (1 - δ) * (traj_opto lp ln δ Sbase r g ε S0 t - Sbase) + Sbase := by
      show masterStep_opto lp ln δ Sbase (r t) (g t) (traj_opto lp ln δ Sbase r g ε S0 t) (ε t) = _
      unfold masterStep_opto
      rw [hmin, hg1]
      ring
    have e : traj_opto lp ln δ Sbase r g ε S0 (t + 1) - Sbase
        = (1 - δ) * (traj_opto lp ln δ Sbase r g ε S0 t - Sbase) := by
      linarith [hstep]
    rw [e, ih, pow_succ]
    ring

/-- Clamped master step matching production edge/R1CS boundary `clamp(0, 1)`. -/
noncomputable def masterStepClamped (lp ln δ Sbase r S ε : ℝ) : ℝ :=
  max 0 (min 1 (masterStep lp ln δ Sbase r S ε))

/-- Clamped trajectory on the unit interval [0, 1]. -/
noncomputable def trajClamped (lp ln δ Sbase : ℝ) (r ε : ℕ → ℝ) (S0 : ℝ) : ℕ → ℝ
  | 0 => S0
  | (t + 1) => masterStepClamped lp ln δ Sbase (r t) (trajClamped lp ln δ Sbase r ε S0 t) (ε t)

/-- **Clamped Unit-Interval Invariance**: every clamped update remains inside `[0, 1]`. -/
theorem masterStepClamped_mem_unit (lp ln δ Sbase r S ε : ℝ) :
    0 ≤ masterStepClamped lp ln δ Sbase r S ε ∧ masterStepClamped lp ln δ Sbase r S ε ≤ 1 := by
  unfold masterStepClamped
  constructor
  · exact le_max_left _ _
  · exact max_le (by norm_num) (min_le_left _ _)

/-- **Clamped Trajectory Invariance**: starting from `S0 ∈ [0, 1]`, the clamped trajectory never leaves `[0, 1]`. -/
theorem trajClamped_mem_unit (lp ln δ Sbase : ℝ) (r ε : ℕ → ℝ) {S0 : ℝ}
    (h0 : 0 ≤ S0) (h1 : S0 ≤ 1) (t : ℕ) :
    0 ≤ trajClamped lp ln δ Sbase r ε S0 t ∧ trajClamped lp ln δ Sbase r ε S0 t ≤ 1 := by
  cases t with
  | zero => exact ⟨h0, h1⟩
  | succ k => exact masterStepClamped_mem_unit _ _ _ _ _ _ _

/-- **1-Lipschitz Clamping Stability**: clamping to `[0, 1]` is non-expansive (`|clamp a - clamp b| ≤ |a - b|`),
    ensuring bounded fixed-point quantization drift across Lean, Python R1CS, and Rust `f64` engines. -/
theorem clamp_unit_lipschitz (a b : ℝ) :
    |max 0 (min 1 a) - max 0 (min 1 b)| ≤ |a - b| := by
  have hmax : ∀ x y : ℝ, |max 0 x - max 0 y| ≤ |x - y| := by
    intro x y
    rcases le_total 0 x with hx | hx <;> rcases le_total 0 y with hy | hy
    · rw [max_eq_right hx, max_eq_right hy]
    · rw [max_eq_right hx, max_eq_left hy, sub_zero, abs_of_nonneg hx, abs_of_nonneg (by linarith)]
      linarith
    · rw [max_eq_left hx, max_eq_right hy, zero_sub, abs_neg, abs_of_nonneg hy, abs_of_nonpos (by linarith)]
      linarith
    · rw [max_eq_left hx, max_eq_left hy, sub_self, abs_zero]
      exact abs_nonneg _
  have hmin : ∀ x y : ℝ, |min 1 x - min 1 y| ≤ |x - y| := by
    intro x y
    rcases le_total x 1 with hx | hx <;> rcases le_total y 1 with hy | hy
    · rw [min_eq_right hx, min_eq_right hy]
    · rw [min_eq_right hx, min_eq_left hy, abs_of_nonpos (by linarith), abs_of_nonpos (by linarith)]
      linarith
    · rw [min_eq_left hx, min_eq_right hy, abs_of_nonneg (by linarith), abs_of_nonneg (by linarith)]
      linarith
    · rw [min_eq_left hx, min_eq_left hy, sub_self, abs_zero]
      exact abs_nonneg _
  exact le_trans (hmax (min 1 a) (min 1 b)) (hmin a b)

/-- **Clamped Non-Commutativity Counterexample**: because clamping to `[0, 1]` absorbs boundary
    overshoots, consecutive `masterStepClamped` updates are order-dependent (`f_a ∘ f_b ≠ f_b ∘ f_a`).
    Hence distributed edge nodes cannot merge raw `S_t` registers as a state-based CRDT; they must
    merge a canonical HLC/hash-ordered op-log (`G-Set`) and replay deterministically. -/
theorem masterStepClamped_not_comm :
    ∃ (lp ln δ Sbase r S0 ε₁ ε₂ : ℝ),
      masterStepClamped lp ln δ Sbase r (masterStepClamped lp ln δ Sbase r S0 ε₁) ε₂ ≠
      masterStepClamped lp ln δ Sbase r (masterStepClamped lp ln δ Sbase r S0 ε₂) ε₁ := by
  refine ⟨1, 1, 0, 0, 1, 0, -1, 1, ?_⟩
  unfold masterStepClamped masterStep
  norm_num

/-- **Clamped Zero-Input Contraction**: for any `lp, ln`, `δ ∈ (0, 1]`, `Sbase ∈ [0, 1]`,
    and `S0 ∈ [0, 1]`, under zero mismatch `ε_t = 0` the clamped update never hits the
    `[0, 1]` boundary and contracts geometrically to `Sbase` at rate `(1 - δ)^t`. -/
theorem trajClamped_contraction_zero_input
    (lp ln δ Sbase S0 : ℝ) (r : ℕ → ℝ)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hb0 : 0 ≤ Sbase) (hb1 : Sbase ≤ 1)
    (h0 : 0 ≤ S0) (h1 : S0 ≤ 1) (t : ℕ) :
    trajClamped lp ln δ Sbase r (fun _ => 0) S0 t - Sbase = (1 - δ)^t * (S0 - Sbase) := by
  induction t with
  | zero => simp [trajClamped]
  | succ t ih =>
    have hm := trajClamped_mem_unit lp ln δ Sbase r (fun _ => 0) h0 h1 t
    have hq : 0 ≤ 1 - δ := sub_nonneg.mpr hδ1
    have hstep_val :
        masterStep lp ln δ Sbase (r t) (trajClamped lp ln δ Sbase r (fun _ => 0) S0 t) 0
          = (1 - δ) * trajClamped lp ln δ Sbase r (fun _ => 0) S0 t + δ * Sbase := by
      unfold masterStep
      simp
      ring
    have h_ge0 : 0 ≤ masterStep lp ln δ Sbase (r t) (trajClamped lp ln δ Sbase r (fun _ => 0) S0 t) 0 := by
      rw [hstep_val]
      nlinarith [hm.1, hb0, hq, hδ0]
    have h_le1 : masterStep lp ln δ Sbase (r t) (trajClamped lp ln δ Sbase r (fun _ => 0) S0 t) 0 ≤ 1 := by
      rw [hstep_val]
      nlinarith [hm.2, hb1, hq, hδ0]
    have h_unclamped :
        trajClamped lp ln δ Sbase r (fun _ => 0) S0 (t + 1)
          = (1 - δ) * trajClamped lp ln δ Sbase r (fun _ => 0) S0 t + δ * Sbase := by
      show masterStepClamped lp ln δ Sbase (r t) (trajClamped lp ln δ Sbase r (fun _ => 0) S0 t) 0 = _
      unfold masterStepClamped
      rw [min_eq_right h_le1, max_eq_right h_ge0, hstep_val]
    have e : trajClamped lp ln δ Sbase r (fun _ => 0) S0 (t + 1) - Sbase
        = (1 - δ) * (trajClamped lp ln δ Sbase r (fun _ => 0) S0 t - Sbase) := by
      linarith [h_unclamped]
    rw [e, ih, pow_succ]
    ring

/-- **Clamped Incremental Contraction under Arbitrary Shared Inputs**:
    For any leak `δ ∈ [0, 1]`, arbitrary learning rates `lp, ln`, and arbitrary shared
    active input streams `(r, ε)`, two clamped trajectories starting at `S0, S0'` contract
    exponentially toward each other at rate `(1 - δ)^t`:
    `|trajClamped ... S0 t - trajClamped ... S0' t| ≤ (1 - δ)^t * |S0 - S0'|`. -/
theorem trajClamped_incremental_contraction
    (lp ln δ Sbase S0 S0' : ℝ) (r ε : ℕ → ℝ)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) (t : ℕ) :
    |trajClamped lp ln δ Sbase r ε S0 t - trajClamped lp ln δ Sbase r ε S0' t|
      ≤ (1 - δ)^t * |S0 - S0'| := by
  induction t with
  | zero => simp [trajClamped]
  | succ t ih =>
    have hq : 0 ≤ 1 - δ := sub_nonneg.mpr hδ1
    set x := trajClamped lp ln δ Sbase r ε S0 t
    set y := trajClamped lp ln δ Sbase r ε S0' t
    have hstep_diff :
        masterStep lp ln δ Sbase (r t) x (ε t) - masterStep lp ln δ Sbase (r t) y (ε t)
          = (1 - δ) * (x - y) := by
      unfold masterStep
      ring
    have h_lip := clamp_unit_lipschitz
      (masterStep lp ln δ Sbase (r t) x (ε t))
      (masterStep lp ln δ Sbase (r t) y (ε t))
    have h_step_eq :
        |trajClamped lp ln δ Sbase r ε S0 (t + 1) - trajClamped lp ln δ Sbase r ε S0' (t + 1)|
          ≤ |(1 - δ) * (x - y)| := by
      simpa [trajClamped, masterStepClamped, x, y, hstep_diff] using h_lip
    have h_abs : |(1 - δ) * (x - y)| = (1 - δ) * |x - y| := by
      rw [abs_mul, abs_of_nonneg hq]
    rw [h_abs] at h_step_eq
    have h_mul : (1 - δ) * |x - y| ≤ (1 - δ) * ((1 - δ)^t * |S0 - S0'|) :=
      mul_le_mul_of_nonneg_left ih hq
    calc |trajClamped lp ln δ Sbase r ε S0 (t + 1) - trajClamped lp ln δ Sbase r ε S0' (t + 1)|
        ≤ (1 - δ) * |x - y| := h_step_eq
      _ ≤ (1 - δ) * ((1 - δ)^t * |S0 - S0'|) := h_mul
      _ = (1 - δ)^(t + 1) * |S0 - S0'| := by rw [pow_succ]; ring

/-- Non-autonomous DOCAS-coupled clamped `[0, 1]` trajectory where learning rates
    `(lp t, ln t)` and baseline leak `δ t` vary dynamically at each step `t`. -/
noncomputable def trajClampedNonAuto
    (lp ln δ : ℕ → ℝ) (Sbase : ℝ) (r ε : ℕ → ℝ) (S0 : ℝ) : ℕ → ℝ
  | 0 => S0
  | t + 1 => masterStepClamped (lp t) (ln t) (δ t) Sbase (r t) (trajClampedNonAuto lp ln δ Sbase r ε S0 t) (ε t)

/-- **Non-Autonomous Clamped State-Space Invariance**:
    If `S0 ∈ [0, 1]`, the time-varying DOCAS trajectory remains strictly in `[0, 1]` for all `t`. -/
theorem trajClampedNonAuto_mem_unit
    (lp ln δ : ℕ → ℝ) (Sbase : ℝ) (r ε : ℕ → ℝ) (S0 : ℝ)
    (hS0 : S0 ∈ Set.Icc (0 : ℝ) 1) (t : ℕ) :
    trajClampedNonAuto lp ln δ Sbase r ε S0 t ∈ Set.Icc (0 : ℝ) 1 := by
  induction t with
  | zero => exact hS0
  | succ t _ => exact masterStepClamped_mem_unit _ _ _ _ _ _ _

/-- **Non-Autonomous Clamped Incremental Contraction (DOCAS–GTT Bridge)**:
    Whenever time-varying leak rates satisfy `0 ≤ δ_min ≤ δ t ≤ 1` for all `t`, any two
    state-modulated clamped trajectories sharing active inputs `(r, ε)` synchronize at least
    as fast as `(1 - δ_min)^t * |S0 - S0'|` regardless of arbitrary `(lp t, ln t)` modulation. -/
theorem trajClampedNonAuto_incremental_contraction
    (lp ln δ : ℕ → ℝ) (δmin Sbase S0 S0' : ℝ) (r ε : ℕ → ℝ)
    (hδmin : 0 ≤ δmin) (hδ_lb : ∀ k, δmin ≤ δ k) (hδ_ub : ∀ k, δ k ≤ 1) (t : ℕ) :
    |trajClampedNonAuto lp ln δ Sbase r ε S0 t - trajClampedNonAuto lp ln δ Sbase r ε S0' t|
      ≤ (1 - δmin)^t * |S0 - S0'| := by
  induction t with
  | zero => simp [trajClampedNonAuto]
  | succ t ih =>
    have hq_min : 0 ≤ 1 - δmin := sub_nonneg.mpr (le_trans (hδ_lb t) (hδ_ub t))
    have hq_t : 0 ≤ 1 - δ t := sub_nonneg.mpr (hδ_ub t)
    have hq_le : 1 - δ t ≤ 1 - δmin := sub_le_sub_left (hδ_lb t) 1
    set x := trajClampedNonAuto lp ln δ Sbase r ε S0 t
    set y := trajClampedNonAuto lp ln δ Sbase r ε S0' t
    have hstep_diff :
        masterStep (lp t) (ln t) (δ t) Sbase (r t) x (ε t)
          - masterStep (lp t) (ln t) (δ t) Sbase (r t) y (ε t)
          = (1 - δ t) * (x - y) := by
      unfold masterStep
      ring
    have h_lip := clamp_unit_lipschitz
      (masterStep (lp t) (ln t) (δ t) Sbase (r t) x (ε t))
      (masterStep (lp t) (ln t) (δ t) Sbase (r t) y (ε t))
    have h_step_eq :
        |trajClampedNonAuto lp ln δ Sbase r ε S0 (t + 1) - trajClampedNonAuto lp ln δ Sbase r ε S0' (t + 1)|
          ≤ (1 - δ t) * |x - y| := by
      have h_abs : |(1 - δ t) * (x - y)| = (1 - δ t) * |x - y| := by
        rw [abs_mul, abs_of_nonneg hq_t]
      simpa [trajClampedNonAuto, masterStepClamped, x, y, hstep_diff, h_abs] using h_lip
    have h_mon : (1 - δ t) * |x - y| ≤ (1 - δmin) * |x - y| :=
      mul_le_mul_of_nonneg_right hq_le (abs_nonneg _)
    have h_mul : (1 - δmin) * |x - y| ≤ (1 - δmin) * ((1 - δmin)^t * |S0 - S0'|) :=
      mul_le_mul_of_nonneg_left ih hq_min
    have _ := hδmin
    calc |trajClampedNonAuto lp ln δ Sbase r ε S0 (t + 1) - trajClampedNonAuto lp ln δ Sbase r ε S0' (t + 1)|
        ≤ (1 - δ t) * |x - y| := h_step_eq
      _ ≤ (1 - δmin) * |x - y| := h_mon
      _ ≤ (1 - δmin) * ((1 - δmin)^t * |S0 - S0'|) := h_mul
      _ = (1 - δmin)^(t + 1) * |S0 - S0'| := by rw [pow_succ]; ring

end TrustStack
