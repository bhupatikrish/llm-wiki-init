#!/usr/bin/env python3
"""
Convert a PDF (or any docling-supported document) to markdown.

Usage: python tools/convert_pdf.py <input_path> [output_path]

Prints the path of the saved markdown file so the caller can read it.
If output_path is omitted, writes alongside the input with a .md extension.
"""
import sys
import pathlib


def main():
    if len(sys.argv) < 2:
        print("Usage: convert_pdf.py <input_path> [output_path]", file=sys.stderr)
        sys.exit(1)

    in_path = pathlib.Path(sys.argv[1])
    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    out_path = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else in_path.with_suffix(".md")

    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("docling not found — run: bash tools/setup.sh", file=sys.stderr)
        sys.exit(1)

    converter = DocumentConverter()
    result = converter.convert(str(in_path))
    markdown = result.document.export_to_markdown()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
