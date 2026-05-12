Process all files in `staging/files/` into the wiki.

**Setup (once before the loop)**
1. Read `raw/taxonomy.md`. If it doesn't exist, seed it from the Seed Taxonomy in `CLAUDE.md`.
2. List all files in `staging/files/` (skip `.gitkeep`). If none, stop and say so.

**For each file — single read pass (architect + update check + wiki writing)**

a. Read the file. This one read serves all steps below — do not re-read.

b. **Taxonomy Architect**: determine the best `raw/<path>/` (max 4 levels, lowercase-hyphenated nodes, no new top-level nodes). Update `raw/taxonomy.md` if new nodes are added. Move file: `staging/files/<name>` → `raw/<path>/<name>`.

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

g. Delete the original from `staging/files/`.

**Report**
- Files processed
- Wiki pages created / updated
- Pages marked superseded
- Taxonomy nodes added or changed
