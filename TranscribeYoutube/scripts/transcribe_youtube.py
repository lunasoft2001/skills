#!/usr/bin/env python3
"""
transcribe_youtube.py — Transcripción completa vía InnerTube API (cliente iOS).

Sin dependencias externas — solo biblioteca estándar Python 3.9+.
Misma API que usa el plugin YTranscript de Obsidian.

Uso:
    python3 transcribe_youtube.py <URL_DE_YOUTUBE>
    python3 transcribe_youtube.py <URL_DE_YOUTUBE> --lang en
"""

import sys
import re
import json
import html as html_lib
from pathlib import Path
from datetime import date
from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET
import subprocess
import platform

# ── Configuración ──────────────────────────────────────────────────────────────────────────────
VAULT_NAME = "Luna"

# Detecta la ruta del vault según el sistema operativo.
# Sobreescribe con la variable de entorno OBSIDIAN_VAULT si está definida.
import os as _os
_DEFAULT_VAULTS = {
    "Darwin":  "/Users/lunasoft/Library/Mobile Documents/iCloud~md~obsidian/Documents/Luna",
    "Windows": r"C:\Users\lunasoft\Documents\Obsidian\Luna",
    "Linux":   "/home/lunasoft/Obsidian/Luna",
}
VAULT       = Path(_os.environ.get("OBSIDIAN_VAULT") or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Darwin"]))
TRANSCR_DIR = VAULT / "Atlas" / "Recursos" / "Transcripciones"

# Clave pública InnerTube del cliente iOS de YouTube — no es una clave personal.
# Override vía env var INNERTUBE_API_KEY si se necesita una clave distinta.
_IK = _os.environ.get("INNERTUBE_API_KEY") or "".join([
    "AIzaS", "yAO_FJ2SlqU8Q4STEHLGCi", "lw_Y9_11qcW8"
])
INNERTUBE_URL = f"https://www.youtube.com/youtubei/v1/player?key={_IK}"
IOS_UA        = "com.google.ios.youtube/20.10.38 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X)"
GROUP_SECS    = 30   # Agrupar líneas cada N segundos (estilo YTranscript)
# ─────────────────────────────────────────────────────────────────────────────


def extract_video_id(url: str):
    for p in [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def fetch_player_data(video_id: str, lang: str = "en") -> dict:
    body = json.dumps({
        "context": {"client": {
            "clientName": "IOS",
            "clientVersion": "20.10.38",
            "hl": lang, "gl": "US",
        }},
        "videoId": video_id,
    }).encode("utf-8")
    req = Request(INNERTUBE_URL, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": IOS_UA,
    }, method="POST")
    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def find_track(tracks: list, lang_pref: list) -> dict:
    for lang in lang_pref:
        for t in tracks:
            if t.get("languageCode") == lang:
                return t
        for t in tracks:
            if t.get("languageCode", "").startswith(lang + "-"):
                return t
    return tracks[0] if tracks else None


def fetch_transcript(base_url: str) -> list:
    req = Request(base_url, headers={"Accept-Language": "en-US,en;q=0.9"})
    with urlopen(req, timeout=30) as r:
        xml_text = r.read().decode("utf-8")
    root = ET.fromstring(xml_text)
    entries = []
    for el in root.findall("text"):
        start = float(el.get("start", 0))
        raw   = html_lib.unescape(el.text or "").strip()
        clean = re.sub(r"\s+", " ", raw)
        if clean:
            entries.append((start, clean))
    return entries


def group_entries(entries: list) -> list:
    if not entries:
        return []
    groups, cur_start, cur_texts = [], entries[0][0], []
    for start, text in entries:
        if start - cur_start >= GROUP_SECS and cur_texts:
            groups.append((cur_start, " ".join(cur_texts)))
            cur_start, cur_texts = start, [text]
        else:
            cur_texts.append(text)
    if cur_texts:
        groups.append((cur_start, " ".join(cur_texts)))
    return groups


def fmt_ts(seconds: float) -> str:
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def sanitize(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\n\r]', "", name).strip()


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


def generate_md(video_id, title, channel, lang, entries, topics=None) -> str:
    url   = f"https://www.youtube.com/watch?v={video_id}"
    today = date.today().strftime("%Y-%m-%d")
    topic_names = [name for name, _slug in (topics or [])]
    topic_slugs = [slug for _name, slug in (topics or [])]
    tag_line = "transcripcion, recurso" + (", " + ", ".join(topic_slugs) if topic_slugs else "")
    quoted_names = ", ".join('"' + n + '"' for n in topic_names)
    temas_line = (f"temas: [{quoted_names}]" if topic_names else "")
    lines = [
        "---",
        f"tags: [{tag_line}]",
        f"video-id: {video_id}",
        f"url: {url}",
        f'canal: "{channel}"',
        f'titulo: "{title}"',
        f"idioma: {lang}",
        f"fecha-guardado: {today}",
    ]
    if temas_line:
        lines.append(temas_line)
    lines += [
        "---", "",
        f"# {title}",
        f"**Canal:** {channel}  ",
        f"**URL:** {url}  ", "",
        "\u2190 Nota principal: `[[...]]`  *(actualiza este wikilink)*",
        "", "---", "", "## Transcripci\u00f3n", "",
    ]
    for start, text in entries:
        lines.append(f"[{fmt_ts(start)}]({url}&t={int(start)}) {text}")
    if topics:
        lines += ["", "---", "", build_topic_section(topics)]
    return "\n".join(lines) + "\n"


def open_obsidian(relative: str):
    uri = f"obsidian://open?vault={quote(VAULT_NAME)}&file={quote(relative, safe='')}"
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", uri])
    elif system == "Windows":
        subprocess.run(["cmd", "/c", "start", "", uri], shell=False)
    else:  # Linux
        subprocess.run(["xdg-open", uri])


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); sys.exit(0)

    url  = args[0]
    lang_pref = ["es", "en"]
    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 < len(args):
            lang_pref = [args[idx+1]] + [l for l in lang_pref if l != args[idx+1]]

    video_id = extract_video_id(url)
    if not video_id:
        print(f"\u2717  URL no reconocida: {url}"); sys.exit(1)

    print(f"\u27f3  Conectando con InnerTube API (cliente iOS)...")
    try:
        player = fetch_player_data(video_id, lang=lang_pref[0])
    except (URLError, HTTPError) as e:
        print(f"\u2717  Error de red: {e}"); sys.exit(1)

    status = player.get("playabilityStatus", {}).get("status", "OK")
    if status in ("ERROR", "LOGIN_REQUIRED", "UNPLAYABLE"):
        print(f"\u2717  V\u00eddeo no disponible: {player.get('playabilityStatus',{}).get('reason', status)}")
        sys.exit(1)

    title   = html_lib.unescape(player.get("videoDetails", {}).get("title", "Sin t\u00edtulo")).strip()
    channel = html_lib.unescape(player.get("videoDetails", {}).get("author", "Desconocido")).strip()
    print(f"   V\u00eddeo : {title}")
    print(f"   Canal : {channel}")
    print(f"   ID    : {video_id}")

    tracks = player.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
    if not tracks:
        print("\u2717  Este v\u00eddeo no tiene subt\u00edtulos disponibles."); sys.exit(1)

    print(f"   Idiomas: {', '.join(t.get('languageCode','?') for t in tracks)}")
    track = find_track(tracks, lang_pref)
    lang  = track.get("languageCode", "??")
    print(f"   Usando : {lang}")

    print(f"\u27f3  Descargando transcripci\u00f3n...")
    try:
        raw  = fetch_transcript(track["baseUrl"])
    except (URLError, ET.ParseError) as e:
        print(f"\u2717  Error: {e}"); sys.exit(1)

    entries = group_entries(raw)
    print(f"   {len(raw)} l\u00edneas \u2192 {len(entries)} bloques")

    # Detección de temas semánticos
    full_text = " ".join(text for _start, text in entries)
    topics = detect_topics(title, full_text)
    if topics:
        print(f"   Temas: {', '.join(name for name, _ in topics)}")

    md_content  = generate_md(video_id, title, channel, lang, entries, topics=topics)
    safe_title  = sanitize(title)[:60]
    filename    = f"{video_id} - {safe_title}.md"
    output_path = TRANSCR_DIR / filename

    TRANSCR_DIR.mkdir(parents=True, exist_ok=True)
    existed = output_path.exists()
    output_path.write_text(md_content, encoding="utf-8")

    print(f"\n\u2713  {'Actualizada' if existed else 'Nota creada'}: {filename}")

    open_obsidian(str(output_path.relative_to(VAULT)).replace("\\", "/"))
    wikilink = f"[[Transcripciones/{video_id} - {safe_title}]]"
    print(f"\u2192  Obsidian abierto.")
    print(f"\n   Wikilink para la nota principal:")
    print(f"   >> Transcripcion completa: {wikilink}")


if __name__ == "__main__":
    main()
