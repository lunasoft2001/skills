---
name: presentation-speaker-notes
description: Generates a detailed speaker script for each slide — including per-slide talking points, timing cues, transition phrases, and probable Q&A with suggested answers. Use when the user needs speaker notes, a presenter guide, a talk script, rehearsal notes, or Q&A preparation for a presentation. Triggers on: "write speaker notes", "create a talk script", "generate presenter notes", "Q&A preparation", "rehearsal guide", "timing for my slides", "escribe las notas del presentador", "guión por slide", "prepara el script de la presentación", "notas de orador".
license: MIT
author: lunasoft2001 <https://github.com/lunasoft2001>
---

# Presentation Speaker Notes

Generate a complete presenter script from a storyboard. Output is a speaker-notes document with per-slide talking points, timing, transitions, and a Q&A section.

## Required Inputs

| Field | Source | Description |
|-------|--------|-------------|
| `storyboard` | `storyboard.docx` / Markdown | Slide structure from `presentation-storyboard` |
| `slug` | User / orchestrator | Output folder identifier |
| `speaker_style` | Optional | `conversational` (default) / `formal` / `storytelling` |
| `language` | Optional | Script language (default: user's language) |

## Per-Slide Notes Format

For each slide, produce:

```
---
### Slide <N>: <Title>
**Timing**: ~<X> min  (cumulative: <Y> min elapsed)
**Cue**: [advance from previous slide / pause / click to reveal]

**Script**:
<2–4 sentences to say out loud. Written as natural speech, not bullet points.
Match the speaker_style. Avoid reading the slide — complement what's on screen.>

**Key emphasis**: *<the one phrase to stress or pause on>*

**Transition to next slide**:
"<Bridging sentence that sets up Slide N+1>"
```

## Full Document Structure

```markdown
# Speaker Notes: <topic>

**Presenter**: [fill in]
**Date**: [fill in]
**Venue / Format**: [fill in]
**Total runtime**: ~<N> min

---
## Pre-presentation checklist
- [ ] Test slides on the room's display
- [ ] Confirm clicker / remote is working
- [ ] Have a glass of water ready
- [ ] Know the first sentence by heart — start confident

---
## Slide-by-Slide Script

[per-slide notes...]

---
## Q&A Guide

### Probable Questions
[5–8 questions with suggested answers — see rules below]

### Closing Statement
<2–3 sentences to close the Q&A and thank the audience>
```

## Q&A Section Rules

- Generate 5–8 probable questions based on the storyboard content, audience, and topic.
- For each question: provide a 2–4 sentence suggested answer, plus a deflection phrase if the answer is outside scope.
- Flag questions that touch sensitive areas (budget, headcount, risk) with ⚠️ and suggest a diplomatic framing.

```
**Q**: <question>
**A**: <suggested answer>
**If out of scope**: "That's an important point — let me follow up on that after the session."
```

## Timing Rules

- Default pace: 120 words per minute for conversational style, 100 wpm for formal.
- Warn if any slide's script exceeds its allocated `duration` from the storyboard.
- Add a ⏱️ warning if total script time diverges from `duration` by more than 10%.

## Output

Save to: `/deliverables/<slug>/speaker-notes.docx`

Use the `docx` skill to produce the `.docx` file if available; otherwise produce the Markdown source.

## Limitations

- Scripts are suggestions — the presenter should personalize them.
- Does not record or practice delivery — use rehearsal tools for that.
- Q&A questions are probabilistic, not exhaustive.
- See `references/notes-format-guide.md` for style rules and timing benchmarks.
