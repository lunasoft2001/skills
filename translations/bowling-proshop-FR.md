# Bowling Pro Shop — Foreur de Balle Virtuel & Coach de Piste

Ce document decrit le contenu du skill `bowling-proshop` dans ce depot.

## Description

Un foreur de balle de bowling virtuel et coach de piste specialise dans la selection de balle et les **layouts Dual Angle** (methode Mo Pinel). Il conduit des consultations interactives en plusieurs phases pour etablir le profil du joueur et genere un **rapport HTML visuel complet** avec une vraie image de balle, un schema de piste, un schema de percage et une analyse de layout.

Declencheurs : `selection de balle`, `layout`, `schema d'huile`, `percage`, `rev rate`, `PAP`, `Dual Angle`, `potentiel de hook`, `ajustements de piste`.

## Structure

```text
bowling-proshop/
  SKILL.md                          # Instructions du skill pour GitHub Copilot
  assets/
    logo.jpeg                       # Logo LunaBowling pour le rapport HTML
  references/
    ball-selection.md               # Heuristiques de selection de cover/categorie
    current-balls-2026.md           # Catalogue de balles actuelles (2025-2026) avec slugs verifies
    dual-angle.md                   # Systeme Dual Angle complet (Mo Pinel)
    manufacturers.md                # URLs des fabricants pour les specs
    patterns-reference.md           # Schemas d'huile : house, sport, challenge
    player-types.md                 # Classification speed/rev dominance, PAP, track
  scripts/
    generate_bowling_report_v2.py   # Generateur de rapport HTML visuel
```

## Consultation interactive

Le skill utilise quatre phases via `vscode_askQuestions` :

1. **Phase 1** — Main dominante, type de piste, objectif
2. **Phase 2** — Vitesse de balle, rev rate, PAP/track
3. **Phase 3** — Surface de piste, adherence, arsenal actuel
4. **Phase 4** — Rapport visuel (nom du joueur)

## Rapport HTML visuel

A la fin de la consultation, le skill genere un rapport HTML contenant :

- Carte de balle avec image reelle issue du catalogue du fabricant
- Schema SVG de piste vue de dessus avec la ligne de jeu recommandee
- Schema SVG de percage (pin, PAP, mass bias, trous de doigts)
- Layout Dual Angle avec explication en langage naturel
- Ajustements de piste et donnees a affiner

```bash
python3 scripts/generate_bowling_report_v2.py \
  --data /tmp/bowling_data.json \
  --output ~/Desktop/bowling_report.html

# Ou avec des donnees exemple :
python3 scripts/generate_bowling_report_v2.py --example
```

## Installation

Copie le dossier dans le repertoire des skills GitHub Copilot :

```bash
# macOS / Linux
cp -r bowling-proshop ~/.copilot/skills/bowling-proshop

# Windows (PowerShell)
Copy-Item -Path "bowling-proshop" -Destination "$env:USERPROFILE\.copilot\skills\bowling-proshop" -Recurse
```

Puis redemarre VS Code.

## Prerequis

- Python 3.11+
- Connexion internet (pour les images de balles depuis le catalogue du fabricant)
- Aucune dependance externe — utilise uniquement la bibliotheque standard Python

## Notes

- Ne recommande que des balles listees dans `references/current-balls-2026.md` (catalogue actif, pas de balles discontinuees).
- Les images de balles Storm sont recuperees via des slugs verifies (`KNOWN_SLUG_MAP` dans le script) — sans devinette.
- Le systeme de layout Dual Angle suit Mo Pinel : DA × Pin-to-PAP × VAL.
- Compatible avec les joueurs a une ou deux mains, droitiers et gauchers.
