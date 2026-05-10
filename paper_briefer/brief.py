"""Generate a compressed brief (~3-4K tokens) from extracted metadata."""

import re
from .extract import DocumentMetadata


def generate_brief(meta: DocumentMetadata) -> str:
    """Produce a markdown brief optimized for LLM context injection."""
    parts: list[str] = []

    parts.append(f"# {meta.title}")
    parts.append("")
    parts.append(f"**Authors:** {meta.authors}")
    parts.append(f"**Scope:** {meta.total_pages} pages, {meta.total_images} figures/tables, {meta.total_word_count} words")
    parts.append("")

    if meta.abstract:
        parts.append("## Abstract")
        parts.append("")
        parts.append(meta.abstract)
        parts.append("")

    if meta.key_contributions:
        parts.append("## Key Contributions")
        parts.append("")
        for c in meta.key_contributions:
            parts.append(f"- {c}")
        parts.append("")

    if meta.model_specs:
        parts.append("## Specifications")
        parts.append("")
        for name, data in meta.model_specs.items():
            if isinstance(data, dict):
                items = ", ".join(f"{k}: {v}" for k, v in data.items())
                parts.append(f"- **{name}**: {items}")
        parts.append("")

    if meta.figures_and_tables:
        parts.append("## Key Figures & Tables")
        parts.append("")
        for ft in meta.figures_and_tables:
            parts.append(f"**{ft.id}** (p.{ft.page}): {ft.caption}")
            for anchor in ft.anchor_sentences[:2]:
                clean = re.sub(r"!\[.*?\]\(.*?\)\s*", "", anchor).strip()
                if clean and len(clean) > 30:
                    parts.append(f"  > {clean[:250]}")
        parts.append("")

    if meta.table_of_contents:
        parts.append("## Structure")
        parts.append("")
        for entry in meta.table_of_contents:
            depth = entry["section"].count(".")
            if depth <= 1:
                page_str = f" (p.{entry['page']})" if entry.get("page") else ""
                parts.append(f"- {entry['section']} {entry['title']}{page_str}")
        parts.append("")

    if meta.limitations:
        parts.append("## Limitations & Future Work")
        parts.append("")
        parts.append(meta.limitations[:1000])
        parts.append("")

    if meta.citation_density:
        high = [c for c in meta.citation_density if c["signal"] == "high_citation"]
        low = [c for c in meta.citation_density if c["signal"] == "low_citation"]
        if high or low:
            parts.append("## Evidence Density")
            parts.append("")
            if high:
                page_list = ", ".join(f"p.{c['page']}" for c in high)
                parts.append(f"Reference-heavy pages: {page_list}")
            if low:
                page_list = ", ".join(f"p.{c['page']}" for c in low[:10])
                parts.append(f"Novel content pages: {page_list}")
            parts.append("")

    if meta.cross_references:
        parts.append("## Cross-References")
        parts.append("")
        for cr in meta.cross_references[:12]:
            parts.append(f"- p.{cr.source_page} → {cr.target_id}: {cr.source_context[:100]}")
        parts.append("")

    if meta.keywords:
        parts.append(f"## Keywords")
        parts.append(", ".join(meta.keywords))

    return "\n".join(parts)


def estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 chars for English)."""
    return len(text) // 4
