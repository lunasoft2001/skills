---
name: WebToObsidian
description: "Two-phase pipeline to capture entire websites into Obsidian Second Brain. Phase 1 (scan) auto-detects site type (WordPress REST API, RSS feed, Sitemap, or static) and creates checklist index in Atlas/Personas/<SiteName>.md. Phase 2 (process) downloads each [x] article, converts HTML to Markdown and saves in Atlas/Recursos/<SiteName>/. Fully compatible with PageToObsidian for capturing individual pages first. Use: capture website, blog to Obsidian, scan blog, capture articles, WebToObsidian"
license: MIT
author: lunasoft2001
  https://github.com/lunasoft2001
---

# WebToObsidian

Two-phase pipeline to capture an entire web site into an Obsidian Second Brain.
Follows the same checklist-driven workflow as ChannelToObsidian, with full bidirectional compatibility with PageToObsidian.

**Auto-detects site type:** WordPress REST API → RSS/Atom feed → Sitemap → Static single-page

**Companion skill:** [PageToObsidian](../PageToObsidian/SKILL.md) — capture individual pages before/after/between WebToObsidian phases.

---

## When to use this skill

- The user gives a website/blog URL and wants to capture all articles into Obsidian
- The user says "capture this blog", "scan this site", "WebToObsidian", "indexa todo el blog"
- The user wants to selectively save web articles into their Second Brain
- The user has already downloaded some pages individually via PageToObsidian and wants to capture the full site

---

## Requirements

- **Python 3.9+** — stdlib only for base functionality
- `html2text` (optional, recommended): `pip install html2text` — improves Markdown quality
- `OBSIDIAN_VAULT` environment variable (optional)

---

## Commands

```bash
# Phase 1 — Scan: detect site and create article checklist
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py <URL>

# Phase 2 — Process: generate notes for [x] articles
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py <URL> --process

# Optional: audit current vault coverage/health
python3 ~/.copilot/skills/WebToObsidian/scripts/audit_vault.py
```

---

## Supported site types (auto-detected in order)

| Type | Detection | Coverage |
|------|-----------|----------|
| **WordPress** | `/wp-json/wp/v2/posts` | All posts, paginated |
| **RSS / Atom** | `/feed`, `/rss.xml`, `/atom.xml`, custom | All feed items |
| **Sitemap** | `/sitemap.xml`, `/sitemap_index.xml` | All pages (filters images/categories) |
| **Single-page** | Fallback — named anchors, h2/h3 headings | Sections of the page |

---

## Full workflow

### Phase 1 — Scan

```bash
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://example.com"
```

What happens:
1. Auto-detects site type (WordPress → RSS → Sitemap → Single-page)
2. Fetches all article/section metadata
3. Creates/updates `Atlas/Personas/<SiteName>.md` with checklist:
   - `[ ]` — not yet reviewed
   - `[x]` — selected for processing
   - `[p]` — already processed (note exists, often from PageToObsidian)
4. Opens the index in Obsidian

**Example index output:**
```markdown
## Artículos

- [ ] **Ribbon para torpes** · https://accessaplicaciones.com/ribbon.html · `ribbon`
- [x] **Access Vs MySQL** · https://accessaplicaciones.com/mysql.html · `mysql`
- [p] **Tratar XML con DOM** · 2023-10-15 · https://... · `tratar-xml-con-dom`
```

### Between phases — User reviews the checklist

Open `Atlas/Personas/<SiteName>.md` in Obsidian and:
- Change `[ ]` to `[x]` for articles you want to save
- Leave `[ ]` for items to skip
- Items with `[p]` are already processed (note exists) — leave them unchanged
- This is compatible with items processed by PageToObsidian

### Phase 2 — Process

```bash
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://example.com" --process
```

What happens for each `[x]` item:
1. Downloads the article URL
2. Extracts the main content (`<article>`, `<main>`, `<div class="content">`, etc.)
3. Converts HTML to Markdown (html2text if installed, else built-in converter)
4. Saves note to `Atlas/Recursos/<SiteName>/<Title>.md` with YAML frontmatter
5. Marks item as `[p]` in the index
6. Appends wikilink to the index "Notas generadas" section

---

## Bidirectional compatibility with PageToObsidian

You can use both skills together seamlessly:

**Scenario 1: Pages first, then site**
```bash
# Download individual pages you find interesting
python3 ~/.copilot/skills/PageToObsidian/scripts/page_to_obsidian.py "https://example.com/article1"
python3 ~/.copilot/skills/PageToObsidian/scripts/page_to_obsidian.py "https://example.com/article2"

# Then scan the entire site
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://example.com"

# Those two pages will show as [p] in the checklist
```

**Scenario 2: Site first, then individual pages**
```bash
# Scan the entire site
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://example.com"

# Mark some as [x], process them
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://example.com" --process

# Later, find another article and capture it individually
python3 ~/.copilot/skills/PageToObsidian/scripts/page_to_obsidian.py "https://example.com/late-discovery"

# The new article gets added to the same Personas index
```

Both skills share:
- The same `Atlas/Personas/<SiteName>.md` index file
- The same folder structure `Atlas/Recursos/<SiteName>/`
- The same note format and frontmatter

Compatibility note:
- `WebToObsidian` now normalizes site name from root domain (e.g., `blog.luna-soft.es` → `Luna-soft`) to match `PageToObsidian` and avoid split Personas.

---

## Generated note structure

```markdown
---
tags: [atlas, recurso, web, site-name]
sitio: "Site Name"
persona: "[[Atlas/Personas/Site Name]]"
url: "https://example.com/post"
author: "Author Name"
date-published: "2024-01-15"
date-guardado: 2026-04-15
---

# Article Title

> 👤 De: [[Atlas/Personas/Site Name]]
> 📅 Publicado: 2024-01-15
> 🔗 [Fuente original](https://example.com/post)

---

[converted article content in Markdown]
```

---

## Examples

```bash
# WordPress blog
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://myblog.com"

# Static site with named-anchor sections
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://accessaplicaciones.com/ejemplos.html"

# Process selected articles
python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://accessaplicaciones.com/ejemplos.html" --process

# Override vault path
OBSIDIAN_VAULT="/path/to/vault" python3 ~/.copilot/skills/WebToObsidian/scripts/web_to_obsidian.py "https://example.com"
```

---

## Notes

- **Rate limiting**: 0.5s delay between requests
- **Page cache**: For single-page sites, the page is downloaded once; sections are extracted locally
- **Deduplication**: Re-running scan preserves existing `[x]` and `[p]` states
- **Encoding**: Handles UTF-8, ISO-8859-1 and other common encodings automatically
- **html2text** (optional): `pip install html2text` produces cleaner Markdown for complex articles
- **Automatic audit**: `enrich_second_brain.py` now also writes `Atlas/Meta/Auditoria.md` with coverage by topic/source and recommendations
