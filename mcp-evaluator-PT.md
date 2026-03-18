# MCP Evaluator — Auditoria de Servidores MCP: Segurança, Privacidade e Qualidade

Este documento descreve o skill `mcp-evaluator` neste repositório.

## Descrição

Skill que audita servidores MCP (Model Context Protocol) em segurança, privacidade e qualidade técnica. Analisa código-fonte (TypeScript/Python), definições de tools, arquivos de configuração e SKILL.md companion. Produz um relatório estruturado PASS/PARTIAL/FAIL com correções acionáveis.

Gatilhos: `auditar MCP`, `avaliar servidor MCP`, `verificar segurança MCP`, `revisar tools MCP`, `meu MCP é seguro`, `MCP pronto para publicar`.

## Estrutura

```text
mcp-evaluator/
  SKILL.md                              # Instruções + fluxo de avaliação em 3 fases
  references/
    mcp-rai-checklist.md               # Critérios de segurança e privacidade (RAI + OWASP)
    mcp-quality-checklist.md           # Critérios de qualidade técnica
```

## Funcionalidades

- **Fase 1 — Segurança e Privacidade**: credenciais, PII, operações destrutivas, injeção/SSRF, tokens
- **Fase 2 — Qualidade Técnica**: design de tools, tratamento de erros, skill companion, dependências, logging
- **Fase 3 — Responsabilidade**: licença, repo, versões, mantenedor
- Gera relatório Markdown com seções pontuadas (PASS / PARTIAL / FAIL)
- Veredicto geral: `SAFE TO USE` / `NEEDS FIXES` / `SECURITY RISK`

## Como usar

1. Instale o skill (veja abaixo)
2. Abra o chat do GitHub Copilot
3. Digite: `"Audite meu MCP do LinkedIn por segurança"` — Copilot lerá o código-fonte e gerará o relatório completo

## Instalação do skill

```bash
# macOS / Linux
cp -r mcp-evaluator ~/.copilot/skills/mcp-evaluator
```

Em seguida, reinicie o VS Code.

## Requisitos

- VS Code com GitHub Copilot
- Acesso ao código-fonte do servidor MCP a avaliar
