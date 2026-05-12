Bring the wiki page **$ARGUMENTS** up to date against current knowledge.

If `$ARGUMENTS` is empty or the page is not found, list all concept and entity pages sorted by `last_verified` ascending (oldest first) and ask which to refresh.

**Gather context**

1. Read the target page (`wiki/concepts/`, `wiki/entities/`, or `wiki/analyses/` — try in that order).

2. Collect contributing sources:
   - Find `wiki/sources/` pages that link to this page via `[[WikiLink]]`
   - Collect their `raw_path` values

3. Search for related wiki pages:
   `tools/.venv/bin/python tools/search.py "<page title>" --top 10`

4. Scan `raw/` directories adjacent to known `raw_path` files for newer files not yet reflected in this page.

**Assess changes since `last_verified`**

- Claims that newer sources **update or refine** → rewrite in-place
- Claims that newer sources **directly contradict** → note both positions with source dates; current understanding prevails in the main body
- Concepts that have been **superseded or renamed** → update terminology; note old name in Changelog
- New sub-concepts worth a dedicated page → create stubs and link them

**Rewrite rules**

- Main body always reflects **current best understanding**
- Historical context removed from the main body moves to `## Changelog` — never deleted
- Contested claims: *"As of [date], [[Source-A]] argues X while [[Source-B]] argues Y"*

**Finalise**

5. Update frontmatter: `last_verified: today`, `updated: today`, `sources` count if changed.

6. Append to `## Changelog` (create section if absent, newest entry first):
   `- **YYYY-MM-DD** — Refreshed: <what changed and why>`

7. If a source page is now superseded: set `status: superseded` and `superseded_by: [[NewerPage]]` on the old source page.

8. Append `## [YYYY-MM-DD] refresh | $ARGUMENTS` to `wiki/log.md`.

**Report**
- Sections updated and why
- Any claims that remain contested (both sources noted)
- Source pages marked superseded
- New sources in `raw/` not yet ingested that are directly relevant (suggest `/ingest-files`)
