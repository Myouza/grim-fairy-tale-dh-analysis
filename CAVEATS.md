# Interpretation Caveats

## About This Repository

This repository documents **work in progress**—a pilot study demonstrating the feasibility of computational analysis on undocumented Chinese indie RPGs. All figures, tables, and metrics are **demonstration analyses** showing that standard digital humanities methods operate on extracted game data.

### Two-Stage Validation Context

This is **Stage 2** of a two-stage validation:

| Stage | Game | Purpose |
|-------|------|---------|
| Stage 1 | *Songs of Memory* (author-created) | Develop extraction on known ground truth |
| Stage 2 | *小红帽* (randomly selected) | Test transferability to unknown game |

The extraction prompt was developed in Stage 1 and applied here without modification. See [`docs/research_context.md`](docs/research_context.md) for details.

---

## Key Caveats

### 1. These Are Demonstration Values

The experiments show the pipeline **works**, not that the specific findings are definitive:

| Metric | What It Demonstrates | What It Does NOT Prove |
|--------|---------------------|------------------------|
| 76.9% alignment | Hypothesis testing is possible | That remediation occurred |
| +21.9% military shift | Semantic tracking is feasible | Authorial intent |
| 4 communities | Network analysis operates | "True" thematic structure |

### 2. Parameters Are Configurable

All analysis parameters are researcher choices, not discoveries:

- **Keywords**: Any set can be substituted
- **Reference texts**: Any film/novel can serve as comparand
- **Thresholds**: Classification boundaries are adjustable
- **Semantic fields**: Any taxonomy can replace the current one

The current values are **proof-of-concept choices**. Different parameters produce different results—this is a feature (flexibility), not a bug.

### 3. We Analyze Code, Not Experience

The dataset represents **authored potentiality**—the narrative space the developer created. It does not capture:

- How players actually traverse the game
- Which branches players choose
- Emotional responses to content
- Cultural reception in original context

This is **Code Archaeology**, not Reception Studies. Both are valid scholarly approaches; this project claims only the former.

### 4. Pilot Study Limitations

| Limitation | Status | Future Work |
|------------|--------|-------------|
| N=2 validation | Acknowledged | Expand to 10+ games |
| No null model | Acknowledged | Permutation tests planned |
| LLM variance | Acknowledged | Frozen model protocol |
| No significance tests | Acknowledged | Requires corpus-scale data |

These are expected for a pilot study and define the research agenda.

---

## How to Read These Outputs

### Figures
Each figure demonstrates that **visualization of this type is possible** with extracted data. Patterns shown are starting points for interpretation, not conclusions.

### Tables
Each table demonstrates that **structured data export works**. Values are queryable data points, not definitive facts.

### Metrics
Each metric demonstrates that **quantitative measurement is feasible**. Numbers are baseline measurements for future comparison, not standalone findings.

---

## Recommended Citation Practice

When citing outputs from this repository:

✓ **Do say**: "The extraction pipeline enables alignment scoring; for example, testing a *Ballad of a Soldier* hypothesis yields 76.9% correspondence (Zhu, 2026)."

✗ **Don't say**: "This game has 76.9% alignment with *Ballad of a Soldier*, proving systematic remediation (Zhu, 2026)."

The pipeline enables claims; the outputs demonstrate feasibility.

---

## Questions These Outputs Address

✓ "Is keyword search possible on this data?"  
✓ "Can we calculate spatial metrics?"  
✓ "Do network methods work?"  
✓ "Is longitudinal tracking feasible?"  

## Questions Requiring Future Work

✗ "What does this game really mean?" → Requires interpretation beyond metrics  
✗ "Is the author's intent X?" → Requires biographical/historical research  
✗ "How did players experience this?" → Requires reception study  
✗ "Are these patterns typical?" → Requires corpus comparison  
✗ "Is this statistically significant?" → Requires null models and larger N  

---

## Summary

**This is a pilot study demonstrating feasibility.**

The contribution is the pipeline—showing that undocumented games can be transformed into citable, queryable, measurable datasets. The specific findings are demonstrations of capability, not settled interpretations.

Future work will address robustness, null models, formal verification, and corpus-scale analysis. See [`docs/research_context.md`](docs/research_context.md) for the full research roadmap.
