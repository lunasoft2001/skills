# ChannelToObsidian

## Objectif
Skill en deux phases pour capturer un canal YouTube complet dans un Second Brain Obsidian. La phase 1 analyse tous les vidéos du canal et génère une liste de contrôle Markdown. La phase 2 traite uniquement les vidéos sélectionnées via le pipeline complet VideoToObsidian.

## Structure
- `ChannelToObsidian/SKILL.md` — définition du skill et workflow complet en deux phases
- `ChannelToObsidian/scripts/channel_to_obsidian.py` — script qui récupère tous les vidéos du canal (InnerTube browse API), construit l'index et délègue à VideoToObsidian les éléments sélectionnés

**Dépendance :** skill `VideoToObsidian` (doit être installé dans le répertoire voisin)

## Fonctionnalités principales
- Récupère tous les vidéos du canal via l'API InnerTube browse (sans dépendances externes, pagination incluse)
- Crée/met à jour `Atlas/Personas/<NomCanal>.md` comme liste de contrôle sélectionnable
- Marqueurs d'état : `[ ]` non examiné · `[x]` sélectionné · `[p]` déjà traité
- La phase 2 appelle VideoToObsidian pour chaque élément `[x]` et le marque `[p]` une fois terminé
- Supporte les URLs de canal : handle (`@nom`), `/c/`, `/channel/UC…` ou URL de vidéo
- Chemin du vault configurable via la variable d'environnement `OBSIDIAN_VAULT`

## Cas d'utilisation typiques
- Construire une base de connaissances à partir d'une chaîne technique favorite
- Examiner tous les vidéos d'un créateur avant de décider lesquels étudier
- Traitement par lot d'un canal ou d'une playlist avec curation sélective
- Maintenir un index de canal à jour au fur et à mesure des nouvelles publications
