<div class="center">

<span class="smallcaps">The Trust Stack</span>

*An Open Research Collection*

Devon Shigaki — The FreshCredit Lab — Independent Research

Correspondence: freshcredit.xyz

------------------------------------------------------------------------

</div>

<div class="center">

*Version 4.0 — October 2026*

</div>

This collection gathers works on a single question: what is trust, measured honestly? The works share one ontological foundation — that trust is not a psychological sentiment confined to human heads, but the invariant biophysical binding dynamic by which living systems maintain collective agency and minimize prediction error across scales, preceding the nervous system by over a billion years. The works share one formal object — trust as the measurable relation between an agent’s expectations and the validations its environment returns — and one discipline: every claim is intended to carry its epistemic status (derived, standard, analogy, homology, empirical, hypothesized, simulated); lapses are logged in the correction register below. Every claim carries its own falsification criteria, and a stack-wide symbol registry ($`\varepsilon_t = V_t - E_t`$, validation minus expectation; simulation identifiers Sim G…, Sim D…, Sim P…, Sim W…) keeps the notation consistent across works. Each work is self-contained in its claims and can be read without the others; derivations cited to the Technical Appendix are self-attested until it is deposited. The collection opens with *The Value of Trust*, a note from the author prefacing the works that follow.

**This collection is open and growing.** New works will be added over time as the research program develops; the listing below is the current state of the collection, not a fixed or final count.

<div class="center">

<span class="smallcaps">Contents</span>

</div>

## The Value of Trust — a note from the author, prefacing the collection

The collection’s prefacing note from the author: a standalone reflective essay on the asset beneath every other asset. Trust is the prior capacity that language, cooperation, and exchange each presuppose; it resists being willed, and that resistance is the concept’s most important property. Drawing on Erikson’s “basic trust versus basic mistrust” and the attachment framework of Bowlby and Ainsworth, the essay treats trust as the first survival mechanism and credit as trust made transactional, then sets down — as personal conviction, not theory — the ladder from self-love through discipline and self-respect to credibility, the asset a person holds when they have nothing else to offer as collateral. It closes with the epistemic terms on which the author asks to be read: transparency before elegance, simplicity after it, and no overclaiming anywhere a theory of trust is concerned. The essay serves as the philosophical and personal anchor of the collection, establishing the ethical and epistemic commitments of the program without reporting quantitative data.

The General Theory of Trust: A Multiscale Formalism\
for Expectation–Validation Dynamics
----------------------------------------------------

The theory paper. GTT proposes that trust is a measurable dynamical quantity defined by the relationship between an agent’s expectations ($`E`$) and the validations ($`V`$) returned by its environment, formalized as a five-component vector $`T = [D, O, C, A, S]`$ whose stabilization component obeys the update law $`\Delta S_t = \lambda(V_t - E_t)`$ — the Rescorla–Wagner delta rule with trust as the state variable. The paper assembles the theory’s machinery from established formalisms (Fisher–Rao information geometry on the stage-activity simplex, Lyapunov stability of the alignment state, a Langevin/Fokker–Planck stochastic extension, an observation-dependent dissipation model, and a Kuramoto-type collective transition labeled as formal analogy), separates four senses of “measurement,” reviews convergent evidence from behavioral genetics to economic institutions, and specifies a pre-registered empirical program whose population target $`\mu_\lambda = 0.61`$ inside an equivalence corridor $`[0.46, 0.76]`$ is a target hypothesis with stated falsification criteria, not an obtained result.

## The DOCAS Framework: A Computational Model of Trust Dynamics as a Parallel Multi-Timescale Neuromodulatory Architecture

The biology paper. DOCAS specifies the biological instantiation of the GTT trust vector: five neuromodulatory channels — Dopamine, Oxytocin, Cortisol, Adrenergic/noradrenergic arousal, Serotonin — running as a parallel, multi-timescale architecture (functional roles, not a serial cascade) in which the stabilized model recursively becomes the next expectation. Each channel is defined functionally against common mislabelings; channel interactions are formalized through $`\tau = -\mathrm{EFE}`$ with affective readouts as derivatives of $`\Delta\tau`$. The genetics content is held to a two-gate standard (genome-wide significance and independent replication): PDE4B fails the second gate and its cAMP-gain mechanism is presented strictly as a labeled hypothesis, and historical candidate genes are reviewed and set aside. A fully specified, pre-registered experimental protocol (OSF DOI: \[insert\]) — the dual-layer wearable/financial experiment and the DOCAS-GATE-1 pharmacological carrier gate — is specified as the framework’s decisive test; forward encoding with released TRIBE v2 weights is reported as instrument-level evidence only, and no neurochemistry was measured.

## The Fresh Protocol: A Decentralized Architecture for Trust Measurement and Validation

The engineering paper. TFP is a domain-agnostic, decentralized architecture that implements the GTT stability law as a live computational process: any verifiable interaction — a transaction, a credential check, an API call, a device attestation — functions as a validation event that updates a user-owned record: trust measurement where genuine vulnerability is at stake; verification/reputation measurement otherwise. The five-layer stack combines W3C decentralized identifiers with selective-disclosure credentials (SD-JWT, RFC 9901), database-per-tenant edge storage, a Substrate settlement and audit layer with demonstrated throughput, light-client verification, and x402 micropayment rails. The protocol ships no domain logic; its defining constraint is measurement-theoretic — centralized observation measurably distorts the observed, so measurement must be user-owned — and two honest boundaries are stated up front: user-owned measurement reduces but does not eliminate observation distortion, and per-tenant custody converts rare-catastrophic loss into frequent-small loss, a variance reduction whose expected-loss advantage is conditional and quantified.

## FreshCredit: Credit as Trust Quantified — whitepaper

The application. FreshCredit points the protocol’s domain-agnostic measurement stack at financial validation streams and rebuilds the credit pipeline — Report $`\to`$ Score $`\to`$ Offer — as the externalization of the DOCAS expectation–validation loop. The whitepaper documents the incumbent system’s failures with regulator- and primary-source-verified statistics (exclusion of tens of millions of creditworthy people, sanctioned error rates, concentrated breach risk, surveillance distortion), then specifies the replacement: dual measurement layers (a financial stream and a physiological stream that is structurally excluded from credit decisions), user-owned records with selective-disclosure credentials, and verified on-chain feedback. Benchmarks are printed as frozen, dated snapshots; modeled projections are labeled as projections; and an in-paper harm accounting (NNH analysis) states what the design costs as well as what it saves.

## Supporting Document — in preparation; deposit pending

The internal, timestamped register referenced across the works: pre-registered hypotheses and frozen criteria, simulation protocols and seeds, and audit trails (the Supporting Document §L/§S/§R references in GTT, DOCAS, and TFP). In preparation; deposit pending. Until it is deposited, the frozen-criteria and protocol claims in the works that cite it are self-attested.

## Technical Appendix — in preparation; deposit pending

The simulation-battery appendix referenced by TFP and the FreshCredit whitepaper (Sim-Battery A: Sybil, cold-start, and adoption studies; Sim-Battery B: control batteries), together with the frozen, versioned cost calculator snapshots. In preparation; deposit pending.

## Connectome-scale simulation series — deposited

Since the original deposit, the collection has run a pre-registered connectome simulation program testing the theory’s neural-level claims directly on synaptic wiring data. Two complete series and one in-progress replication are deposited in full — registrations, amendments, closures, readout CSVs, code, and logs — at OSF (DOI: \[insert\]):

- **F1 series** (*Drosophila* mushroom body, FlyWire v783): sugar–GRN gate PASS; F1a single-glomerulus drive INDETERMINATE-instrument; F1a2 FAIL on its frozen control-shuffle criterion (position-based 0.873, class-faithful 0.680, against a $`>0.95`$ requirement; acquisition and ablation criteria met); F1b compartment-resolved DAN gating PASS (7/7 as frozen; criteria 6–7 met at a floor-saturation value that is a calibration artifact, so the evidential weight rests on criteria 1–5). Reference fact: Kenyon cells supply 98.2% of the MBON input budget (whole-brain count). Reported in the DOCAS paper (F1-series subsection).

- **Simulation H1** (MICrONS mouse cortex, `minnie65_public` materialization 1822; frozen sample of 12,000 post-synaptic roots; four disclosed amendments): structural single-class dominance FAIL (median 0.313, maximum 0.360, against a 0.50 criterion); availability-tracking MET for 8/11 classes (exceptions are the self-recurrent 6P-IT, 6P-CT, 5P-NP motifs); dynamical permutation robustness MET ($`R_{\mathrm{perm}} = 1.340 \geq 0.50`$; gate 4/4). Compound verdict FAIL on the structural arm, MET on the dynamical arm: global partner permutation fails to abolish function in both species — on different metrics and criteria (the fly’s abolition index vs. a cortical throughput ratio), not a matched quantitative replication — while the single-class structural basis does not transfer. The joint pattern is the signature the framework’s functional-universality claim predicts: the law recurs, the wiring does not. Reported in the DOCAS paper (§5.7).

- **Simulation H01** (human cortex, H01 dataset): pre-registered under the same frozen criteria; in progress at the time of deposit.

| Simulation | Substrate | Verdict | Reported in |
|:---|:---|:---|:---|
| F1 gate / F1a / F1a2 / F1b | FlyWire v783 | PASS / INDETERMINATE / FAIL / PASS | DOCAS |
| H1 (A1 / A2 / B2) | MICrONS v1822 | FAIL / MET / MET | DOCAS §5.7 |
| H01 | H01 human cortex | in progress | (pre-registered) |
| G22 (C1–C4, C6 / C5 / compound) | G6-M1 stage manifold | PASS / FAIL / FAIL | GTT §4.6 |
| Sim L (L1 / L2 / L3) | 1,024-cell bioelectric lattice | FAIL / PASS / PASS | DOCAS §5.10 |
| Sim D17 (C1–C4) | 1,000 agents, thermal weather | FAIL as frozen (0/4) | DOCAS §5.11 |
| Sim D18 (C1–C4) | 1,000 agents, Baylor unconscious | FAIL as frozen (2/4) | DOCAS §5.12 |
| Sim D19 (C1–C4) | 1,000 agents, Perky reality filter | FAIL as frozen (2/4) | DOCAS §5.13 |
| Sim G24 (C1–C4) | 1,000 microcircuits, AM missense | FAIL as frozen (0/4) | DOCAS §5.14 |
| Sim G25 (C1–C4) | 1,000 agents, dB_T & pain threshold | FAIL as frozen (2/4) | DOCAS §5.15 |
| Sim D20 (C1–C4) | 1,000 agents, fast-talking audio | FAIL as frozen (3/4) | DOCAS §5.16 |
| Sim D21 (C1–C4) | 27 stimuli, multimodal TRIBE v2 | FAIL as frozen (3/4) | DOCAS §5.17 |
| Sim N (C1–C3) | 1,000 agents, Markov blanket | FAIL as frozen (2/3) | DOCAS §5.18 |
| Sim V (C1–C3) | 1D harmonic oscillator, fatigue | FAIL as frozen (1/3) | DOCAS §5.19 |
| Sim G26 (C1–C4) | 500 nodes, cultural topologies | FAIL as frozen (1/4) | GTT §7 |
| Sim M (C1–C4) | 10,000 listening sessions | PASS (4/4) | DOCAS §5.20 |
| Sim K (K1 / K2 / K3) | 1,024 agents, 50 generations | FAIL / PASS / PASS | DOCAS §5.21 |
| Sim C (C1 / C2 / C3) | 1,000 present-biased agents | PASS (3/3) | DOCAS §5.22 |
| Sim S (S1 / S2 / S3) | 256 agents, 8D embedding | PASS (3/3) | DOCAS §5.23 |
| Sim DMN (DMN-1–3) | 1,000 agents, K in [1..10] | FAIL / PASS / PASS | DOCAS §5.24 |
| Sim CRIT (CRIT-1–3) | 1,024 nodes, branching | FAIL / PASS / PASS | DOCAS §5.25 |
| Sim B (B1 / B2 / B3) | 512 non-neural cells, maze | PASS (3/3) | DOCAS §5.26 |
| Sim X (X1 / X2 / X3) | 4 substrates, Cell to Human | PASS (3/3) | DOCAS §5.27 |
| Sim META (META-1–3) | Universal cross-scale vector | FAIL / PASS / PASS | DOCAS §5.28 |
| Sim P7b / P8b | Protocol limitations gap closure | FAIL / PASS | TFP §3.7 |

## Perception-layer simulation — deposited

One further pre-registered simulation beyond the connectome series is deposited in full — registration, closure note, code, and results JSON — at OSF (DOI: \[insert\]): **Sim G22** (reality-monitoring corruption of trust-stage dynamics; seed 20260913; frozen criteria C1–C6). Expectation imagery intermixed with outcome perception corrupts convergence to the trust-stage attractor in the G6-M1 model at the source study’s sample-mean imagery vividness; both failure modes occur across the tested vividness grid (evidence explained away at low vividness; hallucinated-outcome updates under sparse outcomes at high vividness); eight-channel aggregation attenuates the bias $`\approx`$$`2.9\times`$ but fails its frozen restoration criterion; and shared expectations — the formalized collective illusion — collapse the rescue entirely. C1–C4 and C6 PASS; C5 FAIL; compound FAIL, reported (simulation on the G6-M1 model: $`\lambda`$ planted, vividness distribution imported from a visual-imagery study; no claim about human trust dynamics is made). Reported in GTT §4.6.

## About the author

Devon Shigaki is an independent researcher and founder of The FreshCredit Lab (Independent Research), Bellevue, Washington — an applied research lab working on trust, identity, and credit infrastructure. The papers in this collection were developed over six years, alongside and following formal professional training at MIT xPRO (MIT Professional Education) — Professional Certificate programs in Full Stack Development, Data Engineering, and AI & Machine Learning (certificate programs awarding continuing education units, not degree programs) — building on a decade of self-directed study in engineering and the behavioral sciences.

Shigaki is the sole inventor of record on four granted U.S. utility patents covering decentralized data storage, authorization, tokenization, and authorized execution (US 12,236,480; US 12,293,410; US 12,293,411; US 12,307,515); the papers’ conflict-of-interest statements disclose this portfolio and his role at FreshCredit. Every idea, formalism, and claim in these papers is his. AI assistants (Kimi K3, Moonshot AI; Claude Fable 5, Anthropic) were used for validation, adversarial review, and simulation code, and are acknowledged in each paper.

The work is personal in origin: after experiencing identity theft, and years of chronic loneliness — a condition the CDC reports affects roughly one in three U.S. adults — he set out to understand what trust actually is and how it could be measured without surveilling the people it is meant to serve. Over a year of recorded conversations on *The Credit of Things* podcast, he pressure-tested these questions with practitioners and scholars across finance, law, engineering, and public policy — including researchers at Harvard’s Human Flourishing Program and the University of Washington. The conversations shaped the questions; the papers stand on their own evidence.

ORCID: 0009-0003-8977-8010 $`\cdot`$ Correspondence: freshcredit.xyz $`\cdot`$ Bio: tism.ing

## Correction register

The stack-wide register of major withdrawn or corrected claims, one line each, with pointers into the works. This is the sole register; the cited sections state the current claims only, and the Supporting Document (deposit pending) holds the audit trails.

1.  **$`\lambda = 0.61`$ is a target, not a constant.** The population-mean trust-sensitivity is re-registered as a pre-registered target hypothesis inside equivalence corridor $`[0.46, 0.76]`$, with no derivation claimed (GTT §6 H2; whitepaper §3.4).

2.  **Corridor corroboration is achievable by misspecification bias alone.** The estimator certification is restricted: under Behrens-style adaptive-$`\lambda`$ truth the constant-$`\lambda`$ estimator recovers the $`\varepsilon^2`$-weighted gain, not the time average (21.7% of users outside the 0.15 corridor; population $`\hat{\lambda} = 0.472`$ at truth $`0.355`$ — inside the corridor, truth outside); the Behrens model comparison is load-bearing (SIM-R1 battery 1; GTT §6; whitepaper §3.4).

3.  **The 7.17-step ringing prediction is closure-conditional.** Zero-delay closure destroys ringing; smoothing closures drift the period 7.17–17.65 steps; empirical tests must verify the closure or joint-fit $`(\lambda, \alpha)`$ (SIM-R1 battery 2; GTT §6, §7(ix)).

4.  **Break/build asymmetry is harder to identify than assumed.** The two-gain estimator detects asymmetry direction (AUC 0.968) but inflates magnitude (2.84 vs 2.00) and reports spurious asymmetry under symmetric adaptive truth (p95 ratio 2.23) (SIM-R1 battery 1; GTT §7(x); TFP §3.7).

5.  **Phase-map artifact.** The retired arctan map reported $`R \approx 0.635`$ at zero coupling (an “incoherent control” showing coherence); the stereographic map restores the $`1/\sqrt{N}`$ floor (GTT §3.4, G21; TFP §3.6).

6.  **Kuramoto threshold demoted, then measured on real topologies.** $`K_c = 2/\pi g(0)`$ is a labeled mean-field reference, not a numerical prediction; the $`R > 0.7`$ level at $`K = 4.5`$ fails on sparse networks ($`\langle k\rangle
    \lesssim 25`$; BA $`m = 2`$ collapses to 0.416) while the $`K_c \approx 2`$ onset and functional form survive (SIM-R2 battery 4; GTT §3.4; TFP §3.6 Sim P1c).

7.  **Spectral separation reframed.** The 8.2-fold stable/volatile spectral figure is retired; the surviving $`3.5\times`$ result is a definitional consistency check, not external evidence (GTT §3.6 M2, G16).

8.  **“Costly to fake” deleted.** \$1.01 buys 10 units of standing unattested; the real Sybil defense is the attestation multiplier plus the wall-clock time floor (TFP §3.7 Sim P8; whitepaper §1.4).

9.  **DebtRank cascade withdrawn.** The custody-topology cascade application was a category error; both amplification numbers are deleted (TFP §3.7 Sim P6).

10. **Estimator artifacts on record.** The initial P5 transfer-entropy estimate carried a 0.6-bit finite-sample bias that inverted the verdict; P5b’s first kurtosis was float rounding; both corrections are documented with the runs (TFP §3.7).

11. **Throughput figures re-anchored to measurements.** The 623,230 TPS figure is Parity’s linear extrapolation, not a measurement; the printed figures are the measured 143,343 TPS (batch, 23 cores) and 10,920 TPS (P2P, 15 cores) (TFP §3.4).

12. **S-channel lexical null corrected and stabilized.** The “marginal” S result (p = .054) was a truncated-concept-list artifact; the corrected re-run is a full null (0/15, p = 1.0), stable across all six macroareas (SIM-R2 battery 7; DOCAS §4.6). CLICS node count clarified: 1,725 graph nodes after parsing vs 1,730 concept-table entries in the source (Tjuka et al. 2025); the filtered analysis graph is 1,386 concepts / 3,986 edges.

13. **Family-wise multiplicity demotions.** Across DOCAS’s 24-test permutation family (TFP’s and the whitepaper’s permutation tests sit outside this family), 9/24 survive Bonferroni and 13/24 survive BH; D-Expectation fails Bonferroni; D8-EN paraphrase and the adjacency ratio fail both; 6/13 BH survivors are disclosed post-hoc assemblies; the N.3 category-LOO decode survives every correction while remaining a known templatic-lexicon artifact (SIM-R2 battery 5; DOCAS §4.6).

14. **Benefit side priced with declared gaps.** The NNT benefit ledger (error-correction NNT 52/24/19 at $`q = 0.37/0.80/1.00`$, ceiling 19 = the incumbent’s 5.2% harm rate; cost channel net-negative at $`m = 1000`$; inclusion NNE $`\approx`$ 3.7–5, gated by cold-start seeding) declares Boost-based and global NNTs not computable without new data (SIM-R2 battery 6; whitepaper §4.4).

15. **Registration gap: reference scales unprinted.** The pre-registered $`\hat{a}_i`$ reference scales the Fisher–Rao simplex requires are printed nowhere in the stack; absolute metric values must carry their $`\hat{a}`$, and the values must be printed in the Supporting Document (SIM-R2 battery 3; GTT §3.1, §7(viii)).

16. **Cohen’s $`d = 3.7`$ effect size withdrawn.** The printed $`d = 3.7`$ was computed on a deterministic model (zero run variance), giving an invalid denominator; the effect size is withdrawn and the pipeline’s self-consistency results are reported as correlations against pre-registered thresholds only (DOCAS §5.2; Supporting Document §L).

17. **E2 frozen-criterion failure kept on record.** The neuromodulatory operator simulation failed its pre-registered double-dissociation criterion as frozen (O and C lesions); the cascade-signature reinterpretation is labeled post-hoc hypothesis generation, and the harness-mechanics amendments (criteria untouched) are documented with the run (DOCAS §5.3; Supporting Document §S.7).

18. **Barrett citation inversion corrected.** Earlier versions cited constructed-emotion theory as support for the five-carrier mapping — the reverse of its position; the corrected text states where DOCAS agrees (anti-essentialism) and where it departs (functional diagonal-dominance, in testable tension with degeneracy) (DOCAS §3).

19. **A-channel carrier conflation corrected.** Earlier versions labeled the fourth channel “Adrenaline (epinephrine/norepinephrine)”; epinephrine is peripheral and BBB-excluded, so the A channel is redefined as central noradrenergic arousal with peripheral sympathoadrenal activation as a coupled but distinct somatic channel (DOCAS §2.4).

<div class="center">

------------------------------------------------------------------------

</div>

*The collection is maintained by The FreshCredit Lab. Works are added as they are completed; each addition is self-contained, shares the collection’s symbol registry and epistemic labeling discipline, and carries its own competing-interests, data-availability, and verification statements. Simulation code, seeds, figures, and pre-registration documents are public on OSF (DOI: \[insert\]); the Supporting Document and Technical Appendix are in preparation, and the works’ claims that cite them are self-attested until they are deposited.*
