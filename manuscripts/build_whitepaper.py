#!/usr/bin/env python3
"""Convert whitepaper.md (+ mandatory patches) to submission LaTeX."""
import os, re, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(BASE_DIR, 'whitepaper.md')
OUT_TEX = os.path.join(BASE_DIR, 'whitepaper.tex')


# ============================ load =========================================
md = open(MD_PATH).read()

# ======================= mandatory patches =================================
def rep(old, new, label):
    global md
    assert md.count(old) == 1, f"PATCH FAIL [{label}]: {md.count(old)}x {old[:80]!r}"
    md = md.replace(old, new)
    print("patch ok:", label)

rep("The full machinery has been run end-to-end on synthetic users with known ground truth, against pre-registered criteria frozen in code before the passing run: latent trajectory recovery r = 0.879 (threshold 0.7); λ̂ recovery error 0.024 (threshold 0.15); planted",
    "The full machinery has been run end-to-end on synthetic users with known ground truth, against pre-registered criteria frozen in code before the passing run: latent trajectory recovery r = 0.879 (threshold 0.7);\x03TRAJ\x04 λ̂ recovery error 0.024 against the certified tolerance 0.15 — and a 300-user re-run of the estimator (mixed-sign ε̃ streams with 12–15% negative heavy-tailed betrayals, Poisson cadence 0.3–3 events/day over 365 days, median 569 events per user, heavy-tailed Student-t observation noise, and a deliberately misspecified Kalman/EM noise setting) reports |λ̂ − λ| mean 0.0074, p95 0.0215, max 0.0343: the tolerance passes at every summary level (Figure 6). A planted λ = 0 negative control recovers max|λ̂| = 0.0092 (no phantom sensitivity), and an ultra-thin-stream stress test (60–110 events per user) yields maximum error 0.0737 — under half the tolerance at the worst corner; planted",
    "P1 estimator validation")

rep("(the base-rate dependence is demonstrated on real credit data in Sim W7: the same instrument's PPV falls from 0.47 at 22% prevalence to 0.03 at 1%)",
    "(the base-rate dependence is demonstrated on real credit data in Sim W7: the same instrument's PPV falls from 0.47 at 22% prevalence to 0.03 at 1% — reproduced exactly in the re-run, Figure 7)",
    "P2 PPV figure ref")

rep("Any nonzero organic floor escapes, but on very different clocks: at 0.01 organic events/day the trust state stabilizes at **day 562**; at 0.05/day, day 143; at 5/day, **day 23**.",
    "Any nonzero organic floor escapes, but on very different clocks: at 0.01 organic events/day the trust state stabilizes at **day 562**; at 0.05/day, day 143; at 5/day, **day 23**.\x03COLD\x04 A seeded, score-independent floor of 2 events/day for the first 30 days (provider-initiated onboarding events) escapes to a decisionable score at **day 72** — versus day 563 on the organic-only 0.01/day clock, a 7.8× acceleration from a one-month seeding commitment (Figure 8).",
    "P3 cold-start")

rep("and each newly measurable user densifies the validation graph, lowering per-measurement cost for the next — but both are bootstrapping-phase dynamics (§4.7 carries the cold-start analysis), and no static CAC figure is asserted.",
    "and each newly measurable user densifies the validation graph, lowering per-measurement cost for the next — but both are bootstrapping-phase dynamics (§4.7 carries the cold-start analysis), and no static CAC figure is asserted. The densification mechanism is quantified in the battery's adoption model (an adoption ODE with densification coupling κ feeding back through the cold-start clock of Figure 8; Figure 9), and its regions are stated, not assumed: adoption **stalls** (adopted fraction after 10 years < 0.2) when the organic event floor is ≲ 0.01/day **and** κ ≲ 0.5 jointly — the compounding assumption fails there; it **compounds** (adopted fraction ≥ 0.8 by year 10) at an organic floor ≥ ~0.1/day, or κ ≥ ~2, or strong densification alone; and the exact trap exists only at (floor, κ) = (0, 0). One modeling-choice caveat is carried explicitly: densification alone (κ = 5, zero organic floor) bootstraps off the model's 1% initial cohort to ~95% adoption by year 10, so the population-level trap requires both floors at zero while the individual-level trap of §4.7 is sharper — the boundary between stall and escape is a stated modeling choice with stated parameters, not a tuned constant.",
    "P4 adoption regions")

rep("while at K ≥ 6 the R > 0.7 claim survives to ℓ ≈ 0.15.",
    "while at K = 6 the R > 0.7 claim survives to ℓ ≈ 0.225 in the re-rendered surface (the previously printed ℓ ≈ 0.15 was a conservative coarse read-off; K = 8 survives beyond ℓ = 0.30).",
    "P5a K=6 robustness")

rep("R rises from the 1/√N floor to ≈ 0.85 at K = 8, ℓ = 0, and the R = 0.7 contour retreats from K ≈ 4.4 (ℓ = 0) to K ≈ 5.5 (ℓ = 0.1), K ≈ 7 (ℓ = 0.2), and off-grid for ℓ ≳ 0.25. (b) R vs. K at fixed ℓ. At the K = 4.5 operating point the coherence claim R > 0.7 survives only for ℓ ≲ 0.02 (fragile); at K ≥ 6 it survives to ℓ ≈ 0.15.",
    "R rises from the 1/√N floor to ≈ 0.85 at K = 8, ℓ = 0, and the R = 0.7 contour retreats from K ≈ 4.4 (ℓ = 0) to K ≈ 5.0 (ℓ = 0.1) and K ≈ 5.9 (ℓ = 0.2) on the re-rendered surface — the previously printed K ≈ 5.5 / ≈ 7 were conservative coarse read-offs, and the values here are the precise ones — moving off-grid for ℓ ≳ 0.25. (b) R vs. ℓ at fixed K. At the K = 4.5 operating point the coherence claim R > 0.7 survives only for ℓ ≲ 0.02 (fragile); at K = 6 it survives to ℓ ≈ 0.225 and at K = 8 beyond ℓ = 0.30 (printed ≈0.15/≈0.25 conservative).",
    "P5b Figure 5 caption")

rep("robust to ℓ ≈ 0.15 at K ≥ 6; corrected control baseline 0.03–0.05",
    "robust to ℓ ≈ 0.225 at K = 6 (printed ≈0.15 conservative; K = 8: ℓ > 0.30); corrected control baseline 0.03–0.05",
    "P5c W4 claims-map row")

rep("while a DID anchored once, accumulating validated history on the same blockchain-plus-edge infrastructure that already collapsed payment settlement to sub-cent (x402), makes each subsequent verification a local read against an existing historical identity.",
    "while a DID anchored once, accumulating validated history on the same blockchain-plus-edge infrastructure that already collapsed payment settlement to sub-cent (x402), makes each subsequent verification a local read against an existing historical identity. Stated as one concrete like-for-like decision: over a 20-query decision life (twenty verification reads against the same standing), the incumbent re-purchases identity at every query — $1,000–$2,200 at the $50–$110+ per-pull band — while FreshCredit anchors the history once at ~$1.01 unrolled ($0.0001 rolled, K = 10⁴) and each of the twenty reads is a local read at ≈$0 (Figure 4).",
    "P6 20-query cost")

rep("the key/guardian-loss channel is a separate term: at a 0.5%/yr key-loss base rate it adds ~1.5M record-equivalents/yr at 3×10⁸ tenants — **the same order as the entire per-tenant attacker-exposure win in the favorable region (1.8M/yr)**.",
    "the key/guardian-loss channel is a separate term, scaling linearly in the key-loss base rate: **0.3 / 1.5 / 3.0 million record-equivalents per year at p_key = 0.001 / 0.005 / 0.01** (3×10⁸ tenants), printed side by side with the per-tenant attacker-exposure win of 1.8M/yr (Figure 10) — at the 0.5%/yr base rate the counter-term (~1.5M/yr) is **the same order as the entire security win in the favorable region (1.8M/yr)**.",
    "P7 NNH key-loss")

rep("""**Figure 4.** The cost of manufactured history is time, not money (Technical Appendix, Sim-Battery A, Study 3). Left: Sybil cost per 10 units of standing vs. provider-attestation multiplier m — without attestation, $1.01 buys 10 units (the "costly to fake" claim is false in money); attestation multiplies cost linearly but remains a weak deterrent at m ≤ 10. Right: the wall-clock time floor — at maximum plausible attested validation rates of 0.5/1/2/5 events/day, manufacturing 10 units takes 5.5/2.8/1.4/0.6 years minimum; block rollups cut the honest user's lifetime anchoring cost 10⁴× ($1.005 → $0.0001) without touching the time floor. Caveat carried in-paper: parallel-provider collusion divides the floor.

*Figure 4: Sybil cost and the wall-clock defense (deposited figure: fig5_sybil.png, [to be deposited: OSF DOI pending])*""",
    """**Figure 4.** The cost of manufactured history is time, not money — and the honest user's cost is decoupled from both (Technical Appendix, Sim-Battery A, Study 3; whitepaper battery W5). The Sybil-side numbers, carried in §1.4: without provider attestation $1.01 buys 10 units of standing (the "costly to fake" claim is false in money); attestation multiplies cost linearly in the multiplier m but is a weak deterrent at m ≤ 10; the real defense is the wall-clock time floor — at maximum plausible attested validation rates of 0.5/1/2/5 events/day, manufacturing 10 units takes 5.5/2.8/1.4/0.6 years minimum — with the parallel-provider-collusion caveat carried in-paper. The rendered panels price the honest side: (a) anchoring cost per unit of standing vs. events per score (10³–10⁵), unrolled (~$0.001/event) vs. rolled (K = 10⁴ events/anchor), against the incumbent per-pull band ($50–$110+): the lifetime ~1,005-event history anchors for $1.005 unrolled and $0.0001 rolled — a 10⁴× discount that does not touch the Sybil time floor; (b) cumulative cost over repeated verification queries — the incumbent re-purchases identity at every query while the anchored identity's reads are local (≈$0).

*Figure 4: Sybil cost, the wall-clock defense, and honest-side cost accounting (whitepaper battery figure figW5; [to be deposited: OSF DOI pending])*""",
    "F4 caption")

rep("*Figure 5: Leakage-graded coherence surface (deposited figure: figB1_R_surface.png, [to be deposited: OSF DOI pending])*",
    "*Figure 5: Leakage-graded coherence surface (whitepaper battery re-render figW7 of figB1_R_surface.png; [to be deposited: OSF DOI pending])*",
    "F5 line")

FIG_ADD = """
**Figure 6.** Estimator validation on synthetic ground truth (whitepaper battery W1; §3.4). 300 synthetic users, true λ ~ U[0.05, 0.95], mixed-sign ε̃ streams (12–15% negative, heavier-tailed betrayals), Poisson cadence 0.3–3.0 events/day over 365 days (median 569 events/user, range 112–1100), heavy-tailed Student-t observation noise, and a deliberately misspecified Kalman/EM estimator. (a) True vs. recovered λ̂ with the ±0.15 certified band; (b) recovery-error histogram against the certified tolerance 0.15 and the printed 0.024 — re-run |λ̂ − λ|: mean 0.0074, p95 0.0215, max 0.0343; planted λ = 0 negative control max|λ̂| = 0.0092; ultra-thin streams (60–110 events) max error 0.0737; (c) example latent-trajectory recovery (single-stream scope; median r = 1.000 — see the §3.4 scope note).

*Figure 6: Estimator validation (whitepaper battery figure figW1)*

**Figure 7.** Base-rate dependence of predictive value (Sim W7 re-run; §1.5). Same instrument (sensitivity 0.90, specificity 0.71), 16× PPV collapse purely from the base rate. (a) PPV vs. prevalence: 0.47 at 22% prevalence falling to 0.03 at 1% — analytic values and Monte-Carlo crosses (2M files, seed 42) coincide with the printed points. (b) PPV vs. prevalence at sensitivity 0.90 across specificities: specificity, not sensitivity, dominates PPV at low prevalence.

*Figure 7: PPV vs. base rate (whitepaper battery figure figW2)*

**Figure 8.** The cold-start trap and the seeded-floor escape (Sim-Battery A, Study 1 re-run; §4.7 channel 4). (a) Trust-state trajectories S(t): with zero organic floor the new user never converges (the trap); at 0.01/day the state stabilizes at day 563; at 5/day, day 24; and a seeded score-independent floor of 2 events/day for 30 days escapes at day 72 — a 7.8× acceleration over the organic-only 0.01/day clock. (b) Time to first decisionable score vs. organic floor (median of 5 seeds), printed points overlaid; days carry a ±1 threshold-crossing convention.

*Figure 8: Cold-start trajectories (whitepaper battery figure figW3)*

**Figure 9.** Adoption compounding with densification feedback (whitepaper battery W4; §4.5). Adoption ODE with densification coupling κ feeding back through the cold-start clock of Figure 8. (a) Adopted fraction after 10 years over (organic floor × κ): the stall region (floor ≲ 0.01/day **and** κ ≲ 0.5; adopted fraction < 0.2), the compounding region (floor ≥ ~0.1/day, or κ ≥ ~2, or strong densification alone; ≥ 0.8), and the exact trap only at (floor, κ) = (0, 0). (b) Representative trajectories: trap, stall, partial, compound, and the densification-only arm — κ = 5 with zero organic floor bootstraps off the 1% initial cohort to ~95% by year 10, the modeling-choice caveat carried in §4.5.

*Figure 9: Adoption phase diagram (whitepaper battery figure figW4)*

**Figure 10.** Number-needed-to-harm accounting (whitepaper battery W6; §4.7). (a) Fee totals (log scale): fractions of a cent per lifetime — $1.005 unrolled, $0.0001 rolled for a full ~1,005-event history — against the incumbent's $50–$110+ per pull (re-paid at every query) and $510–$725 per closed loan. (b) Records per year: centralized expected exposure 15M/yr (p_org = 0.05, 3×10⁸ tenants), per-tenant attacker-exposed 1.8M/yr (8.3× reduction), and the key/guardian-loss counter-term 0.3 / 1.5 / 3.0M/yr at p_key = 0.001 / 0.005 / 0.01 — the security win and the availability offset printed side by side.

*Figure 10: NNH — the win and the counter-term (whitepaper battery figure figW6)*

## References"""
assert md.count("## References") == 1
md = md.replace("## References", FIG_ADD.strip())
print("patch ok: Figures 6-10 appended")

# ================= footnotes (patch side-notes) ============================
FOOTNOTES = {
 'TRAJ': ("Scope note on the trajectory statistic: the 300-user re-run exercises the single-stream (financial) "
          "state-space estimator alone and recovers latent trajectories at median r = 1.000 (p5 = 0.999, min 0.990); "
          "the printed 0.879 comes from the full dual-layer (financial + physiological) pipeline with its loading "
          "matrix. The scopes differ; both pass the pre-registered 0.7 threshold, and the load-bearing λ̂ tolerance "
          "replicates (p95 0.0215 vs. printed 0.024)."),
 'COLD': ("A seed-42 re-run of the cold-start engine reproduces the full floor grid as days 563 / 144 / 140 / 120 / "
          "72 / 24 for organic floors 0.01 / 0.05 / 0.1 / 0.5 / 1 / 5 events/day, versus the printed 562 / 143 / 139 / "
          "119 / 71 / 23 — a ±1-day first-crossing-vs.-stabilization convention; no claim is affected."),
}

# ================= numbered display equations ==============================
EQ_EPS = ("\n\\begin{equation}\n\\varepsilon_t := V_t - E_t, \\qquad "
          "\\tilde{\\varepsilon} = \\frac{V - E}{s_d}\n\\label{eq:epsilon}\n\\end{equation}\n")
EQ_MAIN = ("\n\\begin{align}\n\\Delta S &= \\lambda\\,(V - E) \\label{eq:master}\\\\\n"
           "\\mathrm{EU}(a \\mid T) &= \\sum_o \\tilde{P}(o \\mid a, T)\\,U(o) \\label{eq:eu}\\\\\n"
           "\\tilde{P}(o \\mid a, T) &\\propto P(o \\mid a)\\,"
           "\\exp\\!\\big(\\gamma\\,\\iota(T)\\,\\hat{u}(o)\\big) \\label{eq:tilt}\\\\\n"
           "\\iota(T) &= \\tanh(w\\,\\tilde{T}) \\in (-1,1) \\label{eq:iota}\n\\end{align}\n")
EQ_BREAKEVEN = ("\n\\begin{equation}\np_{\\mathrm{device}} + p_{\\mathrm{commonmode}} < p_{\\mathrm{org}}\n"
                "\\label{eq:breakeven}\n\\end{equation}\n")
EQ_LEAK = ("\n\\begin{equation}\nK_{\\mathrm{eff}} = K(1-\\ell), \\qquad \\sigma_{\\eta} = \\pi\\ell/2\n"
           "\\label{eq:leakage}\n\\end{equation}\n")

lines = md.split('\n')
out_lines = []
for ln in lines:
    out_lines.append(ln)
    if ln.startswith('FreshCredit consumes The Fresh Protocol unchanged'):
        # §3 architecture paragraph -> collected equations after it
        out_lines.append('\x10EQ_MAIN\x11')
    elif ln.startswith('Two properties of this architecture are established'):
        out_lines.append('\x10EQ_BREAKEVEN\x11')
    elif ln.startswith('- **Simulation evidence exists for the protocol layer'):
        # leakage equation at the end of the bullet
        out_lines[-1] = ln + '\n\x10EQ_LEAK_INLINE\x11'
md = '\n'.join(out_lines)
# eq:epsilon goes with the epistemic paragraph (handled in front matter assembly)
print("equation sentinels placed")

# ================= Unicode math / symbol replacement =======================
# generated LaTeX is wrapped in \x01...\x02 so later escaping skips it.
def prot(s): return '\x01' + s + '\x02'

TOKENS = [
    # --- multi-char formulas, longest first ---
    ('EU(a | T) = Σ_o P̃(o|a, T)·U(o)',
     r'$\mathrm{EU}(a \mid T) = \sum_o \tilde{P}(o \mid a, T)\,U(o)$'),
    ('P̃(o|a,T) ∝ P(o|a)·exp(γ·ι(T)·û(o))',
     r'$\tilde{P}(o \mid a, T) \propto P(o \mid a)\,\exp\!\big(\gamma\,\iota(T)\,\hat{u}(o)\big)$'),
    ('ι(T) = tanh(w·T̃) ∈ (−1, 1)',
     r'$\iota(T) = \tanh(w\,\tilde{T}) \in (-1, 1)$'),
    ('ΔS = λ(V − E)', r'$\Delta S = \lambda\,(V - E)$'),
    ('ε_t := V_t − E_t', r'$\varepsilon_t := V_t - E_t$'),
    ('ε̃ = (V − E)/s_fin', r'$\tilde{\varepsilon} = (V - E)/s_{\mathrm{fin}}$'),
    ('ε̃ = (V − E)/s_d', r'$\tilde{\varepsilon} = (V - E)/s_d$'),
    ('p_device + p_commonmode < p_org',
     r'$p_{\mathrm{device}} + p_{\mathrm{commonmode}} < p_{\mathrm{org}}$'),
    ('p_org ∈ {0.02–0.10}/yr', r'$p_{\mathrm{org}} \in \{0.02\text{--}0.10\}$/yr'),
    ('K_eff = K(1−ℓ)', r'$K_{\mathrm{eff}} = K(1-\ell)$'),
    ('σ_η = πℓ/2', r'$\sigma_{\eta} = \pi\ell/2$'),
    ('ψ → ψ_min < 0', r'$\psi \rightarrow \psi_{\min} < 0$'),
    ('ψ = −0.05μ', r'$\psi = -0.05\mu$'),
    ('μ_λ = 0.61', r'$\mu_{\lambda} = 0.61$'),
    ('1/√N', r'$1/\sqrt{N}$'),
    ('10⁴×', r'$10^{4}\times$'),
    ('3×10⁸', r'$3\times 10^{8}$'),
    ('10³–10⁵', r'$10^{3}$--$10^{5}$'),
    ('K = 10⁴', r'$K = 10^{4}$'),
    ('λ ~ U[0.05, 0.95]', r'$\lambda \sim \mathrm{U}[0.05, 0.95]$'),
    ('(floor, κ) = (0, 0)', r'$(\mathrm{floor},\, \kappa) = (0, 0)$'),
    ('H₀', r'$\mathrm{H}_0$'),
    ('H₁', r'$\mathrm{H}_1$'),
    ('ℓ*', r'$\ell^{*}$'),
    # --- combining-accent tokens (base + U+0302 / U+0303) ---
    ('λ̂_u', r'$\hat{\lambda}_u$'),
    ('T̂_t', r'$\hat{T}_t$'),
    ('T̂/λ̂', r'$\hat{T}/\hat{\lambda}$'),
    ('λ̂', r'$\hat{\lambda}$'),
    ('T̂', r'$\hat{T}$'),
    ('P̃', r'$\tilde{P}$'),
    ('T̃', r'$\tilde{T}$'),
    ('ε̃', r'$\tilde{\varepsilon}$'),
    ('û', r'$\hat{u}$'),
    # --- identifier tokens with subscripts ---
    ('p_commonmode', r'$p_{\mathrm{commonmode}}$'),
    ('p_device', r'$p_{\mathrm{device}}$'),
    ('p_org', r'$p_{\mathrm{org}}$'),
    ('p_key', r'$p_{\mathrm{key}}$'),
    ('K_eff', r'$K_{\mathrm{eff}}$'),
    ('σ_η', r'$\sigma_{\eta}$'),
    ('ψ_min', r'$\psi_{\min}$'),
    ('s_fin', r'$s_{\mathrm{fin}}$'),
    ('s_d', r'$s_d$'),
    ('w_u', r'$w_u$'),
    ('ε_t', r'$\varepsilon_t$'),
    ('V_t', r'$V_t$'),
    ('E_t', r'$E_t$'),
    ('Σ_o', r'$\sum_o$'),
    ('βδ', r'$\beta\delta$'),
    # --- single symbols ---
    ('Δ', r'$\Delta$'),
    ('λ', r'$\lambda$'),
    ('δ', r'$\delta$'),
    ('γ', r'$\gamma$'),
    ('ι', r'$\iota$'),
    ('τ', r'$\tau$'),
    ('ψ', r'$\psi$'),
    ('μ', r'$\mu$'),
    ('π', r'$\pi$'),
    ('σ', r'$\sigma$'),
    ('η', r'$\eta$'),
    ('ε', r'$\varepsilon$'),
    ('κ', r'$\kappa$'),
    ('β', r'$\beta$'),
    ('ℓ', r'$\ell$'),
    # --- relations / operators ---
    ('≲', r'$\lesssim$'),
    ('≳', r'$\gtrsim$'),
    ('≈', r'$\approx$'),
    ('≤', r'$\leq$'),
    ('≥', r'$\geq$'),
    ('∝', r'$\propto$'),
    ('∈', r'$\in$'),
    ('×', r'$\times$'),
    ('±', r'$\pm$'),
    ('√', r'$\surd$'),
    ('·', r'$\cdot$'),
    ('→', r'$\rightarrow$'),
    ('~', r'$\sim$'),
    # --- typographic ---
    ('§', r'\S~'),
    ('—', '---'),
    ('–', '--'),
    ('…', r'\ldots{}'),
    ('ł', r'\l{}'),
    ('ö', r'\"o'),
    ('á', r"\'a"),
    ('−', '-'),
]

def symbol_pass(s):
    for old, new in TOKENS:
        if '\\' in new or '$' in new:
            chunks = re.split('(\x01[^\x02]*\x02)', s)
            s = ''.join(c if c.startswith('\x01') else c.replace(old, prot(new))
                        for c in chunks)
        else:
            s = s.replace(old, new)
    return s

md = symbol_pass(md)

# ================== per-paragraph text conversion ==========================
SPECIALS = [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'),
            ('_', r'\_'), ('{', r'\{'), ('}', r'\}')]

def convert_text(s):
    """escape specials outside protected chunks, markdown emphasis, < >."""
    # footnote sentinels \x03KEY\x04 -> \footnote{...}
    def fn_sub(m):
        inner = convert_text(symbol_pass(FOOTNOTES[m.group(1)]))
        return prot(r'\footnote{' + inner + '}')
    s = re.sub('\x03(\\w+)\x04', fn_sub, s)
    # split on protected chunks
    parts = re.split('(\x01[^\x02]*\x02)', s)
    out = []
    for p in parts:
        if p.startswith('\x01'):
            out.append(p)
            continue
        for a, b in SPECIALS:
            p = p.replace(a, b)
        p = p.replace(' < ', prot(' $<$ ')).replace(' > ', prot(' $>$ '))
        p = re.sub(r'(^|\s)>', lambda m: m.group(1) + prot('$>$'), p)   # >14M etc
        p = re.sub(r'(^|\s)<', lambda m: m.group(1) + prot('$<$'), p)
        out.append(p)
    s = ''.join(out)
    # markdown emphasis (avoid protected chunks)
    s = re.sub('\x01([^\x02]*)\x02', lambda m: '\x05' + str(len(m.group(0))) + '\x06' + m.group(1) + '\x07',
               s)
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'\*([^*\x05]+?)\*', r'\\emph{\1}', s)
    # restore protected chunks
    s = re.sub('\x05' + r'(\d+)' + '\x06(.*?)\x07', lambda m: m.group(2), s, flags=re.S)
    return s

# ====================== structural conversion ==============================
FIG_FILES = {
    4: 'figures/figW5_cost_accounting.png',
    5: 'figures/figW7_R_surface.png',
    6: 'figures/figW1_estimator_validation.png',
    7: 'figures/figW2_ppv_baserate.png',
    8: 'figures/figW3_coldstart.png',
    9: 'figures/figW4_adoption_compounding.png',
    10: 'figures/figW6_nnh_harm.png',
}
print("engine loaded")

# ========================= structural parser ===============================
EQ_BLOCKS = {'EQ_MAIN': EQ_MAIN, 'EQ_BREAKEVEN': EQ_BREAKEVEN, 'EQ_LEAK_INLINE': EQ_LEAK}

def flush_para(buf, out):
    if buf:
        out.append(convert_text(' '.join(x.strip() for x in buf)) + '\n')
        buf.clear()

def convert_table(tbl_lines, kind):
    """kind 'vendor' (2 col) or 'claims' (5 col) -> table* float, booktabs."""
    rows = []
    for ln in tbl_lines:
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        rows.append(cells)
    header, rows = rows[0], rows[2:]  # skip separator row
    ncol = len(header)
    if ncol == 2:
        cols = r'p{0.26\textwidth} p{0.67\textwidth}'
        caption = ('Deployed cash-flow underwriting outcomes: vendor-published case studies, single deployments '
                   'without control groups (see text for caveats).')
        label = 'tab:vendor'
    else:
        cols = r'p{0.026\textwidth} p{0.21\textwidth} p{0.098\textwidth} p{0.379\textwidth} p{0.19\textwidth}'
        caption = ('Claims-to-evidence map: the load-bearing claims of this whitepaper with epistemic label, '
                   'support, and status.')
        label = 'tab:claims'
    def one_table(hdr, rws, cap, lab):
        o = [r'\begin{table*}[t!]', r'\centering', r'\footnotesize',
             r'\caption{%s}\label{%s}' % (cap, lab),
             r'\begin{tabular}{@{}%s@{}}' % cols, r'\toprule']
        o.append(' & '.join(convert_text(c) for c in hdr) + r' \\')
        o.append(r'\midrule')
        for r in rws:
            cells = [convert_text(c) for c in r]
            if len(cells) == 5:
                cells[2] = r'\hspace{0pt}' + cells[2]  # allow label hyphenation
            o.append(' & '.join(cells) + r' \\')
        o += [r'\bottomrule', r'\end{tabular}', r'\end{table*}', '']
        return '\n'.join(o)
    if ncol != 2 and len(rows) > 8:   # claims map: split W1-W6 / W7-W12
        half = 6
        return (one_table(header, rows[:half], caption + ' (W1--W6).', label) + '\n' +
                one_table(header, rows[half:], caption + ' (W7--W12, continued).', label + '-b'))
    return one_table(header, rows, caption, label)

def convert_figures_section(block_lines):
    """block_lines: the paragraphs of the '## Figures' section."""
    figs = {}
    cur = None
    for ln in block_lines:
        m = re.match(r'\*\*Figure (\d+)\.\*\*\s*(.*)', ln)
        if m:
            cur = int(m.group(1)); figs[cur] = {'caption': m.group(2), 'pointer': ''}
        elif cur and re.match(r'\*Figure \d+:', ln):
            figs[cur]['pointer'] = ln.strip().strip('*')
        elif cur and ln.strip():
            figs[cur]['caption'] += ' ' + ln.strip()
    o = [r'\section*{Figures}', '']
    o.append(r'\setcounter{figure}{3}% next caption is Figure 4')
    for n in sorted(figs):
        cap = convert_text(figs[n]['caption'])
        ptr = convert_text(figs[n]['pointer'])
        if n in FIG_FILES:
            o.append(r'\begin{figure*}[t!]')
            o.append(r'\centering')
            o.append(r'\includegraphics[width=\textwidth]{%s}' % FIG_FILES[n])
            o.append(r'\caption{%s \emph{%s}}' % (cap, ptr))
            o.append(r'\end{figure*}')
            o.append('')
        else:
            o.append(r'\noindent\textbf{Figure %d.} %s' % (n, cap))
            o.append('')
            o.append(r'\emph{%s}' % ptr)
            o.append('')
    o.append(r'\clearpage')
    return '\n'.join(o)

def parse_body(body):
    lines = body.split('\n')
    out, buf = [], []
    i = 0
    while i < len(lines):
        ln = lines[i]
        stripped = ln.strip()
        # equation sentinel blocks
        m = re.match('\x10(\\w+)\x11', stripped)
        if m:
            flush_para(buf, out)
            out.append(EQ_BLOCKS[m.group(1)])
            i += 1; continue
        if not stripped:
            flush_para(buf, out); i += 1; continue
        if stripped.startswith('### '):
            flush_para(buf, out)
            out.append(r'\subsection*{' + convert_text(stripped[4:]) + '}\n')
            i += 1; continue
        if stripped.startswith('## '):
            flush_para(buf, out)
            title = stripped[3:]
            if title == 'Figures':
                # collect until '## References'
                j = i + 1; block = []
                while j < len(lines) and not lines[j].startswith('## References'):
                    block.append(lines[j]); j += 1
                out.append(convert_figures_section([b for b in block if b.strip()]))
                i = j; continue
            if title == 'References':
                break   # reference list replaced by \bibliography; tail already extracted
            out.append(r'\section*{' + convert_text(title) + '}\n')
            i += 1; continue
        if stripped.startswith('|'):
            flush_para(buf, out)
            j = i
            while j < len(lines) and lines[j].strip().startswith('|'):
                j += 1
            ncol = lines[i].count('|') - 1
            out.append(convert_table(lines[i:j], 'vendor' if ncol == 2 else 'claims'))
            i = j; continue
        if stripped.startswith('- '):
            flush_para(buf, out)
            out.append(r'\begin{itemize}')
            while i < len(lines) and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:]
                # an item may carry an equation sentinel on a following line
                eqs = []
                while i + 1 < len(lines) and re.match('\x10(\\w+)\x11', lines[i+1].strip()):
                    eqs.append(EQ_BLOCKS[re.match('\x10(\\w+)\x11', lines[i+1].strip()).group(1)])
                    i += 1
                out.append(r'\item ' + convert_text(item))
                out.extend(eqs)
                i += 1
            out.append(r'\end{itemize}' + '\n')
            continue
        if re.match(r'^\d+\.\s', stripped):
            flush_para(buf, out)
            out.append(r'\begin{enumerate}')
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                item = re.sub(r'^\d+\.\s', '', lines[i].strip())
                out.append(r'\item ' + convert_text(item))
                i += 1
            out.append(r'\end{enumerate}' + '\n')
            continue
        if stripped.startswith('> '):
            flush_para(buf, out)
            q = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                q.append(lines[i].strip()[2:]); i += 1
            out.append('\\begin{quote}\n' + convert_text(' '.join(q)) + '\n\\end{quote}\n')
            continue
        if stripped == '---':
            flush_para(buf, out); i += 1; continue
        buf.append(ln); i += 1
    flush_para(buf, out)
    return '\n'.join(out)

print("parser loaded")

# ============================ assembly =====================================
md_lines = md.split('\n')
epistemic = None; abstract = None; body_start = None
for i, ln in enumerate(md_lines):
    if ln.startswith('**Epistemic labels'):
        epistemic = ln
    if ln.strip() == '## Abstract':
        abstract = md_lines[i + 2]
    if ln.startswith('## 0. Hypotheses'):
        body_start = i
assert epistemic and abstract and body_start
body = '\n'.join(md_lines[body_start:])

TAILNOTE = None
def parse_body_wrap(b):
    global TAILNOTE
    m = re.search(r'^\*Companion documents:.*$', b, flags=re.M)
    if m:
        TAILNOTE = m.group(0)
        b = b[:m.start()]
    return parse_body(b)

body_tex = parse_body_wrap(body)
epistemic_tex = convert_text(epistemic)
abstract_tex = convert_text(abstract)
tail_tex = convert_text(TAILNOTE) if TAILNOTE else ''

PREAMBLE = r"""\documentclass[11pt,twocolumn]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,margin=0.95in]{geometry}
\usepackage{amsmath,amsthm,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[authoryear,round]{natbib}
\usepackage[font=small,labelfont=bf]{caption}
\usepackage{microtype}
\usepackage[hidelinks,breaklinks=true]{hyperref}

\title{FreshCredit: Credit as Trust Quantified\\[4pt]
  \large\itshape A whitepaper on the financial application of The Fresh Protocol}
\author{Devon Shigaki\\
  \normalsize The FreshCredit Lab --- Independent Research\\
  \normalsize Correspondence \& live benchmarks: \texttt{freshcredit.xyz} $\cdot$
  \texttt{freshcredit.xyz/cost}}
\date{September 2026}

\begin{document}
\makeatletter
\twocolumn[\begin{@twocolumnfalse}
\maketitle
\begin{abstract}
ABSTRACT_HERE
\end{abstract}
\vspace{1.2em}
\end{@twocolumnfalse}]
\makeatother

"""

tex = PREAMBLE.replace('ABSTRACT_HERE', abstract_tex)
tex += epistemic_tex + '\n' + EQ_EPS + '\n'
tex += body_tex + '\n'
tex += "\\bibliographystyle{plainnat}\n\\nocite{*}\n\\bibliography{whitepaper}\n\n"
if tail_tex:
    tex += "\\vspace{1em}\\begin{footnotesize}\n" + tail_tex + "\n\\end{footnotesize}\n"
tex += "\\end{document}\n"
# safety: no stray sentinels
for bad in ['\x01','\x02','\x03','\x04','\x05','\x06','\x07','\x10','\x11']:
    assert bad not in tex, f"stray sentinel {bad!r} in output"
open(OUT_TEX, 'w').write(tex)
print("wrote", OUT_TEX, len(tex), "chars")

# ============================ whitepaper.bib ===============================
def bib_escape(s):
    for a, b in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_')]:
        s = s.replace(a, b)
    s = symbol_pass(s)
    return s.replace('\x01', '').replace('\x02', '')

BIB = [
 # key, type, author, year, title, extra fields
 ('battiston2012','article','Battiston, Stefano and Puliga, Michelangelo and Kaushik, Rahul and Tasca, Paolo and Caldarelli, Guido','2012',
  'DebtRank: Too central to fail? Financial networks, the FED and systemic risk',
  {'journal':'Scientific Reports','volume':'2','pages':'541',
   'note':'Interbank balance-sheet exposure cascade measure; cited to scope the withdrawal of its application to data custody in TFP Sim P6.'}),
 ('beinhocker2006','book','Beinhocker, Eric D.','2006','The Origin of Wealth',{'publisher':'Harvard Business School Press'}),
 ('bharadwaj2021','article','Bharadwaj, Prashant and Jack, William and Suri, Tavneet','2021',
  'Fintech and household resilience to shocks: Evidence from digital loans in Kenya',
  {'journal':'Journal of Development Economics','volume':'152','pages':'102697',
   'note':'M-Shwari fuzzy RDD: access reduced cutting essential expenses after shocks by ~6.3pp; small-sample caveat.'}),
 ('bialowolski2023','misc','Białowolski, Piotr','2023','Household financial behavior and well-being research',
  {'howpublished':'Harvard Kennedy School'}),
 ('bjorkegren2022','misc','Björkegren, Daniel and Blumenstock, Joshua E. and Folajimi-Senjobi, Olubukola and Mauro, Jonathan and Nair, Suraj R.','2022',
  'Instant loans can lift subjective well-being: A randomized evaluation of digital credit in Nigeria',
  {'howpublished':'arXiv:2202.13540 / CEGA Working Paper WP-198'}),
 ('bjs2023','misc','{Bureau of Justice Statistics}','2023','Victims of Identity Theft, 2021',
  {'howpublished':'U.S. Department of Justice'}),
 ('buterin2021','misc','Buterin, Vitalik and others','2021','ERC-4337: Account abstraction without Ethereum protocol changes (deployed March 2023); Ethereum Pectra upgrade (EIP-7702, 2025)',
  {'note':'Passkey signers per the W3C WebAuthn standard.'}),
 ('campbell1979','article','Campbell, Donald T.','1979','Assessing the impact of planned social change',
  {'journal':'Evaluation and Program Planning','volume':'2','number':'1','pages':'67--90'}),
 ('chainalysis2017','misc','{Chainalysis}','2017','Estimate of 2.78--3.79M BTC (~17--23\\% of supply) stranded in wallets with inaccessible keys',
  {'howpublished':'As reported by Fortune, November 2017; corroborated by Unchained Capital (2018) via different methodology',
   'note':'Methodology unpublished; cited as order-of-magnitude.'}),
 ('chla2024','misc','{Community Home Lenders of America}','2024','Update to Rapidly-Rising Credit Scoring Costs',
  {'note':'Credit costs per closed loan: ~\\$50 in 2022 $\\rightarrow$ \\$100+ in late 2023 $\\rightarrow$ \\$150--\\$250 in 2024; including sunk costs of unclosed applications, total credit costs per closed loan \\$510--\\$725+.'}),
 ('cakipa2021','misc','{Competition Authority of Kenya} and {IPA}','2021','Digital Credit Market Inquiry',
  {'note':'Provider-level late/default rates 19.4\\%/7.2\\% and 30.7\\%/1.5\\%; median effective APRs 86--122\\%.'}),
 ('cfpb2015','techreport','{Consumer Financial Protection Bureau}','2015','Data Point: Credit Invisibles',
  {'note':'Original 26M/19M estimates --- superseded; see the 2025 technical correction.'}),
 ('cfpb2025correction','techreport','{Consumer Financial Protection Bureau}','2025','Technical Correction and Update to the Credit Invisibles Estimate',
  {'note':'Corrected 2010: 13.5M invisible (5.8\\%), 29.7M unscored (12.7\\%); 2020: 7.0M invisible (2.7\\%), ~25.3M unscored (9.8\\%); scored share 81.6\\% $\\rightarrow$ 87.5\\%.'}),
 ('cfpb2025response','techreport','{Consumer Financial Protection Bureau}','2025','Consumer Response Annual Report: January 1--December 31, 2024',
  {'note':'~3,187,900 total complaints; ~2,703,400 credit/consumer reporting (85\\%); >2,514,000 naming the NCRAs (~93\\%); incorrect-information issue +247\\% vs. prior-two-year monthly average; ~3\\% of credit-reporting complaints flagged as potentially unauthorized third-party submissions.'}),
 ('cfpb2026response','techreport','{Consumer Financial Protection Bureau}','2026','Consumer Response Annual Report: January 1--December 31, 2025',
  {'note':'6,635,400 total complaints, roughly double 2024; credit/consumer reporting 5,806,800 (88\\%); 5,102,800 naming the NCRAs.'}),
 ('cfpb2025fcra','techreport','{Consumer Financial Protection Bureau}','2025','FCRA \\S 611(e) Annual Report',
  {'note':'Jan 2024--Jun 2025: >5.6M complaints, ~4.786M credit/consumer reporting, ~3.9M against the three NCRAs; NCRA volume ~+3,000\\% since Jan 2020; ~90\\% of consumers reported a prior dispute, confirmed by Equifax in only ~37\\% and TransUnion ~30\\% of cases.'}),
 ('cfpb2026ccd','misc','{Consumer Financial Protection Bureau}','2026','Consumer Complaint Database API (queried 2026)',
  {'note':'Base: published complaints, product ``Credit reporting or other personal consumer reports,\'\' received 2024-01-01 to 2024-12-31, N = 2,365,586: ``incorrect information on your report\'\' 1,175,009 (49.7\\%); ``problem with a company\'s investigation into an existing problem\'\' 455,637 (19.3\\%); together 69.0\\% of the database population.'}),
 ('cfpb2024rfi','misc','{Consumer Financial Protection Bureau}','2024','Request for information on fees imposed in residential mortgage transactions',
  {'note':'Lender-reported tri-merge per-pull increases; ~\\$15/\\$30 single/joint $\\rightarrow$ \\$50--\\$110+ in two years.'}),
 ('cfpb2022circular','misc','{Consumer Financial Protection Bureau}','2022','Circular 2022-03: Adverse action notification requirements in connection with credit decisions based on complex algorithms',
  {'note':'Specific reasons required; model opacity not a defense; withdrawn May 12, 2025 --- underlying ECOA/Reg B duty unchanged.'}),
 ('interagency2019','misc','{Consumer Financial Protection Bureau} and {Federal Reserve} and {FDIC} and {NCUA} and {OCC}','2019',
  'Interagency Statement on the Use of Alternative Data in Credit Underwriting',{'note':'December 3, 2019; OCC Bulletin 2019-62.'}),
 ('jointstatement2023','misc','{Consumer Financial Protection Bureau} and {DOJ Civil Rights Division} and {EEOC} and {FTC}','2023',
  'Joint Statement on Enforcement Efforts Against Discrimination and Bias in Automated Systems',{'note':'April 25, 2023.'}),
 ('cfpbvpgx2024','misc','{Consumer Financial Protection Bureau v. PGX Holdings/Progrexion (Lexington Law; CreditRepair.com)}','2024',
  'District-court ruling and victims\'-relief distribution',
  {'note':'March 2023 ruling: illegal advance fees (Telemarketing Sales Rule), deceptive marketing (CFPA); ~\\$2.7B judgment and 10-year telemarketing ban; December 2024: \\$1.8B distributed to ~4.3M harmed consumers --- the CFPB\'s largest victims\'-relief distribution.'}),
 ('consumerreports2024','misc','{Consumer Reports} and {WorkMoney}','2024','Credit Checkup: Improving the Accuracy of Credit Reports',
  {'note':'Volunteer sample, 4,300+ participants, not nationally representative; 44\\% of successful checkers found $\\geq$ 1 error; 27\\% found account/debt errors affecting creditworthiness; 25\\% of sign-ups unable to access their reports.'}),
 ('currie2015','article','Currie, Janet and Tekin, Erdal','2015','Is there a link between foreclosure and health?',
  {'journal':'American Economic Journal: Economic Policy','volume':'7','number':'1','pages':'63--94',
   'note':'Zip-level foreclosure spikes $\\rightarrow$ significant increases in urgent unscheduled hospitalizations, incl. preventable and mental-health conditions; quasi-causal.'}),
 ('dalio2013','misc','Dalio, Ray','2013','How the Economic Machine Works',
  {'note':'Transactions as the economic primitive; credit created against trust, becoming simultaneous asset and liability; one participant\'s spending as another\'s income; short- and long-term debt cycles of ~5--8 and ~75--100 years.'}),
 ('dobbie2015','article','Dobbie, Will and Song, Jae','2015','Debt relief and debtor outcomes: Measuring the effects of consumer bankruptcy protection',
  {'journal':'American Economic Review','volume':'105','number':'12','pages':'3852--3881',
   'note':'Judge-leniency IV: Chapter 13 protection increases earnings and decreases mortality.'}),
 ('experianboost2024','misc','{Experian}','2022','Experian Boost results',
  {'howpublished':'Business Wire, Sept 7, 2022; April 2024 release; US News, June 2023',
   'note':'Average +13 points FICO Score 8 among users with an increase; ~+19--20 thin-file, ~+17 subprime; >88M cumulative points; ~60--66\\% of completing users saw an increase; >14M consumers connected; >10,000 previously unscorable consumers per month became scoreable. Vendor-reported.'}),
 ('fed2019sif','misc','{Federal Reserve FedPayments Improvement}','2019','Synthetic Identity Payments Fraud white-paper series (Defining / Detecting / Mitigating) and 2022 SIF Mitigation Toolkit',
  {'note':'Identities seasoned months--years before bust-out; industry estimates of multi-billion-dollar unsecured-credit losses. U.S. SSA eCBSV (electronic Consent Based SSN Verification) as the deployed authoritative-issuer cross-check.'}),
 ('ftc20132015','misc','{Federal Trade Commission}','2013','Credit report accuracy study and follow-up (Section 319, FACT Act)',
  {'note':'2013: 26\\% potentially material error; 21\\% modified after dispute; 13\\% score change; 5\\% moved to a worse credit-risk tier. 2015 follow-up: 80\\% of disputants received some modification, 37\\% all requested; ~70\\% of unresolved disputants still believed the information inaccurate.'}),
 ('ftctradeline','misc','{Federal Trade Commission}','2020','Enforcement against tradeline-rental sellers under the Credit Repair Organizations Act',
  {'note':'Authorized-user slots marketed at \\$325--\\$4,000+ per tradeline; ``100--120 points in 2--6 weeks\'\' claims alleged unsubstantiated.'}),
 ('fico2016','misc','{FICO}','2015','FICO Score XD pilot results; UltraFICO launch projections',
  {'note':'NCTUE telecom/utility + LexisNexis public records; >50\\% of previously unscorable card applicants scoreable; >1/3 of newly scored $\\geq$ 620 --- vendor-reported, not independently audited. UltraFICO: ~15M potentially scoreable --- [UNVERIFIED vendor claims].'}),
 ('finreglab2019','techreport','{FinRegLab}','2019','The Use of Cash-Flow Data in Underwriting Credit: Empirical Research Findings',
  {'note':'Analysis by Charles River Associates; six lenders; cash-flow variables/scores predictive across heterogeneous populations incl. no-/low-score borrowers; no disparate impact detected among protected populations in study samples.'}),
 ('finreglab2025','techreport','{FinRegLab}','2025','Advancing the Credit Ecosystem: Machine Learning \\& Cash Flow Data in Consumer Underwriting; Sharpening the Focus',
  {'note':'ML + cash-flow model most predictive overall and across all subgroups; highest approval rates at most thresholds; expanded modeled access without increased modeled default risk. Also: 38,000+ small-business loans; gains largest for young, low-score-owned businesses.'}),
 ('ganong2023','article','Ganong, Peter and Noel, Pascal','2023','Why do borrowers default on mortgages?',
  {'journal':'Quarterly Journal of Economics','volume':'138','number':'2','pages':'1001--1065',
   'note':'Linked servicing + bank-account data, 3.2M borrowers: ~6\\% of underwater defaults purely strategic; ~70\\% cash-flow shocks only; 24\\% double-trigger.'}),
 ('gerardi2018','article','Gerardi, Kristopher and Herkenhoff, Kyle and Ohanian, Lee and Willen, Paul','2018',"Can't pay or won't pay? Unemployment, negative equity, and strategic default",
  {'journal':'Review of Financial Studies','volume':'31','number':'3','pages':'1098--1131'}),
 ('guiso2013','article','Guiso, Luigi and Sapienza, Paola and Zingales, Luigi','2013','The determinants of attitudes toward strategic default on mortgages',
  {'journal':'Journal of Finance','volume':'68','number':'4','pages':'1473--1515',
   'note':'82\\% view strategic default as morally wrong; attitudes/hypotheticals, not behavior; acquaintance-based estimates imply 65--75\\% of observed crisis-era defaults non-strategic.'}),
 ('holtlunstad2015','article','Holt-Lunstad, Julianne and Smith, Timothy B. and Baker, Mark and Harris, Tyler and Stephenson, David','2015',
  'Loneliness and social isolation as risk factors for mortality: A meta-analytic review',
  {'journal':'Perspectives on Psychological Science','volume':'10','number':'2','pages':'227--237',
   'note':'70 prospective studies; 3.4M participants; confounder-adjusted ORs: social isolation 1.29, loneliness 1.26, living alone 1.32 --- associational; reverse causation not excluded.'}),
 ('itrc2026','techreport','{Identity Theft Resource Center}','2026','2025 Annual Data Breach Report',
  {'note':'Record 3,322 U.S. compromises in 2025; 278,827,933 victim notices, -79\\% from 2024\'s restated 1,367,117,021 --- a mega-breach year in which six mega-breaches, four preventable with MFA/passkeys, accounted for ~84\\% of notices.'}),
 ('itrc2025','techreport','{Identity Theft Resource Center}','2025','2024 Annual Data Breach Report',
  {'note':'Originally released with 1,728,519,397 notices (+312\\% YoY); ITRC\'s database has since restated 2024 to 1,367,117,021 --- the figure used consistently in this document.'}),
 ('ic32026','techreport','{FBI Internet Crime Complaint Center}','2026','2025 Internet Crime Report',
  {'note':'1,008,597 complaints; \\$20.877 billion reported losses (+26\\% YoY); over-60 losses \\$7.7B. IC3 SIM-swap losses: \\$72.7M (2022) $\\rightarrow$ \\$26.0M (2024) $\\rightarrow$ \\$17.4M (2025); single-incident tail >\\$400M (FTX wallets, DOJ indictment unsealed Jan 2024).'}),
 ('israel2014','article','Israel, Salomon and Caspi, Avshalom and Belsky, Daniel W. and others','2014','Credit scores, cardiovascular disease risk, and human capital',
  {'journal':'PNAS','volume':'111','number':'48','pages':'17087--17092',
   'note':'Dunedin cohort, N = 1,037; human-capital factors explain ~45\\% of the credit-score--cardiovascular-risk association --- substantial third-factor confounding.'}),
 ('kahneman2011','book','Kahneman, Daniel','2011','Thinking, Fast and Slow',{'publisher':'Farrar, Straus and Giroux'}),
 ('kluender2021','article','Kluender, Raymond and Mahoney, Neale and Wong, Francis and Yin, Wesley','2021','Medical debt in the US, 2009--2020',
  {'journal':'JAMA','volume':'326','number':'3','pages':'250--256',
   'note':'17.8\\% of credit-report holders with medical debt in collections, June 2020; Medicaid expansion cut medical-debt flow 34pp vs. non-expansion, diff-in-diff.'}),
 ('lee2020','inproceedings','Lee, Kevin and Kaiser, Ben and Mayer, Jonathan and Narayanan, Arvind','2020','An empirical study of wireless carrier authentication for SIM swaps',
  {'booktitle':'IEEE S\\&P Workshops','note':'Princeton CITP; 39 of 50 unauthorized SIM-swap attempts succeeded across 5 major U.S. prepaid carriers.'}),
 ('lexisnexis2025','techreport','{LexisNexis Risk Solutions}','2025','True Cost of Fraud Study',{'note':'\\$5.75 per \\$1 of fraud losses.'}),
 ('loopring2024','misc','{Loopring}','2024','Smart Wallet ``Official Guardian\'\' compromise post-mortem',
  {'note':'June 9, 2024; ~\\$5M lost across ~58 users\' wallets via guardian-service 2FA compromise.'}),
 ('lovenheim2011','article','Lovenheim, Michael F.','2011','The effect of liquid housing wealth on college enrollment',
  {'journal':'Journal of Labor Economics','volume':'29','number':'4','pages':'741--771',
   'note':'+\\$10,000 liquid housing wealth $\\rightarrow$ ~0.7--0.9pp higher enrollment.'}),
 ('lovenheim2013','article','Lovenheim, Michael F. and Reynolds, C. Lockwood','2013','The effect of housing wealth on college choice',
  {'journal':'Journal of Human Resources','volume':'48','number':'1','pages':'1--35',
   'note':'+\\$10,000 housing wealth $\\rightarrow$ +2.0\\% flagship enrollment, +1.8\\% completion for low-income; plausibly exogenous variation.'}),
 ('mccambridge2012','article','McCambridge, Jim and Witton, John and Elbourne, Diana R.','2012','Systematic review of the Hawthorne effect',
  {'journal':'Journal of Clinical Epidemiology','volume':'65','number':'3'}),
 ('nclc2026','misc','{National Consumer Law Center}','2026','Comments on CFPB complaint-intake changes',
  {'note':'Reporting the CFPB\'s finding that ~3\\% of credit-reporting complaints were flagged as potentially submitted by unauthorized third parties.'}),
 ('occ2011','misc','{Office of the Comptroller of the Currency} and {Federal Reserve} and {FDIC}','2011','SR 11-7 / OCC 2011-12, Supervisory Guidance on Model Risk Management (FDIC FIL-22-2017)',
  {'note':'Status: OCC rescinded Bulletin 2011-12 via OCC 2026-13 (April 17, 2026); successor guidance to be tracked.'}),
 ('osg2023','misc','{Office of the U.S. Surgeon General}','2023','Our Epidemic of Loneliness and Isolation',{}),
 ('oliverwyman2022','techreport','{Oliver Wyman} and {Experian}','2022','Financial Inclusion and Access to Credit',
  {'note':'28M invisible; 21M unscorable; 96\\% scorable with expanded data --- pre-correction frame, superseded for market sizing by the CFPB 2025 technical correction; demographic detail retained.'}),
 ('openzeppelin2020','misc','{OpenZeppelin}','2020','Argent recovery vulnerability report (CVE-2020-15302)',
  {'note':'Zero-guardian recovery edge case; 329 wallets immediately at risk, fixed pre-exploitation.'}),
 ('owid2023','misc','{Our World in Data} and Roser, Max','2023','Extreme poverty: how far have we come, and how far do we still have to go?',
  {'note':'84\\% of world population --- 6.7B people --- live on less than \\$30/day, international-\\$, price-adjusted.'}),
 ('penney2016','article','Penney, Jonathon W.','2016','Chilling effects: Online surveillance and Wikipedia use',
  {'journal':'Berkeley Technology Law Journal','volume':'31','number':'1'}),
 ('plaid2024zillow','misc','{Plaid}','2024','Zillow Home Loans customer story',
  {'note':'Vendor-reported: 3.2$\\times$ more pre-approved loans with digitally verified assets; 29\\% faster pre-approvals; 511\\% increase in GSE reps-and-warranties-relief-eligible loans.'}),
 ('plaid2025rentapp','misc','{Plaid}','2025','Rent App customer story',
  {'note':'Vendor-reported: ~10-second approval decisions; delinquency ``dropping up to 50\\% month-over-month\'\' --- baseline not disclosed; ~90\\% third-party fraud reduction.'}),
 ('plaid2024livble','misc','{Plaid}','2024','Livble customer story',
  {'note':'Vendor-reported: ~3$\\times$ more tenants approved at equal default rates vs. FICO-680-only policy; ~25\\% fewer false positives.'}),
 ('plaidyougov2024','misc','{Plaid} and {YouGov}','2024','Fintech Effect consumer survey',
  {'note':'n = 2,077 U.S. adults; 74\\% comfortable sharing cash-flow data; only 3 in 10 believe credit scores accurately reflect financial health.'}),
 ('experianplaid2024','misc','{Experian} and {Plaid}','2024','Lender sentiment on open banking and alternative credit data',
  {'note':'88\\% increased confidence; 89\\% say open banking enhances credit decisions; 51\\% cite limited negative-payment-history visibility as top gap; 55\\% of denials attributed to low credit score.'}),
 ('polkadot2024','misc','{Polkadot} and {Distractive \\& Parity Technologies}','2024','The Spammening Report 2024',
  {'note':'Dec 4, 2024 community test on Kusama: 143,343 batch/one-to-many TPS peak on 23 of 100 cores; Nov 26, 2024 controlled test: 10,920 TPS ordinary P2P transfers on 15 cores; Polkadot 2.0 features live.'}),
 ('selffinancial2025','misc','{Self Financial}','2025','How Many Americans Are Hiding Debts?',
  {'note':'Survey, n = 1,078; 66.3\\% of indebted respondents minimized or hid debt; shame the leading reason (29.7\\%).'}),
 ('sifma2026','techreport','{SIFMA}','2026','Capital Markets Fact Book',
  {'note':'Global fixed-income debt outstanding \\$160.7T (+10.6\\% Y/Y); global equity market capitalization \\$157.8T (+18.9\\% Y/Y), end-2025.'}),
 ('suri2016','article','Suri, Tavneet and Jack, William','2016','The long-run poverty and gender impacts of mobile money',
  {'journal':'Science','volume':'354','number':'6317','pages':'1288--1292',
   'note':'M-Pesa access lifted ~194,000 households --- 2\\% of Kenyan households --- out of poverty; agent-proximity instrument. Critique: Bateman, Duvendack \\& Loubere, 2019, ROAPE.'}),
 ('sweet2013','article','Sweet, Elizabeth and Nandi, Arijit and Adam, Emma K. and McDade, Thomas W.','2013','The high price of debt: Household financial debt and its impact on mental and physical health',
  {'journal':'Social Science \\& Medicine','volume':'91','pages':'94--100',
   'note':'NLSY79, ages 24--32; high debt-to-assets associated with +11.7\\% perceived stress, +13.2\\% depressive symptoms, worse self-reported health, controlling for prior health and SES; diastolic-BP association weaker in adjusted models; associational.'}),
 ('tala','misc','{Tala}','2024','Smartphone-metadata scoring (company reports)',
  {'note':'Company-reported repayment >90\\%, 6M+ customers, >\\$2B disbursed --- [UNVERIFIED vendor claims]; no peer-reviewed default study located.'}),
 ('thaler2015','book','Thaler, Richard H.','2015','Misbehaving: The Making of Behavioral Economics',{'publisher':'W. W. Norton'}),
 ('thorne2006','article','Thorne, Deborah and Anderson, Leon','2006','Managing the stigma of personal bankruptcy',
  {'journal':'Sociological Focus','volume':'39','number':'2','pages':'77--97'}),
 ('doj2017','misc','{U.S. Department of Justice}','2017','Justice Department and state partners secure nearly \\$864 million settlement with Moody\'s arising from conduct in the lead-up to the financial crisis',{}),
 ('upstart2022','misc','{Upstart} and {CFPB}','2017','First CFPB no-action letter testing protocol (2017--2022)',
  {'note':'+27\\% approvals vs. traditional model at -16\\% average APRs; 23--29\\% approval gains across tested race/ethnicity/sex segments; ~2$\\times$ approval for near-prime (FICO 620--660). NAL terminated 2022 after model changes sought outside the agreed protocol.'}),
 ('verizon2025','techreport','{Verizon}','2025','2025 Data Breach Investigations Report',
  {'note':'Human element in ~60\\% of breaches; stolen credentials ~22\\%, vulnerability exploitation ~18\\%, phishing ~14\\% as leading initial vectors; third-party involvement doubled to 30\\%.'}),
 ('w3cietf','misc','{W3C} and {IETF}','2022','DID Core 1.0 (W3C Recommendation, July 19, 2022); Verifiable Credentials Data Model 2.0 (W3C Recommendation, May 15, 2025); SD-JWT Selective Disclosure (IETF RFC 9901); BBS Data Integrity cryptosuites (W3C Candidate Recommendation Draft)',
  {'note':'BBS cryptosuites not yet a W3C Recommendation.'}),
 ('worldbank2025findex','misc','{World Bank}','2025','Global Findex Database',
  {'note':'Account ownership 78.7\\% global / 97.0\\% U.S., 2024.'}),
 ('worldbank2019','misc','{World Bank}','2019','Credit Reporting Knowledge Guide',
  {'note':'Public credit-registry coverage of adults: OECD 64.4\\%; Sub-Saharan Africa 7.0\\%.'}),
 ('worldbank2025credit','misc','{World Bank}','2025','Responsible Digital Credit',
  {'note':'Kenya: 2.7M defaulters 2014--2016; ~14M accounts in default by end-2022; 86\\% of digital borrowers facing repayment challenges in 2024 phone surveys.'}),
 ('x402','misc','{x402 Foundation}','2025','x402 micropayment protocol',
  {'note':'Incubated by Coinbase (May 2025); x402 Foundation co-launched with Cloudflare (Sept 2025); moved under the Linux Foundation (April 2026); 100M+ payments in first ~6 months, 169M+ in year one (Coinbase; early volume inflated by memecoin-mint/retry traffic --- caveat retained); zero protocol fees, sub-cent gas on Base.'}),
]

def write_bib(path):
    out = []
    for key, typ, author, year, title, extra in BIB:
        fields = [('author', author), ('year', year), ('title', '{' + title + '}')]
        fields += list(extra.items())
        def bval(v):
            v = v.replace('~', r'$\sim$')
            for a, b in [('ł', r'\l{}'), ('ö', r'\"o'), ('á', r"\'a"),
                         ('–', '--'), ('—', '---'), ('§', r'\S~')]:
                v = v.replace(a, b)
            return v
        body = ',\n'.join('  %s = {%s}' % (k, bval(v)) for k, v in fields)
        out.append('@%s{%s,\n%s\n}' % (typ, key, body))
    open(path, 'w').write('\n\n'.join(out) + '\n')
    print("wrote", path, len(BIB), "entries")

import os
write_bib(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whitepaper.bib'))
