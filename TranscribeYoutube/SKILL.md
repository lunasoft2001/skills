---
name: TranscribeYoutube
description: Generates a complete Obsidian-ready .md transcript note from any YouTube URL using the YouTube InnerTube Player API (iOS client) with zero external dependencies — only Python 3.9+ standard library. Saves the note to Atlas/Recursos/Transcripciones/VIDEO_ID - Title.md with YAML frontmatter, clickable timestamps, and a wikilink ready to embed in the main resource note. Use when the user asks to transcribe a video, generate a YouTube transcript, capture video content, create a transcript note, or mentions TranscribeYoutube, transcript YouTube, or extract subtitles.
license: MIT
author: lunasoft2001
https://github.com/lunasoft2001
---

# TranscribeYoutube

Fetches the complete transcript of any YouTube video and generates an Obsidian-ready `.md` note — directly from VS Code, with zero external dependencies.

Uses the **InnerTube Player API** (iOS client), the same API used internally by the [obsidian-yt-transcript](https://github.com/lstrzepek/obsidian-yt-transcript) plugin. No `yt-dlp`, no API keys, no installs beyond Python 3.9+.

## When to Use This Skill

- User asks to transcribe a YouTube video
- User wants to capture video content into their Second Brain / Obsidian vault
- User mentions a YouTube URL and wants a transcript note generated
- Trigger phrases: `TranscribeYoutube`, `transcript`, `YouTube transcript`, `capture video`, `extraer subtítulos`, `transcribir vídeo`

## Requirements

- **Python 3.9+** — standard library only, no pip installs needed
- Internet connection
- The video must have subtitles available (automatic or manual) on YouTube
- Obsidian installed with the vault name configured (see Configuration below)

## Configuration

Set the `OBSIDIAN_VAULT` environment variable to your vault's absolute path:

```bash
# macOS/Linux
export OBSIDIAN_VAULT="/path/to/your/Obsidian/VaultName"

# Windows (PowerShell)
$env:OBSIDIAN_VAULT = "C:\Users\you\Documents\Obsidian\VaultName"
```

Also set `OBSIDIAN_VAULT_NAME` if your vault name differs from the folder name:

```bash
export OBSIDIAN_VAULT_NAME="MyVault"
```

If not set, the script uses the defaults defined at the top of `transcribe_youtube.py`.

## Command

```bash
python3 TranscribeYoutube/scripts/transcribe_youtube.py <YOUTUBE_URL>
```

Optional language preference (default: tries `es` then `en`):

```bash
python3 TranscribeYoutube/scripts/transcribe_youtube.py <URL> --lang en
```

## Full Workflow

1. **Run the script** with the YouTube URL
2. The script fetches metadata + transcript via InnerTube API and writes the `.md` file
3. Obsidian opens automatically on the new note
4. **Copy the wikilink** printed in the terminal into the main resource note under the video iframe:
   ```
   Transcript: [[Transcripciones/VIDEO_ID - Title]]
   ```
5. Optionally, ask Copilot to generate a **summary** from the transcript and add it to the resource note

## Output Format

File saved at:
```
<VAULT>/Atlas/Recursos/Transcripciones/VIDEO_ID - Title.md
```

Structure:
```markdown
---
tags: [transcripcion, recurso]
video-id: <ID>
url: https://www.youtube.com/watch?v=<ID>
canal: "<Channel>"
titulo: "<Title>"
idioma: es
fecha-guardado: YYYY-MM-DD
---

# Title
**Canal:** ...
**URL:** ...

← Main note: `[[...]]`  *(update this wikilink)*

---

## Transcripción

[00:00](https://...&t=0) First grouped text block...
[00:30](https://...&t=30) Next block...
```

Lines are grouped every 30 seconds (same grouping as the YTranscript plugin). Timestamps are clickable and open the video at that exact second.

## File Naming Convention

```
VIDEO_ID - Title (max 60 chars).md
```

Examples:
- `7GqL6xUvDuM - Imagen a VECTOR AUTOMÁTICAMENTE Affinity 3.0.md`
- `dQw4w9WgXcQ - Never Gonna Give You Up.md`

## Cross-Platform Support

| OS | Open command |
|---|---|
| macOS | `open obsidian://...` |
| Windows | `cmd /c start obsidian://...` |
| Linux | `xdg-open obsidian://...` |

## Notes

- No external dependencies — pure Python 3.9+ standard library
- Uses the same InnerTube API (iOS client) as the YTranscript Obsidian plugin
- If a video has no subtitles, the script exits with a clear error message
- If the note already exists, it is overwritten (useful to refresh transcripts)
- The `← Main note:` line must be updated manually after creating the resource note

## Reference Files

- `scripts/transcribe_youtube.py` — main script
