# Presentation Bundle Manager

Ce document décrit le skill `presentation-bundle-manager`.

## Description

Regroupe tous les livrables de présentation dans un dossier de projet structuré. Génère un index `index.xlsx` (deux feuilles : Résumé + Fichiers) et un `manifest.json` avec des sommes de contrôle SHA256 et un état de validation.

## Déclencheurs

`regrouper la présentation`, `empaqueter les livrables`, `créer le manifeste`, `générer l'index`, `finaliser le package de présentation`

## Fichiers de Sortie

| Fichier | Description |
|---------|-------------|
| `index.xlsx` | Index Excel à deux feuilles : Résumé + Fichiers |
| `manifest.json` | Manifeste JSON avec sommes de contrôle et validation |

## Utilisation

```bash
python3 scripts/bundle_manager.py \
  --slug mon-slug \
  --title "Ma Présentation" \
  --author "Marie Dupont"
```

## Prérequis

- Python 3.9+ (bibliothèque standard uniquement pour `manifest.json`)
- `pip install openpyxl` (pour `index.xlsx`)
