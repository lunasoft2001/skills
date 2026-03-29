# Presentation PPTX Builder

Questo documento descrive lo skill `presentation-pptx-builder`.

## Descrizione

Genera un file `.pptx` da uno storyboard usando `python-pptx`. Applica un layout professionale e pulito con quattro temi disponibili. Inserisce segnaposto etichettati per grafici e diagrammi invece di inventare dati.

## Trigger

`crea il pptx`, `genera il deck`, `crea il PowerPoint`, `produci il file di presentazione`

## Temi

| Tema | Stile |
|------|-------|
| `corporate` | Bianco + Blu marino — default aziendale |
| `minimal` | Bianco + Antracite — pulito e semplice |
| `dark` | Scuro + Ciano — tecnologia e moderno |
| `vibrant` | Bianco + Viola — creativo e audace |

## Utilizzo

```bash
python3 scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

## Requisiti

- Python 3.9+
- `pip install python-pptx`
