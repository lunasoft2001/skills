# VideoToObsidian

## Objectif
Pipeline complet pour capturer une vidéo YouTube sous forme de note technique structurée dans Obsidian. Combine le téléchargement automatique des métadonnées et de la transcription avec une analyse intelligente du contenu pour générer le document adapté au type de vidéo.

## Structure
- `VideoToObsidian/SKILL.md` — définition du skill et workflow complet étape par étape
- `VideoToObsidian/scripts/video_to_obsidian.py` — script qui récupère les métadonnées, délègue la transcription à TranscribeYoutube et émet un JSON pour Copilot

**Dépend de :** skill `TranscribeYoutube` (doit être installé dans le répertoire voisin)

## Fonctionnalités principales
- Récupère les métadonnées via l'API InnerTube (titre, chaîne, description, durée)
- Délègue la transcription au skill `TranscribeYoutube`
- Détecte le type de contenu : TUTORIEL / CONCEPT / DÉMO / CONFÉRENCE
- Applique le modèle de note correspondant (checklist d'étapes, points clés, citations…)
- Génère une note Obsidian complète avec vidéo intégrée, résumé et wikilink vers la transcription
- Ouvre la note dans Obsidian automatiquement (macOS / Windows / Linux)
- Chemin du vault configurable via la variable d'environnement `OBSIDIAN_VAULT`

## Cas d'usage typiques
- Capturer un tutoriel YouTube comme note de référence avec étapes
- Transformer une vidéo conceptuelle en entrée structurée du Second Brain
- Documenter une démo ou présentation logicielle
- Archiver une conférence ou interview avec les idées clés mises en évidence
