# WhatsApp MCP — Mensajes, Archivos y Grupos desde GitHub Copilot

Este documento describe el skill `whatsapp-mcp` en este repositorio.

## Descripción

Skill para enviar mensajes de texto, imágenes, PDFs y archivos VCF a contactos y grupos de WhatsApp directamente desde GitHub Copilot. Gestiona grupos (añadir/eliminar miembros, obtener enlace) y lee el historial de chats. Si el MCP no está instalado, guía al usuario paso a paso para configurarlo.

Activadores: `enviar WhatsApp`, `mensaje WhatsApp`, `mandar por WhatsApp`, `enviar archivo WhatsApp`, `grupo WhatsApp`, `contacto WhatsApp`, `instalar MCP WhatsApp`.

## Estructura

```text
whatsapp-mcp/
  SKILL.md                    # Instrucciones del skill para GitHub Copilot
  references/
    tools.md                  # Referencia completa de todas las tools MCP
    install.md                # Guía de instalación paso a paso
```

## Funcionalidades

- Enviar mensajes de texto a contactos y grupos
- Enviar archivos (PDF, imágenes, VCF) como documentos adjuntos
- Buscar contactos por nombre o número
- Listar grupos y miembros
- Añadir o eliminar participantes de grupos
- Obtener enlace de invitación de grupo
- Leer historial de mensajes de un chat
- Detectar si el MCP está disponible y guiar la instalación si no lo está

## Instalación del skill

```bash
# macOS / Linux
cp -r whatsapp-mcp ~/.copilot/skills/whatsapp-mcp
```

Luego reinicia VS Code.

## Requisitos

- VS Code con GitHub Copilot
- Node.js ≥ 18
- Servidor MCP `whatsapp-mcp-server` instalado y configurado
  - Repositorio: https://github.com/lunasoft2001/mcp
  - Si no está instalado, el skill guía al usuario automáticamente

## Notas

- La sesión de WhatsApp se guarda en `.wwebjs_auth` — no es necesario escanear el QR en cada sesión.
- El skill siempre hace un preview (`dryRun`) antes de enviar para que el usuario confirme.
- PDFs y archivos no-imagen se envían automáticamente como documentos (`sendMediaAsDocument: true`).
