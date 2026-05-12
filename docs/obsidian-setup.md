# Obsidian Setup

Obsidian is an optional viewer for the wiki. Claude never uses it — it reads files directly.
The wiki is plain markdown and works in any viewer (VS Code, Typora, GitHub, etc.).

## Configuration

Open your wiki folder as an Obsidian vault, then:

| Setting | Value |
|---------|-------|
| Files & links → Attachment folder path | `raw/assets` |
| Files & links → Default location for new notes | `wiki/` |

## Recommended plugins

- **Dataview** — query page frontmatter as a database
- **Marp** — render markdown as slide decks directly from wiki content

## Graph view

`[[WikiLink]]` syntax in wiki pages renders as graph edges automatically.
The graph view is the best way to see which pages are hubs and which are orphans.

## Useful Dataview queries

List all wiki pages sorted by last update:
```dataview
TABLE type, updated, last_verified, sources FROM "wiki"
SORT updated DESC
```

Find stale pages (not verified in 60+ days):
```dataview
TABLE last_verified FROM "wiki"
WHERE type != "overview" AND date(last_verified) < date(today) - dur(60 days)
SORT last_verified ASC
```

Find superseded source pages:
```dataview
TABLE superseded_by FROM "wiki/sources"
WHERE status = "superseded"
```
