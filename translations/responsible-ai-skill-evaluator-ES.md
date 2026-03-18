# Responsible AI Skill Evaluator — Audita Skills según RAI de Microsoft y AgentSkills.io

Este documento describe el skill `responsible-ai-skill-evaluator` de este repositorio.

## Descripción

Skill que evalúa si otro skill (SKILL.md) cumple con los 6 principios de IA Responsable de Microsoft (Equidad, Confiabilidad y Seguridad, Privacidad y Seguridad, Inclusividad, Transparencia, Responsabilidad) y con los estándares de formato y calidad de AgentSkills.io. Genera un informe de auditoría estructurado con hallazgos puntuados y correcciones accionables.

Disparadores: `evalúa este skill`, `audita skill`, `cumple con IA responsable`, `revisa SKILL.md`, `skill listo para publicar`, `certificación de skill`.

## Estructura

```text
responsible-ai-skill-evaluator/
  SKILL.md                                    # Instrucciones + flujo de evaluación
  references/
    microsoft-rai-checklist.md               # 6 principios RAI de Microsoft aplicados a skills
    agentskills-quality-checklist.md         # Criterios de formato y calidad de AgentSkills.io
```

## Funcionalidades

- Evalúa un skill según los 6 principios de IA Responsable de Microsoft
- Evalúa un skill según los estándares de formato y calidad de AgentSkills.io
- Genera un informe de auditoría en Markdown con puntuaciones (PASS / PARTIAL / FAIL)
- Identifica bloqueadores (FAIL) y recomendaciones (PARTIAL)
- Emite un veredicto general: READY TO PUBLISH / NEEDS FIXES / NOT COMPLIANT

## Cómo usarlo

1. Instala el skill (ver abajo)
2. Abre el chat de GitHub Copilot
3. Escribe: `"Evalúa este skill para cumplimiento de IA Responsable:"` y pega o referencia el skill a auditar

## Instalación del skill

```bash
# macOS / Linux
cp -r responsible-ai-skill-evaluator ~/.copilot/skills/responsible-ai-skill-evaluator
```

Luego reinicia VS Code.

## Requisitos

- VS Code con GitHub Copilot
- Un skill (SKILL.md) a evaluar

## Referencias

- [Microsoft: Seis principios de IA Responsable](https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai)
- [AgentSkills.io: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
