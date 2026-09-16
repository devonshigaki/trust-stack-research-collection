# SIM G22 — Pre-registration (frozen before any data access)

**Title:** Reality-monitoring corruption of trust-stage dynamics — a source-mixing extension of Sim G6-M1
**Date frozen:** 2026-09-13
**Status:** FROZEN prior to implementation. No data have been generated for this study at freeze time.
**Parent model:** GTT §2–§3 trust-stage dynamics on Δ⁴; discrete stability law of Sim G6-M1.
**Empirical basis for the extension (verified against primary sources):**

- Dijkstra, N. & Fleming, S. M. (2023). Subjective signal strength distinguishes reality from imagination. *Nature Communications* 14. DOI 10.1038/s41467-023-37322-1. — Source-mixing model: percept P = V + αX (imagery sample V intermixed with perceptual sample αX); reality judgment = P > T (reality threshold, T = 2.5 = population mean vividness); V ~ N(2.5, 1) across subjects; congruent imagery raises judged-real probability (0.41 vs 0.25); judged-real trials show higher vividness; source-confusion frequency rises with imagery vividness.
- Dijkstra, N., von Rein, T., Kok, P. & Fleming, S. M. (2025). A neural basis for distinguishing imagination from reality. *Neuron* 113(15), 2536–2542.e4. DOI 10.1016/j.neuron.2025.05.015.
- Dijkstra, N., Kok, P. & Fleming, S. M. (2022). Perceptual reality monitoring: Neural mechanisms dissociating imagination from reality. *Neuroscience & Biobehavioral Reviews* 135, 104557. DOI 10.1016/j.neubiorev.2022.104557.
- Gendron, M., Lindquist, K. A., Barsalou, L. & Barrett, L. F. (2012). Emotion words shape emotion percepts. *Emotion* 12(2), 314–325. DOI 10.1037/a0026007. — Linguistic modulation of percept formation (motivates expectation vividness as linguistically influenced).

**Research question.** GTT's update law consumes the *perceived* outcome signal, not the veridical one. If outcome perception intermixes external evidence with internally generated expectation (imagery), then (a) trust convergence toward the true stage-mix target T* should degrade with imagery vividness, (b) weak-imagery observers should over-suppress genuine evidence (explained-away stagnation), and (c) a system-side aggregation defense should restore convergence only when expectations are idiosyncratic — not when they are shared (collective-illusion boundary).

## Frozen design

**Constants (identical to Sim G6-M1 unless stated):** state θ ∈ Δ⁴; λ = 0.35 (planted, not empirical); T\* = (0.2, 0.2, 0.2, 0.2); 60 initial conditions ~ Dirichlet(1); horizon 25 steps; master seed 20260913 (legacy `numpy.random.RandomState` stream); distance = Hellinger chord √(1 − Σ√(θφ)) (the convention established for the printed G6-M1 values); all decision means carry 10,000-draw percentile bootstrap 95% CIs.

**Per-observer imagery:** imagined target E_i ~ Dirichlet(1), fixed per trajectory per arm; imagery strength v_i ~ N(μ_v, 1) truncated at ≥ 0. Vividness grid μ_v ∈ {0, 1.25, 2.5, 3.75, 5.0}; E and v redrawn per grid point from sub-seed = master + grid index (deterministic).

**Update rule (all arms except Arm 0):** each step t, external evidence x_t ∈ {0,1} with strength α = 1. Mixed signal m_i(t) = v_i + α·x_t; judged **real** iff m_i(t) > T with T = 2.5 (ungated arms A/B) or T_i^cal = v_i + α/2 (calibrated arm C/D logic — see arms). Perceived target when x_t = 1: Ŝ_i = (α·T\* + v_i·E_i)/(α + v_i) — inseparable convex mixture, per source mixing. When x_t = 0 the signal is imagery-only; if judged real (hallucinated outcome) the update target is E_i. If judged imagined: no update (signal explained away as self-generated).

**Arms:**
- **Arm 0 — clean-perception gate.** v_i ≡ 0, reality gate bypassed (veridical observation). Exact G6-M1 reproduction.
- **Arm A — dense outcomes, idiosyncratic expectation.** x_t = 1 every step; ungated threshold T = 2.5.
- **Arm B — sparse outcomes.** x_t ~ Bernoulli(0.5) i.i.d. per step per trajectory (sub-seed = master + 100 + grid index); ungated.
- **Arm C — aggregation defense, idiosyncratic.** k = 8 independent channels per trajectory (independent E_{i,c}, v_{i,c} per channel, c = 1..8); each channel computes its own mixed Ŝ; the update consumes the channel mean of the judged-real channels' Ŝ (if none judged real, no update). Threshold per channel ungated T = 2.5.
- **Arm D — aggregation under correlated expectation (collective illusion).** As Arm C, but all channels share one E_s ~ Dirichlet(1) per trajectory (sub-seed = master + 200 + grid index).

## Frozen decision criteria (computed blind to outcomes; quantities not yet computed at freeze time)

- **C1 (instrument gate):** Arm 0: 60/60 trajectories inside d_H(θ₇, T\*) < 0.05. If C1 fails → study verdict **INDETERMINATE** (instrument), halt, report.
- **C2 (corruption, primary):** Arm A: d̄₂₅(T\*) > 0.05 at μ_v = 2.5 **and** at μ_v = 5.0; **and** at μ_v = 5.0, ⟨d(θ₂₅, E)⟩ < ⟨d(θ₂₅, T\*)⟩ (capture by expectation). All three → **PASS**, else **FAIL**.
- **C3 (stagnation, secondary failure mode):** Arm A at μ_v = 1.25: no-update step fraction ≥ 50% **and** d̄₂₅(T\*) > 0.05. Both → **PASS**, else **FAIL**.
- **C4 (sparse hallucination):** Arm B at μ_v = 5.0: imagination-driven update fraction (x=0 judged real) ≥ 10% **and** ⟨d(θ₂₅, E)⟩ < ⟨d(θ₂₅, T\*)⟩. Both → **PASS**, else **FAIL**.
- **C5 (aggregation rescue):** Arm C at μ_v = 5.0: d̄₂₅(T\*) ≤ 0.05 **and** dispersion ratio (d̄₂₅/d̄₀) within 1.25× of Arm 0's dispersion ratio. Both → **PASS**, else **FAIL**.
- **C6 (collective-illusion boundary):** Arm D at μ_v = 5.0: d̄₂₅(T\*) > 0.05 (rescue fails under shared expectation). **PASS**/**FAIL** — either outcome is reported as the documented boundary of the defense.

**Compound headline claim:** "imagery–perception intermixing corrupts trust convergence; multi-channel aggregation restores it if and only if expectations are idiosyncratic" holds iff C1 ∧ C2 ∧ C5 ∧ C6 all PASS. C3/C4 are reported independently regardless. No outcome is dropped.

**Statistical framing:** deterministic simulation against frozen thresholds; bootstrap CIs on decision quantities only. No p-values (pseudo-replication theater is disclaimed collection-wide).

**Permitted actions after data:** report PASS/FAIL/INDETERMINATE exactly as frozen; any post-hoc analysis is labeled post-hoc. Amendments before unblinding require a dated amendment block in this file with justification, added before criterion quantities are computed.

**Planned deposit artifacts:** `technical-appendix/sim-code/g22_reality_monitoring.py`, `technical-appendix/numbers/g22_results.json`, `figures/gtt/figG22_reality_monitoring.png` (+ `_column.png`), this file, and `SIM_G22_CLOSURE.md` after evaluation.
