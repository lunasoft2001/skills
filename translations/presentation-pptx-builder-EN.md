# Presentation PPTX Builder

This document describes the `presentation-pptx-builder` skill.

## Description

Generates a `.pptx` presentation file from a storyboard using `python-pptx`. Applies a clean professional layout with four available themes (corporate, minimal, dark, vibrant). Inserts labeled placeholders for charts and diagrams instead of fabricating data.

## Triggers

`build the pptx`, `generate the deck`, `create the PowerPoint`, `make the slides file`, `produce the .pptx`

## Themes

| Theme | Style |
|-------|-------|
| `corporate` | White + Navy — default for business |
| `minimal` | White + Charcoal — clean and simple |
| `dark` | Dark + Cyan — tech and modern |
| `vibrant` | White + Purple — creative and bold |

## Usage

```bash
python3 scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

## Requirements

- Python 3.9+
- `pip install python-pptx`

## Structure

```
presentation-pptx-builder/
  SKILL.md
  scripts/
    build_pptx.py
  evals/
    evals.json
  references/
    pptx-design-guide.md
```
