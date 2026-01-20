# 废土小红帽 (Apocalyptic Little Red Riding Hood): Forensic Ludology Pilot Study

**Stage 2 Validation: Blind Replication of the Automated Archaeology Pipeline**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Project Status

This repository documents **work in progress**—a pilot study demonstrating the feasibility of computational analysis on undocumented Chinese indie RPGs. It is part of the **Forensic Ludology** research program described in my [PhD Portfolio](https://myouza.github.io/phd-portfolio/).

**What this is**: Stage 2 of a two-stage validation, testing whether extraction methodology transfers to an unfamiliar game.

**What this is not**: A finished research product with definitive interpretations.

---

## The Research Program: Forensic Ludology

### The Dark Archive

Between 2005 and 2015, Chinese indie communities—particularly 66rpg.com—produced thousands of RPG Maker games. These works represent a significant but ephemeral moment in Sinophone digital culture: amateur creators using accessible tools to produce narrative experiences that circulated within tight-knit online communities before vanishing as platforms closed.

Unlike commercial games preserved by industry archives, these works exist only as scattered downloads, forum posts, and degrading storage media. They constitute **cultural dark data**—artifacts with scholarly value that remain inaccessible, undocumented, and at risk of permanent loss.

The corpus is a treasure: a vast spectrum of creative expression spanning adapted folklore, historical fiction, philosophical explorations, personal narratives, genre experiments, and hybrid forms that resist easy categorization. My goal is to make this archive computationally accessible.

### The Three-Pillar Pipeline

My methodology proceeds through three integrated stages:

| Pillar | Description | Portfolio Work |
|--------|-------------|----------------|
| **Critical Theory → Hypothesis Generation** | Narratological frameworks generate testable hypotheses | [Critical Game Essay](https://myouza.github.io/phd-portfolio/), Poincaré Monograph |
| **Computational Linguistics → Formal Verification** | NLP tools with stability guarantees for safe interpretation | [Stability Analysis](https://myouza.github.io/phd-portfolio/) (Lipschitz bounds; ongoing refinement) |
| **Game Design → Research-Creation** | Verified findings translated into design knowledge | [Songs of Memory](https://myouza.github.io/phd-portfolio/) (300k-word narrative RPG; presentable build) |

This repository demonstrates **Pillar 2**: the Automated Archaeology pipeline that extracts structured, citable narrative data from game event logs.

---

## Two-Stage Validation Design

### Stage 1: Ground Truth Development (*Songs of Memory*)

**Game**: A 300,000-word narrative RPG I created over several years.

**Purpose**: Develop and calibrate the extraction methodology on a game with **known ground truth**—I know every branch, variable, and hidden ending.

**Status**: Presentable. See [portfolio](https://myouza.github.io/phd-portfolio/) for methodology and Game Design Document. Further expansion possible.

### Stage 2: Blind Replication (*废土小红帽*) — This Repository

**Game**: An undocumented RPG Maker game from the 66rpg.com community.

**Purpose**: Test whether the methodology **transfers** to an unknown game without modification.

**Key Claim**: I selected this game randomly and encountered it for the first time on the day of extraction. The same prompt developed in Stage 1 was applied without game-specific tuning.

### Why Two Stages?

| Stage | Known Ground Truth? | Tests What? |
|-------|---------------------|-------------|
| Stage 1 | Yes — I am the author | Extraction **accuracy** (recall/precision) |
| Stage 2 | No — first encounter | Extraction **transferability** (game-agnostic claim) |

Single-stage validation cannot establish both properties.

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXTRACTION PIPELINE                       │
└─────────────────────────────────────────────────────────────────┘

[RPG Maker Game]
       │
       ▼ (Data dump — see data/SOURCE.md)
[EventTextDump.txt]  ←── 84,123 lines of raw event commands
       │
       ▼ (LLM prompt — see src/prompts/)
[narrative_extraction.md]  ←── Arc → Sequence → Beat structure
       │
       ▼ (Python analysis — parameterized)
[Experiments 1-4]  ←── 26 figures, 8 tables, 4 metrics files

Time: ~15 seconds from extracted data to publication-ready outputs
```

---

## What This Repository Demonstrates

Four experiments test whether standard DH methods operate on the extracted data:

| Experiment | Validates | Result |
|------------|-----------|--------|
| Structural Alignment | Intertextual hypotheses are testable | ✓ Produces citable alignment scores |
| Narrative Density | Spatial metrics are calculable | ✓ Per-map statistics computable |
| Semantic Network | Co-occurrence analysis operates | ✓ Network methods work |
| Motif Evolution | Longitudinal tracking is feasible | ✓ Semantic drift measurable |

**The experiments demonstrate capability, not conclusion.** The specific findings are proof-of-concept values showing the data is "DH-ready"—citable, queryable, measurable, and comparable.

---

## Quick Start

```bash
git clone https://github.com/Myouza/grim-fairy-tale-dh-analysis.git
cd grim-fairy-tale-dh-analysis
pip install -r requirements.txt
python run_all_experiments.py
```

Generates in ~15 seconds: 26 figures, 8 tables, 4 metrics files.

---

## Future Directions

This pilot study opens several research paths I plan to pursue:

### Extraction Robustness
- More adaptive rule-based NLP extraction with explicit heuristics
- Variance analysis across multiple LLM runs (temperature=0, frozen model versions)
- Permutation tests: does the pipeline find "structure" in shuffled data?

### DH Method Alignment
- Design extraction schemas that align better with established DH workflows
- Integrate with existing digital humanities tool ecosystems
- Develop interoperability with corpus linguistics platforms

### Formal Verification
- Apply the [Stability Analysis](https://myouza.github.io/phd-portfolio/) framework to each pipeline stage
- Establish "safe interpretation zones" for extracted metrics
- Connect to the broader goal of mathematically verified distant reading

### Corpus Expansion
- Process 10+ additional games to establish extraction robustness
- Blind third-party validation (unfamiliar researcher runs pipeline)
- Build baseline statistics for "typical" metric values

### Scholarly Application
- Cross-game comparative analysis
- Genre and style clustering across the corpus
- Historical periodization of design conventions (2005-2015)

---

## Repository Structure

```
grim-fairy-tale-dh-analysis/
├── README.md                    # This file
├── CAVEATS.md                   # Interpretation guidelines
├── data/
│   ├── EventTextDump.txt        # Raw extracted event data
│   ├── narrative_extraction.md  # LLM-generated narrative structure
│   ├── SOURCE.md                # Data provenance and attribution
│   └── *.json                   # Reference data for experiments
├── src/
│   ├── prompts/                 # LLM prompts used in extraction
│   │   └── NarrativeExtraction_Prompt_v2.md
│   ├── parsers.py               # Data parsing utilities
│   ├── experiment_*.py          # Individual experiments
│   └── visualization.py         # Plotting utilities
├── outputs/                     # Generated figures, tables, metrics
├── notebooks/                   # Interactive exploration
└── docs/
    ├── methodology.md           # Two-stage validation design
    ├── validation_results.md    # What experiments demonstrate
    ├── pipeline_design.md       # Extraction architecture
    ├── research_context.md      # PhD research program context
    └── theoretical_foundations.md
```

---

## Connection to Other Work

This repository is one component of a broader research program:

| Project | Role in Pipeline | Status |
|---------|------------------|--------|
| **Stability Analysis** | Formal guarantees for NLP metrics | Documented ([portfolio](https://myouza.github.io/phd-portfolio/)); ongoing refinement |
| **Songs of Memory** | Ground truth corpus + research-creation | Presentable build ([portfolio](https://myouza.github.io/phd-portfolio/)); expansion possible |
| **This Repository** | Blind replication of extraction | Current work |
| **Corpus-scale analysis** | 50+ games, searchable database | Future work |

The goal is a complete pipeline from raw game binaries through mathematically verified metrics to cultural interpretation. Each component is at a stage where it can be presented and discussed, while remaining open to further development.

---

## Links

- **PhD Portfolio**: [https://myouza.github.io/phd-portfolio/](https://myouza.github.io/phd-portfolio/)
- **Stability Analysis**: Lipschitz bounds for Word Mover's Distance (portfolio)
- **Songs of Memory**: 300k-word narrative RPG and Game Design Document (portfolio)
- **JMM 2026 Presentation**: Fast Inverse Square Root optimization
- **Source Game**: [https://rpg.blue/thread-164657-1-1.html](https://rpg.blue/thread-164657-1-1.html)

## Author

**Xuanlin Zhu**  
B.S. Applied Mathematics & Computer Science, William & Mary  
xzhu09@wm.edu

---

## License

MIT License — see [LICENSE](LICENSE)

---

*This repository documents work in progress as part of PhD applications in Computational Media and Critical Game Design. The pipeline is the contribution; the findings are demonstrations.*
