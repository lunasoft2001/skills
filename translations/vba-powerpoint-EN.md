# PowerPoint VBA Skill Bundle

This document describes the contents of the `vba-powerpoint` skill in this repository.

## Structure

```text
vba-powerpoint/
  SKILL.md                        # Skill metadata (vba-powerpoint)
  references/
    ppt-vba-patterns.md           # VBA component types, events, and common patterns
  scripts/
    export_vba_ppt.py             # Export VBA modules to .bas/.cls files
    import_vba_ppt.py             # Import .bas/.cls files back into .pptm
```

## Purpose

Extract all VBA modules from PowerPoint macro-enabled presentations (`.pptm` / `.potm`), refactor them in VS Code, and safely re-import them — always creating a timestamped backup before any import.

## Installation

Copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "vba-powerpoint" -Destination "$env:USERPROFILE\.copilot\skills\vba-powerpoint" -Recurse
```

Then restart VS Code.

## Notes

- Requires Windows + Microsoft PowerPoint installed.
- Enable "Trust access to the VBA project object model" in PowerPoint Trust Center.
- PowerPoint COM automation may require the application to be visible — scripts handle this automatically.
- Always close PowerPoint before running export or import scripts.
- A backup of the `.pptm` is created automatically before any import.
- Part of the **Office VBA Suite** — use `office-vba-orchestrator` to route between skills.
