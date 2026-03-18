# Responsible AI Skill Evaluator — Valutazione degli skill secondo RAI di Microsoft e AgentSkills.io

Questo documento descrive lo skill `responsible-ai-skill-evaluator` in questo repository.

## Descrizione

Skill che valuta se un altro skill (SKILL.md) rispetta i 6 principi di IA Responsabile di Microsoft (Equità, Affidabilità e Sicurezza, Privacy e Sicurezza, Inclusività, Trasparenza, Responsabilità) e gli standard di formato e qualità di AgentSkills.io. Genera un report di audit strutturato con valutazioni e correzioni operative.

Trigger: `valuta questo skill`, `audit skill`, `conformità IA responsabile`, `revisione SKILL.md`, `skill pronto per la pubblicazione`, `certificazione skill`.

## Struttura

```text
responsible-ai-skill-evaluator/
  SKILL.md                                    # Istruzioni + flusso di valutazione
  references/
    microsoft-rai-checklist.md               # 6 principi RAI di Microsoft applicati agli skill
    agentskills-quality-checklist.md         # Criteri di formato e qualità di AgentSkills.io
```

## Funzionalità

- Valuta uno skill secondo i 6 principi di IA Responsabile di Microsoft
- Valuta uno skill secondo gli standard di formato e qualità di AgentSkills.io
- Genera un report di audit in Markdown con punteggi (PASS / PARTIAL / FAIL)
- Identifica i bloccanti (FAIL) e i suggerimenti (PARTIAL)
- Emette un verdetto globale: READY TO PUBLISH / NEEDS FIXES / NOT COMPLIANT

## Come usarlo

1. Installare lo skill (vedi sotto)
2. Aprire la chat di GitHub Copilot
3. Scrivere: `"Valuta questo skill per la conformità all'IA Responsabile:"` e incollare o fare riferimento allo skill da valutare

## Installazione dello skill

```bash
# macOS / Linux
cp -r responsible-ai-skill-evaluator ~/.copilot/skills/responsible-ai-skill-evaluator
```

Quindi riavviare VS Code.

## Requisiti

- VS Code con GitHub Copilot
- Uno skill (SKILL.md) da valutare

## Riferimenti

- [Microsoft: Sei principi di IA Responsabile](https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai)
- [AgentSkills.io: Valutazione della qualità dell'output degli skill](https://agentskills.io/skill-creation/evaluating-skills)
