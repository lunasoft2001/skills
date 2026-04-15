# mssql-second-brain — SQL Server to Obsidian Second Brain

## Description

Public skill that generates a complete Obsidian knowledge vault from SQL Server metadata. It extracts schemas, tables, views, procedures, and relationships using a local Python script (`pyodbc`) with zero AI tokens during extraction.

Optional AI step: create `_overview.md` from `_index.md` after generation.

## Structure

```text
mssql-second-brain/
  SKILL.md
  scripts/
    generate_second_brain.py
```

## Main Features

- SQL Server metadata extraction from `INFORMATION_SCHEMA` + `sys.*`
- One Markdown note per schema/table/view/procedure
- YAML frontmatter + wikilinks + reverse references ("Used by")
- Obsidian-ready folder layout for graph navigation
- Optional AI-generated conceptual overview file

## Typical Use Cases

- Database onboarding for new developers
- Building living architecture documentation
- Creating searchable internal knowledge bases
- Tracking table dependencies and FK topology

## Requirements

- Python 3
- `pyodbc`
- SQL Server network access
