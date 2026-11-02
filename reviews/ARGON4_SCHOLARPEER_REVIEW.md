# ScholarPeer: Adversarial Reviewer Report (Gemini 4 Argon)

# Peer Review Report: DOCAS Version 4.0 Manuscript

**Journal:** *Nature Neuroscience* / *ICML* (Joint Computational-Biological Track)  
**Manuscript Title:** DOCAS Version 4.0: Parallel, Multi-Timescale Neuromodulatory Instantiation of the Expectation–Validation Trust Architecture  
**Review Agent:** ScholarPeer (Gemini 4 Argon)

---

## Editorial Note on Manuscript Truncation
Before proceeding to the adversarial reviews, the editorial system notes a **critical submission defect**: the provided manuscript text terminates abruptly mid-word at the end of Section 4.4 (*"...if the relation fails at bas"*). **Sections 4.5–4.6 and the entirety of Sections 5, 6, and 7 are missing from the submitted text**, although their contents are previewed in the Abstract, Introduction (§1.1), and Section 2 cross-references. 

Both reviewers have evaluated the submitted text (Sections 1–4.4) with maximum rigor and have addressed the five requested empirical/simulation pillars based on their formal setup in the text and the epistemic constraints established in the Abstract and Introduction.

---

## Reviewer 1: Theoretical & Systems Neuroscience
**Expertise:** Neuromodulatory systems, Active Inference, Criticality, Psychiatric Genetics

### General Assessment
This is an exceptionally rare theoretical neuroscience manuscript: it is aggressively self-critical, mathematically explicit, and epistemically disciplined. By abandoning a physiologically absurd serial cascade in favor of a **parallel, multi-timescale modulation architecture** spanning four orders of magnitude ($10^{-1}\text{ s}$ to $2.7 \times 10^3\text{ s}$), the authors rescue the DOCAS framework from immediate biological falsification. 

The manuscript’s greatest strength is its **evidentiary honesty**. In a subfield plagued by just-so stories and zombie candidate genes (e.g., *OXTR*, *SLC6A4*), the authors enforce a strict two-gate genetic standard (GWS + independent replication) and immediately use it to **demote their own lead candidate (*PDE4B* rs7528604)** after it failed lookup in the UK Biobank ($p = .18$) and showed null cis-eQTL/sQTL signals in GTEx v8 adult brain (Sim D15). Similarly, the treatment of cortical criticality (§4.4) is the most balanced summary of the Touboul/Destexhe vs. Plenz/Beggs debate I have read in a primary model paper.

However, a major internal contradiction emerges in §4.2 vs. §4.4, and the mathematical coupling across timescales in §2.9 requires formal tightening.

### Major Theoretical & Neurobiological Critiques

1. **Internal Contradiction on the *PDE4B* Schizophrenia Paradox (§4.2 vs. §4.4):**
   In §4.2, the authors note that *PDE4B* expression is *downregulated* in schizophrenia postmortem brain, which points the wrong way for their model ($\text{PDE4B}\downarrow \to \text{cAMP}\uparrow \to \text{high }\lambda / \text{trust}$). In §4.2, they explicitly state: *"The contradiction is explicitly unresolved... none is adopted."* Yet two pages later, in §4.4, they state: *"The apparent contradiction regarding schizophrenia postmortem tissue... is resolved through the classic inverted-U profile of prefrontal cortical cAMP signaling"* (citing HCN/KCNQ channel shunting driving supercritical $\nu > 1$ chaos and compensatory rigid paranoid priors). The Arnsten inverted-U cAMP/HCN rescue is neurobiologically brilliant and biophysically sound—**pick one stance**. Either leave it unresolved in both sections or adopt the inverted-U supercriticality rescue as the unified `[HYPOTHESIS]` in §4.2 as well.

2. **Discrete-Time Operator Composition Across Four Orders of Magnitude (§2.9):**
   Equation (DOCAS preset) writes the master update law in discrete steps $t \to t+1$:
   $$S_{t+1} = S_t + \lambda\, r_t\, \varepsilon_t - \delta_S (S_t - S_{\mathrm{base}})$$
   If $\varepsilon_t$ is carried by phasic dopamine ($100\text{–}400\text{ ms}$) and $r_t$ is gated by cortisol ($C_t$, peaking at $20\text{–}40\text{ min}$), what is the physical duration of a single time step $\Delta t$? If $\Delta t \approx 200\text{ ms}$, then $r_t$ is quasi-static over $10^4$ steps, meaning cortisol cannot gate *which specific* phasic prediction error is consolidated unless $r_t$ acts retroactively on an eligibility trace (consistent with McGaugh’s basolateral amygdala consolidation literature cited in §2.3). You must explicitly introduce a synaptic eligibility trace $e_t$ (decaying over minutes) so that slow $C_t$ can retroactively gate fast $\varepsilon_t$ into $S_{t+1}$.

3. **Affective Readout and Dominance Noise Amplification (§3):**
   Defining dominance as the smoothed discrete second difference $\mathrm{dominance}_t = \Delta^2\tau_t * K_{\mathrm{smooth}}$ to avoid quadratic high-frequency noise amplification is mathematically necessary. However, if $K_{\mathrm{smooth}}$ is matched to the physiological integration window of the $C$ channel ($20\text{–}45\text{ min}$), how can the model account for rapid, sub-second shifts in subjective agency/dominance (e.g., sudden threat neutralization triggering an immediate transition from freeze to fight/flight via phasic LC-NE bursts)? The smoothing kernel should be tied to the **A channel (tonic-to-phasic LC mode-switching, seconds)** rather than the HPA axis.

4. **Diagonal Dominance of the Gain Matrix $M$ (Claim 1):**
   Claim 1 states $|M_{ii}| > \sum_{j \neq i} |M_{ij}|$ row-wise. Because the five neuromodulatory concentrations $m = (\mathrm{DA}, \mathrm{OT}, \mathrm{CORT}, \mathrm{NA}, \mathrm{5\mathord{-}HT})$ and the five computational gains $g = (\Pi, \gamma_O, (\theta_C, \beta_C), g_A, h_S)$ have entirely different physical units and dynamic ranges, diagonal dominance of $M$ is arbitrary unless both $m$ and $g$ are standardized (e.g., Z-scored or variance-normalized across naturalistic distributions). Specify the normalization scheme required to make Claim 1 scale-invariant.

---

## Reviewer 2: Methodological, Computational & Adversarial
**Expertise:** Neural Decoding, fMRI Encoding Models, Causal Inference, Pre-registration Auditing

### General Assessment
The authors deserve substantial credit for stripping away the inflated "isometry" claims often found in representational alignment papers and reporting modest, realistic effect sizes ($r = 0.252$ cortical, $r = 0.240$ embedding) alongside pre-registered null results (Sim D8, D9, D11, D15) and failed double-dissociation lesion cascades (§2.9). The explicit disclaimer in the Abstract—*"All in-silico evidence reported here is instrument-level: no neurochemistry was measured anywhere in this paper"*—preempts the most obvious adversarial attack.

However, because the submitted manuscript truncates at the end of §4.4, **the entirety of Section 5 (which houses the actual empirical and simulation battery) is absent from the review packet.** Below, I evaluate the five specific experimental/simulation modules requested by the Editor based on the architectural claims in §§1–4 and standard adversarial vulnerabilities in these paradigms.

---

### Evaluation of Specific Modules

#### 1. In-Silico Neural Decoding (Brain-IT / TRIBE vs. Gallant/Huth Semantic Atlas)
* **Strengths:** Using released Algonauts 2025-winning TRIBE v2 weights and supervised ridge bridges (LLaMA $\leftrightarrow$ eng1000) rather than unstable unsupervised GAN alignment (vec2vec) when paired stimuli exist is methodologically sound. Explicitly downgrading H1 from "isometry" to "measurable correlation" ($r = 0.252$ / $0.240$) and recording the out-of-distribution (OOD) null is exemplary.
* **Adversarial Critique:** TRIBE v2 and Huth/Gallant `eng1000` models are themselves trained on massive language/stimulus embeddings. Demonstrating a Mantel correlation of $r \approx 0.25$ between DOCAS-labeled stimuli and *predicted* cortical vectors (via TRIBE/eng1000) runs a severe risk of **feature circularity**: you are correlating one LLM-derived representation with a linear/nonlinear projection of another LLM-derived representation trained on fMRI. To prove this reflects biological trust geometry rather than shared transformer token statistics, Section 5 must report partial Mantel tests controlling for baseline lexical co-occurrence / low-level acoustic-visual envelope confounds, and explain why Sim D8 (multilingual) and Sim D9 (second encoder) yielded nulls.

#### 2. Perceptual Cloaking (Sim D16)
* **Adversarial Critique:** While Sim D16 is missing from the truncated text, "perceptual cloaking" in the context of expectation–validation loops ($E_t$ vs. $V_t$) and adversarial perturbations typically tests whether sub-threshold or metameric perturbations can alter downstream stabilization ($S_t$) or recognition gating ($C_t$) without triggering overt mismatch detection ($|\varepsilon_t| < \theta_C$). For this simulation to be valid in the revised manuscript, the authors must demonstrate that cloaked perturbations do not simply exploit artifacts in the ridge regression decoder or high-frequency aliasing in $\Delta^2\tau_t$, and must establish a clear psychophysical bound comparing human/biological perceptual thresholds against the logistic threshold $\theta_C$ in §2.9.

#### 3. Causal Optogenetics (Sim O-Series)
* **Strengths:** In §2.5 and §2.9, the authors rely on optogenetic DRN 5-HT stimulation (Miyazaki/Fonseca waiting paradigms) and closed-loop state-space control to validate the operator loop. Crucially, in §2.9 they admit that single-operator lesions/perturbations failed a pre-registered double-dissociation criterion because the closed loop ($S \to E$) creates an **ordered-cascade lesion signature**.
* **Adversarial Critique:** Calling an in-silico state-space simulation "Causal Optogenetics (Sim O-Series)" requires careful epistemic labeling (`[SIMULATION]`, not `[EMPIRICAL]`). Furthermore, if single-channel perturbations propagate around the loop ($D \to O \to C \to A \to S \to D$), then step-function optogenetic clamping of a single node (e.g., clamping 5-HT / $h_S$) will confound the identification of off-diagonal minority activations ($M_{ij}$) with recurrent loop propagation. To disambiguate direct off-diagonal coupling ($M_{ij} \neq 0$) from recurrent loop propagation in Sim O-Series, the perturbation impulse response must be measured at lag $\Delta t < \text{loop transit time}$, or recurrent edges must be computationally severed via open-loop clamping.

#### 4. Weather Gating (Sim D17)
* **Adversarial Critique:** In wearable longitudinal protocols (Section 5 pre-registration using HRV, sleep, and activity streams), environmental and meteorological variables ("Weather Gating", Sim D17—photoperiod, barometric pressure, ambient temperature) act as massive slow-timescale confounders on autonomic arousal ($A$), cortisol awakening response ($C$), and tonic serotonergic mood/seasonality ($S_{\mathrm{base}}$). If Sim D17 models exogenous environmental gating of the homeostatic baseline $S_{\mathrm{base}}$ or threshold $\theta_C$, the authors must prove that their decoder does not mistake meteorological/circadian autocorrelation in HRV and sleep architecture for endogenous social trust updates ($\Delta S_t$).

#### 5. Baylor Unconscious Gating (Sim D18)
* **Adversarial Critique:** Modeling sub-conscious / pre-conscious striatal prediction errors or social exchange gating (referencing Baylor-tradition human sub-second voltammetry / fMRI trust paradigms where caudate/putamen RPEs precede conscious declarative shifts) directly tests the split between fast phasic $D_t / O_t$ and slow thresholded recognition $C_t = \mathrm{logistic}(\beta_C(|\varepsilon_t| - \theta_C))$. Specifically, when $|\varepsilon_t| < \theta_C$, $r_t \approx 0$: the mismatch is registered sub-consciously in the fast $D$ channel ($E_{t+1}$ updates via $\alpha_D \Pi_t \varepsilon_t$) without triggering conscious allostatic recognition ($C_t$) or revising baseline stabilization ($S_{t+1}$). The authors must ensure that Sim D18 explicitly verifies this **mathematical dissociation between $E_{t+1}$ updating and $S_{t+1}$ stabilization** when $r_t \to 0$. Note: Currently, Equation (DOCAS preset) updates $S_{t+1}$ directly from $\varepsilon_t$ without showing how $E_{t+1}$ tracks $S_t$. If $E_t$ updates via $\alpha_D \Pi_t \varepsilon_t$ *and* "today’s $S$ becomes tomorrow’s $E$" (§2.5), the exact algebraic coupling between $E_{t+1}$ and $S_{t+1}$ is over-determined! Write out the coupled $(E_t, S_t)$ dynamical system explicitly.

---

## 6. Summary Decision

**Decision: MAJOR REVISION (Incomplete Submission — Missing §§4.5–7)**

### Conditions Required for Acceptance:
1. **Supply the Complete Manuscript:** Re-submit the full manuscript containing the truncated portion of §4.4, §§4.5–4.6, and the complete Sections 5, 6, and 7 so that the empirical/simulation batteries (Sim D8–D18, Sim L, Sim M, Sim O) and the OSF pre-registered wearable protocol can be audited directly.
2. **Resolve the Coupled $(E_t, S_t)$ Dynamics and Timescale Eligibility Trace (§2.9):** Explicitly write the joint update equations connecting $E_{t+1}$ and $S_{t+1}$, and introduce a synaptic eligibility trace $e_t$ to explain how a 20–40 minute cortisol gate ($r_t$) modulates a 200 ms dopaminergic prediction error ($\varepsilon_t$).
3. **Harmonize the *PDE4B* Schizophrenia Stance (§4.2 vs. §4.4):** Reconcile the "explicitly unresolved" statement in §4.2 with the "resolved through the classic inverted-U profile" statement in §4.4.
4. **Standardize the Gain Matrix $M$ (Claim 1):** Define the unit-normalization required to make diagonal dominance ($|M_{ii}| > \sum_{j \neq i} |M_{ij}|$) mathematically well-posed across heterogeneous biochemical and computational scales.