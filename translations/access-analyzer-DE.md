# Access Analyzer Skill Bundle

Dieses Dokument beschreibt den Inhalt des Skills `access-analyzer` in diesem Repository.

## Struktur

```text
access-analyzer/
  SKILL.md                        # Metadaten des Skills
  scripts/                        # PowerShell-Automatisierungsskripte
    access-backup.ps1             # Backups erstellen
    access-export-git.ps1         # Mit Git-Integration exportieren
    access-import-changed.ps1     # Nur geaenderte Objekte importieren
    access-import.ps1             # Alle Objekte importieren
  references/                     # Referenzdokumentation
    AccessObjectTypes.md          # Access-Objekttypen
    ExportTodoSimple.bas          # VBA-Exportmodul
    VBA-Patterns.md               # VBA-Code-Muster
  assets/                         # Skill-Ressourcen
    AccessAnalyzer.accdb          # Beispiel-/Vorlagen-Datenbank
```

## Installation

Um diesen Skill in GitHub Copilot zu installieren, kopiere diesen Ordner in dein Copilot-Skills-Verzeichnis:

```powershell
Copy-Item -Path "access-analyzer" -Destination "$env:USERPROFILE\.copilot\skills\access-analyzer" -Recurse
```

Starte danach VS Code neu.

## Hinweise

- Dieses Bundle ist fuer GitHub Copilot optimiert.
- Es enthaelt nur die wesentlichen Skill-Dateien.
- `AccessAnalyzer.accdb` befindet sich in `assets/` als Unterstuetzungsressource.
