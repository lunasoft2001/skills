# M365 Email Manager Skill Bundle

This document describes the contents of the `m365-email-manager-skill` in this repository.

## Structure

```text
m365-email-manager-skill/
  SKILL.md                        # Skill metadata and usage guidance
  scripts/                        # Python scripts for setup, auth, and email operations
    setup.py                      # One-time configuration flow
    token_manager.py              # Token storage and refresh handling
    m365_mail.py                  # Main CLI for Microsoft 365 email actions
    m365_mail_es.py               # Spanish CLI variant
    test_demo.py                  # Demo/testing helper
  references/                     # Supporting docs (quickstart, permissions, API, body options)
```

## Installation

To install this skill in GitHub Copilot, copy this folder into your Copilot skills directory:

```powershell
Copy-Item -Path "m365-email-manager-skill" -Destination "$env:USERPROFILE\.copilot\skills\m365-email-manager-skill" -Recurse
```

Then restart VS Code.

## Notes

- This skill automates Microsoft 365 email actions through Microsoft Graph.
- Typical operations include list/search/send/reply/move/mark-as-read.
- Run setup once (`scripts/setup.py`) to avoid repeated authentication prompts.
