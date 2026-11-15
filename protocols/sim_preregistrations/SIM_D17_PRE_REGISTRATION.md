# PRE-REGISTRATION — Sim D17: Atmospheric, Photic, and Thermal Gating on Consumer Vulnerability

**Date:** 2026-10-15 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** DOCAS §4 (Biological Photic Gating) / FreshCredit Whitepaper §3.4 & §4 (WeatherKit Consumer Shield)  
**Random Seed:** 42 everywhere

---

## 1. Domain Hypotheses & Theoretical Motivation

Environmental weather conditions act as an ambient, planetary-scale neuromodulatory intervention. 
1. **Photic Modulation (ipRGC / Melanopsin):** Solar irradiance (~480nm blue spectrum) stimulates retinal melanopsin, directly regulating suprachiasmatic nucleus (SCN) circadian pacing, increasing Serotonin ($S$) and Dopamine ($D$) baseline tone, and suppressing Cortisol ($C$). Overcast skies and winter photoperiods reduce photic drive by over 80%, eroding baseline patience ($S_{\text{base}}$).
2. **Thermal Stress & Cognitive Bandwidth Compression:** As modeled in FreshCredit's Rust core (`sim-core/src/environment/weather.rs`), deviations from optimal ambient temperature ($20^\circ\text{C}$) to extreme heat ($>35^\circ\text{C}$) or severe cold ($<0^\circ\text{C}$) increase metabolic stress factors up to $1.5\times$. This autonomic strain compresses agent cognitive bandwidth ($\kappa_i$), pushing consumers into the vulnerable $D_1$ decision regime identified in Sim D16.
3. **The Consumer Weather-Shield Intervention:** In FreshCredit's non-custodial architecture, an on-device personal data vault pairing Apple Watch autonomic stress with Apple WeatherKit atmospheric alerts can introduce an algorithmic decision buffer (a 24-hour cooling-off period during extreme heat/storm events).

**The Core Hypothesis [HYPOTHESIS / SIMULATION]:**  
Weather extremes (acute heatwaves and winter photoperiod deficits) biologically compress consumer cognitive bandwidth, multiplying the uptake of visually cloaked predatory contracts. An on-device Weather-Shield buffer that delays binding commitments during acute thermal distress will neutralize this weather-induced exploitation.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

All criteria are frozen before executing the simulation script.

* **Criterion C1 (Heatwave Exploitation Spike):**  
  Under an acute heatwave condition ($38^\circ\text{C}$, thermal stress factor $\ge 1.45\times$ per `sim-core/weather.rs`), predatory contract uptake among consumers ($\kappa_i \sim \text{Beta}(2,5)$) must increase by at least $40\%$ ($\text{Relative Risk } \text{RR} \ge 1.40$) compared to the temperate baseline ($20^\circ\text{C}$).
* **Criterion C2 (Winter Season Baseline Trust Erosion):**  
  Longitudinal exposure to Winter conditions ($5^\circ\text{C}$ baseline temperature, $70\%$ photic lux reduction) must suppress the steady-state trust vector norm $\|S_t\|$ by at least $15\%$ relative to Summer conditions due to down-regulated dopaminergic/serotonergic tone.
* **Criterion C3 (Weather-Shield Harm Reduction):**  
  The consumer-side Weather-Shield intervention (imposing a 24-hour decision buffer when ambient thermal stress $>1.30\times$) must reduce predatory loan uptake under severe heatwave conditions by at least $50\%$ ($\ge 0.50$ reduction in uptake).
* **Criterion C4 (Permutation Significance):**  
  Shuffling weather timestamps against contract offer presentations must abolish the weather-exploitation correlation ($p \le 0.001$ under 2,000 permutations).

**Compound Verdict Rule:**  
- **PASS:** All 4 criteria (C1–C4) met.  
- **FAIL:** Any criterion fails as frozen. All results reported openly without post-hoc goalpost adjustment.

---

## 3. Mathematical Specification

### Environmental Photic-Thermal Coupling:
Following `Developer/freshcredit/crates/sim-core/src/environment/weather.rs`:
- Ambient temperature $T_{\text{env}}(t)$ and Season cycles: Spring ($18^\circ\text{C}$), Summer ($28^\circ\text{C}$), Autumn ($15^\circ\text{C}$), Winter ($5^\circ\text{C}$).
- Thermal Energy Stress Factor:
  $$F_{\text{thermal}}(T) = 1.0 + \frac{\max(0, |T - 20.0|)}{15.0} \cdot 0.5 \quad (\text{clamped to } [1.0, 1.5])$$
- Photic Lux Drive: $\Phi_{\text{photic}} \in [0.15, 1.0]$ (Summer/Sunny $= 1.0$, Cloudy $= 0.4$, Rainy/Stormy $= 0.15$, Winter factor $= 0.6$).

### Dynamic Cognitive Bandwidth:
$$\kappa_i(t) = \frac{\kappa_{i, 0}}{F_{\text{thermal}}(t) \cdot \left(1.0 + 0.35 \cdot (1.0 - \Phi_{\text{photic}}(t))\right)}$$
where $\kappa_{i, 0} \sim \text{Beta}(2, 5)$.

### Contract Decision & Cloaking Filter (Sim D16 integration):
$$P_{\text{disc}, i}(t) = \frac{1}{1 + \exp\left(-\gamma \left(\frac{\kappa_i(t)}{\chi} - \tau\right)\right)}$$
with $\chi_{\text{PREDATORY}} = 3.65$, $\gamma = 8.0$, $\tau = 0.20$.
