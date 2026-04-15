# TranscribeYoutube

Skill pour générer des notes de transcription complètes dans Obsidian à partir de vidéos YouTube.

## Objectif

Télécharge la transcription complète de n'importe quelle vidéo YouTube et la sauvegarde comme note `.md` prête pour Obsidian avec frontmatter YAML et timestamps cliquables — directement depuis VS Code, sans dépendances externes.

## Structure

```text
TranscribeYoutube/
  SKILL.md
  scripts/
    transcribe_youtube.py
```

## Fonctionnalités principales

- Utilise l'API InnerTube Player de YouTube (client iOS) — pas de clés API, pas de yt-dlp
- Zéro dépendance externe : Python 3.9+ standard uniquement
- Génère un frontmatter YAML avec les métadonnées de la vidéo
- Regroupe les lignes de transcription toutes les 30 secondes (comme le plugin YTranscript)
- Timestamps cliquables qui ouvrent la vidéo à la seconde exacte
- Multi-plateforme : macOS, Windows, Linux
- Ouvre Obsidian automatiquement sur la note créée
- Chemin du vault configurable via la variable d'environnement `OBSIDIAN_VAULT`

## Cas d'usage typiques

- Capturer un tutoriel YouTube dans son Second Brain
- Générer une note de transcription et la lier depuis la note de ressource principale
- Archiver le contenu vidéo pour référence hors ligne
