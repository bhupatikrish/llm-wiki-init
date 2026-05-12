#!/usr/bin/env python3
"""
Download a URL as markdown using docling.

Usage: python tools/fetch_link.py <url> [output_dir]

Prints the path of the saved markdown file so the caller can read it.
"""
import sys
import pathlib
import re
import urllib.parse


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_link.py <url> [output_dir]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    default_dir = pathlib.Path(__file__).parent.parent / "staging" / "temp"
    out_dir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else default_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("docling not found — run: bash tools/setup.sh", file=sys.stderr)
        sys.exit(1)

    converter = DocumentConverter()
    result = converter.convert(url)
    markdown = result.document.export_to_markdown()

    parsed = urllib.parse.urlparse(url)
    raw_slug = (parsed.netloc + parsed.path).strip("/")
    slug = re.sub(r"[^\w-]", "-", raw_slug)[:80] or "page"
    slug = re.sub(r"-{2,}", "-", slug).strip("-")

    out_path = out_dir / f"{slug}.md"

    content = f"<!-- source: {url} -->\n\n{markdown}"
    out_path.write_text(content, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
