# VideoToObsidian

## Purpose
Complete pipeline to capture a YouTube video into a structured technical note in Obsidian. Combines automatic metadata and transcript download with AI-driven content analysis to produce the right document for the video type.

## Structure
- `VideoToObsidian/SKILL.md` — skill definition and complete step-by-step workflow
- `VideoToObsidian/scripts/video_to_obsidian.py` — script that fetches metadata, delegates transcription to TranscribeYoutube, and emits a JSON payload for Copilot

**Depends on:** skill `TranscribeYoutube` (must be installed in the sibling directory)

## Main Features
- Fetches video metadata via InnerTube API (title, channel, description, duration)
- Delegates transcription to the `TranscribeYoutube` skill
- Detects content type: TUTORIAL / CONCEPT / DEMO / TALK
- Applies the matching note template (steps checklist, key points, quotes…)
- Generates a complete Obsidian note with embedded video, summary, wikilink to transcript
- Opens the note in Obsidian automatically (macOS / Windows / Linux)
- Configurable vault path via `OBSIDIAN_VAULT` environment variable

## Typical Use Cases
- Capturing a YouTube tutorial as a step-by-step reference note
- Turning a concept video into a structured knowledge base entry
- Documenting a software demo or tool showcase
- Archiving a talk or interview with key ideas highlighted
