"""Core extraction engine: ZIP → structured metadata → brief."""

import json
import re
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class FigureTableEntry:
    id: str
    page: int
    caption: str
    anchor_sentences: list[str] = field(default_factory=list)


@dataclass
class CrossReference:
    source_page: int
    source_context: str
    target_type: str
    target_id: str


@dataclass
class PageMetadata:
    page_number: int
    word_count: int
    has_images: bool
    image_count: int
    has_tables: bool
    headings: list[str] = field(default_factory=list)


@dataclass
class DocumentMetadata:
    title: str
    authors: str
    source_file: str
    total_pages: int
    total_word_count: int
    total_images: int
    language: str
    document_type: str
    abstract: str
    key_contributions: list[str]
    model_specs: dict
    table_of_contents: list[dict]
    limitations: str
    figures_and_tables: list[FigureTableEntry] = field(default_factory=list)
    cross_references: list[CrossReference] = field(default_factory=list)
    citation_density: list[dict] = field(default_factory=list)
    pages: list[PageMetadata] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


def extract(zip_path: str | Path) -> DocumentMetadata:
    """Extract structured metadata from an OCR Playground ZIP export."""
    zip_path = Path(zip_path)
    if not zip_path.exists():
        raise FileNotFoundError(f"File not found: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        doc_prefix = names[0].split("/")[0]

        page_dirs = sorted(
            {
                n.split("/pages/")[1].split("/")[0]
                for n in names
                if "/pages/" in n and "/" in n.split("/pages/")[1]
            },
            key=lambda x: int(re.search(r"\d+", x).group()),
        )

        full_markdown = ""
        full_md_path = f"{doc_prefix}/markdown.md"
        if full_md_path in names:
            full_markdown = zf.read(full_md_path).decode("utf-8", errors="replace")

        pages_metadata = []
        page_texts: dict[int, str] = {}
        toc_entries = []

        for page_dir in page_dirs:
            page_num = int(re.search(r"\d+", page_dir).group())
            prefix = f"{doc_prefix}/pages/{page_dir}/"

            md_path = f"{prefix}markdown.md"
            page_text = ""
            if md_path in names:
                page_text = zf.read(md_path).decode("utf-8", errors="replace")
            page_texts[page_num] = page_text

            images = [n for n in names if n.startswith(prefix) and n.endswith(".jpeg")]
            headings = _extract_headings(page_text)
            word_count = len(page_text.split())
            has_tables = _detect_tables(page_text)

            if page_num in (2, 3):
                toc_entries.extend(_extract_toc_entries(page_text))

            pages_metadata.append(
                PageMetadata(
                    page_number=page_num,
                    word_count=word_count,
                    has_images=len(images) > 0,
                    image_count=len(images),
                    has_tables=has_tables,
                    headings=headings,
                )
            )

        figures_and_tables = _extract_figures_and_tables(
            full_markdown, zf, names, doc_prefix, page_dirs
        )
        cross_references = _extract_cross_references(page_texts)
        citation_density = _compute_citation_density(page_texts)

        return DocumentMetadata(
            title=_extract_title(full_markdown),
            authors=_extract_authors(full_markdown),
            source_file=zip_path.name,
            total_pages=len(pages_metadata),
            total_word_count=sum(p.word_count for p in pages_metadata),
            total_images=sum(p.image_count for p in pages_metadata),
            language=_detect_language(full_markdown),
            document_type="technical_report",
            abstract=_extract_abstract(full_markdown),
            key_contributions=_extract_contributions(full_markdown),
            model_specs=_extract_specs(full_markdown),
            table_of_contents=toc_entries,
            limitations=_extract_limitations(full_markdown),
            figures_and_tables=figures_and_tables,
            cross_references=cross_references,
            citation_density=citation_density,
            pages=pages_metadata,
            keywords=_extract_keywords(full_markdown),
        )


# --- Private helpers ---


def _extract_headings(text: str) -> list[str]:
    return re.findall(r"^#{1,4}\s+(.+)$", text, re.MULTILINE)


def _detect_tables(text: str) -> bool:
    return bool(re.search(r"^\|.*\|.*\|", text, re.MULTILINE))


def _extract_toc_entries(text: str) -> list[dict]:
    entries = []
    for m in re.finditer(r"^(\d+(?:\.\d+)*)\s+(.+?)\s+(\d+)\s*$", text, re.MULTILINE):
        entries.append({"section": m.group(1), "title": m.group(2), "page": int(m.group(3))})
    if not entries:
        for m in re.finditer(r"^[-•]\s+(\d+(?:\.\d+)*)\s+(.+)$", text, re.MULTILINE):
            entries.append({"section": m.group(1), "title": m.group(2), "page": None})
    return entries


def _extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        if len(title) > 10:
            return title
    lines = text.strip().split("\n")
    for line in lines[:10]:
        line = line.strip().lstrip("#").strip()
        if len(line) > 10 and not line.startswith("!"):
            return line
    return "Untitled"


def _extract_authors(text: str) -> str:
    patterns = [
        r"(?:^|\n)([A-Z][a-z]+ [A-Z][a-z]+(?:,\s*[A-Z][a-z]+ [A-Z][a-z]+)*)",
        r"(\S+@\S+\.\S+)",
    ]
    for p in patterns:
        m = re.search(p, text[:3000])
        if m:
            return m.group(1).strip()
    return "Unknown"


def _extract_abstract(text: str) -> str:
    match = re.search(r"#\s*Abstract\s*\n(.+?)(?=\n#|\n!\[)", text, re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1).strip())[:1500]
    return ""


def _extract_contributions(text: str) -> list[str]:
    text_flat = re.sub(r"\s+", " ", text[:8000])
    contributions = []
    numbered = re.findall(r"\(\d+\)\s*([^;(]+?)(?=\(\d+\)|$)", text_flat)
    if numbered:
        contributions = [c.strip().rstrip(",. ") for c in numbered if len(c.strip()) > 20][:7]
    if not contributions:
        for m in re.finditer(r"(?:introduce|propose|design|develop)\s+(.{20,120}?)(?:[.,;])", text_flat, re.IGNORECASE):
            contributions.append(m.group(1).strip())
    return contributions[:7]


def _extract_specs(text: str) -> dict:
    specs = {}
    param_matches = re.finditer(
        r"(\w[\w\s-]{3,30})\s+with\s+([\d.]+[TBMK])\s+(?:total\s+)?parameters?\s*\((\d+[TBMK])\s+activated\)",
        text[:10000],
    )
    for m in param_matches:
        name = m.group(1).strip()
        specs[name] = {"total_parameters": m.group(2), "activated_parameters": m.group(3)}
    return specs


def _extract_limitations(text: str) -> str:
    patterns = [
        r"(?:#{1,3}\s*)?(?:Limitations?|Future\s+(?:Work|Directions?))[^\n]*\n(.+?)(?=\n#{1,3}\s|\Z)",
        r"(?:#{1,3}\s*)?Conclusion.*?\n(.+?)(?=\n#{1,3}\s*(?:References|Appendix|A\s)|\Z)",
    ]
    for p in patterns:
        m = re.search(p, text, re.DOTALL | re.IGNORECASE)
        if m:
            content = m.group(1).strip()
            content = re.sub(r"\s+", " ", content)
            if len(content) > 100:
                return content[:2000]
    return ""


def _extract_keywords(text: str) -> list[str]:
    kw_match = re.search(r"[Kk]eywords?:?\s*(.+?)(?:\n|$)", text[:5000])
    if kw_match:
        return [k.strip() for k in kw_match.group(1).split(",") if k.strip()]

    candidates = set()
    for m in re.finditer(r"\*\*([A-Z][^*]{3,40})\*\*", text[:15000]):
        candidates.add(m.group(1).strip())
    return sorted(candidates)[:20]


def _detect_language(text: str) -> str:
    sample = text[:5000].lower()
    fr_markers = sum(1 for w in ["les", "des", "est", "une", "dans", "pour"] if f" {w} " in sample)
    en_markers = sum(1 for w in ["the", "and", "for", "are", "with", "from"] if f" {w} " in sample)
    return "fr" if fr_markers > en_markers else "en"


def _extract_figures_and_tables(
    full_text: str,
    zf: zipfile.ZipFile,
    names: list[str],
    doc_prefix: str,
    page_dirs: list[str],
) -> list[FigureTableEntry]:
    entries = []
    seen_ids: set[str] = set()

    for pattern, prefix_label in [
        (r"(?:^|\n)(Figure\s+(\d+)\s*\|?\s*(.+?)(?:\n|$))", "Figure"),
        (r"(?:^|\n)(Table\s+(\d+)\s*\|?\s*(.+?)(?:\n|$))", "Table"),
    ]:
        for m in re.finditer(pattern, full_text, re.MULTILINE):
            fig_id = f"{prefix_label} {m.group(2)}"
            if fig_id in seen_ids:
                continue
            seen_ids.add(fig_id)
            caption = m.group(3).strip()
            anchors = _find_anchor_sentences(full_text, fig_id)
            page = _find_page_for_ref(fig_id, zf, names, doc_prefix, page_dirs)
            entries.append(FigureTableEntry(id=fig_id, page=page, caption=caption, anchor_sentences=anchors))

    return entries


def _find_anchor_sentences(text: str, ref_id: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    pattern = re.compile(re.escape(ref_id), re.IGNORECASE)
    anchors = []
    for sent in sentences:
        if pattern.search(sent) and len(sent) > 20:
            clean = re.sub(r"\s+", " ", sent).strip()
            clean = re.sub(r"!\[.*?\]\(.*?\)\s*", "", clean).strip()
            if clean and clean not in anchors:
                anchors.append(clean[:300])
    return anchors[:3]


def _find_page_for_ref(
    ref_id: str,
    zf: zipfile.ZipFile,
    names: list[str],
    doc_prefix: str,
    page_dirs: list[str],
) -> int:
    pattern = re.compile(re.escape(ref_id), re.IGNORECASE)
    for page_dir in page_dirs:
        md_path = f"{doc_prefix}/pages/{page_dir}/markdown.md"
        if md_path in names:
            content = zf.read(md_path).decode("utf-8", errors="replace")
            if pattern.search(content):
                return int(re.search(r"\d+", page_dir).group())
    return 0


def _extract_cross_references(page_texts: dict[int, str]) -> list[CrossReference]:
    refs = []
    patterns = [
        (r"(?:see|as (?:shown|discussed|described) in|refer to)\s+(Section\s+[\d.]+)", "section"),
        (r"(?:see|as (?:shown|discussed|described) in|refer to)\s+(Figure\s+\d+)", "figure"),
        (r"(?:see|as (?:shown|discussed|described) in|refer to)\s+(Table\s+\d+)", "table"),
    ]
    for page_num, text in page_texts.items():
        for pat, ref_type in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                ctx_start = max(0, m.start() - 50)
                ctx_end = min(len(text), m.end() + 50)
                context = re.sub(r"\s+", " ", text[ctx_start:ctx_end]).strip()
                refs.append(
                    CrossReference(
                        source_page=page_num,
                        source_context=context,
                        target_type=ref_type,
                        target_id=m.group(1).strip(),
                    )
                )
    return refs


def _compute_citation_density(page_texts: dict[int, str]) -> list[dict]:
    densities = []
    for page_num, text in sorted(page_texts.items()):
        citations = len(re.findall(r"\([A-Z][a-z]+(?:\s+et\s+al\.?)?,\s*\d{4}[a-z]?\)", text))
        citations += len(re.findall(r"\*\([^)]+,\s*\d{4}[a-z]?\)\*", text))
        word_count = len(text.split())
        density = round(citations / max(word_count, 1) * 100, 2)
        densities.append(
            {
                "page": page_num,
                "citation_count": citations,
                "density_pct": density,
                "signal": "high_citation" if density > 3.0 else ("low_citation" if density < 0.5 else "normal"),
            }
        )
    return densities
