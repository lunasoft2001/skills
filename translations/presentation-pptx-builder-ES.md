# Presentation PPTX Builder

Este documento describe el skill `presentation-pptx-builder`.

## Descripción

Genera un archivo `.pptx` desde un storyboard usando `python-pptx`. Aplica un diseño profesional y limpio con cuatro temas disponibles. Inserta marcadores de posición etiquetados para gráficos y diagramas en lugar de inventar datos.

## Activadores

`genera el pptx`, `crea las diapositivas`, `arma el PowerPoint`, `produce el deck`, `construye el archivo de presentación`

## Temas

| Tema | Estilo |
|------|--------|
| `corporate` | Blanco + Azul marino — negocio por defecto |
| `minimal` | Blanco + Carbón — limpio y simple |
| `dark` | Oscuro + Cian — tecnología y moderno |
| `vibrant` | Blanco + Púrpura — creativo y audaz |

## Uso

```bash
python3 scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

## Requisitos

- Python 3.9+
- `pip install python-pptx`

## Estructura

```
suites/presentation/presentation-pptx-builder/
  SKILL.md
  scripts/
    build_pptx.py
  evals/
    evals.json
  references/
    pptx-design-guide.md
```
