# TranscribeYoutube

Skill para generar notas de transcripción completas en Obsidian a partir de vídeos de YouTube.

## Propósito

Descarga la transcripción completa de cualquier vídeo de YouTube y la guarda como una nota `.md` lista para Obsidian con frontmatter YAML y timestamps clicables — directamente desde VS Code, sin dependencias externas.

## Estructura

```text
TranscribeYoutube/
  SKILL.md
  scripts/
    transcribe_youtube.py
```

## Funcionalidades principales

- Usa la InnerTube Player API de YouTube (cliente iOS) — sin API keys, sin yt-dlp
- Cero dependencias externas: solo Python 3.9+ estándar
- Genera frontmatter YAML con metadatos del vídeo
- Agrupa líneas de transcripción cada 30 segundos (igual que el plugin YTranscript)
- Timestamps clicables que abren el vídeo en el segundo exacto
- Cross-platform: macOS, Windows, Linux
- Abre Obsidian automáticamente en la nota creada
- Ruta del vault configurable con la variable de entorno `OBSIDIAN_VAULT`

## Casos de uso

- Capturar un tutorial de YouTube en tu Second Brain
- Generar una nota de transcripción y enlazarla desde la nota de recurso principal
- Archivar contenido de vídeo para referencia offline
- Crear una base de conocimiento buscable a partir de vídeos formativos
