# mssql-second-brain — SQL Server Second Brain fuer Obsidian

## Beschreibung

Oeffentliches Skill, das aus SQL-Server-Metadaten automatisch ein vollstaendiges Obsidian-Wissensvault erzeugt. Es extrahiert Schemas, Tabellen, Views, Procedures und Beziehungen mit einem lokalen Python-Skript (`pyodbc`) und verbraucht dabei 0 KI-Tokens.

Optionale KI-Stufe: `_overview.md` aus `_index.md` erzeugen.

## Struktur

```text
mssql-second-brain/
  SKILL.md
  scripts/
    generate_second_brain.py
```

## Hauptfunktionen

- Metadaten-Extraktion aus `INFORMATION_SCHEMA` + `sys.*`
- Eine Markdown-Notiz pro Schema/Tabelle/View/Procedure
- YAML-Frontmatter + Wikilinks + Rueckverweise ("Verwendet in")
- Obsidian-kompatible Struktur fuer Graph-Navigation
- Optionales konzeptionelles Ueberblicksdokument mit KI

## Typische Anwendungsfaelle

- Onboarding fuer neue Entwickler
- Lebende Datenbank-Architekturdokumentation
- Durchsuchbare interne Wissensbasis
- Analyse von Tabellenabhaengigkeiten und FK-Topologie

## Voraussetzungen

- Python 3
- `pyodbc`
- Netzwerkzugriff auf SQL Server
