# Current Work: 小红帽 Pilot Study
## Forensic Ludology — Stage 2 Validation

*Xuanlin Zhu*

---

# What I've Been Working On

**The short version:**

I took a random game from the 66rpg.com archive and ran my extraction pipeline on it — no tuning, no game-specific modifications.

It worked.

This slide deck walks through what that means.

---

# The Game: 小红帽 (Little Red Riding Hood)

- RPG Maker game from the 66rpg.com community
- ~84,000 lines of event data, 170 maps
- First encounter: the day I ran the experiment

**Why this game?**
- Random selection from the corpus
- Tests whether my pipeline transfers to unfamiliar content
- (Turns out it's surprisingly rich — post-apocalyptic military reframing of the fairy tale)

---

# Theoretical Touchstones

Two works frame what makes this game analytically interesting:

**Catherine Orenstein, *Little Red Riding Hood Uncloaked* (2002)**
- Traces the fairy tale's mutations across cultures and centuries
- The "Red Riding Hood" figure as a vessel for cultural anxieties

**Grigori Chukhrai, *Ballad of a Soldier* (1959)**
- Soviet anti-war film: soldier's brief leave, obligation-filled journey home
- Circular structure: departure → delays → brief reunion → return to war

The game remediates both — fairy tale iconography meets wartime leave narrative.

---

# Two-Stage Validation Design

```
┌─────────────────────────────────────────────────────────┐
│  STAGE 1: Songs of Memory (my own game)                │
│  ───────────────────────────────────────               │
│  • 300,000 words — I know every branch                 │
│  • Developed extraction prompt here                     │
│  • Can verify: did it capture what I know is there?    │
│  • Result: Prompt calibrated on known complexity       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 2: 小红帽 (random selection)        ← THIS REPO │
│  ───────────────────────────────────────               │
│  • First encounter on experiment day                   │
│  • Same prompt, zero modifications                     │
│  • Can verify: does it transfer to unknown content?    │
│  • Result: Yes — this slide deck                       │
└─────────────────────────────────────────────────────────┘
```

---

# The Pipeline

```
[RPG Maker .exe]
       │
       ▼ (Ruby script — one click)
[EventTextDump.txt]  ←── 84,123 lines of raw event commands
       │
       ▼ (LLM prompt — game-agnostic, no tuning)
[narrative_extraction.md]  ←── Arc → Sequence → Beat structure
       │
       ▼ (Python analysis — parameterized)
[Experiments 1-4]  ←── Figures, tables, metrics
```

**Key point:** The middle step (LLM extraction) uses the exact prompt from Stage 1.
No revision. It just worked.

---

# What I Wanted to Test

Four questions about the extracted data:

| Question | Experiment |
|----------|------------|
| Can we test intertextual hypotheses? | Structural Alignment |
| Can we calculate spatial metrics? | Narrative Density |
| Can we run network analysis? | Semantic Network |
| Can we track symbols over time? | Motif Evolution |

These are standard DH methods. The question is: do they work on this data?

---

# Experiment 1: Structural Alignment

**Hypothesis:** The game remediates *Ballad of a Soldier*

**Method:** Match narrative beats by structural type

**Result:** 76.9% correspondence (10 of 13 film beats have game equivalents)

![Timeline alignment showing beat correspondence]

**What this shows:** Intertextual hypotheses are now *testable* with citable locations.
(Not "proving" remediation — enabling the question.)

---

# Experiment 2: Narrative Density

**Question:** How does dialogue distribute across the game's geography?

**Method:** density = dialogue_commands / total_commands per map

**Result:** 162 maps analyzed
- 83.3% combat/traversal (< 0.3 density)
- 16.7% narrative hubs (0.3–0.7 density)

![Density heatmap]

**What this shows:** Spatial metrics are calculable. We can now ask "where does story happen?"

---

# Experiment 3: Semantic Network

**Question:** Can we build thematic networks from extracted dialogue?

**Method:** Co-occurrence of 35 keywords across 2,415 dialogue segments

**Result:** 28-node network, 4 detected communities

![Semantic network visualization]

**What this shows:** Network analysis operates. Keywords are parameterized — swap them for different questions.

---

# Experiment 4: Motif Evolution

**Question:** How do the symbol's associations change across the narrative?

**Method:** Track "小红帽" instances, score surrounding context by semantic field

**Result:** 380 instances tracked
- Military context: +21.9% over narrative arc
- Innocence context: -13.8%

![Context evolution chart]

**What this shows:** Longitudinal semantic tracking is feasible.

---

# The 15-Second Demo

```bash
$ python run_all_experiments.py

✓ Experiment 1 complete!
✓ Experiment 2 complete!
✓ Experiment 3 complete!
✓ Experiment 4 complete!

Duration: 13.6 seconds

Outputs Generated:
  • Figures: 26 files
  • Tables:  8 files
  • Metrics: 4 files
```

From raw dump to publication-ready outputs in under 15 seconds.

---

# What This Validates

| Property | Evidence |
|----------|----------|
| **Citable** | Every claim has Map/Event/Line location |
| **Queryable** | Keyword search returns results with counts |
| **Measurable** | Density, frequency, co-occurrence all calculable |
| **Comparable** | Same templates can run on other games |
| **Transferable** | Prompt from Stage 1 worked here without changes |

---

# What This Doesn't Claim

- That the specific findings are definitive
- That these keywords are the only valid ones
- That the numbers are statistically significant (need corpus for that)
- That I've "solved" the interpretation

**These are demonstration values** — proof the data is DH-ready.

---

# Immediate Next Steps

1. **Robustness:** Run a few more games to confirm transferability
2. **Null model:** Permutation test — does the pipeline find "structure" in shuffled data?
3. **Third-party test:** Have someone unfamiliar run the pipeline
4. **Integration:** Connect to Stability Analysis for formal metric verification

---

# The Bigger Picture

This is one piece of the Forensic Ludology pipeline:

```
[Dark Archive: thousands of games]
       │
       ▼
[Extraction: this pipeline]
       │
       ▼
[Verification: Stability Analysis bounds]
       │
       ▼
[Interpretation: DH methods with formal guarantees]
       │
       ▼
[Scholarship: corpus-scale cultural analysis]
```

We're at step 2. The pilot works. Now we scale.

---

# Questions?

**Repository:** github.com/Myouza/grim-fairy-tale-dh-analysis

**Portfolio:** myouza.github.io/phd-portfolio

---

*"The pipeline is the contribution. The findings are demonstrations."*
