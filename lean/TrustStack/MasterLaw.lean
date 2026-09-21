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
      ≤ |lp * max ε 0 * r| + |ln * min ε 0 * r| := abs_add _ _
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
          + |lp * max (ε t) 0 * r t + ln * min (ε t) 0 * r t| := abs_add _ _
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

end TrustStack
