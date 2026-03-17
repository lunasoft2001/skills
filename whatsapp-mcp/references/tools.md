# WhatsApp MCP — Tools Reference

Todas las tools disponibles en el servidor MCP `whatsapp-mcp-server`.

## Mensajes

### `send_direct_message`
Envía un mensaje de texto privado a un número de teléfono.
- `phoneNumber` (string): número internacional sin `+` (ej: `436608668107`)
- `message` (string): texto del mensaje
- `dryRun` (bool, default false): si true, muestra preview sin enviar

### `send_group_message`
Envía un mensaje de texto a un grupo de WhatsApp.
- `chatId` (string): ID del grupo (termina en `@g.us`)
- `message` (string): texto del mensaje
- `dryRun` (bool, default false)

### `send_media_message`
Envía un archivo (PDF, imagen, VCF, etc.) a un grupo o contacto.
- `chatId` (string): ID destino (`@c.us` o `@g.us`)
- `filePath` (string): ruta absoluta al archivo en disco
- `caption` (string, opcional): texto que acompaña al archivo
- `dryRun` (bool, default false)

> PDFs y no-imágenes se envían automáticamente como documento (`sendMediaAsDocument: true`).

### `get_chat_messages`
Devuelve los últimos mensajes de un chat.
- `chatId` (string): ID del chat
- `limit` (int, 1-100, default 20): número de mensajes a recuperar

---

## Contactos

### `find_whatsapp_contact`
Busca contactos por nombre o número.
- `search` (string): nombre parcial o número
- Devuelve array con `id`, `number`, `name`, `pushname`, `isMyContact`
- Usar el `id` que termina en `@c.us` para enviar mensajes

---

## Grupos

### `list_whatsapp_groups`
Lista todos los grupos en los que participa la cuenta.
- Sin parámetros
- Devuelve `id` (@g.us), `name`, `participantsCount`

### `find_whatsapp_group`
Busca grupos por nombre.
- `search` (string): nombre parcial del grupo

### `list_group_members`
Lista los miembros de un grupo.
- `chatId` (string): ID del grupo (`@g.us`)
- Devuelve array con `id`, `number`, `name`, `isAdmin`

### `add_group_participant`
Añade un participante a un grupo.
- `chatId` (string): ID del grupo (`@g.us`)
- `phoneNumber` (string): número del nuevo miembro (sin `+`)
- `dryRun` (bool, default false)

### `remove_group_participant`
Elimina un participante de un grupo.
- `chatId` (string): ID del grupo (`@g.us`)
- `phoneNumber` (string): número del miembro a eliminar
- `dryRun` (bool, default false)

### `get_group_invite_link`
Obtiene el enlace de invitación de un grupo.
- `chatId` (string): ID del grupo (`@g.us`)

---

## Sistema

### `healthcheck_whatsapp`
Devuelve el estado del servidor MCP y del cliente WhatsApp.
- Sin parámetros
- Respuesta: `{ mcpServer, whatsapp, uptime, readySince }`
- Estados posibles de `whatsapp`: `ready`, `initializing`, `disconnected`
