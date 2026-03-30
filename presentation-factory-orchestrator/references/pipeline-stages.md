# Presentation Pipeline — Stage Contracts

This document defines the input/output contracts for each pipeline stage and the error codes the orchestrator should handle.

---

## Stage Contracts

### Stage 1: presentation-storyboard

**Input contract:**
```json
{
  "topic": "string (required)",
  "audience": "string (required)",
  "duration": "integer, minutes (required)",
  "slug": "string, lowercase-hyphenated (required)",
  "key_messages": ["string", "..."] ,
  "style": "corporate | storytelling | educational | pitch",
  "language": "string (ISO 639-1 code, e.g. 'en', 'es')"
}
```

**Output contract:**
- File 1: `/deliverables/<slug>/storyboard.docx` — human-readable document
- File 2: `/deliverables/<slug>/storyboard.json` — machine-readable JSON, direct input to Stage 2
- Success signal: **both files** exist and slide count > 0

> **Stage 1 → Stage 2 handoff**: `storyboard.json` is produced by `presentation-storyboard` as a mandatory co-output of the docx. Stage 2 (`presentation-pptx-builder`) reads `storyboard.json` directly via `--storyboard`. No manual conversion is required when running the full pipeline.

**Expected errors:**
| Code | Reason | Orchestrator action |
|------|--------|---------------------|
| `ERR_DURATION_TOO_SHORT` | Duration < 2 min | Warn user, ask to confirm or extend |
| `ERR_DURATION_TOO_LONG` | Duration > 45 min | Recommend splitting; proceed if confirmed |
| `ERR_NO_KEY_MESSAGES` | key_messages empty | Proceed without, note output may lack focus |

---

### Stage 2: presentation-pptx-builder

**Input contract:**
```json
{
  "slug": "string (required)",
  "storyboard_json": "path to /deliverables/<slug>/storyboard.json (required)",
  "theme": "corporate | minimal | dark | vibrant (default: corporate)",
  "logo_path": "string (optional)"
}
```

**Output contract:**
- File: `/deliverables/<slug>/deck.pptx`
- Success signal: file exists, size > 0, slide count matches storyboard

**Expected errors:**
| Code | Reason | Orchestrator action |
|------|--------|---------------------|
| `ERR_MISSING_PPTX_DEP` | python-pptx not installed | Surface `pip install python-pptx` to user |
| `ERR_STORYBOARD_NOT_FOUND` | storyboard.json missing | Offer to re-run Stage 1 |
| `ERR_INVALID_STORYBOARD` | JSON schema validation failed | Show specific field causing failure |

---

### Stage 3: presentation-speaker-notes

**Input contract:**
```json
{
  "slug": "string (required)",
  "storyboard": "path to /deliverables/<slug>/storyboard.docx or storyboard.json (required)",
  "speaker_style": "conversational | formal | storytelling (default: conversational)",
  "language": "string (ISO 639-1 code)"
}
```

**Output contract:**
- File: `/deliverables/<slug>/speaker-notes.docx`
- Success signal: file exists, section count matches slide count + 1 (Q&A)

**Expected errors:**
| Code | Reason | Orchestrator action |
|------|--------|---------------------|
| `ERR_STORYBOARD_NOT_FOUND` | storyboard missing | Offer to re-run Stage 1 |
| `ERR_TIMING_OVERFLOW` | Total script > duration + 10% | Warn user with ⏱️; offer to trim |

---

### Stage 4: presentation-bundle-manager

**Input contract:**
```json
{
  "slug": "string (required)",
  "deliverables_path": "/deliverables/<slug>/ (default)",
  "project_title": "string (optional)",
  "author": "string (optional)"
}
```

**Output contract:**
- Files: `/deliverables/<slug>/index.xlsx` + `/deliverables/<slug>/manifest.json`
- Success signal: both files exist

**Expected errors:**
| Code | Reason | Orchestrator action |
|------|--------|---------------------|
| `ERR_MISSING_XLSX_DEP` | openpyxl not installed | Surface `pip install openpyxl`; manifest.json still created |
| `ERR_EMPTY_FOLDER` | No files found in slug folder | Abort with clear message; offer to start from Stage 1 |

---

## Slug Sanitization Rules

Apply before any stage is started:

```python
import re

def sanitize_slug(raw: str) -> str:
    s = raw.strip().lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)   # remove special chars
    s = re.sub(r'[\s]+', '-', s)           # spaces to hyphens
    s = re.sub(r'-+', '-', s)              # collapse multiple hyphens
    return s.strip('-')
```

Examples:
- `"Q2 Roadmap 2026"` → `"q2-roadmap-2026"`
- `"Annual Report (Draft)"` → `"annual-report-draft"`
- `"AI & ML Strategy"` → `"ai-ml-strategy"`

---

## Deliverables Folder Bootstrap

Before Stage 1 runs, ensure the folder exists:

```bash
mkdir -p /deliverables/<slug>
```

If the base path `/deliverables/` does not exist (e.g., running locally), substitute with `~/presentations/<slug>/` or the user's preferred path.
