# MCP Evaluator — Audit dei server MCP: Sicurezza, Privacy e Qualità

Questo documento descrive lo skill `mcp-evaluator` in questo repository.

## Descrizione

Skill che audita i server MCP (Model Context Protocol) per sicurezza, privacy e qualità tecnica. Analizza il codice sorgente (TypeScript/Python), le definizioni dei tool, i file di configurazione e il SKILL.md companion. Produce un report strutturato PASS/PARTIAL/FAIL con correzioni operative.

Trigger: `auditare MCP`, `valutare server MCP`, `verificare sicurezza MCP`, `revisionare i tool MCP`, `il mio MCP è sicuro`, `MCP pronto per la pubblicazione`.

## Struttura

```text
mcp-evaluator/
  SKILL.md                              # Istruzioni + flusso di valutazione in 3 fasi
  references/
    mcp-rai-checklist.md               # Criteri di sicurezza e privacy (RAI + OWASP)
    mcp-quality-checklist.md           # Criteri di qualità tecnica
```

## Funzionalità

- **Fase 1 — Sicurezza & Privacy**: credenziali, PII, operazioni distruttive, injection/SSRF, token
- **Fase 2 — Qualità Tecnica**: design dei tool, gestione degli errori, skill companion, dipendenze, logging
- **Fase 3 — Responsabilità**: licenza, repository, versioni, manutentore
- Genera un report Markdown con sezioni valutate (PASS / PARTIAL / FAIL)
- Verdetto globale: `SAFE TO USE` / `NEEDS FIXES` / `SECURITY RISK`

## Come usarlo

1. Installare lo skill (vedi sotto)
2. Aprire la chat di GitHub Copilot
3. Scrivere: `"Audita il mio MCP LinkedIn per la sicurezza"` — Copilot leggerà il codice sorgente e genererà il report completo

## Installazione dello skill

```bash
# macOS / Linux
cp -r mcp-evaluator ~/.copilot/skills/mcp-evaluator
```

Quindi riavviare VS Code.

## Requisiti

- VS Code con GitHub Copilot
- Accesso al codice sorgente del server MCP da valutare
