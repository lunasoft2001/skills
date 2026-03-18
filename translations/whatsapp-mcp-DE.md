# WhatsApp MCP — Nachrichten, Dateien und Gruppen aus GitHub Copilot

Dieses Dokument beschreibt das Skill `whatsapp-mcp` in diesem Repository.

## Beschreibung

Skill zum Senden von Textnachrichten, Bildern, PDFs und VCF-Dateien an WhatsApp-Kontakte und Gruppen direkt aus GitHub Copilot. Verwaltet Gruppen (Mitglieder hinzufügen/entfernen, Einladungslink abrufen) und liest den Chat-Verlauf. Falls der MCP nicht installiert ist, führt er den Benutzer Schritt für Schritt durch die Konfiguration.

Auslöser: `WhatsApp senden`, `WhatsApp Nachricht`, `WhatsApp Datei`, `WhatsApp Gruppe`, `WhatsApp MCP installieren`.

## Struktur

```text
whatsapp-mcp/
  SKILL.md                    # Skill-Anweisungen für GitHub Copilot
  references/
    tools.md                  # Vollständige Referenz aller MCP-Tools
    install.md                # Schritt-für-Schritt Installationsanleitung
```

## Installation des Skills

```bash
cp -r whatsapp-mcp ~/.copilot/skills/whatsapp-mcp
```

Dann VS Code neu starten.

## Voraussetzungen

- VS Code mit GitHub Copilot
- Node.js ≥ 18
- MCP-Server `whatsapp-mcp-server` installiert und konfiguriert
  - Repository: https://github.com/lunasoft2001/mcp
