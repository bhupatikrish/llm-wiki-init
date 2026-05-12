Run a health check on the wiki and fix issues found.

1. Scan all pages in `wiki/` (entities/, concepts/, sources/, analyses/) for:
   - **Contradictions** — claims in one page that conflict with another
   - **Orphan pages** — no `[[inbound links]]` from any other wiki page
   - **Broken raw_path pointers** — `raw_path` in frontmatter pointing to a non-existent file
   - **Missing pages** — concepts or entities referenced via `[[WikiLink]]` but lacking their own page
   - **Missing cross-references** — clearly related pages that don't link to each other
   - **Stale pages** — concept/entity pages where `last_verified` is more than 90 days ago
     (for fast-moving domains like AI/LLM, use 60 days as the threshold)
   - **Uncovered newer sources** — active source pages whose `raw/` directory contains newer files
     not yet reflected in the concept pages that cite them

2. For each issue:
   - Fix directly if the correct action is unambiguous (add a missing link, correct a broken path)
   - Flag for user if judgment is required (conflicting claims, uncertain taxonomy)

3. Browse `raw/` directories via `raw_path` breadcrumbs to surface related unprocessed files worth ingesting.

4. List all stale pages sorted by `last_verified` ascending (oldest first) as candidates for `/refresh`.

5. Append `## [YYYY-MM-DD] lint | health check` to `wiki/log.md`.

6. Report:
   - Issues found by type
   - Issues fixed automatically
   - Stale pages needing `/refresh` (sorted oldest first)
   - Issues needing user input
   - Suggested new sources to ingest
