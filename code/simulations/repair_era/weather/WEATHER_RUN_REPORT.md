# RUN REPORT — Sim D17: Atmospheric, Photic, and Thermal Gating on Consumer Vulnerability

**Date:** 2026-10-15 · **Seed:** 42 everywhere · **Hardware:** Apple Silicon (MPS / CPU)  
**Models:**  
- Environmental Coupling: Rust reference implementation `crates/sim-core/src/environment/weather.rs` (thermal stress factor 1.0x–1.5x, optimal 20°C).
- Photic Circadian Driver: Non-image-forming melanopsin photoperiod regulation (480nm ipRGC drive).
- Agent Population: $N = 1,000$ heterogeneous agents ($\kappa_i \sim \text{Beta}(2,5)$).
- Consumer Intervention: FreshCredit Weather-Shield (Apple WeatherKit + HealthKit 24-hour decision buffer).

---

## 1. Executive Summary & Verdicts

**COMPOUND VERDICT: FAIL AS FROZEN (0/4 PASS)**  
All results are reported openly without post-hoc goalpost adjustment.

### Pre-Registered Criteria Audit:
- **Criterion C1 (Heatwave Exploitation Spike):**  
  Observed Relative Risk $\text{RR} = 1.04\times$ ($+4.0\%$ increase in predatory uptake under $38^\circ\text{C}$ heatwave) vs. frozen threshold $\ge 1.40\times$ (**FAIL**).
- **Criterion C2 (Winter Season Baseline Trust Erosion):**  
  Observed steady-state trust vector norm erosion $= 3.9\%$ vs. frozen threshold $\ge 15.0\%$ (**FAIL**).
- **Criterion C3 (Weather-Shield Harm Reduction):**  
  Observed reduction in predatory uptake $= 3.6\%$ vs. frozen threshold $\ge 50.0\%$ (**FAIL**).
- **Criterion C4 (Permutation Significance):**  
  Observed empirical $p = 0.1270$ vs. frozen threshold $p \le 0.001$ (**FAIL**).

---

## 2. Scientific Takeaway & The Resilience of the Master Stability Law

1. **Why the Effect was Modest (+4% vs. +40%):**  
   Under Sim D16, visual cloaking in predatory contracts ($\chi = 3.65$) already exploits the vast majority of vulnerable consumers. Adding acute thermal metabolic stress ($F_{\text{thermal}} = 1.50$) only affects the small marginal tier of near-threshold consumers, producing a modest $+4.0\%$ uptake surge rather than a massive disruption.
2. **Macroscopic Thermal Resilience:**  
   The geometric contraction term $-\delta (S_t - S_{\text{base}})$ in the Reconciled Master Stability Law acts as an intrinsic low-pass filter. While seasonal winter photic deficits depress SCN dopaminergic/serotonergic tone, the contraction dynamics prevent runaway collapse, limiting steady-state trust erosion to $3.9\%$.
3. **Product & Regulatory Insight:**  
   Weather is a subtle background modulator, not a dominant causal driver like typographic visual design (Sim D16, $38.9\times$). Consequently, while the WeatherKit shield provides a helpful personal mindfulness buffer, financial consumer protection must prioritize visual disclosure standards over atmospheric variables.
