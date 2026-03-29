# Presentation Factory Orchestrator

Dieses Dokument beschreibt den Skill `presentation-factory-orchestrator`.

## Beschreibung

Ein End-to-End-Orchestrator, der die vollständige Präsentationserstellungs-Pipeline über vier Stufen koordiniert: Storyboard → PPTX-Builder → Sprechernotizen → Bundle-Manager. Validiert Mindesteingaben und leitet jede Stufe an den entsprechenden Sub-Skill weiter. Das Ergebnis wird in `/deliverables/<slug>/` abgelegt.

## Auslöser

`Präsentation erstellen`, `Deck erstellen`, `Folien bauen`, `vollständiges Präsentationspaket`, `Präsentation von Anfang bis Ende`

## Pipeline-Stufen

1. **Stufe 1** — `presentation-storyboard`: narrative Struktur
2. **Stufe 2** — `presentation-pptx-builder`: Präsentationsdatei
3. **Stufe 3** — `presentation-speaker-notes`: Moderatorskript
4. **Stufe 4** — `presentation-bundle-manager`: Index + Manifest

## Erforderliche Eingaben

- **topic** — Thema der Präsentation
- **audience** — Teilnehmer und Kenntnisstand
- **duration** — Gesamtdauer in Minuten
- **slug** — Kurzbezeichner für den Ausgabeordner (z. B. `q2-roadmap-2026`)

## Ausgabe

```
/deliverables/<slug>/
  storyboard.docx
  deck.pptx
  speaker-notes.docx
  index.xlsx
  manifest.json
```
