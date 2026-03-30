# Bundle di competenza: Word VBA

Questo documento descrive il contenuto della competenza `vba-word` in questo repository.

## Struttura

```text
suites/office-vba/vba-word/
  SKILL.md                        # Metadati della competenza (vba-word)
  references/
    word-vba-patterns.md          # Tipi di componenti VBA, eventi e pattern comuni
  scripts/
    export_vba_word.py            # Esportare i moduli VBA in file .bas/.cls
    import_vba_word.py            # Reimportare i file .bas/.cls nel .docm
```

## Scopo

Estrarre tutti i moduli VBA da documenti Word abilitati alle macro (`.docm` / `.dotm`), refactorizzarli in VS Code e reimportarli in modo  creando sempre un backup con timestamp prima di ogni importazione.sicuro 

## Installazione

Copiare questa cartella nella directory delle competenze di Copilot:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Poi riavviare VS Code.

## Note

- Richiede Windows + Microsoft Word installato.
- Abilitare "Considera attendibile l'accesso al modello a oggetti del progetto VBA" nel Centro protezione di Word.
- Chiudere sempre Word prima di eseguire gli script.
- Un backup del `.docm` viene creato automaticamente prima di ogni importazione.
- Fa parte della **Suite VBA di  usare `office-vba-orchestrator` per instradare tra le competenze.Office** 
