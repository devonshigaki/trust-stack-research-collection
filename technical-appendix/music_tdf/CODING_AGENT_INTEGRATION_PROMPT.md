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

## 4. DELIVERABLES VERIFICATION CHECKLIST
- [ ] `crates/engine-ports/src/apple_music.rs` updated with `TdfMusicVector`
- [ ] `crates/sim-core/src/music.rs` wired with $\tau$, $E$, $H_s$, and $\Delta \phi$
- [ ] `src/ingestion/apple_music_adapter.py` created and tested
- [ ] Integration tests in `crates/sim-core/tests/music_integration.rs` passing
- [ ] All statistical deliverables (`results/statistical_validation.json`, `results/plots/`) preserved
