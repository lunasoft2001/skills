# mssql-second-brain — Second Brain de SQL Server para Obsidian

## Descricao

Skill publico que gera um vault de conhecimento completo no Obsidian a partir de metadados do SQL Server. Extrai schemas, tabelas, views, procedures e relacoes usando script Python local (`pyodbc`) com 0 tokens de IA durante a extracao.

Etapa opcional com IA: criar `_overview.md` a partir de `_index.md` apos a geracao.

## Estrutura

```text
mssql-second-brain/
  SKILL.md
  scripts/
    generate_second_brain.py
```

## Principais funcionalidades

- Extracao de metadados SQL Server via `INFORMATION_SCHEMA` + `sys.*`
- Uma nota Markdown por schema/tabela/view/procedure
- Frontmatter YAML + wikilinks + referencias reversas ("Usado por")
- Estrutura pronta para Obsidian e visualizacao em grafo
- Arquivo conceitual opcional gerado por IA

## Casos de uso

- Onboarding de novos desenvolvedores
- Documentacao viva de arquitetura de banco de dados
- Base de conhecimento interna pesquisavel
- Analise de dependencias de tabelas e topologia de FKs

## Requisitos

- Python 3
- `pyodbc`
- Acesso de rede ao SQL Server
