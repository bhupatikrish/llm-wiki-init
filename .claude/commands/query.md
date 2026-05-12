Answer the question: $ARGUMENTS

1. Read the relevant category section(s) of `wiki/index.md` — not the whole file.
   Target by section header: Sources / Concepts / Entities / Analyses.

2. If the question spans multiple categories or needs broader search:
   `tools/.venv/bin/python tools/search.py "<question>" --top 8`

3. Read the top candidate wiki pages.

4. Synthesize an answer with `[[Page]]` citations.

5. **Raw fallback** — if wiki summaries lack sufficient detail:
   - Read `raw_path` from the relevant source page's frontmatter
   - Read the raw source file directly from `raw/<capability-path>/`
   - Browse adjacent files in the same `raw/` directory for related context

6. If the answer is a valuable synthesis (comparison, analysis, discovered connection):
   - File as `wiki/analyses/<slug>.md` with proper frontmatter (`last_verified: today`, `status: active`)
   - Add a row to the Analyses section of `wiki/index.md`
   - Append `## [YYYY-MM-DD] query | <Question summary>` to `wiki/log.md`

Provide the answer, then note at the end whether it was filed to the wiki.
