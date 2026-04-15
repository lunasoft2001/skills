---
name: ChannelToObsidian
description: "Two-phase pipeline to capture an entire YouTube channel into an Obsidian Second Brain. Phase 1 (scan) fetches all video metadata and creates a checklist index in Atlas/Personas/<ChannelName>.md. Phase 2 (process) reads the index, processes only the videos marked with [x], and delegates each one to the VideoToObsidian skill. Zero external dependencies — InnerTube API only. Use when the user asks to capture a YouTube channel, index a channel, process channel videos, ChannelToObsidian, scan YouTube channel."
license: MIT
author: lunasoft2001
  https://github.com/lunasoft2001
---

# ChannelToObsidian

Two-phase pipeline to capture a YouTube channel into an Obsidian Second Brain. Inspired by Zsolt's workflow (batch channel download + NotebookLM) but integrated directly into Obsidian with zero external dependencies and deep Second Brain wikilink structure.

**Depends on:** skill `VideoToObsidian` (must be installed as sibling directory)

---

## When to use this skill

- The user gives a YouTube channel URL and wants to capture its content
- The user says "scan this channel", "index this channel", "ChannelToObsidian"
- The user wants to selectively process videos from a channel into structured notes

---

## Requirements

- **Python 3.9+** — stdlib only, no external dependencies
- Skill **VideoToObsidian** installed at `~/.copilot/skills/VideoToObsidian/`
- `OBSIDIAN_VAULT` environment variable (optional)

---

## Commands

```bash
# Phase 1 — Scan: create video checklist
python3 ~/.copilot/skills/ChannelToObsidian/scripts/channel_to_obsidian.py <channel_URL>

# Phase 2 — Process: generate notes for [x] videos
python3 ~/.copilot/skills/ChannelToObsidian/scripts/channel_to_obsidian.py <channel_URL> --process
```

Accepted channel URL formats:
- `https://www.youtube.com/@channelhandle`
- `https://www.youtube.com/c/channelslug`
- `https://www.youtube.com/channel/UCxxxxxxxx`
- `@channelhandle` (shorthand)

---

## Full workflow

### Phase 1 — Scan

```bash
python3 ~/.copilot/skills/ChannelToObsidian/scripts/channel_to_obsidian.py "https://www.youtube.com/@channelhandle"
```

What happens:
1. Resolves the channel handle → channel name + UC browse ID via InnerTube
2. Paginates through all channel videos (handles channels with hundreds of videos)
3. Creates/updates `Atlas/Personas/<ChannelName>.md` with a checklist of every video:
   - `[ ]` — not yet reviewed
   - `[x]` — selected for processing
   - `[p]` — already processed (note exists in Atlas/Recursos/)
4. Opens the index in Obsidian automatically

**Example output (index file):**
```markdown
## Videos

- [ ] **How to vectorize images automatically** `7GqL6xUvDuM` · 5:42 · 2 years ago
- [ ] **Obsidian as automation workbench** `l0cfhGwaAG8` · 29:29 · 1 year ago
- [p] **Getting started with Excalidraw** `abc123defgh` · 12:15 · 3 years ago
```

### Between phases — User reviews the checklist

The user opens `Atlas/Personas/<ChannelName>.md` in Obsidian and:
- Changes `[ ]` to `[x]` for videos they want to process
- Leaves `[ ]` for videos to skip
- Already-processed videos show `[p]` — leave them unchanged

### Phase 2 — Process

```bash
python3 ~/.copilot/skills/ChannelToObsidian/scripts/channel_to_obsidian.py "https://www.youtube.com/@channelhandle" --process
```

What happens:
1. Reads the index file
2. Finds all videos marked `[x]`
3. For each one: calls **VideoToObsidian** → full note + transcript
4. Marks processed videos `[p]` in the index
5. Opens the index in Obsidian when done

---

## Second Brain structure

```
Atlas/
├── Personas/
│   └── <ChannelName>.md          ← channel index (MOC) ← created by Phase 1
├── Recursos/
│   ├── <VideoTitle>.md           ← technical notes ← created by Phase 2
│   └── Transcripciones/
│       └── VIDEO_ID - Title.md   ← transcripts ← created by Phase 2
```

**Why `Atlas/Personas/`?** A YouTube channel is a person or organization — a source of knowledge, not a resource itself. The index acts as a Map of Content (MOC) for that creator's work.

---

## Conventions

- **Channel index file name**: `<ChannelName>.md` (max 60 chars, no special characters)
- **Video note file name**: same as VideoToObsidian: `<VideoTitle>.md`
- **State markers**: `[ ]` = pending, `[x]` = selected, `[p]` = processed

---

## Notes

- Phase 1 is non-destructive: re-running it updates the video list without losing `[x]` or `[p]` states
- Phase 2 pauses 1 second between videos to avoid hammering the API
- If a video has no subtitles, VideoToObsidian creates the note without transcript section
- The script handles channels with hundreds of videos via InnerTube pagination
- No Google Cloud API key, no OpenAI API key, no yt-dlp needed
