# Skills Repository

This public repository stores reusable skills that can be installed and used with GitHub Copilot workflows.

## Skills Catalog

### access-analyzer
- Purpose: Analyze, export, refactor, and re-import Microsoft Access applications (`.accdb`/`.mdb`).
- What it includes: Automation scripts, VBA export references, and supporting assets.
- Typical use cases: Backup before changes, full object export, VBA/query refactoring in VS Code, and controlled re-import.
- Main files:
  - `access-analyzer/SKILL.md`
  - `access-analyzer/scripts/`
  - `access-analyzer/references/`
  - `access-analyzer/assets/`
- Language docs:
  - `access-analyzer-EN.md`
  - `access-analyzer-ES.md`
  - `access-analyzer-PT.md`
  - `access-analyzer-DE.md`
  - `access-analyzer-FR.md`
  - `access-analyzer-IT.md`

### vbaExcel
- Purpose: Extract, refactor, and re-import VBA code for Excel macro-enabled workbooks (`.xlsm`) on Windows.
- What it includes: Python scripts for VBA export/import, VBOM access helper, and install notes.
- Typical use cases: Export VBA modules to `.bas`, edit in VS Code, and safely import changes back into the workbook.
- Main files:
  - `vbaExcel/SKILL.md`
  - `vbaExcel/INSTALL.txt`
  - `vbaExcel/scripts/`
- Language docs:
  - `vbaExcel-EN.md`
  - `vbaExcel-ES.md`
  - `vbaExcel-PT.md`
  - `vbaExcel-DE.md`
  - `vbaExcel-FR.md`
  - `vbaExcel-IT.md`

### m365-email-manager-skill
- Purpose: Manage Microsoft 365 email (Outlook/Exchange Online) through Microsoft Graph with reusable CLI workflows.
- What it includes: Setup/auth scripts, token management, email operation commands, and reference docs.
- Typical use cases: List unread/recent mail, search by text, send/reply messages, mark as read, and move emails across folders.
- Main files:
  - `m365-email-manager-skill/SKILL.md`
  - `m365-email-manager-skill/scripts/`
  - `m365-email-manager-skill/references/`
- Language docs:
  - `m365-email-manager-skill-EN.md`
  - `m365-email-manager-skill-ES.md`
  - `m365-email-manager-skill-PT.md`
  - `m365-email-manager-skill-DE.md`
  - `m365-email-manager-skill-FR.md`
  - `m365-email-manager-skill-IT.md`

### bowling-proshop
- Purpose: Virtual bowling ball driller and lane coach using the Dual Angle layout system (Mo Pinel style).
- What it includes: Interactive 4-phase player consultation, ball recommendation from the active 2026 catalog, visual HTML report with real ball images and SVG diagrams.
- Typical use cases: Ball selection for house/sport/challenge patterns, Dual Angle layout calculation, player profile diagnosis (speed/rev dominance), lane adjustment coaching.
- Main files:
  - `bowling-proshop/SKILL.md`
  - `bowling-proshop/scripts/generate_bowling_report_v2.py`
  - `bowling-proshop/references/current-balls-2026.md`
  - `bowling-proshop/references/dual-angle.md`
- Language docs:
  - `bowling-proshop-EN.md`
  - `bowling-proshop-ES.md`
  - `bowling-proshop-PT.md`
  - `bowling-proshop-DE.md`
  - `bowling-proshop-FR.md`
  - `bowling-proshop-IT.md`

### mcp-evaluator
- Purpose: Audit MCP servers (Model Context Protocol) for security, privacy, and technical quality through a 3-phase evaluation.
- What it includes: Evaluation workflow, RAI+OWASP security checklist for MCPs, and technical quality checklist.
- Typical use cases: Checking if an MCP has hardcoded credentials, verifying destructive tools have confirmation steps, assessing companion SKILL.md coverage, validating error handling and dependency security.
- Main files:
  - `mcp-evaluator/SKILL.md`
  - `mcp-evaluator/references/mcp-rai-checklist.md`
  - `mcp-evaluator/references/mcp-quality-checklist.md`
- Language docs:
  - `mcp-evaluator-EN.md`
  - `mcp-evaluator-ES.md`
  - `mcp-evaluator-PT.md`
  - `mcp-evaluator-DE.md`
  - `mcp-evaluator-FR.md`
  - `mcp-evaluator-IT.md`

### responsible-ai-skill-evaluator
- Purpose: Evaluate whether a skill (SKILL.md) complies with Microsoft's 6 Responsible AI principles and AgentSkills.io format and quality standards.
- What it includes: Evaluation workflow, Microsoft RAI checklist, and AgentSkills.io quality checklist as reference files.
- Typical use cases: Auditing a skill before publishing, checking RAI compliance, getting a structured PASS/PARTIAL/FAIL report with actionable fixes.
- Main files:
  - `responsible-ai-skill-evaluator/SKILL.md`
  - `responsible-ai-skill-evaluator/references/microsoft-rai-checklist.md`
  - `responsible-ai-skill-evaluator/references/agentskills-quality-checklist.md`
- Language docs:
  - `responsible-ai-skill-evaluator-EN.md`
  - `responsible-ai-skill-evaluator-ES.md`
  - `responsible-ai-skill-evaluator-PT.md`
  - `responsible-ai-skill-evaluator-DE.md`
  - `responsible-ai-skill-evaluator-FR.md`
  - `responsible-ai-skill-evaluator-IT.md`

## How New Skills Are Documented

For every new skill added to this repository, this README will include:
- A short English description of the skill.
- Its main purpose and typical use cases.
- Links to the key files/folders.
- Optional links to language-specific docs.

