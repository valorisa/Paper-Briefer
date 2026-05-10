# ADR-001: Repo Positioning — "paper-briefer" (Option C)

**Date:** 2026-05-10
**Status:** Accepted
**Decision makers:** LLM Council (5 advisors + peer review + chairman)

## Context

Three positioning options were evaluated for this repo:

- **A: "ocr-paper-parser"** — narrow converter tool
- **B: "paper-anatomist"** — ambitious semantic engine
- **C: "paper-briefer"** — use-case focused LLM context optimizer

## Decision

Option C was selected: position as a tool that compresses papers into optimized LLM context.

## Rationale

- **Instant comprehension**: a newcomer understands the value without knowing OCR Playground
- **Largest audience**: anyone using LLMs for research (not just OCR Playground users)
- **Natural scope constraint**: the brief output format (~3-4K tokens) prevents scope creep
- **Shippable in days**: the demo writes itself (paper -> brief -> Claude conversation)

## Rejected Alternatives

- **Option A**: unsearchable, invisible, requires explaining OCR Playground first
- **Option B**: 6-month research project for a solo developer; unvalidated claims on one paper

## Risks Accepted

- Context windows expanding may reduce need for compression (mitigated: cognitive load still matters)
- OCR Playground format dependency (mitigated: architecture supports future input format plugins)

## Validation

Compression test passed: 4/5 questions answered correctly from a 3.9K token brief of a 20K word paper, with zero hallucination.
