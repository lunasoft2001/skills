# Skill-Bundle: Access VBA

Dieses Dokument beschreibt den Inhalt des Skills `vba-access` in diesem Repository.

## Struktur

```text
suites/office-vba/vba-access/
  SKILL.md                        # Skill-Metadaten (vba-access)
  references/
    access-vba-patterns.md        # VBA-Komponententypen, DAO/ADO-Muster und Fehlerbehebung
  scripts/
    export_vba_access.py          # Standard-/Klassenmodule in .bas/.cls exportieren
    import_vba_access.py          # .bas/.cls-Dateien zurück in .accdb importieren
```

## Zweck

Standard- und Klassen-VBA-Module aus Access-Datenbanken (`.accdb` / `.mdb`) extrahieren, in VS Code refaktorieren und sicher reimportieren — mit automatischem Zeitstempel-Backup vor jedem Import.

> **Hinweis:** Dieser Skill verarbeitet nur VBA-Module. Für vollständige Datenbankanalyse (Tabellen, Abfragen, Formulare, Berichte) den Skill **access-analyzer** verwenden.

## Installation

```powershell
Copy-Item -Path "vba-access" -Destination "$env:USERPROFILE\.copilot\skills\vba-access" -Recurse
```

## Hinweise

- Erfordert Windows + Microsoft Access installiert.
- Vertrauenswürdigen VBA-Zugriff im Trust Center aktivieren.
- Access schließen und sicherstellen, dass keine `.laccdb`-Sperrdatei vorhanden ist.
- Vor jedem Import wird automatisch ein Backup erstellt.
- Teil der **Office-VBA-Suite** — `office-vba-orchestrator` verwenden.
