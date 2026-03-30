# Bundle de Skill: Orquestador VBA de Office

Este documento describe el contenido del skill `office-vba-orchestrator` en este repositorio.

## Estructura

```text
suites/office-vba/office-vba-orchestrator/
  SKILL.md                        # Metadata del skill (office-vba-orchestrator)
  references/
    routing-guide.md              # Detección de tipo de archivo y lógica de enrutamiento
    backup-policy.md              # Política de backup obligatoria y procedimientos de rollback
```

## Propósito

Enrutar las tareas VBA de Office hacia el skill correcto por aplicación (vbaExcel, vba-word, vba-powerpoint, vba-access) y aplicar la política obligatoria de backup-antes-de-importar en toda la suite VBA de Office.

## Cuándo Usarlo

- Cuando el usuario menciona una tarea VBA de Office sin especificar la aplicación.
- Cuando se trabaja con múltiples tipos de archivo de Office en la misma sesión.
- Para obtener una referencia rápida sobre qué skill gestiona qué tipo de archivo.
- Para aplicar la política de backup antes de cualquier operación destructiva.

## Skills Soportados

| Tipo de archivo | Aplicación | Skill |
|-----------------|------------|-------|
| `.xlsm`, `.xlam` | Excel | `vbaExcel` |
| `.docm`, `.dotm` | Word | `vba-word` |
| `.pptm`, `.potm` | PowerPoint | `vba-powerpoint` |
| `.accdb`, `.mdb` | Access | `vba-access` |
| Outlook | — | ❌ No soportado |

## Instalación

Copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "office-vba-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\office-vba-orchestrator" -Recurse
```

Luego reinicia VS Code.

## Notas

- Todos los sub-skills deben estar instalados también.
- El orquestador aplica la política universal de backup definida en `references/backup-policy.md`.
- El VBA de Outlook está explícitamente excluido de esta suite.
