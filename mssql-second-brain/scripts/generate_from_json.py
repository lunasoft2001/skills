#!/usr/bin/env python3
"""
mssql-second-brain v3: Genera vault Obsidian leyendo metadata.json extraído vía MCP.

Uso:
    python3 generate_from_json.py --metadata /path/metadata.json --output /path/vault/

No requiere pyodbc ni conexión a base de datos.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers de formato Obsidian
# ---------------------------------------------------------------------------

def safe_name(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_").replace("\\", "_")


def object_fname(schema: str, name: str) -> str:
    return safe_name(name) if schema.lower() == "dbo" else f"{safe_name(schema)}_{safe_name(name)}"


def table_link(schema: str, table: str) -> str:
    return f"[[tables/{object_fname(schema, table)}]]"


def view_link(schema: str, view: str) -> str:
    return f"[[views/{object_fname(schema, view)}]]"


def proc_link(schema: str, proc: str) -> str:
    return f"[[procedures/{object_fname(schema, proc)}]]"


def definition_excerpt(definition: str | None, max_lines: int = 20) -> str:
    if not definition:
        return "-- definición no disponible"
    lines = definition.strip().splitlines()
    excerpt = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        excerpt += f"\n-- ... ({len(lines) - max_lines} líneas más)"
    return excerpt


def today_iso() -> str:
    return date.today().isoformat()


def table_key(schema: str, table: str) -> str:
    return f"{schema}.{table}"


# ---------------------------------------------------------------------------
# Generadores de .md
# ---------------------------------------------------------------------------

def build_table_md(schema, table, columns, pks, fk_out, fk_in, used_views, used_procs):
    has_pk = bool(pks)
    has_fk = bool(fk_out)

    fk_col_refs = {}
    for fk in fk_out:
        fk_col_refs[fk["fk_column"]] = (fk["ref_schema"], fk["ref_table"])

    lines = [
        "---",
        "type: db-table",
        f"schema: {schema}",
        f"table: {table}",
        f"columns: {len(columns)}",
        f"has_pk: {'true' if has_pk else 'false'}",
        f"has_fk: {'true' if has_fk else 'false'}",
        "tags:",
        "  - db/table",
        f"  - schema/{schema}",
        f"created: {today_iso()}",
        "---",
        "",
        f"# {table}",
        "",
        "## Columnas",
        "",
        "| Columna | Tipo | Nullable | PK | FK |",
        "|---------|------|----------|----|----|",
    ]

    for col in columns:
        col_name = col["column_name"]
        dtype = col["data_type"]
        maxlen = col.get("character_maximum_length")
        if maxlen:
            dtype = f"{dtype}(MAX)" if maxlen == -1 else f"{dtype}({maxlen})"
        nullable = "NO" if col["is_nullable"] == "NO" else "SÍ"
        pk_mark = "✅" if col_name in pks else ""
        if col_name in fk_col_refs:
            rs, rt = fk_col_refs[col_name]
            fk_mark = f"→ {table_link(rs, rt)}"
        else:
            fk_mark = ""
        lines.append(f"| {col_name} | {dtype} | {nullable} | {pk_mark} | {fk_mark} |")

    lines += ["", "## Relaciones", ""]
    if fk_out:
        for fk in fk_out:
            lines.append(f"- → {table_link(fk['ref_schema'], fk['ref_table'])} via `{fk['fk_column']}`")
    if fk_in:
        for fk in fk_in:
            lines.append(f"- ← {table_link(fk['fk_schema'], fk['fk_table'])} via `{fk['fk_column']}`")
    if not fk_out and not fk_in:
        lines.append("_(sin relaciones FK)_")

    lines += ["", "## Usada en", ""]
    used = [f"- {view_link(s, n)}" for s, n in used_views] + \
           [f"- {proc_link(s, n)}" for s, n in used_procs]
    lines += used if used else ["_(no se encontraron referencias en views/procedures)_"]

    return "\n".join(lines) + "\n"


def build_view_md(schema, view, definition, referenced_tables):
    lines = [
        "---",
        "type: db-view",
        f"schema: {schema}",
        f"view: {view}",
        "tags:",
        "  - db/view",
        f"  - schema/{schema}",
        f"created: {today_iso()}",
        "---",
        "",
        f"# {view}",
        "",
        "## Tablas que usa",
        "",
    ]
    if referenced_tables:
        for ts, tn in referenced_tables:
            lines.append(f"- {table_link(ts, tn)}")
    else:
        lines.append("_(no se encontraron referencias de tablas)_")

    lines += [
        "",
        "## Definición (extracto)",
        "",
        "```sql",
        definition_excerpt(definition),
        "```",
        "",
    ]
    return "\n".join(lines)


def build_procedure_md(schema, proc, definition, referenced_tables):
    lines = [
        "---",
        "type: db-procedure",
        f"schema: {schema}",
        f"procedure: {proc}",
        "tags:",
        "  - db/procedure",
        f"  - schema/{schema}",
        f"created: {today_iso()}",
        "---",
        "",
        f"# {proc}",
        "",
        "## Tablas que referencia",
        "",
    ]
    if referenced_tables:
        for ts, tn in referenced_tables:
            lines.append(f"- {table_link(ts, tn)}")
    else:
        lines.append("_(no se encontraron referencias de tablas)_")

    lines += [
        "",
        "## Definición (extracto)",
        "",
        "```sql",
        definition_excerpt(definition),
        "```",
        "",
    ]
    return "\n".join(lines)


def build_schema_md(schema, tables, views, procs):
    lines = [
        "---",
        "type: db-schema",
        f"schema: {schema}",
        f"total_tables: {len(tables)}",
        f"total_views: {len(views)}",
        f"total_procedures: {len(procs)}",
        "tags:",
        "  - db/schema",
        f"created: {today_iso()}",
        "---",
        "",
        f"# Schema: {schema}",
        "",
        f"## Tablas ({len(tables)})",
        "",
    ]
    for t in sorted(tables):
        lines.append(f"- {table_link(schema, t)}")
    lines += ["", f"## Views ({len(views)})", ""]
    for v in sorted(views):
        lines.append(f"- {view_link(schema, v)}")
    lines += ["", f"## Procedures ({len(procs)})", ""]
    for p in sorted(procs):
        lines.append(f"- {proc_link(schema, p)}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Generadores de .base (Obsidian Bases)
# ---------------------------------------------------------------------------

def build_all_tables_base():
    return """\
filters:
  and:
    - 'type == "db-table"'
properties:
  file.name:
    displayName: Tabla
  schema:
    displayName: Schema
  columns:
    displayName: Columnas
  has_pk:
    displayName: Tiene PK
  has_fk:
    displayName: Tiene FK
views:
  - type: table
    name: Todas las tablas
    order:
      - file.name
      - schema
      - columns
      - has_pk
      - has_fk
  - type: cards
    name: Cards de tablas
    order:
      - file.name
      - schema
      - columns
      - has_pk
      - has_fk
"""


def build_tables_no_pk_base():
    return """\
filters:
  and:
    - 'type == "db-table"'
    - 'has_pk == false'
properties:
  file.name:
    displayName: Tabla
  schema:
    displayName: Schema
  columns:
    displayName: Columnas
  has_fk:
    displayName: Tiene FK
views:
  - type: table
    name: Tablas sin Primary Key
    order:
      - file.name
      - schema
      - columns
      - has_fk
"""


def build_tables_with_fk_base():
    return """\
filters:
  and:
    - 'type == "db-table"'
    - 'has_fk == true'
properties:
  file.name:
    displayName: Tabla
  schema:
    displayName: Schema
  columns:
    displayName: Columnas
  has_pk:
    displayName: Tiene PK
views:
  - type: table
    name: Tablas con Foreign Keys
    order:
      - file.name
      - schema
      - columns
      - has_pk
"""


def build_all_views_base():
    return """\
filters:
  and:
    - 'type == "db-view"'
properties:
  file.name:
    displayName: Vista
  schema:
    displayName: Schema
views:
  - type: table
    name: Todas las vistas
    order:
      - file.name
      - schema
  - type: cards
    name: Cards de vistas
    order:
      - file.name
      - schema
"""


def build_all_procedures_base():
    return """\
filters:
  and:
    - 'type == "db-procedure"'
properties:
  file.name:
    displayName: Stored Procedure
  schema:
    displayName: Schema
views:
  - type: table
    name: Todos los stored procedures
    order:
      - file.name
      - schema
  - type: cards
    name: Cards de procedures
    order:
      - file.name
      - schema
"""


def build_db_overview_base():
    return """\
filters:
  or:
    - 'type == "db-table"'
    - 'type == "db-view"'
    - 'type == "db-procedure"'
properties:
  file.name:
    displayName: Objeto
  type:
    displayName: Tipo
  schema:
    displayName: Schema
views:
  - type: table
    name: Todos los objetos
    groupBy:
      property: type
      direction: ASC
    order:
      - file.name
      - type
      - schema
"""


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

def build_index_md(database, schemas, all_tables, all_views, all_procs):
    lines = [
        "---",
        "type: db-index",
        f"database: {database}",
        f"generated: {today_iso()}",
        f"total_tables: {len(all_tables)}",
        f"total_views: {len(all_views)}",
        f"total_procedures: {len(all_procs)}",
        f"total_schemas: {len(schemas)}",
        "---",
        "",
        f"# {database} — Second Brain Index",
        "",
        "_Generado automáticamente con mssql-second-brain skill._",
        "",
        f"## Schemas ({len(schemas)})",
        "",
    ]
    for s in sorted(schemas):
        lines.append(f"- [[schemas/{safe_name(s)}]]")

    lines += ["", f"## Tablas ({len(all_tables)})", ""]
    for ts, tn in sorted(all_tables):
        lines.append(f"- {table_link(ts, tn)}")

    lines += ["", f"## Views ({len(all_views)})", ""]
    for vs, vn in sorted(all_views):
        lines.append(f"- {view_link(vs, vn)}")

    lines += ["", f"## Procedures ({len(all_procs)})", ""]
    for ps, pn in sorted(all_procs):
        lines.append(f"- {proc_link(ps, pn)}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="mssql-second-brain v3: genera vault Obsidian desde metadata.json"
    )
    parser.add_argument("--metadata", required=True, help="Ruta al metadata.json generado por el agente")
    parser.add_argument("--output",   required=True, help="Ruta base del vault Obsidian")
    parser.add_argument("--schemas",  default=None,  help="Schemas a incluir, separados por coma")
    parser.add_argument("--no-procedures", action="store_true", help="Excluir stored procedures")
    parser.add_argument("--no-views",      action="store_true", help="Excluir views")
    return parser.parse_args()


def main():
    args = parse_args()

    metadata_path = Path(args.metadata)
    if not metadata_path.exists():
        print(f"ERROR: No se encontró {metadata_path}")
        sys.exit(1)

    print(f"📖 Leyendo {metadata_path}...")
    with open(metadata_path, encoding="utf-8") as f:
        data = json.load(f)

    database      = data.get("database", "unknown")
    raw_columns   = data.get("columns", [])
    raw_pks       = data.get("primary_keys", [])
    raw_fks       = data.get("foreign_keys", [])
    raw_views     = data.get("views", []) if not args.no_views else []
    raw_procs     = data.get("procedures", []) if not args.no_procedures else []
    raw_deps      = data.get("dependencies", [])

    # Normalizar claves a minúsculas (por si el agente las dejó en otro caso)
    def norm(rows):
        return [{k.lower(): v for k, v in row.items()} for row in rows]

    raw_columns = norm(raw_columns)
    raw_pks     = norm(raw_pks)
    raw_fks     = norm(raw_fks)
    raw_views   = norm(raw_views)
    raw_procs   = norm(raw_procs)
    raw_deps    = norm(raw_deps)

    allowed_schemas = {s.strip() for s in args.schemas.split(",")} if args.schemas else None

    def schema_ok(s):
        return allowed_schemas is None or s in allowed_schemas

    raw_columns = [r for r in raw_columns if schema_ok(r.get("table_schema", ""))]
    raw_pks     = [r for r in raw_pks     if schema_ok(r.get("table_schema", ""))]
    raw_fks     = [r for r in raw_fks     if schema_ok(r.get("fk_schema", ""))]
    raw_views   = [r for r in raw_views   if schema_ok(r.get("table_schema", ""))]
    raw_procs   = [r for r in raw_procs   if schema_ok(r.get("routine_schema", ""))]

    # Índices
    table_cols  = defaultdict(list)
    for r in raw_columns:
        table_cols[table_key(r["table_schema"], r["table_name"])].append(r)

    table_pks = defaultdict(set)
    for r in raw_pks:
        table_pks[table_key(r["table_schema"], r["table_name"])].add(r["column_name"])

    table_fk_out = defaultdict(list)
    for r in raw_fks:
        table_fk_out[table_key(r["fk_schema"], r["fk_table"])].append(r)

    table_fk_in = defaultdict(list)
    for r in raw_fks:
        table_fk_in[table_key(r["ref_schema"], r["ref_table"])].append(r)

    tables_set = set()
    for k in table_cols:
        schema, tname = k.split(".", 1)
        tables_set.add((schema, tname))

    views_set = {(r["table_schema"], r["table_name"]) for r in raw_views}
    procs_set = {(r["routine_schema"], r["routine_name"]) for r in raw_procs}

    known_tables_lower = {t.lower() for _, t in tables_set}
    view_names_lower   = {v.lower() for _, v in views_set}
    proc_names_lower   = {p.lower() for _, p in procs_set}

    obj_refs_tables = defaultdict(set)
    table_used_by   = defaultdict(set)

    for r in raw_deps:
        src_schema = r.get("src_schema") or ""
        src_name   = r.get("src_name") or ""
        ref_name   = r.get("ref_name") or ""
        ref_schema = r.get("ref_schema") or ""

        if ref_name.lower() not in known_tables_lower:
            continue

        src_is_view = src_name.lower() in view_names_lower
        src_is_proc = src_name.lower() in proc_names_lower

        if src_is_view or src_is_proc:
            obj_type = "view" if src_is_view else "proc"
            obj_refs_tables[f"{src_schema}.{src_name}"].add((ref_schema, ref_name))
            for ts, tn in tables_set:
                if tn.lower() == ref_name.lower():
                    table_used_by[table_key(ts, tn)].add((src_schema, src_name, obj_type))
                    break

    def used_by_split(tk):
        used_v, used_p = [], []
        for ss, sn, st in table_used_by.get(tk, set()):
            (used_v if st == "view" else used_p).append((ss, sn))
        return used_v, used_p

    # Carpetas
    root = Path(args.output) / "db-second-brain"
    for sub in ("tables", "views", "procedures", "schemas"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    file_count  = 0
    all_schemas = set()

    # Tablas
    print("📝 Generando notas de tablas...")
    for schema, tname in sorted(tables_set):
        all_schemas.add(schema)
        tk     = table_key(schema, tname)
        used_v, used_p = used_by_split(tk)
        content = build_table_md(
            schema, tname,
            table_cols.get(tk, []),
            table_pks.get(tk, set()),
            table_fk_out.get(tk, []),
            table_fk_in.get(tk, []),
            used_v, used_p,
        )
        (root / "tables" / f"{object_fname(schema, tname)}.md").write_text(content, encoding="utf-8")
        file_count += 1

    # Views
    if not args.no_views:
        print("📝 Generando notas de views...")
        view_def_map = {(r["table_schema"], r["table_name"]): r.get("view_definition") for r in raw_views}
        for schema, vname in sorted(views_set):
            all_schemas.add(schema)
            refs = list(obj_refs_tables.get(f"{schema}.{vname}", set()))
            content = build_view_md(schema, vname, view_def_map.get((schema, vname)), refs)
            (root / "views" / f"{object_fname(schema, vname)}.md").write_text(content, encoding="utf-8")
            file_count += 1

    # Procedures
    if not args.no_procedures:
        print("📝 Generando notas de procedures...")
        proc_def_map = {(r["routine_schema"], r["routine_name"]): r.get("routine_definition") for r in raw_procs}
        for schema, pname in sorted(procs_set):
            all_schemas.add(schema)
            refs = list(obj_refs_tables.get(f"{schema}.{pname}", set()))
            content = build_procedure_md(schema, pname, proc_def_map.get((schema, pname)), refs)
            (root / "procedures" / f"{object_fname(schema, pname)}.md").write_text(content, encoding="utf-8")
            file_count += 1

    # Schemas
    print("📝 Generando notas de schemas...")
    s_tables = defaultdict(list)
    s_views  = defaultdict(list)
    s_procs  = defaultdict(list)
    for s, t in tables_set: s_tables[s].append(t)
    for s, v in views_set:  s_views[s].append(v)
    for s, p in procs_set:  s_procs[s].append(p)

    for schema in sorted(all_schemas):
        content = build_schema_md(schema, s_tables[schema], s_views[schema], s_procs[schema])
        (root / "schemas" / f"{safe_name(schema)}.md").write_text(content, encoding="utf-8")
        file_count += 1

    # Index
    print("📝 Generando _index.md...")
    index_content = build_index_md(
        database,
        list(all_schemas),
        list(tables_set),
        list(views_set) if not args.no_views else [],
        list(procs_set) if not args.no_procedures else [],
    )
    (root / "_index.md").write_text(index_content, encoding="utf-8")
    file_count += 1

    # Bases (Obsidian Bases)
    print("📊 Generando archivos .base (Obsidian Bases)...")
    bases_dir = root / "bases"
    bases_dir.mkdir(parents=True, exist_ok=True)
    bases_count = 0

    (bases_dir / "all-tables.base").write_text(build_all_tables_base(), encoding="utf-8")
    bases_count += 1
    (bases_dir / "tables-no-pk.base").write_text(build_tables_no_pk_base(), encoding="utf-8")
    bases_count += 1
    (bases_dir / "tables-with-fk.base").write_text(build_tables_with_fk_base(), encoding="utf-8")
    bases_count += 1
    (bases_dir / "db-overview.base").write_text(build_db_overview_base(), encoding="utf-8")
    bases_count += 1

    if not args.no_views:
        (bases_dir / "all-views.base").write_text(build_all_views_base(), encoding="utf-8")
        bases_count += 1

    if not args.no_procedures:
        (bases_dir / "all-procedures.base").write_text(build_all_procedures_base(), encoding="utf-8")
        bases_count += 1

    file_count += bases_count

    print()
    print(f"✅ Second Brain generado en: {root}")
    print(f"   Schemas:    {len(all_schemas)}")
    print(f"   Tablas:     {len(tables_set)}")
    print(f"   Views:      {len(views_set) if not args.no_views else 0}")
    print(f"   Procedures: {len(procs_set) if not args.no_procedures else 0}")
    print(f"   Bases:      {bases_count}")
    print(f"   Ficheros:   {file_count}")
    print()
    print("Para generar el overview con IA, abre Copilot y escribe:")
    print('  "Genera _overview.md leyendo db-second-brain/_index.md"')


if __name__ == "__main__":
    main()
