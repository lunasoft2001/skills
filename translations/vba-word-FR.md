# Bundle de comptence : Word VBA

Ce document dcrit le contenu de la comptence `vba-word` dans ce dptttt.

## Structure

```text
vba-word/
  SKILL.md                        # Mtadonnes de la comptence (vba-word)
  references/
    word-vba-patterns.md          # Types de composants VBA, vnements et modles courants
  scripts/
    export_vba_word.py            # Exporter les modules VBA en fichiers .bas/.cls
    import_vba_word.py            # Rimporter les fichiers .bas/.cls dans le .docm
```

## Objectif

Extraire tous les modules VBA des documents Word avec macros (`.docm` / `.dotm`), les refactoriser dans VS Code, puis les rimporter en toute  avec crScuritation automatique d'une sauvegarde horodat e avant chaque importation.

## Installation

Copiez ce dossier dans le rpertoire des comptences Copilot :

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Puis redmarrez VS Code.

## Notes

- Ncessite Windows + Microsoft Word install.
-  Faire confiance au modActiverle objet du projet  dans le Centre de gestion de la confidentialitVba de Word.  
- Toujours fermer Word avant d'excuter les scripts.
- Une sauvegarde du `.docm` est cre automatiquement avant chaque importation.
- Fait partie de la **Suite VBA  utiliser `office-vba-orchestrator` pour router entre les compOfficetences.** 
