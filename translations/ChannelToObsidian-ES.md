# ChannelToObsidian

## Propósito
Skill en dos fases para capturar un canal de YouTube completo en un Second Brain de Obsidian. Primero escanea todos los vídeos del canal generando un checklist en Markdown; después procesa únicamente los que selecciones ejecutando el pipeline completo de VideoToObsidian para cada uno.

## Estructura
- `ChannelToObsidian/SKILL.md` — definición del skill y workflow completo en dos fases
- `ChannelToObsidian/scripts/channel_to_obsidian.py` — script que obtiene todos los vídeos del canal (InnerTube browse API), construye el índice y delega en VideoToObsidian los elementos seleccionados

**Depende de:** skill `VideoToObsidian` (debe estar instalado en el directorio hermano)

## Funcionalidades principales
- Obtiene todos los vídeos del canal mediante la InnerTube browse API (sin dependencias externas, paginación incluida)
- Crea/actualiza `Atlas/Personas/<NombreCanal>.md` como checklist seleccionable
- Marcadores de estado: `[ ]` sin revisar · `[x]` seleccionado · `[p]` ya procesado
- La fase 2 llama a VideoToObsidian por cada elemento `[x]` y lo marca `[p]` al terminar
- Soporta URLs de canal: handle (`@nombre`), `/c/`, `/channel/UC…` o URL de vídeo
- Ruta del vault configurable mediante la variable de entorno `OBSIDIAN_VAULT`

## Casos de uso típicos
- Construir una base de conocimiento a partir de un canal técnico favorito
- Revisar todos los vídeos de un creador antes de decidir cuáles estudiar
- Procesar en lote un canal o playlist completo con curación selectiva
- Mantener actualizado el índice de un canal conforme se publican nuevos vídeos
