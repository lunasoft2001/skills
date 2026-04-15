# VideoToObsidian

## Propósito
Pipeline completo para capturar un vídeo de YouTube como nota técnica estructurada en Obsidian. Combina descarga automática de metadatos y transcripción con análisis inteligente del contenido para generar el documento adecuado según el tipo de vídeo.

## Estructura
- `VideoToObsidian/SKILL.md` — definición del skill y flujo paso a paso completo
- `VideoToObsidian/scripts/video_to_obsidian.py` — script que obtiene metadatos, delega la transcripción en TranscribeYoutube y emite un JSON para Copilot

**Depende de:** skill `TranscribeYoutube` (debe estar instalado en el directorio hermano)

## Características principales
- Obtiene metadatos del vídeo vía InnerTube API (título, canal, descripción, duración)
- Delega la transcripción en el skill `TranscribeYoutube`
- Detecta el tipo de contenido: TUTORIAL / CONCEPTO / DEMO / CHARLA
- Aplica la plantilla de nota correspondiente (checklist de pasos, puntos clave, citas…)
- Genera una nota Obsidian completa con vídeo embebido, resumen y wikilink a la transcripción
- Abre la nota en Obsidian automáticamente (macOS / Windows / Linux)
- Ruta del vault configurable vía variable de entorno `OBSIDIAN_VAULT`

## Casos de uso típicos
- Capturar un tutorial de YouTube como nota de referencia con pasos
- Convertir un vídeo conceptual en una entrada estructurada del Second Brain
- Documentar una demo o showcase de software
- Archivar una charla o entrevista con las ideas clave resaltadas
