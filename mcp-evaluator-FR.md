# MCP Evaluator — Audit des serveurs MCP : Sécurité, Confidentialité et Qualité

Ce document décrit le skill `mcp-evaluator` de ce dépôt.

## Description

Skill qui audite les serveurs MCP (Model Context Protocol) en termes de sécurité, confidentialité et qualité technique. Analyse le code source (TypeScript/Python), les définitions de tools, les fichiers de configuration et le SKILL.md companion. Produit un rapport structuré PASS/PARTIAL/FAIL avec des corrections actionnables.

Déclencheurs : `auditer MCP`, `évaluer serveur MCP`, `vérifier sécurité MCP`, `réviser les tools MCP`, `mon MCP est-il sécurisé`, `MCP prêt à publier`.

## Structure

```text
mcp-evaluator/
  SKILL.md                              # Instructions + workflow d'évaluation en 3 phases
  references/
    mcp-rai-checklist.md               # Critères de sécurité et confidentialité (RAI + OWASP)
    mcp-quality-checklist.md           # Critères de qualité technique
```

## Fonctionnalités

- **Phase 1 — Sécurité & Confidentialité** : identifiants, PII, opérations destructives, injection/SSRF, tokens
- **Phase 2 — Qualité Technique** : conception des tools, gestion des erreurs, skill companion, dépendances, logging
- **Phase 3 — Responsabilité** : licence, dépôt, versionnage, mainteneur
- Génère un rapport Markdown avec des sections notées (PASS / PARTIAL / FAIL)
- Verdict global : `SAFE TO USE` / `NEEDS FIXES` / `SECURITY RISK`

## Utilisation

1. Installer le skill (voir ci-dessous)
2. Ouvrir le chat GitHub Copilot
3. Saisir : `"Audite mon MCP LinkedIn pour la sécurité"` — Copilot lira le code source et générera le rapport complet

## Installation du skill

```bash
# macOS / Linux
cp -r mcp-evaluator ~/.copilot/skills/mcp-evaluator
```

Puis redémarrer VS Code.

## Prérequis

- VS Code avec GitHub Copilot
- Accès au code source du serveur MCP à évaluer
