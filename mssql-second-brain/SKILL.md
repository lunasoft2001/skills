---
name: mssql-second-brain
description: >
  Generate an Obsidian Second Brain vault from a SQL Server database.
  Connect via MCP mssql or pyodbc, extract metadata from INFORMATION_SCHEMA + sys.*,
  and create Markdown notes with YAML frontmatter, FK wikilinks, and reverse usage sections.
  Zero AI tokens during extraction (local Python script). Optional AI only for _overview.md.
triggers:
  - second brain
  - SQL Server vault
  - mssql second brain
  - generate database documentation
  - map database structure
  - create SQL Server Obsidian vault
  - export schema to Obsidian
  - mssql-second-brain
tools:
  - create_file
  - run_in_terminal
  - read_file
---

# Skill: mssql-second-brain

Automatically generates an Obsidian vault that documents a full SQL Server database as a navigable Second Brain. The extraction script does not call any AI model: zero tokens during generation.

## When to Activate

Activate this skill when the user asks for any of the following:
- "second brain", "mssql second brain", "SQL Server vault"
- "generate database documentation", "map database structure"
 name: mssql-second-brain
 description: >
   Generate an Obsidian Second Brain vault from a SQL Server database.
   Connect via MCP mssql or pyodbc, extract metadata from INFORMATION_SCHEMA + sys.*,
   and create Markdown notes with YAML frontmatter, FK wikilinks, and reverse usage sections.
   Zero AI tokens during extraction (local Python script). Optional AI only for _overview.md.
 triggers:
   - second brain
   - SQL Server vault
   - mssql second brain
   - generate database documentation
   - map database structure
   - create SQL Server Obsidian vault
   - export schema to Obsidian
   - mssql-second-brain
 tools:
   - create_file
   - run_in_terminal
   - read_file
 ---
 
 # Skill: mssql-second-brain
 
 Automatically generates an Obsidian vault that documents a full SQL Server database as a navigable Second Brain. The extraction script does not call any AI model: zero tokens during generation.
 
 ## When to Activate
 
 Activate this skill when the user asks for any of the following:
 - "second brain", "mssql second brain", "SQL Server vault"
 - "generate database documentation", "map database structure"
 - "create SQL Server Obsidian vault", "export schema to Obsidian"
 - "mssql-second-brain"
 
 ---
 
 ## Execution Flow
 
 ### Step 1 - Collect Parameters
 
 Ask for missing parameters before running:
 
 Required:
 - `server`: SQL Server host/instance (e.g. `localhost`, `192.168.1.10\\SQLEXPRESS`)
 - `database`: database name
 - `output_dir`: Obsidian destination path
 
 Optional (use defaults if missing):
 - `schemas`: comma-separated schema list (default: all)
 - `include_procedures`: true/false (default: true)
 - `include_views`: true/false (default: true)
 - `user`: SQL login user (if missing, use integrated auth)
 - `password`: SQL login password (prefer env var `MSSQL_PASSWORD`)
 
 ### Step 2 - Validate Dependencies
 
 Run:
 ```bash
 python -c "import pyodbc; print('pyodbc OK')"
 ```
 
 If it fails, suggest:
 ```bash
 pip install pyodbc
 ```
 On macOS, `unixodbc` may also be needed:
 ```bash
 brew install unixodbc
 ```
 
 ### Step 3 - Locate the Generator Script
 
 Use the local script bundled with this skill:
 - `scripts/generate_second_brain.py`
 
 ### Step 4 - Execute Generation
 
 ```bash
 python generate_second_brain.py \
   --server "{server}" \
   --database "{database}" \
   --output "{output_dir}" \
   [--schemas "dbo,hr"] \
   [--no-procedures] \
   [--no-views] \
   [--user "sa"] \
   [--password "***"]
 ```
 
 The script creates `db-second-brain/` under `output_dir` and prints a final summary.
 
 ### Step 5 - Optional AI Overview
 
 After generation, ask:
 > "Do you want me to create `_overview.md` from `_index.md` with a conceptual map of your database?"
 
 If yes:
 1. Read `{output_dir}/db-second-brain/_index.md`
 2. Generate `{output_dir}/db-second-brain/_overview.md` including:
    - High-level system purpose inferred from naming
    - Thematic table clusters (e.g. customers, billing, operations)
    - Key cross-module relationships
    - Candidate central tables by inbound FK count
 
 ---
 
 ## Output Vault Structure
 
 ```text
 {output_dir}/
 └── db-second-brain/
     ├── _index.md
     ├── _overview.md            # optional AI-generated file
     ├── schemas/
     │   └── {schema}.md
     ├── tables/
     │   └── {table}.md
     ├── views/
     │   └── {view}.md
     └── procedures/
         └── {procedure}.md
 ```
 
 ---
 
 ## Generated Note Content
 
 ### `tables/{table}.md`
 - YAML frontmatter: `type`, `schema`, `table`, `columns`, `has_pk`, `has_fk`, `tags`, `created`
 - Column table: name, datatype, nullable, PK, FK target with wikilinks
 - Relationships section:
   - Outbound FKs (`->`)
   - Inbound FKs (`<-`)
 - "Used by" section: views/procedures referencing the table
 
 ### `views/{view}.md`
 - YAML frontmatter: `type`, `schema`, `view`, `tags`, `created`
 - Referenced tables (wikilinks)
 - SQL definition excerpt (first lines)
 
 ### `procedures/{procedure}.md`
 - YAML frontmatter: `type`, `schema`, `procedure`, `tags`, `created`
 - Referenced tables (wikilinks)
 - SQL definition excerpt (first lines)
 
 ### `schemas/{schema}.md`
 - Schema summary counts: tables, views, procedures
 - Full object index with wikilinks
 
 ### `_index.md`
 - Global database stats
 - Master index linking all generated objects
 
 ---
 
 ## Security Notes
 
 - Never hardcode credentials in files.
 - Prefer environment variables (e.g. `MSSQL_PASSWORD`).
 - Generated Markdown must not contain connection secrets.
 
 ---
 
 ## Versioning
 
 - `v1.0`: full one-shot generation (current)
 - `v2.0` (planned): incremental generation with manifest + change detection
