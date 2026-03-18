# Bowling Pro Shop — Furador de Bola Virtual & Coach de Pista

Este documento descreve o conteudo do skill `bowling-proshop` neste repositorio.

## Descricao

Um furador de bola de bowling virtual e coach de pista especializado em selecao de bola e **layouts Dual Angle** (metodo Mo Pinel). Conduz consultas interativas em multiplas fases para construir o perfil do jogador e gera um **relatorio HTML visual completo** com imagem real da bola, diagrama de pista, diagrama de furacaoamento e analise de layout.

Palavras-chave: `selecao de bola`, `layout`, `padrao de oleo`, `furacaoamento`, `rev rate`, `PAP`, `Dual Angle`, `potencial de hook`, `ajustes na pista`.

## Estrutura

```text
bowling-proshop/
  SKILL.md                          # Instrucoes do skill para o GitHub Copilot
  assets/
    logo.jpeg                       # Logo LunaBowling para o relatorio HTML
  references/
    ball-selection.md               # Heuristicas de selecao de cover/categoria
    current-balls-2026.md           # Catalogo de bolas atuais (2025-2026) com slugs verificados
    dual-angle.md                   # Sistema Dual Angle completo (Mo Pinel)
    manufacturers.md                # URLs dos fabricantes para busca de specs
    patterns-reference.md           # Padroes de oleo: house, sport, challenge
    player-types.md                 # Classificacao speed/rev dominance, PAP, track
  scripts/
    generate_bowling_report_v2.py   # Gerador de relatorios HTML visuais
```

## Consulta interativa

O skill usa quatro fases via `vscode_askQuestions`:

1. **Fase 1** — Mao dominante, tipo de pista, objetivo
2. **Fase 2** — Velocidade da bola, rev rate, PAP/track
3. **Fase 3** — Superficie da pista, aderencia, arsenal atual
4. **Fase 4** — Relatorio visual (nome do jogador)

## Relatorio HTML visual

Ao final da consulta, o skill gera um relatorio HTML com:

- Card da bola com imagem real obtida do catalogo do fabricante
- Diagrama SVG da pista vista de cima com a linha de jogo recomendada
- Diagrama SVG de furacaoamento (pin, PAP, mass bias, furos)
- Layout Dual Angle com explicacao em linguagem natural
- Ajustes na pista e dados a refinar

```bash
python3 scripts/generate_bowling_report_v2.py \
  --data /tmp/bowling_data.json \
  --output ~/Desktop/bowling_report.html

# Ou com dados de exemplo:
python3 scripts/generate_bowling_report_v2.py --example
```

## Instalacao

Copie a pasta para o diretorio de skills do GitHub Copilot:

```bash
# macOS / Linux
cp -r bowling-proshop ~/.copilot/skills/bowling-proshop

# Windows (PowerShell)
Copy-Item -Path "bowling-proshop" -Destination "$env:USERPROFILE\.copilot\skills\bowling-proshop" -Recurse
```

Em seguida, reinicie o VS Code.

## Requisitos

- Python 3.11+
- Conexao com a internet (para imagens de bolas do catalogo do fabricante)
- Sem dependencias externas — usa apenas a biblioteca padrao do Python

## Notas

- Recomenda apenas bolas listadas em `references/current-balls-2026.md` (catalogo ativo, sem bolas descontinuadas).
- Imagens de bolas Storm sao obtidas via slugs verificados (`KNOWN_SLUG_MAP` no script) — sem adivinhacao.
- O sistema de layout Dual Angle segue Mo Pinel: DA × Pin-to-PAP × VAL.
- Compativel com jogadores de uma e duas maos, destros e canhotos.
