---
name: mcp-evaluator
description: Evaluates MCP servers (Model Context Protocol) for security, safety, privacy, and quality. Analyzes source code (TypeScript/Python), mcp.json configuration, tool definitions, and companion SKILL.md. Checks for hardcoded credentials, missing confirmation steps before destructive operations (publish, send, delete), PII handling, token security, error handling, and tool description quality. Produces a structured PASS/PARTIAL/FAIL audit report. Use when: audit MCP, evaluate MCP server, check MCP security, review MCP tools, is my MCP safe, MCP ready to publish, evaluar MCP, auditar servidor MCP, revisar seguridad MCP.
license: MIT
---

# MCP Evaluator

Perform a three-phase audit of an MCP server and produce a structured report with scored findings and actionable fixes.

## Preparation

Collect these artifacts from the MCP being evaluated:

1. **Source code** — `src/` or main implementation files (TypeScript, Python, etc.)
2. **Tool definitions** — where tools are registered (e.g., `src/index.ts`, `server.py`)
3. **Configuration** — `mcp.json` or `.env.example` or equivalent
4. **Package manifest** — `package.json` / `requirements.txt` / `pyproject.toml`
5. **Companion skill** — `~/.copilot/skills/<mcp-name>/SKILL.md` if it exists

Load the two reference checklists:
- `references/mcp-rai-checklist.md`
- `references/mcp-quality-checklist.md`

## Evaluation Workflow

### Phase 1 — Security & Privacy (OWASP / RAI)

Evaluate against `references/mcp-rai-checklist.md`.

Sections:
1. Credential & Secret Handling
2. PII and Data Privacy
3. Destructive Operations Safety
4. Injection & SSRF Risks
5. Authentication & Token Security

Score each section: **PASS / PARTIAL / FAIL**
Quote exact file + line number as evidence where possible.

### Phase 2 — Technical Quality

Evaluate against `references/mcp-quality-checklist.md`.

Sections:
1. Tool Design (descriptions, parameters, types)
2. Error Handling
3. Companion Skill existence
4. Dependencies & Supply Chain
5. Logging & Observability

Score each section: **PASS / PARTIAL / FAIL**

### Phase 3 — Accountability

| Check | Score | Evidence |
|-------|-------|----------|
| License field in package manifest | - | - |
| Source code in public/private repo | - | - |
| Changelog or version tracking | - | - |
| Author / maintainer contact | - | - |

## Report Format

```markdown
# MCP Audit Report: <mcp-name>

**Date**: <today>
**Auditor**: GitHub Copilot (mcp-evaluator)
**Source analyzed**: <files read>

---

## Phase 1: Security & Privacy

| Section | Score | Evidence |
|---------|-------|----------|
| Credential & Secret Handling | PASS/PARTIAL/FAIL | <file:line or description> |
| PII and Data Privacy | ... | ... |
| Destructive Operations Safety | ... | ... |
| Injection & SSRF Risks | ... | ... |
| Authentication & Token Security | ... | ... |

**Security Score**: X/5 passing

---

## Phase 2: Technical Quality

| Section | Score | Evidence |
|---------|-------|----------|
| Tool Design | PASS/PARTIAL/FAIL | ... |
| Error Handling | ... | ... |
| Companion Skill | ... | ... |
| Dependencies & Supply Chain | ... | ... |
| Logging & Observability | ... | ... |

**Quality Score**: X/5 passing

---

## Phase 3: Accountability

| Check | Score | Evidence |
|-------|-------|----------|
| License | PASS/PARTIAL/FAIL | ... |
| Source repo | ... | ... |
| Version tracking | ... | ... |
| Maintainer | ... | ... |

---

## Overall Verdict

**SAFE TO USE** / **NEEDS FIXES** / **SECURITY RISK**

---

## Blockers (must fix before deploying)

<FAIL findings only>

## Recommendations (non-blocking)

<PARTIAL findings and improvement suggestions>
```

## Grading Rules

- **PASS**: Criterion fully met with clear evidence.
- **PARTIAL**: Partially met — issue present but not severe.
- **FAIL**: Clear violation or complete absence of a required security control.

**Overall verdict logic**:
- Any FAIL in Phase 1 → **SECURITY RISK** (stop, fix before any use)
- Any FAIL in Phase 2 → **NEEDS FIXES**
- All PASS or PARTIAL → **SAFE TO USE**

## Notes

- When reading source files, search for: `token`, `key`, `secret`, `password`, `credential`, `apiKey`, `Bearer` to detect potential secret exposure.
- For TypeScript MCPs, the tool registration is typically in `src/index.ts` or `src/tools/`.
- If no companion SKILL.md exists and the MCP performs consequential actions (publishing, sending, deleting), flag as PARTIAL under both Destructive Operations Safety and Companion Skill.
- Do not penalize MCPs that correctly use environment variables (`process.env.TOKEN`) for credentials — that is the correct pattern.
