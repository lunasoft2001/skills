# Bundle di competenza: Orchestratore VBA Office

Questo documento descrive il contenuto della competenza `office-vba-orchestrator` in questo repository.

## Struttura

```text
office-vba-orchestrator/
  SKILL.md                        # Metadati della competenza (office-vba-orchestrator)
  references/
    routing-guide.md              # Rilevamento del tipo di file e logica di instradamento
    backup-policy.md              # Politica di backup obbligatoria e procedure di rollback
```

## Scopo

Instradare le attività VBA di Office verso la competenza corretta (vbaExcel, vba-word, vba-powerpoint, vba-access) e applicare la politica obbligatoria di backup-prima-dell'importazione in tutta la suite VBA di Office.

## Competenze supportate

| Tipo di file | Applicazione | Competenza |
|---|---|---|
| `.xlsm`, `.xlam` | Excel | `vbaExcel` |
| `.docm`, `.dotm` | Word | `vba-word` |
| `.pptm`, `.potm` | PowerPoint | `vba-powerpoint` |
| `.accdb`, `.mdb` | Access | `vba-access` |
| Outlook | — | ❌ Non supportato |

## Installazione

```powershell
Copy-Item -Path "office-vba-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\office-vba-orchestrator" -Recurse
```

## Note

- Tutte le sotto-competenze devono essere installate separatamente.
- L'orchestratore applica la politica universale di backup.
- VBA Outlook è esplicitamente escluso da questa suite.
