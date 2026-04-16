#!/usr/bin/env python3
"""
page_to_obsidian.py  —  Skill PageToObsidian

Captura de una página web individual a Obsidian.
Detecta tipo de sitio, convierte HTML a Markdown, gestiona índice de Personas.

Uso:
    python3 page_to_obsidian.py <URL>

Requiere:
    - Python 3.9+ (solo stdlib)
"""

import sys
import os
import re
import json
import platform
from pathlib import Path
from datetime import date
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, quote
from html.parser import HTMLParser

# ── Configuración ─────────────────────────────────────────────────────────────

_DEFAULT_VAULTS = {
    "Darwin":  "/Users/lunasoft/Library/Mobile Documents/iCloud~md~obsidian/Documents/Luna",
    "Windows": os.path.expanduser("~/Documents/Obsidian/MyVault"),
    "Linux":   os.path.expanduser("~/Documents/Obsidian/MyVault"),
}
VAULT = Path(
    os.environ.get("OBSIDIAN_VAULT")
    or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Darwin"])
)
VAULT_NAME   = os.environ.get("OBSIDIAN_VAULT_NAME") or VAULT.name
PERSONAS_DIR = VAULT / "Atlas" / "Personas"
RECURSOS_DIR = VAULT / "Atlas" / "Recursos"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# ── HTTP ───────────────────────────────────────────────────────────────────────

def fetch(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
    })
    with urlopen(req, timeout=timeout) as r:
        raw = r.read()
        ct = r.headers.get("Content-Type", "")
    
    enc = None
    m = re.search(r"charset=([^\s;\"']+)", ct)
    if m:
        enc = m.group(1).strip('"').lower()
    if not enc:
        try:
            raw.decode("utf-8")
            enc = "utf-8"
        except UnicodeDecodeError:
            enc = "latin-1"
    
    return raw.decode(enc, errors="replace")

# ── Extracción de metadatos ────────────────────────────────────────────────────

def extract_site_name(url: str) -> str:
    """Extrae nombre del sitio del dominio."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    # Algunos nombres comunes
    names = {
        "accessaplicaciones.com": "Accessaplicaciones",
        "area404.com": "Area 404",
        "github.com": "GitHub",
    }
    if domain in names:
        return names[domain]
    # Fallback: usar dominio limpio
    name = domain.split(".")[0].replace("-", " ").title()
    return name

def extract_title(html: str) -> str:
    """Extrae título de <title> o <h1>."""
    m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", html, re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return "Sin título"

def extract_content(html: str) -> str:
    """Extrae contenido principal (article, main, post, o body)."""
    patterns = [
        r"<article[^>]*>(.*?)</article>",
        r'<div[^>]*class=["\']main["\'][^>]*>(.*?)</div>',
        r"<main[^>]*>(.*?)</main>",
        r'<div[^>]*id=["\']post["\'][^>]*>(.*?)</div>',
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1)
    # Fallback: buscar el texto mayor
    m = re.search(r"<body[^>]*>(.*?)</body>", html, re.IGNORECASE | re.DOTALL)
    return m.group(1) if m else html

def extract_date(html: str) -> str | None:
    """Busca fecha de publicación en meta tags o patrones comunes."""
    patterns = [
        r'<meta\s+name=["\']publish_date["\'][^>]*content=["\']([^"\']+)["\']',
        r'<meta\s+property=["\']article:published_time["\'][^>]*content=["\']([^"\']+)["\']',
        r'<time[^>]*datetime=["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            date_str = m.group(1)
            # Limpiar si es ISO 8601
            date_str = date_str.split("T")[0]
            return date_str
    return None

def extract_author(html: str) -> str | None:
    """Busca autor en meta tags o patrones comunes."""
    patterns = [
        r'<meta\s+name=["\']author["\'][^>]*content=["\']([^"\']+)["\']',
        r'<meta\s+property=["\']article:author["\'][^>]*content=["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            return m.group(1)
    return None

# ── Conversión HTML → Markdown (muy básica) ────────────────────────────────────

def html_to_markdown(html: str) -> str:
    """Conversión simplificada HTML → Markdown."""
    # Eliminar scripts y styles
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.IGNORECASE | re.DOTALL)
    
    # Headers
    html = re.sub(r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<h4[^>]*>(.*?)</h4>", r"\n#### \1\n", html, flags=re.IGNORECASE | re.DOTALL)
    
    # Párrafos
    html = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\1\n", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<div[^>]*>(.*?)</div>", r"\n\1\n", html, flags=re.IGNORECASE | re.DOTALL)
    
    # Énfasis
    html = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<i[^>]*>(.*?)</i>", r"*\1*", html, flags=re.IGNORECASE | re.DOTALL)
    
    # Enlaces
    html = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r"[\2](\1)", html, flags=re.IGNORECASE | re.DOTALL)
    
    # Listas
    html = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1\n", html, flags=re.IGNORECASE | re.DOTALL)
    
    # Saltos de línea
    html = re.sub(r"<br\s*/?>\s*", "\n", html, flags=re.IGNORECASE)
    
    # Eliminar tags restantes
    html = re.sub(r"<[^>]+>", "", html)
    
    # Limpiar espacios en blanco excesivos
    html = re.sub(r"\n\s*\n\s*\n+", "\n\n", html)
    html = html.strip()
    
    return html

# ── Persona: Crear o actualizar ────────────────────────────────────────────────

def get_persona_path(site_name: str) -> Path:
    personas_dir = VAULT / "Atlas" / "Personas"
    personas_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r'[\\/*?:"<>|#\[\]]', '', site_name).strip()[:60].strip()
    return personas_dir / f"{safe_name}.md"

def persona_exists(site_name: str) -> bool:
    return get_persona_path(site_name).exists()

def safe_filename(title: str, max_len: int = 60) -> str:
    clean = re.sub(r'[\\/*?:"<>|#\[\]]', '', title)
    return clean.strip()[:max_len].strip()

def page_id_from_url(url: str) -> str:
    """Genera un ID único para la página (slug del path o hash)."""
    parsed = urlparse(url)
    path = parsed.path.strip("/").split("/")[-1]
    if path and "." not in path:
        return path
    # Fallback: usar hash del URL
    return str(hash(url) & 0x7fffffff)[:8]

def create_persona_index(site_name: str, page_title: str, page_url: str, 
                        page_id: str, date_published: str, wikilink_page: str) -> Path:
    """Crea un nuevo archivo de Persona."""
    persona_path = get_persona_path(site_name)
    
    content = f"""---
tags: [atlas, persona, sitio-web]
sitio: "{site_name}"
url: {urlparse(page_url).scheme}://{urlparse(page_url).netloc}
updated: {date.today().isoformat()}
total-articulos: 1
---

# {site_name} — Índice de artículos

> Sitio web con artículos capturados.
> Marca con `[x]` los que quieras procesar con WebToObsidian.
> Los marcados con `[p]` ya han sido procesados (nota generada en Atlas/Recursos/).

---

## Artículos

- [p] **{page_title}** · {date_published or "s.d."} · {page_url} · `{page_id}`

---

## Notas generadas

{wikilink_page}
"""
    
    persona_path.write_text(content, encoding="utf-8")
    return persona_path

def add_page_to_persona(persona_path: Path, page_title: str, page_url: str,
                       page_id: str, date_published: str, wikilink_page: str):
    """Agrega esta página a un archivo de Persona existente."""
    content = persona_path.read_text(encoding="utf-8")
    
    # Evitar duplicados
    if f"`{page_id}`" in content:
        return
    
    page_line = f"- [p] **{page_title}** · {date_published or 's.d.'} · {page_url} · `{page_id}`\n"
    
    # Insertar en sección Artículos
    lines = content.splitlines(keepends=True)
    new_lines = []
    inserted = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and "## Artículos" in "\n".join(lines[:i+1]) and line.strip() == "---":
            new_lines.pop()
            new_lines.append(page_line)
            new_lines.append(line)
            inserted = True
    
    # Actualizar wikilink en "Notas generadas"
    final_content = "".join(new_lines)
    if not inserted:
        final_content = final_content.replace(
            "\n## Artículos",
            f"\n- [p] **{page_title}** · {date_published or 's.d.'} · {page_url} · `{page_id}`\n\n## Artículos"
        )
    
    if wikilink_page not in final_content:
        final_content = final_content.replace(
            "## Notas generadas\n",
            f"## Notas generadas\n\n{wikilink_page}"
        )
    
    # Actualizar total-articulos
    count = final_content.count("`")
    if count > 0:
        final_content = re.sub(
            r"total-articulos: \d+",
            f"total-articulos: {count // 2}",
            final_content,
            count=1
        )
    
    persona_path.write_text(final_content, encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 page_to_obsidian.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    
    # 1. Descargar página
    print(f">> [1/4] Descargando: {url}", file=sys.stderr)
    try:
        html = fetch(url)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 2. Extraer metadatos
    print(">> [2/4] Extrayendo metadatos...", file=sys.stderr)
    title = extract_title(html)
    site_name = extract_site_name(url)
    date_published = extract_date(html)
    author = extract_author(html)
    page_id = page_id_from_url(url)
    
    # 3. Convertir HTML → Markdown
    print(">> [3/4] Convirtiendo a Markdown...", file=sys.stderr)
    content_html = extract_content(html)
    markdown_content = html_to_markdown(content_html)
    
    # 4. Gestionar Persona
    print(">> [4/4] Actualizando índice de Personas...", file=sys.stderr)
    safe_title = safe_filename(title)
    
    # Crear carpeta de recursos del sitio
    site_recursos_dir = RECURSOS_DIR / safe_filename(site_name)
    site_recursos_dir.mkdir(parents=True, exist_ok=True)
    
    target_note = site_recursos_dir / f"{safe_title}.md"
    wikilink_page = f"- [[Atlas/Recursos/{safe_filename(site_name)}/{safe_title}]]"
    
    persona_path = get_persona_path(site_name)
    if not persona_exists(site_name):
        persona_path = create_persona_index(
            site_name, title, url, page_id,
            date_published or "s.d.", wikilink_page
        )
        created_now = True
    else:
        add_page_to_persona(
            persona_path, title, url, page_id,
            date_published or "s.d.", wikilink_page
        )
        created_now = False
    
    # Emitir JSON
    output = {
        "title": title,
        "site_name": site_name,
        "url": url,
        "page_id": page_id,
        "date_published": date_published,
        "author": author,
        "content": markdown_content,
        "target_note": str(target_note),
        "fecha_guardado": date.today().isoformat(),
        "persona": {
            "name": site_name,
            "path": str(persona_path),
            "wikilink": f"[[Atlas/Personas/{safe_filename(site_name)}]]",
            "created_now": created_now,
        }
    }
    
    print("\n--- PAGE_TO_OBSIDIAN_JSON_START ---", file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("--- PAGE_TO_OBSIDIAN_JSON_END ---", file=sys.stderr)

if __name__ == "__main__":
    main()
