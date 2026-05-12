Process all files in `staging/files/` into the wiki.

**Setup (once before the loop)**
1. Read `raw/taxonomy.md`. If it doesn't exist, seed it from the Seed Taxonomy in `CLAUDE.md`.
2. List all files in `staging/files/` (skip `.gitkeep`). If none, stop and say so.
3. **Pre-process PDFs**: for every `.pdf` in `staging/files/`, run:
   ```
   tools/.venv/bin/python tools/convert_pdf.py "staging/files/<name>.pdf" "staging/files/<name>.md"
   ```
   Keep the original `.pdf` in `staging/files/` — it will be moved to `raw/` alongside its `.md` in step (b). **Do not delete the `.pdf`.**

**Process files one at a time — complete each file fully before starting the next.**

Do NOT read multiple files in parallel. Read one `.md` file, write all its wiki pages, update index and log, delete staging copies — then move to the next file. **Skip any `.pdf` files when iterating** — they are moved automatically alongside their matching `.md` in step (b).

For each `.md` file:

a. Read the file. This one read serves all steps below — do not re-read.

b. **Taxonomy Architect**: determine the best `raw/<path>/` (max 4 levels, lowercase-hyphenated nodes, no new top-level nodes). Update `raw/taxonomy.md` if new nodes are added. Then:
   - Move the `.md`: `staging/files/<name>.md` → `raw/<path>/<name>.md`
   - If a matching `.pdf` exists at `staging/files/<name>.pdf`, move it to the same location: `staging/files/<name>.pdf` → `raw/<path>/<name>.pdf`

c. **Update check** (content is already in context — no extra reads of the new source):
   - Scan `wiki/index.md` for existing concept/entity pages related to this source's topics
   - Read those pages (the only extra I/O here; justified by keeping the wiki current)
   - For each related page:
     - **Updates a claim** → rewrite that section in-place; set `last_verified` to today; append to `## Changelog`
     - **Contradicts a claim** → note both positions with source dates in the body; record the disagreement in `## Changelog`
     - **Supersedes an old source page** → set `superseded_by: [[ThisNewSlug]]` and `status: superseded` on the old source page's frontmatter

d. **Write wiki pages** (using content still in context):
   - `wiki/sources/<slug>.md` — summary, key points, frontmatter with `raw_path` and `last_verified: today`
   - `wiki/entities/<name>.md` — create or update; set `last_verified: today`; append to `## Changelog`
   - `wiki/concepts/<name>.md` — create or update; set `last_verified: today`; append to `## Changelog`

e. Update the relevant category section of `wiki/index.md` (not the whole file).

f. Append `## [YYYY-MM-DD] ingest | <Title>` to `wiki/log.md`.

g. Delete the `.md` from `staging/files/`. (The `.pdf` was already moved in step (b) — nothing left to delete.)

**Report**
- Files processed
- Wiki pages created / updated
- Pages marked superseded
- Taxonomy nodes added or changed
