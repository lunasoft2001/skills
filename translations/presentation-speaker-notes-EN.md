# Presentation Speaker Notes

This document describes the `presentation-speaker-notes` skill.

## Description

Generates a detailed speaker script for each slide: per-slide talking points, timing cues, transition phrases, and a Q&A section with probable audience questions and suggested answers.

## Triggers

`write speaker notes`, `create a talk script`, `generate presenter notes`, `Q&A preparation`, `rehearsal guide`, `timing for my slides`

## Per-Slide Output

- Timing + cumulative elapsed time
- Advance cue (click / pause / reveal)
- Natural-speech script (2–4 sentences)
- Key emphasis phrase
- Transition to next slide

## Q&A Section

- 5–8 probable questions with suggested answers
- Diplomatic framing for sensitive questions (budget, risk, headcount)
- Out-of-scope deflection phrases

## Speaking Pace

| Style | Pace |
|-------|------|
| Conversational | 120 wpm |
| Formal | 100 wpm |
| Storytelling | 110 wpm |

## Structure

```
suites/presentation/presentation-speaker-notes/
  SKILL.md
  evals/
    evals.json
  references/
    notes-format-guide.md
```

## Output File

`/deliverables/<slug>/speaker-notes.docx`
