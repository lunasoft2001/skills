# MCP Evaluator — Audit MCP Servers for Security, Safety & Quality

This document describes the `mcp-evaluator` skill in this repository.

## Description

Skill that audits MCP servers (Model Context Protocol) for security, privacy, and technical quality. Analyzes source code (TypeScript/Python), tool definitions, configuration files, and companion SKILL.md. Produces a structured PASS/PARTIAL/FAIL report with actionable fixes.

Triggers: `audit MCP`, `evaluate MCP server`, `check MCP security`, `review MCP tools`, `is my MCP safe`, `MCP ready to publish`.

## Structure

```text
mcp-evaluator/
  SKILL.md                              # Skill instructions + 3-phase evaluation workflow
  references/
    mcp-rai-checklist.md               # Security & privacy criteria (RAI + OWASP)
    mcp-quality-checklist.md           # Technical quality criteria
```

## Features

- **Phase 1 — Security & Privacy**: credential handling, PII, destructive operations, injection/SSRF, token security
- **Phase 2 — Technical Quality**: tool design, error handling, companion skill, dependencies, logging
- **Phase 3 — Accountability**: license, repo, versioning, maintainer
- Produces structured Markdown report with scored sections (PASS / PARTIAL / FAIL)
- Overall verdict: `SAFE TO USE` / `NEEDS FIXES` / `SECURITY RISK`

## How to use

1. Install the skill (see below)
2. Open GitHub Copilot chat
3. Ask: `"Audit my LinkedIn MCP for security"` — Copilot will read your MCP source files and produce a full report

## Skill installation

```bash
# macOS / Linux
cp -r mcp-evaluator ~/.copilot/skills/mcp-evaluator
```

Then restart VS Code.

## Requirements

- VS Code with GitHub Copilot
- Access to the MCP server source code to evaluate
