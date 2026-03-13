# M365 Email Manager Skill Bundle

Dieses Dokument beschreibt den Inhalt des `m365-email-manager-skill` in diesem Repository.

## Struktur

```text
m365-email-manager-skill/
  SKILL.md                        # Skill-Metadaten und Nutzungshinweise
  scripts/                        # Python-Skripte fuer Setup, Authentifizierung und E-Mail-Operationen
    setup.py                      # Einmaliger Konfigurationsablauf
    token_manager.py              # Token-Speicherung und -Erneuerung
    m365_mail.py                  # Haupt-CLI fuer Microsoft 365 E-Mail-Aktionen
    m365_mail_es.py               # Spanische CLI-Variante
    test_demo.py                  # Demo-/Test-Helfer
  references/                     # Zusatzdokumentation (Quickstart, Berechtigungen, API, Body-Optionen)
```

## Installation

Um diesen Skill in GitHub Copilot zu installieren, kopiere diesen Ordner in dein Copilot-Skills-Verzeichnis:

```powershell
Copy-Item -Path "m365-email-manager-skill" -Destination "$env:USERPROFILE\.copilot\skills\m365-email-manager-skill" -Recurse
```

Starte danach VS Code neu.

## Hinweise

- Dieser Skill automatisiert Microsoft 365 E-Mail-Aktionen ueber Microsoft Graph.
- Typische Aktionen: listen, suchen, senden, antworten, verschieben, als gelesen markieren.
- Fuehre das Setup einmal aus (`scripts/setup.py`), um wiederholte Authentifizierungsabfragen zu vermeiden.
