# WhatsApp MCP — Messages, Fichiers et Groupes depuis GitHub Copilot

Ce document décrit le skill `whatsapp-mcp` dans ce dépôt.

## Description

Skill pour envoyer des messages texte, images, PDFs et fichiers VCF à des contacts et groupes WhatsApp directement depuis GitHub Copilot. Gère les groupes (ajouter/supprimer des membres, obtenir un lien d'invitation) et lit l'historique des chats. Si le MCP n'est pas installé, guide l'utilisateur étape par étape pour le configurer.

Déclencheurs : `envoyer WhatsApp`, `message WhatsApp`, `fichier WhatsApp`, `groupe WhatsApp`, `installer MCP WhatsApp`.

## Structure

```text
whatsapp-mcp/
  SKILL.md                    # Instructions du skill pour GitHub Copilot
  references/
    tools.md                  # Référence complète de tous les outils MCP
    install.md                # Guide d'installation étape par étape
```

## Installation du skill

```bash
cp -r whatsapp-mcp ~/.copilot/skills/whatsapp-mcp
```

Redémarrer VS Code.

## Prérequis

- VS Code avec GitHub Copilot
- Node.js ≥ 18
- Serveur MCP `whatsapp-mcp-server` installé et configuré
  - Dépôt : https://github.com/lunasoft2001/mcp
