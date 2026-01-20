# Validation Results

## Executive Summary

Four experiments confirm that the extracted dataset supports standard digital humanities methods. The data is **citable**, **queryable**, **measurable**, and **comparable**.

| Experiment | Validation Question | Result |
|------------|---------------------|--------|
| Structural Alignment | Can we test intertextual hypotheses? | ✓ Hypotheses produce citable scores |
| Narrative Density | Can we calculate spatial metrics? | ✓ Per-map statistics are computable |
| Semantic Network | Can we build co-occurrence networks? | ✓ Network analysis operates successfully |
| Motif Evolution | Can we track semantic change over structure? | ✓ Longitudinal patterns are measurable |

**Bottom line**: The extraction pipeline transforms this game from opaque binary to scholarship-ready dataset.

---

## Experiment 1: Structural Alignment

### Validation Outcome

**Demonstrated**: Intertextual hypotheses are testable with citable evidence.

### Test Case

Hypothesis: "This game systematically remediates *Ballad of a Soldier* (1959)"

### Metrics Produced

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Alignment score | 76.9% | 10 of 13 film beats have structural correspondents |
| Direct transpositions | 4 | Content AND structure match |
| Structural homologies | 6 | Structure matches, content transforms |

### What This Enables

- **Comparative testing**: The same method can test other hypotheses (e.g., *Grave of the Fireflies*, *Pan's Labyrinth*, fairy tale variants)
- **Citable argumentation**: Claims reference specific locations (Map 47, Event 12)
- **Quantified comparison**: Future studies can compare alignment scores across game-film pairs

### Sample Output

The alignment produces a table like:

| Beat Type | Film Location | Game Location | Match Type |
|-----------|---------------|---------------|------------|
| heroic_act | 00:03:20 | Arc 1, Seq 1.1 | Direct |
| obligation | 00:18:30 | Arc 1, Seq 1.2 | Structural |

This format supports scholarly citation and cross-study comparison.

---

## Experiment 2: Narrative Density Mapping

### Validation Outcome

**Demonstrated**: Spatial distribution metrics are calculable across the game's geography.

### Metrics Produced

| Metric | Value |
|--------|-------|
| Maps analyzed | 162 |
| Mean density | 0.154 |
| Median density | 0.089 |
| Story-heavy (>0.7) | 0 (0.0%) |
| Mixed (0.3-0.7) | 27 (16.7%) |
| Combat/Traversal (<0.3) | 135 (83.3%) |

### What This Enables

- **Spatial queries**: "Which maps have highest dialogue concentration?"
- **Comparative metrics**: Density distributions can compare across games
- **Design analysis**: Patterns reveal authorial choices about story-space relationships

### Interpretive Note

The 83% combat/traversal classification is a **description of authorial design**, not a claim about player experience. Whether players visit these maps, and in what order, requires separate study.

### Alternative Formulations

The density metric could be refined:
- Dialogue word count instead of command count
- Unique speaker count per map
- Quest-level aggregation instead of map-level

The pipeline supports any such reformulation—data structure enables method flexibility.

---

## Experiment 3: Semantic Network Analysis

### Validation Outcome

**Demonstrated**: Co-occurrence analysis operates successfully on extracted dialogue.

### Metrics Produced

| Metric | Value |
|--------|-------|
| Dialogue segments | 2,415 |
| Co-occurrence pairs | 160 |
| Network nodes | 28 |
| Network edges | 99 |
| Density | 0.262 |
| Avg clustering | 0.537 |
| Communities | 4 |

### What This Enables

- **Keyword flexibility**: Any keyword set can be substituted (characters, themes, objects, locations)
- **Network metrics**: Standard measures (centrality, clustering, community) are computable
- **Visualization**: Force-directed layouts reveal thematic clustering

### Parameterization

The current analysis uses 20 entities and 15 themes. These are **demonstration parameters**, not claims about the game's "true" thematic structure. A researcher interested in different concepts can substitute their own keyword set and re-run.

### Sample Query

"Which characters co-occur with '血' (blood)?"
→ The dataset supports this query, returning counts and locations.

---

## Experiment 4: Motif Evolution Tracking

### Validation Outcome

**Demonstrated**: Longitudinal semantic tracking is feasible across narrative structure.

### Metrics Produced

| Metric | Value |
|--------|-------|
| Motif instances | 380 |
| Arcs tracked | 5 |
| Innocence shift | -13.8% |
| Military shift | +21.9% |
| Posthuman shift | -2.4% |

### What This Enables

- **Diachronic analysis**: How do associations change across the narrative?
- **Symbol tracking**: Any term can serve as the tracked motif
- **Context flexibility**: Semantic fields are researcher-defined parameters

### Interpretive Caution

The +21.9% military shift means: "Instances of '小红帽' in later arcs more frequently co-occur with military keywords than instances in earlier arcs."

This is a **descriptive statistic**, not a claim about authorial intent or reader interpretation. The value is that such questions are now **answerable with data**.

### Semantic Field Parameterization

Current fields:
- **Innocence**: 外婆, 罐头, 家, 想你, 梦见, etc.
- **Military**: 团长, 战斗, 狼人, 士兵, 命令, etc.
- **Posthuman**: 血, 病毒, 基因, 吸血鬼, 感染, etc.

Alternative fields could include:
- Spatial terms (indoor/outdoor, safe/dangerous)
- Emotional terms (fear, hope, grief)
- Sensory terms (visual, auditory, tactile)

The pipeline is agnostic to keyword content.

---

## Cross-Experiment Synthesis

### Data Properties Confirmed

| Property | Evidence |
|----------|----------|
| **Citable** | All experiments output location metadata (Map/Event/Line) |
| **Queryable** | Keyword searches return relevant segments with counts |
| **Measurable** | Density, frequency, co-occurrence, alignment scores all calculable |
| **Comparable** | Templates designed for cross-game application |

### Pipeline Validated For

| Task | Feasibility |
|------|-------------|
| Intertextual hypothesis testing | ✓ Demonstrated |
| Spatial narrative analysis | ✓ Demonstrated |
| Thematic network construction | ✓ Demonstrated |
| Symbol/motif tracking | ✓ Demonstrated |
| Dialogue search | ✓ Demonstrated |
| Character registry | ✓ Demonstrated |

### Ready for Scaling

The validation confirms readiness for:

1. **Corpus expansion**: Same extraction on 10-50 additional games
2. **Comparative analysis**: Cross-game metrics using identical templates
3. **Community contribution**: Documented pipeline enables other researchers

---

## Limitations Acknowledged

### What This Study Does NOT Demonstrate

| Limitation | Explanation |
|------------|-------------|
| Player experience | We analyze authored content, not reception |
| Statistical significance | Heuristics, not hypothesis tests (requires corpus) |
| Interpretive certainty | Metrics enable debate, not resolve it |
| Corpus generalizability | N=1 validates pipeline, not population claims |

### What This Study DOES Demonstrate

| Capability | Explanation |
|------------|-------------|
| Extraction feasibility | RPG Maker data can be structured |
| Method compatibility | Standard DH methods operate successfully |
| Citation infrastructure | Claims can reference precise locations |
| Scaling potential | Uniform engine → transferable pipeline |

---

## Conclusion

The extracted dataset passes all validation tests. The game formerly existed as an opaque binary searchable only through play. It now exists as a structured dataset supporting:

- Keyword search with location results
- Quantitative metrics (density, frequency, co-occurrence)
- Network analysis and visualization
- Longitudinal semantic tracking
- Intertextual comparison

**The data is DH-ready.** Interpretation can now proceed with the infrastructure necessary for rigorous, citable scholarship.

---

## Next Steps

This validation enables the following research directions:

1. **Corpus expansion**: Apply the same pipeline to 10+ additional games
2. **Robustness testing**: Variance analysis, permutation tests, null models
3. **Formal verification**: Integrate Stability Analysis bounds for each metric
4. **Scholarly application**: Cross-game comparison once corpus is established

See [`research_context.md`](research_context.md) for the full research roadmap.

---

## Links

- **PhD Portfolio**: [https://myouza.github.io/phd-portfolio/](https://myouza.github.io/phd-portfolio/)
- **Stability Analysis**: Lipschitz bounds for semantic metrics (portfolio)
- **Songs of Memory**: Stage 1 ground truth validation (portfolio)
