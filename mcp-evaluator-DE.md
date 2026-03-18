# MCP Evaluator — MCP-Server auditieren: Sicherheit, Datenschutz und Qualität

Dieses Dokument beschreibt den Skill `mcp-evaluator` in diesem Repository.

## Beschreibung

Skill, der MCP-Server (Model Context Protocol) auf Sicherheit, Datenschutz und technische Qualität prüft. Analysiert Quellcode (TypeScript/Python), Tool-Definitionen, Konfigurationsdateien und begleitende SKILL.md. Erstellt einen strukturierten PASS/PARTIAL/FAIL-Bericht mit umsetzbaren Korrekturen.

Auslöser: `MCP auditieren`, `MCP-Server evaluieren`, `MCP-Sicherheit prüfen`, `MCP-Tools überprüfen`, `ist mein MCP sicher`, `MCP bereit zur Veröffentlichung`.

## Struktur

```text
mcp-evaluator/
  SKILL.md                              # Anweisungen + 3-Phasen-Evaluierungsworkflow
  references/
    mcp-rai-checklist.md               # Sicherheits- und Datenschutzkriterien (RAI + OWASP)
    mcp-quality-checklist.md           # Technische Qualitätskriterien
```

## Funktionen

- **Phase 1 — Sicherheit & Datenschutz**: Zugangsdaten, PII, destruktive Operationen, Injection/SSRF, Tokens
- **Phase 2 — Technische Qualität**: Tool-Design, Fehlerbehandlung, Companion-Skill, Abhängigkeiten, Logging
- **Phase 3 — Verantwortlichkeit**: Lizenz, Repo, Versionierung, Maintainer
- Erstellt Markdown-Bericht mit bewerteten Abschnitten (PASS / PARTIAL / FAIL)
- Gesamturteil: `SAFE TO USE` / `NEEDS FIXES` / `SECURITY RISK`

## Verwendung

1. Skill installieren (siehe unten)
2. GitHub Copilot Chat öffnen
3. Eingeben: `"Auditiere meinen LinkedIn-MCP auf Sicherheit"` — Copilot liest den Quellcode und erstellt den vollständigen Bericht

## Skill-Installation

```bash
# macOS / Linux
cp -r mcp-evaluator ~/.copilot/skills/mcp-evaluator
```

Danach VS Code neu starten.

## Anforderungen

- VS Code mit GitHub Copilot
- Zugriff auf den Quellcode des zu evaluierenden MCP-Servers
