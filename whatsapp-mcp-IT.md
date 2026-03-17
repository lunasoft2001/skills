# WhatsApp MCP — Messaggi, File e Gruppi da GitHub Copilot

Questo documento descrive lo skill `whatsapp-mcp` in questo repository.

## Descrizione

Skill per inviare messaggi di testo, immagini, PDF e file VCF a contatti e gruppi WhatsApp direttamente da GitHub Copilot. Gestisce i gruppi (aggiungere/rimuovere membri, ottenere link di invito) e legge la cronologia delle chat. Se l'MCP non è installato, guida l'utente passo dopo passo per configurarlo.

Attivatori: `invia WhatsApp`, `messaggio WhatsApp`, `file WhatsApp`, `gruppo WhatsApp`, `installare MCP WhatsApp`.

## Struttura

```text
whatsapp-mcp/
  SKILL.md                    # Istruzioni dello skill per GitHub Copilot
  references/
    tools.md                  # Riferimento completo di tutti gli strumenti MCP
    install.md                # Guida all'installazione passo dopo passo
```

## Installazione dello skill

```bash
cp -r whatsapp-mcp ~/.copilot/skills/whatsapp-mcp
```

Riavviare VS Code.

## Requisiti

- VS Code con GitHub Copilot
- Node.js ≥ 18
- Server MCP `whatsapp-mcp-server` installato e configurato
  - Repository: https://github.com/lunasoft2001/mcp
