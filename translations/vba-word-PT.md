# Bundle de habilidade: Word VBA

Este documento descreve o conteúdo da habilidade `vba-word` neste repositório.

## Estrutura

```text
suites/office-vba/vba-word/
  SKILL.md                        # Metadados da habilidade (vba-word)
  references/
    word-vba-patterns.md          # Tipos de componentes VBA, eventos e padrões comuns
  scripts/
    export_vba_word.py            # Exportar módulos VBA para arquivos .bas/.cls
    import_vba_word.py            # Reimportar arquivos .bas/.cls para o .docm
```

## Objetivo

Extrair todos os módulos VBA de documentos Word com macros (`.docm` / `.dotm`),
refatorá-los no VS Code e reimportá-los com segurança — sempre criando um backup
com timestamp antes de qualquer importação.

## Instalação

Copie esta pasta para o diretório de habilidades do Copilot:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Em seguida, reinicie o VS Code.

## Notas

- Requer Windows + Microsoft Word instalado.
- Ative "Confiar no acesso ao modelo de objeto do projeto VBA" no Centro de Confiabilidade do Word.
- Sempre feche o Word antes de executar os scripts.
- Um backup do `.docm` é criado automaticamente antes de qualquer importação.
- Faz parte da **Suite VBA do Office** — use `office-vba-orchestrator` para rotear entre habilidades.
