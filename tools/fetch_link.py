#!/usr/bin/env python3
"""
Download a URL as markdown using markitdown.

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
    out_dir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path("/tmp/llm-wiki-fetch")
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from markitdown import MarkItDown
    except ImportError:
        print("markitdown not found — run: bash tools/setup.sh", file=sys.stderr)
        sys.exit(1)

    md = MarkItDown()
    result = md.convert(url)

    parsed = urllib.parse.urlparse(url)
    raw_slug = (parsed.netloc + parsed.path).strip("/")
    slug = re.sub(r"[^\w-]", "-", raw_slug)[:80] or "page"
    slug = re.sub(r"-{2,}", "-", slug).strip("-")

    out_path = out_dir / f"{slug}.md"

    # Prepend source URL as a comment so the ingest workflow can reference it
    content = f"<!-- source: {url} -->\n\n{result.text_content}"
    out_path.write_text(content, encoding="utf-8")

    print(out_path)


if __name__ == "__main__":
    main()
