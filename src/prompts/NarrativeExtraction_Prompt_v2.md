# Narrative Extraction Prompt for RPG Maker Event Dumps
## Version 2.0 — Hierarchical Summary with Source Citations

---

## Purpose

You are extracting narrative content from an RPG Maker event text dump. Your goal is to produce a **multi-level summary** of the game's story—like taking comprehensive notes on a book—where every claim can be traced back to its source location in the original file.

This is **Stage 1** of a computational game archaeology pipeline: extraction and organization, not interpretation.

---

## Core Principle: Hierarchical Narrative Tracking

Think of the game as a text to be summarized at multiple levels of granularity:

```
Level 1: MACRO     — Overall story arcs (章, 记, or thematic groupings)
Level 2: SEQUENCE  — Episodes/scenes within an arc (triggered event chains)
Level 3: BEAT      — Individual moments (a line of dialogue, a revelation, a choice)
```

Each level references the level below it. Each beat cites its exact source.

---

## Input Format

RPG Maker event dumps follow this general structure:

```
Map ID: [number]
Map Name: [name]
[map metadata]

Event ID: [number]
Event Name: [name]
(X,Y): ([coordinates])

Page #[n]
Conditions
[trigger conditions]

List of Event Commands:
@>[Command Type]: [parameters]
```

Key command types for narrative extraction:
- `@>Text:` — Dialogue (may include speaker tags like `\name[...]`)
- `@>Conditional Branch:` — Story branching based on variables/switches
- `@>Control Variables:` — State changes that track progression
- `@>Control Switches:` — Binary state flags
- `@>Change Party Member:` — Character joins/leaves
- `@>Transfer Player:` — Location changes
- `@>Battle Processing:` — Combat encounters
- `@>Play BGM:` / `@>Fade Out BGM:` — Music changes (note if name suggests mood/theme)
- `@>Change Items:` — Item acquisition
- `@>Call Common Event:` — Reusable event sequences

---

## Output Structure

---

### § 1. EXTRACTION SUMMARY

Begin with a brief overview:

```markdown
# [Game Title if identifiable]

## Overview
- **Total Maps with Narrative Content:** [count]
- **Identified Story Arcs:** [list arc names]
- **Major Characters:** [list]
- **Estimated Narrative Scope:** [brief assessment]

## Arc Registry
| Arc Identifier | Tracking Mechanism | Phases Identified | Primary Characters |
|----------------|-------------------|-------------------|-------------------|
| [name/ID] | Variable [XXXX] / Switch [XXXX] | [count or range] | [names] |
```

---

### § 2. NARRATIVE CHRONICLE

This is the core output. For each identified arc:

```markdown
# [Arc Name/Identifier]

**Tracking:** [Variable/Switch ID and name]
**Scope:** [Phase/Value range, e.g., "0 → 15"]
**Primary Locations:** [Map names]
**Primary Characters:** [Names]

---

## Sequence [N]: [Descriptive Title]

**Trigger:** [Conditions required — variable values, switches, party members, etc.]
**Location:** Map [ID]: [Name], Event [ID]: [Name], (X, Y)
**Source:** Lines [start]–[end]

### Summary
[2-5 sentence description of what happens in this sequence]

### Key Beats

1. **[Beat description]**
   > 「[Original dialogue in Chinese]」
   > — [Speaker]
   
   *Source: Line [N]*

2. **[Beat description]**
   > 「[Original dialogue]」
   > — [Speaker]
   
   *Source: Lines [N]–[M]*

3. **[Action/Event beat]**
   [Description: e.g., "Battle with [enemy]" / "[Character] joins the party" / "Player transferred to [location]"]
   
   *Source: Line [N]*

### State Changes
- `[Variable/Switch]`: [old value] → [new value]
- Party: [+/- Character]
- Items: [+/- Item]
- Location unlocked: [Map]

### Leads To
→ Sequence [N+1]: [Title] (when [condition])
→ Sequence [Alt]: [Title] (when [alternate condition])

---
```

Repeat for each sequence within the arc, then for each arc.

---

### § 3. CHARACTER REGISTRY

For each character who speaks or is narratively significant:

```markdown
## [Character Name]

**Identifier:** [How they're referenced: event name, \name tag, variable]
**First Appearance:** Map [ID], Event [ID] — [Arc] Sequence [N]
**Source:** Line [N]

### Role Summary
[1-3 sentences describing their narrative function]

### Arc Involvement
| Arc | Sequences | Role |
|-----|-----------|------|
| [Arc Name] | [Sequence numbers] | [Brief role description] |

### Sample Dialogue
> 「[Representative line in Chinese]」
> — [Context]
> *Source: Line [N]*
```

---

### § 4. LOCATION INDEX

```markdown
## [Map Name] (Map ID: [N])

**Narrative Density:** [High/Medium/Low — based on amount of story content]
**Connected To:** [List of maps reachable from here]
**BGM:** [If named, note the name — may indicate tone]

### Narrative Events Here
| Event ID | Event Name | Arc | Sequence | Brief Description |
|----------|------------|-----|----------|-------------------|
| [ID] | [Name] | [Arc] | [Seq #] | [1-line summary] |

*Sources: Lines [range]*
```

---

### § 5. BRANCHING & STATE LOGIC

Document narrative-affecting branches:

```markdown
## Branch: [Descriptive Name]

**Location:** Map [ID], Event [ID]
**Source:** Lines [N]–[M]

**Condition:** `[Variable/Switch] [operator] [value]`

**If True:**
- [What happens]
- Leads to: [Sequence/State]

**If False/Else:**
- [What happens]  
- Leads to: [Sequence/State]

**Narrative Impact:** [Why this branch matters to the story]
```

For complex state machines:

```markdown
## State Progression: [Arc Name]

**Variable:** [ID]: [Name]

| Value | State Description | Triggered By | Leads To |
|-------|------------------|--------------|----------|
| 0 | [Initial state] | [Game start / prior arc completion] | → 1 |
| 1 | [Description] | [Trigger] | → 2 or → 3 |
| 2 | [Description] | [Trigger from 1] | → 4 |
| ... | ... | ... | ... |

*Sources: [Line references for each transition]*
```

---

### § 6. DIALOGUE EXTRACTION

For complete preservation, extract all dialogue grouped by context:

```markdown
## [Arc Name] — [Sequence N] Dialogue

**Location:** Map [ID]: [Name], Event [ID]
**Trigger:** [Conditions]

| Line | Speaker | Dialogue | Notes |
|------|---------|----------|-------|
| [N] | [Name] | 「[Chinese text]」 | [Control codes, expression changes, etc.] |
| [N+1] | [Name] | 「[Chinese text]」 | |
| ... | ... | ... | ... |
```

---

### § 7. SUPPLEMENTARY ELEMENTS

#### Items with Narrative Significance

```markdown
| Item Name | Acquisition | Arc/Sequence | Narrative Role |
|-----------|-------------|--------------|----------------|
| [Name] | Map [ID] (X,Y), Line [N] | [Arc, Seq] | [Why it matters] |
```

#### Named Music Cues

```markdown
| BGM Name | First Used | Context | Suggested Mood |
|----------|------------|---------|----------------|
| [Name] | Map [ID], Line [N] | [Scene description] | [If name suggests meaning] |
```

#### Common Events with Narrative Function

```markdown
| Common Event Name | Called From | Narrative Purpose |
|-------------------|-------------|-------------------|
| [Name] | [Locations/Events] | [What story function it serves] |
```

---

### § 8. INFERENCE LOG

Document all inferences made during extraction:

```markdown
## Event Name Inferences

| Map | Event ID | Original Name | Inferred Purpose | Evidence |
|-----|----------|---------------|------------------|----------|
| [ID] | [ID] | [Generic name] | [Your inference] | [Why: commands present, context, etc.] |

## Structural Inferences

| Inference | Evidence | Confidence |
|-----------|----------|------------|
| [e.g., "Arc X must precede Arc Y"] | [Variable dependencies, etc.] | [High/Medium/Low] |

## Ambiguities & Gaps

| Location | Issue | Notes |
|----------|-------|-------|
| [Reference] | [What's unclear] | [Possible interpretations] |
```

---

## Extraction Guidelines

### What to Extract (Priority Order)

**Must Capture:**
1. All dialogue (`@>Text:`) with speaker identification
2. All story-tracking variable/switch changes and conditions
3. Party composition changes
4. Location transitions that advance narrative
5. Significant battles (named enemies, boss fights)

**Should Capture:**
6. Item acquisitions that seem plot-relevant
7. BGM changes with meaningful names
8. Animation/visual cues that mark emotional beats

**May Summarize:**
9. Movement choreography (unless narratively meaningful)
10. Technical scripting, waits, system calls

### Source Citation Format

Always cite sources so readers can locate content in the original:

```
Line [N]                    — Single line reference
Lines [N]–[M]               — Range reference  
Map [ID], Event [ID]        — Location reference
Map [ID], Event [ID], Line [N]  — Full reference
```

Line numbers refer to the original dump file.

### Handling Ambiguity

**Generic Event Names (EV001, EV002, etc.):**
- Infer purpose from commands present
- Document inference in the Inference Log
- Use descriptive names in your summary: "[Character] Encounter", "[Location] Transition", "[Item] Acquisition"

**Unclear Story Structure:**
- If arc boundaries are ambiguous, note this
- Group by tracking variable if possible
- Group by map/location if no clear variable tracking
- Mark uncertain groupings as provisional

**Incomplete or Corrupted Data:**
- Note gaps explicitly
- Do not fabricate content
- Mark sections as "[Incomplete]" if data is missing

### Language Handling

- **Dialogue:** Preserve exactly in original language within 「」
- **Structural documentation:** Write in English
- **Character/Location names:** Keep original, provide romanization if helpful
- **Control codes:** Note in parentheses if they affect meaning
  - `\s[n]` = expression/portrait change
  - `\|` = pause
  - `\p[n]` = portrait position
  - `\n[n]` = name variable reference
  - `\name[x]` = speaker name tag

---

## Extraction Process

1. **First Pass — Survey**
   - Identify all maps with narrative content
   - Identify all story-tracking variables and switches
   - List all speaking characters

2. **Second Pass — Structure**
   - Determine arc boundaries
   - Map variable value ranges to narrative phases
   - Identify sequence breaks within arcs

3. **Third Pass — Extract**
   - Work through each arc sequentially
   - Extract all beats with full citations
   - Document all state changes

4. **Fourth Pass — Cross-Reference**
   - Build character registry from extracted content
   - Build location index
   - Document branches and state logic

5. **Final Pass — Verify**
   - Check all citations are valid
   - Ensure no orphaned sequences
   - Log all inferences and ambiguities

---

## Output Verification Checklist

Before completing:

- [ ] All narrative-containing events are accounted for
- [ ] All speaking characters are in the registry
- [ ] All story-tracking variables are documented
- [ ] All dialogue preserved in original language with citations
- [ ] All state transitions have source references
- [ ] All inferences are logged with evidence
- [ ] Summary accurately reflects extracted content
- [ ] A reader unfamiliar with the game could follow the story

---

## Begin Extraction

Process the provided event dump following the five-pass method above. Produce a complete hierarchical summary where:

- **Level 1 (Arc)** gives the overall shape of each storyline
- **Level 2 (Sequence)** breaks down the episodes within each arc  
- **Level 3 (Beat)** preserves the specific moments with exact citations

The output should allow a researcher to understand the game's complete narrative without playing it, and to locate any specific moment in the original source file.
