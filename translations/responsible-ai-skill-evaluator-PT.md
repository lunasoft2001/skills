# Responsible AI Skill Evaluator — Verificação de Skills frente à RAI da Microsoft e AgentSkills.io

Este documento descreve o skill `responsible-ai-skill-evaluator` neste repositório.

## Descrição

Skill que avalia se outro skill (SKILL.md) cumpre os 6 princípios de IA Responsável da Microsoft (Equidade, Confiabilidade e Segurança, Privacidade e Segurança, Inclusividade, Transparência, Responsabilidade) e os padrões de formato e qualidade do AgentSkills.io. Gera um relatório de auditoria estruturado com avaliações e correções acionáveis.

Gatilhos: `avalie este skill`, `auditoria de skill`, `conformidade com IA responsável`, `revisar SKILL.md`, `skill pronto para publicar`, `certificação de skill`.

## Estrutura

```text
responsible-ai-skill-evaluator/
  SKILL.md                                    # Instruções + fluxo de avaliação
  references/
    microsoft-rai-checklist.md               # 6 princípios RAI da Microsoft aplicados a skills
    agentskills-quality-checklist.md         # Critérios de formato e qualidade do AgentSkills.io
```

## Funcionalidades

- Avalia um skill segundo os 6 princípios de IA Responsável da Microsoft
- Avalia um skill segundo os padrões de formato e qualidade do AgentSkills.io
- Gera um relatório de auditoria em Markdown com pontuações (PASS / PARTIAL / FAIL)
- Identifica bloqueadores (FAIL) e recomendações (PARTIAL)
- Emite um veredicto geral: READY TO PUBLISH / NEEDS FIXES / NOT COMPLIANT

## Como usar

1. Instale o skill (veja abaixo)
2. Abra o chat do GitHub Copilot
3. Digite: `"Avalie este skill para conformidade com IA Responsável:"` e cole ou referencie o skill a auditar

## Instalação do skill

```bash
# macOS / Linux
cp -r responsible-ai-skill-evaluator ~/.copilot/skills/responsible-ai-skill-evaluator
```

Em seguida, reinicie o VS Code.

## Requisitos

- VS Code com GitHub Copilot
- Um skill (SKILL.md) a avaliar

## Referências

- [Microsoft: Seis princípios de IA Responsável](https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai)
- [AgentSkills.io: Avaliando qualidade de saída de skills](https://agentskills.io/skill-creation/evaluating-skills)
