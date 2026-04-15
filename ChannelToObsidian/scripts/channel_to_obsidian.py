#!/usr/bin/env python3
"""
channel_to_obsidian.py  —  Skill ChannelToObsidian

Flujo en dos fases para capturar un canal de YouTube al Second Brain en Obsidian.

  FASE 1 — Scan (por defecto):
      python3 channel_to_obsidian.py <URL_canal>
      → Crea/actualiza Atlas/Personas/<ChannelName>.md con checklist de todos los vídeos.
        Abre Obsidian. Tú marcas con [x] los que quieres procesar.

  FASE 2 — Process:
      python3 channel_to_obsidian.py <URL_canal> --process
      → Lee el checklist, procesa los marcados con [x] llamando a VideoToObsidian.

Requiere:
    - Python 3.9+ (solo stdlib)
    - Skill VideoToObsidian instalado como directorio hermano
    - Conexión a internet
"""

import sys
import os
import re
import json
import time
import platform
import subprocess
from pathlib import Path
from datetime import date
from urllib.request import Request, urlopen
from urllib.parse import quote

# ── Configuración ─────────────────────────────────────────────────────────────

_DEFAULT_VAULTS = {
    "Darwin":  os.path.expanduser("~/Documents/Obsidian/MyVault"),
    "Windows": os.path.expanduser("~/Documents/Obsidian/MyVault"),
    "Linux":   os.path.expanduser("~/Documents/Obsidian/MyVault"),
}
VAULT = Path(os.environ.get("OBSIDIAN_VAULT") or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Darwin"]))
VAULT_NAME = os.environ.get("OBSIDIAN_VAULT_NAME") or VAULT.name

PERSONAS_DIR  = VAULT / "Atlas" / "Personas"
RECURSOS_DIR  = VAULT / "Atlas" / "Recursos"

VTO_SCRIPT = Path(__file__).parent.parent / "VideoToObsidian" / "scripts" / "video_to_obsidian.py"

# InnerTube (clave pública del cliente iOS de YouTube — no es una clave personal)
_IK = os.environ.get("INNERTUBE_API_KEY") or "".join([
    "AIzaS", "yAO_FJ2SlqU8Q4STEHLGCi", "lw_Y9_11qcW8"
])
_BROWSE_URL = f"https://www.youtube.com/youtubei/v1/browse?key={_IK}"
_IOS_UA     = "com.google.ios.youtube/20.10.38 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X)"

# Parámetros base64 del tab "Videos" del canal en InnerTube
_VIDEOS_TAB_PARAM = "EgZ2aWRlb3PyBgQKAhgA"


# ── InnerTube helpers ──────────────────────────────────────────────────────────

def _it_post(payload: dict) -> dict:
    body = json.dumps(payload).encode()
    req = Request(_BROWSE_URL, data=body, headers={
        "Content-Type":              "application/json",
        "User-Agent":                _IOS_UA,
        "X-YouTube-Client-Name":     "5",
        "X-YouTube-Client-Version":  "20.10.38",
    })
    return json.loads(urlopen(req, timeout=20).read())


def _base_payload(browse_id: str) -> dict:
    return {
        "browseId": browse_id,
        "context": {
            "client": {
                "clientName":    "IOS",
                "clientVersion": "20.10.38",
                "deviceModel":   "iPhone16,2",
                "userAgent":     _IOS_UA,
                "hl": "en", "gl": "US",
            }
        }
    }


# ── Resolución del canal ───────────────────────────────────────────────────────

def resolve_channel(url: str) -> tuple[str, str]:
    """
    Devuelve (browse_id, channel_name).
    Acepta: @handle, /c/slug, /channel/UCxxx, /user/xxx, URL completa.
    """
    url = url.strip().rstrip("/")

    # Extraer la parte relevante
    m = re.search(r'youtube\.com/(@[\w.-]+|c/[\w.-]+|channel/(UC[\w-]+)|user/[\w.-]+)', url)
    if m:
        part = m.group(1)
    elif re.match(r'^@', url):
        part = url           # ya es un handle
    elif re.match(r'^UC[\w-]{20,}$', url):
        part = f"channel/{url}"
    else:
        part = url           # lo intentamos tal cual

    # Si tenemos UC directamente
    uc_match = re.search(r'channel/(UC[\w-]+)', part)
    browse_id = uc_match.group(1) if uc_match else part

    print(f">> Resolviendo canal: {browse_id}", file=sys.stderr)

    payload = _base_payload(browse_id)
    payload["params"] = _VIDEOS_TAB_PARAM
    data = _it_post(payload)

    # Extraer nombre del canal
    channel_name = (
        data.get("header", {})
            .get("c4TabbedHeaderRenderer", {})
            .get("title", browse_id)
    )
    # Si el browse_id era un handle, obtener el UC real
    uc_id = (
        data.get("header", {})
            .get("c4TabbedHeaderRenderer", {})
            .get("channelId", browse_id)
    )

    return uc_id, channel_name, data


# ── Extracción de vídeos ───────────────────────────────────────────────────────

def _extract_videos_from_response(data: dict) -> tuple[list[dict], str | None]:
    """Extrae lista de vídeos y token de continuación de una respuesta browse."""
    videos = []
    continuation = None

    # Navegar la estructura de la respuesta browse (puede variar)
    def walk(obj):
        nonlocal continuation
        if isinstance(obj, dict):
            # ¿Es un videoRenderer?
            if "videoId" in obj and "title" in obj:
                vid_id = obj.get("videoId", "")
                title_runs = obj.get("title", {}).get("runs", [])
                title = title_runs[0].get("text", "Sin título") if title_runs else obj.get("title", {}).get("simpleText", "Sin título")
                duration = obj.get("lengthText", {}).get("simpleText", "?")
                published = obj.get("publishedTimeText", {}).get("simpleText", "")
                views = obj.get("viewCountText", {}).get("simpleText", "")
                if vid_id:
                    videos.append({
                        "video_id":  vid_id,
                        "title":     title,
                        "duration":  duration,
                        "published": published,
                        "views":     views,
                    })
            # ¿Token de continuación?
            if "continuationCommand" in obj:
                token = obj.get("continuationCommand", {}).get("token")
                if token:
                    continuation = token
            elif "token" in obj and "continuationEndpoint" in str(obj.get("endpoint", "")):
                continuation = obj.get("token")
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return videos, continuation


def fetch_all_videos(browse_id: str, initial_data: dict) -> list[dict]:
    """Pagina InnerTube hasta obtener todos los vídeos del canal."""
    all_videos = []
    data = initial_data

    page = 1
    while True:
        videos, continuation = _extract_videos_from_response(data)
        all_videos.extend(videos)
        print(f"   Página {page}: {len(videos)} vídeos (total: {len(all_videos)})", file=sys.stderr)

        if not continuation:
            break

        page += 1
        time.sleep(0.5)  # cortesía hacia la API
        payload = _base_payload(browse_id)
        payload["continuation"] = continuation
        try:
            data = _it_post(payload)
        except Exception as e:
            print(f"   AVISO: error en página {page}: {e}", file=sys.stderr)
            break

    return all_videos


# ── Fichero de índice del canal ────────────────────────────────────────────────

def safe_name(s: str, max_len: int = 60) -> str:
    return re.sub(r'[\\/*?:"<>|#\[\]]', '', s).strip()[:max_len].strip()


def channel_index_path(channel_name: str) -> Path:
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    return PERSONAS_DIR / f"{safe_name(channel_name)}.md"


def load_existing_index(path: Path) -> dict[str, str]:
    """Devuelve {video_id: estado} de un índice existente."""
    states = {}
    if not path.exists():
        return states
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r'- \[([ xXpP✓])\].*`([a-zA-Z0-9_-]{11})`', line)
        if m:
            mark, vid_id = m.group(1), m.group(2)
            states[vid_id] = mark.strip()
    return states


def write_index(path: Path, channel_name: str, videos: list[dict], existing_states: dict):
    """Escribe o actualiza el fichero de índice manteniendo los estados existentes."""
    lines = [
        "---",
        f"tags: [atlas, persona, canal-youtube]",
        f"canal: \"{channel_name}\"",
        f"url: https://www.youtube.com/@{channel_name.replace(' ', '')}",
        f"updated: {date.today().isoformat()}",
        f"total-videos: {len(videos)}",
        "---",
        "",
        f"# {channel_name} — Índice de vídeos",
        "",
        f"> Canal de YouTube con {len(videos)} vídeos capturados.",
        f"> Marca con `[x]` los que quieras procesar con ChannelToObsidian.",
        f"> Los marcados con `[p]` ya han sido procesados (nota generada en Atlas/Recursos/).",
        "",
        "---",
        "",
        "## Vídeos",
        "",
        "| Estado | Título | Dur. | Publicado | ID |",
        "|--------|--------|------|-----------|-----|",
    ]

    for v in videos:
        vid_id   = v["video_id"]
        state    = existing_states.get(vid_id, " ")
        mark     = f"[{state}]" if state else "[ ]"
        title    = v["title"].replace("|", "–")[:70]
        dur      = v["duration"]
        pub      = v["published"]
        lines.append(f"- {mark} **{title}** `{vid_id}` · {dur} · {pub}")

    lines += [
        "",
        "---",
        "",
        "## Notas generadas",
        "",
        "> Los vídeos procesados aparecerán aquí como wikilinks.",
        "",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")


def update_index_processed(path: Path, video_id: str):
    """Cambia [x] → [p] para un video_id ya procesado."""
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    # Reemplaza solo el [x] de esa línea específica
    content = re.sub(
        rf'(- \[)[xX](\].*`{re.escape(video_id)}`)',
        r'\1p\2',
        content
    )
    path.write_text(content, encoding="utf-8")


# ── Apertura en Obsidian ───────────────────────────────────────────────────────

def open_in_obsidian(abs_path: Path):
    rel = abs_path.relative_to(VAULT)
    encoded = quote(str(rel).replace("\\", "/"), safe="/")
    uri = f"obsidian://open?vault={quote(VAULT_NAME)}&file={encoded}"
    sys_name = platform.system()
    if sys_name == "Darwin":
        os.system(f'open "{uri}"')
    elif sys_name == "Windows":
        os.system(f'cmd /c start "" "{uri}"')
    else:
        os.system(f'xdg-open "{uri}"')


# ── Fase 2: procesar seleccionados ────────────────────────────────────────────

def process_selected(index_path: Path, channel_name: str):
    if not VTO_SCRIPT.exists():
        print(f"ERROR: VideoToObsidian no encontrado en {VTO_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    states = load_existing_index(index_path)
    selected = [vid_id for vid_id, s in states.items() if s.lower() in ("x",)]

    if not selected:
        print(">> No hay vídeos marcados con [x] en el índice.", file=sys.stderr)
        print(f"   Abre {index_path} en Obsidian y marca con [x] los vídeos que quieras procesar.", file=sys.stderr)
        sys.exit(0)

    print(f">> Procesando {len(selected)} vídeo(s) seleccionado(s)...", file=sys.stderr)

    for i, vid_id in enumerate(selected, 1):
        url = f"https://www.youtube.com/watch?v={vid_id}"
        print(f"\n[{i}/{len(selected)}] {url}", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, str(VTO_SCRIPT), url],
            capture_output=False
        )
        if result.returncode == 0:
            update_index_processed(index_path, vid_id)
            print(f"   ✓ {vid_id} procesado y marcado como [p]", file=sys.stderr)
        else:
            print(f"   ✗ {vid_id} falló (código {result.returncode})", file=sys.stderr)

        time.sleep(1)  # pausa entre vídeos

    print(f"\n>> Índice actualizado: {index_path}", file=sys.stderr)
    open_in_obsidian(index_path)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    channel_url = args[0]
    do_process  = "--process" in args

    # Resolver canal
    try:
        browse_id, channel_name, initial_data = resolve_channel(channel_url)
    except Exception as e:
        print(f"ERROR al resolver el canal: {e}", file=sys.stderr)
        sys.exit(1)

    print(f">> Canal: {channel_name} ({browse_id})", file=sys.stderr)

    index_path     = channel_index_path(channel_name)
    existing_states = load_existing_index(index_path)

    if do_process:
        # ── FASE 2: procesar los marcados con [x] ──
        process_selected(index_path, channel_name)
    else:
        # ── FASE 1: scan — obtener todos los vídeos y crear índice ──
        print(">> [Fase 1] Escaneando todos los vídeos del canal...", file=sys.stderr)
        try:
            videos = fetch_all_videos(browse_id, initial_data)
        except Exception as e:
            print(f"ERROR al obtener vídeos: {e}", file=sys.stderr)
            sys.exit(1)

        if not videos:
            print("AVISO: no se encontraron vídeos. Verifica la URL del canal.", file=sys.stderr)
            sys.exit(1)

        print(f">> {len(videos)} vídeos encontrados. Escribiendo índice...", file=sys.stderr)
        write_index(index_path, channel_name, videos, existing_states)

        print(f"✓  Índice creado: {index_path}", file=sys.stderr)
        print(f"   Abre el fichero en Obsidian, marca con [x] los vídeos que quieras procesar", file=sys.stderr)
        print(f"   y ejecuta de nuevo con --process", file=sys.stderr)

        open_in_obsidian(index_path)

        # Imprimir resumen para Copilot
        print(json.dumps({
            "channel_name":  channel_name,
            "browse_id":     browse_id,
            "total_videos":  len(videos),
            "index_path":    str(index_path),
            "next_command":  f'python3 {__file__} "{channel_url}" --process',
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
