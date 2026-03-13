# Access Analyzer Skill Bundle

Ce document decrit le contenu du skill `access-analyzer` dans ce depot.

## Structure

```text
access-analyzer/
  SKILL.md                        # Metadonnees du skill
  scripts/                        # Scripts PowerShell d'automatisation
    access-backup.ps1             # Creer des sauvegardes
    access-export-git.ps1         # Exporter avec integration Git
    access-import-changed.ps1     # Importer uniquement les objets modifies
    access-import.ps1             # Importer tous les objets
  references/                     # Documentation de reference
    AccessObjectTypes.md          # Types d'objets Access
    ExportTodoSimple.bas          # Module VBA d'export
    VBA-Patterns.md               # Modeles de code VBA
  assets/                         # Ressources du skill
    AccessAnalyzer.accdb          # Base de donnees exemple/modele
```

## Installation

Pour installer ce skill dans GitHub Copilot, copie ce dossier dans le repertoire des skills Copilot :

```powershell
Copy-Item -Path "access-analyzer" -Destination "$env:USERPROFILE\.copilot\skills\access-analyzer" -Recurse
```

Puis redemarre VS Code.

## Notes

- Ce bundle est optimise pour GitHub Copilot.
- Il inclut uniquement les fichiers essentiels du skill.
- `AccessAnalyzer.accdb` est fourni dans `assets/` comme ressource de support.
