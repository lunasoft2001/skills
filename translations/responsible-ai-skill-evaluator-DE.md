# Responsible AI Skill Evaluator — Skills auf Microsoft RAI & AgentSkills.io prüfen

Dieses Dokument beschreibt den Skill `responsible-ai-skill-evaluator` in diesem Repository.

## Beschreibung

Skill, der prüft, ob ein anderer Skill (SKILL.md) den 6 Prinzipien für verantwortungsvolle KI von Microsoft (Fairness, Zuverlässigkeit & Sicherheit, Datenschutz & Sicherheit, Inklusion, Transparenz, Verantwortlichkeit) sowie den Format- und Qualitätsstandards von AgentSkills.io entspricht. Erstellt einen strukturierten Auditbericht mit bewerteten Befunden und umsetzbaren Korrekturen.

Auslöser: `diesen Skill evaluieren`, `Skill auditieren`, `RAI-Konformität prüfen`, `SKILL.md reviewen`, `Skill für Veröffentlichung bereit`, `Skill-Zertifizierung`.

## Struktur

```text
responsible-ai-skill-evaluator/
  SKILL.md                                    # Anweisungen + Evaluierungsworkflow
  references/
    microsoft-rai-checklist.md               # 6 Microsoft RAI-Prinzipien angewendet auf Skills
    agentskills-quality-checklist.md         # Format- und Qualitätskriterien von AgentSkills.io
```

## Funktionen

- Bewertet einen Skill anhand der 6 Prinzipien für verantwortungsvolle KI von Microsoft
- Bewertet einen Skill anhand der Format- und Qualitätsstandards von AgentSkills.io
- Erstellt einen strukturierten Markdown-Auditbericht mit Bewertungen (PASS / PARTIAL / FAIL)
- Identifiziert Blocker (FAIL) und Empfehlungen (PARTIAL)
- Gibt ein Gesamturteil aus: READY TO PUBLISH / NEEDS FIXES / NOT COMPLIANT

## Verwendung

1. Skill installieren (siehe unten)
2. GitHub Copilot Chat öffnen
3. Eingeben: `"Evaluiere diesen Skill auf RAI-Konformität:"` und den zu prüfenden Skill einfügen oder referenzieren

## Skill-Installation

```bash
# macOS / Linux
cp -r responsible-ai-skill-evaluator ~/.copilot/skills/responsible-ai-skill-evaluator
```

Danach VS Code neu starten.

## Anforderungen

- VS Code mit GitHub Copilot
- Ein zu evaluierender Skill (SKILL.md)

## Referenzen

- [Microsoft: Sechs Prinzipien für verantwortungsvolle KI](https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/3-six-principles-of-responsible-ai)
- [AgentSkills.io: Skill-Ausgabequalität evaluieren](https://agentskills.io/skill-creation/evaluating-skills)
