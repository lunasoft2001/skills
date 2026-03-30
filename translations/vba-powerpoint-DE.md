# Skill-Bundle: PowerPoint VBA

Dieses Dokument beschreibt den Inhalt des Skills `vba-powerpoint` in diesem Repository.

## Struktur

```text
vba-powerpoint/
  SKILL.md                        # Skill-Metadaten (vba-powerpoint)
  references/
    ppt-vba-patterns.md           # VBA-Komponententypen, Ereignisse und Muster
  scripts/
    export_vba_ppt.py             # VBA-Module in .bas/.cls-Dateien exportieren
    import_vba_ppt.py             # .bas/.cls-Dateien zurück in .pptm importieren
```

## Zweck

Alle VBA-Module aus makrofähigen PowerPoint-Präsentationen (`.pptm` / `.potm`) extrahieren, in VS Code refaktorieren und sicher reimportieren — mit automatischem Zeitstempel-Backup vor jedem Import.

## Installation

```powershell
Copy-Item -Path "vba-powerpoint" -Destination "$env:USERPROFILE\.copilot\skills\vba-powerpoint" -Recurse
```

Danach VS Code neu starten.

## Hinweise

- Erfordert Windows + Microsoft PowerPoint installiert.
- Vertrauenswürdigen VBA-Zugriff im Trust Center aktivieren.
- PowerPoint vor dem Ausführen der Skripte immer schließen.
- Vor jedem Import wird automatisch ein Backup der `.pptm`-Datei erstellt.
- Teil der **Office-VBA-Suite** — `office-vba-orchestrator` zur Weiterleitung zwischen Skills verwenden.
