# Methodology: Data Validation Framework

## Purpose

This document explains the **validation logic** behind each experiment. The goal is not to prove interpretive claims about the game, but to demonstrate that the extracted dataset supports standard digital humanities methods.

Each experiment answers a **tractability question**: "Can we do X with this data?"

---

## Two-Stage Validation Design

This repository represents **Stage 2** of a two-stage validation sequence. Understanding this sequence is essential for evaluating the methodology's rigor.

### Stage 1: Ground Truth Development (*Songs of Memory*)

**Game**: *Songs of Memory* (雨后的声音) — a 300,000-word narrative RPG created by the researcher.

**Purpose**: Develop and calibrate the extraction methodology on a game with **known ground truth**.

**Validation Logic**: Because the researcher authored the game, every narrative branch, variable trigger, and hidden ending is known in advance. The extraction prompt was developed and refined until it successfully captured this known complexity.

**Outcome**: A game-agnostic extraction prompt validated against verifiable ground truth.

**Documentation**: See the [PhD Portfolio](https://myouza.github.io/phd-portfolio/) and the *Songs of Memory* Game Design Document for Stage 1 methodology and results.

### Stage 2: Blind Replication (*小红帽*)

**Game**: *小红帽* (Little Red Riding Hood) — an undocumented RPG Maker game from the 66rpg.com community.

**Purpose**: Test whether the methodology **transfers** to an unknown game without modification.

**Validation Logic**: The researcher selected this game randomly from the corpus and encountered it for the first time on the day of extraction. No game-specific prompt tuning was performed. The same extraction methodology developed in Stage 1 was applied without modification.

**Outcome**: This repository — demonstrating that the prompt transfers to unfamiliar content.

### Why Two Stages?

| Stage | Known Ground Truth? | Tests What? |
|-------|---------------------|-------------|
| Stage 1 (Songs of Memory) | Yes — researcher is author | Extraction **accuracy** (recall/precision) |
| Stage 2 (小红帽) | No — first encounter | Extraction **transferability** (game-agnostic claim) |

Single-stage validation cannot establish both properties. Stage 1 alone would raise "overfitting to your own game" concerns. Stage 2 alone would raise "how do you know the extraction is correct?" concerns. Together, they provide complementary evidence.

### Independence Claim

The extraction prompt was developed **before** encountering *小红帽*. This repository does not demonstrate prompt engineering for a specific game—it demonstrates that a pre-existing methodology applies to arbitrary RPG Maker content.

---

## Data Extraction Pipeline

### Source Material

| File | Lines | Content |
|------|-------|---------|
| `EventTextDump.txt` | 84,123 | Raw RPG Maker event commands |
| `narrative_extraction.md` | 1,503 | Human-annotated Arc→Sequence→Beat structure |

### Extraction Properties

The extraction preserves **citability**—every data point traces to a precise location:

```
Map ID → Event ID → Command Index → Line Number
```

This is analogous to folio/line citation in manuscript studies. Any claim about the data can be verified against the source.

### Parser Architecture

**EventDumpParser** processes raw event logs:
- Recognizes RPG Maker command syntax
- Classifies command types (Text, Battle, Logic, Navigation, Visual/Audio)
- Preserves map/event hierarchy
- Extracts dialogue with full location metadata

**NarrativeExtractionParser** processes annotated structure:
- Parses Arc→Sequence→Beat hierarchy
- Links beats to source locations
- Builds character registry

Both parsers are **deterministic**—identical inputs produce identical outputs.

---

## Experiment Design Principles

### 1. Validation, Not Discovery

Each experiment tests whether a **reasonable DH method** operates on the data. The specific findings are demonstrations of capability:

| Experiment | Tests Whether... |
|------------|------------------|
| Structural Alignment | Hypotheses about intertextual relationships are testable |
| Narrative Density | Spatial distribution metrics are calculable |
| Semantic Network | Co-occurrence analysis produces coherent results |
| Motif Evolution | Longitudinal semantic tracking is feasible |

### 2. Parameterized Analysis

Experiments accept **configurable inputs** (keywords, reference beats, thresholds). This demonstrates the data's flexibility:

- Experiment 1: Any film/text can serve as comparison reference
- Experiment 3: Any keyword set can define the network
- Experiment 4: Any semantic fields can track motif evolution

The specific parameters used are **proof-of-concept choices**, not claims about the only valid analysis.

### 3. Reproducibility

All experiments are:
- **Deterministic**: Same inputs → same outputs (except Louvain community detection, which is robust to partition variation)
- **Documented**: Parameters recorded in output JSON
- **Executable**: `python run_all_experiments.py` regenerates all outputs

---

## Experiment 1: Structural Alignment

### Validation Question

> Can we formally test hypotheses about the game's relationship to external texts?

### Method

1. Define reference beats from comparison text (*Ballad of a Soldier*)
2. Define game beats from extracted narrative structure
3. Match by structural type (heroic_act, obligation, reunion, etc.)
4. Calculate alignment score = matched / total

### What This Demonstrates

- The extraction provides **citable beat locations** (Map 47, Event 12)
- Intertextual hypotheses become **testable propositions**
- Different reference texts can be substituted

### Limitations Acknowledged

- Beat selection involves interpretive judgment
- The score is a **heuristic for comparison**, not proof of remediation
- Value emerges from comparative application across multiple works/hypotheses

---

## Experiment 2: Narrative Density Mapping

### Validation Question

> Can we calculate spatial metrics from the extracted data?

### Method

1. Count commands by type for each map
2. Calculate density = dialogue_commands / total_commands
3. Classify maps by density threshold
4. Visualize distribution

### What This Demonstrates

- Command-type classification is **automatable**
- Per-map statistics are **calculable**
- Spatial distribution patterns are **visualizable**

### Limitations Acknowledged

- "Narrative density" is a novel metric requiring further validation
- Alternative formulations possible (e.g., dialogue length, unique speakers)
- The metric measures **authorial design**, not player experience

---

## Experiment 3: Semantic Network Analysis

### Validation Question

> Can we build co-occurrence networks from extracted dialogue?

### Method

1. Define keyword sets (entities, themes)
2. Extract all dialogue containing keywords
3. Build co-occurrence matrix (pairs in same segment)
4. Construct network, apply community detection

### What This Demonstrates

- Dialogue is **searchable** by keyword
- Co-occurrence is **countable**
- Network analysis methods **operate successfully**

### Limitations Acknowledged

- Keywords are researcher-selected (parameterized, not discovered)
- Results change with different keyword sets (this is a feature, not a bug)
- Network structure is descriptive, not explanatory

---

## Experiment 4: Motif Evolution Tracking

### Validation Question

> Can we track semantic change across narrative structure?

### Method

1. Define semantic fields (innocence, military, posthuman keywords)
2. Extract all instances of target motif (小红帽)
3. Score each instance by surrounding context
4. Aggregate by narrative arc, calculate distribution shifts

### What This Demonstrates

- Motif instances are **extractable with locations**
- Context scoring is **calculable**
- Longitudinal patterns are **measurable**

### Limitations Acknowledged

- Semantic fields are researcher-defined
- Context scoring uses proximity, not deep semantics
- Shift percentages are **descriptive statistics**, not significance tests

---

## Addressing Anticipated Critiques

### "The findings are circular—you found what you looked for"

**Response**: Correct, and intentional. These experiments demonstrate that **looking is now possible**. Previously, testing whether *Ballad of a Soldier* influenced this game required playing through entirely and relying on memory. Now it's a queryable operation with citable outputs.

### "N=1 doesn't generalize"

**Response**: This is **pipeline validation**, not corpus analysis. The two-stage design (Stage 1: Songs of Memory, Stage 2: 小红帽) establishes both accuracy and transferability. RPG Maker's uniform data structures mean the extraction step transfers directly. Scaling to 50+ games is an engineering task, not a methodological one.

### "No statistical significance"

**Response**: These are **heuristic metrics for comparison**. Significance testing requires corpus-scale data and null models—planned future work. The current goal is demonstrating measurability, not establishing population parameters.

### "You're analyzing the script, not the experience"

**Response**: Explicitly so. This is **Code Archaeology**—documenting the narrative potentiality encoded by the author. Reception studies require different methods (player interviews, playthroughs). Both are valid; we claim only the former.

---

## Connection to Stability Analysis

This pipeline is designed to integrate with the formal verification framework developed in the [Stability Analysis](https://myouza.github.io/phd-portfolio/) project. That work establishes Lipschitz bounds for Word Mover's Distance, providing a "safe interpretation zone" where measured semantic distances exceed model noise.

**Future integration**: Each experiment's metrics can be validated against stability bounds before humanistic interpretation. The goal is a complete pipeline where every computational claim has formal backing.

---

## Future Directions

This methodology opens several research paths:

### More Robust Extraction
- Adaptive rule-based NLP with explicit, auditable heuristics
- Variance analysis across multiple LLM runs
- "Frozen state" protocol (temperature=0, documented model versions)

### Null Model Validation
- Permutation tests on shuffled data
- Random keyword baseline comparisons
- Explicit failure condition definitions

### Formal Verification Integration
- Apply Stability Analysis bounds to each pipeline stage
- Establish interpretation rules before humanistic claims
- Connect extraction confidence to downstream validity

### DH Method Alignment
- Design extraction schemas for existing DH tool ecosystems
- Develop interoperability with corpus linguistics platforms
- Align with standards from established digital humanities projects

---

## Summary

| Property | Validation Method |
|----------|-------------------|
| **Citable** | All outputs include Map/Event/Line locations |
| **Queryable** | Keyword search operates on dialogue corpus |
| **Measurable** | Density, frequency, co-occurrence are calculable |
| **Comparable** | Same templates can run on other games |

The experiments prove the extracted data is **DH-ready**. Interpretation is enabled, not concluded.
