# WhatsApp MCP — Mensagens, Arquivos e Grupos do GitHub Copilot

Este documento descreve o skill `whatsapp-mcp` neste repositório.

## Descrição

Skill para enviar mensagens de texto, imagens, PDFs e arquivos VCF para contatos e grupos do WhatsApp diretamente do GitHub Copilot. Gerencia grupos (adicionar/remover membros, obter link de convite) e lê o histórico de chats. Se o MCP não estiver instalado, orienta o usuário passo a passo para configurá-lo.

Gatilhos: `enviar WhatsApp`, `mensagem WhatsApp`, `arquivo WhatsApp`, `grupo WhatsApp`, `instalar MCP WhatsApp`.

## Estrutura

```text
whatsapp-mcp/
  SKILL.md                    # Instruções do skill para GitHub Copilot
  references/
    tools.md                  # Referência completa de todas as ferramentas MCP
    install.md                # Guia de instalação passo a passo
```

## Instalação do skill

```bash
cp -r whatsapp-mcp ~/.copilot/skills/whatsapp-mcp
```

Reiniciar o VS Code.

## Requisitos

- VS Code com GitHub Copilot
- Node.js ≥ 18
- Servidor MCP `whatsapp-mcp-server` instalado e configurado
  - Repositório: https://github.com/lunasoft2001/mcp
