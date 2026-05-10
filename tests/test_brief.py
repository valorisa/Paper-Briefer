"""Tests for the brief generator."""

from paper_briefer.extract import DocumentMetadata, FigureTableEntry
from paper_briefer.brief import generate_brief, estimate_tokens


def _make_sample_metadata() -> DocumentMetadata:
    return DocumentMetadata(
        title="Test Paper: A Novel Method",
        authors="Test Author (test@example.com)",
        source_file="test.zip",
        total_pages=10,
        total_word_count=5000,
        total_images=3,
        language="en",
        document_type="technical_report",
        abstract="We present a novel method that achieves state-of-the-art results.",
        key_contributions=["New attention mechanism", "Efficient training pipeline"],
        model_specs={"TestModel": {"params": "1B", "context": "128K"}},
        table_of_contents=[
            {"section": "1", "title": "Introduction", "page": 1},
            {"section": "2", "title": "Method", "page": 3},
        ],
        limitations="Our method only works on English text. Future work will address multilingual support.",
        figures_and_tables=[
            FigureTableEntry(
                id="Figure 1",
                page=3,
                caption="Architecture of our system",
                anchor_sentences=["As shown in Figure 1, the system processes input."],
            )
        ],
        cross_references=[],
        citation_density=[
            {"page": 1, "citation_count": 0, "density_pct": 0.0, "signal": "low_citation"},
            {"page": 5, "citation_count": 12, "density_pct": 4.5, "signal": "high_citation"},
        ],
        pages=[],
        keywords=["attention", "efficiency", "language model"],
    )


def test_brief_contains_title():
    meta = _make_sample_metadata()
    brief = generate_brief(meta)
    assert "Test Paper: A Novel Method" in brief


def test_brief_contains_abstract():
    meta = _make_sample_metadata()
    brief = generate_brief(meta)
    assert "state-of-the-art" in brief


def test_brief_contains_limitations():
    meta = _make_sample_metadata()
    brief = generate_brief(meta)
    assert "only works on English" in brief


def test_brief_contains_figures():
    meta = _make_sample_metadata()
    brief = generate_brief(meta)
    assert "Figure 1" in brief
    assert "Architecture of our system" in brief


def test_brief_contains_evidence_density():
    meta = _make_sample_metadata()
    brief = generate_brief(meta)
    assert "Reference-heavy" in brief or "Novel content" in brief


def test_estimate_tokens():
    text = "a" * 400
    assert estimate_tokens(text) == 100


def test_brief_size_reasonable():
    meta = _make_sample_metadata()
    brief = generate_brief(meta)
    tokens = estimate_tokens(brief)
    assert tokens < 5000
