# Bundle de compétence : Access VBA

Ce document décrit le contenu de la compétence `vba-access` dans ce dépôt.

## Structure

```text
suites/office-vba/vba-access/
  SKILL.md                        # Métadonnées de la compétence (vba-access)
  references/
    access-vba-patterns.md        # Types de composants VBA, modèles DAO/ADO et dépannage
  scripts/
    export_vba_access.py          # Exporter les modules standard/classe en .bas/.cls
    import_vba_access.py          # Réimporter les fichiers dans le .accdb
```

## Objectif

Extraire les modules VBA standard et de classe des bases de données Access (`.accdb` / `.mdb`), les refactoriser dans VS Code et les réimporter en toute sécurité — avec sauvegarde horodatée automatique avant chaque importation.

> **Note :** Ce skill gère uniquement les modules VBA. Pour une analyse complète de la base de données (tables, requêtes, formulaires, rapports), utiliser le skill **access-analyzer**.

## Installation

```powershell
Copy-Item -Path "vba-access" -Destination "$env:USERPROFILE\.copilot\skills\vba-access" -Recurse
```

## Notes

- Nécessite Windows + Microsoft Access installé.
- Activer l'accès de confiance au modèle objet VBA dans le Centre de gestion de la confidentialité.
- Fermer Access et vérifier l'absence de fichier de verrouillage `.laccdb`.
- Une sauvegarde du `.accdb` est créée automatiquement avant chaque importation.
- Fait partie de la **Suite VBA Office** — utiliser `office-vba-orchestrator`.
