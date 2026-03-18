# Responsible AI Skill Evaluator — Évaluation des skills selon la RAI de Microsoft et AgentSkills.io

Ce document décrit le skill `responsible-ai-skill-evaluator` de ce dépôt.

## Description

Skill qui évalue si un autre skill (SKILL.md) respecte les 6 principes d'IA Responsable de Microsoft (Équité, Fiabilité & Sécurité, Confidentialité & Sécurité, Inclusivité, Transparence, Responsabilité) ainsi que les standards de format et de qualité d'AgentSkills.io. Génère un rapport d'audit structuré avec des résultats notés et des corrections actionnables.

Déclencheurs : `évaluer ce skill`, `auditer skill`, `conformité IA responsable`, `réviser SKILL.md`, `skill prêt à publier`, `certification skill`.

## Structure

```text
responsible-ai-skill-evaluator/
  SKILL.md                                    # Instructions + flux d'évaluation
  references/
    microsoft-rai-checklist.md               # 6 principes RAI de Microsoft appliqués aux skills
    agentskills-quality-checklist.md         # Critères de format et de qualité d'AgentSkills.io
```

## Fonctionnalités

- Évalue un skill selon les 6 principes d'IA Responsable de Microsoft
- Évalue un skill selon les standards de format et de qualité d'AgentSkills.io
- Génère un rapport d'audit Markdown avec des scores (PASS / PARTIAL / FAIL)
- Identifie les bloqueurs (FAIL) et les recommandations (PARTIAL)
- Émet un verdict global : READY TO PUBLISH / NEEDS FIXES / NOT COMPLIANT

## Utilisation

1. Installer le skill (voir ci-dessous)
2. Ouvrir le chat GitHub Copilot
3. Saisir : `"Évalue ce skill pour la conformité IA Responsable :"` et coller ou référencer le skill à auditer

## Installation du skill

```bash
# macOS / Linux
cp -r responsible-ai-skill-evaluator ~/.copilot/skills/responsible-ai-skill-evaluator
```

Puis redémarrer VS Code.

## Prérequis

- VS Code avec GitHub Copilot
- Un skill (SKILL.md) à évaluer

## Références

- [Microsoft : Six principes d'IA Responsable](https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai)
- [AgentSkills.io : Évaluation de la qualité de sortie des skills](https://agentskills.io/skill-creation/evaluating-skills)
