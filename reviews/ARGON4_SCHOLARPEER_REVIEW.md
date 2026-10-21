# ScholarPeer: Adversarial Reviewer Report (Gemini 4 Argon)

# Peer Review Simulation: DOCAS Version 4.0 Manuscript

**Journal Target:** *Nature Neuroscience* / *ICML* (Cross-disciplinary Neuro-AI & Computational Psychiatry)  
**Manuscript Title:** Biological Instantiation of the DOCAS Trust Architecture (Version 4.0)

---

## Reviewer 1: Theoretical & Systems Neuroscience
**Expertise:** Neuromodulatory systems, Active Inference, Constructivist Emotion Theory, Behavioral Genetics.

### General Assessment
This is an unusually self-critical and epistemically disciplined theoretical manuscript. Version 4.0 resolves the most fatal physiological flaw of earlier serial-cascade models of social evaluation: the timescale mismatch. By explicitly refactoring the Dopamine-Oxytocin-Cortisol-Adrenergic-Serotonin (DOCAS) framework into a **parallel, multi-timescale modulation architecture** spanning four orders of magnitude ($10^{-1}\text{ s}$ to $10^{3}\text{ s}$), the authors rescue the biological plausibility of the model. 

Furthermore, the manuscript’s adherence to post-2019 evidentiary standards in genetics and neuroendocrinology is exemplary. Demoting the Kosfeld intranasal oxytocin literature in favor of Shamay-Tsoory’s social salience hypothesis, explicitly separating central locus coeruleus–norepinephrine (LC-NE) from peripheral BBB-excluded epinephrine, and transparently reporting that their own lead genetic candidate (*PDE4B* rs7528604) fails independent replication in the UK Biobank (Purves et al.) and lacks GTEx v8 adult brain cis-eQTL support (Sim D15) sets a high bar for transparency.

However, significant theoretical tensions remain in the active inference formalization, the unresolved *PDE4B* schizophrenia directionality paradox, and the absence of sections §4.6 and §5 in the provided text, which allegedly contain the core in-silico empirical discharges.

### Specific Theoretical Critiques

#### 1. Active Inference Formalization and the Fragility of Dominance ($\S 3$)
The authors define $\tau = -\text{EFE}$ (Expected Free Energy) and map the Pleasure-Arousal-Dominance (PAD) space onto its trajectory:
$$\text{valence} = \text{sign}(\Delta\tau), \quad \text{arousal} = |\Delta\tau|, \quad \text{dominance} = \frac{d(\Delta\tau)}{dt}$$
While mapping affective readouts to derivatives of free energy is well-precedented (e.g., Joffily & Coricelli, 2013; Hesp et al., 2021), there is a mathematical inconsistency here. In discrete-time active inference (Friston et al., 2015, 2017), EFE ($G(\pi)$) is evaluated over policies $\pi$, whereas variational free energy ($F$) is evaluated over states per time step. $\Delta\tau$ is a discrete difference across belief updates, yet dominance is defined via a continuous time derivative $d(\Delta\tau)/dt$ (essentially $\ddot{\tau}$, affective acceleration). 
* **Critique:** In biological recordings or behavioral choice paradigms, taking the second derivative of a latent, model-fitted quantity ($\tau$) amplifies high-frequency estimation noise quadratically. The authors acknowledge sampling-rate dependence, but they must formalize this as a discrete second-order difference $\Delta^2 \tau_t = \Delta\tau_t - \Delta\tau_{t-1}$ or specify a temporal smoothing kernel (e.g., matched to the integration window of the C or S channel) to prevent the dominance term from being dominated by estimator variance.

#### 2. Diagonal Dominance vs. Constructivist Degeneracy ($\S 2.6, \S 2.9, \S 3$)
The authors formalize the carrier-to-function mapping via a gain matrix $g = M m$, claiming in **Claim 1** that $M$ is strictly diagonally dominant ($|M_{ii}| > \sum_{j \neq i} |M_{ij}|$). They frame this in direct, testable tension with Barrett’s Theory of Constructed Emotion, which posits *degeneracy* (many-to-one neural/chemical realizations of a functional or affective state).
* **Critique:** Neuromodulatory systems exhibit massive anatomical and receptor-level cross-talk (e.g., DRN 5-HT projections directly inhibit VTA DA neurons; OXTR expression on VTA/NAcc neurons gates dopaminergic RPE; BLA glucocorticoid effects require concurrent $\beta$-adrenergic activation, as the authors themselves cite via Roozendaal). Because $g$ and $m$ have heterogeneous physical units (e.g., $\Pi_t$ is inverse variance; $h_S$ is a step horizon; $\text{CORT}$ is nanomolar concentration while $\text{DA}$ is phasic firing rate), **row-wise diagonal dominance of $M$ is arbitrary under unit rescaling**. For Claim 1 to be falsifiable, $g$ and $m$ must be strictly non-dimensionalized (e.g., standardized to $z$-scores or fractional dynamic range under naturalistic variance) before evaluating $|M_{ii}| > \sum_{j \neq i} |M_{ij}|$.

#### 3. The *PDE4B* Schizophrenia Paradox ($\S 4.2, \S 4.4$)
The authors candidly flag a fatal directional contradiction: their model posits $\text{PDE4B}\downarrow \to \text{cAMP}\uparrow \to \lambda\uparrow$ (flexible updating, near-critical dynamics, high trust). Yet postmortem schizophrenia brains (Fatemi et al.; CommonMind)—a canonical phenotype of persecutory delusions and severely impaired social trust—exhibit *PDE4B* downregulation.
* **Critique:** Leaving this unresolved while maintaining Hypothesis 3 weakens the manuscript. The resolution likely lies in **inverted-U cAMP/PKA signaling in the prefrontal cortex** (Arnsten, 2009) and precision-weighting pathologies in psychosis (Adams et al., 2013). Excessive cAMP signaling in dendritic spines opens $\text{K}^+$ channels (HCN/KCNQ), *disconnecting* prefrontal recurrent networks and driving aberrant salience ($\Pi_t \to \infty$, supercritical noise $\nu > 1$). If $\text{PDE4B}\downarrow$ pushes the system *past* $\nu \approx 1$ into the supercritical runaway regime ($\S 4.4$), expectation $E$ is swamped by noise and paranoid priors lock in via compensatory top-down rigidity. Integrating this non-linear (inverted-U) mapping between cAMP and $\nu$ would resolve the schizophrenia paradox within the authors' own criticality framework.

#### 4. Fixed-$\lambda$ vs. Hierarchical Volatility ($\S 2.1, \S 2.9$)
The authors note that their fixed-$\lambda$ leaky delta rule lags behind hierarchical Bayesian learners (Behrens et al., 2007; Mathys et al., 2011). Yet in $\S 2.9$, the effective update rate in the master law is $\lambda r_t$, where $r_t$ is a monotone readout of $C_t = \text{logistic}(\beta_C(|\varepsilon_t| - \theta_C))$. Because $r_t$ scales with unsigned surprise $|\varepsilon_t|$, **$\lambda r_t$ already functions as an endogenous Pearce-Hall / volatility-modulated learning rate**. The authors are underselling their own math here: $C_t$ dynamically gates plasticity based on environmental volatility.

---

## Reviewer 2: Methodological, Computational & Adversarial Review
**Expertise:** Neuro-AI decoding, Representational Similarity Analysis (RSA), Pre-registration auditing, Simulation validation.

### General Assessment
My role is to audit the empirical claims, the epistemic tags, and the specific simulation batteries (Sim D-series and O-series). **First, a major structural defect must be flagged:** the submitted manuscript text cuts off mid-sentence at the end of $\S 4.5$ (*"...music transmits the temporal structure"*), omitting $\S 4.6$ and the entirety of $\S 5$ (*The DOCAS Experiment*), $\S 6$, and $\S 7$, while also leaving citation keys blank (e.g., `;` instead of author-year). 

However, evaluating the claims anchored in the Abstract, $\S 1.1$, $\S 2.9$, and $\S 4.2$ against the 5 specific methodological audit points reveals both commendable epistemic restraint (reporting pre-registered nulls) and severe limitations regarding what *in-silico* surrogate models can actually prove about wetware neurochemistry.

### Specific Audit of Required Empirical & Simulation Modules

#### 1. In-Silico Neural Decoding: Brain-IT / TRIBE vs. Gallant/Huth Atlas ($\S 1.1$)
* **Evaluation:** The authors discharge Proof Obligations 1–4 using TRIBE v2 (the Algonauts 2025 fMRI-prediction architecture) and supervised ridge regression bridging LLaMA embeddings to the Gallant/Huth `eng1000` semantic atlas, reporting Mantel correlations of $r = 0.252$ (cortical) and $r = 0.240$ (embedding), alongside pre-registered nulls on out-of-distribution (OOD) stimuli, multilingual arms (Sim D8), and a second encoder (Sim D9).
* **Adversarial Critique:** 
  1. **Circularity of Surrogate fMRI (TRIBE):** Testing whether DOCAS-labeled stimuli produce separable cortical patterns *predicted by an encoding model trained on naturalistic stimuli* (TRIBE / Brain-IT) does not test brain geometry; it tests the smoothness and feature space of the deep neural network surrogate. Because both LLaMA embeddings and TRIBE predictions are functions of stimulus text/audio statistics, a Mantel correlation of $r \approx 0.25$ predominantly reflects shared stimulus autocorrelation and low-level semantic clustering, not neuromodulatory channel separability.
  2. **Supervised Ridge vs. Unsupervised `vec2vec`:** In $\S 1.1$, Obligation 4 claims to discharge `vec2vec` (unsupervised latent space translation) by building a *supervised ridge map* on paired LLaMA $\leftrightarrow$ `eng1000` data. That is a bait-and-switch: fitting a regularized linear projection in a paired setting with thousands of dimensions is guaranteed to find a subspace alignment and does not validate the unsupervised geometric isomorphism claimed by `vec2vec`.
  3. **OOD Failure:** The recorded null on out-of-distribution stimuli (Sim D11 $\to$ D13 marginal) is the most diagnostic result in the paper: it proves the linear readouts are overfitting to the stimulus domain of the training corpus rather than capturing an invariant 5-channel biological coordinate system.

#### 2. Perceptual Cloaking (Sim D16)
* **Evaluation:** Not present in the truncated main text ($\S 5$ missing). In the context of the DOCAS operator loop ($\S 2.9$), perceptual cloaking / adversarial perturbation of input stimuli ($V_t$ or $s_t$) designed to evade the Recognition gate $C_t = \text{logistic}(\beta_C(|\varepsilon_t| - \theta_C))$ while accumulating drift in $S_t$ is a direct mathematical consequence of a hard threshold $\theta_C$.
* **Adversarial Critique:** Any adversary who bounds per-step betrayal below the cortisol recognition threshold ($|\varepsilon_t| < \theta_C$) drives $r_t \to 0$, preventing mismatch recognition or adrenergic activation ($A_t$) while exploiting the baseline leak $\delta_S$. However, until Sim D16 is explicitly integrated into the main text of $\S 5$ with formal bounds on sub-threshold drift versus cumulative integrator models (e.g., CUSUM), this claim cannot be verified from the manuscript text alone.

#### 3. Causal Optogenetics / Lesion Cascade (Sim O-Series / $\S 2.9$ & $\S 5.3$)
* **Evaluation:** In $\S 2.9$, the authors make a crucial admission regarding their in-silico lesion/perturbation battery ($\S 5.3$): *"Whether that cascade signature was a prediction or a post-hoc rationalization is answered in §5.3: as a pre-registered double-dissociation criterion it failed; as post-hoc hypothesis generation it is the next experiment’s target."*
* **Adversarial Critique:** I commend the authors for not HARKing (Hypothesizing After the Results are Known) here. Because the five operators are coupled in a closed recurrent loop ($E_{t+1}$ depends on $\varepsilon_t = V_t - E_t$, where $V_t$ is gated by $\gamma_O$, and $S_{t+1}$ is gated by $r_t(C_t)$), **clamping or lesioning any single parameter (e.g., $\alpha_D$, $\gamma_O$, $\beta_C$) necessarily perturbs all downstream state variables**. Consequently, the system *cannot* exhibit classic double dissociation under single-channel perturbation; it produces an ordered cascade. While the authors correctly label the failure of their pre-registered double-dissociation gate and reframe the ordered cascade as a post-hoc target, they must show in $\S 5.3$ that the *directed transfer entropy* or *Granger causality* of the cascade uniquely identifies the lesioned node, otherwise the 5-channel model is structurally unidentifiable from behavioral time series alone.

#### 4. Weather Gating / Exogenous Confounders (Sim D17)
* **Evaluation:** Omitted from the truncated text ($\S 5$). In peripheral wearable protocols (HRV, actigraphy, sleep architecture—which the authors admit in $\S 2.6$ are *"several inference steps from neuromodulatory tone"*), exogenous environmental variance (ambient temperature, barometric/seasonal shifts, circadian phase, physical exertion) massively confounds autonomic proxies of the A (sympathoadrenal) and C (HPA/cortisol) channels.
* **Adversarial Critique:** If Sim D17 models exogenous/weather gating on peripheral autonomic streams, the authors must demonstrate that their pre-registered de-confounding pipeline removes seasonal/meteorological variance without regressing out the slow tonic components of the S (hours/days) and C (20–45 min) channels. Because Cortisol and Serotonin operate on slow timescales that overlap with diurnal and environmental cycles, aggressive high-pass filtering will blind the wearable decoder to the C and S channels entirely.

#### 5. Baylor Unconscious Gating / Sub-threshold Interoceptive Gating (Sim D18)
* **Evaluation:** Omitted from the truncated text ($\S 5$). Within the DOCAS architecture ($\S 2.2, \S 2.9$), unconscious or pre-conscious gating corresponds to the dissociation between fast subcortical prediction error ($\text{DA}, \sim 100\text{ ms}$) / social coupling ($\gamma_O$) and conscious affective readout or thresholded recognition ($C_t, \theta_C$).
* **Adversarial Critique:** The manuscript explicitly states in the Abstract that *"All in-silico evidence reported here is instrument-level: no neurochemistry was measured anywhere in this paper."* Therefore, any simulation of unconscious striatal/insular gating (e.g., modeling Baylor-style sub-threshold reward/trust tasks in Sim D18) is strictly a **mathematical property of the parameterized logistic gate $C_t$ and the gain matrix $M$**—it is `[SIMULATION]`, not `[EMPIRICAL]` validation of human subcortical gating. It cannot be cited as evidence for biological carrier separability without concurrent fast-scan cyclic voltammetry (FSCV) or fMRI.

---

## 6. Summary Decision & Editorial Recommendation

**Decision: MAJOR REVISION (Borderline Reject if $\S 4.6$–$\S 7$ and missing citations are not restored)**

### Justification for Decision
This manuscript exhibits a level of epistemic honesty—specifically its `[HYPOTHESIS]` / `[SIMULATION]` labeling, its dismantling of its own *PDE4B* candidate via UK Biobank and GTEx v8 nulls (Sim D14/D15), and its transparent reporting of failed pre-registered double-dissociation criteria ($\S 2.9$) and OOD/multilingual nulls ($\S 1.1$)—that is rare and refreshing in computational neuroscience. The pivot to a parallel, multi-timescale architecture ($\S 2.8$) successfully addresses the physiological impossibility of serial neuromodulatory cascades.

However, the manuscript cannot be accepted in its current state for three reasons:
1. **Incomplete Manuscript Compilation:** The text terminates abruptly mid-sentence at the end of $\S 4.5$, omitting $\S 4.6, \S 5, \S 6, \S 7$, and the bibliography, and leaving LaTeX citation keys blank (`;`) throughout. The core empirical/simulation sections (including Sims D16, D17, D18, and the O-series lesion battery) are referenced in the front matter but missing from the body.
2. **Mathematical Normalization of Claim 1:** The diagonal-dominance claim for the neuromodulator-to-gain matrix $M$ ($\S 2.9$) is mathematically ill-posed without strict dimensionless normalization of both the neuromodulatory vector $m$ and the operator gain vector $g$.
3. **Over-interpretation of Surrogate Encoding Models:** Using TRIBE v2 and supervised ridge regression on `eng1000` ($\S 1.1$) to claim cortical-semantic alignment ($r = 0.252$) measures the smoothness of deep language/fMRI encoding models, not biological neuromodulatory channels. This must be explicitly downgraded from an empirical test of the biological architecture to an instrument-level consistency check.

### Mandatory Action Items for Revision
1. **Restore Full Text & Bibliography:** Supply the complete text of $\S 4.6$–$\S 7$ (specifically the full specifications and results of Sims D8–D18 and the O-series operator lesion battery) and fix all broken LaTeX `\cite{}` commands.
2. **Non-Dimensionalize the Gain Matrix $M$ ($\S 2.9$):** Define the exact unit-normalization or variance-standardization procedure for $g = Mm$ under which $|M_{ii}| > \sum_{j \neq i} |M_{ij}|$ is invariant to arbitrary unit rescaling.
3. **Regularize the Dominance Derivative ($\S 3$):** Replace the continuous derivative $d(\Delta\tau)/dt$ in Eq. (1) with a discrete-time filtered difference operator to bound estimation variance in empirical fits.
4. **Resolve the *PDE4B* Directionality Paradox via Inverted-U Dynamics ($\S 4.2, \S 4.4$):** Incorporate non-linear cAMP/PKA gain dynamics (where extreme *PDE4B* downregulation drives supercritical $\nu > 1$ noise and compensatory paranoid rigidity) to reconcile the schizophrenia postmortem expression data with the model’s equations.