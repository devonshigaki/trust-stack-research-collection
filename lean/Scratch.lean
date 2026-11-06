import Mathlib

theorem kuramoto_triangle (x1 y1 x2 y2 : ℝ) 
  (h1 : x1^2 + y1^2 ≤ 1) (h2 : x2^2 + y2^2 ≤ 1) :
  ((x1 + x2)/2)^2 + ((y1 + y2)/2)^2 ≤ 1 := by
  have h3 : (x1 - x2)^2 ≥ 0 := sq_nonneg (x1 - x2)
  have h4 : (y1 - y2)^2 ≥ 0 := sq_nonneg (y1 - y2)
  linarith
