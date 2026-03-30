---
name: presentation-factory-orchestrator
description: End-to-end orchestrator for creating professional presentations. Routes the full pipeline across four stages — storyboard → pptx-builder → speaker-notes → bundle-manager — and validates minimum inputs before starting. Use when the user wants to create a complete presentation package, build a deck from scratch, or produce a full presentation bundle with slides and speaker guide. Triggers on: "create a presentation", "make a deck", "build slides", "full presentation package", "crea una presentación", "prepara un deck", "necesito diapositivas", "armá una presentación completa".
license: MIT
author: lunasoft2001 <https://github.com/lunasoft2001>
---

# Presentation Factory — Orchestrator

Route the full presentation pipeline, validate inputs, and coordinate all four sub-skills to deliver a complete `/deliverables/<slug>/` bundle.

## Minimum Required Inputs

Before starting the pipeline, collect these four fields. Use `vscode_askQuestions` if any are missing:

| Field | Description | Example |
|-------|-------------|---------|
| `topic` | Core subject of the presentation | "Q2 2026 Product Roadmap" |
| `audience` | Who will attend and their expertise level | "C-suite, non-technical" |
| `duration` | Target presentation length in minutes | 20 |
| `slug` | Short identifier for output folder (lowercase, hyphens) | `q2-roadmap-2026` |

Optional but recommended:
- `key_messages` — up to 5 bullet points the audience must remember
- `style` — tone/style preference (e.g., corporate, storytelling, educational)
- `language` — output language (default: same as user input)

## Pipeline Stages

Run stages sequentially. Confirm completion of each before proceeding to the next.

```
Stage 1: presentation-storyboard
  → Input: topic, audience, duration, key_messages, style, language
  → Output: storyboard.docx  (human-readable, saved to /deliverables/<slug>/)
            storyboard.json  (machine-readable, direct input to Stage 2 — no conversion needed)

Stage 2: presentation-pptx-builder
  → Input: storyboard from Stage 1
  → Output: deck.pptx saved to /deliverables/<slug>/

Stage 3: presentation-speaker-notes
  → Input: storyboard from Stage 1
  → Output: speaker-notes.docx saved to /deliverables/<slug>/

Stage 4: presentation-bundle-manager
  → Input: all files in /deliverables/<slug>/
  → Output: index.xlsx + manifest.json in /deliverables/<slug>/
```

## Orchestration Rules

- **Validate before starting**: if `topic`, `audience`, `duration`, or `slug` are missing, ask for them using `vscode_askQuestions`. Do not proceed without all four.
- **Slug sanitization**: auto-convert `slug` to lowercase with hyphens if the user provides it in another format (e.g., "Q2 Roadmap 2026" → `q2-roadmap-2026`).
- **Stage failures**: if a stage fails or produces incomplete output, surface the error to the user and offer to retry that stage before continuing.
- **Progress reporting**: after each stage, confirm what was produced and where it was saved before moving to the next.
- **Partial runs**: if the user only wants specific stages (e.g., "just build the PPTX"), route directly to that sub-skill without forcing the full pipeline.

## Output Structure

All deliverables land in a single project folder:

```
/deliverables/<slug>/
  storyboard.docx       ← Stage 1
  deck.pptx             ← Stage 2
  speaker-notes.docx    ← Stage 3
  index.xlsx            ← Stage 4
  manifest.json         ← Stage 4
```

## Status Summary Format

After the full pipeline completes, output:

```
## ✅ Presentation Package Ready

**Project**: <topic>
**Slug**: <slug>
**Folder**: /deliverables/<slug>/

| File | Status | Notes |
|------|--------|-------|
| storyboard.docx | ✅ Created | <N> slides |
| deck.pptx | ✅ Created | <N> slides |
| speaker-notes.docx | ✅ Created | <total_time> min script |
| index.xlsx | ✅ Created | |
| manifest.json | ✅ Created | |
```

## Limitations

- This skill orchestrates; the actual file generation is handled by the four sub-skills.
- Does not submit or publish to any external service.
- Requires Python 3.9+ if using the bundle-manager script.
- See `references/pipeline-stages.md` for detailed stage contracts and error codes.
