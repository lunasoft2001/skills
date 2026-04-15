# ChannelToObsidian

## Purpose
Two-phase skill to capture an entire YouTube channel into an Obsidian Second Brain vault. First scans all channel videos into a Markdown checklist, then processes only the ones you select by running the full VideoToObsidian pipeline on each.

## Structure
- `ChannelToObsidian/SKILL.md` — skill definition and complete two-phase workflow
- `ChannelToObsidian/scripts/channel_to_obsidian.py` — script that fetches all channel videos (InnerTube browse API), builds the index, and drives VideoToObsidian for selected items

**Depends on:** skill `VideoToObsidian` (must be installed in the sibling directory)

## Main Features
- Fetches all channel videos via InnerTube browse API (zero external dependencies, pagination included)
- Creates/updates `Atlas/Personas/<ChannelName>.md` as a selectable checklist
- State markers: `[ ]` not reviewed · `[x]` selected · `[p]` already processed
- Phase 2 calls VideoToObsidian for each `[x]` item and marks it `[p]` when done
- Supports channel URLs: handle (`@name`), `/c/`, `/channel/UC…`, or watch URL
- Configurable vault path via `OBSIDIAN_VAULT` environment variable

## Typical Use Cases
- Building a knowledge base from a favourite technical channel
- Reviewing all videos of a creator before deciding which ones to study
- Batch-processing an entire playlist or channel with selective curation
- Maintaining an up-to-date index of a channel as new videos are published
