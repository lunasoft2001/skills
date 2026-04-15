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
    "Darwin":  os.path.expanduser("~/Documents/Obsidian/MyVault"),
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

    # 4. Construir JSON de salida para Copilot
    safe_title    = safe_filename(meta["title"])
    embed_url     = f"https://www.youtube.com/embed/{video_id}"
    watch_url     = f"https://www.youtube.com/watch?v={video_id}"
    wikilink_tr   = f"[[Atlas/Recursos/Transcripciones/{video_id} - {safe_title}]]"
    target_note   = str(VAULT / "Atlas" / "Recursos" / f"{safe_title}.md")

    output = {
        "video_id":          video_id,
        "title":             meta["title"],
        "channel":           meta["channel"],
        "description":       meta["description"],
        "duration":          duration_str(meta["duration_secs"]),
        "url":               watch_url,
        "embed_url":         embed_url,
        "fecha_guardado":    date.today().isoformat(),
        "transcript_path":   str(transcript_path) if transcript_path else None,
        "transcript_found":  transcript_path is not None,
        "wikilink_transcript": wikilink_tr,
        "transcript_content": transcript_content,
        "vault":             str(VAULT),
        "target_note":       target_note,
    }

    # Separador para que Copilot distinga el JSON del output del script de transcripción
    print("\n--- VIDEO_TO_OBSIDIAN_JSON_START ---", file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("--- VIDEO_TO_OBSIDIAN_JSON_END ---", file=sys.stderr)


if __name__ == "__main__":
    main()
