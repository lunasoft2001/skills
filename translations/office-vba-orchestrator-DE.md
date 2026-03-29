# Skill-Bundle: Office-VBA-Orchestrator

Dieses Dokument beschreibt den Inhalt des Skills `office-vba-orchestrator` in diesem Repository.

## Struktur

```text
office-vba-orchestrator/
  SKILL.md                        # Skill-Metadaten (office-vba-orchestrator)
  references/
    routing-guide.md              # Dateitypenerkennung und Weiterleitungslogik
    backup-policy.md              # Verbindliche Backup-Richtlinie und Rollback-Verfahren
```

## Zweck

Office-VBA-Aufgaben an den richtigen anwendungsspezifischen Skill weiterleiten (vbaExcel, vba-word, vba-powerpoint, vba-access) und die verbindliche Backup-vor-Import-Sicherheitsrichtlinie für die gesamte Office-VBA-Suite durchsetzen.

## Unterstützte Skills

| Dateityp | Anwendung | Skill |
|----------|-----------|-------|
| `.xlsm`, `.xlam` | Excel | `vbaExcel` |
| `.docm`, `.dotm` | Word | `vba-word` |
| `.pptm`, `.potm` | PowerPoint | `vba-powerpoint` |
| `.accdb`, `.mdb` | Access | `vba-access` |
| Outlook | — | ❌ Nicht unterstützt |

## Installation

```powershell
Copy-Item -Path "office-vba-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\office-vba-orchestrator" -Recurse
```

## Hinweise

- Alle Sub-Skills müssen ebenfalls installiert sein.
- Der Orchestrator setzt die universelle Backup-Richtlinie durch.
- Outlook-VBA ist explizit ausgeschlossen.
