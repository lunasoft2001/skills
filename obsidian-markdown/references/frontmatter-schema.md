# Frontmatter Schema

Use these fields as defaults for Obsidian operational notes.

## Minimal Schema

```yaml
---
type: note
fecha: YYYY-MM-DD
estado: borrador
tags:
  - obsidian
---
```

## Extended Operational Schema

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
owner: juanjo
prioridad: media
sistema: ops
---
```

## Rules

1. Keep frontmatter at top of file.
2. Never use tabs in YAML.
3. Use 2-space indentation for list items.
4. Keep key names stable (snake_case).
