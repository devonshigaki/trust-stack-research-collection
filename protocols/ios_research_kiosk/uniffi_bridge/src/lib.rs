uniffi::setup_scaffolding!();

/// Error type for invalid telemetry or parameter inputs
#[derive(Debug, Clone, PartialEq, thiserror::Error, uniffi::Error)]
pub enum TrustError {
    #[error("Non-finite input encountered in Master Law transition")]
    NonFiniteInput,
    #[error("Invalid recognition gate r_t (must lie in [0.0, 1.0])")]
    InvalidRecognitionGate,
    #[error("Invalid Master Law parameter (must satisfy 0 <= lambda, 0 < delta <= 1, s_base/s_t in [0, 1])")]
    InvalidParameterDomain,
    #[error("Audit chain integrity violation (non-monotonic version or broken prev_hash link)")]
    AuditChainBroken,
}

/// Master Stability Law parameters
#[derive(Clone, Debug, uniffi::Record)]
pub struct MasterLawConfig {
    pub lambda_plus: f64,
    pub lambda_minus: f64,
    pub delta: f64,
    pub s_base: f64,
    pub s_d: f64,
}

/// A sovereign trust record state
#[derive(Clone, Debug, PartialEq, uniffi::Record)]
pub struct TrustState {
    pub current_s: f64,
}

/// Append-only audit chain entry matching TFP_Edge_Protocol.tla
#[derive(Clone, Debug, PartialEq, uniffi::Record)]
pub struct AuditChainEntry {
    pub version: u64,
    pub prev_hash: String,
    pub state_s: f64,
    pub entry_hash: String,
}

fn sha256_hex(msg: &[u8]) -> String {
    const K: [u32; 64] = [
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
    ];
    let mut h: [u32; 8] = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    let mut buf = msg.to_vec();
    let bit_len = (buf.len() as u64) * 8;
    buf.push(0x80);
    while (buf.len() % 64) != 56 { buf.push(0); }
    buf.extend_from_slice(&bit_len.to_be_bytes());
    for chunk in buf.chunks_exact(64) {
        let mut w = [0u32; 64];
        for i in 0..16 { w[i] = u32::from_be_bytes([chunk[4*i], chunk[4*i+1], chunk[4*i+2], chunk[4*i+3]]); }
        for i in 16..64 {
            let s0 = w[i-15].rotate_right(7) ^ w[i-15].rotate_right(18) ^ (w[i-15] >> 3);
            let s1 = w[i-2].rotate_right(17) ^ w[i-2].rotate_right(19) ^ (w[i-2] >> 10);
            w[i] = w[i-16].wrapping_add(s0).wrapping_add(w[i-7]).wrapping_add(s1);
        }
        let [mut a,mut b,mut c,mut d,mut e,mut f,mut g,mut hh] = h;
        for i in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ ((!e) & g);
            let t1 = hh.wrapping_add(s1).wrapping_add(ch).wrapping_add(K[i]).wrapping_add(w[i]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = s0.wrapping_add(maj);
            hh = g; g = f; f = e; e = d.wrapping_add(t1); d = c; c = b; b = a; a = t1.wrapping_add(t2);
        }
        for (i, val) in [a,b,c,d,e,f,g,hh].iter().enumerate() { h[i] = h[i].wrapping_add(*val); }
    }
    h.iter().map(|x| format!("{x:08x}")).collect()
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

    /// Evaluates the Master Stability Law matching formal/lean/TrustStack/MasterLaw.lean:
    ///   eps_tilde = (V_t - E_t) / max(s_d, 1e-4)
    ///   Delta S_t = lambda(+/-) * eps_tilde * r_t - delta * (S_t - S_base)
    /// Rejects NaN/Inf and out-of-range recognition gates cleanly.
    pub fn apply_validation_event(
        &self,
        state: TrustState,
        v_t: f64,
        e_t: f64,
        r_t: f64,
    ) -> Result<TrustState, TrustError> {
        if !(state.current_s.is_finite()
            && v_t.is_finite()
            && e_t.is_finite()
            && r_t.is_finite()
            && self.config.lambda_plus.is_finite()
            && self.config.lambda_minus.is_finite()
            && self.config.delta.is_finite()
            && self.config.s_base.is_finite()
            && self.config.s_d.is_finite())
        {
            return Err(TrustError::NonFiniteInput);
        }
        if !(0.0..=1.0).contains(&r_t) {
            return Err(TrustError::InvalidRecognitionGate);
        }
        if self.config.lambda_plus < 0.0
            || self.config.lambda_minus < 0.0
            || self.config.delta <= 0.0
            || self.config.delta > 1.0
            || !(0.0..=1.0).contains(&self.config.s_base)
            || !(0.0..=1.0).contains(&state.current_s)
            || self.config.s_d <= 0.0
        {
            return Err(TrustError::InvalidParameterDomain);
        }

        let scale_sd = self.config.s_d.max(1e-4);
        let epsilon_tilde = (v_t - e_t) / scale_sd;
        let lambda = if epsilon_tilde >= 0.0 {
            self.config.lambda_plus
        } else {
            self.config.lambda_minus
        };

        let delta_s = (lambda * epsilon_tilde * r_t)
            - (self.config.delta * (state.current_s - self.config.s_base));
        let next_s = (state.current_s + delta_s).clamp(0.0, 1.0);
        Ok(TrustState { current_s: next_s })
    }

    /// Exact fixed-point integer Master Stability Law step (`FIXED_SCALE = 10^9`, `div_euclid`),
    /// matching `fresh-protocol-spec::MasterLawParams::step_fixed_i64` and `zk_master_law_stp.py` bit-for-bit.
    pub fn apply_validation_event_fixed_i64(
        &self,
        current_s_fixed: i64,
        v_fixed: i64,
        e_fixed: i64,
        r_fixed: i64,
    ) -> Result<i64, TrustError> {
        const FIXED_SCALE: i128 = 1_000_000_000;
        let cfg = &self.config;
        if !cfg.lambda_plus.is_finite()
            || !cfg.lambda_minus.is_finite()
            || !cfg.delta.is_finite()
            || !cfg.s_base.is_finite()
            || !cfg.s_d.is_finite()
        {
            return Err(TrustError::NonFiniteInput);
        }
        if cfg.lambda_plus < 0.0
            || cfg.lambda_minus < 0.0
            || cfg.delta <= 0.0
            || cfg.delta > 1.0
            || !(0.0..=1.0).contains(&cfg.s_base)
            || cfg.s_d <= 0.0
        {
            return Err(TrustError::InvalidParameterDomain);
        }
        let s = i128::from(current_s_fixed);
        let v = i128::from(v_fixed);
        let e = i128::from(e_fixed);
        let r = i128::from(r_fixed);
        if !(0..=FIXED_SCALE).contains(&s)
            || !(0..=FIXED_SCALE).contains(&v)
            || !(0..=FIXED_SCALE).contains(&e)
            || !(0..=FIXED_SCALE).contains(&r)
        {
            return Err(TrustError::InvalidParameterDomain);
        }
        let lp = (cfg.lambda_plus * (FIXED_SCALE as f64)).round() as i128;
        let ln = (cfg.lambda_minus * (FIXED_SCALE as f64)).round() as i128;
        let delta = (cfg.delta * (FIXED_SCALE as f64)).round() as i128;
        let s_base = (cfg.s_base * (FIXED_SCALE as f64)).round() as i128;
        let s_d_fixed = (cfg.s_d.max(1e-4) * (FIXED_SCALE as f64)).round().max(1.0) as i128;
        let eps = if s_d_fixed == FIXED_SCALE {
            v - e
        } else {
            ((v - e) * FIXED_SCALE).div_euclid(s_d_fixed)
        };
        let (eps_p, eps_n) = if eps >= 0 { (eps, 0) } else { (0, -eps) };
        let q_d = ((lp * eps_p - ln * eps_n) * r).div_euclid(FIXED_SCALE * FIXED_SCALE);
        let q_l = (delta * (s - s_base)).div_euclid(FIXED_SCALE);
        let clamped = (s + q_d - q_l).clamp(0, FIXED_SCALE);
        i64::try_from(clamped).map_err(|_| TrustError::InvalidParameterDomain)
    }

    /// Computes domain-separated SHA-256 entry hash for append-only audit chain anchoring.
    pub fn build_audit_entry(&self, prev: Option<AuditChainEntry>, next_s: f64) -> Result<AuditChainEntry, TrustError> {
        if !next_s.is_finite() || !(0.0..=1.0).contains(&next_s) {
            return Err(TrustError::InvalidParameterDomain);
        }
        let canon_s = if next_s == 0.0 { 0.0 } else { next_s };
        let (version, prev_hash) = match prev {
            Some(p) => (p.version + 1, p.entry_hash),
            None => (1, "0".repeat(64)),
        };
        let payload = format!("TFP_AUDIT_V1:{version}:{prev_hash}:{canon_s:.9}");
        let entry_hash = sha256_hex(payload.as_bytes());
        Ok(AuditChainEntry { version, prev_hash, state_s: canon_s, entry_hash })
    }

    /// Verifies strict monotonicity, state domain bounds, and hash-chaining of an audit chain slice.
    pub fn verify_audit_chain(&self, entries: Vec<AuditChainEntry>) -> Result<bool, TrustError> {
        let mut expected_prev = "0".repeat(64);
        for (idx, e) in entries.iter().enumerate() {
            if !e.state_s.is_finite() || !(0.0..=1.0).contains(&e.state_s) {
                return Err(TrustError::AuditChainBroken);
            }
            if e.version != (idx as u64) + 1 || e.prev_hash != expected_prev {
                return Err(TrustError::AuditChainBroken);
            }
            let canon_s = if e.state_s == 0.0 { 0.0 } else { e.state_s };
            let payload = format!("TFP_AUDIT_V1:{}:{}:{:.9}", e.version, e.prev_hash, canon_s);
            if sha256_hex(payload.as_bytes()) != e.entry_hash {
                return Err(TrustError::AuditChainBroken);
            }
            expected_prev = e.entry_hash.clone();
        }
        Ok(true)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn default_engine() -> TrustEngine {
        TrustEngine::new(MasterLawConfig {
            lambda_plus: 0.228,
            lambda_minus: 0.912,
            delta: 0.010,
            s_base: 0.500,
            s_d: 1.0,
        })
    }

    #[test]
    fn test_master_law_parity_nan_domain_and_audit_chain() {
        let eng = default_engine();
        let s0 = TrustState { current_s: 0.50 };
        let s1 = eng.apply_validation_event(s0.clone(), 0.85, 0.50, 1.0).unwrap();
        assert!((s1.current_s - 0.5798).abs() < 1e-9);

        assert_eq!(eng.apply_validation_event(s0.clone(), f64::NAN, 0.50, 1.0), Err(TrustError::NonFiniteInput));
        assert_eq!(eng.apply_validation_event(s0.clone(), 0.85, 0.50, 1.5), Err(TrustError::InvalidRecognitionGate));
        assert_eq!(eng.apply_validation_event(TrustState { current_s: 1.2 }, 0.85, 0.50, 1.0), Err(TrustError::InvalidParameterDomain));

        let bad_eng = TrustEngine::new(MasterLawConfig { lambda_plus: -0.1, lambda_minus: 0.9, delta: 0.01, s_base: 0.5, s_d: 1.0 });
        assert_eq!(bad_eng.apply_validation_event(s0, 0.85, 0.50, 1.0), Err(TrustError::InvalidParameterDomain));

        let e1 = eng.build_audit_entry(None, s1.current_s).unwrap();
        let mut e2 = eng.build_audit_entry(Some(e1.clone()), 0.43).unwrap();
        assert!(eng.verify_audit_chain(vec![e1.clone(), e2.clone()]).unwrap());
        e2.version = 1; // Replay / non-monotonic attack
        assert_eq!(eng.verify_audit_chain(vec![e1.clone(), e2]), Err(TrustError::AuditChainBroken));

        // Canonical -0.0 parity & rejection of forged NaN/out-of-range states in verify_audit_chain
        let ez_pos = eng.build_audit_entry(None, 0.0).unwrap();
        let ez_neg = eng.build_audit_entry(None, -0.0).unwrap();
        assert_eq!(ez_pos.entry_hash, ez_neg.entry_hash);

        let mut e_nan = eng.build_audit_entry(None, 0.5).unwrap();
        e_nan.state_s = f64::NAN;
        assert_eq!(eng.verify_audit_chain(vec![e_nan]), Err(TrustError::AuditChainBroken));
        let mut e_oob = eng.build_audit_entry(None, 0.5).unwrap();
        e_oob.state_s = 1.5;
        assert_eq!(eng.verify_audit_chain(vec![e_oob]), Err(TrustError::AuditChainBroken));

        // Exact fixed-point integer parity with fresh-protocol-spec & ZK-STP v8
        let fx1 = eng.apply_validation_event_fixed_i64(500_000_000, 850_000_000, 500_000_000, 1_000_000_000).unwrap();
        assert_eq!(fx1, 579_800_000);
        let fx2 = eng.apply_validation_event_fixed_i64(fx1, 100_000_000, 750_000_000, 1_000_000_000).unwrap();
        assert_eq!(fx2, 0);
        let fx3 = eng.apply_validation_event_fixed_i64(430_802_000, 500_000_000, 500_000_000, 1_000_000_000).unwrap();
        assert_eq!(fx3, 431_493_980);

        // Non-unit s_d = 2.0 fixed-point parity and NaN/<=0 domain rejection
        let eng_sd2 = TrustEngine::new(MasterLawConfig {
            lambda_plus: 0.228,
            lambda_minus: 0.912,
            delta: 0.010,
            s_base: 0.500,
            s_d: 2.0,
        });
        let s_sd2_float = eng_sd2.apply_validation_event(TrustState { current_s: 0.500 }, 0.850, 0.500, 1.0).unwrap().current_s;
        let s_sd2_fixed = eng_sd2.apply_validation_event_fixed_i64(500_000_000, 850_000_000, 500_000_000, 1_000_000_000).unwrap();
        assert!((s_sd2_float - (s_sd2_fixed as f64) / 1_000_000_000.0).abs() < 1e-8);

        let eng_nan_sd = TrustEngine::new(MasterLawConfig { lambda_plus: 0.228, lambda_minus: 0.912, delta: 0.010, s_base: 0.500, s_d: f64::NAN });
        assert_eq!(eng_nan_sd.apply_validation_event_fixed_i64(500_000_000, 850_000_000, 500_000_000, 1_000_000_000), Err(TrustError::NonFiniteInput));
        let eng_neg_sd = TrustEngine::new(MasterLawConfig { lambda_plus: 0.228, lambda_minus: 0.912, delta: 0.010, s_base: 0.500, s_d: -1.0 });
        assert_eq!(eng_neg_sd.apply_validation_event_fixed_i64(500_000_000, 850_000_000, 500_000_000, 1_000_000_000), Err(TrustError::InvalidParameterDomain));
    }
}

