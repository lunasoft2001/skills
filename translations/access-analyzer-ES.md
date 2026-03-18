# Access Analyzer Skill Bundle

Este documento describe el contenido del skill `access-analyzer` dentro de este repositorio.

## Estructura

```text
access-analyzer/
  SKILL.md                        # Metadata del skill
  scripts/                        # Scripts PowerShell de automatizacion
    access-backup.ps1             # Crear backups
    access-export-git.ps1         # Exportar con integracion Git
    access-import-changed.ps1     # Importar solo objetos modificados
    access-import.ps1             # Importar todos los objetos
  references/                     # Documentacion de referencia
    AccessObjectTypes.md          # Tipos de objetos en Access
    ExportTodoSimple.bas          # Modulo VBA de exportacion
    VBA-Patterns.md               # Patrones de codigo VBA
  assets/                         # Recursos del skill
    AccessAnalyzer.accdb          # Base de datos de ejemplo/template
```

## Instalacion

Para instalar este skill en GitHub Copilot, puedes copiar esta carpeta a tu directorio de skills de Copilot:

```powershell
Copy-Item -Path "access-analyzer" -Destination "$env:USERPROFILE\.copilot\skills\access-analyzer" -Recurse
```

Luego reinicia VS Code.

## Notas

- Este bundle esta optimizado para GitHub Copilot.
- Incluye solo los archivos esenciales del skill.
- `AccessAnalyzer.accdb` se incluye en `assets/` como recurso de soporte.
