---
name: presentation-pptx-builder
description: Generates a .pptx presentation file consistent with a storyboard. Applies a clean, professional layout to each slide using python-pptx. Use when the user has a storyboard and wants to build the actual PowerPoint deck, generate slides programmatically, or produce a .pptx from structured content. Triggers on: "build the pptx", "generate the deck", "create the PowerPoint", "make the slides file", "produce the .pptx", "genera el pptx", "crea las diapositivas", "arma el PowerPoint", "produce el deck".
license: MIT
author: lunasoft2001 <https://github.com/lunasoft2001>
---

# Presentation PPTX Builder

Convert a storyboard into a `.pptx` file using `scripts/build_pptx.py`. Each slide is built from the storyboard's per-slide data: title, message, visual type, and act label.

## Required Inputs

| Field | Source | Description |
|-------|--------|-------------|
| `storyboard` | `/deliverables/<slug>/storyboard.json` (preferred) or Markdown/docx | Slide-by-slide structure from `presentation-storyboard` |
| `slug` | User / orchestrator | Output folder identifier |
| `theme` | Optional | Color theme: `corporate` (default) / `minimal` / `dark` / `vibrant` |
| `logo_path` | Optional | Path to a logo image file to embed on title slide |

**Primary input path**: `presentation-storyboard` always produces `/deliverables/<slug>/storyboard.json` alongside `storyboard.docx`. Use the JSON file directly — it requires no conversion.

**Fallback input**: if only a `.docx` or Markdown storyboard is available (e.g., the user created the storyboard manually), convert it to the JSON schema below before running the script.

## Build Workflow

1. **Locate the storyboard JSON**: check `/deliverables/<slug>/storyboard.json` first. If absent, ask whether the storyboard was created with `presentation-storyboard` (it should exist) or offer to convert from docx/Markdown.
2. **Select layout per slide** (see `references/pptx-design-guide.md`):
   - Title slide → `LAYOUT_TITLE`
   - Content slides → `LAYOUT_CONTENT` or `LAYOUT_TWO_COLUMN`
   - Closing / Q&A → `LAYOUT_BLANK` with large centered text
3. **Run the builder script**:

```bash
python3 suites/presentation/presentation-pptx-builder/scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

4. **Confirm output**: verify the file exists and slide count matches the storyboard.

## Storyboard JSON Contract

If the storyboard is in `.docx` or Markdown, convert to this JSON before running the script:

```json
{
  "title": "Presentation Title",
  "slug": "my-deck-2026",
  "theme": "corporate",
  "slides": [
    {
      "number": 1,
      "title": "Slide Title",
      "message": "One-sentence key message",
      "act": "Context",
      "duration_min": 2,
      "visual_type": "title",
      "body_bullets": ["Optional bullet 1", "Optional bullet 2"]
    }
  ]
}
```

Save this JSON to `/deliverables/<slug>/storyboard.json` before calling the script.

## Slide Design Rules

- **One message = one slide**: the `message` goes in the subtitle or as a large bold statement.
- **Body text maximum**: 5 bullets per slide, max 8 words per bullet.
- **Visual placeholders**: when `visual_type` is `chart`, `diagram`, or `photo`, insert a labeled placeholder rectangle — do not fabricate data.
- **Consistent branding**: title font, accent color, and footer apply uniformly across all slides.
- **Slide numbers**: add to all slides except the title slide.

## Themes

| Theme | Background | Accent | Font |
|-------|-----------|--------|------|
| `corporate` | White | Navy (#1B3A6B) | Calibri |
| `minimal` | White | Charcoal (#333333) | Arial |
| `dark` | Dark (#1A1A2E) | Cyan (#00D4FF) | Calibri |
| `vibrant` | White | Purple (#7B2FBE) | Segoe UI |

## Output

Saves to: `/deliverables/<slug>/deck.pptx`

## Limitations

- Requires `python-pptx` (`pip install python-pptx`).
- Does not generate real charts or data visualizations — inserts labeled placeholders.
- Does not embed live data from Excel or external sources.
- For design details and layout reference, see `references/pptx-design-guide.md`.
