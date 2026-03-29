# Presentation Bundle Manager

Dieses Dokument beschreibt den Skill `presentation-bundle-manager`.

## Beschreibung

Packt alle Präsentations-Deliverables in einen strukturierten Projektordner. Erstellt einen `index.xlsx`-Index (zwei Tabellenblätter: Zusammenfassung + Dateien) und eine `manifest.json` mit SHA256-Prüfsummen und Validierungsstatus.

## Auslöser

`Präsentation bündeln`, `Deliverables paketieren`, `Manifest erstellen`, `Index generieren`, `Präsentationspaket finalisieren`

## Ausgabedateien

| Datei | Beschreibung |
|-------|-------------|
| `index.xlsx` | Excel-Index mit zwei Blättern: Zusammenfassung + Dateien |
| `manifest.json` | JSON-Manifest mit Prüfsummen und Validierung |

## Struktur des manifest.json

```json
{
  "schema_version": "1.0",
  "project": { "title", "slug", "author", "generated_at", "generated_by" },
  "deliverables": [
    { "file": "storyboard.docx", "type": "storyboard", "sha256": "...", "status": "present" },
    { "file": "storyboard.json", "type": "storyboard_json", "sha256": "...", "status": "present" },
    { "file": "deck.pptx", "type": "presentation", "sha256": "...", "status": "present" },
    { "file": "speaker-notes.docx", "type": "speaker_notes", "sha256": "...", "status": "present" }
  ],
  "validation": { "all_core_files_present": true, "warnings": [] }
}
```

## Verwendung

```bash
python3 scripts/bundle_manager.py \
  --slug mein-slug \
  --title "Meine Präsentation" \
  --author "Max Mustermann"
```

## Voraussetzungen

- Python 3.9+ (nur Standardbibliothek für `manifest.json`)
- `pip install openpyxl` (für `index.xlsx`)

## Verzeichnisstruktur

```
presentation-bundle-manager/
  SKILL.md
  scripts/
    bundle_manager.py
  evals/
    evals.json
```
