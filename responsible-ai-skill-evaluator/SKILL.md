---
name: responsible-ai-skill-evaluator
description: Evaluates whether a skill (SKILL.md) complies with Microsoft's 6 Responsible AI principles (Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, Accountability) and with AgentSkills.io format and quality standards. Use when asked to audit, review, verify, certify, or check a skill for responsible AI compliance, or to assess if a skill is ready for public publishing. Triggers on: "evaluate this skill", "audit skill for responsible AI", "check skill compliance", "review SKILL.md", "is this skill RAI compliant", "skill certification", "verify skill quality", "skill ready to publish".
license: MIT
---

# Responsible AI Skill Evaluator

Perform a two-phase audit of a target skill and produce a structured report with scored findings and actionable fixes.

## Preparation

1. **Read the target skill**: Load the full SKILL.md (and all bundled files) of the skill under review.
2. **Load references**: Read both reference files in this skill's `references/` directory:
   - `references/microsoft-rai-checklist.md` — criteria for the 6 Microsoft RAI principles applied to skills
   - `references/agentskills-quality-checklist.md` — AgentSkills.io format and eval quality criteria

## Evaluation Workflow

### Phase 1 — Microsoft Responsible AI (6 Principles)

For each principle, assess the skill against the criteria in `references/microsoft-rai-checklist.md`.
Score each principle: **PASS / PARTIAL / FAIL**
Record specific evidence: quote or cite the exact line in the skill that supports or violates the criterion.

Principles to evaluate:
1. Fairness
2. Reliability & Safety
3. Privacy & Security
4. Inclusiveness
5. Transparency
6. Accountability

### Phase 2 — AgentSkills.io Quality Standards

Evaluate the skill against the criteria in `references/agentskills-quality-checklist.md`.
Score each section: **PASS / PARTIAL / FAIL**

Sections to evaluate:
- Structure & Format
- Frontmatter quality
- Body conciseness (context efficiency)
- Bundled resources appropriateness
- Eval coverage (if evals/evals.json exists)

## Report Format

Produce the final report in this structure:

```markdown
# Skill Audit Report: <skill-name>

**Date**: <today>
**Auditor**: GitHub Copilot (responsible-ai-skill-evaluator)

---

## Phase 1: Microsoft Responsible AI

| Principle | Score | Evidence |
|-----------|-------|----------|
| Fairness | PASS/PARTIAL/FAIL | <quote or line reference> |
| Reliability & Safety | ... | ... |
| Privacy & Security | ... | ... |
| Inclusiveness | ... | ... |
| Transparency | ... | ... |
| Accountability | ... | ... |

**RAI Score**: X/6 principles passing

---

## Phase 2: AgentSkills.io Quality

| Section | Score | Notes |
|---------|-------|-------|
| Structure & Format | PASS/PARTIAL/FAIL | ... |
| Frontmatter quality | ... | ... |
| Body conciseness | ... | ... |
| Bundled resources | ... | ... |
| Eval coverage | ... | ... |

**Quality Score**: X/5 sections passing

---

## Overall Verdict

**READY TO PUBLISH** / **NEEDS FIXES** / **NOT COMPLIANT**

---

## Required Fixes (blockers)

List only FAIL findings that must be resolved before publishing.

## Recommendations (non-blocking)

List PARTIAL findings and improvement suggestions.
```

## Grading Rules

- **PASS**: Fully meets the criterion with clear evidence.
- **PARTIAL**: Partially meets it — issue present but not severe, or criterion is aspirational for the skill type.
- **FAIL**: Clear violation or complete absence of a required element.

**Overall verdict logic**:
- Any FAIL in Phase 1 → **NOT COMPLIANT**
- Any FAIL in Phase 2 → **NEEDS FIXES**
- All PASS or PARTIAL → **READY TO PUBLISH**

## Important Notes

- Apply Microsoft RAI principles to the *instructions the skill gives*, not to an AI system in production. A skill cannot control model training, but it can promote or undermine responsible behavior through the guidance it provides.
- For skills that are purely technical (no demographic targeting, no personal data), mark inapplicable criteria as PASS with note "N/A for this skill type".
- Do not penalize a skill for not having evals if it is a simple, single-purpose skill. Mark eval coverage as PARTIAL rather than FAIL in that case.
