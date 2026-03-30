# Presentation Bundle Manager

Questo documento descrive lo skill `presentation-bundle-manager`.

## Descrizione

Raggruppa tutti i deliverable della presentazione in una cartella di progetto strutturata. Genera un indice `index.xlsx` (due fogli: Riepilogo + File) e un `manifest.json` con hash SHA256 e stato di validazione.

## Trigger

`raggruppa la presentazione`, `pacchettizza i deliverable`, `crea il manifesto`, `genera l'indice`, `finalizza il pacchetto di presentazione`

## File di Output

| File | Descrizione |
|------|-------------|
| `index.xlsx` | Indice Excel a due fogli: Riepilogo + File |
| `manifest.json` | Manifesto JSON con hash e validazione |

## Struttura del manifest.json

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

## Utilizzo

```bash
python3 scripts/bundle_manager.py \
  --slug il-mio-slug \
  --title "La Mia Presentazione" \
  --author "Mario Rossi"
```

## Requisiti

- Python 3.9+ (solo libreria standard per `manifest.json`)
- `pip install openpyxl` (per `index.xlsx`)

## Struttura

```
presentation-bundle-manager/
  SKILL.md
  scripts/
    bundle_manager.py
  evals/
    evals.json
```
