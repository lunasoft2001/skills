# Excel Analyzer Skill Bundle

This document describes the contents of the `vbaExcel` skill in this repository.

## Structure

```text
vbaExcel/
  SKILL.md                        # Skill metadata (vbaExcel)
  INSTALL.txt                     # Quick install and usage notes
  scripts/                        # PowerShell/Python helper scripts
    export_vba.py                 # Export VBA modules to .bas files
    import_vba.py                 # Import .bas files back into .xlsm
    enable_vba_access.reg         # Enable programmatic VBOM access
```

## Installation

To install this skill in GitHub Copilot, copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "vbaExcel" -Destination "$env:USERPROFILE\.copilot\skills\vbaExcel" -Recurse
```

Then restart VS Code.

## Notes

- This bundle is focused on VBA extraction and re-import for Excel `.xlsm` files on Windows.
- Close Excel before export/import operations.
- Always create a backup of your workbook before importing VBA changes.

