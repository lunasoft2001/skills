---
name: mssql-second-brain
description: >
  Genera un vault Obsidian con el Second Brain completo de una base de datos SQL Server.
  Usa las herramientas MCP de mssql (mssql_connect, mssql_run_query, mssql_list_databases,
  mssql_list_servers) para extraer metadatos con INFORMATION_SCHEMA + sys.*, vuelca el resultado
  a un único metadata.json con create_file, y delega la generación de todos los .md a un script
  Python local (0 tokens en generación). IA opcional solo para _overview.md (MOC).
triggers:
  - second brain
  - SQL Server vault
  - mssql second brain
  - generar documentación de la BD
  - mapear base de datos
  - crear vault de SQL Server
  - exportar estructura a Obsidian
  - mssql-second-brain
tools:
  - create_file
  - run_in_terminal
  - mssql_connect
  - mssql_run_query
  - mssql_list_servers
  - mssql_list_databases
---

# Skill: mssql-second-brain

Genera automáticamente un vault Obsidian con la estructura completa de una base de datos SQL Server como un Second Brain navegable.

**Arquitectura híbrida (mínimo uso de IA):**
1. La IA extrae metadatos vía MCP mssql y escribe **un único** `metadata.json`.
2. Un script Python local lee el JSON y genera todos los `.md` — **0 tokens** en esta fase.
3. La IA solo vuelve a intervenir si el usuario pide el `_overview.md` opcional.

No requiere pyodbc ni driver ODBC — la conexión va íntegramente por MCP.

## Cuándo activarse

Activar cuando el usuario mencione cualquiera de:
- "second brain", "mssql second brain", "SQL Server vault"
- "generar documentación de la BD", "mapear base de datos"
- "crear vault de SQL Server", "exportar estructura a Obsidian"
- "mssql-second-brain"

---

## Flujo de ejecución

### Paso 1 — Recopilar parámetros

Preguntar al usuario los parámetros que no haya proporcionado:

**Requeridos:**
- `database`: nombre de la base de datos a documentar
- `output_dir`: ruta absoluta donde crear el vault (ej: `/workspaces/proyecto/vault/`)

**Opcionales** (usar defaults si no se indican):
- `schemas`: schemas a incluir separados por coma (defecto: todos)
- `include_procedures`: incluir stored procedures (defecto: true)
- `include_views`: incluir views (defecto: true)

### Paso 2 — Conectar vía MCP

1. Llamar a `mssql_list_servers` para listar perfiles disponibles.
2. Si hay un solo servidor usarlo directamente; si hay varios, preguntar al usuario.
3. Llamar a `mssql_connect` con el perfil elegido para obtener `connectionId`.
4. Llamar a `mssql_list_databases` con `connectionId` y confirmar que `database` existe.

### Paso 3 — Extraer metadatos con mssql_run_query

Ejecutar las siguientes queries con `mssql_run_query` (`connectionId` + `database`).

#### 3.1 Columnas
```sql
SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE,
       IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH, ORDINAL_POSITION
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
```

#### 3.2 Claves primarias
```sql
SELECT tc.TABLE_SCHEMA, tc.TABLE_NAME, kcu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
  ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
 AND tc.TABLE_SCHEMA    = kcu.TABLE_SCHEMA
 AND tc.TABLE_NAME      = kcu.TABLE_NAME
WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
```

#### 3.3 Claves foráneas
```sql
SELECT
  fk.name                                                       AS fk_name,
  OBJECT_SCHEMA_NAME(fk.parent_object_id)                       AS fk_schema,
  OBJECT_NAME(fk.parent_object_id)                              AS fk_table,
  COL_NAME(fkc.parent_object_id, fkc.parent_column_id)          AS fk_column,
  OBJECT_SCHEMA_NAME(fk.referenced_object_id)                   AS ref_schema,
  OBJECT_NAME(fk.referenced_object_id)                          AS ref_table,
  COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id)  AS ref_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
```

#### 3.4 Views (omitir si `include_views = false`)
```sql
SELECT TABLE_SCHEMA, TABLE_NAME, VIEW_DEFINITION
FROM INFORMATION_SCHEMA.VIEWS
ORDER BY TABLE_SCHEMA, TABLE_NAME
```

#### 3.5 Stored Procedures (omitir si `include_procedures = false`)
```sql
SELECT ROUTINE_SCHEMA, ROUTINE_NAME, ROUTINE_DEFINITION
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_TYPE = 'PROCEDURE'
ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
```

#### 3.6 Dependencias
```sql
SELECT
  OBJECT_SCHEMA_NAME(referencing_id)  AS src_schema,
  OBJECT_NAME(referencing_id)         AS src_name,
  referenced_schema_name              AS ref_schema,
  referenced_entity_name              AS ref_name
FROM sys.sql_expression_dependencies
WHERE referenced_entity_name IS NOT NULL
```

### Paso 4 — Volcar a metadata.json (UNA sola llamada a create_file)

Con todos los resultados en memoria, construir el siguiente JSON y escribirlo en
`{output_dir}/metadata.json` con **una única llamada a `create_file`**:

```json
{
  "database": "{database}",
  "generated": "{fecha_hoy_ISO}",
  "columns":      [ ...filas de query 3.1... ],
  "primary_keys": [ ...filas de query 3.2... ],
  "foreign_keys": [ ...filas de query 3.3... ],
  "views":        [ ...filas de query 3.4... ],
  "procedures":   [ ...filas de query 3.5... ],
  "dependencies": [ ...filas de query 3.6... ]
}
```

Cada fila es un objeto con las mismas claves que los nombres de columna de la query (en minúsculas).

### Paso 5 — Ejecutar el script Python local

El script `generate_from_json.py` se encuentra en la misma carpeta que este SKILL.md:
`.github/skills/mssql-second-brain/scripts/generate_from_json.py`

Ejecutar en terminal:
```bash
python3 .github/skills/mssql-second-brain/scripts/generate_from_json.py \
  --metadata "{output_dir}/metadata.json" \
  --output   "{output_dir}" \
  [--schemas "dbo,hr"] \
  [--no-procedures] \
  [--no-views]
```

El script genera la carpeta `db-second-brain/` dentro de `output_dir` e imprime un resumen al terminar. La IA no interviene en este paso.

### Paso 6 — Overview IA (opcional)

Tras la generación, preguntar:
> "¿Deseas que genere un `_overview.md` con un mapa conceptual de la base de datos?"

Si el usuario dice sí, leer `{output_dir}/db-second-brain/_index.md` y generar
`{output_dir}/db-second-brain/_overview.md` con:
- Descripción general deducida de nombres de tablas/schemas
- Agrupaciones temáticas (usuarios, documentos, auditoría, etc.)
- Relaciones clave entre módulos
- Tablas "centrales" por número de FK entrantes

---

## Estructura del vault generado

```
{output_dir}/
├── metadata.json              ← datos crudos extraídos por MCP (borrable tras generación)
└── db-second-brain/
    ├── _index.md              ← stats globales + links a todo
    ├── _overview.md           ← opcional, generado por IA
    ├── schemas/
    │   └── {schema}.md
    ├── tables/
    │   └── {tabla}.md
    ├── views/
    │   └── {vista}.md
    ├── procedures/
    │   └── {procedure}.md
    └── bases/
        ├── all-tables.base         ← todas las tablas (table + cards view)
        ├── tables-no-pk.base       ← tablas sin Primary Key
        ├── tables-with-fk.base     ← tablas con Foreign Keys
        ├── all-views.base          ← todas las vistas (table + cards view)
        ├── all-procedures.base     ← todos los stored procedures (table + cards view)
        └── db-overview.base        ← todos los objetos agrupados por tipo
```

---

## Contenido de las notas generadas

### `tables/{tabla}.md`
- Frontmatter YAML: `type`, `schema`, `table`, `columns`, `has_pk`, `has_fk`, `tags`, `created`
- Tabla de columnas: nombre, tipo, nullable, PK, FK con wikilink
- Sección Relaciones: FK salientes (→) y entrantes (←) con wikilinks
- Sección "Usada en": views y procedures que referencian esta tabla

### `views/{vista}.md`
- Frontmatter YAML: `type`, `schema`, `view`, `tags`, `created`
- Tablas que usa (wikilinks)
- Definición SQL (extracto primeras 20 líneas)

### `procedures/{proc}.md`
- Frontmatter YAML: `type`, `schema`, `procedure`, `tags`, `created`
- Tablas que referencia (wikilinks)
- Definición SQL (extracto primeras 20 líneas)

### `schemas/{schema}.md`
- Resumen del schema: total tablas, views, procedures
- Índice con wikilinks a todos los objetos del schema

### `_index.md`
- Stats globales de la BD
- Índice completo con wikilinks a todos los objetos

### `bases/*.base` (Obsidian Bases)
Archivos `.base` con queries vivas que filtran por el frontmatter `type` de los `.md`:

| Archivo | Filtro | Vistas |
|---------|--------|--------|
| `all-tables.base` | `type == "db-table"` | table + cards |
| `tables-no-pk.base` | `type == "db-table"` + `has_pk == false` | table |
| `tables-with-fk.base` | `type == "db-table"` + `has_fk == true` | table |
| `all-views.base` | `type == "db-view"` | table + cards |
| `all-procedures.base` | `type == "db-procedure"` | table + cards |
| `db-overview.base` | tablas + vistas + procedures | table agrupado por tipo |

> **Requiere:** Obsidian con el core plugin **Bases** activado.

---

## Notas de seguridad

- Las credenciales se gestionan en el perfil de conexión MCP, nunca se hardcodean.
- El agente nunca escribe credenciales en los ficheros `.md` ni en `metadata.json`.

---

## Versiones

- **v1.0**: pyodbc + script Python completo (requería ODBC driver)
- **v2.0**: MCP + agente genera todos los .md (uso alto de tokens)
- **v3.0**: MCP extrae → metadata.json → script Python genera .md (mínimo uso de IA)
- **v3.1**: Añadidos archivos `.base` (Obsidian Bases) en carpeta `bases/`
