---
name: office-vba-orchestrator
description: "Route Office VBA tasks to the correct per-application skill (vba-word, vba-powerpoint, vba-access, vbaExcel) and enforce the mandatory backup-before-import policy for all Office macro-enabled files. Use when the user mentions any Office VBA task without specifying which skill to use, when working with mixed Office file types, or when you need to remind the user of the backup policy. Explicitly excludes Outlook VBA. Triggers on: Office VBA, VBA suite, which VBA skill, office macros, VBA workflow, extraer VBA Office, importar VBA Office, macros Office, .xlsm .docm .pptm .accdb VBA, suite VBA, orchestrate VBA skills."
---

# office-vba-orchestrator

Detect the target Office application and route to the correct VBA skill, always enforcing the backup-first policy.

## ⚠️ Universal Backup Policy (Mandatory)

> **No import, overwrite, or destructive operation without a verified backup.**  
> If the user has not confirmed a recent backup, **stop the flow and perform the backup step first** before proceeding with any import or rewrite.

This policy applies to ALL skills in the Office VBA suite.

## Routing Table

| File type | Application | Skill to activate |
|-----------|-------------|-------------------|
| `.xlsm`, `.xlam`, `.xltm` | Excel | **vbaExcel** |
| `.docm`, `.dotm` | Word | **vba-word** |
| `.pptm`, `.potm` | PowerPoint | **vba-powerpoint** |
| `.accdb`, `.mdb` | Access | **vba-access** |
| Outlook (`.otm`) | — | ❌ **Not supported** — excluded from this suite |

## Decision Flow

```
1. Identify file type from user message or file path
2. Check routing table → select skill
3. Verify backup exists → if not, pause and backup first
4. Delegate to the selected skill's recommended workflow:
   healthcheck → backup → export → refactor → import → validate
```

## Per-Skill Quick Reference

### vbaExcel — Excel `.xlsm`
- Export: `python scripts/export_vba.py workbook.xlsm ./exported_vba/`
- Import: `python scripts/import_vba.py workbook.xlsm ./exported_vba/` *(backup first)*
- Enable VBOM: `scripts/enable_vba_access.reg`

### vba-word — Word `.docm`
- Export: `python scripts/export_vba_word.py MyDoc.docm ./exported_vba/`
- Import: `python scripts/import_vba_word.py MyDoc.docm ./exported_vba/` *(backup automatic)*

### vba-powerpoint — PowerPoint `.pptm`
- Export: `python scripts/export_vba_ppt.py Deck.pptm ./exported_vba/`
- Import: `python scripts/import_vba_ppt.py Deck.pptm ./exported_vba/` *(backup automatic)*

### vba-access — Access `.accdb` (VBA modules only)
- Export: `python scripts/export_vba_access.py MyApp.accdb ./exported_vba/`
- Import: `python scripts/import_vba_access.py MyApp.accdb ./exported_vba/` *(backup automatic)*
- Full DB analysis: use **access-analyzer** instead

## Backup Command (Universal)
```powershell
# Works for any Office file
$file = "path\to\YourFile.xlsm"  # or .docm / .pptm / .accdb
Copy-Item $file ($file -replace '\.\w+$', "_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss')$([System.IO.Path]::GetExtension($file))")
```

## Common Scenarios

**"I want to refactor VBA in my Excel workbook"** → Use **vbaExcel**.

**"Export macros from my Word document"** → Use **vba-word**.

**"Edit PowerPoint slide macros in VS Code"** → Use **vba-powerpoint**.

**"Clean up Access VBA modules"** → Use **vba-access** (VBA only) or **access-analyzer** (full DB).

**"I have an .xlsm and a .docm to process"** → Run each skill independently; backup both files first.

## References

- [routing-guide.md](./references/routing-guide.md) — detailed routing logic and file type detection.
- [backup-policy.md](./references/backup-policy.md) — full backup policy, verification checklist, and rollback procedures.

---
*Part of the [Office VBA Suite](https://github.com/lunasoft2001/skills) · MIT License*
