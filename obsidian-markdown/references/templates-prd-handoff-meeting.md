# Templates: PRD, Handoff, Meeting

## PRD Daily

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

- [x] Ejemplo tarea cerrada

## Tareas pendientes

- [ ] P1 - Pendiente
```

## Handoff

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

## Contexto

...

## Acciones

- [ ] Paso 1
- [ ] Paso 2
```

## Meeting Note

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

## Acciones

- [ ] Responsable X - tarea
```
