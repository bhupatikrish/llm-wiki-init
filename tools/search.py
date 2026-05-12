#!/usr/bin/env python3
"""
BM25 search over wiki/ markdown files.

Usage: python tools/search.py "query text" [--top N] [--dir PATH]

Falls back to TF-IDF term frequency if rank_bm25 is not installed.
Skips index.md and log.md (high noise, low signal for search).
"""
import argparse
import pathlib
import re
import math
import sys
from typing import List, Tuple


SKIP_FILES = {"index.md", "log.md"}


def load_pages(wiki_dir: pathlib.Path) -> List[Tuple[pathlib.Path, str]]:
    pages = []
    for path in sorted(wiki_dir.rglob("*.md")):
        if path.name in SKIP_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            pages.append((path, text))
        except OSError:
            pass
    return pages


def tokenize(text: str) -> List[str]:
    # Strip YAML frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:]
    return re.findall(r"[a-z0-9]+", text.lower())


def snippet(text: str, query_tokens: List[str], length: int = 200) -> str:
    lower = text.lower()
    best_pos = 0
    for token in query_tokens:
        pos = lower.find(token)
        if pos != -1:
            best_pos = max(0, pos - 40)
            break
    chunk = text[best_pos: best_pos + length].replace("\n", " ").strip()
    return chunk + ("..." if len(text) - best_pos > length else "")


def bm25_search(query: str, pages, top_n: int):
    try:
        from rank_bm25 import BM25Okapi
        tokenized_corpus = [tokenize(text) for _, text in pages]
        bm25 = BM25Okapi(tokenized_corpus)
        q_tokens = tokenize(query)
        scores = bm25.get_scores(q_tokens)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return [(pages[i][0], pages[i][1], score) for i, score in ranked[:top_n] if score > 0]
    except ImportError:
        return tfidf_search(query, pages, top_n)


def tfidf_search(query: str, pages, top_n: int):
    q_tokens = set(tokenize(query))
    n_docs = len(pages)
    results = []
    for path, text in pages:
        tokens = tokenize(text)
        if not tokens:
            continue
        tf = {t: tokens.count(t) / len(tokens) for t in q_tokens if t in tokens}
        if not tf:
            continue
        score = sum(
            v * math.log(n_docs / max(1, sum(1 for _, t in pages if tok in tokenize(t))))
            for tok, v in tf.items()
        )
        results.append((path, text, score))
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_n]


def main():
    parser = argparse.ArgumentParser(description="Search wiki markdown files")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--dir", default="wiki", help="Wiki directory (default: wiki)")
    args = parser.parse_args()

    wiki_dir = pathlib.Path(args.dir)
    if not wiki_dir.exists():
        print(f"Directory not found: {wiki_dir}", file=sys.stderr)
        sys.exit(1)

    pages = load_pages(wiki_dir)
    if not pages:
        print("No pages found.")
        return

    results = bm25_search(args.query, pages, args.top)
    if not results:
        print("No results.")
        return

    q_tokens = tokenize(args.query)
    for path, text, score in results:
        print(f"[{score:.3f}] {path}")
        print(f"  {snippet(text, q_tokens)}")
        print()


if __name__ == "__main__":
    main()
