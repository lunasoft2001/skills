# Excel Analyzer Skill Bundle

Dieses Dokument beschreibt den Inhalt des Skills `vbaExcel` in diesem Repository.

## Struktur

```text
suites/office-vba/vbaExcel/
  SKILL.md                        # Metadaten des Skills (vbaExcel)
  INSTALL.txt                     # Kurze Installations- und Nutzungshinweise
  scripts/                        # PowerShell/Python-Hilfsskripte
    export_vba.py                 # Exportiert VBA-Module nach .bas
    import_vba.py                 # Importiert .bas zurueck in .xlsm
    enable_vba_access.reg         # Aktiviert programmgesteuerten VBOM-Zugriff
```

## Installation

Um diesen Skill in GitHub Copilot zu installieren, kopiere diesen Ordner in dein Copilot-Skills-Verzeichnis:

```powershell
Copy-Item -Path "vbaExcel" -Destination "$env:USERPROFILE\.copilot\skills\vbaExcel" -Recurse
```

Starte danach VS Code neu.

## Hinweise

- Dieses Bundle ist auf VBA-Export und Re-Import fuer Excel `.xlsm` unter Windows ausgerichtet.
- Schliesse Excel vor Export/Import.
- Erstelle vor dem Import von VBA-Aenderungen immer ein Backup.

