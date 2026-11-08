/-
TrustStack.Tilt

The exponential (Esscher) tilt of GTT §2 (equations eq:tilt / eq:eu in the paper)
and its four printed Properties:

  1. P̃ is a probability vector (positivity, normalization).
  2. Neutral reduction: at ι = 0 the tilt is the identity, P̃ = P.
  3. Monotone optimism: tilted expected utility is nondecreasing in the trust
     index ι (proved in integrated form, EU s ≥ EU t for s ≥ t, which is the
     content of dEU/dι ≥ 0 without invoking differentiation machinery).
  4. Bounded distortion: |log(P̃(o)/P(o))| ≤ |γ ι|·(max U − min U), the sharp
     form of the printed bound 2γ·max|û| at |ι| ≤ 1 (see the paper's remark:
     the printed bound is the looser safe form).

No `sorry` placeholders are used.
-/

import Mathlib

open Finset Real

namespace TrustStack

variable {O : Type*} [Fintype O] [Nonempty O]

/-- Unnormalized tilt weight: w(o) = P(o)·exp(γ·ι·U(o)). -/
noncomputable def wtilt (P U : O → ℝ) (γ ι : ℝ) (o : O) : ℝ :=
  P o * Real.exp (γ * ι * U o)

/-- Partition function Z. -/
noncomputable def tiltZ (P U : O → ℝ) (γ ι : ℝ) : ℝ :=
  ∑ o, wtilt P U γ ι o

/-- The tilted probability vector P̃(o) = w(o)/Z. -/
noncomputable def tiltP (P U : O → ℝ) (γ ι : ℝ) (o : O) : ℝ :=
  wtilt P U γ ι o / tiltZ P U γ ι

/-- Tilted expected utility (eq:eu): EU(ι) = Σ_o P̃(o)·U(o). -/
noncomputable def EU (P U : O → ℝ) (γ ι : ℝ) : ℝ :=
  ∑ o, tiltP P U γ ι o * U o

section Basic

lemma wtilt_pos {P U : O → ℝ} (hP : ∀ o, 0 < P o) {γ ι : ℝ} (o : O) :
    0 < wtilt P U γ ι o :=
  mul_pos (hP o) (Real.exp_pos _)

lemma tiltZ_pos {P U : O → ℝ} (hP : ∀ o, 0 < P o) {γ ι : ℝ} :
    0 < tiltZ P U γ ι :=
  Finset.sum_pos (fun o _ => wtilt_pos hP o) Finset.univ_nonempty

/-- **Property 1a** — positivity of the tilted vector. -/
theorem tiltP_pos {P U : O → ℝ} (hP : ∀ o, 0 < P o) {γ ι : ℝ} (o : O) :
    0 < tiltP P U γ ι o :=
  div_pos (wtilt_pos hP o) (tiltZ_pos hP)

/-- **Property 1b** — the tilted vector sums to one. -/
theorem tiltP_sum {P U : O → ℝ} (hP : ∀ o, 0 < P o) {γ ι : ℝ} :
    ∑ o, tiltP P U γ ι o = 1 := by
  unfold tiltP
  rw [← Finset.sum_div]
  exact div_self (ne_of_gt (tiltZ_pos hP (γ := γ) (ι := ι)))

/-- **Property 2** — neutral reduction: at ι = 0, P̃ = P. -/
theorem tiltP_neutral {P U : O → ℝ} (hP1 : ∑ o, P o = 1) {γ : ℝ} (o : O) :
    tiltP P U γ 0 o = P o := by
  have hz : tiltZ P U γ 0 = 1 := by
    simp [tiltZ, wtilt, hP1]
  simp [tiltP, wtilt, hz]

end Basic

section Monotone

/-- Algebraic identity: the cross-normalized difference of tilted numerators
    expands as a double sum of pair terms. -/
lemma A_eq {P U : O → ℝ} {γ : ℝ} (s t : ℝ) :
    (∑ o, wtilt P U γ s o * U o) * (∑ o, wtilt P U γ t o)
      - (∑ o, wtilt P U γ t o * U o) * (∑ o, wtilt P U γ s o)
    = ∑ o, ∑ o', wtilt P U γ s o * wtilt P U γ t o' * (U o - U o') := by
  have step1 : ∀ o : O,
      (∑ o', wtilt P U γ s o * wtilt P U γ t o' * (U o - U o'))
      = wtilt P U γ s o * (U o * (∑ o', wtilt P U γ t o')
          - (∑ o', wtilt P U γ t o' * U o')) := by
    intro o
    rw [show (∑ o', wtilt P U γ s o * wtilt P U γ t o' * (U o - U o'))
        = ∑ o', (wtilt P U γ s o * (wtilt P U γ t o' * U o)
            - wtilt P U γ s o * (wtilt P U γ t o' * U o'))
        from Finset.sum_congr rfl (fun o' _ => by ring)]
    rw [Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
        ← Finset.sum_mul]
    ring
  rw [Finset.sum_congr rfl (fun o _ => step1 o)]
  rw [show (∑ o, wtilt P U γ s o * (U o * (∑ o', wtilt P U γ t o')
        - (∑ o', wtilt P U γ t o' * U o')))
      = ∑ o, ((wtilt P U γ s o * U o) * (∑ o', wtilt P U γ t o')
          - wtilt P U γ s o * (∑ o', wtilt P U γ t o' * U o'))
      from Finset.sum_congr rfl (fun o _ => by ring)]
  rw [Finset.sum_sub_distrib, ← Finset.sum_mul, ← Finset.sum_mul]
  ring

/-- Swapping the dummy indices in the double sum leaves it unchanged. -/
lemma swap_sum {P U : O → ℝ} {γ : ℝ} (s t : ℝ) :
    (∑ o, ∑ o', wtilt P U γ s o * wtilt P U γ t o' * (U o - U o'))
    = ∑ o, ∑ o', wtilt P U γ s o' * wtilt P U γ t o * (U o' - U o) := by
  rw [Finset.sum_comm]

/-- Nonnegativity of the symmetrized pair summand: for a ≥ 0,
    (x − y)·(e^{ax} − e^{ay}) ≥ 0, lifted through the positive weight factors. -/
lemma summand_nonneg {P U : O → ℝ} (hP : ∀ o, 0 < P o) {γ : ℝ} (hγ : 0 ≤ γ)
    {s t : ℝ} (hst : t ≤ s) (o o' : O) :
    0 ≤ (U o - U o') * (wtilt P U γ s o * wtilt P U γ t o'
        - wtilt P U γ s o' * wtilt P U γ t o) := by
  have e1 : Real.exp (γ * s * U o) * Real.exp (γ * t * U o')
      = Real.exp (γ * t * (U o + U o')) * Real.exp (γ * (s - t) * U o) := by
    rw [← Real.exp_add, ← Real.exp_add]
    congr 1
    ring
  have e2 : Real.exp (γ * s * U o') * Real.exp (γ * t * U o)
      = Real.exp (γ * t * (U o + U o')) * Real.exp (γ * (s - t) * U o') := by
    rw [← Real.exp_add, ← Real.exp_add]
    congr 1
    ring
  have hfac : wtilt P U γ s o * wtilt P U γ t o'
        - wtilt P U γ s o' * wtilt P U γ t o
      = P o * P o' * Real.exp (γ * t * (U o + U o'))
        * (Real.exp (γ * (s - t) * U o) - Real.exp (γ * (s - t) * U o')) := by
    unfold wtilt
    rw [show P o * Real.exp (γ * s * U o) * (P o' * Real.exp (γ * t * U o'))
        = P o * P o' * (Real.exp (γ * s * U o) * Real.exp (γ * t * U o'))
        from by ring]
    rw [show P o' * Real.exp (γ * s * U o') * (P o * Real.exp (γ * t * U o))
        = P o * P o' * (Real.exp (γ * s * U o') * Real.exp (γ * t * U o))
        from by ring]
    rw [e1, e2]
    ring
  rw [hfac]
  have ha : 0 ≤ γ * (s - t) := mul_nonneg hγ (sub_nonneg.mpr hst)
  have hexp : 0 ≤ (U o - U o')
      * (Real.exp (γ * (s - t) * U o) - Real.exp (γ * (s - t) * U o')) := by
    rcases le_total (U o) (U o') with h | h
    · have h1 : U o - U o' ≤ 0 := sub_nonpos.mpr h
      have h2 : Real.exp (γ * (s - t) * U o) ≤ Real.exp (γ * (s - t) * U o') :=
        Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left h ha)
      exact mul_nonneg_of_nonpos_of_nonpos h1 (sub_nonpos.mpr h2)
    · have h1 : 0 ≤ U o - U o' := sub_nonneg.mpr h
      have h2 : Real.exp (γ * (s - t) * U o') ≤ Real.exp (γ * (s - t) * U o) :=
        Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left h ha)
      exact mul_nonneg h1 (sub_nonneg.mpr h2)
  have hp : 0 ≤ P o * P o' * Real.exp (γ * t * (U o + U o')) :=
    le_of_lt (mul_pos (mul_pos (hP o) (hP o')) (Real.exp_pos _))
  calc 0 ≤ (P o * P o' * Real.exp (γ * t * (U o + U o')))
        * ((U o - U o') * (Real.exp (γ * (s - t) * U o)
            - Real.exp (γ * (s - t) * U o'))) := mul_nonneg hp hexp
    _ = (U o - U o') * (P o * P o' * Real.exp (γ * t * (U o + U o'))
        * (Real.exp (γ * (s - t) * U o) - Real.exp (γ * (s - t) * U o'))) := by ring

/-- **Property 3** — monotone optimism, integrated form:
    EU is nondecreasing in the trust index. -/
theorem EU_mono {P U : O → ℝ} (hP : ∀ o, 0 < P o) {γ : ℝ} (hγ : 0 ≤ γ)
    {s t : ℝ} (hst : t ≤ s) :
    EU P U γ t ≤ EU P U γ s := by
  have hZt : 0 < ∑ o, wtilt P U γ t o :=
    Finset.sum_pos (fun o _ => wtilt_pos hP o) Finset.univ_nonempty
  have hZs : 0 < ∑ o, wtilt P U γ s o :=
    Finset.sum_pos (fun o _ => wtilt_pos hP o) Finset.univ_nonempty
  have hEU : ∀ x : ℝ, EU P U γ x
      = (∑ o, wtilt P U γ x o * U o) / (∑ o, wtilt P U γ x o) := by
    intro x
    simp only [EU, tiltP, tiltZ, div_mul_eq_mul_div, ← Finset.sum_div]
  have hA : 0 ≤ (∑ o, wtilt P U γ s o * U o) * (∑ o, wtilt P U γ t o)
             - (∑ o, wtilt P U γ t o * U o) * (∑ o, wtilt P U γ s o) := by
    rw [A_eq s t]
    have hsym : ∀ o o' : O, 0 ≤ wtilt P U γ s o * wtilt P U γ t o' * (U o - U o')
        + wtilt P U γ s o' * wtilt P U γ t o * (U o' - U o) := by
      intro o o'
      have h := summand_nonneg (U := U) hP hγ hst o o'
      have e : wtilt P U γ s o * wtilt P U γ t o' * (U o - U o')
          + wtilt P U γ s o' * wtilt P U γ t o * (U o' - U o)
          = (U o - U o') * (wtilt P U γ s o * wtilt P U γ t o'
              - wtilt P U γ s o' * wtilt P U γ t o) := by ring
      rwa [e]
    have hsum : 0 ≤ ∑ o, ∑ o', (wtilt P U γ s o * wtilt P U γ t o' * (U o - U o')
        + wtilt P U γ s o' * wtilt P U γ t o * (U o' - U o)) :=
      Finset.sum_nonneg (fun o _ => Finset.sum_nonneg (fun o' _ => hsym o o'))
    have h2 : (∑ o, ∑ o', (wtilt P U γ s o * wtilt P U γ t o' * (U o - U o')
        + wtilt P U γ s o' * wtilt P U γ t o * (U o' - U o)))
        = 2 * (∑ o, ∑ o', wtilt P U γ s o * wtilt P U γ t o' * (U o - U o')) := by
      simp only [Finset.sum_add_distrib]
      rw [swap_sum]
      ring
    rw [h2] at hsum
    linarith
  rw [hEU t, hEU s, div_le_div_iff hZt hZs]
  linarith

end Monotone

section Bounded

/-- **Property 4** — bounded distortion, sharp form:
    |log(P̃(o)/P(o))| ≤ |γ ι|·(max U − min U). -/
theorem tilt_log_bound {P U : O → ℝ} (hP : ∀ o, 0 < P o) (hP1 : ∑ o, P o = 1)
    {γ : ℝ} (ι : ℝ) (o : O) :
    |Real.log (tiltP P U γ ι o / P o)|
      ≤ |γ * ι| * ((Finset.univ.image U).max' (Finset.univ_nonempty.image U)
          - (Finset.univ.image U).min' (Finset.univ_nonempty.image U)) := by
  classical
  set M := (Finset.univ.image U).max' (Finset.univ_nonempty.image U) with hM
  set m := (Finset.univ.image U).min' (Finset.univ_nonempty.image U) with hm
  have himg : ∀ o' : O, U o' ∈ Finset.univ.image U :=
    fun o' => Finset.mem_image.mpr ⟨o', Finset.mem_univ _, rfl⟩
  have hleM : ∀ o', U o' ≤ M := fun o' => Finset.le_max' _ _ (himg o')
  have hlem : ∀ o', m ≤ U o' := fun o' => Finset.min'_le _ _ (himg o')
  have hMm : 0 ≤ M - m := sub_nonneg.mpr (le_trans (hlem o) (hleM o))
  -- Bounds on c·U in terms of the extremes, with c := γ·ι of either sign.
  have hcmax : ∀ o', (γ * ι) * U o' ≤ max ((γ * ι) * m) ((γ * ι) * M) := by
    intro o'
    rcases le_total 0 (γ * ι) with hc | hc
    · exact le_max_of_le_right (mul_le_mul_of_nonneg_left (hleM o') hc)
    · exact le_max_of_le_left (mul_le_mul_of_nonpos_left (hlem o') hc)
  have hcmin : ∀ o', min ((γ * ι) * m) ((γ * ι) * M) ≤ (γ * ι) * U o' := by
    intro o'
    rcases le_total 0 (γ * ι) with hc | hc
    · exact min_le_of_left_le (mul_le_mul_of_nonneg_left (hlem o') hc)
    · exact min_le_of_right_le (mul_le_mul_of_nonpos_left (hleM o') hc)
  -- Bounds on Z: exp(min) ≤ Z ≤ exp(max).
  have hZle : tiltZ P U γ ι ≤ Real.exp (max ((γ * ι) * m) ((γ * ι) * M)) := by
    calc tiltZ P U γ ι
        ≤ ∑ o, P o * Real.exp (max ((γ * ι) * m) ((γ * ι) * M)) := by
          apply Finset.sum_le_sum
          intro o' _
          exact mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr (hcmax o'))
            (le_of_lt (hP o'))
      _ = Real.exp (max ((γ * ι) * m) ((γ * ι) * M)) := by
          rw [← Finset.sum_mul, hP1, one_mul]
  have hZge : Real.exp (min ((γ * ι) * m) ((γ * ι) * M)) ≤ tiltZ P U γ ι := by
    calc Real.exp (min ((γ * ι) * m) ((γ * ι) * M))
        = ∑ o, P o * Real.exp (min ((γ * ι) * m) ((γ * ι) * M)) := by
          rw [← Finset.sum_mul, hP1, one_mul]
      _ ≤ tiltZ P U γ ι := by
          apply Finset.sum_le_sum
          intro o' _
          exact mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr (hcmin o'))
            (le_of_lt (hP o'))
  -- Pass the bounds through the logarithm.
  have hlogZle : Real.log (tiltZ P U γ ι) ≤ max ((γ * ι) * m) ((γ * ι) * M) := by
    have h := (Real.log_le_log_iff (tiltZ_pos hP) (Real.exp_pos _)).mpr hZle
    rwa [Real.log_exp] at h
  have hlogZge : min ((γ * ι) * m) ((γ * ι) * M) ≤ Real.log (tiltZ P U γ ι) := by
    have h := (Real.log_le_log_iff (Real.exp_pos _) (tiltZ_pos hP)).mpr hZge
    rwa [Real.log_exp] at h
  -- The log-ratio is exactly γιU(o) − log Z.
  have hlog : Real.log (tiltP P U γ ι o / P o)
      = γ * ι * U o - Real.log (tiltZ P U γ ι) := by
    unfold tiltP wtilt
    rw [Real.log_div
        (ne_of_gt (div_pos (mul_pos (hP o) (Real.exp_pos _)) (tiltZ_pos hP)))
        (ne_of_gt (hP o)),
      Real.log_div (ne_of_gt (mul_pos (hP o) (Real.exp_pos _)))
        (ne_of_gt (tiltZ_pos hP)),
      Real.log_mul (ne_of_gt (hP o)) (ne_of_gt (Real.exp_pos _)), Real.log_exp]
    ring
  -- max(cM, cm) − min(cM, cm) = |c|·(M − m).
  have hspread : max ((γ * ι) * m) ((γ * ι) * M) - min ((γ * ι) * m) ((γ * ι) * M)
      = |γ * ι| * (M - m) := by
    have e : max ((γ * ι) * m) ((γ * ι) * M) - min ((γ * ι) * m) ((γ * ι) * M)
        = |(γ * ι) * M - (γ * ι) * m| := by
      rcases le_total ((γ * ι) * m) ((γ * ι) * M) with h | h
      · rw [max_eq_right h, min_eq_left h, abs_of_nonneg (sub_nonneg.mpr h)]
      · rw [max_eq_left h, min_eq_right h, abs_of_nonpos (sub_nonpos.mpr h)]
        ring
    rw [e, show (γ * ι) * M - (γ * ι) * m = (γ * ι) * (M - m) from by ring,
        abs_mul, abs_of_nonneg hMm]
  -- Assemble: |γιU(o) − log Z| ≤ max − min = |γι|(M − m).
  have h1 : γ * ι * U o - Real.log (tiltZ P U γ ι)
      ≤ max ((γ * ι) * m) ((γ * ι) * M) - min ((γ * ι) * m) ((γ * ι) * M) := by
    have ha := hcmax o
    linarith
  have h2 : -(γ * ι * U o - Real.log (tiltZ P U γ ι))
      ≤ max ((γ * ι) * m) ((γ * ι) * M) - min ((γ * ι) * m) ((γ * ι) * M) := by
    have hb := hcmin o
    linarith
  rw [hlog, ← hspread, abs_le]
  constructor <;> linarith

end Bounded

end TrustStack
