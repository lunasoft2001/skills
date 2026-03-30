# Bundle de habilidade: Access VBA

Este documento descreve o conteúdo da habilidade `vba-access` neste repositório.

## Estrutura

```text
vba-access/
  SKILL.md                        # Metadados da habilidade (vba-access)
  references/
    access-vba-patterns.md        # Tipos de componentes VBA, padrões DAO/ADO e solução de problemas
  scripts/
    export_vba_access.py          # Exportar módulos standard/classe para .bas/.cls
    import_vba_access.py          # Reimportar os arquivos no .accdb
```

## Objetivo

Extrair módulos VBA standard e de classe de bancos de dados Access (`.accdb` / `.mdb`), refatorá-los no VS Code e reimportá-los com segurança — com backup automático com timestamp antes de cada importação.

> **Nota:** Esta habilidade gerencia apenas módulos VBA. Para análise completa do banco de dados (tabelas, consultas, formulários, relatórios), use a habilidade **access-analyzer**.

## Instalação

```powershell
Copy-Item -Path "vba-access" -Destination "$env:USERPROFILE\.copilot\skills\vba-access" -Recurse
```

## Notas

- Requer Windows + Microsoft Access instalado.
- Ative o acesso confiável ao modelo VBA no Centro de Confiabilidade do Access.
- Feche o Access e verifique a ausência de arquivo de bloqueio `.laccdb`.
- Um backup do `.accdb` é criado automaticamente antes de cada importação.
- Faz parte da **Suite VBA do Office** — use `office-vba-orchestrator`.
