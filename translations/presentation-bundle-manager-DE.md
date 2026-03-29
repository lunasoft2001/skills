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
