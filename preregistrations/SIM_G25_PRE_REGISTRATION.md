# PRE-REGISTRATION — Sim G25: The Weber–Fechner Decibel of Trust ($\text{dB}_T$) & Psychophysical Pain Threshold

**Date:** 2026-10-30 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** GTT §3, §4 / DOCAS §2.9, §5.13 / Master Stability Law  
**Random Seed:** 42 everywhere  

**Theoretical Anchors:**  
- Fechner, G. T. (1860). *Elemente der Psychophysik*. (Weber–Fechner logarithmic law).  
- Stevens, S. S. (1957). "On the psychophysical law." *Psychological Review*, 64(3), 153–181.  
- Melzack, R., & Wall, P. D. (1965). "Pain mechanisms: a new theory." *Science*, 150(3699), 971–979.  
- McEwen, B. S. (1998). "Stress, adaptation, and disease: Allostasis and allostatic load." *Annals of the New York Academy of Sciences*, 840(1), 33–44.

---

## 1. Domain Hypotheses & Theoretical Motivation

Trust is a physical force vector governing expectation–validation loops ($\varepsilon_t = V_t - E_t$). However, in human consciousness, it is perceived as a constructed psychological coordinate scaling logarithmically, directly analogous to acoustic loudness (Phons/Decibels) and pitch. 

We formalize the **Decibel of Trust ($\text{dB}_T$)**:
$$\text{dB}_T = 20 \log_{10}\left(\frac{S_t}{S_{\text{base}}}\right)$$
where $S_{\text{base}} = 0.50$ represents baseline neutrality.

The psychological update law incorporates logarithmic compression:
$$\Delta S_t = \lambda_{\text{eff}} \cdot \operatorname{sign}(\varepsilon_t) \cdot \ln\left(1 + \frac{|\varepsilon_t|}{\varepsilon_0}\right) - \delta_S (S_t - S_{\text{base}})$$

When mismatch magnitude exceeds the **Pain Threshold** ($|\varepsilon_t| \ge \theta_{\text{pain}}$), an allostatic gate flips: plasticity collapses ($\lambda_{\text{eff}} \to 0$), Cortisol surges to ceiling, and the agent enters irreversible structural trauma (trauma freezing), preventing further updates.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

- **C1 (Logarithmic Compression):** Across stimulus mismatch amplitudes $|\varepsilon| \in [0.1, 100.0]$, perceived trust updating $\Delta S$ must scale logarithmically ($R^2 \ge 0.95$ for logarithmic fit vs. $R^2 \le 0.70$ for linear fit).
- **C2 (Dynamic Range Expansion in $\text{dB}_T$):** The defined $\text{dB}_T$ metric spans $[-26.0\text{ dB}, +6.0\text{ dB}]$ across viable trust states ($S \in [0.025, 1.0]$), linearizing subjective discrimination near baseline ($S \approx 0.50$).
- **C3 (Pain Threshold Phase Transition):** When mismatch exceeds $\theta_{\text{pain}} = 3.5 \varepsilon_0$, learning plasticity collapses by at least $90.0\%$ ($\lambda_{\text{eff}} \le 0.10 \lambda_0$), and Cortisol locks at maximum ($C \ge 0.90$) in $\ge 95.0\%$ of agents.
- **C4 (Allostatic Structural Default):** Under repetitive sub-threshold stress accumulating beyond allostatic reserve ($A_{\text{cum}} \ge A_{\text{crit}} = 50.0$), the system undergoes sudden structural default (irreversible collapse of $S_t \to 0$), demonstrating that chronic stress precipitates pain collapse without a single acute catastrophe.

**Compound Verdict Rule:** PASS requires all four criteria (C1, C2, C3, C4) satisfied simultaneously. Any failure is reported as frozen without adjustment.
