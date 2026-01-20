# Pipeline Design: Extraction Architecture and Scalability

## Overview

This document explains why the extraction pipeline validated on one game transfers to thousands of others. The key insight: **RPG Maker enforces uniform data structures**, making game-to-game transfer an engineering task rather than a methodological reinvention.

---

## The 66rpg.com Corpus

### Historical Context

The 66rpg.com community (2005-2015) was the cradle of Sinophone indie game development—a decade of grassroots digital creativity before mobile dominance and Steam's Chinese expansion. The corpus is a treasure: thousands of games spanning an enormous range of creative expression.

### What's In The Archive

The games resist easy categorization. They include:

- Adapted folklore and mythology from multiple traditions
- Historical fiction spanning Chinese and world history
- Philosophical and existentialist explorations
- Personal and autobiographical narratives
- Genre experiments (horror, romance, comedy, drama)
- Hybrid forms mixing incompatible aesthetics
- Cross-cultural adaptations and remixes
- Meta-commentary on games and game-making

This diversity is precisely why computational methods are needed—no individual scholar can play through thousands of games, but a validated pipeline can extract and index them for targeted study.

### Why RPG Maker?

The community standardized on RPG Maker (primarily XP and VX Ace). This is fortunate for computational analysis: the engine enforces consistent data structures across all games, regardless of content.

---

## RPG Maker Data Uniformity

### Engine Architecture

RPG Maker games share a common architecture regardless of content:

```
Game.exe
├── Data/
│   ├── Map001.rxdata    # Map definitions
│   ├── Map002.rxdata
│   ├── ...
│   ├── CommonEvents.rxdata
│   └── System.rxdata
├── Graphics/
└── Audio/
```

All narrative content lives in the `.rxdata` files (Ruby serialized objects) or their equivalents in later versions (`.json` in MV/MZ).

### Event Command Syntax

Every RPG Maker version uses the same command structure:

```
[Command Code] [Parameters]
```

For example:
- `101`: Show Text
- `102`: Show Choices
- `111`: Conditional Branch
- `301`: Battle Processing

This **standardized command vocabulary** means parsers written for one game work on all games using the same engine version.

### Cross-Version Compatibility

| Version | Era | Data Format | Parser Complexity |
|---------|-----|-------------|-------------------|
| RPG Maker 2000/2003 | Early 2000s | LCF binary | Moderate |
| RPG Maker XP | Mid 2000s | Ruby Marshal | Low |
| RPG Maker VX/VX Ace | Late 2000s-2010s | Ruby Marshal | Low |
| RPG Maker MV/MZ | 2015+ | JSON | Trivial |

The 66rpg.com community primarily used XP and VX Ace, both of which use Ruby Marshal format—well-documented and easily parsed.

---

## Extraction Pipeline Components

### Stage 1: Data Dump

**Tool**: RPG Maker decryption utilities (widely available)

**Input**: Encrypted game archive
**Output**: Raw event data (text dump)

This stage is **fully automated** and version-specific tools exist for all major RPG Maker releases.

### Stage 2: Structural Parsing

**Tool**: `parsers.py` (this repository)

**Input**: Raw event dump
**Output**: Structured JSON/DataFrame with:
- Map hierarchy
- Event hierarchy
- Command classification
- Dialogue extraction with locations

This stage requires **minimal per-game customization**. The command vocabulary is fixed by the engine.

### Stage 3: Narrative Annotation (Optional)

**Tool**: Human annotation following schema

**Input**: Parsed event data
**Output**: Arc→Sequence→Beat hierarchy

This stage is **game-specific** but follows a consistent methodology. It can be:
- Skipped for purely computational analysis
- Automated via heuristics for large-scale survey
- Performed manually for deep case studies

### Stage 4: Analysis

**Tool**: Experiment modules (this repository)

**Input**: Parsed data + parameter files (keywords, reference beats)
**Output**: Metrics, visualizations, tables

This stage is **fully parameterized**. Same code, different inputs.

---

## Scaling Architecture

### Level 1: Manual Extraction (Current)

```
1 game → 1 researcher → Validated pipeline
```

Demonstrated in this repository.

### Level 2: Batch Extraction

```
10-50 games → Scripted pipeline → Comparative corpus
```

Requirements:
- Version detection (which RPG Maker?)
- Batch decryption
- Automated parsing
- Standardized output format

Technical effort: ~1 week engineering

### Level 3: Corpus-Scale Survey

```
1000+ games → Fully automated → Searchable archive
```

Requirements:
- Web scraping for game collection
- Automated version detection
- Error handling for corrupted/non-standard files
- Database for storing structured outputs
- Search interface

Technical effort: ~1-2 months engineering

---

## Why Not Other Engines?

The 66rpg.com community standardized on RPG Maker. However, the **methodology** (not the specific code) transfers to any engine with:

1. **Accessible data**: Game files can be extracted
2. **Documented format**: Command structure is known
3. **Text encoding**: Dialogue is stored as parseable text

| Engine | Accessibility | Format Documentation | Feasibility |
|--------|---------------|---------------------|-------------|
| RPG Maker (all) | High | Excellent | ✓ Demonstrated |
| Ren'Py | High | Excellent | ✓ Feasible |
| Unity (indie) | Moderate | Varies | Possible |
| Game Maker | Moderate | Good | Feasible |
| Custom engines | Low | Poor | Case-by-case |

The methodology adapts; the specific pipeline implements for a target engine family.

---

## Data Output Schema

### Standard Output Format

All extracted games produce:

```json
{
  "metadata": {
    "game_id": "string",
    "engine_version": "string",
    "extraction_date": "ISO-8601",
    "total_maps": "int",
    "total_events": "int",
    "total_dialogue_segments": "int"
  },
  "maps": [
    {
      "map_id": "int",
      "map_name": "string",
      "events": [...]
    }
  ],
  "dialogue_index": [
    {
      "text": "string",
      "map_id": "int",
      "event_id": "int",
      "command_index": "int",
      "speaker": "string (if detectable)"
    }
  ]
}
```

This standardized schema enables:
- Cross-game queries ("Find all dialogue mentioning X across corpus")
- Aggregate statistics ("Average dialogue density by game")
- Network analysis across games ("Character name co-occurrence patterns")

---

## Limitations and Edge Cases

### Known Challenges

| Challenge | Mitigation |
|-----------|------------|
| Encrypted archives | Use standard decryption tools (widely available) |
| Custom plugins | Parse base content; flag plugin commands as "custom" |
| Non-standard encoding | Detect encoding; fallback to binary preservation |
| Corrupted files | Log errors; continue with valid files |

### Out of Scope

| Case | Reason |
|------|--------|
| Real-time dialogue (no script) | No text to extract |
| Procedurally generated content | Content not in data files |
| DRM-protected commercial games | Legal/ethical concerns |

---

## Comparison to Related Work

### Digital Humanities Pipelines

| Project | Domain | Scale | This Work |
|---------|--------|-------|-----------|
| HathiTrust | Books | Millions | Established corpus |
| EEBO-TCP | Early modern texts | 60K+ | Established corpus |
| This pipeline | Indie RPGs | Thousands (potential) | Demonstrated on 1, scalable |

### Game Preservation

| Project | Focus | Approach |
|---------|-------|----------|
| Internet Archive | Playable preservation | Emulation |
| VGHF | Metadata cataloging | Documentation |
| This work | Narrative extraction | Data transformation |

The contribution is **transforming games into datasets**, not just preserving them as playable artifacts.

---

## Roadmap

### Current State (This Repository)

- [x] Extraction validated on complex case
- [x] Parser for RPG Maker XP/VX format
- [x] Analysis templates (density, network, motif, alignment)
- [x] Output schemas documented
- [x] Reproducible pipeline

### Next Phase

- [ ] Batch processing for 10-50 games
- [ ] Cross-game comparison metrics
- [ ] Baseline statistics for "typical" density, network properties
- [ ] Error handling for edge cases

### Future Vision

- [ ] Corpus-scale extraction (1000+ games)
- [ ] Searchable database interface
- [ ] Automated survey generation (per-game summaries)
- [ ] Community contribution workflow

---

## Conclusion

The extraction pipeline is **not game-specific**. RPG Maker's enforced data uniformity means:

1. Parsers transfer across games within the same engine version
2. Analysis templates are parameterized for reuse
3. Scaling is an engineering task, not a methodological one

This single-game validation proves feasibility. Corpus-scale application is the next step.

---

## Connection to Research Program

This pipeline is one component of the **Forensic Ludology** methodology:

| Component | Role | Status |
|-----------|------|--------|
| Stability Analysis | Formal guarantees for NLP metrics | Documented ([portfolio](https://myouza.github.io/phd-portfolio/)); ongoing refinement |
| Automated Archaeology | Extraction from event logs | Validated (this repo) |
| Songs of Memory | Ground truth corpus | Presentable build ([portfolio](https://myouza.github.io/phd-portfolio/)) |
| Corpus infrastructure | Scaled extraction + database | Future work |

The goal is a unified pipeline from raw game binaries through mathematically verified metrics to cultural interpretation. Each component is at a stage where it can be presented, while remaining open to further development.

---

## Links

- **PhD Portfolio**: [https://myouza.github.io/phd-portfolio/](https://myouza.github.io/phd-portfolio/)
- **Research Context**: [`docs/research_context.md`](research_context.md)
