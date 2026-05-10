"""Tests for the extraction engine."""

import zipfile
import tempfile
from pathlib import Path

from paper_briefer.extract import extract, _extract_headings, _extract_abstract, _detect_language


def _make_test_zip(tmp_path: Path) -> Path:
    """Create a minimal OCR Playground-style ZIP for testing."""
    zip_path = tmp_path / "test-paper.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("TestPaper.pdf/markdown.md", """# Test Paper: A Novel Approach

# Abstract

We present a novel approach to testing that achieves 99% accuracy on synthetic benchmarks. Our method introduces three key innovations: (1) structured extraction, (2) semantic compression, and (3) brief generation.

# 1. Introduction

This paper addresses the problem of testing.

# 2. Method

Our method uses regex patterns.

Figure 1 | Architecture of our testing system.

As shown in Figure 1, the system processes input documents.

# 3. Results

Table 1 | Comparison with baselines.

As shown in Table 1, our method outperforms all baselines.

# 6. Limitations and Future Work

Our approach has several limitations. First, it only supports one input format. Second, extraction quality depends on OCR output quality. In future work, we plan to support PDF and arXiv inputs directly.

# References

(Smith et al., 2024) introduced the baseline method.
(Jones et al., 2025) proposed an alternative approach.
""")
        zf.writestr("TestPaper.pdf/pages/page-1/markdown.md", """# Test Paper: A Novel Approach

# Abstract

We present a novel approach to testing that achieves 99% accuracy.
""")
        zf.writestr("TestPaper.pdf/pages/page-2/markdown.md", """1 Introduction 1
2 Method 2
3 Results 3
6 Limitations and Future Work 4
""")
        zf.writestr("TestPaper.pdf/pages/page-3/markdown.md", """# 2. Method

Our method uses regex patterns.

Figure 1 | Architecture of our testing system.
""")
    return zip_path


def test_extract_headings():
    text = "# Title\n## Section 1\n### Subsection\nNot a heading"
    result = _extract_headings(text)
    assert result == ["Title", "Section 1", "Subsection"]


def test_extract_abstract():
    text = "# Abstract\nThis is the abstract content.\n# Introduction\nThis is not."
    result = _extract_abstract(text)
    assert "abstract content" in result
    assert "Introduction" not in result


def test_detect_language_english():
    text = "The model achieves state of the art results with the new architecture for training."
    assert _detect_language(text) == "en"


def test_detect_language_french():
    text = "Les resultats sont dans les tableaux. Une methode est proposee pour les donnees."
    assert _detect_language(text) == "fr"


def test_full_extraction(tmp_path):
    zip_path = _make_test_zip(tmp_path)
    metadata = extract(zip_path)

    assert metadata.title == "Test Paper: A Novel Approach"
    assert metadata.total_pages >= 2
    assert "novel approach" in metadata.abstract.lower()
    assert metadata.limitations != ""
    assert "one input format" in metadata.limitations


def test_figures_extracted(tmp_path):
    zip_path = _make_test_zip(tmp_path)
    metadata = extract(zip_path)

    figure_ids = [f.id for f in metadata.figures_and_tables]
    assert "Figure 1" in figure_ids


def test_toc_extraction(tmp_path):
    zip_path = _make_test_zip(tmp_path)
    metadata = extract(zip_path)

    sections = [e["section"] for e in metadata.table_of_contents]
    assert "1" in sections or "2" in sections
