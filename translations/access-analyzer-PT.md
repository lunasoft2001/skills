# Access Analyzer Skill Bundle

Este documento descreve o conteudo do skill `access-analyzer` neste repositorio.

## Estrutura

```text
access-analyzer/
  SKILL.md                        # Metadados do skill
  scripts/                        # Scripts PowerShell de automacao
    access-backup.ps1             # Criar backups
    access-export-git.ps1         # Exportar com integracao Git
    access-import-changed.ps1     # Importar apenas objetos alterados
    access-import.ps1             # Importar todos os objetos
  references/                     # Documentacao de referencia
    AccessObjectTypes.md          # Tipos de objetos do Access
    ExportTodoSimple.bas          # Modulo VBA de exportacao
    VBA-Patterns.md               # Padroes de codigo VBA
  assets/                         # Recursos do skill
    AccessAnalyzer.accdb          # Base de dados de exemplo/template
```

## Instalacao

Para instalar este skill no GitHub Copilot, copie esta pasta para o diretorio de skills do Copilot:

```powershell
Copy-Item -Path "access-analyzer" -Destination "$env:USERPROFILE\.copilot\skills\access-analyzer" -Recurse
```

Depois, reinicie o VS Code.

## Notas

- Este bundle esta otimizado para GitHub Copilot.
- Inclui apenas os arquivos essenciais do skill.
- `AccessAnalyzer.accdb` esta em `assets/` como recurso de apoio.
