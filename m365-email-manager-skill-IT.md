# M365 Email Manager Skill Bundle

Questo documento descrive il contenuto del `m365-email-manager-skill` in questo repository.

## Struttura

```text
m365-email-manager-skill/
  SKILL.md                        # Metadati dello skill e guida d'uso
  scripts/                        # Script Python per setup, autenticazione e operazioni email
    setup.py                      # Flusso di configurazione iniziale
    token_manager.py              # Gestione e rinnovo dei token
    m365_mail.py                  # CLI principale per azioni email Microsoft 365
    m365_mail_es.py               # Variante CLI in spagnolo
    test_demo.py                  # Helper di demo/test
  references/                     # Documentazione di supporto (quickstart, permessi, API, opzioni body)
```

## Installazione

Per installare questo skill in GitHub Copilot, copia questa cartella nella directory degli skill di Copilot:

```powershell
Copy-Item -Path "m365-email-manager-skill" -Destination "$env:USERPROFILE\.copilot\skills\m365-email-manager-skill" -Recurse
```

Poi riavvia VS Code.

## Note

- Questo skill automatizza le azioni email Microsoft 365 tramite Microsoft Graph.
- Operazioni tipiche: elenco, ricerca, invio, risposta, spostamento, segna come letto.
- Esegui il setup una sola volta (`scripts/setup.py`) per evitare prompt ripetuti di autenticazione.
