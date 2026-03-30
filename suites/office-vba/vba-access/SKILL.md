---
name: vba-access
description: "Extract, refactor, and re-import VBA modules (standard modules and class modules) from Microsoft Access databases (.accdb/.mdb) on Windows using Python and COM automation. Use when: exporting Access VBA code to .bas files for version control or editing in VS Code, importing refactored .bas files back into an Access database, enabling VBA project access in Access. Always creates a verified backup before any import — flow stops if no backup exists. Note: for full database analysis (tables, queries, forms, reports), use the access-analyzer skill instead. Triggers on: export VBA Access, import VBA Access, vba-access, Access VBA modules, accdb VBA, extraer módulos VBA Access, importar VBA Access, refactorizar VBA Access, módulos VBA Access, Access automation."
---

# vba-access

Export, refactor, and re-import VBA modules from Access `.accdb` / `.mdb` files on Windows.

> **Scope:** This skill handles VBA code (standard and class modules) only. For full database analysis — tables, queries, forms, reports, macros — use the **access-analyzer** skill.

## ⚠️ Mandatory Safety Rule

**No import or overwrite without a verified backup.**  
If no recent backup of the `.accdb` exists, stop and create one before proceeding. This rule is not optional.

## Recommended Workflow

```
healthcheck → backup → export → refactor → import → validate
```

### 1. Healthcheck
- Confirm Access is installed and the `.accdb` file is accessible.
- Verify VBA project access is enabled (see [access-vba-patterns.md](./references/access-vba-patterns.md)).
- Close all Access instances and ensure no `.laccdb` lock file exists.

### 2. Backup
```powershell
Copy-Item "MyApp.accdb" "MyApp_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').accdb"
```
> Do not skip. Import overwrites modules and cannot be undone.

### 3. Export VBA Modules
```bash
python scripts/export_vba_access.py MyApp.accdb ./exported_vba/
```
Exports all standard (`.bas`) and class (`.cls`) modules in the database.

### 4. Refactor
Edit `.bas` / `.cls` files in VS Code. Keep module names unchanged between export and import.

### 5. Import VBA Modules
```bash
python scripts/import_vba_access.py MyApp.accdb ./exported_vba/
```
The script **automatically creates a new backup** immediately before importing. Replaces matching modules in the database.

### 6. Validate
- Open `MyApp.accdb` in Access.
- Test the affected forms or run the affected modules.
- Open the VBA editor (Alt+F11) and verify no compile errors.

## Important Notes

- **Always close Access** before running export or import scripts.
- Module names must match exactly between export and import.
- Form and report code modules (behind forms) are **not** exported by this skill — use **access-analyzer** for those.
- Ensure "Trust access to the VBA project object model" is enabled in Access Trust Center.

## Included Scripts

- `scripts/export_vba_access.py` — exports standard and class modules via COM to `.bas` / `.cls` files.
- `scripts/import_vba_access.py` — imports `.bas` / `.cls` files back into the `.accdb` via COM, creating a backup first.

## References

- [access-vba-patterns.md](./references/access-vba-patterns.md) — enabling VBOM access, module types, DAO/ADO patterns, and common Access VBA patterns.

---
*Part of the [Office VBA Suite](https://github.com/lunasoft2001/skills) · MIT License*
