#!/usr/bin/env python3
"""
Tool: Structured Academic CRM & Campaign Tracker Generator
Generates OUTREACH_CAMPAIGN_TRACKER.csv for managing multi-stage academic engagement.
"""

import os
import csv

CSV_PATH = "/Users/devonshigaki/Desktop/Research/OUTREACH_CAMPAIGN_TRACKER.csv"

RECORDS = [
    {
        "ID": 1,
        "PI_Name": "Lee Cronin",
        "Institution": "University of Glasgow / Chemify",
        "PI_Email": "Lee.Cronin@glasgow.ac.uk",
        "Lead_2Hop_Contact": "Dr. Stuart M. Marshall (Senior Postdoc)",
        "Lead_2Hop_Role_or_Email": "stuart.marshall@glasgow.ac.uk",
        "Domain": "Natural Philosophy & Assembly Theory",
        "Anchor_Paper_2024_2026": "Molecular assembly as a universal biosignature (2026 PNAS)",
        "Code_Artifact": "sim_tandem_ms_assembly_trees.py & sim_at2_assembly_results.json",
        "Stage": "Stage 1: Postdoc Code Verification",
        "Status": "Ready to Send",
        "Next_Action": "Email Stuart Marshall re CID tree of cAMP (MA=14)",
        "Target_Date": "2026-11-10"
    },
    {
        "ID": 2,
        "PI_Name": "Michael Levin",
        "Institution": "Tufts University / Allen Discovery Center",
        "PI_Email": "michael.levin@tufts.edu",
        "Lead_2Hop_Contact": "Lakshwin Shreesha (Doctoral Fellow)",
        "Lead_2Hop_Role_or_Email": "lakshwin.shreesha@tufts.edu",
        "Domain": "Developmental Bioelectrics & Basal Cognition",
        "Anchor_Paper_2024_2026": "Stress-sharing as cognitive glue (2024 BBRC)",
        "Code_Artifact": "sim_cellular_coincidence_levin.py",
        "Stage": "Stage 1: Postdoc Code Verification",
        "Status": "Ready to Send",
        "Next_Action": "Share 2D Connexin syncytium repolarization results with Shreesha",
        "Target_Date": "2026-11-10"
    },
    {
        "ID": 3,
        "PI_Name": "Karl Friston",
        "Institution": "University College London / Wellcome Centre",
        "PI_Email": "k.friston@ucl.ac.uk",
        "Lead_2Hop_Contact": "Dr. Lancelot Da Costa (Postdoc / Math Lead)",
        "Lead_2Hop_Role_or_Email": "lancelot.dacosta@ucl.ac.uk",
        "Domain": "Free Energy Principle & Active Inference",
        "Anchor_Paper_2024_2026": "Renormalising Generative Models for Active Inference (2026 arXiv)",
        "Code_Artifact": "sim_landauer_trust_thermodynamics.py & z3_multiscale_assembly_manifold.py",
        "Stage": "Stage 1: Math Verification",
        "Status": "Ready to Send",
        "Next_Action": "Inquire with Da Costa on Landauer bound erasure in EFE path integrals",
        "Target_Date": "2026-11-11"
    },
    {
        "ID": 4,
        "PI_Name": "Lisa Feldman Barrett",
        "Institution": "Northeastern University / IASLab",
        "PI_Email": "l.barrett@northeastern.edu",
        "Lead_2Hop_Contact": "Dr. Jordan Theriault (Assistant Professor)",
        "Lead_2Hop_Role_or_Email": "j.theriault@northeastern.edu",
        "Domain": "Constructed Emotion & Predictive Processing",
        "Anchor_Paper_2024_2026": "Categorization is 'baked' into the brain (2026 NRN)",
        "Code_Artifact": "sim_meta_results.json & DOCAS §3 Core Affect derivation",
        "Stage": "Stage 1: Model Feedback",
        "Status": "Ready to Send",
        "Next_Action": "Send Core Affect derivative proof eliminating essentialist emotion circuits",
        "Target_Date": "2026-11-12"
    },
    {
        "ID": 5,
        "PI_Name": "Kristen Lindquist",
        "Institution": "The Ohio State University / Affective Science Lab",
        "PI_Email": "lindquist.118@osu.edu",
        "Lead_2Hop_Contact": "Dr. Xuan Yang (CCBBI Postdoc)",
        "Lead_2Hop_Role_or_Email": "yang.xuan@osu.edu",
        "Domain": "Cross-Linguistic Emotion Semantics",
        "Anchor_Paper_2024_2026": "Emotions Are Folk Concepts in a Predicting Brain (2026 Brain Sci)",
        "Code_Artifact": "query_clics4_cldf.py & clics_permutation_verified.json",
        "Stage": "Stage 1: Graph Audit",
        "Status": "Ready to Send",
        "Next_Action": "Share 51k-edge CLICS 4.0 permutation test with Dr. Xuan Yang",
        "Target_Date": "2026-11-12"
    },
    {
        "ID": 6,
        "PI_Name": "Daniel Levitin",
        "Institution": "McGill University / Minerva",
        "PI_Email": "daniel.levitin@mcgill.ca",
        "Lead_2Hop_Contact": "Lindsay A. Fleming, MA (Lab Manager)",
        "Lead_2Hop_Role_or_Email": "lindsay.fleming@mcgill.ca",
        "Domain": "Cognitive Neuroscience of Music & Groove",
        "Anchor_Paper_2024_2026": "From Zero to Sixty: Calibrating Real-Time Responses (2025 Psychometrika)",
        "Code_Artifact": "sim_m_series_results.json",
        "Stage": "Stage 1: Technical Verification",
        "Status": "Ready to Send",
        "Next_Action": "Inquire with Koulis/Fleming on real-time Kuramoto phase calibration",
        "Target_Date": "2026-11-13"
    },
    {
        "ID": 7,
        "PI_Name": "Amy Arnsten",
        "Institution": "Yale School of Medicine",
        "PI_Email": "amy.arnsten@yale.edu",
        "Lead_2Hop_Contact": "Dr. Min Wang / Dr. Constantinos Paspalas",
        "Lead_2Hop_Role_or_Email": "min.wang@yale.edu / constantinos.paspalas@yale.edu",
        "Domain": "Prefrontal Cortical Stress Signaling & DNC",
        "Anchor_Paper_2024_2026": "Dynamic network connectivity: Molecular regulation (2024 NRN)",
        "Code_Artifact": "sim_patch_clamp_hcn_shunting.py",
        "Stage": "Stage 1: Cable Model Review",
        "Status": "Ready to Send",
        "Next_Action": "Send apical HCN1 shunting cable simulation to Min Wang & Paspalas",
        "Target_Date": "2026-11-13"
    },
    {
        "ID": 8,
        "PI_Name": "Dietmar Plenz",
        "Institution": "National Institute of Mental Health / NIH",
        "PI_Email": "plenzd@mail.nih.gov",
        "Lead_2Hop_Contact": "Dr. Sinisa Pajevic (Staff Scientist)",
        "Lead_2Hop_Role_or_Email": "pajevics@mail.nih.gov",
        "Domain": "Critical Brain Dynamics & Neuronal Avalanches",
        "Anchor_Paper_2024_2026": "Self-organized criticality in the brain (2024/2026 Front Syst Neurosci)",
        "Code_Artifact": "sim_crit_branching.py",
        "Stage": "Stage 1: Code Verification",
        "Status": "Ready to Send",
        "Next_Action": "Share Brian2 branching parameter model (sigma=1.0) with Sinisa Pajevic",
        "Target_Date": "2026-11-14"
    },
    {
        "ID": 9,
        "PI_Name": "Randy Buckner",
        "Institution": "Harvard University / Center for Brain Science",
        "PI_Email": "randy_buckner@harvard.edu",
        "Lead_2Hop_Contact": "Dr. Jingnan Du (Postdoctoral Fellow)",
        "Lead_2Hop_Role_or_Email": "jingnandu@fas.harvard.edu",
        "Domain": "Default Mode Network & Cortical Parcellation",
        "Anchor_Paper_2024_2026": "Parallel interdigitated distributed networks (2024 J Neurophysiol)",
        "Code_Artifact": "sim_d21_results.json & DU15NET cortical overlay",
        "Stage": "Stage 1: Parcellation Alignment",
        "Status": "Ready to Send",
        "Next_Action": "Contact Jingnan Du on depth-5 counterfactual rollout overlay on DU15NET",
        "Target_Date": "2026-11-14"
    },
    {
        "ID": 10,
        "PI_Name": "Robert Sapolsky",
        "Institution": "Stanford University",
        "PI_Email": "sapolsky@stanford.edu",
        "Lead_2Hop_Contact": "Lisa Share (Research Assistant)",
        "Lead_2Hop_Role_or_Email": "sapolsky_lab@stanford.edu",
        "Domain": "Stress Endocrinology & Behavioral Biology",
        "Anchor_Paper_2024_2026": "Determined: Life without Free Will (2023/2024)",
        "Code_Artifact": "sim_s1_results.json (MSN dendritic trace r=1.0)",
        "Stage": "Stage 2: PI Philosophical Inquiry",
        "Status": "Ready to Send",
        "Next_Action": "Send inquiry on restorative non-punitive credit underwriting in TFP",
        "Target_Date": "2026-11-15"
    },
    {
        "ID": 11,
        "PI_Name": "Richard Thaler",
        "Institution": "University of Chicago Booth",
        "PI_Email": "Richard.Thaler@chicagobooth.edu",
        "Lead_2Hop_Contact": "Joshua Conrad Jackson (Bridge Faculty)",
        "Lead_2Hop_Role_or_Email": "joshua.jackson@chicagobooth.edu",
        "Domain": "Behavioral Economics & Choice Architecture",
        "Anchor_Paper_2024_2026": "Behavioral Public Policy: Past, Present, and Future (2025 BPP)",
        "Code_Artifact": "sim_p7b_results.json",
        "Stage": "Stage 2: PI Strategic Inquiry",
        "Status": "Ready to Send",
        "Next_Action": "Present event-time feedback model eliminating predatory contract uptake",
        "Target_Date": "2026-11-15"
    },
    {
        "ID": 12,
        "PI_Name": "Cass Sunstein",
        "Institution": "Harvard Law School",
        "PI_Email": "csunstei@law.harvard.edu",
        "Lead_2Hop_Contact": "Lucia Reisch (Co-Author / Research Lead)",
        "Lead_2Hop_Role_or_Email": "lreisch@law.harvard.edu",
        "Domain": "Sludge Auditing & Behavioral Administrative Law",
        "Anchor_Paper_2024_2026": "Imperfect Oracle: What AI Can and Cannot Do (2025 OUP)",
        "Code_Artifact": "sim_d16_results.json & sim_d20_results.json",
        "Stage": "Stage 2: PI Strategic Inquiry",
        "Status": "Ready to Send",
        "Next_Action": "Share psychophysical reality-monitoring threshold (T=2.5) for sludge audits",
        "Target_Date": "2026-11-16"
    },
    {
        "ID": 13,
        "PI_Name": "Sendhil Mullainathan",
        "Institution": "MIT Economics & EECS / The Bike Shop@MIT",
        "PI_Email": "mullain@mit.edu",
        "Lead_2Hop_Contact": "Dr. Frank Schilbach (Associate Professor, MIT)",
        "Lead_2Hop_Role_or_Email": "fschilb@mit.edu",
        "Domain": "Scarcity & Economics in the Age of Algorithms",
        "Anchor_Paper_2024_2026": "Do Financial Concerns Make Workers Less Productive? (2025 QJE)",
        "Code_Artifact": "Project Clearing-Shock telemetry protocol & sim_w8_shapley.py",
        "Stage": "Stage 1: Faculty Bridge Discussion",
        "Status": "Ready to Send",
        "Next_Action": "Contact Frank Schilbach on measuring bank fee cognitive taxes via fNIRS/EEG",
        "Target_Date": "2026-11-16"
    },
    {
        "ID": 14,
        "PI_Name": "George Loewenstein",
        "Institution": "Carnegie Mellon University",
        "PI_Email": "gl20@andrew.cmu.edu",
        "Lead_2Hop_Contact": "Zachary Wojtowicz (Postdoctoral Fellow)",
        "Lead_2Hop_Role_or_Email": "zwojtowi@andrew.cmu.edu",
        "Domain": "Economics of Attention & S-Frame Policy",
        "Anchor_Paper_2024_2026": "The Economics of Attention (2025 JEL)",
        "Code_Artifact": "sim_d21_results.json & TFP S-Frame specification",
        "Stage": "Stage 1: Postdoc Discussion",
        "Status": "Ready to Send",
        "Next_Action": "Share TFP as an S-Frame systemic architecture with Zachary Wojtowicz",
        "Target_Date": "2026-11-17"
    },
    {
        "ID": 15,
        "PI_Name": "Piotr Bialowolski",
        "Institution": "Harvard T.H. Chan School of Public Health",
        "PI_Email": "pbialowolski@hsph.harvard.edu",
        "Lead_2Hop_Contact": "Dr. Tyler VanderWeele (Director, Flourishing Program)",
        "Lead_2Hop_Role_or_Email": "tvanderw@hsph.harvard.edu",
        "Domain": "Financial Fragility & Population Health",
        "Anchor_Paper_2024_2026": "Bidirectional Associations Between Finance and Health (2025 SSM)",
        "Code_Artifact": "Whitepaper §4.3 NNH Allostatic Harm Ledger",
        "Stage": "Stage 2: PI Strategic Inquiry",
        "Status": "Ready to Send",
        "Next_Action": "Send NNH=1.03 clinical harm calculation for credit bureau rejections",
        "Target_Date": "2026-11-17"
    },
    {
        "ID": 16,
        "PI_Name": "Colin Camerer",
        "Institution": "Caltech (Visiting Harvard / MIT)",
        "PI_Email": "camerer@hss.caltech.edu",
        "Lead_2Hop_Contact": "Thomas L. Henning (PhD Candidate / AI Trust Lead)",
        "Lead_2Hop_Role_or_Email": "thenning@caltech.edu",
        "Domain": "Neuroeconomics & Behavioral Game Theory",
        "Anchor_Paper_2024_2026": "Neural substrates of calibrated trust in artificial agents (2025/2026)",
        "Code_Artifact": "sim_p9_dyn_couple.py (Kuramoto R=0.907)",
        "Stage": "Stage 1: PhD Student Validation",
        "Status": "Ready to Send",
        "Next_Action": "Engage Thomas Henning on dyadic Kuramoto PLV on TFP x402 payment rails",
        "Target_Date": "2026-11-18"
    },
    {
        "ID": 17,
        "PI_Name": "Timothy Behrens",
        "Institution": "University of Oxford / Wellcome Centre",
        "PI_Email": "behrens@fmrib.ox.ac.uk",
        "Lead_2Hop_Contact": "Dr. Laurence Hunt (Associate Professor)",
        "Lead_2Hop_Role_or_Email": "laurence.hunt@psy.ox.ac.uk",
        "Domain": "Prefrontal Cognitive Maps & Volatility Learning",
        "Anchor_Paper_2024_2026": "Cholinergic modulation of reinforcement learning (2026 Preprint)",
        "Code_Artifact": "SIM-R1 Misspecification Battery (+0.117 recovery bias)",
        "Stage": "Stage 1: Co-Author In-Silico Check",
        "Status": "Ready to Send",
        "Next_Action": "Contact Laurence Hunt on constant-lambda vs volatility-adaptive estimators",
        "Target_Date": "2026-11-18"
    },
    {
        "ID": 18,
        "PI_Name": "Brian Knutson",
        "Institution": "Stanford University / SPCI Lab",
        "PI_Email": "knutson@stanford.edu",
        "Lead_2Hop_Contact": "Dr. Alexander Genevsky (Alumnus / Bridge)",
        "Lead_2Hop_Role_or_Email": "genevsky@rsm.nl",
        "Domain": "Neuroforecasting & Striatal Valuation",
        "Anchor_Paper_2024_2026": "Neuroforecasting reveals generalizable components of choice (2025 PNAS)",
        "Code_Artifact": "sim_d21_results.json",
        "Stage": "Stage 1: Bridge Discussion",
        "Status": "Ready to Send",
        "Next_Action": "Share forward-encoding model of insula numbing under predatory contracts",
        "Target_Date": "2026-11-19"
    },
    {
        "ID": 19,
        "PI_Name": "Camilla Nord",
        "Institution": "University of Cambridge / MRC CBU",
        "PI_Email": "camilla.nord@mrc-cbu.cam.ac.uk",
        "Lead_2Hop_Contact": "Dr. Lydia Hickman (Wellcome Postdoc)",
        "Lead_2Hop_Role_or_Email": "lydia.hickman@mrc-cbu.cam.ac.uk",
        "Domain": "Interoception & Computational Mental Health",
        "Anchor_Paper_2024_2026": "Interoceptive precision in psychiatric illness (2024 NBR)",
        "Code_Artifact": "Project Clearing-Shock telemetry dataset specification",
        "Stage": "Stage 1: Postdoc Review",
        "Status": "Ready to Send",
        "Next_Action": "Send overnight RMSSD collapse dataset following bank overdraft clearing",
        "Target_Date": "2026-11-19"
    },
    {
        "ID": 20,
        "PI_Name": "Russell Poldrack",
        "Institution": "Stanford University",
        "PI_Email": "poldrack@stanford.edu",
        "Lead_2Hop_Contact": "Dr. Eric Bridgeford / Dr. Patrick Bissett",
        "Lead_2Hop_Role_or_Email": "ebridgeford@stanford.edu / pbissett@stanford.edu",
        "Domain": "Dense Phenotyping & Open Science Workflows",
        "Anchor_Paper_2024_2026": "Longitudinal precision neuroimaging (2024 NRN)",
        "Code_Artifact": "stationary_block_bootstrap_granger.py & ds003020 audit",
        "Stage": "Stage 1: Postdoc Stats Check",
        "Status": "Ready to Send",
        "Next_Action": "Inquire with Eric Bridgeford on block-bootstrap stationary lag-selection",
        "Target_Date": "2026-11-20"
    },
    {
        "ID": 21,
        "PI_Name": "Joe Gladstone",
        "Institution": "University of California, San Diego",
        "PI_Email": "jgladstone@ucsd.edu",
        "Lead_2Hop_Contact": "Dr. Sandra Matz (Bridge / Columbia)",
        "Lead_2Hop_Role_or_Email": "sm4409@gsb.columbia.edu",
        "Domain": "Banking Records & Consumer Financial Distress",
        "Anchor_Paper_2024_2026": "Detecting Feelings of Financial Distress from Bank Transactions (2025/2026)",
        "Code_Artifact": "Plaid transaction synchronization pipeline with wearable telemetry",
        "Stage": "Stage 2: PI Strategic Inquiry",
        "Status": "Ready to Send",
        "Next_Action": "Share real-time cash-flow buffer underwriting model with Gladstone",
        "Target_Date": "2026-11-20"
    },
    {
        "ID": 22,
        "PI_Name": "Gary King",
        "Institution": "Harvard University / IQSS",
        "PI_Email": "king@harvard.edu",
        "Lead_2Hop_Contact": "Dr. Steven Worthington (Director of Data Science)",
        "Lead_2Hop_Role_or_Email": "worthington@iqss.harvard.edu",
        "Domain": "Open Science & Quantitative Replication",
        "Anchor_Paper_2024_2026": "Improving the reliability of social science replication archives (2024 Science)",
        "Code_Artifact": "run_tier1_tier2_suite.py (19 tasks) & Lean 4 proofs",
        "Stage": "Stage 1: Data Science Audit",
        "Status": "Ready to Send",
        "Next_Action": "Request open-science reproducibility audit from Steven Worthington",
        "Target_Date": "2026-11-21"
    }
]

def generate_csv():
    fieldnames = [
        "ID", "PI_Name", "Institution", "PI_Email", 
        "Lead_2Hop_Contact", "Lead_2Hop_Role_or_Email", "Domain", 
        "Anchor_Paper_2024_2026", "Code_Artifact", "Stage", 
        "Status", "Next_Action", "Target_Date"
    ]

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in RECORDS:
            writer.writerow(r)

    print(f"Successfully generated structured CRM campaign tracker: {CSV_PATH}")
    print(f"Total Logged Entities: {len(RECORDS)} PIs with mapped 2-Hop postdocs and action gates.")

if __name__ == "__main__":
    generate_csv()
