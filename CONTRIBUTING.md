# Contributing to paper-briefer

## Development Setup

```bash
git clone https://github.com/valorisa/paper-briefer.git
cd paper-briefer
pip install -e .
```

No external dependencies required — the tool uses only Python standard library.

## Running Tests

```bash
python -m pytest tests/
```

## Project Structure

```
paper-briefer/
  paper_briefer/        <- source package
  tests/                <- test suite
  examples/             <- sample outputs (brief + metadata)
  docs/
    design-decisions/   <- architectural decision records
  README.md
  CONTRIBUTING.md
  CLAUDE.md             <- AI coding assistant instructions
  pyproject.toml
  LICENSE
```

## Adding Input Format Support

New input formats (PDF, arXiv, etc.) should be implemented as separate modules in `paper_briefer/` that produce the same `DocumentMetadata` dataclass. The brief generator is format-agnostic.

## Commit Convention

We use Conventional Commits 1.0.0:

```
feat(extract): add equation context extraction
fix(brief): handle papers without abstract section
docs: update compression quality results
```

## What Makes a Good PR

- Focused: one feature or fix per PR
- Tested: include a test case or example output showing the change
- Documented: if it changes user-facing behavior, update the README
