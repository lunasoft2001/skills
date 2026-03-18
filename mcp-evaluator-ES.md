# MCP Evaluator — Auditoría de Servidores MCP: Seguridad, Privacidad y Calidad

Este documento describe el skill `mcp-evaluator` de este repositorio.

## Descripción

Skill que audita servidores MCP (Model Context Protocol) en seguridad, privacidad y calidad técnica. Analiza código fuente (TypeScript/Python), definiciones de tools, archivos de configuración y SKILL.md companion. Produce un informe estructurado PASS/PARTIAL/FAIL con correcciones accionables.

Disparadores: `auditar MCP`, `evaluar servidor MCP`, `revisar seguridad MCP`, `revisar tools MCP`, `mi MCP es seguro`, `MCP listo para publicar`.

## Estructura

```text
mcp-evaluator/
  SKILL.md                              # Instrucciones + flujo de evaluación en 3 fases
  references/
    mcp-rai-checklist.md               # Criterios de seguridad y privacidad (RAI + OWASP)
    mcp-quality-checklist.md           # Criterios de calidad técnica
```

## Funcionalidades

- **Fase 1 — Seguridad y Privacidad**: credenciales, PII, operaciones destructivas, inyección/SSRF, tokens
- **Fase 2 — Calidad Técnica**: diseño de tools, manejo de errores, skill companion, dependencias, logging
- **Fase 3 — Responsabilidad**: licencia, repo, versiones, mantenedor
- Genera informe Markdown con secciones puntuadas (PASS / PARTIAL / FAIL)
- Veredicto global: `SAFE TO USE` / `NEEDS FIXES` / `SECURITY RISK`

## Cómo usarlo

1. Instala el skill (ver abajo)
2. Abre el chat de GitHub Copilot
3. Escribe: `"Audita mi MCP de LinkedIn para seguridad"` — Copilot leerá el código fuente y generará el informe completo

## Instalación del skill

```bash
# macOS / Linux
cp -r mcp-evaluator ~/.copilot/skills/mcp-evaluator
```

Luego reinicia VS Code.

## Requisitos

- VS Code con GitHub Copilot
- Acceso al código fuente del servidor MCP a evaluar
