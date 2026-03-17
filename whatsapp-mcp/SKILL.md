---
name: whatsapp-mcp
description: "Send WhatsApp messages, files (PDF, images, VCF), and manage groups and contacts using the WhatsApp MCP server (whatsapp-web.js). Use this skill when the user wants to send a WhatsApp message, find a contact, list groups, send a document or image via WhatsApp, add/remove group members, or get chat history. Also use when the user asks how to install or configure the WhatsApp MCP. Triggers on: send WhatsApp, mensaje WhatsApp, mandar por WhatsApp, enviar archivo WhatsApp, grupo WhatsApp, contacto WhatsApp, instalar MCP WhatsApp."
---

# WhatsApp MCP Skill

Este skill permite enviar mensajes, archivos y gestionar grupos de WhatsApp desde GitHub Copilot usando el servidor MCP `whatsapp-mcp-server` (basado en whatsapp-web.js).

## Paso 0 — Verificar si el MCP está disponible

Antes de cualquier operación, ejecuta `healthcheck_whatsapp`. Interpreta el resultado:

| Resultado | Acción |
|---|---|
| `"whatsapp": "ready"` | Continúa normalmente |
| `"whatsapp": "initializing"` | Espera 5-10 segundos y reintenta |
| Error / tool no disponible | Guía al usuario con [references/install.md](references/install.md) |

## Flujo principal

### Enviar mensaje de texto
1. Buscar contacto: `find_whatsapp_contact` con nombre o número
2. Usar el `id` que termina en `@c.us` como `chatId`/`phoneNumber`
3. Siempre hacer `dryRun: true` primero para que el usuario confirme
4. Con confirmación: enviar con `dryRun: false`

### Enviar archivo (PDF, imagen, VCF, etc.)
1. Verificar que el archivo existe en disco (ruta absoluta)
2. Si hay que convertir HTML→PDF: usar Chrome headless:
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --headless=new --disable-gpu --no-sandbox \
     --print-to-pdf="/ruta/output.pdf" --print-to-pdf-no-header \
     "file:///ruta/input.html"
   ```
3. `dryRun: true` → confirmar → `send_media_message` con `dryRun: false`

### Grupos
- Listar grupos: `list_whatsapp_groups`
- Añadir miembro: `add_group_participant` (necesita número normalizado)
- Eliminar miembro: `remove_group_participant`
- Link de invitación: `get_group_invite_link`

### Historial de chat
- `get_chat_messages` con `chatId` y `limit` (máx 100)

## Reglas importantes

- **Siempre dryRun primero** antes de enviar — nunca enviar sin confirmación del usuario.
- Los `chatId` para contactos terminan en `@c.us`, para grupos en `@g.us`.
- Para números austriacos: el código de país es `43`. Los locales `069x` se normalizan automáticamente.
- PDFs e imágenes: `send_media_message` acepta ruta absoluta en disco del servidor.
- Si el contacto no aparece: probar con apellido/nombre invertidos o variantes de mayúsculas.

## Referencia de tools

Ver [references/tools.md](references/tools.md) para descripción completa de cada tool MCP disponible.

## Instalación del MCP

Si el MCP no está disponible, ver [references/install.md](references/install.md) para guiar al usuario paso a paso.
