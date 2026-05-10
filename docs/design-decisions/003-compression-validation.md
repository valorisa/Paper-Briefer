# ADR-003: Compression Validation Protocol

**Date:** 2026-05-10
**Status:** Accepted

## Context

Before committing to the "paper-briefer" positioning, we needed to validate that a compressed brief actually enables useful LLM conversations about a paper.

## Decision

Adopted a 5-question validation protocol:

1. **Architecture/Methodology** — Can the LLM explain how the system works?
2. **Quantitative claims** — Can it reproduce specific numbers?
3. **Limitations** — Does it know what doesn't work?
4. **Novelty assessment** — Can it distinguish new from inherited?
5. **Practical implications** — Can it derive actionable advice?

## Acceptance Criteria

- 4/5 questions answered substantively
- Zero hallucinations (must say "I don't know" when info is missing)
- Confidence calibration correlates with answer quality

## Result

Passed on first attempt (after adding limitations extraction). The protocol is now the standard test for any extraction changes.
