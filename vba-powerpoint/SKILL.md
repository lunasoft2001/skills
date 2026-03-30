---
name: vba-powerpoint
description: "Extract, refactor, and re-import VBA code from PowerPoint macro-enabled presentations (.pptm) and templates (.potm) on Windows using Python and COM automation. Use when: exporting PowerPoint VBA modules to .bas files for version control, editing presentation macros in VS Code, importing refactored modules back into a .pptm, enabling VBA project access in PowerPoint. Always creates a verified backup before any import — flow stops if no backup exists. Triggers on: export VBA PowerPoint, import VBA PowerPoint, vba-powerpoint, PowerPoint macros, pptm VBA, extraer macros PowerPoint, importar VBA PowerPoint, refactorizar macros PowerPoint, módulos VBA PowerPoint, PowerPoint automation, backup pptm."
---

# vba-powerpoint

Export, refactor, and re-import VBA modules from PowerPoint `.pptm` / `.potm` files on Windows.

## ⚠️ Mandatory Safety Rule

**No import or overwrite without a verified backup.**  
If no recent backup of the `.pptm` exists, stop and create one before proceeding. This rule is not optional.

## Recommended Workflow

```
healthcheck → backup → export → refactor → import → validate
```

### 1. Healthcheck
- Confirm PowerPoint is installed and the `.pptm` file is accessible.
- Verify VBA project access is enabled (see [ppt-vba-patterns.md](./references/ppt-vba-patterns.md)).
- Close all PowerPoint instances.

### 2. Backup
```powershell
Copy-Item "Deck.pptm" "Deck_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').pptm"
```
> Do not skip. Import overwrites modules and cannot be undone.

### 3. Export VBA
```bash
python scripts/export_vba_ppt.py Deck.pptm ./exported_vba/
```
Each VBA component is exported as a `.bas` or `.cls` file.

### 4. Refactor
Edit `.bas` / `.cls` files in VS Code. Keep module names unchanged between export and import.

### 5. Import VBA
```bash
python scripts/import_vba_ppt.py Deck.pptm ./exported_vba/
```
The script **automatically creates a new backup** immediately before importing. Replaces matching modules in the presentation.

### 6. Validate
- Open `Deck.pptm` in PowerPoint.
- Run a macro (Developer → Macros) and confirm expected behaviour.
- Open the VBA editor (Alt+F11) and verify no compile errors.

## Important Notes

- **Always close PowerPoint** before running export or import scripts.
- Module names must match exactly between export and import.
- `ThisPresentation` module is exported as `.cls` — edit carefully; it is the presentation event handler.
- `.potm` templates follow the same workflow; substitute the file path.
- `UserForm` binary (`.frx`) is skipped — only text code is exported/imported.
- **PowerPoint COM requires `Visible = True`** — unlike Word and Access, PowerPoint may briefly display a window during automation. This is a COM limitation, not a script error.

## Included Scripts

- `scripts/export_vba_ppt.py` — exports all VBA components via COM to `.bas` / `.cls` files.
- `scripts/import_vba_ppt.py` — imports `.bas` / `.cls` files back into the `.pptm` via COM, creating a backup first.

## References

- [ppt-vba-patterns.md](./references/ppt-vba-patterns.md) — component types, events, enabling VBOM access, and common PowerPoint VBA patterns.

---
*Part of the [Office VBA Suite](https://github.com/lunasoft2001/skills) · MIT License*
