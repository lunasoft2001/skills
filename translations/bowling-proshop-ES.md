# Bowling Pro Shop — Virtual Ball Driller & Lane Coach

Este documento describe el contenido del skill `bowling-proshop` en este repositorio.

## Descripción

Coach virtual de bowling especializado en selección de bola y layouts **Dual Angle** (estilo Mo Pinel). Realiza consultas interactivas en fases para recopilar el perfil del jugador y genera un **reporte visual HTML** completo con imagen real de la bola, diagrama de pista, drill de la bola y análisis de layout.

Activadores: `qué bola uso`, `layout`, `patrón de aceite`, `taladrado`, `rev rate`, `PAP`, `Dual Angle`, `selección de bola`, `ajustes en pista`.

## Estructura

```text
bowling-proshop/
  SKILL.md                          # Instrucciones del skill para GitHub Copilot
  assets/
    logo.jpeg                       # Logo LunaBowling para el reporte HTML
  references/
    ball-selection.md               # Heurísticas de selección de cover/categoría
    current-balls-2026.md           # Catálogo de bolas actuales (2025-2026) con slugs verificados
    dual-angle.md                   # Sistema de layout Dual Angle completo (Mo Pinel)
    manufacturers.md                # URLs de fabricantes para búsqueda de specs
    patterns-reference.md           # Patrones de aceite: house, sport, challenge
    player-types.md                 # Clasificación speed/rev dominance, PAP, track
  scripts/
    generate_bowling_report_v2.py   # Generador de reportes HTML visuales
```

## Consulta interactiva

El skill usa cuatro fases de preguntas mediante `vscode_askQuestions`:

1. **Fase 1** — Mano dominante, tipo de pista, objetivo
2. **Fase 2** — Velocidad, rev rate, PAP/track
3. **Fase 3** — Superficie de pista, agarre, arsenal actual
4. **Fase 4** — Reporte visual (nombre del jugador)

## Reporte visual HTML

Al finalizar la consulta, el skill genera un reporte HTML con:

- Card de la bola con imagen real obtenida del catálogo del fabricante
- Diagrama SVG de pista top-down con línea de juego
- Diagrama SVG de drill (pin, PAP, mass bias, agujeros)
- Layout Dual Angle detallado con explicación en lenguaje natural
- Ajustes en pista y datos a refinar

```bash
python3 scripts/generate_bowling_report_v2.py \
  --data /tmp/bowling_data.json \
  --output ~/Desktop/bowling_report.html

# O con datos de ejemplo:
python3 scripts/generate_bowling_report_v2.py --example
```

## Instalación

Copia la carpeta al directorio de skills de GitHub Copilot:

```bash
# macOS / Linux
cp -r bowling-proshop ~/.copilot/skills/bowling-proshop

# Windows (PowerShell)
Copy-Item -Path "bowling-proshop" -Destination "$env:USERPROFILE\.copilot\skills\bowling-proshop" -Recurse
```

Luego reinicia VS Code.

## Requisitos

- Python 3.11+
- Conectividad a internet (para obtener imágenes del catálogo del fabricante)
- Sin dependencias externas — usa únicamente la biblioteca estándar de Python

## Notas

- Solo recomienda bolas listadas en `references/current-balls-2026.md` (bolas activas en catálogo, no descatalogadas).
- Las imágenes de bolas Storm se obtienen directamente del catálogo oficial mediante slugs verificados (`KNOWN_SLUG_MAP` en el script).
- El cálculo de layout Dual Angle sigue el sistema Mo Pinel: DA × Pin-to-PAP × VAL.
- Compatible con jugadores de una y dos manos, diestros y zurdos.
