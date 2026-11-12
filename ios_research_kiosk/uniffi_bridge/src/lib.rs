uniffi::setup_scaffolding!();

/// Master Stability Law parameters
#[derive(uniffi::Record)]
pub struct MasterLawConfig {
    pub lambda_plus: f64,
    pub lambda_minus: f64,
    pub delta: f64,
    pub s_base: f64,
}

/// A sovereign trust record state
#[derive(uniffi::Record)]
pub struct TrustState {
    pub current_s: f64,
}

/// Encapsulates the core mathematical operations for the iOS Edge Kiosk
#[derive(uniffi::Object)]
pub struct TrustEngine {
    config: MasterLawConfig,
}

#[uniffi::export]
impl TrustEngine {
    #[uniffi::constructor]
    pub fn new(config: MasterLawConfig) -> Self {
        Self { config }
    }

    /// Evaluates the Master Stability Law: Delta S_t = lambda(V_t - E_t) - delta(S_t - S_base)
    /// Exposes memory-safe computation to Swift via C-ABI
    pub fn apply_validation_event(&self, state: TrustState, v_t: f64, e_t: f64) -> TrustState {
        let epsilon = v_t - e_t;
        let lambda = if epsilon >= 0.0 {
            self.config.lambda_plus
        } else {
            self.config.lambda_minus
        };
        
        let delta_s = (lambda * epsilon) - (self.config.delta * (state.current_s - self.config.s_base));
        let mut next_s = state.current_s + delta_s;
        
        // Clamp to [0, 1]
        if next_s > 1.0 { next_s = 1.0; }
        if next_s < 0.0 { next_s = 0.0; }

        TrustState { current_s: next_s }
    }
}
