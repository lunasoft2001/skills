# PageToObsidian

Captura de una página web individual a Obsidian con gestión automática de índice de Personas.

## Quick start

```bash
python3 scripts/page_to_obsidian.py "https://example.com/articulo"
```

La página se descarga, convierte a Markdown y se guarda con su Persona index automáticamente.

## Features

- ✅ Descarga y conversión HTML → Markdown
- ✅ Extrae título, fecha, autor automáticamente
- ✅ Crea/actualiza `Atlas/Personas/<SiteName>.md`
- ✅ Compatible con WebToObsidian — ambos usan la misma Persona
- ✅ Solo stdlib Python 3.9+

## Uso

```bash
python3 scripts/page_to_obsidian.py <URL>
```

## Output

- Nota en: `Atlas/Recursos/<SiteName>/<TítuloPágina>.md`
- Persona en: `Atlas/Personas/<SiteName>.md`
- JSON emitido a stderr con metadatos

## Compatibilidad

Totalmente bidireccional con:
- **WebToObsidian** — capture sitios completos antes, después o intercalado
- **ChannelToObsidian** — mismo patrón para canales YouTube
- **VideoToObsidian** — mismo patrón para vídeos individuales

Ver `SKILL.md` para documentación completa.
