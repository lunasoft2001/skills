# M365 Email Manager Skill Bundle

Este documento describe el contenido del `m365-email-manager-skill` en este repositorio.

## Estructura

```text
m365-email-manager-skill/
  SKILL.md                        # Metadata del skill y guia de uso
  scripts/                        # Scripts Python para setup, autenticacion y operaciones de correo
    setup.py                      # Flujo de configuracion inicial
    token_manager.py              # Gestion y renovacion de tokens
    m365_mail.py                  # CLI principal para acciones de correo en Microsoft 365
    m365_mail_es.py               # Variante de CLI en espanol
    test_demo.py                  # Helper de demo/pruebas
  references/                     # Documentacion de apoyo (quickstart, permisos, API, body options)
```

## Instalacion

Para instalar este skill en GitHub Copilot, copia esta carpeta al directorio de skills de Copilot:

```powershell
Copy-Item -Path "m365-email-manager-skill" -Destination "$env:USERPROFILE\.copilot\skills\m365-email-manager-skill" -Recurse
```

Luego reinicia VS Code.

## Notas

- Este skill automatiza acciones de correo de Microsoft 365 mediante Microsoft Graph.
- Operaciones tipicas: listar, buscar, enviar, responder, mover y marcar como leido.
- Ejecuta setup una vez (`scripts/setup.py`) para evitar prompts repetidos de autenticacion.
