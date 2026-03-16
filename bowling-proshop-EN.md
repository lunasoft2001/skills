# Bowling Pro Shop — Virtual Ball Driller & Lane Coach

This document describes the contents of the `bowling-proshop` skill in this repository.

## Description

A virtual bowling ball driller and lane coach specialized in ball selection and **Dual Angle layouts** (Mo Pinel style). Conducts interactive multi-phase consultations to build the player's profile and generates a complete **visual HTML report** with a real ball image, lane diagram, ball drill diagram, and layout analysis.

Triggers: `ball selection`, `layout`, `oil pattern`, `drilling`, `rev rate`, `PAP`, `Dual Angle`, `hook potential`, `lane adjustments`.

## Structure

```text
bowling-proshop/
  SKILL.md                          # Skill instructions for GitHub Copilot
  assets/
    logo.jpeg                       # LunaBowling logo for the HTML report
  references/
    ball-selection.md               # Cover/category selection heuristics
    current-balls-2026.md           # Current ball catalog (2025-2026) with verified slugs
    dual-angle.md                   # Full Dual Angle layout system (Mo Pinel)
    manufacturers.md                # Manufacturer URLs for spec lookups
    patterns-reference.md           # Oil patterns: house, sport, challenge
    player-types.md                 # Speed/rev dominance, PAP, track classification
  scripts/
    generate_bowling_report_v2.py   # Visual HTML report generator
```

## Interactive Consultation

The skill uses four phases via `vscode_askQuestions`:

1. **Phase 1** — Dominant hand, lane type, goal
2. **Phase 2** — Ball speed, rev rate, PAP/track
3. **Phase 3** — Lane surface, friction, current arsenal
4. **Phase 4** — Visual report (player name)

## Visual HTML Report

At the end of the consultation, the skill generates an HTML report containing:

- Ball card with a real image fetched from the manufacturer's catalog
- Top-down SVG lane diagram with the recommended playing line
- SVG drill diagram (pin, PAP, mass bias, finger holes)
- Dual Angle layout with plain-language explanation
- Lane adjustments and data to refine

```bash
python3 scripts/generate_bowling_report_v2.py \
  --data /tmp/bowling_data.json \
  --output ~/Desktop/bowling_report.html

# Or with sample data:
python3 scripts/generate_bowling_report_v2.py --example
```

## Installation

Copy the folder into the GitHub Copilot skills directory:

```bash
# macOS / Linux
cp -r bowling-proshop ~/.copilot/skills/bowling-proshop

# Windows (PowerShell)
Copy-Item -Path "bowling-proshop" -Destination "$env:USERPROFILE\.copilot\skills\bowling-proshop" -Recurse
```

Then restart VS Code.

## Requirements

- Python 3.11+
- Internet connection (to fetch ball images from the manufacturer's catalog)
- No external dependencies — uses Python standard library only

## Notes

- Only recommends balls listed in `references/current-balls-2026.md` (active catalog, no discontinued balls).
- Storm ball images are fetched via verified slugs (`KNOWN_SLUG_MAP` in the script) — no guessing.
- Dual Angle layout system follows Mo Pinel: DA × Pin-to-PAP × VAL.
- Supports one-handed and two-handed players, right- and left-handed.
