# CLAUDE.md

## What this project is

`paper-briefer` compresses academic papers (from OCR Playground ZIP exports) into ~3-4K token briefs optimized for LLM context injection. No runtime dependencies beyond Python 3.10+ standard library.

## Commands

```bash
# Run on a ZIP file
python -m paper_briefer.cli input.zip -o output/

# Run tests
python -m pytest tests/

# Install in development mode
pip install -e .
```

## Architecture

- `paper_briefer/extract.py` — Core extraction (ZIP -> DocumentMetadata dataclass)
- `paper_briefer/brief.py` — Brief generation (DocumentMetadata -> markdown string)
- `paper_briefer/cli.py` — CLI entry point

## Key Design Decisions

- No external dependencies. Pure stdlib (zipfile, re, json, dataclasses).
- Extraction is regex/heuristic-based (layers 1-2). LLM-augmented extraction (layer 3) is planned but optional.
- The brief format is designed for context injection, not human reading. Structure > prose.
- Figure/table captions + anchor sentences are the highest-ROI extraction target.

## Commit Convention

Conventional Commits 1.0.0. Types: feat, fix, docs, refactor, test, chore.
