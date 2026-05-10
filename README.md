# paper-briefer

> Compress academic papers into optimized context for LLM conversations.

## The Problem

You've just found a 40-page technical paper you need to understand. You want to discuss it with Claude, ChatGPT, or any other LLM — ask questions about the architecture, challenge the methodology, understand the limitations.

But pasting the raw text is wasteful:

- OCR output is full of formatting noise, image references, and boilerplate
- Most of the token budget goes to content that doesn't help the conversation
- The LLM has no structural map of the paper — it can't distinguish novel claims from background review
- You're paying for tokens that carry zero semantic value

## The Solution

`paper-briefer` extracts the **semantic skeleton** of a paper — the claims, the evidence, the specifications, the limitations, the argument structure — and compresses it into a ~3-4K token brief that preserves discussion quality.

The brief isn't a summary. It's a **structured context injection** designed to give an LLM everything it needs to have an informed conversation about the paper, without the noise.

## Quick Start

### Installation

```bash
pip install paper-briefer
```

### Basic Usage

```bash
paper-briefer paper-export.zip
```

This produces two files:

- `paper-export-brief.md` — the compressed brief (~3-4K tokens), ready to paste into any LLM
- `paper-export-metadata.json` — full structured metadata for programmatic use

### Example

```bash
$ paper-briefer deepseek-v4.zip -o output/

Extracting metadata from deepseek-v4.zip...
  -> output/deepseek-v4-metadata.json (46 pages, 22 figures)
  -> output/deepseek-v4-brief.md (~4155 tokens)
  Compression: 20270 words -> ~4155 tokens (20%)
Done.
```

## What's in the Brief?

The brief is organized into semantic layers, each serving a specific purpose for LLM comprehension:

| Section | Purpose | Example |
|---------|---------|---------|
| Title + scope | Paper identity and scale | "46 pages, 22 figures/tables, 20K words" |
| Abstract | Core claims in the authors' own words | Full abstract preserved |
| Key contributions | What's genuinely novel | "hybrid attention combining CSA and HCA" |
| Specifications | Numbers that define the system | "1.6T params, 49B activated, 1M context" |
| Figures & tables | Visual evidence with captions + anchor sentences | What each figure proves, in context |
| Structure | Navigable table of contents | Section hierarchy with page numbers |
| Limitations & future work | What the authors acknowledge doesn't work | Extracted from conclusion |
| Evidence density | Which pages are reference-heavy vs novel content | Guides where to look for innovation |
| Cross-references | How sections depend on each other | "Section 3.2 references Figure 5" |
| Keywords | Technical vocabulary | Enables precise follow-up queries |

### Why These Layers?

This structure was designed and validated through an adversarial review process (documented in `docs/design-decisions/`). Key insight: **figures and tables carry the proof**. A paper's claims live in the text, but the evidence lives in the visuals. Extracting figure captions with their in-text anchor sentences ("Figure 3 shows that...") transforms the brief from a document index into an evidence map.

## How to Use the Brief

### With Claude or ChatGPT

Paste the brief as context, then have a natural conversation:

```
Here's a structured brief of the paper I want to discuss:

[paste brief.md content here]

Based on this paper:
1. How does the attention architecture differ from the previous version?
2. What are the specific efficiency gains for long-context scenarios?
3. What limitations should I be aware of before building on this work?
```

### With Claude Code or Cursor

Place the brief in your project and reference it:

```bash
paper-briefer paper.zip -o docs/
# Then in Claude Code: "Read docs/paper-brief.md and explain the architecture"
```

### As a Research Pipeline

```python
from paper_briefer.extract import extract
from paper_briefer.brief import generate_brief

metadata = extract("paper.zip")

# Access structured data programmatically
for fig in metadata.figures_and_tables:
    print(f"{fig.id}: {fig.caption}")
    for anchor in fig.anchor_sentences:
        print(f"  Evidence: {anchor}")

# Generate the brief
brief = generate_brief(metadata)
```

## Compression Quality

### Validation Methodology

We tested the brief on the DeepSeek-V4 technical report (46 pages, 20,270 words, 22 figures) by giving the brief to a fresh LLM instance (no access to the original paper) and asking 5 substantive technical questions covering architecture, quantitative claims, limitations, novelty assessment, and practical implications.

### Results

| Metric | Value |
|--------|-------|
| Input size | 20,270 words (~27K tokens) |
| Brief size | ~4,155 tokens |
| Compression ratio | ~5x |
| Questions answered correctly | 4/5 |
| Hallucinations | 0 |
| Correctly identified gaps | Yes (said "I don't know" when info was missing) |

### What Worked

- **Architecture questions**: Correctly explained the CSA/HCA hybrid mechanism from figure descriptions
- **Quantitative claims**: All benchmark numbers reproduced exactly (pass rates, FLOPs ratios)
- **Novelty assessment**: Distinguished inherited from new components
- **Deployment implications**: Derived practical advantages from specs

### What Failed (and How We Fixed It)

- **Limitations question**: The original brief didn't extract the "Limitations & Future Work" section. The LLM correctly said "this information is not in the brief" rather than hallucinating. Fixed in v0.1 by adding limitations extraction.

## Input Format

### Currently Supported

**OCR Playground ZIP exports** — the structured format produced by [OCR Playground](https://ocr.space) when exporting processed documents. The ZIP contains:

```
document.pdf/
  markdown.md              <- full document as markdown
  pages/
    page-1/
      markdown.md          <- per-page content
      img-0.jpeg           <- extracted images
      img-0.jpeg-annotation.json
      hyperlinks.md        <- extracted URLs
    page-2/
      ...
```

### Planned

- Direct PDF input (via built-in OCR or external tools)
- arXiv LaTeX source
- Plain markdown files

## CLI Reference

```bash
# Basic: produce both brief and metadata
paper-briefer input.zip

# Specify output directory
paper-briefer input.zip -o ./analysis/

# Only the markdown brief (for pasting into LLMs)
paper-briefer input.zip --brief-only

# Only the structured JSON (for programmatic use)
paper-briefer input.zip --json-only
```

## Architecture

```
paper_briefer/
  __init__.py     <- version
  extract.py      <- Core extraction engine (ZIP -> DocumentMetadata)
  brief.py        <- Brief generator (DocumentMetadata -> markdown)
  cli.py          <- Command-line interface
```

### Extraction Layers

The extraction engine operates in three passes:

1. **Structural pass** (regex): headings, ToC, page boundaries, word counts
2. **Semantic pass** (regex + heuristics): figure captions, anchor sentences, cross-references, citation density, limitations
3. **Intelligence pass** (planned, optional): LLM-augmented claim summaries, evidence typing

Layers 1 and 2 require no API keys or external dependencies. Layer 3 will be optional and use the Claude API for deeper semantic analysis.

## Design Decisions

The positioning and feature set of this tool were validated through two LLM Council sessions (5 independent advisors + peer review + chairman synthesis). Key decisions documented in `docs/design-decisions/`:

- **Why "brief" over "summary"**: A summary loses structure. A brief preserves queryable relationships.
- **Why figures first**: Figures and tables concentrate a paper's proof. Caption + anchor extraction gives 10x more comprehension ROI than section boundary detection.
- **Why limitations matter**: The only question that failed validation was about limitations. Papers that acknowledge weaknesses are more trustworthy — and LLMs need that signal.
- **Why not full semantic analysis in v1**: Regex extraction at ~0 cost covers 80% of value. LLM inference for claim graphs is the 20% that costs $5/paper — reserved for v2.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
