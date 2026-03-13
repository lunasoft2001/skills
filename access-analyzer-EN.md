# Access Analyzer Skill Bundle

This document describes the contents of the `access-analyzer` skill in this repository.

## Structure

```text
access-analyzer/
  SKILL.md                        # Skill metadata
  scripts/                        # PowerShell automation scripts
    access-backup.ps1             # Create backups
    access-export-git.ps1         # Export with Git integration
    access-import-changed.ps1     # Import only changed objects
    access-import.ps1             # Import all objects
  references/                     # Reference documentation
    AccessObjectTypes.md          # Access object types
    ExportTodoSimple.bas          # VBA export module
    VBA-Patterns.md               # VBA code patterns
  assets/                         # Skill assets
    AccessAnalyzer.accdb          # Sample/template database
```

## Installation

To install this skill in GitHub Copilot, copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "access-analyzer" -Destination "$env:USERPROFILE\.copilot\skills\access-analyzer" -Recurse
```

Then restart VS Code.

## Notes

- This bundle is optimized for GitHub Copilot.
- It includes only the essential skill files.
- `AccessAnalyzer.accdb` is provided in `assets/` as a support resource.
