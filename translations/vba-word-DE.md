# Skill-Bundle: Word VBA

Dieses Dokument beschreibt den Inhalt des Skills `vba-word` in diesem Repository.

## Struktur

```text
suites/office-vba/vba-word/
  SKILL.md                        # Skill-Metadaten (vba-word)
  references/
    word-vba-patterns.md          # VBA-Komponententypen, Ereignisse und gngige Muster
  scripts/
    export_vba_word.py            # VBA-Module in .bas/.cls-Dateien exportieren
            {                 echo ___BEGIN___COMMAND_OUTPUT_MARKER___;                 PS1="";PS2="";unset HISTFILE;                 EC=$?;                 echo "___BEGIN___COMMAND_DONE_MARKER___$EC";             }ck in .docm importieren
```

## Zweck

Alle VBA-Module aus makrofhigen Word-Dokumenten (`.docm` / `.dotm`) extrahieren, in VS Code refaktorieren und sicher  mit automatisch erstelltem Zeitstempel-Backup vor jedem Import.reimportieren 

## Installation

Diesen Ordner in das Copilot-Skills-Verzeichnis kopieren:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Danach VS Code neu starten.

## Hinweise

- Erfordert Windows + installiertes Microsoft Word.
            {                 echo ___BEGIN___COMMAND_OUTPUT_MARKER___;                 PS1="";PS2="";unset HISTFILE;                 EC=$?;                 echo "___BEGIN___COMMAND_DONE_MARKER___$EC";             }rdigen Zugriff auf das VBA-Projektobjektmodell" im Trust Center aktivieren.
            {                 echo ___BEGIN___COMMAND_OUTPUT_MARKER___;                 PS1="";PS2="";unset HISTFILE;                 EC=$?;                 echo "___BEGIN___COMMAND_DONE_MARKER___$EC";             }hren der Skripte immer schlieen.
- Vor jedem Import wird automatisch ein Backup der `.docm`-Datei erstellt.
- Teil der **Office-VBA- `office-vba-orchestrator` zur Weiterleitung zwischen Skills verwenden.Suite** 
