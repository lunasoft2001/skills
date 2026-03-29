# Skills Repository

This public repository stores reusable skills that can be installed and used with GitHub Copilot workflows.

## Repository Structure

```
skills/
├── README.md                   ← you are here
├── translations/               ← skill descriptions in DE, EN, ES, FR, IT, PT
│   ├── access-analyzer-EN.md
│   ├── access-analyzer-ES.md
│   └── ...
├── access-analyzer/            ← skill folder (SKILL.md + scripts + references)
├── bowling-proshop/
├── m365-email-manager-skill/
├── mcp-evaluator/
├── office-vba-orchestrator/    ← NEW: routes Office VBA tasks; enforces backup policy
├── responsible-ai-skill-evaluator/
├── vba-access/                 ← NEW: VBA modules for Access .accdb
├── vba-powerpoint/             ← NEW: VBA modules for PowerPoint .pptm
├── vba-word/                   ← NEW: VBA modules for Word .docm
├── vbaExcel/
└── whatsapp-mcp/
```

Each skill folder contains its own `SKILL.md` (the file GitHub Copilot reads) plus optional `scripts/`, `references/`, and `assets/` subfolders.  
The `translations/` folder contains human-readable descriptions of each skill in multiple languages — useful for non-technical users who want to understand what a skill does before installing it.

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
  - `translations/access-analyzer-EN.md`
  - `translations/access-analyzer-ES.md`
  - `translations/access-analyzer-PT.md`
  - `translations/access-analyzer-DE.md`
  - `translations/access-analyzer-FR.md`
  - `translations/access-analyzer-IT.md`

### vbaExcel
- Purpose: Extract, refactor, and re-import VBA code for Excel macro-enabled workbooks (`.xlsm`) on Windows.
- What it includes: Python scripts for VBA export/import, VBOM access helper, and install notes.
- Typical use cases: Export VBA modules to `.bas`, edit in VS Code, and safely import changes back into the workbook.
- Main files:
  - `vbaExcel/SKILL.md`
  - `vbaExcel/INSTALL.txt`
  - `vbaExcel/scripts/`
- Language docs:
  - `translations/vbaExcel-EN.md`
  - `translations/vbaExcel-ES.md`
  - `translations/vbaExcel-PT.md`
  - `translations/vbaExcel-DE.md`
  - `translations/vbaExcel-FR.md`
  - `translations/vbaExcel-IT.md`

### m365-email-manager-skill
- Purpose: Manage Microsoft 365 email (Outlook/Exchange Online) through Microsoft Graph with reusable CLI workflows.
- What it includes: Setup/auth scripts, token management, email operation commands, and reference docs.
- Typical use cases: List unread/recent mail, search by text, send/reply messages, mark as read, and move emails across folders.
- Main files:
  - `m365-email-manager-skill/SKILL.md`
  - `m365-email-manager-skill/scripts/`
  - `m365-email-manager-skill/references/`
- Language docs:
  - `translations/m365-email-manager-skill-EN.md`
  - `translations/m365-email-manager-skill-ES.md`
  - `translations/m365-email-manager-skill-PT.md`
  - `translations/m365-email-manager-skill-DE.md`
  - `translations/m365-email-manager-skill-FR.md`
  - `translations/m365-email-manager-skill-IT.md`

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
  - `translations/bowling-proshop-EN.md`
  - `translations/bowling-proshop-ES.md`
  - `translations/bowling-proshop-PT.md`
  - `translations/bowling-proshop-DE.md`
  - `translations/bowling-proshop-FR.md`
  - `translations/bowling-proshop-IT.md`

### mcp-evaluator
- Purpose: Audit MCP servers (Model Context Protocol) for security, privacy, and technical quality through a 3-phase evaluation.
- What it includes: Evaluation workflow, RAI+OWASP security checklist for MCPs, and technical quality checklist.
- Typical use cases: Checking if an MCP has hardcoded credentials, verifying destructive tools have confirmation steps, assessing companion SKILL.md coverage, validating error handling and dependency security.
- Main files:
  - `mcp-evaluator/SKILL.md`
  - `mcp-evaluator/references/mcp-rai-checklist.md`
  - `mcp-evaluator/references/mcp-quality-checklist.md`
- Language docs:
  - `translations/mcp-evaluator-EN.md`
  - `translations/mcp-evaluator-ES.md`
  - `translations/mcp-evaluator-PT.md`
  - `translations/mcp-evaluator-DE.md`
  - `translations/mcp-evaluator-FR.md`
  - `translations/mcp-evaluator-IT.md`

### responsible-ai-skill-evaluator
- Purpose: Evaluate whether a skill (SKILL.md) complies with Microsoft's 6 Responsible AI principles and AgentSkills.io format and quality standards.
- What it includes: Evaluation workflow, Microsoft RAI checklist, and AgentSkills.io quality checklist as reference files.
- Typical use cases: Auditing a skill before publishing, checking RAI compliance, getting a structured PASS/PARTIAL/FAIL report with actionable fixes.
- Main files:
  - `responsible-ai-skill-evaluator/SKILL.md`
  - `responsible-ai-skill-evaluator/references/microsoft-rai-checklist.md`
  - `responsible-ai-skill-evaluator/references/agentskills-quality-checklist.md`
- Language docs:
  - `translations/responsible-ai-skill-evaluator-EN.md`
  - `translations/responsible-ai-skill-evaluator-ES.md`
  - `translations/responsible-ai-skill-evaluator-PT.md`
  - `translations/responsible-ai-skill-evaluator-DE.md`
  - `translations/responsible-ai-skill-evaluator-FR.md`
  - `translations/responsible-ai-skill-evaluator-IT.md`

## How New Skills Are Documented

---

## Office VBA Suite

A coordinated suite of four skills for extracting, refactoring, and re-importing VBA code across Office applications. All skills share a mandatory **backup-before-import** safety rule.

### office-vba-orchestrator *(new)*
- Purpose: Route Office VBA tasks to the correct per-application skill and enforce the backup policy for the entire suite. Excludes Outlook.
- What it includes: Routing table, file type detection logic, universal backup policy with rollback procedures.
- Typical use cases: Identifying which skill to use for an Office file, enforcing backup before any import, handling multi-application sessions.
- Main files:
  - `office-vba-orchestrator/SKILL.md`
  - `office-vba-orchestrator/references/routing-guide.md`
  - `office-vba-orchestrator/references/backup-policy.md`
- Language docs:
  - `translations/office-vba-orchestrator-EN.md`
  - `translations/office-vba-orchestrator-ES.md`
  - `translations/office-vba-orchestrator-PT.md`
  - `translations/office-vba-orchestrator-DE.md`
  - `translations/office-vba-orchestrator-FR.md`
  - `translations/office-vba-orchestrator-IT.md`

### vba-word *(new)*
- Purpose: Extract, refactor, and re-import VBA code from Word macro-enabled documents (`.docm` / `.dotm`) on Windows.
- What it includes: Python export/import scripts via COM, VBA component reference, Word event patterns.
- Typical use cases: Exporting Word VBA modules to `.bas` files, editing macros in VS Code, importing refactored code back safely.
- Main files:
  - `vba-word/SKILL.md`
  - `vba-word/scripts/export_vba_word.py`
  - `vba-word/scripts/import_vba_word.py`
  - `vba-word/references/word-vba-patterns.md`
- Language docs:
  - `translations/vba-word-EN.md`
  - `translations/vba-word-ES.md`
  - `translations/vba-word-PT.md`
  - `translations/vba-word-DE.md`
  - `translations/vba-word-FR.md`
  - `translations/vba-word-IT.md`

### vba-powerpoint *(new)*
- Purpose: Extract, refactor, and re-import VBA code from PowerPoint macro-enabled presentations (`.pptm` / `.potm`) on Windows.
- What it includes: Python export/import scripts via COM, VBA component reference, PowerPoint event patterns.
- Typical use cases: Exporting PowerPoint VBA modules to `.bas` files, editing presentation macros in VS Code, importing refactored code back safely.
- Main files:
  - `vba-powerpoint/SKILL.md`
  - `vba-powerpoint/scripts/export_vba_ppt.py`
  - `vba-powerpoint/scripts/import_vba_ppt.py`
  - `vba-powerpoint/references/ppt-vba-patterns.md`
- Language docs:
  - `translations/vba-powerpoint-EN.md`
  - `translations/vba-powerpoint-ES.md`
  - `translations/vba-powerpoint-PT.md`
  - `translations/vba-powerpoint-DE.md`
  - `translations/vba-powerpoint-FR.md`
  - `translations/vba-powerpoint-IT.md`

### vba-access *(new)*
- Purpose: Extract, refactor, and re-import VBA modules (standard and class modules) from Access databases (`.accdb` / `.mdb`) on Windows. For full database analysis, use `access-analyzer`.
- What it includes: Python export/import scripts via COM, DAO/ADO patterns, Access VBA component reference.
- Typical use cases: Exporting Access VBA modules to `.bas` files, editing modules in VS Code, importing refactored code back safely.
- Main files:
  - `vba-access/SKILL.md`
  - `vba-access/scripts/export_vba_access.py`
  - `vba-access/scripts/import_vba_access.py`
  - `vba-access/references/access-vba-patterns.md`
- Language docs:
  - `translations/vba-access-EN.md`
  - `translations/vba-access-ES.md`
  - `translations/vba-access-PT.md`
  - `translations/vba-access-DE.md`
  - `translations/vba-access-FR.md`
  - `translations/vba-access-IT.md`

For every new skill added to this repository, this README will include:
- A short English description of the skill.
- Its main purpose and typical use cases.
- Links to the key files/folders.
- Optional links to language-specific docs.

