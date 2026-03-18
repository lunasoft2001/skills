# M365 Email Manager Skill Bundle

Ce document decrit le contenu du `m365-email-manager-skill` dans ce depot.

## Structure

```text
m365-email-manager-skill/
  SKILL.md                        # Metadonnees du skill et guide d'utilisation
  scripts/                        # Scripts Python pour setup, authentification et operations email
    setup.py                      # Flux de configuration initiale
    token_manager.py              # Gestion et renouvellement des tokens
    m365_mail.py                  # CLI principale pour les actions email Microsoft 365
    m365_mail_es.py               # Variante CLI en espagnol
    test_demo.py                  # Helper de demo/test
  references/                     # Documentation de support (quickstart, permissions, API, options de body)
```

## Installation

Pour installer ce skill dans GitHub Copilot, copie ce dossier dans le repertoire des skills Copilot :

```powershell
Copy-Item -Path "m365-email-manager-skill" -Destination "$env:USERPROFILE\.copilot\skills\m365-email-manager-skill" -Recurse
```

Puis redemarre VS Code.

## Notes

- Ce skill automatise les actions email Microsoft 365 via Microsoft Graph.
- Operations typiques : lister, rechercher, envoyer, repondre, deplacer, marquer comme lu.
- Execute le setup une seule fois (`scripts/setup.py`) pour eviter les invites d'authentification repetitives.
