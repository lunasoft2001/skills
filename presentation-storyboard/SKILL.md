---
name: presentation-storyboard
description: Structures the narrative arc of a presentation slide by slide. For each slide produces a message, objective, recommended duration, and suggested visual. Use when the user wants to plan a presentation, outline slides, define the story arc, create a storyboard, or structure a deck before building it. Triggers on: "storyboard a presentation", "plan my slides", "structure my deck", "outline the presentation", "define slide flow", "planea mis diapositivas", "estructura la presentación", "arma el guión de slides", "define el hilo narrativo".
---

# Presentation Storyboard

Build a slide-by-slide narrative structure before any visual is created. Output is a storyboard document that feeds `presentation-pptx-builder` and `presentation-speaker-notes`.

## Required Inputs

Collect the following before generating. Use `vscode_askQuestions` if any are missing:

| Field | Required | Description |
|-------|----------|-------------|
| `topic` | ✅ | Presentation subject |
| `audience` | ✅ | Who attends and their context |
| `duration` | ✅ | Total length in minutes |
| `key_messages` | Recommended | Up to 5 core takeaways |
| `style` | Optional | Tone: corporate / storytelling / educational / pitch |
| `language` | Optional | Output language (default: user's language) |

## Storyboard Generation Rules

1. **Calculate slide budget**: use ~2 minutes per content slide, 1 minute for title/closing.
2. **Apply a 3-act narrative arc**:
   - **Act 1 — Context** (≈20% of slides): Why this matters / the problem
   - **Act 2 — Content** (≈60% of slides): Data, analysis, solutions, story
   - **Act 3 — Action** (≈20% of slides): Recommendations, next steps, Q&A
3. **One message per slide**: each slide has exactly one main message (the slide's headline).
4. **No filler slides**: every slide must earn its place. Combine or cut if needed.

## Per-Slide Output Format

For each slide, produce:

```
### Slide <N>: <Title>

**Act**: Context / Content / Action
**Message**: One sentence — the single takeaway from this slide.
**Objective**: What the audience should feel or understand after this slide.
**Duration**: ~X min
**Visual suggestion**: [chart type / photo / diagram / table / text-only] — brief description
**Transition note**: How this slide connects to the next (one sentence).
```

## Full Storyboard Document Format

```markdown
# Storyboard: <topic>

**Audience**: <audience>
**Total duration**: <N> min
**Slide count**: <N>
**Key messages**:
- <message 1>
- ...

---

## Act 1 — Context (<N> slides)

[slides...]

## Act 2 — Content (<N> slides)

[slides...]

## Act 3 — Action (<N> slides)

[slides...]

---

## Narrative Thread Summary

One paragraph explaining the red thread that connects all slides.
```

## Output

Save the storyboard to: `/deliverables/<slug>/storyboard.docx`

Use the `docx` skill to produce the `.docx` file if available; otherwise produce the Markdown source so the user can convert it.

## Quality Rules

- Every `key_message` must appear as a slide headline in Act 2 or Act 3.
- No slide should carry more than one concept.
- Visual suggestions must match the data type (never suggest a bar chart for a qualitative claim).
- If `duration` is under 5 min, limit to 4 slides max (title, problem, solution, call-to-action).
- If `duration` is over 45 min, recommend splitting into two modules.

## Limitations

- Does not generate actual images or graphics — only text descriptions.
- Does not produce the PPTX file — hand off to `presentation-pptx-builder`.
- See `references/slide-structure-guide.md` for narrative models and visual suggestion catalog.
