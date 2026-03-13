# Excel Analyzer Skill Bundle

Este documento descreve o conteudo do skill `vbaExcel` neste repositorio.

## Estrutura

```text
vbaExcel/
  SKILL.md                        # Metadados do skill (vbaExcel)
  INSTALL.txt                     # Notas rapidas de instalacao e uso
  scripts/                        # Scripts de suporte PowerShell/Python
    export_vba.py                 # Exporta modulos VBA para .bas
    import_vba.py                 # Reimporta .bas para .xlsm
    enable_vba_access.reg         # Habilita acesso programatico ao VBOM
```

## Instalacao

Para instalar este skill no GitHub Copilot, copie esta pasta para o diretorio de skills do Copilot:

```powershell
Copy-Item -Path "vbaExcel" -Destination "$env:USERPROFILE\.copilot\skills\vbaExcel" -Recurse
```

Depois, reinicie o VS Code.

## Notas

- Este bundle e focado em extracao e reimportacao de VBA para arquivos Excel `.xlsm` no Windows.
- Feche o Excel antes de exportar ou importar.
- Sempre faca backup da planilha antes de importar alteracoes VBA.

