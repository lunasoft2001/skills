# mssql-second-brain — Second Brain SQL Server per Obsidian

## Descrizione

Skill pubblico che genera automaticamente un vault di conoscenza completo in Obsidian partendo dai metadati di SQL Server. Estrae schema, tabelle, viste, stored procedure e relazioni con uno script Python locale (`pyodbc`) usando 0 token IA durante l'estrazione.

Passo IA opzionale: creare `_overview.md` da `_index.md` dopo la generazione.

## Struttura

```text
mssql-second-brain/
  SKILL.md
  scripts/
    generate_second_brain.py
```

## Funzionalita principali

- Estrazione metadati SQL Server da `INFORMATION_SCHEMA` + `sys.*`
- Una nota Markdown per schema/tabella/vista/procedura
- Frontmatter YAML + wikilink + riferimenti inversi ("Usata in")
- Struttura pronta per Obsidian e navigazione a grafo
- File panoramico opzionale generato da IA

## Casi d'uso

- Onboarding di nuovi sviluppatori
- Documentazione viva dell'architettura database
- Base di conoscenza interna ricercabile
- Analisi dipendenze tabelle e topologia delle foreign key

## Requisiti

- Python 3
- `pyodbc`
- Accesso di rete a SQL Server
