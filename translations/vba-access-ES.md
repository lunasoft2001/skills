# Bundle de Skill: Access VBA

Este documento describe el contenido del skill `vba-access` en este repositorio.

## Estructura

```text
vba-access/
  SKILL.md                        # Metadata del skill (vba-access)
  references/
    access-vba-patterns.md        # Tipos de componentes VBA, patrones DAO/ADO y solución de problemas
  scripts/
    export_vba_access.py          # Exporta módulos VBA estándar/clase a archivos .bas/.cls
    import_vba_access.py          # Reimporta archivos .bas/.cls al .accdb
```

## Propósito

Extraer módulos VBA estándar y de clase de bases de datos Access (`.accdb` / `.mdb`), refactorizarlos en VS Code y reimportarlos de forma segura — creando siempre una copia de seguridad con marca de tiempo antes de cualquier importación.

> **Nota:** Este skill gestiona únicamente módulos VBA. Para análisis completo de la base de datos (tablas, consultas, formularios, informes), usa el skill **access-analyzer**.

## Instalación

Copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "vba-access" -Destination "$env:USERPROFILE\.copilot\skills\vba-access" -Recurse
```

Luego reinicia VS Code.

## Notas

- Requiere Windows + Microsoft Access instalado.
- Habilita "Confiar en el acceso al modelo de objetos del proyecto VBA" en el Centro de confianza de Access.
- Cierra siempre Access y asegúrate de que no exista ningún archivo `.laccdb` de bloqueo antes de ejecutar los scripts.
- Se crea un backup del `.accdb` automáticamente antes de cualquier importación.
- Parte de la **Suite VBA de Office** — usa `office-vba-orchestrator` para enrutar entre skills.
