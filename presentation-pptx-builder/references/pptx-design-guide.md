# PPTX Design Guide

Layout reference and design rules for `presentation-pptx-builder`.

---

## Slide Layouts

| Layout key | Use case | python-pptx index |
|---|---|---|
| `LAYOUT_TITLE` | Title slide (first slide only) | 0 |
| `LAYOUT_BLANK` | All other slides (content, section, closing) | 6 |

Layout selection by slide type:
- `act == "Title"` or `visual_type == "title"` → `LAYOUT_TITLE` (index 0)
- `act == "Section break"` or `visual_type == "section"` → `LAYOUT_BLANK` (index 6), accent background applied
- All others (content, closing, Q&A) → `LAYOUT_BLANK` (index 6)

---

## Theme Specifications

### corporate (default)

```python
BACKGROUND_COLOR = "FFFFFF"   # white
ACCENT_COLOR     = "1B3A6B"   # navy
TEXT_COLOR       = "222222"   # near-black
FONT_TITLE       = "Calibri"
FONT_BODY        = "Calibri"
FONT_SIZE_TITLE  = 36          # pt
FONT_SIZE_BODY   = 20          # pt
FONT_SIZE_SMALL  = 14          # pt (footer, notes)
```

### minimal

```python
BACKGROUND_COLOR = "FFFFFF"
ACCENT_COLOR     = "333333"
TEXT_COLOR       = "333333"
FONT_TITLE       = "Arial"
FONT_BODY        = "Arial"
```

### dark

```python
BACKGROUND_COLOR = "1A1A2E"
ACCENT_COLOR     = "00D4FF"
TEXT_COLOR       = "F0F0F0"
FONT_TITLE       = "Calibri"
FONT_BODY        = "Calibri"
```

### vibrant

```python
BACKGROUND_COLOR = "FFFFFF"
ACCENT_COLOR     = "7B2FBE"
TEXT_COLOR       = "1A1A1A"
FONT_TITLE       = "Segoe UI"
FONT_BODY        = "Segoe UI"
```

---

## Slide Composition Rules

**Text limits (design guidelines):**
- Title: max 10 words
- Subtitle / message: max 20 words
- Body bullets: max 5 bullets, max 8 words each
  - Note: the builder currently enforces only the *number* of body bullets (max 5). It does **not** automatically trim or validate title/subtitle word counts or the "max 8 words per bullet" guideline.

**Visual placeholder format:**
```
┌─────────────────────────────────────────┐
│  [CHART: Revenue Trend Q1–Q4 2026]      │
│  Replace with actual data visualization │
└─────────────────────────────────────────┘
```
- Background: light gray (`EEEEEE`)
- Border: 1pt, accent color
- Label: 12pt italic, centered

**Slide numbers:**
- Position: bottom-right, 11pt, `TEXT_COLOR` at 50% opacity
- Omit on title slide (`slide_number == 1`)

**Footer (optional):**
- Position: bottom-center, 10pt
- Content: `<project_title> | Confidential` or omit if not specified

---

## python-pptx Dimensions Reference

Default slide size (widescreen 16:9):
```python
from pptx.util import Inches, Pt
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
```

Common element positions (inches from top-left):
```python
# Title area
title_left   = Inches(0.5)
title_top    = Inches(0.4)
title_width  = Inches(12.33)
title_height = Inches(1.2)

# Body area
body_left    = Inches(0.5)
body_top     = Inches(1.8)
body_width   = Inches(12.33)
body_height  = Inches(5.0)

# Placeholder rectangle (chart/diagram)
ph_left      = Inches(1.0)
ph_top       = Inches(2.0)
ph_width     = Inches(11.33)
ph_height    = Inches(4.5)
```

---

## Dependency

```bash
pip install python-pptx
```

Minimum version: `python-pptx >= 0.6.21`
