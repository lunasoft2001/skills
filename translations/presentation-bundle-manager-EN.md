# Presentation Bundle Manager

This document describes the `presentation-bundle-manager` skill.

## Description

Packages all presentation deliverables into a structured project folder, generates an `index.xlsx` inventory (two sheets: Summary + Files) and a `manifest.json` with SHA256 checksums and validation status. Handles partial bundles gracefully when core files are missing.

## Triggers

`bundle the presentation`, `package the deliverables`, `create the manifest`, `generate the index`, `finalize the presentation package`

## Output Files

| File | Description |
|------|-------------|
| `index.xlsx` | Two-sheet Excel index: Summary + Files |
| `manifest.json` | JSON manifest with checksums and validation |

## manifest.json Structure

```json
{
  "schema_version": "1.0",
  "project": { "title", "slug", "author", "generated_at", "generated_by" },
  "deliverables": [ { "file", "type", "size_bytes", "sha256", "status" } ],
  "validation": { "all_core_files_present", "warnings" }
}
```

## Usage

```bash
python3 scripts/bundle_manager.py \
  --slug my-slug \
  --title "My Presentation" \
  --author "Jane Smith"
```

## Requirements

- Python 3.9+ (standard library only for `manifest.json`)
- `pip install openpyxl` (for `index.xlsx`)

## Structure

```
presentation-bundle-manager/
  SKILL.md
  scripts/
    bundle_manager.py
  evals/
    evals.json
```
