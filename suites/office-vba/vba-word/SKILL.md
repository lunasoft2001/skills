---
name: vba-word
description: "Extract, refactor, and re-import VBA code from Word macro-enabled documents (.docm) and templates (.dotm) on Windows using Python and COM automation. Use when: exporting Word VBA modules to .bas files for version control, editing Word macros in VS Code, importing refactored modules back into a .docm, enabling VBA project access in Word. Always creates a verified backup before any import — flow stops if no backup exists. Triggers on: export VBA Word, import VBA Word, vba-word, Word macros, docm VBA, extraer macros Word, importar VBA Word, refactorizar macros Word, módulos VBA Word, Word automation, backup docm."
---

# vba-word

Export, refactor, and re-import VBA modules from Word `.docm` / `.dotm` files on Windows.

## ⚠️ Mandatory Safety Rule

**No import or overwrite without a verified backup.**  
If no recent backup of the `.docm` exists, stop and create one before proceeding. This rule is not optional.

## Recommended Workflow

```
healthcheck → backup → export → refactor → import → validate
```

### 1. Healthcheck
- Confirm Word is installed and the `.docm` file is accessible.
- Verify VBA project access is enabled (see [word-vba-patterns.md](./references/word-vba-patterns.md)).
- Close all Word instances.

### 2. Backup
```powershell
Copy-Item "MyDoc.docm" "MyDoc_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').docm"
```
> Do not skip. Import overwrites modules and cannot be undone.

### 3. Export VBA
```bash
python scripts/export_vba_word.py MyDoc.docm ./exported_vba/
```
Each VBA component is exported as a `.bas` or `.cls` file.

### 4. Refactor
Edit `.bas` / `.cls` files in VS Code. Keep module names unchanged between export and import.

### 5. Import VBA
```bash
python scripts/import_vba_word.py MyDoc.docm ./exported_vba/
```
The script **automatically creates a new backup** immediately before importing. Replaces matching modules in the document.

### 6. Validate
- Open `MyDoc.docm` in Word.
- Run a macro and confirm expected behaviour.
- Open the VBA editor (Alt+F11) and verify no compile errors.

## Important Notes

- **Always close Word** before running export or import scripts.
- Module names must match exactly between export and import.
- `ThisDocument` module is exported as `.cls` — edit carefully; it is the document event handler.
- `.dotm` templates follow the same workflow; substitute the file path.
- `UserForm` binary (`.frx`) is skipped — only text code is exported/imported.

## Included Scripts

- `scripts/export_vba_word.py` — exports all VBA components via COM to `.bas` / `.cls` files.
- `scripts/import_vba_word.py` — imports `.bas` / `.cls` files back into the `.docm` via COM, creating a backup first.

## References

- [word-vba-patterns.md](./references/word-vba-patterns.md) — component types, events, enabling VBOM access, and common Word VBA patterns.

---
*Part of the [Office VBA Suite](https://github.com/lunasoft2001/skills) · MIT License*
