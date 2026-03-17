# WhatsApp MCP — Messages, Files and Groups from GitHub Copilot

This document describes the `whatsapp-mcp` skill in this repository.

## Description

Skill to send text messages, images, PDFs and VCF files to WhatsApp contacts and groups directly from GitHub Copilot. Manages groups (add/remove members, get invite link) and reads chat history. If the MCP is not installed, guides the user step by step to configure it.

Triggers: `send WhatsApp`, `WhatsApp message`, `WhatsApp file`, `WhatsApp group`, `WhatsApp contact`, `install WhatsApp MCP`.

## Structure

```text
whatsapp-mcp/
  SKILL.md                    # Skill instructions for GitHub Copilot
  references/
    tools.md                  # Complete reference of all MCP tools
    install.md                # Step-by-step installation guide
```

## Features

- Send text messages to contacts and groups
- Send files (PDF, images, VCF) as document attachments
- Search contacts by name or number
- List groups and members
- Add or remove group participants
- Get group invite link
- Read chat message history
- Detect if MCP is available and guide installation if not

## Skill installation

```bash
# macOS / Linux
cp -r whatsapp-mcp ~/.copilot/skills/whatsapp-mcp
```

Then restart VS Code.

## Requirements

- VS Code with GitHub Copilot
- Node.js ≥ 18
- `whatsapp-mcp-server` MCP server installed and configured
  - Repository: https://github.com/lunasoft2001/mcp
  - If not installed, the skill guides the user automatically

## Notes

- WhatsApp session is saved in `.wwebjs_auth` — no need to scan QR every session.
- The skill always shows a preview (`dryRun`) before sending for user confirmation.
- PDFs and non-image files are automatically sent as documents (`sendMediaAsDocument: true`).
