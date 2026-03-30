# Presentation PPTX Builder

Ce document décrit le skill `presentation-pptx-builder`.

## Description

Génère un fichier `.pptx` à partir d'un storyboard en utilisant `python-pptx`. Applique une mise en page professionnelle et propre avec quatre thèmes disponibles. Insère des espaces réservés étiquetés pour les graphiques au lieu d'inventer des données.

## Déclencheurs

`créer le pptx`, `générer le deck`, `créer le PowerPoint`, `produire le fichier de présentation`

## Thèmes

| Thème | Style |
|-------|-------|
| `corporate` | Blanc + Marine — par défaut pour les affaires |
| `minimal` | Blanc + Anthracite — propre et simple |
| `dark` | Sombre + Cyan — technologie et modernité |
| `vibrant` | Blanc + Violet — créatif et audacieux |

## Utilisation

```bash
python3 scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

## Prérequis

- Python 3.9+
- `pip install python-pptx`
