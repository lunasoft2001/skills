# Bundle de Skill: PowerPoint VBA

Este documento describe el contenido del skill `vba-powerpoint` en este repositorio.

## Estructura

```text
suites/office-vba/vba-powerpoint/
  SKILL.md                        # Metadata del skill (vba-powerpoint)
  references/
    ppt-vba-patterns.md           # Tipos de componentes VBA, eventos y patrones comunes
  scripts/
    export_vba_ppt.py             # Exporta módulos VBA a archivos .bas/.cls
    import_vba_ppt.py             # Reimporta archivos .bas/.cls al .pptm
```

## Propósito

Extraer todos los módulos VBA de presentaciones PowerPoint con macros (`.pptm` / `.potm`), refactorizarlos en VS Code y reimportarlos de forma segura — creando siempre una copia de seguridad con marca de tiempo antes de cualquier importación.

## Instalación

Copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "vba-powerpoint" -Destination "$env:USERPROFILE\.copilot\skills\vba-powerpoint" -Recurse
```

Luego reinicia VS Code.

## Notas

- Requiere Windows + Microsoft PowerPoint instalado.
- Habilita "Confiar en el acceso al modelo de objetos del proyecto VBA" en el Centro de confianza de PowerPoint.
- La automatización COM puede requerir que PowerPoint sea visible — los scripts lo gestionan automáticamente.
- Cierra siempre PowerPoint antes de ejecutar los scripts.
- Se crea un backup del `.pptm` automáticamente antes de cualquier importación.
- Parte de la **Suite VBA de Office** — usa `office-vba-orchestrator` para enrutar entre skills.
