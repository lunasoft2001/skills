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
