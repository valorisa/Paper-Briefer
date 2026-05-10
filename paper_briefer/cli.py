"""Command-line interface for paper-briefer."""

import argparse
import sys
from pathlib import Path

from .extract import extract
from .brief import generate_brief, estimate_tokens


def main():
    parser = argparse.ArgumentParser(
        prog="paper-briefer",
        description="Compress academic papers into optimized LLM context",
    )
    parser.add_argument("input", help="Path to OCR Playground ZIP export")
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: current directory)",
        default=".",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only produce metadata.json, skip brief generation",
    )
    parser.add_argument(
        "--brief-only",
        action="store_true",
        help="Only produce the markdown brief",
    )

    args = parser.parse_args()
    zip_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not zip_path.exists():
        print(f"Error: {zip_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting metadata from {zip_path.name}...")
    metadata = extract(zip_path)

    stem = zip_path.stem.replace(" ", "-").lower()

    if not args.brief_only:
        json_path = output_dir / f"{stem}-metadata.json"
        json_path.write_text(metadata.to_json(), encoding="utf-8")
        print(f"  -> {json_path} ({metadata.total_pages} pages, {metadata.total_images} figures)")

    if not args.json_only:
        brief = generate_brief(metadata)
        tokens = estimate_tokens(brief)
        brief_path = output_dir / f"{stem}-brief.md"
        brief_path.write_text(brief, encoding="utf-8")
        print(f"  -> {brief_path} (~{tokens} tokens)")
        print(f"  Compression: {metadata.total_word_count} words -> ~{tokens} tokens ({round(tokens / metadata.total_word_count * 100)}%)")

    print("Done.")


if __name__ == "__main__":
    main()
