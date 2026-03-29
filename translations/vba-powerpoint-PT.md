# Bundle de habilidade: PowerPoint VBA

Este documento descreve o conteúdo da habilidade `vba-powerpoint` neste repositório.

## Estrutura

```text
vba-powerpoint/
  SKILL.md                        # Metadados da habilidade (vba-powerpoint)
  references/
    ppt-vba-patterns.md           # Tipos de componentes VBA, eventos e padrões
  scripts/
    export_vba_ppt.py             # Exportar módulos VBA para arquivos .bas/.cls
    import_vba_ppt.py             # Reimportar os arquivos no .pptm
```

## Objetivo

Extrair todos os módulos VBA de apresentações PowerPoint com macros (`.pptm` / `.potm`), refatorá-los no VS Code e reimportá-los com segurança — com backup automático com timestamp antes de cada importação.

## Instalação

```powershell
Copy-Item -Path "vba-powerpoint" -Destination "$env:USERPROFILE\.copilot\skills\vba-powerpoint" -Recurse
```

Em seguida, reinicie o VS Code.

## Notas

- Requer Windows + Microsoft PowerPoint instalado.
- Ative o acesso confiável ao modelo VBA no Centro de Confiabilidade do PowerPoint.
- Feche o PowerPoint antes de executar os scripts.
- Um backup do `.pptm` é criado automaticamente antes de cada importação.
- Faz parte da **Suite VBA do Office** — use `office-vba-orchestrator` para rotear entre habilidades.
