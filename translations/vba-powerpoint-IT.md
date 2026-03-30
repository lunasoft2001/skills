# Bundle di competenza: PowerPoint VBA

Questo documento descrive il contenuto della competenza `vba-powerpoint` in questo repository.

## Struttura

```text
suites/office-vba/vba-powerpoint/
  SKILL.md                        # Metadati della competenza (vba-powerpoint)
  references/
    ppt-vba-patterns.md           # Tipi di componenti VBA, eventi e pattern comuni
  scripts/
    export_vba_ppt.py             # Esportare i moduli VBA in file .bas/.cls
    import_vba_ppt.py             # Reimportare i file nel .pptm
```

## Scopo

Estrarre tutti i moduli VBA da presentazioni PowerPoint abilitate alle macro (`.pptm` / `.potm`), refactorizzarli in VS Code e reimportarli in modo sicuro — con backup automatico con timestamp prima di ogni importazione.

## Installazione

```powershell
Copy-Item -Path "vba-powerpoint" -Destination "$env:USERPROFILE\.copilot\skills\vba-powerpoint" -Recurse
```

Poi riavviare VS Code.

## Note

- Richiede Windows + Microsoft PowerPoint installato.
- Abilitare l'accesso attendibile al modello VBA nel Centro protezione.
- Chiudere PowerPoint prima di eseguire gli script.
- Un backup del `.pptm` viene creato automaticamente prima di ogni importazione.
- Fa parte della **Suite VBA di Office** — usare `office-vba-orchestrator` per instradare tra le competenze.
