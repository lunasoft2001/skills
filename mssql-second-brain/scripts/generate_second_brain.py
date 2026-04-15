#!/usr/bin/env python3
"""
mssql-second-brain: Genera vault Obsidian desde metadatos de SQL Server.

Uso:
    python generate_second_brain.py --server localhost --database MyDB --output /path/to/vault

Dependencias:
    pip install pyodbc
    (macOS) brew install unixodbc
"""

import argparse
import os
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Verificar pyodbc
# ---------------------------------------------------------------------------
try:
    import pyodbc
except ImportError:
    print("ERROR: pyodbc no está instalado.")
    print("  pip install pyodbc")
    print("  (macOS) brew install unixodbc")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Conexión
# ---------------------------------------------------------------------------

def build_connection_string(server: str, database: str, user: str | None, password: str | None) -> str:
    pwd = password or os.environ.get("MSSQL_PASSWORD")
    if user and pwd:
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};"
            f"UID={user};PWD={pwd};"
        )
    # Autenticación integrada (Windows/Trusted)
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};DATABASE={database};"
        f"Trusted_Connection=yes;"
    )


def connect(server: str, database: str, user: str | None, password: str | None) -> pyodbc.Connection:
    conn_str = build_connection_string(server, database, user, password)
    try:
        return pyodbc.connect(conn_str, timeout=15)
    except pyodbc.Error as e:
        print(f"ERROR: No se pudo conectar a SQL Server.")
        print(f"  {e.args[-1] if e.args else e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

SQL_COLUMNS = """
SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE,
       IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH, ORDINAL_POSITION
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
"""

SQL_PRIMARY_KEYS = """
SELECT tc.TABLE_SCHEMA, tc.TABLE_NAME, kcu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
  ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
     AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
     AND tc.TABLE_NAME   = kcu.TABLE_NAME
WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
"""

SQL_FOREIGN_KEYS = """
SELECT
  fk.name                                                    AS fk_name,
  OBJECT_SCHEMA_NAME(fk.parent_object_id)                    AS fk_schema,
  OBJECT_NAME(fk.parent_object_id)                           AS fk_table,
  COL_NAME(fkc.parent_object_id, fkc.parent_column_id)       AS fk_column,
  OBJECT_SCHEMA_NAME(fk.referenced_object_id)                AS ref_schema,
  OBJECT_NAME(fk.referenced_object_id)                       AS ref_table,
  COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ref_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
"""

SQL_VIEWS = """
SELECT TABLE_SCHEMA, TABLE_NAME, VIEW_DEFINITION
FROM INFORMATION_SCHEMA.VIEWS
ORDER BY TABLE_SCHEMA, TABLE_NAME
"""

SQL_PROCEDURES = """
SELECT ROUTINE_SCHEMA, ROUTINE_NAME, ROUTINE_DEFINITION
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_TYPE = 'PROCEDURE'
ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
"""

SQL_DEPENDENCIES = """
SELECT
  OBJECT_SCHEMA_NAME(referencing_id)  AS src_schema,
  OBJECT_NAME(referencing_id)         AS src_name,
  referenced_schema_name              AS ref_schema,
  referenced_entity_name              AS ref_name
FROM sys.sql_expression_dependencies
WHERE referenced_entity_name IS NOT NULL
"""


def fetch_all(cursor: pyodbc.Cursor, sql: str) -> list[dict]:
    cursor.execute(sql)
    cols = [c[0].lower() for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Helpers de formato Obsidian
# ---------------------------------------------------------------------------

def safe_name(name: str) -> str:
    """Sanitiza nombre para usar como nombre de fichero."""
    return name.replace(" ", "_").replace("/", "_").replace("\\", "_")


def table_key(schema: str, table: str) -> str:
    return f"{schema}.{table}"


def table_link(schema: str, table: str) -> str:
    fname = safe_name(table) if schema.lower() == "dbo" else f"{safe_name(schema)}_{safe_name(table)}"
    return f"[[tables/{fname}]]"


def view_link(schema: str, view: str) -> str:
    fname = safe_name(view) if schema.lower() == "dbo" else f"{safe_name(schema)}_{safe_name(view)}"
    return f"[[views/{fname}]]"


def proc_link(schema: str, proc: str) -> str:
    fname = safe_name(proc) if schema.lower() == "dbo" else f"{safe_name(schema)}_{safe_name(proc)}"
    return f"[[procedures/{fname}]]"


def object_fname(schema: str, name: str) -> str:
    return safe_name(name) if schema.lower() == "dbo" else f"{safe_name(schema)}_{safe_name(name)}"


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


# ---------------------------------------------------------------------------
# Generadores de .md
# ---------------------------------------------------------------------------

def build_table_md(
    schema: str,
    table: str,
    columns: list[dict],
    pks: set[str],
    fk_out: list[dict],   # FKs donde esta tabla es la de origen
    fk_in: list[dict],    # FKs donde esta tabla es la referenciada
    used_in_views: list[tuple[str, str]],
    used_in_procs: list[tuple[str, str]],
) -> str:
    has_pk = bool(pks)
    has_fk = bool(fk_out)
    fname = object_fname(schema, table)

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

    # Columnas
    fk_col_refs: dict[str, tuple[str, str, str]] = {}
    for fk in fk_out:
        fk_col_refs[fk["fk_column"]] = (fk["ref_schema"], fk["ref_table"], fk["ref_column"])

    for col in columns:
        col_name = col["column_name"]
        dtype = col["data_type"]
        if col.get("character_maximum_length"):
            maxlen = col["character_maximum_length"]
            dtype = f"{dtype}({maxlen})" if maxlen != -1 else f"{dtype}(MAX)"
        nullable = "NO" if col["is_nullable"] == "NO" else "SÍ"
        pk_mark = "✅" if col_name in pks else ""
        if col_name in fk_col_refs:
            rs, rt, rc = fk_col_refs[col_name]
            fk_mark = f"→ {table_link(rs, rt)}"
        else:
            fk_mark = ""
        lines.append(f"| {col_name} | {dtype} | {nullable} | {pk_mark} | {fk_mark} |")

    # Relaciones
    lines += ["", "## Relaciones", ""]
    if fk_out:
        for fk in fk_out:
            lines.append(f"- → {table_link(fk['ref_schema'], fk['ref_table'])} via `{fk['fk_column']}`")
    if fk_in:
        for fk in fk_in:
            lines.append(f"- ← {table_link(fk['fk_schema'], fk['fk_table'])} via `{fk['fk_column']}`")
    if not fk_out and not fk_in:
        lines.append("_(sin relaciones FK)_")

    # Usada en
    lines += ["", "## Usada en", ""]
    used_links = []
    for vs, vn in used_in_views:
        used_links.append(f"- {view_link(vs, vn)}")
    for ps, pn in used_in_procs:
        used_links.append(f"- {proc_link(ps, pn)}")
    if used_links:
        lines += used_links
    else:
        lines.append("_(no se encontraron referencias en views/procedures)_")

    return "\n".join(lines) + "\n"


def build_view_md(schema: str, view: str, definition: str | None, referenced_tables: list[tuple[str, str]]) -> str:
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


def build_procedure_md(schema: str, proc: str, definition: str | None, referenced_tables: list[tuple[str, str]]) -> str:
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


def build_schema_md(
    schema: str,
    tables: list[str],
    views: list[str],
    procs: list[str],
) -> str:
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


def build_index_md(
    database: str,
    schemas: list[str],
    all_tables: list[tuple[str, str]],
    all_views: list[tuple[str, str]],
    all_procs: list[tuple[str, str]],
) -> str:
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
    for ts, tn in sorted(all_tables, key=lambda x: (x[0], x[1])):
        lines.append(f"- {table_link(ts, tn)}")

    lines += ["", f"## Views ({len(all_views)})", ""]
    for vs, vn in sorted(all_views, key=lambda x: (x[0], x[1])):
        lines.append(f"- {view_link(vs, vn)}")

    lines += ["", f"## Procedures ({len(all_procs)})", ""]
    for ps, pn in sorted(all_procs, key=lambda x: (x[0], x[1])):
        lines.append(f"- {proc_link(ps, pn)}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="mssql-second-brain: genera vault Obsidian desde SQL Server"
    )
    parser.add_argument("--server",   required=True, help="Host/instancia SQL Server")
    parser.add_argument("--database", required=True, help="Nombre de la base de datos")
    parser.add_argument("--output",   required=True, help="Ruta base del vault Obsidian")
    parser.add_argument("--schemas",  default=None,  help="Schemas a incluir, separados por coma")
    parser.add_argument("--no-procedures", action="store_true", help="Excluir stored procedures")
    parser.add_argument("--no-views",      action="store_true", help="Excluir views")
    parser.add_argument("--user",     default=None, help="Usuario SQL (sin esto se usa auth integrada)")
    parser.add_argument("--password", default=None, help="Contraseña SQL (mejor usar MSSQL_PASSWORD)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.password:
        print("⚠️  Aviso: pasar contraseña por argumento es menos seguro. Considera usar MSSQL_PASSWORD.")

    allowed_schemas: set[str] | None = None
    if args.schemas:
        allowed_schemas = {s.strip() for s in args.schemas.split(",")}

    print(f"🔌 Conectando a {args.server}/{args.database}...")
    conn = connect(args.server, args.database, args.user, args.password)
    cursor = conn.cursor()

    print("📥 Extrayendo metadatos...")
    raw_columns   = fetch_all(cursor, SQL_COLUMNS)
    raw_pks       = fetch_all(cursor, SQL_PRIMARY_KEYS)
    raw_fks       = fetch_all(cursor, SQL_FOREIGN_KEYS)
    raw_views     = fetch_all(cursor, SQL_VIEWS) if not args.no_views else []
    raw_procs     = fetch_all(cursor, SQL_PROCEDURES) if not args.no_procedures else []
    raw_deps      = fetch_all(cursor, SQL_DEPENDENCIES)
    conn.close()

    # Filtrar por schema si aplica
    def schema_ok(s: str) -> bool:
        return allowed_schemas is None or s in allowed_schemas

    raw_columns = [r for r in raw_columns if schema_ok(r["table_schema"])]
    raw_pks     = [r for r in raw_pks     if schema_ok(r["table_schema"])]
    raw_fks     = [r for r in raw_fks     if schema_ok(r["fk_schema"])]
    raw_views   = [r for r in raw_views   if schema_ok(r["table_schema"])]
    raw_procs   = [r for r in raw_procs   if schema_ok(r["routine_schema"])]

    # Construir índices
    # tabla → [(col_name, data_type, is_nullable, char_max_len, ordinal)]
    table_cols: dict[str, list[dict]] = defaultdict(list)
    for r in raw_columns:
        table_cols[table_key(r["table_schema"], r["table_name"])].append(r)

    # tabla → set(pk_column_names)
    table_pks: dict[str, set[str]] = defaultdict(set)
    for r in raw_pks:
        table_pks[table_key(r["table_schema"], r["table_name"])].add(r["column_name"])

    # tabla → list(fk_out dicts)
    table_fk_out: dict[str, list[dict]] = defaultdict(list)
    for r in raw_fks:
        table_fk_out[table_key(r["fk_schema"], r["fk_table"])].append(r)

    # tabla → list(fk_in dicts)  (otras tablas que apuntan a esta)
    table_fk_in: dict[str, list[dict]] = defaultdict(list)
    for r in raw_fks:
        table_fk_in[table_key(r["ref_schema"], r["ref_table"])].append(r)

    # objeto origen → set de tablas referenciadas (schema, name)
    obj_refs_tables: dict[str, set[tuple[str, str]]] = defaultdict(set)
    # tabla destino → set de objetos que la usan (schema, name)
    table_used_by: dict[str, set[tuple[str, str, str]]] = defaultdict(set)  # key → (src_schema, src_name, type)

    # Construir sets únicos de tablas/views/procs
    tables_set: set[tuple[str, str]] = set()
    for k in table_cols:
        schema, tname = k.split(".", 1)
        tables_set.add((schema, tname))

    views_set: set[tuple[str, str]] = {(r["table_schema"], r["table_name"]) for r in raw_views}
    procs_set: set[tuple[str, str]] = {(r["routine_schema"], r["routine_name"]) for r in raw_procs}

    # Dependencias: solo para views y procs que referenci tablas que conocemos
    known_tables_lower: set[str] = {t.lower() for _, t in tables_set}
    view_names_lower: set[str] = {v.lower() for _, v in views_set}
    proc_names_lower: set[str] = {p.lower() for _, p in procs_set}

    for r in raw_deps:
        src_schema = r["src_schema"] or ""
        src_name   = r["src_name"] or ""
        ref_name   = r["ref_name"] or ""
        ref_schema = r["ref_schema"] or ""

        if ref_name.lower() not in known_tables_lower:
            continue

        src_is_view = src_name.lower() in view_names_lower
        src_is_proc = src_name.lower() in proc_names_lower

        if src_is_view or src_is_proc:
            obj_type = "view" if src_is_view else "proc"
            obj_refs_tables[f"{src_schema}.{src_name}"].add((ref_schema, ref_name))
            # Buscar schema real de la tabla referenciada
            for ts, tn in tables_set:
                if tn.lower() == ref_name.lower():
                    table_used_by[table_key(ts, tn)].add((src_schema, src_name, obj_type))
                    break

    # Separar used_by en views/procs por tabla
    def table_used_by_views_procs(tk: str):
        used_v, used_p = [], []
        for src_s, src_n, src_t in table_used_by.get(tk, set()):
            if src_t == "view":
                used_v.append((src_s, src_n))
            else:
                used_p.append((src_s, src_n))
        return used_v, used_p

    # Preparar carpetas de salida
    root = Path(args.output) / "db-second-brain"
    (root / "tables").mkdir(parents=True, exist_ok=True)
    (root / "views").mkdir(parents=True, exist_ok=True)
    (root / "procedures").mkdir(parents=True, exist_ok=True)
    (root / "schemas").mkdir(parents=True, exist_ok=True)

    file_count = 0
    all_schemas: set[str] = set()

    # --- Generar tablas ---
    print("📝 Generando notas de tablas...")
    for schema, tname in sorted(tables_set):
        all_schemas.add(schema)
        tk = table_key(schema, tname)
        cols   = table_cols.get(tk, [])
        pks    = table_pks.get(tk, set())
        fk_out = table_fk_out.get(tk, [])
        fk_in  = table_fk_in.get(tk, [])
        used_v, used_p = table_used_by_views_procs(tk)

        content = build_table_md(schema, tname, cols, pks, fk_out, fk_in, used_v, used_p)
        fname   = object_fname(schema, tname)
        (root / "tables" / f"{fname}.md").write_text(content, encoding="utf-8")
        file_count += 1

    # --- Generar views ---
    if not args.no_views:
        print("📝 Generando notas de views...")
        view_def_map = {(r["table_schema"], r["table_name"]): r["view_definition"] for r in raw_views}
        for schema, vname in sorted(views_set):
            all_schemas.add(schema)
            definition  = view_def_map.get((schema, vname))
            refs_tables = list(obj_refs_tables.get(f"{schema}.{vname}", set()))
            content     = build_view_md(schema, vname, definition, refs_tables)
            fname       = object_fname(schema, vname)
            (root / "views" / f"{fname}.md").write_text(content, encoding="utf-8")
            file_count += 1

    # --- Generar procedures ---
    if not args.no_procedures:
        print("📝 Generando notas de procedures...")
        proc_def_map = {(r["routine_schema"], r["routine_name"]): r["routine_definition"] for r in raw_procs}
        for schema, pname in sorted(procs_set):
            all_schemas.add(schema)
            definition  = proc_def_map.get((schema, pname))
            refs_tables = list(obj_refs_tables.get(f"{schema}.{pname}", set()))
            content     = build_procedure_md(schema, pname, definition, refs_tables)
            fname       = object_fname(schema, pname)
            (root / "procedures" / f"{fname}.md").write_text(content, encoding="utf-8")
            file_count += 1

    # --- Generar schemas ---
    print("📝 Generando notas de schemas...")
    schema_tables: dict[str, list[str]] = defaultdict(list)
    schema_views:  dict[str, list[str]] = defaultdict(list)
    schema_procs:  dict[str, list[str]] = defaultdict(list)
    for s, t in tables_set: schema_tables[s].append(t)
    for s, v in views_set:  schema_views[s].append(v)
    for s, p in procs_set:  schema_procs[s].append(p)

    for schema in sorted(all_schemas):
        content = build_schema_md(
            schema,
            schema_tables.get(schema, []),
            schema_views.get(schema, []),
            schema_procs.get(schema, []),
        )
        (root / "schemas" / f"{safe_name(schema)}.md").write_text(content, encoding="utf-8")
        file_count += 1

    # --- Generar _index.md ---
    print("📝 Generando _index.md...")
    index_content = build_index_md(
        args.database,
        list(all_schemas),
        list(tables_set),
        list(views_set) if not args.no_views else [],
        list(procs_set) if not args.no_procedures else [],
    )
    (root / "_index.md").write_text(index_content, encoding="utf-8")
    file_count += 1

    # --- Resumen final ---
    print()
    print(f"✅ Second Brain generado en: {root}")
    print(f"   Schemas:    {len(all_schemas)}")
    print(f"   Tablas:     {len(tables_set)}")
    print(f"   Views:      {len(views_set) if not args.no_views else 0}")
    print(f"   Procedures: {len(procs_set) if not args.no_procedures else 0}")
    print(f"   Ficheros:   {file_count}")
    print()
    print("Para generar el overview con IA, abre Copilot y escribe:")
    print('  "Genera _overview.md leyendo db-second-brain/_index.md"')


if __name__ == "__main__":
    main()
