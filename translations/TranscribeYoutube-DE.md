# TranscribeYoutube

Skill zum Generieren vollständiger Obsidian-Transkriptnotizen aus YouTube-Videos.

## Zweck

Lädt das vollständige Transkript eines beliebigen YouTube-Videos herunter und speichert es als Obsidian-ready `.md`-Datei mit YAML-Frontmatter und klickbaren Zeitstempeln — direkt aus VS Code, ohne externe Abhängigkeiten.

## Struktur

```text
TranscribeYoutube/
  SKILL.md
  scripts/
    transcribe_youtube.py
```

## Hauptfunktionen

- Verwendet die YouTube InnerTube Player API (iOS-Client) — keine API-Schlüssel, kein yt-dlp
- Keine externen Abhängigkeiten: nur Python 3.9+ Standardbibliothek
- Erzeugt YAML-Frontmatter mit Video-Metadaten
- Gruppiert Transkriptzeilen alle 30 Sekunden (wie das YTranscript-Plugin)
- Klickbare Zeitstempel, die das Video an der genauen Stelle öffnen
- Plattformübergreifend: macOS, Windows, Linux
- Öffnet Obsidian automatisch in der erstellten Notiz
- Vault-Pfad konfigurierbar über `OBSIDIAN_VAULT`-Umgebungsvariable

## Typische Anwendungsfälle

- YouTube-Tutorial ins Second Brain erfassen
- Transkriptnotiz erstellen und mit der Hauptressourcennotiz verknüpfen
- Videoinhalte für Offline-Referenz archivieren
