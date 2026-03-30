# Office VBA Suite — Mandatory Backup Policy

## Policy Statement

> **No import, overwrite, or destructive operation on any Office macro-enabled file without a verified, recent backup.**

This policy applies unconditionally to all skills in the Office VBA suite:
- **vbaExcel** (`.xlsm`, `.xlam`, `.xltm`)
- **vba-word** (`.docm`, `.dotm`)
- **vba-powerpoint** (`.pptm`, `.potm`, `.ppsm`)
- **vba-access** (`.accdb`, `.mdb`)

---

## Why This Matters

VBA import operations overwrite existing module code directly in the binary file. If an import fails mid-way, the file may be left in a corrupted or partial state. There is **no undo** once modules are overwritten.

A verified backup is the only reliable rollback mechanism.

---

## Backup Verification Checklist

Before any import, confirm ALL of the following:

- [ ] A backup file exists with a timestamp in its name.
- [ ] The backup was created **after** the last known-good state of the file.
- [ ] The backup file size is non-zero and matches approximately the original.
- [ ] The backup is in a **different folder** from the source file (prevents accidental overwrite).
- [ ] The backup is **not** the original file renamed — it is a true copy.

If any item is unchecked → **stop, create the backup, then continue**.

---

## Creating a Backup (Universal Command)

```powershell
# PowerShell — works for any Office file type
$src = "C:\projects\MyApp.accdb"   # change to your file path
$ts  = Get-Date -Format "yyyyMMdd_HHmmss"
$dst = [System.IO.Path]::Combine(
    [System.IO.Path]::GetDirectoryName($src),
    [System.IO.Path]::GetFileNameWithoutExtension($src) + "_BACKUP_" + $ts + [System.IO.Path]::GetExtension($src)
)
Copy-Item -Path $src -Destination $dst -ErrorAction Stop
Write-Host "Backup created: $dst"
```

### Per-Application Quick Commands

```powershell
# Excel
Copy-Item "workbook.xlsm" "workbook_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').xlsm"

# Word
Copy-Item "MyDoc.docm" "MyDoc_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').docm"

# PowerPoint
Copy-Item "Deck.pptm" "Deck_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').pptm"

# Access
Copy-Item "MyApp.accdb" "MyApp_BACKUP_$(Get-Date -f 'yyyyMMdd_HHmmss').accdb"
```

---

## Automatic Backup in Import Scripts

The import scripts for **vba-word**, **vba-powerpoint**, and **vba-access** automatically create a timestamped backup immediately before any write operation. However:

- The automatic backup is a safety net, **not a substitute** for a manual pre-session backup.
- Always create a manual backup before starting a refactoring session — the automatic one only covers the moment of import.

---

## Rollback Procedure

If an import produces unexpected results:

1. **Close the application immediately** without saving.
2. Locate the most recent backup (highest timestamp in filename).
3. Copy the backup over the original:
   ```powershell
   Copy-Item "MyApp_BACKUP_20260329_143000.accdb" "MyApp.accdb" -Force
   ```
4. Reopen the application and verify the restored state.
5. Investigate the root cause before retrying the import.

---

## Backup Retention Recommendation

| Scenario | Recommended retention |
|---|---|
| Active refactoring session | Keep all backups until session is validated |
| After successful validation | Keep last 2–3 backups |
| Long-term archival | At least 1 backup per major change milestone |

---

## What Counts as a "Recent" Backup?

A backup is considered recent if it was created **in the current work session** and captures the state of the file **before any edits began**. A backup from a previous day is acceptable only if no changes have been made to the file since then.

When in doubt → create a new backup. Disk space is cheap; recovery time is not.
