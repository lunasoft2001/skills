# Bundle de Skill: Word VBA

Este documento describe el contenido del skill `vba-word` en este repositorio.

## Estructura

```text
suites/office-vba/vba-word/
  SKILL.md                        # Metadata del skill (vba-word)
  references/
    word-vba-patterns.md          # Tipos de componentes VBA, eventos y patrones comunes
  scripts/
    export_vba_word.py            # Exporta módulos VBA a archivos .bas/.cls
    import_vba_word.py            # Reimporta archivos .bas/.cls al .docm
```

## Propósito

Extraer todos los módulos VBA de documentos Word con macros (`.docm` / `.dotm`),
refactorizarlos en VS Code y reimportarlos de forma segura — creando siempre una
copia de seguridad con marca de tiempo antes de cualquier importación.

## Instalación

Copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Luego reinicia VS Code.

## Notas

- Requiere Windows + Microsoft Word instalado.
- Habilita "Confiar en el acceso al modelo de objetos del proyecto VBA" en el Centro de confianza de Word.
- Cierra siempre Word antes de ejecutar los scripts de exportación o importación.
- Se crea un backup del `.docm` automáticamente antes de cualquier importación.
- Parte de la **Suite VBA de Office** — usa `office-vba-orchestrator` para enrutar entre skills.
