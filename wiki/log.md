# Wiki Log

Append-only chronological record of all wiki operations.

**Format**: `## [YYYY-MM-DD] <operation> | <title>`
**Operations**: `ingest`, `query`, `lint`, `reorg`, `init`
**Parse last 5 entries**: `grep "^## \[" wiki/log.md | tail -5`

---

## [2026-05-12] init | Wiki initialized
