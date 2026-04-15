# ChannelToObsidian

## Zweck
Zweiphasiges Skill zur vollständigen Erfassung eines YouTube-Kanals in einem Obsidian Second Brain. Phase 1 scannt alle Videos des Kanals und erstellt eine Markdown-Checkliste. Phase 2 verarbeitet nur die markierten Videos über die vollständige VideoToObsidian-Pipeline.

## Struktur
- `ChannelToObsidian/SKILL.md` — Skill-Definition und vollständiger zweiphasiger Workflow
- `ChannelToObsidian/scripts/channel_to_obsidian.py` — Skript, das alle Kanal-Videos abruft (InnerTube Browse API), den Index erstellt und VideoToObsidian für ausgewählte Elemente aufruft

**Abhängigkeit:** Skill `VideoToObsidian` (muss im Nachbarverzeichnis installiert sein)

## Hauptfunktionen
- Ruft alle Kanal-Videos über die InnerTube Browse API ab (keine externen Abhängigkeiten, Paginierung inklusive)
- Erstellt/aktualisiert `Atlas/Personas/<KanalName>.md` als auswählbare Checkliste
- Zustandsmarkierungen: `[ ]` nicht geprüft · `[x]` ausgewählt · `[p]` bereits verarbeitet
- Phase 2 ruft VideoToObsidian für jedes `[x]`-Element auf und markiert es nach Abschluss mit `[p]`
- Unterstützte Kanal-URLs: Handle (`@name`), `/c/`, `/channel/UC…` oder Video-URL
- Vault-Pfad über Umgebungsvariable `OBSIDIAN_VAULT` konfigurierbar

## Typische Anwendungsfälle
- Aufbau einer Wissensbasis aus einem technischen Lieblingskanal
- Übersicht aller Videos eines Erstellers vor der Auswahl zum Studium
- Stapelverarbeitung eines vollständigen Kanals oder einer Playlist mit selektiver Kuration
- Aktuellen Kanalindex pflegen, wenn neue Videos veröffentlicht werden
