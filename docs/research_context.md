# Research Context: Forensic Ludology Pilot Study

## Overview

This repository is part of **Forensic Ludology**—a research program applying computational methods to rescue and analyze undocumented video games from Chinese indie communities. It represents current work in progress, demonstrating the feasibility of the methodology before corpus-scale application.

**Current Phase**: Pilot validation (two games processed)  
**Next Phase**: Expanded validation and corpus infrastructure  
**Long-term Goal**: PhD-level research program

---

## The Dark Archive: Why This Matters

### A Moment in Digital Culture

Between 2005 and 2015, Chinese indie communities—particularly centered around 66rpg.com—produced thousands of RPG Maker games. This was a specific historical moment:

- **Before mobile dominance**: PC-based creation and distribution
- **Before Steam's Chinese expansion**: Local platforms, forum-based sharing
- **BBS culture era**: Tight-knit communities, hand-coded HTML walkthroughs, vernacular creativity

The platforms have largely vanished. The games exist only as scattered downloads, forum attachments, and degrading storage media.

### Cultural Significance

The corpus is a **treasure**—a vast spectrum of creative expression that resists easy categorization:

- Adapted folklore and mythology
- Historical fiction and period drama
- Philosophical and existentialist explorations
- Personal and autobiographical narratives
- Genre experiments and hybrid forms
- Cross-cultural adaptations and remixes

These works represent grassroots digital creativity in a specific cultural-historical context. They are evidence of how amateur creators negotiated between global game conventions, local literary traditions, and personal expression.

### The Problem

Unlike commercial games preserved by industry archives, these works constitute **cultural dark data**:

- Unsearchable (opaque binary files)
- Undocumented (no metadata, no academic citations)
- Inaccessible (platform closure, link rot)
- At risk of permanent loss

**My goal**: Transform this dark archive into computationally accessible datasets that enable scholarly inquiry.

---

## The Three-Pillar Pipeline

My research methodology integrates three domains:

### Pillar 1: Critical Theory → Hypothesis Generation

Narratological and media-theoretical frameworks generate testable hypotheses about the archive. Theory is not imposed externally but articulates intuitions arising from practice.

**Portfolio work**: 
- "For a New Kind of Game" (critical essay applying Bakhtin to RPG poetics)
- Poincaré Monograph (game engines as geometric conventions)

### Pillar 2: Computational Linguistics → Formal Verification

Rather than treating NLP tools as black boxes, I derive formal guarantees for when computational outputs are safe for humanistic interpretation.

**Portfolio work**:
- Stability Analysis (Lipschitz bounds for Word Mover's Distance)
- This repository (Automated Archaeology pipeline validation)

### Pillar 3: Game Design → Research-Creation

Verified findings are translated into design knowledge through playable prototypes and documentation frameworks.

**Portfolio work**:
- Songs of Memory (300,000-word narrative RPG)
- Game Design Document with Automated Archaeology methodology

---

## Validation Sequence

### Work To Date

| Stage | Game | Scale | Purpose | Status |
|-------|------|-------|---------|--------|
| 1 | *Songs of Memory* | 300,000 words | Ground truth development | Presentable; expansion possible |
| 2 | *小红帽* | 84,123 lines | Blind replication | Current work (this repo) |

### Stage 1: Ground Truth (*Songs of Memory*)

I created this game over several years. Because I am the author, every narrative element is known in advance—all branching paths, variable triggers, hidden content. The extraction prompt was developed and refined against this known ground truth.

When the extraction successfully captured the game's full complexity—including elements invisible to a player who hadn't explored exhaustively—the methodology was considered calibrated.

### Stage 2: Blind Replication (*小红帽*)

This game was selected randomly from the 66rpg.com corpus. I encountered it for the first time on the day of extraction. No game-specific modifications were made to the extraction prompt.

This tests **transferability**: Does a methodology developed on Game A work on Game B without modification?

### Why This Sequence?

- **Stage 1 alone** would raise concerns: "You tuned the prompt to your own game"
- **Stage 2 alone** would raise concerns: "How do you know the extraction is accurate?"
- **Together** they demonstrate: accuracy (Stage 1) AND transferability (Stage 2)

---

## Future Directions

This pilot study opens several research paths. Each addresses a question that strengthens the methodology:

### 1. Extraction Robustness

**Question**: How reliable is the LLM-based extraction across runs and models?

**Planned work**:
- Establish "frozen state" protocol: Temperature=0, documented model versions
- Variance analysis across multiple extraction runs
- Inter-coder reliability framing: treat LLM as "computational coder," measure agreement
- Develop more adaptive rule-based extraction with explicit, auditable heuristics

### 2. Null Model Validation

**Question**: Does the pipeline find "structure" in random data?

**Planned work**:
- Permutation tests on shuffled dialogue
- Random keyword baseline comparisons
- Define explicit failure conditions: What would "not working" look like?

### 3. DH Method Alignment

**Question**: Does the extraction schema align with established DH workflows?

**Planned work**:
- Design extraction outputs that integrate with existing corpus linguistics tools
- Align with standards from projects like HathiTrust, EEBO-TCP
- Develop interoperability with network analysis and topic modeling pipelines

### 4. Formal Verification Integration

**Question**: Can we establish "safe interpretation zones" for each pipeline stage?

**Planned work**:
- Apply Stability Analysis framework (Lipschitz bounds) to extracted metrics
- Derive interpretation rules before making humanistic claims
- Connect extraction confidence to downstream analysis validity

### 5. Corpus Expansion

**Question**: Does the methodology generalize beyond two games?

**Planned work**:
- Process 10+ additional games covering diverse genres and styles
- Blind third-party validation: unfamiliar researcher runs pipeline
- Establish baseline statistics for "typical" metric values across corpus

### 6. Accessibility and Documentation

**Question**: Can researchers without Ruby expertise use this pipeline?

**Planned work**:
- GUI encapsulation for Phase 1 (game data extraction)
- Comprehensive documentation for each pipeline stage
- Tutorial materials for digital humanities researchers

### 7. Scholarly Application

**Question**: What can we learn from the corpus once the infrastructure is in place?

**Planned work**:
- Cross-game comparative analysis (style, structure, theme)
- Historical periodization of design conventions (2005-2015)
- Genre and style clustering
- Tracing adaptation patterns and intertextual relationships

---

## Honest Limitations

This is a pilot study. I acknowledge what it does and does not demonstrate:

### What This Demonstrates

- Extraction is **feasible** (games can be transformed to structured data)
- Methods are **transferable** (prompt works on unseen games)
- Data is **tractable** (standard DH methods operate successfully)

### What This Does Not Demonstrate

- Statistical significance (requires corpus-scale data and null models)
- Interpretive certainty (findings are demonstrations, not conclusions)
- Complete automation (Phase 1 extraction requires technical knowledge)
- Scalability (N=2 validates the approach, not corpus-scale efficiency)

These are **expected limitations for a pilot study**—they define the research agenda rather than undermining it.

---

## Connection to PhD Research

This work demonstrates:

1. **Technical Capability**: Working extraction and analysis pipeline
2. **Methodological Awareness**: Two-stage validation with explicit design rationale
3. **Research Vision**: Clear path from pilot to corpus-scale scholarship
4. **Domain Expertise**: Combining CS/math background with humanities framing
5. **Linguistic Access**: Native Mandarin, Wu dialect fluency, JLPT N1 Japanese—enabling access to regional archives invisible to English-language scholarship

The contribution is not "here is what this game means" but "here is infrastructure that makes meaning-making possible at scale."

---

## Links

- **PhD Portfolio**: [https://myouza.github.io/phd-portfolio/](https://myouza.github.io/phd-portfolio/)
- **Stability Analysis**: Methodological note with proofs (portfolio)
- **Songs of Memory**: Game Design Document and research build (portfolio)
- **Critical Game Essay**: "For a New Kind of Game" (portfolio)
- **JMM 2026**: Fast Inverse Square Root presentation

---

## Contact

**Xuanlin Zhu**  
xzhu09@wm.edu  
GitHub: [Myouza](https://github.com/Myouza)
