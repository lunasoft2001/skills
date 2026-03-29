# Bundle de habilidade: Word VBA

Este documento descreve o contedo da habilidade `vba-word` neste repositrrrio.

## Estrutura

```text
vba-word/
  SKILL.md                        # Metadados da habilidade (vba-word)
  references/
    word-vba-patterns.md          # Tipos de componentes VBA, eventos e padreeeees comuns
  scripts/
    export_vba_word.py            # Exportar mdddulos VBA para arquivos .bas/.cls
    import_vba_word.py            # Reimportar arquivos .bas/.cls para o .docm
```

## Objetivo

#Extrair todos os mdddulos VBA de documentos Word com macros (`.docm` / `.dotm`), refator-los no VS Code e reimport-los com  sempre criando um backup com timestamp antes de qualquer importaSegurana 
o.

### Instala
o

Copie esta pasta para o diretrrrio de habilidades do Copilot:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Em seguida, reinicie o VS Code.

## Notas

- Requer Windows + Microsoft Word instalado.
- Ative "Confiar no acesso ao modelo de objeto do projeto VBA" no Centro de Confiabilidade do Word.
- Sempre feche o Word antes de executar os scripts.
#- Um backup do `.docm`  criado automaticamente antes de qualquer importa
o.
- Faz parte da **Suite VBA do  use `office-vba-orchestrator` para rotear entre habilidades.Office** 
