# LLM Wiki — Schema & Operating Instructions

Loaded every session. Contains conventions Claude needs for all operations.
**When copying this template for a new domain, edit only the Seed Taxonomy section.**

---

## Directory Map

| Path | Purpose |
|------|---------|
| `staging/files/` | User drops files here; Claude processes and removes them |
| `staging/links.md` | User pastes URLs here (one per line); Claude downloads and removes them |
| `raw/` | Immutable processed sources — Claude reads, never edits content |
| `raw/taxonomy.md` | Claude-maintained live capability tree (up to 4 levels) |
| `raw/assets/` | Downloaded images |
| `wiki/index.md` | Content catalog — updated on every ingest |
| `wiki/log.md` | Append-only chronological activity log |
| `wiki/overview.md` | Evolving high-level synthesis |
| `wiki/entities/` | People, models, organizations, systems |
| `wiki/concepts/` | Techniques, ideas, methods, benchmarks |
| `wiki/sources/` | One summary page per raw source |
| `wiki/analyses/` | Comparisons, filed query answers, syntheses |
| `tools/` | Python utilities — always invoke via `tools/.venv/bin/python` |
| `.claude/commands/` | Self-contained skill files: ingest-files, ingest-links, query, lint, refresh, reorg |
| `docs/obsidian-setup.md` | Optional Obsidian viewer configuration |

---

## Seed Taxonomy

> **Edit only this section when copying this template for a new wiki domain.**
> Replace the top-level categories below with your domain's root capabilities (3–5 items).
> Levels 2–4 are built dynamically from content during ingestion — do not pre-fill them.

```
# Seed Taxonomy — AI/LLM Wiki
llm
agents
infrastructure
```

Examples: 
- Personal wiki: `health goals relationships learning
- Business wiki: `product engineering customers operations`

---

## Page Format

Every wiki page must begin with YAML frontmatter. Required fields:

| Field | Required | Values / Notes |
|-------|----------|----------------|
| `title` | always | quoted string |
| `type` | always | `concept` · `entity` · `source` · `analysis` · `overview` |
| `tags` | always | lowercase, hyphenated list |
| `created` | always | YYYY-MM-DD |
| `updated` | always | YYYY-MM-DD — set on every edit |
| `last_verified` | always | YYYY-MM-DD — set on create; update when claims are reviewed |
| `sources` | always | count of raw sources this page draws from |
| `status` | always | `active` · `superseded` · `deprecated` |
| `superseded_by` | source pages only | `[[NewerSourcePage]]` when replaced; empty otherwise |
| `raw_path` | source pages | breadcrumb back to file in `raw/` |

Clean example:

```yaml
---
title: "Retrieval-Augmented Generation"
type: concept
tags: [llm, rag, retrieval]
created: 2026-05-12
updated: 2026-05-12
last_verified: 2026-05-12
sources: 3
status: active
superseded_by: ""
---
```

**Linking:** Use `[[WikiPageName]]` for all internal references. Always link entities and concepts mentioned in the body.

---

## Changelog Convention

Every concept and entity page ends with a `## Changelog` section (append-only, newest first):

```markdown
## Changelog

- **YYYY-MM-DD** — Initial page, sourced from [[SourcePage]]
- **YYYY-MM-DD** — Updated retrieval section; [[NewerSource]] supersedes earlier claim about X
- **YYYY-MM-DD** — Contradiction noted: [[Source-A]] and [[Source-B]] disagree on Y
```

Source pages do **not** get a Changelog — they are immutable records. Supersession is recorded in frontmatter (`superseded_by`) and in the concept page's Changelog only.

---

## Taxonomy Architect Rules

Applied during every ingest (zero extra token cost — content is already in context):

- Read `raw/taxonomy.md`; fall back to Seed Taxonomy above if it doesn't exist yet
- Determine the best capability path — **maximum 4 levels deep**
- **Never invent new top-level nodes** without asking the user; all new nodes go at levels 2–4
- Node names: lowercase, hyphenated (`graph-rag` not `GraphRAG`)
- If content fits two paths equally: pick primary, add alias entry to `raw/taxonomy.md`
- File source to `raw/<path>/filename` — no re-read needed; content is already in context

---

## Log Format

Append to `wiki/log.md` after every operation:

```
## [YYYY-MM-DD] <operation> | <title>
```

Operations: `ingest` · `query` · `lint` · `refresh` · `reorg` · `init`  
Parse last 5 entries: `grep "^## \[" wiki/log.md | tail -5`

---

## Python Tools

Always invoke via the isolated venv — never bare `python`:

```bash
tools/.venv/bin/python tools/search.py "query"
tools/.venv/bin/python tools/fetch_link.py "https://..."
```
