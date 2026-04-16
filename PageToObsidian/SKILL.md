---
name: PageToObsidian
description: "Single web page capture to Obsidian: auto-detects site type, converts HTML to Markdown and creates/updates Personas index. Bidirectionally compatible with WebToObsidian for full-site capture. Use when: capture article, download web page, save page to Obsidian, PageToObsidian, convert HTML to markdown"
license: MIT
author: lunasoft2001
  https://github.com/lunasoft2001
---

# PageToObsidian

Complete capture of a single web page to a technical note in Obsidian. Auto-detects page/site context, converts HTML to quality Markdown, and manages the Personas index identically to `WebToObsidian`.

**Dependencies:** HTML/web utilities toolkit (stdlib)

---

## When to use this skill

- User provides a specific URL and wants to save it as a note in Obsidian
- User says "capture this page", "save this article", "PageToObsidian"
- User wants to document a single web article in their Second Brain
- User downloads individual pages from a blog before capturing the entire site

---

## Requirements

- **Python 3.9+** — stdlib only
- `OBSIDIAN_VAULT` environment variable (optional, defaults to Luna vault)
- Page must be accessible via HTTP/HTTPS

---

## Command to run

```bash
python3 ~/.copilot/skills/PageToObsidian/scripts/page_to_obsidian.py <URL>
```

Script outputs JSON to stderr with all metadata.

---

## Complete workflow step by step

### Step 1 — Run the script

```bash
python3 ~/.copilot/skills/PageToObsidian/scripts/page_to_obsidian.py "https://example.com/article"
```

The script does:
1. Downloads the HTML page
2. If URL is a blog home page, resolves automatically to the first post
3. Extracts: title, content, publish date, author (if available)
4. Normalizes site name from metadata/root domain for Persona compatibility
5. Converts HTML → clean Markdown
6. Saves note in `Atlas/Recursos/<SiteName>/`
7. Outputs JSON with all data

### Step 2 — Output JSON

JSON contains these key fields:

| Field | Description |
|---|---|
| `title` | Page title |
| `site_name` | Site name (e.g., "Accessaplicaciones") |
| `url` | Full URL |
| `requested_url` | Original URL provided by user |
| `resolved_from_home` | `true` if script auto-followed home page to first article |
| `content` | Content converted to Markdown |
| `date_published` | Publication date (if available) |
| `author` | Author name (if available) |
| `page_id` | Unique page ID (slug or hash) |
| `target_note` | Path to save note in `Atlas/Recursos/<SiteName>/` |
| `saved` | `true` when note is written successfully |
| `persona` | Site information object (see below) |

**Persona object:**

| Field | Description |
|---|---|
| `name` | Site name (e.g., "Accessaplicaciones") |
| `path` | Full path to `Atlas/Personas/SiteName.md` |
| `wikilink` | Ready wikilink: `[[Atlas/Personas/SiteName]]` |
| `created_now` | `true` if just created, `false` if already exists |

### Step 2.5 — Automatic Personas management

Script **automatically checks** if `Atlas/Personas/<SiteName>.md` exists:

- **If NOT exists:** Creates new Persona file with this page marked as `[p]` (processed)
- **If ALREADY exists:** Adds page to existing checklist as `[p]` and updates "Generated notes" section

This integration makes `PageToObsidian` **fully compatible with `WebToObsidian`**:
- Download individual pages → registered in their Persona
- Later download entire site → index already has previous pages as `[p]`

**Generated template** (identical to `WebToObsidian`):

```markdown
---
tags: [atlas, persona, web-site]
site: "Site Name"
url: https://example.com
updated: 2026-04-16
total-articles: 3
---

# Site Name — Article Index

## Articles

- [p] **Article Title** · 2026-04-15 · https://example.com/article · `page-id`
- [ ] **Another Article** · 2026-04-10 · https://example.com/another · `another-id`

---

## Generated notes

- [[Atlas/Recursos/Site Name/Article Title saved]]
```

### Step 3 — Output structure

Generated note is saved to:
```
Atlas/Recursos/<SiteName>/
├── Article Title.md       ← technical note
└── ...
```

**Note frontmatter:**

```markdown
---
tags: [atlas, resource, <theme-tag>]
url: <url>
site: "<site_name>"
persona: "[[Atlas/Personas/SiteName]]"
author: "<author>"
date-published: "<date>"
date-saved: <today>
---

# Article Title

> 👤 By: <persona_wikilink>
> 📅 Published: <date>
> 🔗 [Read original](<url>)

---

## Content

<markdown content converted from HTML>

---

## Sources
- [Original article](<url>) — <site_name>
```

### Step 4 — Save the note

Creates folder `Atlas/Recursos/<SiteName>/` if it doesn't exist.
Saves note with clean article title as filename.
If file already exists, it updates the note in place.

### Step 5 — Continue with WebToObsidian (optional)

If the content is good and you want the whole site, run WebToObsidian scan next. Existing page(s) already captured by PageToObsidian will remain marked as `[p]` in the shared Persona index.

---

## Conventions

- **Site name**: extracted from domain or metadata (e.g., "Accessaplicaciones")
- **Domain handling**: subdomains are normalized to root site identity when possible (e.g., `blog.luna-soft.es` → `Luna-soft`)
- **Note location**: `VAULT/Atlas/Recursos/<SiteName>/<Title>.md`
- **Persona location**: `VAULT/Atlas/Personas/<SiteName>.md`
- **Page ID**: clean slug or hash if no slug exists

---

## Notes

- Script may take 3-10 seconds depending on page size
- Automatically converts HTML → Markdown
- Fully compatible with `WebToObsidian` — both use the same Personas template
- You can download individual pages in any order, then run `WebToObsidian --process`
