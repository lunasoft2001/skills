# Bundle di competenza: Access VBA

Questo documento descrive il contenuto della competenza `vba-access` in questo repository.

## Struttura

```text
vba-access/
  SKILL.md                        # Metadati della competenza (vba-access)
  references/
    access-vba-patterns.md        # Tipi di componenti VBA, pattern DAO/ADO e risoluzione problemi
  scripts/
    export_vba_access.py          # Esportare i moduli standard/classe in .bas/.cls
    import_vba_access.py          # Reimportare i file nel .accdb
```

## Scopo

Estrarre i moduli VBA standard e di classe dai database Access (`.accdb` / `.mdb`), refactorizzarli in VS Code e reimportarli in modo sicuro — con backup automatico con timestamp prima di ogni importazione.

> **Nota:** Questa competenza gestisce solo i moduli VBA. Per l'analisi completa del database (tabelle, query, form, report), usare la competenza **access-analyzer**.

## Installazione

```powershell
Copy-Item -Path "vba-access" -Destination "$env:USERPROFILE\.copilot\skills\vba-access" -Recurse
```

## Note

- Richiede Windows + Microsoft Access installato.
- Abilitare l'accesso attendibile al modello VBA nel Centro protezione.
- Chiudere Access e verificare l'assenza di file di blocco `.laccdb`.
- Un backup del `.accdb` viene creato automaticamente prima di ogni importazione.
- Fa parte della **Suite VBA di Office** — usare `office-vba-orchestrator`.
