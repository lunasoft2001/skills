#!/usr/bin/env python3
"""
video_to_obsidian.py — Parte del skill VideoToObsidian

Descarga metadatos + transcripción de un vídeo de YouTube y emite un JSON
que Copilot usa para generar la nota técnica completa en Obsidian.

Uso:
    python3 video_to_obsidian.py <URL_YouTube>

Requiere:
    - Python 3.9+ (solo stdlib)
    - El skill TranscribeYoutube instalado en el mismo directorio padre
"""

import sys
import os
import re
import json
import subprocess
import platform
from pathlib import Path
from datetime import date
from urllib.request import Request, urlopen

# ── Configuración ─────────────────────────────────────────────────────────────

_DEFAULT_VAULTS = {
    "Darwin":  "/Users/lunasoft/Library/Mobile Documents/iCloud~md~obsidian/Documents/Luna",
    "Windows": os.path.expanduser("~/Documents/Obsidian/MyVault"),
    "Linux":   os.path.expanduser("~/Documents/Obsidian/MyVault"),
}
VAULT = Path(os.environ.get("OBSIDIAN_VAULT") or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Darwin"]))

# Script de transcripción (directorio hermano)
TRANSCR_SCRIPT = Path(__file__).parent.parent.parent / "TranscribeYoutube" / "scripts" / "transcribe_youtube.py"

# InnerTube: clave pública del cliente iOS de YouTube (no es una clave personal)
# Override vía env var INNERTUBE_API_KEY si se necesita una clave distinta.
_IK = os.environ.get("INNERTUBE_API_KEY") or "".join([
    "AIzaS", "yAO_FJ2SlqU8Q4STEHLGCi", "lw_Y9_11qcW8"
])
INNERTUBE_URL = f"https://www.youtube.com/youtubei/v1/player?key={_IK}"
IOS_UA = "com.google.ios.youtube/20.10.38 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X)"


# ── Utilidades ────────────────────────────────────────────────────────────────

def extract_video_id(url: str):
    for p in [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def duration_str(secs: int) -> str:
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def safe_filename(title: str, max_len: int = 60) -> str:
    """Elimina caracteres no válidos para nombre de fichero Obsidian."""
    clean = re.sub(r'[\\/*?:"<>|#\[\]]', '', title)
    return clean.strip()[:max_len].strip()


# ── Detección semántica de temas ──────────────────────────────────────────────

TOPIC_SPECS = [
    ("Access", "access", [r"\baccess\b", r"\bvba\b", r"\bdocmd\b", r"\bcurrentdb\b"]),
    ("SQL", "sql", [r"\bsql\b", r"\bselect\b", r"\bjoin\b", r"\bquery\b", r"\bconsulta(?:s)?\b"]),
    ("SQL Server", "sql-server", [r"sql server", r"\bt-sql\b", r"\bssms\b"]),
    ("VBA", "vba", [r"\bvba\b", r"\bcurrentdb\b", r"\bdocmd\b", r"\bfunction\b", r"\bsub\b"]),
    ("Consultas", "consultas", [r"\bconsulta(?:s)?\b", r"\bquery\b", r"\bselect\b", r"\bwhere\b"]),
    ("Tablas", "tablas", [r"\btabla(?:s)?\b", r"\brecordset\b"]),
    ("Formularios", "formularios", [r"\bformulario(?:s)?\b", r"\bsubformulario(?:s)?\b", r"\bcombobox\b", r"\blistbox\b"]),
    ("Informes", "informes", [r"\binforme(?:s)?\b", r"\breport(?:e|es)?\b"]),
    ("DAO", "dao", [r"\bdao\b", r"\brecordsaffected\b", r"\bcurrentdb\b"]),
    ("ADO", "ado", [r"\badodb\b", r"ole\s*db", r"\boledb\b"]),
    ("Excel", "excel", [r"\bexcel\b", r"\bxls[xm]?\b"]),
    ("XML", "xml", [r"\bxml\b", r"\bdom\b"]),
    ("PDF", "pdf", [r"\bpdf\b"]),
    ("API Windows", "api-windows", [r"windows api", r"\bwinapi\b"]),
    ("FSO", "fso", [r"\bfso\b", r"filesystemobject"]),
    ("IA", "ia", [r"\binteligencia artificial\b", r"\b(?:ai|ia)\b", r"\bllm\b", r"\bgpt\b", r"\bchatgpt\b", r"\bcopilot\b"]),
    ("Python", "python", [r"\bpython\b", r"\bpypi\b", r"\bpip\b"]),
    ("Power Automate", "power-automate", [r"power automate", r"\bflow\b", r"power platform"]),
]


def detect_topics(title: str, content: str) -> list[tuple[str, str]]:
    haystack = f"{title}\n{content}".lower()
    topics = []
    for topic_name, topic_slug, patterns in TOPIC_SPECS:
        if any(re.search(p, haystack, re.IGNORECASE) for p in patterns):
            topics.append((topic_name, topic_slug))
    return topics


def build_topic_section(topics: list[tuple[str, str]]) -> str:
    if not topics:
        return ""
    lines = ["## Conexiones", "", "### Temas", ""]
    for topic_name, _slug in topics:
        lines.append(f"- [[Atlas/Temas/{topic_name}]]")
    lines += ["", "### Relacionado", "", "- *(Añade aquí notas relacionadas del vault)*"]
    return "\n".join(lines)


# ── InnerTube: metadatos ───────────────────────────────────────────────────────

def fetch_metadata(video_id: str) -> dict:
    body = json.dumps({
        "videoId": video_id,
        "context": {
            "client": {
                "clientName": "IOS",
                "clientVersion": "20.10.38",
                "deviceModel": "iPhone16,2",
                "userAgent": IOS_UA,
                "hl": "es",
                "gl": "ES",
            }
        }
    }).encode()

    req = Request(INNERTUBE_URL, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": IOS_UA,
        "X-YouTube-Client-Name": "5",
        "X-YouTube-Client-Version": "20.10.38",
    })
    resp = urlopen(req, timeout=15)
    data = json.loads(resp.read())
    vd = data.get("videoDetails", {})
    return {
        "video_id":      vd.get("videoId", video_id),
        "title":         vd.get("title", "Sin título"),
        "channel":       vd.get("author", "Desconocido"),
        "description":   vd.get("shortDescription", "")[:800],
        "duration_secs": int(vd.get("lengthSeconds", 0)),
    }


# ── TranscribeYoutube: delegar ────────────────────────────────────────────────

def run_transcribe(url: str) -> int:
    """Llama al script TranscribeYoutube y devuelve el código de salida."""
    if not TRANSCR_SCRIPT.exists():
        print(f"ERROR: No se encontró TranscribeYoutube en {TRANSCR_SCRIPT}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(TRANSCR_SCRIPT), url],
        capture_output=False   # deja que los prints del script lleguen a stderr/stdout del usuario
    )
    return result.returncode


def find_transcript_file(video_id: str) -> Path | None:
    transcr_dir = VAULT / "Atlas" / "Recursos" / "Transcripciones"
    for f in transcr_dir.glob(f"{video_id} - *.md"):
        return f
    return None


# ── Personas: Crear o actualizar índice del canal ──────────────────────────────

def get_persona_path(channel_name: str) -> Path:
    """Ruta donde guardar el archivo de Persona del canal."""
    personas_dir = VAULT / "Atlas" / "Personas"
    personas_dir.mkdir(parents=True, exist_ok=True)
    safe_name = safe_filename(channel_name)
    return personas_dir / f"{safe_name}.md"


def persona_exists(channel_name: str) -> bool:
    """Comprueba si ya existe un archivo de Persona para este canal."""
    return get_persona_path(channel_name).exists()


def load_persona_index(persona_path: Path) -> dict:
    """Lee un archivo de Persona y devuelve {video_id: estado}."""
    states = {}
    if not persona_path.exists():
        return states
    content = persona_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        m = re.match(r'- \[([ pPxX])\].*`([a-zA-Z0-9_-]{11})`', line)
        if m:
            mark, vid_id = m.group(1), m.group(2)
            states[vid_id] = mark.strip()
    return states


def load_persona_processed_notes(persona_path: Path) -> list[str]:
    """Lee las notas ya procesadas en la sección 'Notas generadas'."""
    if not persona_path.exists():
        return []
    
    content = persona_path.read_text(encoding="utf-8")
    in_notas = False
    notas = []
    for line in content.splitlines():
        if "## Notas generadas" in line:
            in_notas = True
            continue
        if in_notas and line.startswith("##"):
            break
        if in_notas and line.startswith("- [["):
            notas.append(line.strip())
    
    return notas


def create_persona_index(channel_name: str, video_id: str, video_title: str, 
                        duration: str, published: str, wikilink_video: str) -> Path:
    """Crea un nuevo archivo de Persona con este vídeo."""
    persona_path = get_persona_path(channel_name)
    
    safe_channel = safe_filename(channel_name)
    content = f"""---
tags: [atlas, persona, canal-youtube]
canal: "{channel_name}"
url: https://www.youtube.com/{safe_channel}
updated: {date.today().isoformat()}
total-videos: 1
---

# {channel_name} — Índice de vídeos

> Canal de YouTube con vídeos capturados.
> Marca con `[x]` los que quieras procesar con ChannelToObsidian.
> Los marcados con `[p]` ya han sido procesados (nota generada en Atlas/Recursos/).

---

## Vídeos

- [p] **{video_title}** · {duration} · {published} · `{video_id}`

---

## Notas generadas

{wikilink_video}
"""
    
    persona_path.write_text(content, encoding="utf-8")
    return persona_path


def add_video_to_persona(persona_path: Path, video_id: str, video_title: str,
                         duration: str, published: str, wikilink_video: str):
    """Agrega este vídeo a un archivo de Persona existente."""
    content = persona_path.read_text(encoding="utf-8")
    
    # Verificar si ya está este video_id
    if f"`{video_id}`" in content:
        return  # Ya existe, no duplicar
    
    # Insertar en sección Vídeos (antes de "---")
    video_line = f"- [p] **{video_title}** · {duration} · {published} · `{video_id}`\n"
    
    # Buscar la primera línea "---" después de "## Vídeos"
    lines = content.splitlines(keepends=True)
    new_lines = []
    inserted_video = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Si ya insertamos el vídeo, seguir
        if inserted_video:
            continue
        
        # Si estamos en la sección Vídeos y encontramos un "---"
        if "## Vídeos" in "\n".join(lines[:i+1]) and line.strip() == "---":
            # Insertar antes de este "---"
            new_lines.pop()  # quitar el "---" que acabamos de agregar
            new_lines.append(video_line)
            new_lines.append(line)  # volver a poner el "---"
            inserted_video = True
    
    # Si no encontramos la sección Vídeos, insertar al final antes de "## Notas generadas"
    if not inserted_video:
        final_content = "".join(new_lines)
        final_content = final_content.replace(
            "\n## Notas generadas",
            f"\n- [p] **{video_title}** · {duration} · {published} · `{video_id}`\n\n## Notas generadas"
        )
        new_lines = final_content.splitlines(keepends=True)
    
    # Agregar wikilink en "Notas generadas" si no está ya
    final_content = "".join(new_lines)
    notas_section = "## Notas generadas"
    if notas_section in final_content and wikilink_video not in final_content:
        final_content = final_content.replace(
            f"{notas_section}\n",
            f"{notas_section}\n\n{wikilink_video}"
        )
    
    # Actualizar total-videos
    final_content = re.sub(
        r'total-videos: \d+',
        lambda m: f"total-videos: {final_content.count('`') // 2 if '`' in final_content else 1}",
        final_content,
        count=1
    )
    
    persona_path.write_text(final_content, encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 video_to_obsidian.py <URL_YouTube>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)
    if not video_id:
        print(f"ERROR: No se pudo extraer el ID del vídeo de: {url}", file=sys.stderr)
        sys.exit(1)

    # 1. Metadatos
    print(">> [1/3] Descargando metadatos...", file=sys.stderr)
    try:
        meta = fetch_metadata(video_id)
    except Exception as e:
        print(f"ERROR al obtener metadatos: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Transcripción (delega en TranscribeYoutube)
    print(">> [2/3] Descargando transcripción...", file=sys.stderr)
    rc = run_transcribe(url)
    if rc != 0:
        print(f"AVISO: TranscribeYoutube terminó con código {rc} (puede que no haya subtítulos)", file=sys.stderr)

    # 3. Leer fichero de transcripción generado
    print(">> [3/3] Preparando datos para Copilot...", file=sys.stderr)
    transcript_path = find_transcript_file(video_id)
    transcript_content = ""
    if transcript_path and transcript_path.exists():
        transcript_content = transcript_path.read_text(encoding="utf-8")

    # 3b. Detección semántica de temas
    topics = detect_topics(meta["title"], f"{meta['description']}\n{transcript_content}")
    topic_tags   = [slug for _name, slug in topics]
    topic_names  = [name for name, _slug in topics]
    topic_section = build_topic_section(topics)

    # 4. Construir JSON de salida para Copilot
    safe_title    = safe_filename(meta["title"])
    embed_url     = f"https://www.youtube.com/embed/{video_id}"
    watch_url     = f"https://www.youtube.com/watch?v={video_id}"
    wikilink_tr   = f"[[Atlas/Recursos/Transcripciones/{video_id} - {safe_title}]]"
    target_note   = str(VAULT / "Atlas" / "Recursos" / f"{safe_title}.md")
    wikilink_video = f"- {wikilink_tr}"
    
    # 5. Manejar Persona del canal
    channel_name = meta["channel"]
    persona_path = get_persona_path(channel_name)
    persona_exists_flag = persona_exists(channel_name)
    
    published = "hoy"  # Placeholder — VideoToObsidian no obtiene fecha publicación
    duration_display = duration_str(meta["duration_secs"])
    
    if not persona_exists_flag:
        print(f">> Creando Persona: {channel_name}", file=sys.stderr)
        persona_path = create_persona_index(
            channel_name, video_id, meta["title"], 
            duration_display, published, wikilink_video
        )
    else:
        print(f">> Actualizando Persona: {channel_name}", file=sys.stderr)
        add_video_to_persona(
            persona_path, video_id, meta["title"],
            duration_display, published, wikilink_video
        )

    output = {
        "video_id":          video_id,
        "title":             meta["title"],
        "channel":           meta["channel"],
        "description":       meta["description"],
        "duration":          duration_display,
        "url":               watch_url,
        "embed_url":         embed_url,
        "fecha_guardado":    date.today().isoformat(),
        "transcript_path":   str(transcript_path) if transcript_path else None,
        "transcript_found":  transcript_path is not None,
        "wikilink_transcript": wikilink_tr,
        "transcript_content": transcript_content,
        "vault":             str(VAULT),
        "target_note":       target_note,
        "topics":            topic_names,
        "topic_tags":        topic_tags,
        "topic_section":     topic_section,
        "persona": {
            "name":         channel_name,
            "path":         str(persona_path),
            "wikilink":     f"[[{persona_path.relative_to(VAULT)}]]",
            "created_now":  not persona_exists_flag,
        }
    }

    # Separador para que Copilot distinga el JSON del output del script de transcripción
    print("\n--- VIDEO_TO_OBSIDIAN_JSON_START ---", file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("--- VIDEO_TO_OBSIDIAN_JSON_END ---", file=sys.stderr)


if __name__ == "__main__":
    main()
