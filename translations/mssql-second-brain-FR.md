# mssql-second-brain — Second Brain SQL Server pour Obsidian

## Description

Skill public qui genere automatiquement un vault de connaissance Obsidian complet a partir des metadonnees SQL Server. Il extrait schemas, tables, vues, procedures et relations via un script Python local (`pyodbc`) avec 0 tokens IA pendant l'extraction.

Etape IA optionnelle: creer `_overview.md` depuis `_index.md` apres generation.

## Structure

```text
mssql-second-brain/
  SKILL.md
  scripts/
    generate_second_brain.py
```

## Fonctionnalites principales

- Extraction des metadonnees SQL Server via `INFORMATION_SCHEMA` + `sys.*`
- Une note Markdown par schema/table/vue/procedure
- Frontmatter YAML + wikilinks + references inverses ("Utilise dans")
- Structure prete pour Obsidian et navigation graphe
- Fichier de vue d'ensemble optionnel genere par IA

## Cas d'usage

- Onboarding de nouveaux developpeurs
- Documentation vivante d'architecture de base de donnees
- Base de connaissance interne consultable
- Analyse des dependances de tables et topologie des cles etrangeres

## Prerequis

- Python 3
- `pyodbc`
- Acces reseau a SQL Server
