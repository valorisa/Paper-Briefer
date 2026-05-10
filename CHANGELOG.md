# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-10

### Added

- Initial release
- OCR Playground ZIP extraction (structural + semantic layers)
- Brief generation (~3-4K tokens from 20K+ word papers)
- CLI with `--brief-only` and `--json-only` options
- Python API (`extract()` and `generate_brief()`)
- Figure/table caption extraction with anchor sentences
- Cross-reference graph extraction
- Citation density mapping
- Limitations & future work extraction
- Language detection (English/French)
- 14-test validation suite
- Compression quality validated: 4/5 questions correct, 0 hallucinations
