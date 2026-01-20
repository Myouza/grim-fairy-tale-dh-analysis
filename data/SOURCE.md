# Data Source Attribution

## Original Game

**Title**: 废土小红帽 (Apocalyptic Little Red Riding Hood) 

**Source**: [https://rpg.blue/thread-164657-1-1.html](https://rpg.blue/thread-164657-1-1.html)

**Platform**: RPG Maker

**Community**: Originally from 66rpg.com (now rpg.blue / project.blue)

## Research Use

This repository analyzes the game for academic research purposes (criticism, commentary, and scholarship). The extracted event data (`EventTextDump.txt`) can be verified against the original game project available at the source link above.

## Acknowledgment

We acknowledge the original creator's work. This analysis is conducted in the spirit of preserving and studying the cultural artifacts of the Chinese indie RPG Maker community.

## Extraction Method

The pipeline has two extraction stages:

1. **Event Dump**: The raw event data was extracted from the game's data files. The dump file can be verified against the original game project.

2. **Narrative Extraction**: The structured narrative summary (`narrative_extraction.md`) was generated using the LLM prompt documented in [`src/prompts/NarrativeExtraction_Prompt_v2.md`](../src/prompts/NarrativeExtraction_Prompt_v2.md).

The analysis scripts in `src/` operate on the raw dump data, not the LLM-generated extraction. This ensures the quantitative analysis is independent of any potential LLM artifacts.
