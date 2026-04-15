# TranscribeYoutube

Skill to generate complete Obsidian transcript notes from YouTube videos.

## Purpose

Fetch the full transcript of any YouTube video and save it as an Obsidian-ready `.md` note with YAML frontmatter and clickable timestamps — directly from VS Code, with zero external dependencies.

## Structure

```text
TranscribeYoutube/
  SKILL.md
  scripts/
    transcribe_youtube.py
```

## Main Features

- Uses YouTube InnerTube Player API (iOS client) — no API keys, no yt-dlp
- Zero external dependencies: standard Python 3.9+ only
- Generates YAML frontmatter with video metadata
- Groups transcript lines every 30 seconds (same as YTranscript plugin)
- Clickable timestamps that open the video at the exact second
- Cross-platform: macOS, Windows, Linux
- Opens Obsidian automatically on the created note
- Configurable vault path via `OBSIDIAN_VAULT` environment variable

## Typical Use Cases

- Capture a YouTube tutorial into your Second Brain
- Generate a transcript note and link it from the main resource note
- Archive video content for offline reference
- Create a searchable knowledge base from video courses
