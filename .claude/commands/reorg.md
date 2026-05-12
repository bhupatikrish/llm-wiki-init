Reorganize the `raw/` capability taxonomy and update all affected wiki pages.

1. Read `raw/taxonomy.md` in full.
2. Scan the actual `raw/` directory tree to see what files exist and where.
3. Identify improvement opportunities:
   - Nodes deeper than 4 levels
   - Nodes with only one child (may be collapsible)
   - Siblings that belong under a new shared parent
   - Inconsistent names (mixed case, unclear abbreviations)
   - Aliases that should become primary paths

4. **STOP.** Present the proposed new taxonomy to the user and ask for confirmation.
   Do not move any files until the user approves.

5. After user confirms:
   a. Move files to new paths in `raw/`
   b. For every moved file: scan all wiki pages, find pages whose `raw_path` frontmatter
      points to the old path, update them to the new path
   c. Rewrite `raw/taxonomy.md` to reflect the new structure
   d. Append `## [YYYY-MM-DD] reorg | <description>` to `wiki/log.md`

6. Report:
   - Files moved (old path → new path)
   - Wiki pages updated (which `raw_path` fields changed)
   - New taxonomy summary
