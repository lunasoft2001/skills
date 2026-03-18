# Excel Analyzer Skill Bundle

Este documento describe el contenido del skill `vbaExcel` en este repositorio.

## Estructura

```text
vbaExcel/
  SKILL.md                        # Metadata del skill (vbaExcel)
  INSTALL.txt                     # Notas rapidas de instalacion y uso
  scripts/                        # Scripts de soporte PowerShell/Python
    export_vba.py                 # Exporta modulos VBA a .bas
    import_vba.py                 # Reimporta .bas a .xlsm
    enable_vba_access.reg         # Habilita acceso programatico a VBOM
```

## Instalacion

Para instalar este skill en GitHub Copilot, copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "vbaExcel" -Destination "$env:USERPROFILE\.copilot\skills\vbaExcel" -Recurse
```

Luego reinicia VS Code.

## Notas

- Este bundle se centra en extraer y reimportar VBA para archivos Excel `.xlsm` en Windows.
- Cierra Excel antes de exportar o importar.
- Haz siempre backup del libro antes de importar cambios VBA.

