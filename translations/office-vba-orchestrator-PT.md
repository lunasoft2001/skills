# Bundle de habilidade: Orquestrador VBA Office

Este documento descreve o conteúdo da habilidade `office-vba-orchestrator` neste repositório.

## Estrutura

```text
suites/office-vba/office-vba-orchestrator/
  SKILL.md                        # Metadados da habilidade (office-vba-orchestrator)
  references/
    routing-guide.md              # Detecção de tipo de arquivo e lógica de roteamento
    backup-policy.md              # Política de backup obrigatória e procedimentos de rollback
```

## Objetivo

Rotear as tarefas VBA do Office para a habilidade correta (vbaExcel, vba-word, vba-powerpoint, vba-access) e aplicar a política obrigatória de backup-antes-da-importação em toda a suite VBA do Office.

## Habilidades suportadas

| Tipo de arquivo | Aplicação | Habilidade |
|---|---|---|
| `.xlsm`, `.xlam` | Excel | `vbaExcel` |
| `.docm`, `.dotm` | Word | `vba-word` |
| `.pptm`, `.potm` | PowerPoint | `vba-powerpoint` |
| `.accdb`, `.mdb` | Access | `vba-access` |
| Outlook | — | ❌ Não suportado |

## Instalação

```powershell
Copy-Item -Path "office-vba-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\office-vba-orchestrator" -Recurse
```

## Notas

- Todas as sub-habilidades devem ser instaladas separadamente.
- O orquestrador aplica a política universal de backup.
- VBA do Outlook está explicitamente excluído desta suite.
