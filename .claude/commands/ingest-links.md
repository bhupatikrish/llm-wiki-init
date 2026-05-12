Process all URLs in `staging/links.md` into the wiki.

**Setup (once before the loop)**
1. Read `staging/links.md`. Collect all non-blank lines that don't start with `#`. If none, stop and say so.
2. Read `raw/taxonomy.md` (seed from CLAUDE.md Seed Taxonomy if absent).

**For each URL — single read pass (architect + update check + wiki writing)**

a. Run: `tools/.venv/bin/python tools/fetch_link.py "<url>"`
   The script prints the path of the downloaded markdown file.

b. Read the downloaded file. This one read serves all steps below — do not re-read.

c. **Taxonomy Architect**: determine `raw/<path>/` (max 4 levels, lowercase-hyphenated, no new top-level nodes). Update `raw/taxonomy.md` if new nodes needed. Move file from temp path → `raw/<path>/<slug>.md`.

d. **Update check** (content already in context — no extra reads of the new source):
   - Scan `wiki/index.md` for existing concept/entity pages related to this source's topics
   - Read those pages (only extra I/O; keeps the wiki current)
   - For each related page:
     - **Updates a claim** → rewrite in-place; set `last_verified: today`; append to `## Changelog`
     - **Contradicts a claim** → note both positions with source dates; record in `## Changelog`
     - **Supersedes an old source** → set `superseded_by` + `status: superseded` on old source page

e. **Write wiki pages** (content still in context):
   - `wiki/sources/<slug>.md` — summary, key points, frontmatter with `raw_path`, source URL, `last_verified: today`
   - `wiki/entities/<name>.md` — create or update; `last_verified: today`; append to `## Changelog`
   - `wiki/concepts/<name>.md` — create or update; `last_verified: today`; append to `## Changelog`

f. Update relevant category section of `wiki/index.md`.

g. Append `## [YYYY-MM-DD] ingest | <Title>` to `wiki/log.md`.

h. Remove the processed URL line from `staging/links.md`.

**Error handling**: if a URL fails to download, log the error, leave the line in `staging/links.md`, and continue to the next URL.

**Report**
- URLs processed / failed
- Wiki pages created / updated
- Pages marked superseded
- Taxonomy changes
