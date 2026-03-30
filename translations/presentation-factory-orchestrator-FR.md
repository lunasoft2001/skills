# Presentation Factory Orchestrator

Ce document décrit le skill `presentation-factory-orchestrator`.

## Description

Un orchestrateur de bout en bout qui coordonne le pipeline complet de création de présentations en quatre étapes : storyboard → constructeur PPTX → notes du présentateur → gestionnaire de bundle. Valide les entrées minimales et achemine chaque étape vers le sous-skill approprié, livrant un package complet dans `/deliverables/<slug>/`.

## Déclencheurs

`créer une présentation`, `préparer un deck`, `faire des diapositives`, `package de présentation complet`, `présentation de bout en bout`

## Étapes du Pipeline

1. **Étape 1** — `presentation-storyboard` : structure narrative
2. **Étape 2** — `presentation-pptx-builder` : fichier de présentation
3. **Étape 3** — `presentation-speaker-notes` : script du présentateur
4. **Étape 4** — `presentation-bundle-manager` : index + manifeste

## Entrées Requises

- **topic** — sujet de la présentation
- **audience** — participants et niveau d'expertise
- **duration** — durée totale en minutes
- **slug** — identifiant court pour le dossier de sortie (ex. `q2-roadmap-2026`)

## Sortie

```
/deliverables/<slug>/
  storyboard.docx
  deck.pptx
  speaker-notes.docx
  index.xlsx
  manifest.json
```
