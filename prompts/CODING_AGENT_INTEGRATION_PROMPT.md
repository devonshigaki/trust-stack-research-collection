# CODING AGENT INSTRUCTION: PRODUCTION INTEGRATION OF VALIDATED TDF MUSIC LAYER INTO FRESHCREDIT & SIM-CORE

**Context:** Sim M-Series empirical simulation successfully completed with a **COMPOUND PASS (4/4 pre-registered criteria satisfied)** on $N = 10,000$ listening sessions.  
**Theoretical Architecture:** GTT (General Theory of Trust) Master Stability Law $\Delta S_t = \lambda(V_t - E_t)$ & DOCAS §2 Neurochemical Channel Architecture ($D$: Dopamine, $O$: Oxytocin, $C$: Cortisol, $A$: Adrenaline, $S$: Serotonin).  
**Empirical Statistical Verdict:**
- **Metric Hierarchy ($\tau$):** $F = 3,561.48, p < 10^{-15}, \eta^2 = 0.5166$ (resolves scalar BPM degeneracy between Focus vs Decompression and Creative Flow vs Exercise).
- **Mutual Information Escalation:** $I(\text{Target State}; \vec{M}_{\text{TDF}}) = 3.8766\text{ bits}$ vs Baseline $1.6366\text{ bits}$ ($+136.87\%$ relative information gain).
- **State Decoding Macro $F_1$:** $0.9445$ (AUC $= 0.9931$), cutting baseline error by $71.0\%$ (Error Ratio $= 0.290 \le 0.500$).
- **Permutation Significance:** $p_{\text{perm}} = 0.0000$ ($B = 2,000$ iterations).

---

## 1. OBJECTIVE & ARCHITECTURAL OVERVIEW

You are tasked with integrating the empirically validated **TDF (The DOCAS Framework) Music Layer** into the production application and simulation codebase.
Legacy music ingestion and simulation layers rely solely on scalar tempo (BPM) and static genre tags. Your mission is to deploy the 5-dimensional TDF state vector pipeline:
$$\vec{M}_{\text{TDF}} = \begin{bmatrix} 
\text{Tempo (BPM)} \\ 
\text{Metric Hierarchy Ratio } (\tau) \\ 
\text{Spectral Energy / Loudness } (E) \\ 
\text{Session Entropy } (H_s) \\ 
\text{Phase / Skip Dynamics } (\Delta \phi) 
\end{bmatrix} \in \mathbb{R}^5$$

---

## 2. REPOSITORY & CODEBASE TARGETS

Inspect and integrate across the following existing codebase components in `freshcredit`:

1. **Port Trait Definitions:**
   - File: `crates/engine-ports/src/apple_music.rs`
   - Extend `AppleMusicSong`, `AppleMusicAlbum`, and `AppleMusicData` to capture:
     - `time_signature`: e.g., `"3/4"`, `"4/4"`, `"6/8"`
     - `metric_hierarchy_tau`: `f32` ($0.0$ for $3/4$ simple triple, $0.5$ for $4/4$ simple duple, $1.0$ for $6/8$ compound duple)
     - `spectral_energy`: `Option<f32>` ($E \in [0.0, 1.0]$)
     - `isrc`: `Option<String>` (International Standard Recording Code for acoustic metadata enrichment)
2. **Adapter Layer (Apple Music & MusicKit Client):**
   - File: `apps/product/adapters/src/apple_music/client/mod.rs` & `helpers.rs` & `trait_impl.rs`
   - Implement audio feature extraction and metadata enrichment:
     - Add ISRC catalog resolution to fetch meter and acoustic attributes when available.
     - Implement fallback inference for metric hierarchy $\tau$ based on genre, title, meter metadata, or client-side feature ingestion.
3. **Simulation Core Engine (`sim-core`):**
   - File: `crates/sim-core/src/music.rs`
     - Integrate `MetricHierarchyRatio` ($\tau$) into `CadencePattern` and `MusicState`.
     - Update `docas_rhythm` mapping to couple $\tau$ into the Oxytocin ($O$) channel ($\gamma_O = \tau$), $E$ into Adrenaline ($A$), $H_s$ into Cortisol ($C$), and $\Delta \phi$ into Dopamine ($D$).
   - File: `crates/sim-core/src/perception/auditory.rs`
     - Enrich `SoundEvent` and `AudioSignal` to process rhythmic subdivision and meter hierarchy.
4. **Simulator Service & Real-Time Ingestion (`sim-service`):**
   - File: `crates/sim-service/src/api/docas.rs`
     - Add `tdf_music_vector: Option<[f32; 5]>` to `DocasSnapshot` and `DocasPopulationStats`.
5. **Ingestion Adapter Implementation (`src/ingestion/`):**
   - Implement `src/ingestion/apple_music_adapter.py` (or Swift equivalent `apple_music_adapter.swift` for iOS/macOS clients) supporting:
     - Extraction of Apple Music playback telemetry (`playback_duration`, `skips_relative_to_bar`, `pause_events`).
     - Calculation of rolling 30-minute session entropy:
       $$H_s = -\sum_{k} p_k \log_2 p_k$$
     - Non-DRM audio stream metric analysis using vDSP (`Accelerate` framework) or FFT spectral energy estimation.

---

## 3. STEP-BY-STEP IMPLEMENTATION INSTRUCTIONS

### Step 1: Rust Domain Models & Port Trait Update
In `crates/engine-ports/src/apple_music.rs`:
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TdfMusicVector {
    pub tempo_bpm: f32,
    pub metric_hierarchy_tau: f32, // 0.0 = 3/4 simple triple, 0.5 = 4/4 simple duple, 1.0 = 6/8 compound duple
    pub spectral_energy: f32,      // E in [0.0, 1.0]
    pub session_entropy: f32,      // Hs in bits (rolling 30-min window)
    pub skip_dynamics: f32,        // Delta phi: structural boundary skip ratio
}
```
Enrich `AppleMusicSong` with `isrc: Option<String>` and `tdf_metrics: Option<TdfMusicVector>`.

### Step 2: Ingestion Adapter Logic (`src/ingestion/apple_music_adapter.py`)
Create the ingestion adapter `src/ingestion/apple_music_adapter.py`:
- Ingest raw Apple Music playback events (`play`, `seek`, `skip`, `pause`, `stop`).
- Compute `skip_dynamics` ($\Delta \phi$): Identify if a track was skipped within the first 15 seconds or mid-phrase vs. at track completion.
- Compute rolling 30-minute track distribution histogram and calculate Shannon entropy $H_s$.
- Parse time signature metadata into $\tau$:
  - `"3/4"` or `"3/8"` $\to \tau = 0.0$
  - `"4/4"` or `"2/4"` $\to \tau = 0.5$
  - `"6/8"` or `"12/8"` or `"9/8"` $\to \tau = 1.0$
  - Default / Ambiguous $\to 0.5$

### Step 3: Wire TDF Vector into `crates/sim-core/src/music.rs`
Update `MusicState` and `CadencePattern`:
- When an agent processes audio with metric hierarchy $\tau = 1.0$ ($6/8$ compound duple), stimulate Kuramoto coupling $\gamma_O$ and Dopamine exploratory drive:
  $$\Delta O_t = +0.08 \cdot \tau, \quad \Delta D_t = +0.05 \cdot \Delta \phi$$
- When an agent is exposed to high entropy $H_s > 2.0$, open the Cortisol recognition gate:
  $$r_{i,t} = \operatorname{logistic}(\beta_C (H_{s,t} - \theta_C))$$
- Scale sympathetic dissipation bandwidth $\mu$ proportionally to spectral energy $E$:
  $$\mu_t = \mu_0 \cdot (1.0 + 0.5 \cdot E)$$

### Step 4: Verification & Test Coverage
- Add unit and integration tests in `crates/sim-core/tests/music_integration.rs`:
  - Test `test_tdf_vector_modulation`: Verify that $\tau = 1.0$ ($6/8$) vs $\tau = 0.0$ ($3/4$) produces statistically distinguishable DOCAS trajectories at identical scalar BPM.
  - Test `test_session_entropy_gating`: Verify that high $H_s$ triggers Cortisol stress-recognition gating.
- Run `cargo test -p sim-core --test music_integration`.

---

## 4. SCIENTIFIC ATTRIBUTION & LIVE SIMULATOR METADATA

The live simulator and ingestion interfaces must preserve and display the academic research underpinning the simulation layer. When implementing the Rust modules in `crates/sim-core/src/music.rs` and the adapter in `src/ingestion/apple_music_adapter.py`, embed the following citations and computational tool references into module docstrings, metadata structs, and simulation telemetry outputs:

1. **Metric Hierarchies & Subdivision Perception:**
   - London, Justin (2012). *Hearing in Time: Psychological Aspects of Musical Meter* (2nd ed.). Oxford University Press.
   - Large, Edward W., & Jones, Mari Riess (1999). "The dynamics of attending: How people track time-varying events." *Psychological Review*, 106(1), 119–159.
2. **Expectation Dynamics, Downbeats & Prediction Errors:**
   - Huron, David (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
   - Salimpoor, Valorie N., et al. (2011). "Anatomically distinct dopamine release during anticipation and experience of peak emotion to music." *Nature Neuroscience*, 14(2), 257–262.
3. **Multi-Channel Neurochemistry of Music (DOCAS Foundations):**
   - Chanda, Mona Lisa, & Levitin, Daniel J. (2013). "The neurochemistry of music." *Trends in Cognitive Sciences*, 17(4), 179–193. (Maps music to Dopamine, Oxytocin, Cortisol, and Adrenaline).
   - Koelsch, Stefan (2014). "Brain correlates of music-evoked emotions." *Nature Reviews Neuroscience*, 15(3), 170–180.
   - Leman, Marc (2008). *Embodied Music Cognition and Mediation Technology*. MIT Press.
4. **Bioelectrics & Causal Tools in Sister Simulations:**
   - Evans, Benjamin D., et al. (2016). "PyRhO: A Python module for phenomological Modelling of Light-Activated Ion Channels." *Frontiers in Neuroinformatics*, 10: 8 (Sim O-Series).
   - Shreesha, Linda, & Levin, Michael (2024). "Stress sharing as cognitive glue: Morphogenetic homeostasis and bioelectric collective intelligence." *BBRC*, 700: 149591 (Sim L-Series).
   - Levin, Michael (2022). "Technological Approach to Mind Everywhere (TAME)." *Frontiers in Systems Neuroscience*, 16: 768201.

---

## 5. RECENT SIMULATION FRONTIERS FOR LIVE SIMULATOR TUNING

In addition to the TDF Music Layer (Sim M-Series), four new simulation batteries have been pre-registered, executed, and validated (all COMPOUND PASS), providing critical empirical parameters for tuning the live simulator in `crates/sim-core`:

1. **Sim P9 (Dynamically Coupled Kuramoto Layer):**
   - Location: `experiments/simulations_repair_era/tfp/`
   - Empirical Finding: Dynamically linking Master Law updates $\Delta S_k(t)$ to Kuramoto phase velocities ($\omega_k(t) = \Delta S_k(t)$) rescues collective coherence ($R = 0.907 \ge 0.700$) on sparse topologies ($\langle k \rangle \approx 25$). Wire this coupling directly into `crates/sim-core/src/simulation/society_engine.rs`.
2. **Sim B1 (TRIBE-BAYES-STREAM):**
   - Location: `experiments/simulations_repair_era/tribe_bayes/`
   - Empirical Finding: Streaming in-silico DMN threat BOLD proxies into the agent's Kalman filter enables near-perfect tracking of dynamic cognitive sensitivity $\lambda_t$ ($r = 0.996$), reducing state tracking MSE by $46.9\%$.
3. **Sim A1 (ADVERSARIAL-LLM-DMN):**
   - Location: `experiments/simulations_repair_era/adv_llm_dmn/`
   - Empirical Finding: Multi-turn LLM extortion traps destroy present-biased agents ($K = 1$, terminal utility $-1.000$), but deep DMN counterfactual rollout ($K = 5$) neutralizes trap loss by $100.0\%$ (utility $+0.750$). Ensure agent deliberation depth $K \ge 5$ is enabled for high-value contract evaluations.
4. **Sim S1 (SNUDDA-STRIATAL Microcircuits):**
   - Location: `experiments/simulations_repair_era/striatal_microcircuit/`
   - Empirical Finding: Microscopic integration of MSN dendritic eligibility traces $c(t)$ and Dopamine RPE pulses $D(t)$ correlates at $r = 1.0000$ with the discrete Master Law $\Delta S_t = \lambda(V_t - E_t)$, validating the simulator's macro-step equations against biophysical neurophysiology.

---

## 6. DELIVERABLES VERIFICATION CHECKLIST
- [ ] `crates/engine-ports/src/apple_music.rs` updated with `TdfMusicVector`
- [ ] `crates/sim-core/src/music.rs` wired with $\tau$, $E$, $H_s$, and $\Delta \phi$
- [ ] Academic citations and research provenance embedded into simulation docstrings and telemetry structs
- [ ] `src/ingestion/apple_music_adapter.py` created and tested
- [ ] Integration tests in `crates/sim-core/tests/music_integration.rs` passing
- [ ] All statistical deliverables (`results/statistical_validation.json`, `results/plots/`) preserved