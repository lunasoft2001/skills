# M365 Email Manager Skill Bundle

Este documento descreve o conteudo do `m365-email-manager-skill` neste repositorio.

## Estrutura

```text
m365-email-manager-skill/
  SKILL.md                        # Metadados do skill e guia de uso
  scripts/                        # Scripts Python para setup, autenticacao e operacoes de email
    setup.py                      # Fluxo de configuracao inicial
    token_manager.py              # Gerenciamento e renovacao de tokens
    m365_mail.py                  # CLI principal para acoes de email no Microsoft 365
    m365_mail_es.py               # Variante da CLI em espanhol
    test_demo.py                  # Helper de demo/testes
  references/                     # Documentacao de apoio (quickstart, permissoes, API, body options)
```

## Instalacao

Para instalar este skill no GitHub Copilot, copie esta pasta para o diretorio de skills do Copilot:

```powershell
Copy-Item -Path "m365-email-manager-skill" -Destination "$env:USERPROFILE\.copilot\skills\m365-email-manager-skill" -Recurse
```

Depois, reinicie o VS Code.

## Notas

- Este skill automatiza acoes de email do Microsoft 365 por meio do Microsoft Graph.
- Operacoes tipicas: listar, buscar, enviar, responder, mover e marcar como lido.
- Execute o setup uma vez (`scripts/setup.py`) para evitar prompts repetidos de autenticacao.
