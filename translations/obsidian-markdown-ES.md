# Obsidian Markdown

Skill para crear, normalizar y reparar notas Markdown compatibles con Obsidian.

## Proposito

Garantizar que las notas rendericen correctamente en Obsidian usando Properties YAML validas, tareas checkbox, callouts y wikilinks.

## Estructura

```text
obsidian-markdown/
  SKILL.md
  references/
    frontmatter-schema.md
    obsidian-callouts.md
    obsidian-task-conventions.md
    obsidian-linking-rules.md
    obsidian-validation-checklist.md
    templates-prd-handoff-meeting.md
```

## Funcionalidades principales

- Validacion estricta de frontmatter (sin tabs, indentacion valida)
- Normalizacion de markdown para documentos operativos
- Estandar de tareas checkbox (`- [ ]`, `- [x]`)
- Patrones de callouts para contexto/riesgo/pendientes
- Enlaces internos con wikilinks
- Plantillas listas para uso (PRD, handoff, reunion)

## Casos de uso tipicos

- Corregir frontmatter roto en Obsidian
- Convertir markdown generico a formato Obsidian
- Estandarizar PRD diarios y handoffs
- Anadir trazabilidad operativa con tareas y callouts
