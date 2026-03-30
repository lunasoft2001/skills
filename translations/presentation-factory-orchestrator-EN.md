# Presentation Factory Orchestrator

This document describes the `presentation-factory-orchestrator` skill.

## Description

An end-to-end orchestrator that coordinates the full presentation creation pipeline across four stages: storyboard → PPTX builder → speaker notes → bundle manager. Validates minimum inputs and routes each stage to the appropriate sub-skill, delivering a complete project bundle under `/deliverables/<slug>/`.

## Triggers

`create a presentation`, `make a deck`, `build slides`, `full presentation package`, `end-to-end presentation`

## Pipeline Stages

1. **Stage 1** — `presentation-storyboard`: narrative structure
2. **Stage 2** — `presentation-pptx-builder`: slide deck file
3. **Stage 3** — `presentation-speaker-notes`: presenter script
4. **Stage 4** — `presentation-bundle-manager`: index + manifest

## Required Inputs

- **topic** — the subject of the presentation
- **audience** — who attends and their expertise level
- **duration** — total length in minutes
- **slug** — short identifier for the output folder (e.g., `q2-roadmap-2026`)

## Output

```
/deliverables/<slug>/
  storyboard.docx
  deck.pptx
  speaker-notes.docx
  index.xlsx
  manifest.json
```

## Structure

```
suites/presentation/presentation-factory-orchestrator/
  SKILL.md
  evals/
    evals.json
  references/
    pipeline-stages.md
```

## Installation

Copy the folder to your GitHub Copilot skills directory:

```bash
# macOS / Linux
cp -r presentation-factory-orchestrator ~/.copilot/skills/

# Windows (PowerShell)
Copy-Item -Path "presentation-factory-orchestrator" -Destination "$env:USERPROFILE\.copilot\skills\" -Recurse
```
