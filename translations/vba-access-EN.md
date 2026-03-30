# Access VBA Skill Bundle

This document describes the contents of the `vba-access` skill in this repository.

## Structure

```text
suites/office-vba/vba-access/
  SKILL.md                        # Skill metadata (vba-access)
  references/
    access-vba-patterns.md        # VBA component types, DAO/ADO patterns, and troubleshooting
  scripts/
    export_vba_access.py          # Export standard/class VBA modules to .bas/.cls files
    import_vba_access.py          # Import .bas/.cls files back into .accdb
```

## Purpose

Extract standard and class VBA modules from Access databases (`.accdb` / `.mdb`), refactor them in VS Code, and safely re-import them — always creating a timestamped backup before any import.

> **Note:** This skill handles VBA modules only. For full database analysis (tables, queries, forms, reports), use the **access-analyzer** skill.

## Installation

Copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "vba-access" -Destination "$env:USERPROFILE\.copilot\skills\vba-access" -Recurse
```

Then restart VS Code.

## Notes

- Requires Windows + Microsoft Access installed.
- Enable "Trust access to the VBA project object model" in Access Trust Center.
- Always close Access and ensure no `.laccdb` lock file exists before running scripts.
- A backup of the `.accdb` is created automatically before any import.
- Part of the **Office VBA Suite** — use `office-vba-orchestrator` to route between skills.
