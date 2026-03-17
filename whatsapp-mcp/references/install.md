# WhatsApp MCP — Guía de Instalación

Usa esta guía cuando el usuario intente usar el MCP de WhatsApp y no esté disponible (tool no encontrada, error de conexión, o healthcheck falla).

## Requisitos previos

- VS Code con GitHub Copilot
- Node.js ≥ 18 (`node --version`)
- Git

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/lunasoft2001/mcp.git whatsapp-mcp-server
cd whatsapp-mcp-server/whatsapp
npm install
npm run build
```

Confirmar que se generó `dist/index.js`:
```bash
ls dist/index.js
```

### 2. Verificar que `start.sh` es ejecutable

```bash
chmod +x /ruta/completa/whatsapp-mcp-server/start.sh
```

### 3. Configurar en VS Code

**Opción A — Global** (disponible en todos los workspaces):

Abrir `Cmd+Shift+P` → "Open MCP Configuration" y añadir:

```json
"whatsapp": {
  "type": "stdio",
  "command": "/ruta/completa/whatsapp-mcp-server/start.sh",
  "args": [],
  "env": {
    "PATH": "/ruta/a/node/bin:/usr/local/bin:/usr/bin:/bin",
    "DEFAULT_COUNTRY_CODE": "43",
    "LOG_LEVEL": "info",
    "WA_SESSION_PATH": "/ruta/completa/whatsapp-mcp-server/.wwebjs_auth",
    "WA_SESSION_NAME": "mcp-session"
  }
}
```

> Sustituir `/ruta/completa/` por la ruta real donde se clonó el repo.  
> Para encontrar la ruta de node: `which node` o `node -e "console.log(process.execPath)"`

**Opción B — Solo en un workspace**, añadir el mismo bloque dentro de `"mcp": { "servers": { ... } }` en el archivo `.code-workspace` o en `.vscode/settings.json`.

### 4. Recargar VS Code

`Cmd+Shift+P` → "Developer: Reload Window"

### 5. Escanear el QR de WhatsApp

Al primer arranque, el servidor imprime un QR en el log. Para verlo:

1. Abrir la paleta: `Cmd+Shift+P` → "MCP: Show Output"
2. Seleccionar el servidor `whatsapp`
3. Abrir WhatsApp en el móvil → Dispositivos vinculados → Vincular dispositivo → escanear QR

La sesión queda guardada en `.wwebjs_auth` y no se necesita escanear de nuevo.

### 6. Verificar

```
healthcheck_whatsapp → { "whatsapp": "ready" }
```

---

## Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Tool no aparece en Copilot | MCP no arrancó | Recargar ventana, revisar output MCP |
| `whatsapp: initializing` | Sesión cargando | Esperar 10-15 segundos |
| `whatsapp: disconnected` | Sin sesión o móvil desconectado | Escanear QR de nuevo |
| Error `node: command not found` | PATH incorrecto en env | Añadir ruta completa de node al `PATH` del env |
| Proceso duplicado al recargar | Instancia anterior viva | El `start.sh` incluye `pkill` automático |
| PDF no se envía | Versión antigua sin `sendMediaAsDocument` | Actualizar: `git pull && npm run build` |

## Actualizar el servidor

```bash
cd whatsapp-mcp-server
git pull origin main
cd whatsapp
npm run build
```

Luego recargar VS Code.
