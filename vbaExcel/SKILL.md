---
name: vbaExcel
description: Extract and re-import VBA code from Excel .xlsm files on Windows using Python (pywin32/oletools) or VBScript. Use it to export .bas modules, refactor in VS Code, and import changes back into the XLSM.
---

# vbaExcel

## Quick Usage

1. Export VBA code to `.bas` files.
2. Refactor the `.bas` files.
3. Re-import them into the `.xlsm`.

## Recommended Workflow

### 1) Export VBA

- Run the export script at `scripts/export_vba.py`.
- If VBA access fails, enable `AccessVBOM` using `scripts/enable_vba_access.reg`.

### 2) Refactor

- Edit the `.bas` files in VS Code (or in the VBA editor).

### 3) Re-import

- Run `scripts/import_vba.py` to replace each module's code.

## Important Notes

- Excel must be installed.
- Close Excel before exporting or importing.
- Always create an XLSM backup before importing changes.

## Included Scripts

- `scripts/export_vba.py`: exports VBA to `.bas` files via VBScript and COM.
- `scripts/import_vba.py`: imports `.bas` files back into the XLSM via COM.
- `scripts/enable_vba_access.reg`: enables programmatic access to VBA.

## When to Use This Skill

- You want to extract VBA code for refactoring.
- You want to automate importing VBA code back into an XLSM.
- VBProject access is blocked and you need to enable it.
