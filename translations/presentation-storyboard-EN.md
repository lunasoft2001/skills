# Presentation Storyboard

This document describes the `presentation-storyboard` skill.

## Description

Structures the narrative arc of a presentation slide by slide. For each slide produces a message, objective, recommended duration, and suggested visual type. Applies a 3-act arc (Context / Content / Action) and enforces the one-message-per-slide rule.

## Triggers

`storyboard a presentation`, `plan my slides`, `structure my deck`, `outline the presentation`, `define slide flow`, `narrative arc for my talk`

## Output per Slide

- **Title** — slide heading
- **Message** — single key takeaway
- **Objective** — what the audience feels after this slide
- **Duration** — allocated time
- **Visual suggestion** — chart / diagram / photo / text-only
- **Transition note** — bridge to the next slide

## Structure

```
suites/presentation/presentation-storyboard/
  SKILL.md
  evals/
    evals.json
  references/
    slide-structure-guide.md
```

## Narrative Models

- Standard business (3-act)
- Pitch deck (investor)
- Educational / workshop
- Executive summary (10 min or less)

## Output File

`/deliverables/<slug>/storyboard.docx` (and `storyboard.json` for machine use)
