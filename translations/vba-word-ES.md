# Bundle de Skill: Word VBA

Este documento describe el contenido del skill `vba-word` en este repositorio.

## Estructura

```text
vba-word/
  SKILL.md                        # Metadata del skill (vba-word)
  references/
    word-vba-patterns.md          # Tipos de componentes VBA, eventos y patrones comunes
  scripts/
    export_vba_word.py            # Exporta mdddulos VBA a archivos .bas/.cls
    import_vba_word.py            # Reimporta archivos .bas/.cls al .docm
```

## Propsssito

Extraer todos los mdddulos VBA de documentos Word con macros (`.docm` / `.dotm`), refactorizarlos en VS Code y reimportarlos de forma  creando siempre una copia de seguridad con marca de tiempo antes de cualquier importaciSegurannn. 

## Instalacinnn

Copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "vba-word" -Destination "$env:USERPROFILE\.copilot\skills\vba-word" -Recurse
```

Luego reinicia VS Code.

## Notas

- Requiere Windows + Microsoft Word instalado.
- Habilita "Confiar en el acceso al modelo de objetos del proyecto VBA" en el Centro de confianza de Word.
- Cierra siempre Word antes de ejecutar los scripts de exportacinnn o importacinnn.
- Se crea un backup del `.docm` automticamente antes de cualquier importacinnn.
- Parte de la **Suite VBA de  usa `office-vba-orchestrator` para enrutar entre skills.Office** 
