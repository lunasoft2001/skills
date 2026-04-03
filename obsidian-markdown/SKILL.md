---
name: obsidian-markdown
description: Build, normalize, and validate Obsidian-ready Markdown notes with strict YAML frontmatter, checkbox task blocks, callouts, wikilinks, and vault-safe linking rules. Use when users ask to format notes for Obsidian, fix broken frontmatter, convert plain markdown into Obsidian style, add Properties fields, or standardize templates for daily logs, PRDs, handoffs, and operational docs.
license: MIT
author: lunasoft2001 <https://github.com/lunasoft2001>
---

# Obsidian Markdown

Create and repair Markdown so it renders cleanly in Obsidian with valid Properties, stable callouts, task lists, and internal links.

## Core Capabilities

1. Generate new Obsidian-first documents from scratch.
2. Repair broken frontmatter (tabs, invalid lists, missing delimiters, malformed keys).
3. Convert generic Markdown into structured Obsidian templates.
4. Normalize task tracking with checkbox blocks and status tags.
5. Add internal navigation with wikilinks and short index sections.
6. Enforce predictable section layouts for recurring workflows (PRD, handoff, summary, meeting notes).

## Trigger Phrases

Use this skill when the user asks for any of these intents:

- format for obsidian
- fix frontmatter
- validate yaml properties
- convert markdown to obsidian style
- add callouts and checkboxes
- create obsidian template
- prepare daily note/prd for obsidian

## Mandatory Rules

1. Frontmatter must be at the top of file and wrapped exactly with `---` opening and closing lines.
2. YAML indentation must use spaces only (never tabs).
3. YAML list indentation standard: 2 spaces.
4. Keep keys stable and machine-friendly: `snake_case`.
5. Use `tags` as YAML list (not comma-separated text).
6. Include at least one checkbox section for actionable items.
7. Include at least one callout (`[!info]`, `[!warning]`, `[!todo]`, `[!tip]`) when context matters.
8. Prefer wikilinks (`[[...]]`) for vault-internal references.
9. For external systems (GitHub, Trello, URLs), use regular links.
10. Avoid breaking existing content semantics when normalizing format.

## Recommended Properties Schema

Minimum for operational notes:

```yaml
---
type: note
fecha: YYYY-MM-DD
estado: borrador
tags:
  - obsidian
---
```

Recommended extended schema:

```yaml
---
type: prd-diario
fecha: YYYY-MM-DD
dia: Viernes
estado: en-curso
tags:
  - prd
  - diario
  - trabajo
sistema: ops
prioridad: media
owner: juanjo
---
```

## Document Blueprints

### A) Daily PRD Blueprint

```markdown
---
type: prd-diario
fecha: YYYY-MM-DD
dia: Viernes
estado: en-curso
tags:
  - prd
  - diario
  - trabajo
---

# PRD Diario - DD/MM/YYYY

> [!info] Estado general
> Completadas: 0
> En curso: 0
> Pendientes: 0

## Tareas realizadas

- [x] Tarea cerrada de ejemplo

## Tareas en curso

- [ ] Tarea en curso de ejemplo

## Tareas pendientes

- [ ] P1 - Pendiente principal
- [ ] P2 - Pendiente secundaria

## Enlaces

- [[README]]
- [[../DAILY_WORK/YYMMDD/README]]
```

### B) Incident/Handoff Blueprint

```markdown
---
type: handoff
fecha: YYYY-MM-DD
estado: pendiente
tags:
  - handoff
  - incidente
---

# Handoff - Titulo

> [!warning] Riesgo
> Describir impacto si no se resuelve.

## Contexto

...

## Analisis

...

## Acciones

- [ ] Validar en remoto
- [ ] Confirmar con usuario

## Trazabilidad

- Trello: https://trello.com/c/xxxx
- Issue: https://github.com/owner/repo/issues/123
```

### C) Meeting Notes Blueprint

```markdown
---
type: meeting-note
fecha: YYYY-MM-DD
estado: final
tags:
  - meeting
  - notas
---

# Reunion - Tema

## Decisiones

- Decision 1
- Decision 2

## Acciones

- [ ] Responsable A - tarea 1
- [ ] Responsable B - tarea 2

## Referencias

- [[Nota relacionada]]
```

## Repair Workflow (for existing files)

When a file renders incorrectly in Obsidian, run this sequence:

1. Detect frontmatter boundaries.
2. Fix invalid indentation (replace tabs with spaces in YAML block).
3. Ensure YAML keys and list syntax are valid.
4. Normalize `tags` into list form.
5. Ensure at least one actionable checkbox section exists.
6. Add callout for context if missing.
7. Validate that preview no longer shows red YAML/error formatting.

## Output Requirements

Every final output should include:

1. Valid frontmatter.
2. Stable headings.
3. At least one checkbox block.
4. Clean internal links where applicable.
5. No YAML parse warnings.

## Quick Validation Checklist

- Frontmatter starts at line 1.
- Opening `---` and closing `---` both present.
- No tabs in frontmatter.
- `tags` is YAML list.
- At least one callout present when note has status/risk/context.
- At least one task list present for operational notes.

## Reference Files

- `references/frontmatter-schema.md`
- `references/obsidian-callouts.md`
- `references/obsidian-task-conventions.md`
- `references/obsidian-linking-rules.md`
- `references/obsidian-validation-checklist.md`
- `references/templates-prd-handoff-meeting.md`
