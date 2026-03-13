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

## How New Skills Are Documented

For every new skill added to this repository, this README will include:
- A short English description of the skill.
- Its main purpose and typical use cases.
- Links to the key files/folders.
- Optional links to language-specific docs.

