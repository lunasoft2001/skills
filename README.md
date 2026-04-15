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
├── obsidian-markdown/
├── m365-email-manager-skill/
├── mcp-evaluator/
├── mssql-second-brain/
├── suites/office-vba/office-vba-orchestrator/    ← NEW: routes Office VBA tasks; enforces backup policy
├── suites/presentation/presentation-bundle-manager/
├── suites/presentation/presentation-factory-orchestrator/
├── suites/presentation/presentation-pptx-builder/
├── suites/presentation/presentation-speaker-notes/
├── suites/presentation/presentation-storyboard/
├── responsible-ai-skill-evaluator/
├── suites/office-vba/vba-access/                 ← NEW: VBA modules for Access .accdb
├── suites/office-vba/vba-powerpoint/             ← NEW: VBA modules for PowerPoint .pptm
├── suites/office-vba/vba-word/                   ← NEW: VBA modules for Word .docm
├── suites/office-vba/vbaExcel/
├── TranscribeYoutube/
├── VideoToObsidian/
├── ChannelToObsidian/
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
  - `suites/office-vba/vbaExcel/SKILL.md`
  - `suites/office-vba/vbaExcel/INSTALL.txt`
  - `suites/office-vba/vbaExcel/scripts/`
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

### mssql-second-brain
- Purpose: Generate an Obsidian Second Brain vault from SQL Server metadata with zero AI tokens during extraction.
- What it includes: A reusable SKILL.md and Python generator script for schemas, tables, columns, foreign keys, and backlinks.
- Typical use cases: SQL Server database mapping, onboarding documentation, and searchable architecture knowledge bases.
- Main files:
  - `mssql-second-brain/SKILL.md`
  - `mssql-second-brain/scripts/generate_second_brain.py`
- Language docs:
  - `translations/mssql-second-brain-DE.md`
  - `translations/mssql-second-brain-EN.md`
  - `translations/mssql-second-brain-ES.md`
  - `translations/mssql-second-brain-FR.md`
  - `translations/mssql-second-brain-IT.md`
  - `translations/mssql-second-brain-PT.md`

### obsidian-markdown
- Purpose: Build, normalize, and repair Obsidian-ready Markdown with strict YAML frontmatter, checkboxes, callouts, and wikilinks.
- What it includes: Formatting rules, repair workflow, validation checklist, linking rules, and ready-to-use templates for PRD/handoff/meeting notes.
- Typical use cases: Fixing broken Properties blocks, converting generic Markdown to Obsidian style, standardizing recurring operational notes.
- Main files:
  - `obsidian-markdown/SKILL.md`
  - `obsidian-markdown/references/frontmatter-schema.md`
  - `obsidian-markdown/references/obsidian-validation-checklist.md`
  - `obsidian-markdown/references/templates-prd-handoff-meeting.md`
- Language docs:
  - `translations/obsidian-markdown-EN.md`
  - `translations/obsidian-markdown-ES.md`
  - `translations/obsidian-markdown-PT.md`
  - `translations/obsidian-markdown-DE.md`
  - `translations/obsidian-markdown-FR.md`
  - `translations/obsidian-markdown-IT.md`

### TranscribeYoutube
- Purpose: Generate complete Obsidian transcript notes from any YouTube video using the InnerTube Player API (iOS client) with zero external dependencies.
- What it includes: Python script (stdlib only), 30-second block grouping with clickable timestamps, cross-platform Obsidian opener, configurable vault path via `OBSIDIAN_VAULT` environment variable.
- Typical use cases: Capturing YouTube tutorials into a Second Brain vault, generating searchable transcript notes with timestamps, archiving video content offline, saving course transcriptions directly to Obsidian.
- Main files:
  - `TranscribeYoutube/SKILL.md`
  - `TranscribeYoutube/scripts/transcribe_youtube.py`
- Language docs:
  - `translations/TranscribeYoutube-EN.md`
  - `translations/TranscribeYoutube-ES.md`
  - `translations/TranscribeYoutube-PT.md`
  - `translations/TranscribeYoutube-DE.md`
  - `translations/TranscribeYoutube-FR.md`
  - `translations/TranscribeYoutube-IT.md`

### VideoToObsidian
- Purpose: Complete pipeline to capture a YouTube video into a structured Obsidian technical note — metadata, transcript, AI-generated content and embedded video in one step.
- What it includes: Python script (stdlib only), automatic content-type detection (tutorial/concept/demo/talk), 4 note templates, cross-platform Obsidian opener.
- Depends on: `TranscribeYoutube` skill (sibling directory).
- Typical use cases: Turning a YouTube tutorial into a step-by-step reference, capturing concept videos into the Second Brain, documenting software demos, archiving talks with key ideas.
- Main files:
  - `VideoToObsidian/SKILL.md`
  - `VideoToObsidian/scripts/video_to_obsidian.py`
- Language docs:
  - `translations/VideoToObsidian-EN.md`
  - `translations/VideoToObsidian-ES.md`
  - `translations/VideoToObsidian-PT.md`
  - `translations/VideoToObsidian-DE.md`
  - `translations/VideoToObsidian-FR.md`
  - `translations/VideoToObsidian-IT.md`

### ChannelToObsidian
- Purpose: Two-phase skill to capture an entire YouTube channel into an Obsidian Second Brain vault. Phase 1 scans all videos into a selectable checklist; Phase 2 processes only the ones you mark with `[x]` using the full VideoToObsidian pipeline.
- What it includes: Python script (stdlib only), InnerTube browse API with pagination, channel index as MOC in `Atlas/Personas/`, state markers `[ ]` / `[x]` / `[p]`, cross-platform Obsidian opener.
- Depends on: `VideoToObsidian` skill (sibling directory).
- Typical use cases: Building a knowledge base from a favourite channel, reviewing all videos before deciding which to study, batch-processing a channel or playlist with selective curation.
- Main files:
  - `ChannelToObsidian/SKILL.md`
  - `ChannelToObsidian/scripts/channel_to_obsidian.py`
- Language docs:
  - `translations/ChannelToObsidian-EN.md`
  - `translations/ChannelToObsidian-ES.md`
  - `translations/ChannelToObsidian-PT.md`
  - `translations/ChannelToObsidian-DE.md`
  - `translations/ChannelToObsidian-FR.md`
  - `translations/ChannelToObsidian-IT.md`

---

## Presentation Suite

A set of five coordinated skills for creating complete professional presentations end-to-end.

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

### presentation-factory-orchestrator
- Purpose: End-to-end orchestrator for creating professional presentations. Routes the full pipeline across four stages — storyboard → pptx-builder → speaker-notes → bundle-manager — and validates minimum inputs before starting.
- What it includes: Pipeline stage contracts, slug sanitization logic, progress reporting format, and stage failure recovery.
- Typical use cases: Creating a complete presentation package from scratch, routing partial pipelines to individual sub-skills, tracking progress across all four stages.
- Main files:
  - `suites/presentation/presentation-factory-orchestrator/SKILL.md`
  - `suites/presentation/presentation-factory-orchestrator/references/pipeline-stages.md`
  - `suites/presentation/presentation-factory-orchestrator/evals/evals.json`
- Language docs:
  - `translations/presentation-factory-orchestrator-EN.md`
  - `translations/presentation-factory-orchestrator-ES.md`
  - `translations/presentation-factory-orchestrator-PT.md`
  - `translations/presentation-factory-orchestrator-DE.md`
  - `translations/presentation-factory-orchestrator-FR.md`
  - `translations/presentation-factory-orchestrator-IT.md`

### presentation-storyboard
- Purpose: Structure the narrative arc of a presentation slide by slide, producing message, objective, duration, and visual suggestion per slide.
- What it includes: 3-act narrative framework, slide budget calculator, visual suggestion catalog, transition phrase patterns, and four narrative models (business, pitch, educational, executive summary).
- Typical use cases: Planning a presentation before building the deck, defining the story arc and key messages, generating a storyboard document for stakeholder review.
- Main files:
  - `suites/presentation/presentation-storyboard/SKILL.md`
  - `suites/presentation/presentation-storyboard/references/slide-structure-guide.md`
  - `suites/presentation/presentation-storyboard/evals/evals.json`
- Language docs:
  - `translations/presentation-storyboard-EN.md`
  - `translations/presentation-storyboard-ES.md`
  - `translations/presentation-storyboard-PT.md`
  - `translations/presentation-storyboard-DE.md`
  - `translations/presentation-storyboard-FR.md`
  - `translations/presentation-storyboard-IT.md`

### presentation-pptx-builder
- Purpose: Generate a `.pptx` presentation file consistent with a storyboard, using python-pptx with four visual themes and labeled placeholders for charts.
- What it includes: Python builder script, four themes (corporate, minimal, dark, vibrant), storyboard JSON contract, visual placeholder logic, and layout reference.
- Typical use cases: Converting a storyboard into an actual PowerPoint file, applying consistent branding across all slides, generating a deck programmatically.
- Main files:
  - `suites/presentation/presentation-pptx-builder/SKILL.md`
  - `suites/presentation/presentation-pptx-builder/scripts/build_pptx.py`
  - `suites/presentation/presentation-pptx-builder/references/pptx-design-guide.md`
  - `suites/presentation/presentation-pptx-builder/evals/evals.json`
- Language docs:
  - `translations/presentation-pptx-builder-EN.md`
  - `translations/presentation-pptx-builder-ES.md`
  - `translations/presentation-pptx-builder-PT.md`
  - `translations/presentation-pptx-builder-DE.md`
  - `translations/presentation-pptx-builder-FR.md`
  - `translations/presentation-pptx-builder-IT.md`

### presentation-speaker-notes
- Purpose: Generate a per-slide speaker script with timing cues, transition phrases, and a Q&A section with probable audience questions and suggested answers.
- What it includes: Three speaking styles (conversational, formal, storytelling), timing enforcement, diplomatic Q&A framing, pre-presentation checklist, and closing statement template.
- Typical use cases: Preparing a presenter guide for a conference talk, writing rehearsal notes with timing, generating Q&A preparation for a board presentation.
- Main files:
  - `suites/presentation/presentation-speaker-notes/SKILL.md`
  - `suites/presentation/presentation-speaker-notes/references/notes-format-guide.md`
  - `suites/presentation/presentation-speaker-notes/evals/evals.json`
- Language docs:
  - `translations/presentation-speaker-notes-EN.md`
  - `translations/presentation-speaker-notes-ES.md`
  - `translations/presentation-speaker-notes-PT.md`
  - `translations/presentation-speaker-notes-DE.md`
  - `translations/presentation-speaker-notes-FR.md`
  - `translations/presentation-speaker-notes-IT.md`

### presentation-bundle-manager
- Purpose: Package all presentation deliverables into a `/deliverables/<slug>/` folder, generate an `index.xlsx` inventory and a `manifest.json` with SHA256 checksums and validation status.
- What it includes: Python bundle script, two-sheet Excel index (Summary + Files), JSON manifest schema, SHA256 checksum generation, and partial bundle handling.
- Typical use cases: Finalizing a presentation project and archiving all files, generating a delivery checklist, creating a manifest for stakeholder handoff.
- Main files:
  - `suites/presentation/presentation-bundle-manager/SKILL.md`
  - `suites/presentation/presentation-bundle-manager/scripts/bundle_manager.py`
  - `suites/presentation/presentation-bundle-manager/evals/evals.json`
- Language docs:
  - `translations/presentation-bundle-manager-EN.md`
  - `translations/presentation-bundle-manager-ES.md`
  - `translations/presentation-bundle-manager-PT.md`
  - `translations/presentation-bundle-manager-DE.md`
  - `translations/presentation-bundle-manager-FR.md`
  - `translations/presentation-bundle-manager-IT.md`

---

## Presentation Suite — Standard Output Structure

All five presentation skills share a common output folder convention:

```
/deliverables/<slug>/
  storyboard.docx       ← presentation-storyboard
  deck.pptx             ← presentation-pptx-builder
  speaker-notes.docx    ← presentation-speaker-notes
  index.xlsx            ← presentation-bundle-manager
  manifest.json         ← presentation-bundle-manager
```

The `presentation-factory-orchestrator` skill coordinates all four sub-skills end-to-end and delivers the complete bundle in one command.

---

## How New Skills Are Documented

---

## Office VBA Suite

A coordinated suite of four skills for extracting, refactoring, and re-importing VBA code across Office applications. All skills share a mandatory **backup-before-import** safety rule.

### office-vba-orchestrator *(new)*
- Purpose: Route Office VBA tasks to the correct per-application skill and enforce the backup policy for the entire suite. Excludes Outlook.
- What it includes: Routing table, file type detection logic, universal backup policy with rollback procedures.
- Typical use cases: Identifying which skill to use for an Office file, enforcing backup before any import, handling multi-application sessions.
- Main files:
  - `suites/office-vba/office-vba-orchestrator/SKILL.md`
  - `suites/office-vba/office-vba-orchestrator/references/routing-guide.md`
  - `suites/office-vba/office-vba-orchestrator/references/backup-policy.md`
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
  - `suites/office-vba/vba-word/SKILL.md`
  - `suites/office-vba/vba-word/scripts/export_vba_word.py`
  - `suites/office-vba/vba-word/scripts/import_vba_word.py`
  - `suites/office-vba/vba-word/references/word-vba-patterns.md`
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
  - `suites/office-vba/vba-powerpoint/SKILL.md`
  - `suites/office-vba/vba-powerpoint/scripts/export_vba_ppt.py`
  - `suites/office-vba/vba-powerpoint/scripts/import_vba_ppt.py`
  - `suites/office-vba/vba-powerpoint/references/ppt-vba-patterns.md`
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
  - `suites/office-vba/vba-access/SKILL.md`
  - `suites/office-vba/vba-access/scripts/export_vba_access.py`
  - `suites/office-vba/vba-access/scripts/import_vba_access.py`
  - `suites/office-vba/vba-access/references/access-vba-patterns.md`
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

