---
name: mssql-second-brain
description: >
  Genera un vault Obsidian con el Second Brain completo de una base de datos SQL Server.
  Conecta vía MCP mssql o pyodbc, extrae metadatos con INFORMATION_SCHEMA + sys.*,
  y crea .md con frontmatter YAML, tablas de columnas, wikilinks de FK y "Usada en".
  0 tokens en generación — script Python local. IA opcional solo para _overview.md (MOC).
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
  - read_file
---

# Skill: mssql-second-brain

Genera automáticamente un vault Obsidian con la estructura completa de una base de datos SQL Server como un Second Brain navegable. El script Python no llama a ninguna IA — 0 tokens durante la generación.

## Cuándo activarse

Activar cuando el usuario mencione cualquiera de:
- "second brain", "mssql second brain", "SQL Server vault"
- "generar documentación de la BD", "mapear base de datos"
- "crear vault de SQL Server", "exportar estructura a Obsidian"
- "mssql-second-brain"

---

## Flujo de ejecución

### Paso 1 — Recopilar parámetros

Preguntar al usuario los siguientes parámetros si no los ha proporcionado:

**Requeridos:**
- `server`: host o instancia SQL Server (ej: `localhost`, `192.168.1.1\SQLEXPRESS`)
- `database`: nombre de la base de datos
- `output_dir`: ruta de la carpeta Obsidian donde crear el vault (ej: `/Users/yo/vault/`)

**Opcionales** (si no se indican, usar defaults):
- `schemas`: lista de schemas a incluir, separada por comas (defecto: todos)
- `include_procedures`: incluir stored procedures, true/false (defecto: true)
- `include_views`: incluir views, true/false (defecto: true)
- `user`: usuario SQL (si no se indica, se usa autenticación Windows/integrada)
- `password`: contraseña (preferible via variable de entorno `MSSQL_PASSWORD`)

### Paso 2 — Verificar dependencias

Ejecutar en terminal:
```bash
python -c "import pyodbc; print('pyodbc OK')"
```

Si falla, indicar al usuario:
```
pip install pyodbc
```
En macOS también puede ser necesario: `brew install unixodbc`

### Paso 3 — Crear/localizar el script

El script `generate_second_brain.py` está en la misma carpeta que este SKILL.md:
`{ruta_de_este_skill}/scripts/generate_second_brain.py`

### Paso 4 — Ejecutar el script

```bash
python generate_second_brain.py \
  --server "{server}" \
  --database "{database}" \
  --output "{output_dir}" \
  [--schemas "dbo,hr"] \
  [--no-procedures] \
  [--no-views] \
  [--user "sa"] \
  [--password "xxx"]
```

El script genera la carpeta `db-second-brain/` dentro de `output_dir` e imprime un resumen al terminar.

### Paso 5 — Overview IA (opcional)

Tras la generación, preguntar:
> "¿Deseas que genere un archivo `_overview.md` con un mapa conceptual de la base de datos? (solo necesito leer `_index.md`)"

Si el usuario dice sí:
1. Leer el fichero `{output_dir}/db-second-brain/_index.md`
2. Generar `_overview.md` con:
   - Descripción general de la BD deducida de nombres de tablas/schemas
   - Agrupaciones temáticas de tablas (ej: tablas de clientes, de productos, de facturación)
   - Relaciones clave entre módulos
   - Sugerencias de tablas "centrales" por número de FK entrantes
3. Guardar en `{output_dir}/db-second-brain/_overview.md`

---

## Estructura del vault generado

```
{output_dir}/
└── db-second-brain/
    ├── _index.md              ← stats globales + links a todo
    ├── _overview.md           ← opcional, generado por IA
    ├── schemas/
    │   └── {schema}.md
    ├── tables/
    │   └── {tabla}.md
    ├── views/
    │   └── {vista}.md
    └── procedures/
        └── {procedure}.md
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

---

## Notas de seguridad

- **No hardcodear credenciales**. Usar `--user`/`--password` solo en dev local.
- En producción, usar variable de entorno `MSSQL_PASSWORD`.
- El script nunca escribe credenciales en los ficheros `.md` generados.

---

## Versiones

- **v1.0**: generación única completa (este skill)
- **v2.0** (futuro): incremental con `_manifest.json` y detección de cambios
