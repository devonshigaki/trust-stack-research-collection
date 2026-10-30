# PRE-REGISTRATION — Sim P7b & Sim P8b: Closing the TFP Protocol Open Proof Obligations

**Date:** 2026-10-30 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)  
**Authors:** Devon Shigaki · ORCID [0009-0003-8977-8010](https://orcid.org/0009-0003-8977-8010)  
**Research Stack:** TFP §3.7, §4 / Supporting Document §R / Master Stability Law  
**Random Seed:** 42 everywhere  

**Theoretical Anchors:**  
- TFP §3.7 (Open limitations: Sim P7 salience-parameter sensitivity analysis and Sim P8 verification re-run under explicit $\lambda^- = 4\lambda^+$ preset).  
- Axelrod, R. (1984). *The Evolution of Cooperation*.  
- Laibson, D. (1997). "Golden eggs and hyperbolic discounting." *QJE*, 112(2), 443–478.

---

## 1. Domain Hypotheses & Theoretical Motivation

In `tfp_revised.md` §3.7, two technical limitations remained explicitly open:
1. **Sim P7 limitation:** The protective effect of immediate validation against present-biased contract exploitation was demonstrated at only a single salience setting. A full 2D salience sensitivity grid $s \in [0.1, 1.0] \times \beta \in [0.4, 0.9]$ was registered as a requirement for the Supporting Document.
2. **Sim P8 limitation:** The canonical reputation attack taxonomy (Sybil, on-off, whitewashing) was evaluated on provisional code where the exact preset was unconfirmed. It was registered for a verification re-run under the explicit asymmetric preset $\lambda^- = 0.02, \lambda^+ = 0.005$ ($\lambda^- = 4\lambda^+$).

Sim P7b and Sim P8b execute these exact pre-registered batteries, permanently closing all open proof obligations in the TFP manuscript.

---

## 2. Pre-Registered Frozen Criteria (C1–C4)

- **C1 (Sim P7b Salience Monotonicity):** Across the 2D grid $s \in [0.1, 1.0] \times \beta \in [0.4, 0.9]$ ($N = 1,000$ agents, 8 replicas), predatory contract uptake reduction $\Delta U(s)$ must scale monotonically with observation salience $s$ (Spearman $\rho \ge 0.950$, $p < 0.001$).
- **C2 (Sim P7b Robust Protective Floor):** Even at minimal residual salience ($s = 0.20$), immediate validation must reduce adversarial contract uptake by at least $20.0$ percentage points relative to unmonitored baselines ($\Delta U \ge 0.200$, $p < 0.001$).
- **C3 (Sim P8b Explicit Asymmetric On-Off Domination):** Under the explicit asymmetric preset $\lambda^- = 0.02, \lambda^+ = 0.005$, on-off cycling attacks yield strictly negative net utility ($U_{\text{net}} < 0$) across all defection severities $d \ge 2$, verifying the theoretical on-off suppression threshold.
- **C4 (Sim P8b Sybil Linear Cost Multiplier):** Under the explicit asymmetric preset, the cost of manufacturing 10 units of standing scales strictly linearly with provider attestation multiplier $m$ ($R^2 \ge 0.999$), with a wall-clock time floor $\ge 1.4\text{ years}$ at $\le 2\text{ events/day}$.

**Compound Verdict Rule:** PASS requires all four criteria (C1, C2, C3, C4) satisfied simultaneously. Any failure is reported as frozen without adjustment.
