# mssql-second-brain — Second Brain de SQL Server para Obsidian

## Descripción

Skill público que genera un vault de conocimiento completo en Obsidian a partir de metadatos de SQL Server. Extrae schemas, tablas, vistas, procedimientos y relaciones usando un script Python local (`pyodbc`) con 0 tokens de IA durante la extracción.

Paso opcional con IA: crear `_overview.md` leyendo `_index.md` al finalizar.

## Estructura

```text
mssql-second-brain/
  SKILL.md
  scripts/
    generate_second_brain.py
```

## Funcionalidades principales

- Extracción de metadatos SQL Server desde `INFORMATION_SCHEMA` + `sys.*`
- Una nota Markdown por schema/tabla/vista/procedimiento
- Frontmatter YAML + wikilinks + referencias inversas ("Usada en")
- Estructura lista para Obsidian y su grafo
- Archivo conceptual opcional generado por IA

## Casos de uso

- Onboarding técnico de nuevas personas en el equipo
- Documentación viva de arquitectura de base de datos
- Base de conocimiento interna buscable
- Trazabilidad de dependencias y topología de claves foráneas

## Requisitos

- Python 3
- `pyodbc`
- Acceso de red al SQL Server
