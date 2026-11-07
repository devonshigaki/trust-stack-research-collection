# PRE-REGISTRATION — Sim A1: Multi-Turn Generative Attacks vs. DMN Planning (ADVERSARIAL-LLM-DMN)

**Date:** 2026-10-24 · **Status:** FROZEN PRE-REGISTRATION (filed before simulation execution)
**Author:** Devon Shigaki · ORCID [0009-0003-8977-8010]
**Research Stack:** GTT §4.2 / DOCAS §5

## 1. Domain Hypothesis & Theoretical Motivation

Sim D16 tested static visual cloaking, but real-world generative LLM adversaries dynamically manipulate natural language streams over multiple turns to optimize extraction (Zero-Determinant extortion tactics). The defense against this, as hypothesized in the DMN-counterfactual rollout architecture, is forward-looking planning depth $K$.
**Hypothesis (A1):** An active adversary maximizing expectation-validation gaps ($\varepsilon$) will successfully extort (drive agent utility $< 0$) short-sighted, present-biased agents ($K \le 2$). However, equipping the agent with DMN counterfactual rollout planning of depth $K \ge 5$ will successfully neutralize the generative attack, maintaining net positive utility over a 20-round interaction.

## 2. Frozen Quantitative Criteria

### Criterion C1 (Adversarial Exploitation):
Against shallow-planning agents ($K = 1$), the adversary must successfully achieve an extortionate surplus, driving the agent's terminal cumulative utility below $0$.

### Criterion C2 (DMN Defense Neutralization):
Against deep-planning agents ($K \ge 5$), the agent's counterfactual rollout must detect the delayed betrayal traps, maintaining a terminal cumulative utility $> 0$ and reducing the adversary's extraction by at least **80.0%** compared to $K=1$.

## 3. Experimental Parameters & Methodology
- Multi-round trust game ($T = 20$ rounds).
- Adversary policy: Optimize a multi-turn trap (promises high validation $V$, delivers $V \ll E$ late in the sequence).
- Agent policy: MCTS / Counterfactual rollout with depth $K \in \{1, 3, 5, 8\}$.
- Agent evaluates expected utility $EU(a|T)$ over the rollout horizon, incorporating trust state $S_t$.
- $N = 500$ game episodes per $K$ condition.
- **Random Seed:** Strict `seed=42`.

## 4. Compound Verdict Rule
- **PASS:** Criteria C1 and C2 met.
- **FAIL:** Any criterion fails.