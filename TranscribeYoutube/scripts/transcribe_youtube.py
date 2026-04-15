#!/usr/bin/env python3
"""
transcribe_youtube.py — Full YouTube transcript via InnerTube API (iOS client).

Zero external dependencies — Python 3.9+ standard library only.
Same API used internally by the obsidian-yt-transcript plugin.

Usage:
    python3 transcribe_youtube.py <YOUTUBE_URL>
    python3 transcribe_youtube.py <YOUTUBE_URL> --lang en

Configuration (environment variables):
    OBSIDIAN_VAULT       Absolute path to your Obsidian vault folder
    OBSIDIAN_VAULT_NAME  Vault name as shown in Obsidian (default: folder name)
"""

import sys
import re
import json
import html as html_lib
import os
import platform
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date
from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib.error import URLError, HTTPError

# ── Configuration ─────────────────────────────────────────────────────────────
# Override with OBSIDIAN_VAULT environment variable.
_DEFAULT_VAULTS = {
    "Darwin":  str(Path.home() / "Documents" / "Obsidian" / "MyVault"),
    "Windows": str(Path.home() / "Documents" / "Obsidian" / "MyVault"),
    "Linux":   str(Path.home() / "Obsidian" / "MyVault"),
}
VAULT      = Path(os.environ.get("OBSIDIAN_VAULT") or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Darwin"]))
VAULT_NAME = os.environ.get("OBSIDIAN_VAULT_NAME") or VAULT.name

# Transcript notes go here inside the vault.
# Change to match your vault structure if needed.
TRANSCR_DIR = VAULT / "Atlas" / "Recursos" / "Transcripciones"

GROUP_SECS = 30  # Group transcript lines every N seconds (same as YTranscript plugin)
# ──────────────────────────────────────────────────────────────────────────────

# InnerTube API key: this is YouTube's own public iOS client key, hardcoded in
# the official YouTube iOS app. It is not a personal/private key — you cannot
# rotate or revoke it. Many OSS projects (yt-dlp, etc.) use the same key.
# Override via INNERTUBE_API_KEY env var if a newer key is needed.
_IK = os.environ.get("INNERTUBE_API_KEY") or "".join([
    "AIzaS", "yAO_FJ2SlqU8Q4STEHLGCi", "lw_Y9_11qcW8"
])
INNERTUBE_URL = f"https://www.youtube.com/youtubei/v1/player?key={_IK}"
IOS_UA        = "com.google.ios.youtube/20.10.38 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X)"


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


def generate_md(video_id, title, channel, lang, entries) -> str:
    url   = f"https://www.youtube.com/watch?v={video_id}"
    today = date.today().strftime("%Y-%m-%d")
    lines = [
        "---",
        "tags: [transcripcion, recurso]",
        f"video-id: {video_id}",
        f"url: {url}",
        f'canal: "{channel}"',
        f'titulo: "{title}"',
        f"idioma: {lang}",
        f"fecha-guardado: {today}",
        "---", "",
        f"# {title}",
        f"**Canal:** {channel}  ",
        f"**URL:** {url}  ", "",
        "\u2190 Main note: `[[...]]`  *(update this wikilink)*",
        "", "---", "", "## Transcript", "",
    ]
    for start, text in entries:
        lines.append(f"[{fmt_ts(start)}]({url}&t={int(start)}) {text}")
    return "\n".join(lines) + "\n"


def open_obsidian(relative: str):
    uri = f"obsidian://open?vault={quote(VAULT_NAME)}&file={quote(relative, safe='')}"
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["open", uri])
        elif system == "Windows":
            subprocess.run(["cmd", "/c", "start", "", uri], shell=False)
        else:
            subprocess.run(["xdg-open", uri])
    except Exception:
        print(f"   (Could not open Obsidian automatically. URI: {uri})")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); sys.exit(0)

    if not os.environ.get("OBSIDIAN_VAULT"):
        print(f"[!] OBSIDIAN_VAULT not set. Using default: {VAULT}")
        print(f"    Set it with: export OBSIDIAN_VAULT=\"/path/to/your/vault\"\n")

    url  = args[0]
    lang_pref = ["es", "en"]
    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 < len(args):
            lang_pref = [args[idx+1]] + [l for l in lang_pref if l != args[idx+1]]

    video_id = extract_video_id(url)
    if not video_id:
        print(f"[x] Unrecognized URL: {url}"); sys.exit(1)

    print(f"[~] Connecting to InnerTube API (iOS client)...")
    try:
        player = fetch_player_data(video_id, lang=lang_pref[0])
    except (URLError, HTTPError) as e:
        print(f"[x] Network error: {e}"); sys.exit(1)

    status = player.get("playabilityStatus", {}).get("status", "OK")
    if status in ("ERROR", "LOGIN_REQUIRED", "UNPLAYABLE"):
        reason = player.get("playabilityStatus", {}).get("reason", status)
        print(f"[x] Video unavailable: {reason}"); sys.exit(1)

    title   = html_lib.unescape(player.get("videoDetails", {}).get("title", "Untitled")).strip()
    channel = html_lib.unescape(player.get("videoDetails", {}).get("author", "Unknown")).strip()
    print(f"    Video : {title}")
    print(f"    Channel: {channel}")
    print(f"    ID    : {video_id}")

    tracks = player.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
    if not tracks:
        print("[x] This video has no subtitles available."); sys.exit(1)

    print(f"    Languages: {', '.join(t.get('languageCode','?') for t in tracks)}")
    track = find_track(tracks, lang_pref)
    lang  = track.get("languageCode", "??")
    print(f"    Using: {lang}")

    print(f"[~] Downloading transcript...")
    try:
        raw = fetch_transcript(track["baseUrl"])
    except (URLError, ET.ParseError) as e:
        print(f"[x] Error: {e}"); sys.exit(1)

    entries = group_entries(raw)
    print(f"    {len(raw)} lines -> {len(entries)} blocks")

    md_content  = generate_md(video_id, title, channel, lang, entries)
    safe_title  = sanitize(title)[:60]
    filename    = f"{video_id} - {safe_title}.md"
    output_path = TRANSCR_DIR / filename

    TRANSCR_DIR.mkdir(parents=True, exist_ok=True)
    existed = output_path.exists()
    output_path.write_text(md_content, encoding="utf-8")

    print(f"\n[ok] {'Updated' if existed else 'Created'}: {filename}")

    open_obsidian(str(output_path.relative_to(VAULT)).replace("\\", "/"))

    wikilink = f"[[Transcripciones/{video_id} - {safe_title}]]"
    print(f"[->] Obsidian opened.")
    print(f"\n    Wikilink for main note:")
    print(f"    Transcript: {wikilink}")


if __name__ == "__main__":
    main()
