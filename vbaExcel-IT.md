# Excel Analyzer Skill Bundle

Questo documento descrive il contenuto dello skill `vbaExcel` in questo repository.

## Struttura

```text
vbaExcel/
  SKILL.md                        # Metadati dello skill (vbaExcel)
  INSTALL.txt                     # Note rapide di installazione e uso
  scripts/                        # Script di supporto PowerShell/Python
    export_vba.py                 # Esporta moduli VBA in .bas
    import_vba.py                 # Reimporta .bas in .xlsm
    enable_vba_access.reg         # Abilita accesso programmatico a VBOM
```

## Installazione

Per installare questo skill in GitHub Copilot, copia questa cartella nella directory degli skill di Copilot:

```powershell
Copy-Item -Path "vbaExcel" -Destination "$env:USERPROFILE\.copilot\skills\vbaExcel" -Recurse
```

Poi riavvia VS Code.

## Note

- Questo bundle e focalizzato su estrazione e reimportazione VBA per file Excel `.xlsm` su Windows.
- Chiudi Excel prima di esportare o importare.
- Esegui sempre un backup del file prima di importare modifiche VBA.

