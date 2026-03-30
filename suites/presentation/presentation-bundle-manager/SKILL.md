---
name: presentation-bundle-manager
description: Packages all presentation deliverables into a structured project folder, generates an index.xlsx inventory file, and writes a manifest.json with metadata. Use when the user wants to bundle presentation files, create a delivery package, produce a file index, generate a project manifest, or archive a completed presentation project. Triggers on: "bundle the presentation", "package the deliverables", "create the manifest", "generate the index", "finalize the presentation package", "empaqueta la presentación", "crea el índice de archivos", "genera el manifest", "arma el paquete final".
license: MIT
author: lunasoft2001 <https://github.com/lunasoft2001>
---

# Presentation Bundle Manager

Collect all deliverables from `/deliverables/<slug>/`, generate `index.xlsx` and `manifest.json`, and confirm the bundle is complete.

## Required Inputs

| Field | Source | Description |
|-------|--------|-------------|
| `slug` | User / orchestrator | Project folder identifier |
| `deliverables_path` | Optional | Override base path (default: `/deliverables/<slug>/`) |
| `project_title` | Optional | Human-readable project name for the index |
| `author` | Optional | Creator name for manifest metadata |

## Bundle Workflow

1. **Scan the deliverables folder**: list all files in `/deliverables/<slug>/`.
2. **Validate expected files**: check that the five core files are present:
   - `storyboard.docx`
   - `storyboard.json`
   - `deck.pptx`
   - `speaker-notes.docx`
   - *(index.xlsx and manifest.json will be created in this step)*
3. **Report missing files**: list any core files that are absent and offer to generate them via their respective sub-skills.
4. **Run the bundle script**:

```bash
python3 suites/presentation/presentation-bundle-manager/scripts/bundle_manager.py \
  --slug <slug> \
  --path /deliverables/<slug> \
  --title "<project_title>" \
  --author "<author>"
```

5. **Confirm output**: verify `index.xlsx` and `manifest.json` exist in the folder.

## index.xlsx Structure

The Excel index has two sheets:

**Sheet 1 — Summary**

| Field | Value |
|-------|-------|
| Project | `<project_title>` |
| Slug | `<slug>` |
| Author | `<author>` |
| Generated | `<ISO timestamp>` |
| Total files | `<N>` |
| Total size (KB) | `<N>` |

**Sheet 2 — Files**

| File | Type | Size (KB) | Created | Status | Notes |
|------|------|-----------|---------|--------|-------|
| storyboard.docx | Document | ... | ... | ✅ Present | |
| storyboard.json | JSON | ... | ... | ✅ Present | Stage 2 input |
| deck.pptx | Presentation | ... | ... | ✅ Present | |
| speaker-notes.docx | Document | ... | ... | ✅ Present | |
| index.xlsx | Index | ... | ... | ✅ This file | |
| manifest.json | Metadata | ... | ... | ✅ Present | |

## manifest.json Schema

```json
{
  "schema_version": "1.0",
  "project": {
    "title": "<project_title>",
    "slug": "<slug>",
    "author": "<author>",
    "generated_at": "<ISO 8601 timestamp>",
    "generated_by": "presentation-bundle-manager"
  },
  "deliverables": [
    {
      "file": "storyboard.docx",
      "type": "storyboard",
      "size_bytes": 0,
      "sha256": "<hash>",
      "status": "present"
    },
    {
      "file": "storyboard.json",
      "type": "storyboard_json",
      "size_bytes": 0,
      "sha256": "<hash>",
      "status": "present"
    },
    {
      "file": "deck.pptx",
      "type": "presentation",
      "size_bytes": 0,
      "sha256": "<hash>",
      "status": "present"
    },
    {
      "file": "speaker-notes.docx",
      "type": "speaker_notes",
      "size_bytes": 0,
      "sha256": "<hash>",
      "status": "present"
    }
  ],
  "validation": {
    "all_core_files_present": true,
    "warnings": []
  }
}
```

## Validation Rules

- If any core file is missing, set `"status": "missing"` in the manifest and `"all_core_files_present": false`.
- Add a warning entry for each missing file.
- Do not block bundle creation for missing files — produce the index with whatever is present.

## Output

Saves two files to `/deliverables/<slug>/`:
- `index.xlsx` — requires `openpyxl` (`pip install openpyxl`)
- `manifest.json` — pure Python standard library, no dependencies

## Limitations

- Does not zip or compress the bundle — the user can do this manually if needed.
- SHA256 hashes require file access; if files were not saved locally, the hash field is omitted.
- Does not upload or publish the bundle to any external service.
