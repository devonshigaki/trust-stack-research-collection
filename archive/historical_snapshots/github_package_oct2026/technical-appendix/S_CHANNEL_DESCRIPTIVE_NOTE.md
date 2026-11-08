# S-Channel Lexical Geometry — Descriptive Supplement (NOT part of any pre-registered battery)

**Status: descriptive/exploratory only.** Nothing on this page is an inferential
test, and nothing here modifies any frozen criterion, battery outcome, or paper
claim. The pre-registered S-channel battery result stands exactly as reported
in DOCAS (0/15 under the ≥3-family filter, p = 1.0). This note documents the
raw CLICS 4.0 structure around the frozen concept set so readers can see
*why* the null is a property of lexical organization rather than a pipeline
artifact. Computed 2026-09-11 from the deposited CLICS 4.0 copy
(`clics4-main/cldf`, 1,449,893 forms, 3,447 varieties; `clics_graph/colexifications.csv`,
51,562 edges).

## 1. The frozen S-cluster, all 15 pairs (verification of the reported 0/15)

Frozen concept set: {REST, SLEEP, CALM, PEACE, QUIET, STABLE} (the paper's
Stabilization/serotonin channel concepts).

| Pair | families | languages | ≥3-family filter |
|---|---|---|---|
| REST–SLEEP | 1 | 1 | no |
| REST–CALM | 0 | 0 | no |
| REST–PEACE | 2 | 3 | no |
| REST–QUIET | 0 | 0 | no |
| REST–STABLE | 0 | 0 | no |
| SLEEP–CALM | 0 | 0 | no |
| SLEEP–PEACE | 0 | 0 | no |
| SLEEP–QUIET | 1 | 1 | no |
| SLEEP–STABLE | 0 | 0 | no |
| CALM–PEACE | 0 | 0 | no |
| CALM–QUIET | 0 | 0 | no |
| CALM–STABLE | 0 | 0 | no |
| PEACE–QUIET | 0 | 0 | no |
| PEACE–STABLE | 0 | 0 | no |
| QUIET–STABLE | 0 | 0 | no |

Reproduces the paper's 0/15 exactly. Twelve pairs have no attested
colexification anywhere in the database.

## 2. Concept coverage (why "every language has these words" and the null are both true)

| Concept | varieties with a form | language families |
|---|---|---|
| SLEEP | 3,315 / 3,447 | 243 |
| REST | 665 / 3,447 | 75 |

The concepts are near-universal (SLEEP especially; REST's lower count largely
reflects wordlist coverage). Colexification — one word-form covering *both* —
is a separate, much rarer event. The single attested SLEEP–REST colexification
is Manange (Sino-Tibetan; Eurasia), form *4nu* — 1 variety of 3,315.

## 3. Where the geometry actually is (strongest real partners per concept)

- **SLEEP** (269 partners): LIE DOWN (35 families), DREAM (9), LIE/REST (7),
  SLEEP-STATE (5), BED (4) — a night/posture/dream field.
- **QUIET** (157 partners): SLOW (7), BE SILENT (6), SOFT (2), WEAK (2) — a
  low-intensity field.
- **REST** (47 partners): BREATHE (7), CEASE (4), LIE DOWN (3), BREATH (3) —
  a cessation/breath field.
- **PEACE** (29 partners): SILENCE (5), WORLD (4) — a silence/order field.
- **STABLE** (42 partners): FENCE (5), PRISON (3) — a physical-fixity field
  (polysemy-dominated).
- **CALM**: 0 colexification partners in CLICS 4.0.

The six concepts are richly connected — to *different* fields organized along
ecological/embodiment axes (night, posture, silence, slowness, cessation), not
along the neuromodulatory channel the frozen set encodes. Positive control in
the same database: the paper's Recognition-field edges (e.g., HEAR–UNDERSTAND
29 families; SEE–FIND 25 families) — the graph and pipeline detect attractors
where they exist.

## 4. Figure

`figures/figS_channel_descriptive.png` — (a) the 15 frozen pairs against the
≥3-family filter; (b) the strongest attested partners of each S concept.

## 5. Guardrails

- Descriptive only; no p-values computed here; no new claims enter any paper.
- Any *new* test suggested by these observations (e.g., graded
  colexification-probability models, within-family analyses, embedding-based
  semantic-similarity comparisons) would require its own pre-registration
  before touching data.
