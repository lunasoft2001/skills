---
name: VideoToObsidian
description: "Complete pipeline to capture a YouTube video into a structured Obsidian technical note: fetches metadata, downloads the transcript (via TranscribeYoutube), analyzes content, and generates a full technical note with embedded video, summary, steps or key points, and a wikilink to the transcript. Use when the user asks to capture a video, create a technical note from YouTube, VideoToObsidian, technical doc from video, or process a video to Obsidian."
license: MIT
author: lunasoft2001
  https://github.com/lunasoft2001
---

# VideoToObsidian

Complete pipeline to capture any YouTube video into a technical note ready for an Obsidian Second Brain. Combines automatic metadata and transcript download with intelligent content analysis to produce the right document for the video type.

**Depends on:** skill `TranscribeYoutube` (must be installed in the sibling directory)

---

## When to use this skill

- The user provides a YouTube URL and wants a complete technical note
- The user says "capture this to Obsidian", "create a note from this video", "VideoToObsidian"
- The user wants to document a tutorial, concept, or demo from YouTube in their vault
- The user shares a link and says "I want to study this properly"

---

## Requirements

- **Python 3.9+** — stdlib only, no external dependencies
- Skill **TranscribeYoutube** installed at `~/.copilot/skills/TranscribeYoutube/`
- The video must have subtitles available (auto-generated or manual)
- `OBSIDIAN_VAULT` environment variable (optional — defaults to `~/Documents/Obsidian/MyVault`)

---

## Command to run

```bash
python3 ~/.copilot/skills/VideoToObsidian/scripts/video_to_obsidian.py <URL>
```

Capture the JSON output:

```bash
JSON=$(python3 ~/.copilot/skills/VideoToObsidian/scripts/video_to_obsidian.py <URL>)
```

---

## Full workflow step by step

### Step 1 — Run the script

```bash
python3 ~/.copilot/skills/VideoToObsidian/scripts/video_to_obsidian.py <YouTube_URL>
```

The script does:
1. Calls InnerTube API → fetches `title`, `channel`, `description`, `duration`
2. Delegates to TranscribeYoutube → creates `Atlas/Recursos/Transcripciones/VIDEO_ID - Title.md`
3. Reads the generated transcript file
4. Emits a JSON payload with all data via stdout

### Step 2 — Read the JSON

Key fields in the JSON output:

| Field | Description |
|---|---|
| `title` | Video title |
| `channel` | Channel name |
| `description` | Video description (first 800 chars) |
| `duration` | Formatted duration (mm:ss or h:mm:ss) |
| `url` | Full YouTube URL |
| `embed_url` | URL for iframe embed |
| `fecha_guardado` | Today's date |
| `wikilink_transcript` | Ready-to-paste wikilink |
| `transcript_content` | Full transcript text |
| `target_note` | Full path where the main note should be saved |

### Step 3 — Detect content type

Analyze `transcript_content` + `title` + `description` to classify the video:

| Type | Signals in the transcript |
|---|---|
| **TUTORIAL** | "how to", "step", sequential instructions, actionable checklist |
| **CONCEPT/THEORY** | "what is", "means", explanatory language, no concrete steps |
| **DEMO/SHOWCASE** | shows a product/tool, "let me show you", "look at this", not easily replicable |
| **TALK/INTERVIEW** | conversation, Q&A, multiple voices, loose ideas |
| **REVIEW/COMPARISON** | evaluation, pros/cons, "I like", "I don't like", ratings |

### Step 4 — Generate the note with the right template

The frontmatter and video block are always the same:

```markdown
---
tags: [atlas, resource, <topic-tag>]
url: <url>
channel: "<channel>"
duration: "<duration>"
date-saved: <fecha_guardado>
---

# <title>

> 🎥 **<channel>** — [watch on YouTube](<url>)
> <iframe width="100%" height="400" src="<embed_url>" allowfullscreen></iframe>
>
> 📄 Full transcript: <wikilink_transcript>
> 🔗 Original video: [youtube.com/watch?v=<video_id>](<url>)
>
> **Summary:** <3-5 sentence summary generated from the transcript>

---
```

Then add sections based on content type:

#### TUTORIAL template

```markdown
## When to use this
- <use case 1 extracted from transcript>
- <use case 2>

---

## Steps

- [ ] 1. **<action>** — <detail>
- [ ] 2. **<action>** — <detail>
- [ ] ...

---

## Tips
- <tip 1 from transcript>
- <tip 2>

---

## Sources
- Video: [<title>](<url>) — <channel>

## Connections
- [[...]] — <reason for the link>
```

#### CONCEPT/THEORY template

```markdown
## What it is
<2-3 paragraph explanation>

## Why it matters
- <reason 1>
- <reason 2>

## Key points
- **<concept>**: <brief definition>
- **<concept>**: <brief definition>

---

## Sources
- Video: [<title>](<url>) — <channel>

## Connections
- [[...]] — <reason for the link>
```

#### DEMO/SHOWCASE template

```markdown
## What the video shows
<description of what is demonstrated>

## Highlights
- <point 1>
- <point 2>

## Practical application
- <how this could be used in my context>

---

## Sources
- Video: [<title>](<url>) — <channel>

## Connections
- [[...]] — <reason for the link>
```

#### TALK/INTERVIEW template

```markdown
## About
<context about the speaker or topic>

## Main ideas
- <idea 1>
- <idea 2>

## Notable quotes
> "<literal quote from transcript>"

---

## Sources
- Video: [<title>](<url>) — <channel>

## Connections
- [[...]] — <reason for the link>
```

### Step 5 — Save the note

Save the generated note at the `target_note` path from the JSON.  
If a file with that name already exists, **ask the user** whether to overwrite.

### Step 6 — Open in Obsidian

```bash
open "obsidian://open?vault=<vault_name>&file=Atlas/Recursos/<safe_title>"
```

---

## Conventions

- **File name**: cleaned video title, max 60 characters, no special characters
- **Location**: `VAULT/Atlas/Resources/<Title>.md`
- **Transcript**: `VAULT/Atlas/Resources/Transcriptions/<VIDEO_ID> - <Title>.md` (generated by TranscribeYoutube)
- **Topic tags**: infer from title + description (e.g. `affinity-photo`, `python`, `ai`)

---

## Notes

- The script may take 5–15 seconds (InnerTube API + transcript download)
- If the video has no subtitles, the note is created without a transcript or transcript wikilink
- `transcript_found: false` in the JSON indicates no transcript available — generate the note summary from `description` only


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
tags: [atlas, recurso, <tag-tema>]
url: <url>
canal: "<channel>"
duracion: "<duration>"
fecha-guardado: <fecha_guardado>
---

# <title>

> 🎥 **<channel>** — [ver en YouTube](<url>)
> <iframe width="100%" height="400" src="<embed_url>" allowfullscreen></iframe>
>
> 📄 Transcripción completa: <wikilink_transcript>
> 🔗 Vídeo original: [youtube.com/watch?v=<video_id>](<url>)
>
> **Resumen:** <resumen de 3-5 frases generado desde la transcripción>

---
```

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

## Conexiones
- [[...]] — <razón del enlace>
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

## Conexiones
- [[...]] — <razón del enlace>
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

## Conexiones
- [[...]] — <razón del enlace>
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

## Conexiones
- [[...]] — <razón del enlace>
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
