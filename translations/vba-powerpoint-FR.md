# Bundle de compétence : PowerPoint VBA

Ce document décrit le contenu de la compétence `vba-powerpoint` dans ce dépôt.

## Structure

```text
vba-powerpoint/
  SKILL.md                        # Métadonnées de la compétence (vba-powerpoint)
  references/
    ppt-vba-patterns.md           # Types de composants VBA, événements et modèles
  scripts/
    export_vba_ppt.py             # Exporter les modules VBA en fichiers .bas/.cls
    import_vba_ppt.py             # Réimporter les fichiers dans le .pptm
```

## Objectif

Extraire tous les modules VBA des présentations PowerPoint avec macros (`.pptm` / `.potm`), les refactoriser dans VS Code et les réimporter en toute sécurité — avec sauvegarde horodatée automatique avant chaque importation.

## Installation

```powershell
Copy-Item -Path "vba-powerpoint" -Destination "$env:USERPROFILE\.copilot\skills\vba-powerpoint" -Recurse
```

Puis redémarrez VS Code.

## Notes

- Nécessite Windows + Microsoft PowerPoint installé.
- Activer l'accès de confiance au modèle objet VBA dans le Centre de gestion de la confidentialité.
- Fermer PowerPoint avant d'exécuter les scripts.
- Une sauvegarde du `.pptm` est créée automatiquement avant chaque importation.
- Fait partie de la **Suite VBA Office** — utiliser `office-vba-orchestrator` pour router entre les compétences.
