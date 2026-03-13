# Access Analyzer Skill Bundle

Questo documento descrive il contenuto dello skill `access-analyzer` in questo repository.

## Struttura

```text
access-analyzer/
  SKILL.md                        # Metadati dello skill
  scripts/                        # Script PowerShell di automazione
    access-backup.ps1             # Creare backup
    access-export-git.ps1         # Esportare con integrazione Git
    access-import-changed.ps1     # Importare solo gli oggetti modificati
    access-import.ps1             # Importare tutti gli oggetti
  references/                     # Documentazione di riferimento
    AccessObjectTypes.md          # Tipi di oggetti Access
    ExportTodoSimple.bas          # Modulo VBA di esportazione
    VBA-Patterns.md               # Pattern di codice VBA
  assets/                         # Risorse dello skill
    AccessAnalyzer.accdb          # Database di esempio/template
```

## Installazione

Per installare questo skill in GitHub Copilot, copia questa cartella nella directory degli skill di Copilot:

```powershell
Copy-Item -Path "access-analyzer" -Destination "$env:USERPROFILE\.copilot\skills\access-analyzer" -Recurse
```

Poi riavvia VS Code.

## Note

- Questo bundle e ottimizzato per GitHub Copilot.
- Include solo i file essenziali dello skill.
- `AccessAnalyzer.accdb` e incluso in `assets/` come risorsa di supporto.
