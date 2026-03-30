# Presentation PPTX Builder

Dieses Dokument beschreibt den Skill `presentation-pptx-builder`.

## Beschreibung

Generiert eine `.pptx`-Datei aus einem Storyboard mit `python-pptx`. Wendet ein sauberes, professionelles Layout mit vier verfügbaren Designs an. Fügt beschriftete Platzhalter für Diagramme ein, anstatt Daten zu erfinden.

## Auslöser

`PPTX erstellen`, `Deck generieren`, `PowerPoint erstellen`, `Präsentationsdatei bauen`

## Designs

| Design | Stil |
|--------|------|
| `corporate` | Weiß + Marineblau — Standard für Unternehmen |
| `minimal` | Weiß + Dunkelgrau — sauber und einfach |
| `dark` | Dunkel + Cyan — Technologie und modern |
| `vibrant` | Weiß + Lila — kreativ und mutig |

## Verwendung

```bash
python3 scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

## Voraussetzungen

- Python 3.9+
- `pip install python-pptx`
