# ADR-002: Extraction Layer Priorities

**Date:** 2026-05-10
**Status:** Accepted
**Decision makers:** LLM Council (metadata blind spots session)

## Context

After building the initial structural metadata extractor, we needed to decide which semantic layers to add to maximize comprehension ROI.

## Decision

Prioritize extraction layers in this order:

1. Figure/table captions + in-text anchor sentences (what each proves)
2. Limitations & future work extraction
3. Cross-reference graph (sections/figures -> claims)
4. Citation density map (evidence-heavy vs novel content pages)

## Rationale

- **Figures first**: Technical papers concentrate their proof in visuals. Caption + anchor gives 10x more comprehension than section boundaries.
- **Limitations second**: The only question that failed our compression test was about limitations. Papers that acknowledge weaknesses are critical for informed discussion.
- **Cross-refs third**: Shows argument flow without requiring full semantic parsing.
- **Citation density fourth**: Cheap signal (regex) that distinguishes "background review" from "novel contribution" pages.

## What We Deferred

- Claim-evidence graphs (requires LLM inference, ~$5/paper)
- Evidence type taxonomy (empirical vs theoretical vs ablation)
- Section-level claim summaries
- Term disambiguation across sections

These are planned for layer 3 (LLM-augmented extraction) as an optional feature.
