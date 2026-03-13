# Excel Analyzer Skill Bundle

Ce document decrit le contenu du skill `vbaExcel` dans ce depot.

## Structure

```text
vbaExcel/
  SKILL.md                        # Metadonnees du skill (vbaExcel)
  INSTALL.txt                     # Notes rapides d'installation et d'utilisation
  scripts/                        # Scripts d'assistance PowerShell/Python
    export_vba.py                 # Exporte les modules VBA en .bas
    import_vba.py                 # Reimporte les .bas dans .xlsm
    enable_vba_access.reg         # Active l'acces programmatique a VBOM
```

## Installation

Pour installer ce skill dans GitHub Copilot, copie ce dossier dans le repertoire des skills Copilot :

```powershell
Copy-Item -Path "vbaExcel" -Destination "$env:USERPROFILE\.copilot\skills\vbaExcel" -Recurse
```

Puis redemarre VS Code.

## Notes

- Ce bundle est concentre sur l'extraction et la reimportation de VBA pour les fichiers Excel `.xlsm` sous Windows.
- Ferme Excel avant l'export/import.
- Cree toujours une sauvegarde du classeur avant d'importer des changements VBA.

