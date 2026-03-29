# Word VBA Skill Bundle

This document describes the contents of the `vba-word` skill in this repository.

## Structure

```text
vba-word/
  SKILL.md                        # Skill metadata (vba-word)
  references/
    word-vba-patterns.md          # VBA component types, events, and common patterns
  scripts/
    export_vba_word.py            # Export VBA modules to .bas/.cls files
    import_vba_word.py            # Import .bas/.cls files back into .docm
```

## Purpose

Extract all VBA modules from Word macro-enabled documents (`.docm` / `.dotm`),
refactor them in VS Code, and safely re-import them — always creating a
timestamped backup before any import.

## Installation

Copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Then restart VS Code.

## Notes

- Requires Windows + Microsoft Word installed.
- Enable "Trust access to the VBA project object model" in Word Trust Center.
- Always close Word before running export or import scripts.
- A backup of the `.docm` is created automatically before any import.
- Part of the **Office VBA Suite** — use `office-vba-orchestrator` to route between skills.
