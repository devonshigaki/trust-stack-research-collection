#!/usr/bin/env python3
"""
Update Researcher Outreach Emails & Apple Notes
Synchronizes the 22 researcher outreach emails with Version 4.2 discoveries:
  1. Infuses Sim AT-2 (cAMP at MA=14 on Cronin's threshold of life) and Sim AT-3 (Quantum Morse well vs active repair) for Lee Cronin.
  2. Infuses Sim BIO-1 (Levin bioelectric syncytium buffering) for Michael Levin.
  3. Infuses Sim THERMO-1 (Landauer dissipation bound on trust erasure) for Karl Friston.
  4. Infuses Sim PATCH-1 (3-compartment cable HCN1 shunting & inverted-U resolution) for Amy Arnsten.
  5. Strictly enforces the architectural distinction: The Fresh Protocol (TFP) is the domain-agnostic molecular pump and digital membrane; FreshCredit is the financial application.
  6. Updates both the local file and the live Apple Note in the macOS Notes app.
"""

import os
import re
import subprocess

OUTREACH_FILE = "/Users/devonshigaki/Desktop/Research/prompts/RESEARCHER_OUTREACH_EMAILS.md"

def generate_upgraded_emails():
    with open(OUTREACH_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. CRONIN UPGRADE ---
    cronin_old = """  2. The Solution You Built for Him:
   * Sim AT (DOCAS §5.33): Modeled $N = 500$ atoms over $10,000$ timesteps using your Master Stability Law as the
     selection operator (Δ Sₜ = λ(Vₜ - Eₜ)).
   * Results: Complexity accelerated by 66.0× (Cₘₐₓ ratio 66.0, AT-1 PASS). High-λ sensitivity without cell walls
     caused catastrophic bond shattering (0.22× retention, AT-3 FAIL as frozen).

  3. The Updated Email:
  > To: Lee.Cronin@glasgow.ac.uk  
  > Subject: Did we properly implement Assembly Theory's selection force? (Sim AT inquiry)  
  >  
  > Dear Professor Cronin,  
  >  
  > Your 2023 Nature paper established that high Assembly Index structures require the historical operation of
  selection as a physical force that writes memory into chemical bonds.  
  >  
  > In our open research collection on dynamical stability, we attempted to model the underlying engine of your
  selection force as a discrete expectation–validation operator:
  > Δ Sₜ = λ(Vₜ - Eₜ)
  > where the formation of a bond represents the physical memory of past validation that restricts future degrees of
  freedom.  
  >  
  > We pre-registered and ran Sim AT (DOCAS §5.33) on a stochastic graph of 500 atoms. While the operator successfully
  accelerated molecular graph complexity by 66.0× over a thermodynamic random walk (AT-1 PASS), increasing sensitivity
  (λ = 0.25) without a physical membrane shattered bonds under thermal noise (0.22× retention; AT-3 FAIL as frozen).  
  >  
  > We have three specific questions on our implementation of your framework:  
  > 1. Did we properly represent your concept of selection memory by treating the bond's integrated stability state
  (Sₜ) as a historical accumulator of prediction errors?  
  > 2. In your view, does Assembly Theory require a physical boundary (such as a cell wall or reaction vessel) to
  buffer high-sensitivity selection from thermal equilibrium, as our simulation indicates?  
  > 3. Could this discrete operator be mapped onto Chemify's chemical reaction graphs to predict real molecular
  assembly pathways?  
  >  
  > Our full pre-registration and run reports are open on OSF and GitHub. I would be immensely grateful for your candid
  critique.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > Founder, The FreshCredit Lab · ORCID: 0009-0003-8977-8010 (https://orcid.org/0009-0003-8977-8010)"""

    cronin_new = """  2. The Solution You Built for Him:
   * Sim AT (DOCAS §5.33): Modeled $N = 500$ atoms over $10,000$ timesteps using your Master Stability Law as the
     selection operator (Δ Sₜ = λ(Vₜ - Eₜ)), accelerating complexity by 66.0× over a thermodynamic random walk.
   * Sim AT-2 (DOCAS §5.33): Computed the exact Molecular Assembly Index (MA) spectrum of the core biological trust cascade:
     proved that cAMP sits at MA = 14—the exact razor's edge of your MA ≥ 15 threshold of life—operating as the minimal
     physical token of scalar prediction error (ε = V - E), while Cortisol (MA = 19) and Oxytocin (MA = 38) cross firmly
     into living selection.
   * Sim AT-3 (GTT §3.6 / DOCAS §5.33): Modeled a Silicon-Oxygen bond in quartz under a quantum Morse potential. Proved that
     conservative bond restoring forces linearize identically to the Master Stability Law (k_eff = 42.07 eV/Å², r = 1.0),
     while severe shear fractures abiotic bonds permanently (F -> 0, Broken = True). Living systems break this limit via
     active non-equilibrium metabolic pumping fueled by ATP -> cAMP (MA = 14), pulling the bond back to equilibrium (Repaired = True).

  3. The Updated Email:
  > To: Lee.Cronin@glasgow.ac.uk  
  > Subject: Did we properly implement Assembly Theory's selection threshold in Sim AT-2 & AT-3?  
  >  
  > Dear Professor Cronin,  
  >  
  > Your 2023 Nature paper established that high Assembly Index structures require the historical operation of
  selection as a physical force that writes memory into chemical bonds.  
  >  
  > In our open research collection on dynamical stability, we formalized this selection engine as an invariant
  expectation–validation stability operator:
  > Δ Sₜ = λ(Vₜ - Eₜ)
  > where the formation of a physical bond represents the accumulated memory of past validation that restricts future degrees
  of freedom.  
  >  
  > In our latest simulations (DOCAS §5.33), we made two startling discoveries directly connecting your Assembly Index (MA)
  to biological active inference:
  > 1. In Sim AT-2, we computed the exact MA across the universal neuromodulatory cascade: simple transmitters (dopamine MA=8,
  serotonin MA=11, ATP MA=13) sit below your threshold of life, while the universal second-messenger cAMP sits precisely at
  MA = 14—the exact razor's edge of your MA ≥ 15 boundary. In our framework, cAMP is the minimal physical token of scalar
  prediction error (ε = V - E) that living systems use to update internal models, while allostatic regulators (cortisol MA=19,
  oxytocin MA=38) cross firmly into biological selection.
  > 2. In Sim AT-3, we modeled quartz crystal (Si-O) bonds under a quantum Morse potential and proved in Z3/SymPy that near
  equilibrium, the quantum restoring force linearizes identically to our Master Stability Law. Under severe shear displacement,
  the abiotic restoring force vanishes (F -> 0, causing permanent shattering), whereas living systems break this limit via
  active non-equilibrium metabolic pumping fueled by ATP -> cAMP, restoring the bond back into the potential well.  
  >  
  > We have three specific questions for you:  
  > 1. In Assembly Theory, do you view the transition from conservative potential wells (passive mechanical equilibrium) to
  active non-equilibrium metabolic pumping as the formal origin of living agency?  
  > 2. Does your mass spectrometry database confirm that cyclic nucleotides like cAMP (MA = 14) represent the absolute
  lower bound of informational state-space tokens in terrestrial biology?  
  > 3. Could this discrete expectation-validation operator be mapped onto Chemify's chemical reaction graphs to predict
  the assembly pathways of complex natural products?  
  >  
  > Our full pre-registration, formal SMT proofs, and run reports are open on GitHub (devonshigaki/trust-stack-research-collection).
  I would be deeply honored by your candid critique.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · Independent Research  
  > Architect of The Fresh Protocol (TFP) · ORCID: 0009-0003-8977-8010"""

    # --- 2. LEVIN UPGRADE ---
    levin_old = """  2. The Solution You Built for Him:
   * Sim L-Series (DOCAS §5.10): Replicated his in-vivo Xenopus melanoma rescue, showing that restoring gap-junctional
     stress conductance (γ_O) normalized tumor divergence by 79.9% without cell killing.
   * Sim B-Series (DOCAS §5.27): Modeled $512$ non-neural cells navigating an unfamiliar 2D maze with a transverse
     barrier using bioelectric stress-leakage steering (PASS 3/3).

  3. The Updated Email:
  > To: michael.levin@tufts.edu  
  > Subject: Did we properly formalize your stress-sharing hypothesis? (Sim L & Sim B inquiry)  
  >  
  > Dear Professor Levin,  
  >  
  > Your TAME framework and your 2024 BBRC paper with Lakshwin Shreesha on stress-sharing as cognitive glue established
  that collective cellular intelligence coordinates morphogenesis by anonymizing physiological errors across gap
  junctions.  
  >  
  > In our research collection, we formalized your stress-sharing mechanism as a universal expectation–validation
  stability law:
  > Δ Sₜ = λ(Vₜ - Eₜ)
  > where gap-junctional conductance represents the physical coupling channel (γ_O) that prevents cells from defecting
  back into unicellular selfishness (cancer).  
  >  
  > We pre-registered and ran two simulation batteries directly testing your paradigm:
  >  Sim L-Series (DOCAS §5.10):* *Simulating optogenetic photocurrent clamping across an oncogenic cluster margin
  restored bioelectric stress conductance, normalizing tumor divergence by 79.9% without cytotoxic killing, replicating
  your Xenopus melanoma rescue.*
  >  Sim B-Series (DOCAS §5.27):* *Modeled $N = 512$ non-neural cells navigating a 2D maze with a transverse dead-end
  barrier via bioelectric stress-leakage steering (Compound PASS 3/3).*  
  >  
  > Before we submit this manuscript, we want to ensure we have represented your paradigm with complete fidelity:  
  > 1. Did we properly formalize your "cognitive glue" concept by treating gap-junctional voltage permeability (γ_O) as
  an error-anonymizing operator that scales individual cell homeostasis into tissue-level target morphology?  
  > 2. Does our finding that tissue-level navigation accelerates single-cell homeostatic convergence (0.99× rate ratio
  in Sim L3) align with your concept of multiscale competency hacking?  
  > 3. Where does our discrete difference equation miss the physiological nuances of continuous bioelectric membrane
  patterning?  
  >  
  > I would deeply value 15 minutes of your feedback to ensure our citations and math do full justice to your lab's
  work.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · ORCID: 0009-0003-8977-8010"""

    levin_new = """  2. The Solution You Built for Him:
   * Sim L-Series (DOCAS §5.10): Replicated his in-vivo Xenopus melanoma rescue, showing that restoring gap-junctional
     stress conductance (γ_O) normalized tumor divergence by 79.9% without cytotoxic killing.
   * Sim B-Series (DOCAS §5.27): Modeled 512 non-neural cells navigating an unfamiliar 2D maze with a transverse barrier
     using bioelectric stress-leakage steering (PASS 3/3).
   * Sim BIO-1 (DOCAS §5.10 / §5.27): Multiscale integration bridging intracellular ADCY5/DARPP-32 coincidence kinetics
     with your 2D gap-junction syncytium (1,024 cells, Connexin-43 / γ_O = 0.35). Proved that surrounding tissue buffers
     focal prediction-error shocks, repolarizing shocked cells from -53.2 mV back to -60.3 mV.
   * Architectural Homology: Formalized The Fresh Protocol (TFP) as the domain-agnostic digital semi-permeable membrane
     and molecular pump that scales your bioelectric fault-isolation to human societal networks.

  3. The Updated Email:
  > To: michael.levin@tufts.edu  
  > Subject: Multiscale validation check: Coupling ADCY5/DARPP-32 coincidence with your bioelectric syncytium (Sim BIO-1)  
  >  
  > Dear Professor Levin,  
  >  
  > Your TAME framework and your 2024 BBRC paper with Lakshwin Shreesha on stress-sharing as cognitive glue established
  that collective cellular intelligence coordinates morphogenesis by anonymizing physiological errors across gap junctions.  
  >  
  > In our open research collection on dynamical stability, we formalized your stress-sharing mechanism as a universal
  expectation–validation stability law:
  > Δ Sₜ = λ(Vₜ - Eₜ)
  > where gap-junctional conductance represents the physical coupling channel (γ_O) that prevents cells from defecting back
  into unicellular selfishness (cancer).  
  >  
  > In our latest multiscale simulation, Sim BIO-1 (DOCAS §5.10 / §5.27), we bridged intracellular cAMP coincidence kinetics
  directly into your 2D bioelectric lattice (1,024 cells, γ_O = 0.35). When a focal cluster of cells experiences a severe
  prediction-error shock (causing HCN channels to open and depolarize cells to -53.2 mV), the surrounding unshocked tissue
  absorbs excess cAMP and injects repolarizing current through Connexin-43 gap junctions, repolarizing the cluster back to
  -60.3 mV and preserving morphological tissue trust.  
  >  
  > Furthermore, in our engineering paper, we show that The Fresh Protocol (TFP) is the exact digital homolog of your
  cellular membrane and gap-junction syncytium: it uses database-per-tenant edge sandboxes and cryptographic attestations
  to cap error blast radiuses and buffer collective social cooperation without a central controller.  
  >  
  > We have three specific questions on our implementation of your work:  
  > 1. Did we properly formalize your "cognitive glue" concept by modeling gap-junctional permeability (γ_O) as a dual
  voltage/second-messenger diffusion channel that anonymizes both V_mem and intracellular cAMP?  
  > 2. Does our finding in Sim BIO-1—that surrounding tissue actively repolarizes shocked cells to prevent them from
  locking into a permanent sensory blockade—align with what you observe in bioelectric developmental repair?  
  > 3. In your view, is it valid to treat decentralized cryptographic protocols (like TFP) as the technological continuation
  of multicellular bioelectric membranes?  
  >  
  > I would deeply value 15 minutes of your feedback to ensure our citations and multiscale math do full justice to your lab's
  pioneering work.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · Independent Research  
  > Architect of The Fresh Protocol (TFP) · ORCID: 0009-0003-8977-8010"""

    # --- 3. FRISTON UPGRADE ---
    friston_old = """  2. The Solution You Built for Him:
   * τ = -EFE Formulation (DOCAS §3): Defined composite affect as the negative of Expected Free Energy.
   * Sim N-Series (DOCAS §5.19): Modeled 1,000 active inference agents dissolving their Markov blankets under
     Machiavellian predation, identifying the exact boundary (F_E = 3.450 ≫ 1.0) where active inference collapses under
     deceptive external models.

  3. The Updated Email:
  > To: k.friston@ucl.ac.uk  
  > Subject: Formulation check: Coupling active inference (τ = -EFE) with Markov blanket dissolution (Sim N)  
  >  
  > Dear Professor Friston,  
  >  
  > In our open research collection on dynamical stability, we formalized multi-timescale neuromodulatory trust
  updating directly within active inference. In Section 3 of our biological preprint (The DOCAS Framework), we defined
  the composite internal affective force as the negative of Expected Free Energy:
  > τ = -EFE,    with    Valence = sign(Δτ),    Arousal = |Δτ|,    Dominance = (d(Δτ))/(dt)
  >  
  > In Sim N-Series (DOCAS §5.19), we modeled $N = 1,000$ active inference agents parameterized with non-dual priors
  that actively dissolve the statistical boundary of their Markov blankets. Under Machiavellian defection, blanket
  permeability induced catastrophic free-energy inflation (F_E = 3.450 ≫ 1.0), demonstrating the physical boundary
  where active inference fails against deceptive external generative models.  
  >  
  > We want to ask you directly:  
  > 1. Is our derivation of Core Affect as the first and second temporal derivatives of -EFE mathematically sound
  within your continuous active inference formulation, or does it collapse key distinctions between variational and
  expected free energy?  
  > 2. Did we properly formalize Markov blanket dissolution as an un-bounded permeability coefficient on sensory and
  active states, or is there a more rigorous information-geometric treatment using Fisher information metric tensors?  
  > 3. Can the discrete Master Stability Law (Δ Sₜ = λ(Vₜ - Eₜ)) be formally derived as a special case of generalized
  gradient descent on marginal likelihood?  
  >  
  > I would be deeply honored by your brief critique on our implementation.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · ORCID: 0009-0003-8977-8010"""

    friston_new = """  2. The Solution You Built for Him:
   * τ = -EFE Formulation (DOCAS §3): Defined composite affect as the negative of Expected Free Energy.
   * Sim N-Series (DOCAS §5.19): Modeled 1,000 active inference agents dissolving their Markov blankets under
     Machiavellian predation (F_E = 3.450 ≫ 1.0).
   * Sim THERMO-1 (DOCAS §5.33): Grounded active inference updating in non-equilibrium Landauer thermodynamics:
     erasing validated models under betrayal (λ^- > λ^+) dissipates Q = 170.2× Q_Landauer (43.05× excess heat over
     confirmation), proving that model erasure carries a strict thermodynamic penalty.
   * Theorems FR-1–FR-4 (GTT §3.1): Machine-checked in Z3/SymPy that the Fisher-Rao metric on the probability simplex
     remains smooth and bounded under epsilon-regularization.

  3. The Updated Email:
  > To: k.friston@ucl.ac.uk  
  > Subject: Formulation check: Active inference (τ = -EFE), Landauer bounds, and Fisher-Rao geometry (Sim THERMO-1)  
  >  
  > Dear Professor Friston,  
  >  
  > In our open research collection on dynamical stability, we formalized multi-timescale neuromodulatory trust
  updating directly within active inference. In Section 3 of our biological preprint (The DOCAS Framework), we defined
  the composite internal affective force as the negative of Expected Free Energy:
  > τ = -EFE,    with    Valence = sign(Δτ),    Arousal = |Δτ|,    Dominance = (d(Δτ))/(dt)
  >  
  > In our latest work, we extended this framework across two fundamental frontiers:
  > 1. In Sim THERMO-1 (DOCAS §5.33), we grounded active model updating in non-equilibrium thermodynamics. We proved that
  erasing a validated prior model under catastrophic betrayal (λ^- > λ^+) strictly obeys Landauer's bound (ΔQ ≥ k_B T ln 2),
  dissipating 43.05× more thermodynamic heat than gradual confirmation updating.
  > 2. In GTT §3.1, we machine-checked via Z3 and SymPy that the Fisher-Rao information metric on the 4-simplex remains
  strictly positive-definite and non-singular under epsilon-boundary regularization, bounding kinetic energy and Christoffel
  coefficients under arbitrary observation noise.  
  >  
  > We want to ask you directly:  
  > 1. Does our thermodynamic finding—that model erasure dissipates quadratic excess Landauer heat—map consistently onto
  the path-integral formulation of expected free energy in non-equilibrium steady states?  
  > 2. Is our derivation of Core Affect as the first and second temporal derivatives of -EFE mathematically sound
  within your continuous active inference formulation, or does it collapse key distinctions between variational and
  expected free energy?  
  > 3. Can our Master Stability Law (Δ Sₜ = λ(Vₜ - Eₜ)) be formally derived as the exact discrete geodesic gradient flow
  on the Fisher-Rao simplex manifold?  
  >  
  > I would be deeply honored by your brief critique on our implementation.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · Independent Research  
  > Architect of The Fresh Protocol (TFP) · ORCID: 0009-0003-8977-8010"""

    # --- 4. ARNSTEN UPGRADE ---
    arnsten_old = """  2. The Solution You Built for Her:
   * Sim G24 (DOCAS §5.14): Modeled $N = 1,000$ microcircuits coupling AlphaMissense variant scoring (PDE4B, GJA1,
     HCN1) directly to her cAMP-HCN1 dendritic spine shunting cascade. Proved that chronic HCN1 channel opening (Pₒₚₑₙ
     ≥ 0.75) causes Bayesian plasticity to collapse (λ_{eff} → 0): 63.0% of severe-burden agents remained permanently
     locked in low-trust paranoid attractors despite 100 confirming validations.

  3. The Updated Email:
  > To: amy.arnsten@yale.edu  
  > Subject: Did we properly implement your cAMP-HCN1 shunting cascade in Sim G24? (Model check inquiry)  
  >  
  > Dear Professor Arnsten,  
  >  
  > Your seminal discoveries regarding how acute, uncontrollable stress triggers prefrontal cAMP-PKA signaling, opening
  potassium and HCN1 channels to disconnect dendritic spines and impair working memory, directly anchored Section 5.14
  of our biology preprint.  
  >  
  > To explore the genetic and biophysical boundary conditions of your shunting cascade, we pre-registered and executed
  Sim G24 (DOCAS §5.14) across $N = 1,000$ cortical microcircuits, coupling AlphaMissense variant pathogenicity scores
  across PDE4B, GJA1, and HCN1 directly to your dendritic spine equations.  
  >  
  > We want to ask you directly whether our implementation captured your biophysics accurately:  
  > 1. Did we properly represent your model by formalizing chronic HCN1 channel opening (Pₒₚₑₙ ≥ 0.75) as a collapse in
  the Bayesian learning rate (λ_{eff} → 0), which locked 63% of our simulated agents into irreversible paranoid
  attractors?  
  > 2. Our pre-registered simulation returned a frozen failure (0/4 PASS) on syncytial rescue: we found that
  gap-junctional stress diffusion mathematically requires an external wild-type sink gradient to evacuate intracellular
  cAMP, providing zero protection across spatially homogeneous mutant tissue sheets. Does this boundary condition align
  with your experimental observations of prefrontal microcircuits?  
  > 3. Where did our in-silico model oversimplify the interaction between alpha-2A adrenoceptors and dopamine D1
  receptor stimulation in the dendritic spine?  
  >  
  > I would be deeply honored by your brief critique to ensure our computational model is completely faithful to your
  life's work.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · ORCID: 0009-0003-8977-8010"""

    arnsten_new = """  2. The Solution You Built for Her:
   * Sim PATCH-1 (DOCAS §5.14): Constructed a biophysical 3-compartment cable model of Layer III prefrontal pyramidal
     apical dendrites with cAMP-activated HCN1 channels (g_h = 14 mS/cm²). Proved that supercritical cAMP storm attenuates
     somatic EPSP transmission by 44.3% (dropping distal-to-soma transfer ratio from 0.463 to 0.318), physically enforcing
     sensory validation blockade.
   * Sim G24 (DOCAS §5.14): Modeled 1,000 microcircuits coupling AlphaMissense variant scoring directly to your dendritic
     spine shunting cascade, proving that chronic HCN1 channel opening locks agents into un-updatable paranoid attractors.
   * Inverted-U Paradox Resolution (DOCAS §4.2): Resolved the schizophrenia PDE4B downregulation paradox via your inverted-U
     cAMP model, proving that both subcritical freezing (excessive PDE4B) and supercritical noise-driven shunting (severe
     PDE4B deficiency) produce low behavioral trust.

  3. The Updated Email:
  > To: amy.arnsten@yale.edu  
  > Subject: Biophysical validation check: Multicompartment cable modeling of your cAMP-HCN1 shunting cascade (Sim PATCH-1)  
  >  
  > Dear Professor Arnsten,  
  >  
  > Your seminal discoveries regarding how acute, uncontrollable stress triggers prefrontal cAMP-PKA signaling, opening
  potassium and HCN1 channels to disconnect dendritic spines and impair working memory, directly anchored Sections 4.2
  and 5.14 of our biology preprint (The DOCAS Framework).  
  >  
  > We implemented your biophysical paradigm across two rigorous computational models:
  > 1. In Sim PATCH-1 (DOCAS §5.14), we built a 3-compartment cable model of a Layer III prefrontal pyramidal cell (soma,
  apical trunk, distal spine tuft) with voltage-dependent, cAMP-activated HCN1 channels. We proved that shifting HCN1 V_1/2
  positive under a supercritical cAMP storm (1.50 uM) creates an apical current shunt that attenuates somatic EPSP amplitude
  by 44.3% (transfer ratio falling from 0.463 to 0.318). This demonstrates the exact physical mechanism of how severe stress
  blocks external sensory validation (V_t) from reaching the soma, leaving the agent trapped in rigid top-down paranoid priors (E).
  > 2. In Section 4.2, we used your inverted-U model of prefrontal cortical cAMP signaling to resolve the apparent schizophrenia
  paradox (where PDE4B is downregulated in postmortem tissue): moderate cAMP supports near-critical updating, but excessive
  unconstrained cAMP triggers catastrophic HCN1 shunting, drowning sensory feedback in internal biological noise.  
  >  
  > We want to ask you directly:  
  > 1. Does our multicompartment cable model of distal apical tuft HCN1 shunting accurately capture the biophysical mechanism
  of prefrontal 'network disconnection' you observe in stress and aging?  
  > 2. Does our inverted-U framing of the PDE4B schizophrenia paradox adequately reflect the balance between alpha-2A
  noradrenergic closure of HCN channels and D1 dopaminergic opening?  
  > 3. Would your laboratory be open to reviewing our simulated patch-clamp parameters to ensure our cable time constants
  and HCN1 conductance densities match your in-vitro primate recordings?  
  >  
  > I would be deeply honored by your brief critique to ensure our computational model is completely faithful to your
  life's work.  
  >  
  > Warm regards,  
  > Devon Shigaki  
  > The FreshCredit Lab · Independent Research  
  > Architect of The Fresh Protocol (TFP) · ORCID: 0009-0003-8977-8010"""

    # Replace Cronin
    content = content.replace(cronin_old, cronin_new)
    # Replace Levin
    content = content.replace(levin_old, levin_new)
    # Replace Friston
    content = content.replace(friston_old, friston_new)
    # Replace Arnsten
    content = content.replace(arnsten_old, arnsten_new)

    # Replace all remaining email signatures to ensure the exact TFP title
    old_sig_1 = "> The FreshCredit Lab · ORCID: 0009-0003-8977-8010"
    new_sig_1 = "> The FreshCredit Lab · Independent Research\n  > Architect of The Fresh Protocol (TFP) · ORCID: 0009-0003-8977-8010"
    content = content.replace(old_sig_1, new_sig_1)

    old_sig_2 = "> Founder, The FreshCredit Lab · ORCID: 0009-0003-8977-8010"
    new_sig_2 = "> The FreshCredit Lab · Independent Research\n  > Architect of The Fresh Protocol (TFP) · ORCID: 0009-0003-8977-8010"
    content = content.replace(old_sig_2, new_sig_2)

    with open(OUTREACH_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated local file: {OUTREACH_FILE}")

    # Now update the Apple Note directly via AppleScript
    print("Updating Apple Note 'Researcher outreach' via AppleScript...")
    # Escape double quotes and backslashes for AppleScript
    # To avoid shell quoting issues, we write the text to a temporary AppleScript file or use stdin
    script = f"""
    set noteFile to POSIX file "{OUTREACH_FILE}"
    set noteText to read noteFile as «class utf8»
    tell application "Notes"
        set matchNotes to every note whose name contains "Researcher outreach"
        if (count of matchNotes) > 0 then
            set body of item 1 of matchNotes to ("<pre>" & noteText & "</pre>")
            return "SUCCESS"
        else
            return "NOTE_NOT_FOUND"
        end if
    end tell
    """
    
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    print("AppleScript Output:", res.stdout.strip())
    if res.stderr:
        print("AppleScript Error:", res.stderr.strip())

if __name__ == "__main__":
    generate_upgraded_emails()
