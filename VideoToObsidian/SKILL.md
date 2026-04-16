---
name: VideoToObsidian
description: "Proceso completo de captura de vídeo YouTube a nota técnica Obsidian: obtiene metadatos, descarga la transcripción (via TranscribeYoutube), analiza el contenido y genera una nota técnica completa con vídeo embebido, resumen, pasos o puntos clave, y wikilink a la transcripción. Usa cuando el usuario pida: capturar vídeo, crear nota técnica de YouTube, VideoToObsidian, documento técnico de vídeo, procesar vídeo a Obsidian."
license: MIT
author: lunasoft2001
  https://github.com/lunasoft2001
---

# VideoToObsidian

Flujo completo de captura de cualquier vídeo de YouTube a una nota técnica lista para el Second Brain en Obsidian. Combina descarga automática de metadatos + transcripción con análisis inteligente del contenido para generar el documento adecuado al tipo de vídeo.

**Depende de:** skill `TranscribeYoutube` (debe estar instalado en el directorio hermano)

---

## Cuándo usar este skill

- El usuario da una URL de YouTube y quiere una nota técnica completa
- El usuario dice "captura esto a Obsidian", "crea nota de este vídeo", "VideoToObsidian"
- El usuario quiere documentar un tutorial, concepto o demo de YouTube en su vault
- El usuario comparte un link y dice "quiero aprenderlo bien"

---

## Requisitos

- **Python 3.9+** — solo stdlib
- Skill **TranscribeYoutube** instalado en `~/.copilot/skills/TranscribeYoutube/`
- El vídeo debe tener subtítulos disponibles (automáticos o manuales)
- Variable `OBSIDIAN_VAULT` (opcional, por defecto usa el vault Luna)

---

## Comando a ejecutar

```bash
python3 ~/.copilot/skills/VideoToObsidian/scripts/video_to_obsidian.py <URL>
```

El script emite el JSON por stdout. Capturarlo así:

```bash
JSON=$(python3 ~/.copilot/skills/VideoToObsidian/scripts/video_to_obsidian.py <URL>)
```

---

## Flujo completo paso a paso

### Paso 1 — Ejecutar el script

```bash
python3 ~/.copilot/skills/VideoToObsidian/scripts/video_to_obsidian.py <URL_YouTube>
```

El script hace:
1. Llama a InnerTube API → obtiene `title`, `channel`, `description`, `duration`
2. Delega en TranscribeYoutube → crea `Atlas/Recursos/Transcripciones/VIDEO_ID - Título.md`
3. Lee el fichero de transcripción
4. Emite un JSON con todos los datos por stdout

### Paso 2 — Leer el JSON

El JSON contiene estos campos clave:

| Campo | Descripción |
|---|---|
| `title` | Título del vídeo |
| `channel` | Nombre del canal |
| `description` | Descripción del vídeo (primeros 800 chars) |
| `duration` | Duración formateada (mm:ss o h:mm:ss) |
| `url` | URL completa de YouTube |
| `embed_url` | URL para iframe embebido |
| `fecha_guardado` | Fecha de hoy |
| `wikilink_transcript` | Wikilink listo para insertar |
| `transcript_content` | Transcripción completa |
| `target_note` | Ruta donde guardar la nota principal |
| `topics` | Lista de nombres de temas detectados (ej: `["Access", "VBA"]`) |
| `topic_tags` | Lista de slugs para frontmatter (ej: `["access", "vba"]`) |
| `topic_section` | Bloque Markdown listo para insertar como `## Conexiones` |
| `persona` | Objeto con info del canal (ver abajo) |

**Objeto `persona`:**

| Campo | Descripción |
|---|---|
| `name` | Nombre del canal (ej: "Area 404") |
| `path` | Ruta completa al archivo `Atlas/Personas/NombreCanal.md` |
| `wikilink` | Wikilink listo: `[[Atlas/Personas/NombreCanal]]` |
| `created_now` | `true` si se acaba de crear, `false` si ya existía |

### Paso 2.5 — Gestión automática de Personas

El script **verifica automáticamente** si existe `Atlas/Personas/<ChannelName>.md`:

- **Si NO existe:** Crea un nuevo archivo de Persona con este vídeo marcado como `[p]` (procesado)
- **Si SÍ existe:** Agrega el vídeo al checklist existente y actualiza la sección "Notas generadas"

Esta integración permite que `VideoToObsidian` sea **totalmente compatible con `ChannelToObsidian`**:
- Descargas vídeos individuales → se registran en su Persona
- Luego descargas todo el canal → el índice ya tiene los vídeos previos como `[p]`

**Plantilla generada** (igual a `ChannelToObsidian`):

```markdown
---
tags: [atlas, persona, canal-youtube]
canal: "Nombre del Canal"
url: https://www.youtube.com/@canalhandle
updated: 2026-04-16
total-videos: 3
---

# Nombre del Canal — Índice de vídeos

## Vídeos

- [p] **Título del vídeo** · 12:34 · hoy · `VIDEO_ID`
- [ ] **Otro vídeo** · 45:12 · ayer · `OTRO_ID`

---

## Notas generadas

- [[Atlas/Recursos/Título del vídeo procesado]]
```

### Paso 3 — Detectar el tipo de contenido

Analiza `transcript_content` + `title` + `description` para clasificar el vídeo:

| Tipo | Señales en la transcripción |
|---|---|
| **TUTORIAL** | "cómo", "paso", "step", "how to", instrucciones secuenciales, checklist de acciones |
| **CONCEPTO/TEORÍA** | "qué es", "significa", "concepto", lenguaje explicativo sin pasos concretos |
| **DEMO/SHOWCASE** | muestra un producto/herramienta, "te muestro", "fíjate", sin pasos replicables |
| **CHARLA/ENTREVISTA** | conversación, preguntas y respuestas, múltiples voces, ideas sueltas |
| **REVIEW/COMPARATIVA** | evaluación, pros/contras, "me gusta", "no me gusta", puntuaciones |

### Paso 4 — Generar la nota con la plantilla correcta

Usa la plantilla del tipo detectado. **El frontmatter y el bloque de vídeo son siempre iguales:**

```markdown
---
tags: [atlas, recurso, youtube, <topic_tags separados por coma>]
url: <url>
canal: "<channel>"
persona: "<persona_wikilink>"
duracion: "<duration>"
fecha-guardado: <fecha_guardado>
temas: [<topics separados por coma entre comillas>]
---

# <title>

> 👤 Por: <persona_wikilink>
> 🎥 [ver en YouTube](<url>)
> <iframe width="100%" height="400" src="<embed_url>" allowfullscreen></iframe>
>
> 📄 Transcripción completa: <wikilink_transcript>
> 🔗 Vídeo original: [youtube.com/watch?v=<video_id>](<url>)
>
> **Resumen:** <resumen de 3-5 frases generado desde la transcripción>

---
```

> **Nota:** Si `topic_section` viene relleno en el JSON, insertarlo al final de la nota (antes de `## Fuentes` si existe, o al final). Los wikilinks `[[Atlas/Temas/...]]` conectan la nota con los hubs de temas del vault.

Luego añade las secciones según el tipo:

#### Plantilla TUTORIAL

```markdown
## Cuándo usar esto
- <caso de uso 1 extraído de la transcripción>
- <caso de uso 2>

---

## Pasos

- [ ] 1. **<acción>** — <detalle>
- [ ] 2. **<acción>** — <detalle>
- [ ] ...

---

## Consejos
- <consejo 1 extraído de la transcripción>
- <consejo 2>

---

## Fuentes consultadas
- Vídeo: [<title>](<url>) — <channel>

<topic_section>

*(Si `topic_section` está vacío en el JSON, añade aquí manualmente wikilinks a notas relacionadas del vault)*
```

#### Plantilla CONCEPTO/TEORÍA

```markdown
## Qué es
<explicación de 2-3 párrafos>

## Por qué importa
- <razón 1>
- <razón 2>

## Puntos clave
- **<concepto>**: <definición breve>
- **<concepto>**: <definición breve>

---

## Fuentes consultadas
- Vídeo: [<title>](<url>) — <channel>

<topic_section>

*(Si `topic_section` está vacío en el JSON, añade aquí manualmente wikilinks a notas relacionadas del vault)*
```

#### Plantilla DEMO/SHOWCASE

```markdown
## Qué muestra el vídeo
<descripción de lo que se demuestra>

## Aspectos destacados
- <punto 1>
- <punto 2>

## Aplicación práctica
- <cómo podría usarse en mi contexto>

---

## Fuentes consultadas
- Vídeo: [<title>](<url>) — <channel>

<topic_section>

*(Si `topic_section` está vacío en el JSON, añade aquí manualmente wikilinks a notas relacionadas del vault)*
```

#### Plantilla CHARLA/ENTREVISTA

```markdown
## Sobre qué
<contexto del guest o tema general>

## Ideas principales
- <idea 1>
- <idea 2>

## Citas destacadas
> "<cita literal de la transcripción>"

---

## Fuentes consultadas
- Vídeo: [<title>](<url>) — <channel>

<topic_section>

*(Si `topic_section` está vacío en el JSON, añade aquí manualmente wikilinks a notas relacionadas del vault)*
```

### Paso 5 — Guardar la nota

Guarda la nota generada en la ruta `target_note` del JSON.  
Si ya existe un fichero con ese nombre, **pregunta al usuario** si sobreescribir.

### Paso 6 — Abrir en Obsidian

```python
import subprocess, platform, os
vault    = "<vault del JSON>"
rel_path = "<ruta relativa dentro del vault>"
if platform.system() == "Darwin":
    os.system(f'open "obsidian://open?vault={os.path.basename(vault)}&file={rel_path}"')
```

O simplemente ejecuta:
```bash
open "obsidian://open?vault=Luna&file=Atlas/Recursos/<safe_title>"
```

---

## Convenciones

- **Nombre del fichero**: título del vídeo limpio, máx 60 caracteres, sin caracteres especiales
- **Ubicación**: `VAULT/Atlas/Recursos/<Título>.md`
- **Transcripción**: `VAULT/Atlas/Recursos/Transcripciones/<VIDEO_ID> - <Título>.md` (generada por TranscribeYoutube)
- **Tags de tema**: infiere del título + descripción (p.ej. `affinity-photo`, `python`, `ia`)

---

## Notas

- El script puede tardar 5-15 segundos (InnerTube + descarga de transcripción)
- Si el vídeo no tiene subtítulos disponibles, se crea la nota sin transcripción y sin wikilink de transcripción
- El campo `transcript_found: false` en el JSON indica que no hay transcripción
- En ese caso, genera la nota con el resumen basado en `description` solamente
- **Nuevo:** El script maneja automáticamente `Atlas/Personas/<ChannelName>.md`:
  - Si no existe, lo crea con este vídeo marcado como `[p]`
  - Si ya existe, lo actualiza agregando el vídeo al checklist
  - Totalmente compatible con `ChannelToObsidian` — puede ejecutarse antes, después o intercalado
