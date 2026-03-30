# Office VBA Orchestrator Skill Bundle

This document describes the contents of the `office-vba-orchestrator` skill in this repository.

## Structure

```text
suites/office-vba/office-vba-orchestrator/
  SKILL.md                        # Skill metadata (office-vba-orchestrator)
  references/
    routing-guide.md              # File type detection and skill routing logic
    backup-policy.md              # Mandatory backup policy and rollback procedures
```

## Purpose

Route Office VBA tasks to the correct per-application skill (vbaExcel, vba-word, vba-powerpoint, vba-access) and enforce the mandatory backup-before-import safety policy across the entire Office VBA suite.

## When to Use

- When the user mentions an Office VBA task but has not specified which application.
- When working with multiple Office file types in the same session.
- To get a quick reference on which skill handles which file type.
- To enforce the backup policy before any destructive operation.

## Supported Skills

| File type | Application | Skill |
|-----------|-------------|-------|
| `.xlsm`, `.xlam`, `.xltm` | Excel | `vbaExcel` |
| `.docm`, `.dotm` | Word | `vba-word` |
| `.pptm`, `.potm` | PowerPoint | `vba-powerpoint` |
| `.accdb`, `.mdb` | Access | `vba-access` |
| Outlook | — | ❌ Not supported |

## Installation

Copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "office-vba-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\office-vba-orchestrator" -Recurse
```

Then restart VS Code.

## Notes

- All sub-skills (`vba-word`, `vba-powerpoint`, `vba-access`, `vbaExcel`) must also be installed.
- The orchestrator enforces the universal backup policy defined in `references/backup-policy.md`.
- Outlook VBA is explicitly excluded from this suite.
