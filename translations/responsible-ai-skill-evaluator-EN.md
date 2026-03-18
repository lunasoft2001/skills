# Responsible AI Skill Evaluator — Audit Skills for Microsoft RAI & AgentSkills.io Compliance

This document describes the `responsible-ai-skill-evaluator` skill in this repository.

## Description

Skill that evaluates whether another skill (SKILL.md) complies with Microsoft's 6 Responsible AI principles (Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, Accountability) and with AgentSkills.io format and quality standards. Produces a structured audit report with scored findings and actionable fixes.

Triggers: `evaluate this skill`, `audit skill`, `responsible AI compliance`, `review SKILL.md`, `skill ready to publish`, `skill certification`.

## Structure

```text
responsible-ai-skill-evaluator/
  SKILL.md                                    # Skill instructions + evaluation workflow
  references/
    microsoft-rai-checklist.md               # 6 Microsoft RAI principles applied to skills
    agentskills-quality-checklist.md         # AgentSkills.io format & eval quality criteria
```

## Features

- Evaluates a skill against Microsoft's 6 Responsible AI principles
- Evaluates a skill against AgentSkills.io format and quality standards
- Produces a structured Markdown audit report with scored findings (PASS / PARTIAL / FAIL)
- Identifies blockers (FAIL) and recommendations (PARTIAL)
- Provides an overall verdict: READY TO PUBLISH / NEEDS FIXES / NOT COMPLIANT

## How to use

1. Install the skill (see below)
2. Open GitHub Copilot chat
3. Ask: `"Evaluate this skill for Responsible AI compliance:"` and paste or reference the skill to audit

## Skill installation

```bash
# macOS / Linux
cp -r responsible-ai-skill-evaluator ~/.copilot/skills/responsible-ai-skill-evaluator
```

Then restart VS Code.

## Requirements

- VS Code with GitHub Copilot
- A skill (SKILL.md) to evaluate

## References

- [Microsoft: Six principles of Responsible AI](https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai)
- [AgentSkills.io: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
