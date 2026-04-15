# VideoToObsidian

## Zweck
Vollständige Pipeline, um ein YouTube-Video als strukturierte technische Notiz in Obsidian zu erfassen. Kombiniert automatisches Abrufen von Metadaten und Transkriptionen mit KI-gestützter Inhaltsanalyse, um das passende Dokument für den jeweiligen Videotyp zu erstellen.

## Struktur
- `VideoToObsidian/SKILL.md` — Skill-Definition und vollständiger Schritt-für-Schritt-Workflow
- `VideoToObsidian/scripts/video_to_obsidian.py` — Skript, das Metadaten abruft, die Transkription an TranscribeYoutube delegiert und ein JSON für Copilot ausgibt

**Abhängigkeit:** Skill `TranscribeYoutube` (muss im Nachbarverzeichnis installiert sein)

## Hauptfunktionen
- Ruft Video-Metadaten über die InnerTube API ab (Titel, Kanal, Beschreibung, Dauer)
- Delegiert die Transkription an den Skill `TranscribeYoutube`
- Erkennt den Inhaltstyp: TUTORIAL / KONZEPT / DEMO / VORTRAG
- Wendet die passende Notizenvorlage an (Schritt-Checkliste, Kernpunkte, Zitate…)
- Erstellt eine vollständige Obsidian-Notiz mit eingebettetem Video, Zusammenfassung und Wikilink zur Transkription
- Öffnet die Notiz automatisch in Obsidian (macOS / Windows / Linux)
- Vault-Pfad konfigurierbar über Umgebungsvariable `OBSIDIAN_VAULT`

## Typische Anwendungsfälle
- YouTube-Tutorial als Schritt-für-Schritt-Referenznotiz erfassen
- Erklärvideo in einen strukturierten Second-Brain-Eintrag umwandeln
- Software-Demo oder Showcase dokumentieren
- Vortrag oder Interview mit hervorgehobenen Kernideen archivieren
