# Bundle de compétence : Orchestrateur VBA Office

Ce document décrit le contenu de la compétence `office-vba-orchestrator` dans ce dépôt.

## Structure

```text
office-vba-orchestrator/
  SKILL.md                        # Métadonnées de la compétence (office-vba-orchestrator)
  references/
    routing-guide.md              # Détection du type de fichier et logique de routage
    backup-policy.md              # Politique de sauvegarde obligatoire et procédures de rollback
```

## Objectif

Router les tâches VBA Office vers la compétence correcte (vbaExcel, vba-word, vba-powerpoint, vba-access) et appliquer la politique de sauvegarde obligatoire avant toute importation dans toute la suite VBA Office.

## Compétences prises en charge

| Type de fichier | Application | Compétence |
|-----------------|-------------|------------|
| `.xlsm`, `.xlam` | Excel | `vbaExcel` |
| `.docm`, `.dotm` | Word | `vba-word` |
| `.pptm`, `.potm` | PowerPoint | `vba-powerpoint` |
| `.accdb`, `.mdb` | Access | `vba-access` |
| Outlook | — | ❌ Non pris en charge |

## Installation

```powershell
Copy-Item -Path "office-vba-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\office-vba-orchestrator" -Recurse
```

## Notes

- Toutes les sous-compétences doivent également être installées.
- L'orchestrateur applique la politique de sauvegarde universelle.
- VBA Outlook est explicitement exclu de cette suite.
