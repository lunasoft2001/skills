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
from urllib.parse import urlparse, quote, urljoin
from html import unescape
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

def extract_meta_content(html: str, patterns: list[str]) -> str | None:
    """Devuelve el primer content=... para una lista de regex de meta tags."""
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m and m.group(1).strip():
            return m.group(1).strip()
    return None

def normalize_site_name(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip(" -|\t\n\r")
    # Normaliza formatos tipo "El Blog de X" / "The Blog of X"
    name = re.sub(r"^(?:el|the)\s+blog\s+(?:de|of)\s+", "", name, flags=re.IGNORECASE)
    # Si viene en formato "Artículo - Sitio", quedarnos con la parte de sitio
    if " - " in name:
        tail = name.split(" - ")[-1].strip()
        if tail:
            name = tail
    if "|" in name:
        tail = name.split("|")[-1].strip()
        if tail:
            name = tail
    return name[:1].upper() + name[1:] if name else "Sitio"

def infer_site_name_from_domain(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")
    names = {
        "accessaplicaciones.com": "Accessaplicaciones",
        "area404.com": "Area 404",
        "github.com": "GitHub",
    }
    if domain in names:
        return names[domain]

    labels = [p for p in domain.split(".") if p]
    if len(labels) >= 3 and labels[-2] in {"co", "com", "org", "net", "gov", "edu"}:
        base = labels[-3]
    elif len(labels) >= 2:
        base = labels[-2]
    else:
        base = labels[0] if labels else "sitio"
    return normalize_site_name(base)

def extract_site_name(url: str, html: str, title: str | None = None) -> str:
    """Extrae nombre del sitio con prioridad meta tags > título > dominio."""
    meta_name = extract_meta_content(html, [
        r'<meta\s+property=["\']og:site_name["\'][^>]*content=["\']([^"\']+)["\']',
        r'<meta\s+name=["\']application-name["\'][^>]*content=["\']([^"\']+)["\']',
    ])
    if meta_name:
        return normalize_site_name(meta_name)

    if title:
        m = re.search(r"(?:\bde\b|\bof\b)\s+([A-Za-z0-9\-_.]+)$", title, re.IGNORECASE)
        if m:
            return normalize_site_name(m.group(1))

    return infer_site_name_from_domain(url)

def resolve_preferred_source_url(url: str, html: str) -> tuple[str, str, bool]:
    """Si la URL es portada con múltiples artículos, intenta seguir el primer post."""
    parsed = urlparse(url)
    is_home = parsed.path.strip("/") == ""
    has_many_articles = len(re.findall(r"<article\b", html, re.IGNORECASE)) >= 2
    if not (is_home and has_many_articles):
        return url, html, False

    first_article = re.search(r"<article\b[^>]*>(.*?)</article>", html, re.IGNORECASE | re.DOTALL)
    if not first_article:
        return url, html, False

    links = re.findall(r'href=["\']([^"\']+)["\']', first_article.group(1), re.IGNORECASE)
    for link in links:
        lower = link.lower().strip()
        if (not lower or lower.startswith("#") or lower.startswith("mailto:") or
            lower.startswith("javascript:")):
            continue
        if any(x in lower for x in ("/category/", "/tag/", "/author/", "/page/", "/feed", "/comments/", "wp-json")):
            continue
        candidate = urljoin(url, link)
        c_parsed = urlparse(candidate)
        if c_parsed.netloc and c_parsed.netloc != parsed.netloc:
            continue
        try:
            candidate_html = fetch(candidate)
            return candidate, candidate_html, True
        except Exception:
            continue

    return url, html, False

def extract_title(html: str) -> str:
    """Extrae título de <title> o <h1>."""
    m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    if m:
        return unescape(m.group(1)).strip()
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", html, re.IGNORECASE)
    if m:
        return unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    return "Sin título"

def extract_content(html: str) -> str:
    """Extrae contenido principal (article, main, post, o body)."""
    patterns = [
        r'<div[^>]*class=["\'][^"\']*entry-content[^"\']*["\'][^>]*>(.*?)</div>',
        r'<div[^>]*class=["\'][^"\']*post-content[^"\']*["\'][^>]*>(.*?)</div>',
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
    html = unescape(html)

    # Eliminar bloques de ruido típicos de plantillas WordPress/social
    noise_patterns = [
        r"\[\*\*Facebook\].*",
        r"\[\*\*Twitter\].*",
        r"\[\*\*Linkedin\].*",
        r"\[\*\*Whatsapp\].*",
    ]
    for pattern in noise_patterns:
        html = re.sub(pattern, "", html, flags=re.IGNORECASE)

    # Eliminar líneas de contadores aislados tipo *41*
    html = re.sub(r"^\s*\*\d+\*\s*$", "", html, flags=re.MULTILINE)

    # Recortar al llegar a secciones de comentarios/relacionados
    cut_markers = [
        "También te puede interesar",
        "Deja un comentario",
        "0 comentarios",
        "Cancelar respuesta",
    ]
    lines = html.splitlines()
    trimmed = []
    for line in lines:
        if any(marker.lower() in line.lower() for marker in cut_markers):
            break
        trimmed.append(line)
    html = "\n".join(trimmed)
    
    return html

def clean_title(title: str, site_name: str) -> str:
    title = unescape(title)
    title = re.sub(r"\s+", " ", title).strip()

    # Quita sufijos comunes del sitio para dejar título de artículo
    suffix_patterns = [
        rf"\s+[\-–—|]\s+{re.escape(site_name)}$",
        r"\s+[\-–—|]\s+El Blog de .+$",
        r"\s+[\-–—|]\s+Blog de .+$",
    ]
    for pattern in suffix_patterns:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()

    return title or "Sin título"

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

TOPIC_SPECS = [
    ("Access", "access", [r"\baccess\b", r"\bvba\b", r"\bdocmd\b", r"\bcurrentdb\b"]),
    ("SQL", "sql", [r"\bsql\b", r"\bselect\b", r"\bjoin\b", r"\bquery\b", r"\bconsulta(?:s)?\b"]),
    ("SQL Server", "sql-server", [r"sql server", r"\bt-sql\b", r"\bssms\b", r"parameter sniffing", r"always on"]),
    ("VBA", "vba", [r"\bvba\b", r"\bcurrentdb\b", r"\bdocmd\b", r"\bfunction\b", r"\bsub\b"]),
    ("Consultas", "consultas", [r"\bconsulta(?:s)?\b", r"\bquery\b", r"\bselect\b", r"\bwhere\b"]),
    ("Tablas", "tablas", [r"\btabla(?:s)?\b", r"\brecordset\b", r"\bdao\b", r"\bado\b"]),
    ("Formularios", "formularios", [r"\bformulario(?:s)?\b", r"\bsubformulario(?:s)?\b", r"\bcombobox\b", r"\blistbox\b"]),
    ("Informes", "informes", [r"\binforme(?:s)?\b", r"\breport(?:e|es)?\b"]),
    ("DAO", "dao", [r"\bdao\b", r"\brecordsaffected\b", r"\bcurrentdb\b"]),
    ("ADO", "ado", [r"\bado\b", r"adodb", r"ole\s*db", r"oledb"]),
    ("Excel", "excel", [r"\bexcel\b", r"\bxls[xm]?\b"]),
    ("XML", "xml", [r"\bxml\b", r"\bdom\b"]),
    ("PDF", "pdf", [r"\bpdf\b"]),
    ("API Windows", "api-windows", [r"windows api", r"\bapi\b"]),
    ("FSO", "fso", [r"\bfso\b", r"filesystemobject"]),
]

def detect_topics(title: str, markdown_content: str) -> list[tuple[str, str]]:
    haystack = f"{title}\n{markdown_content}".lower()
    topics = []
    for topic_name, topic_slug, patterns in TOPIC_SPECS:
        if any(re.search(pattern, haystack, re.IGNORECASE) for pattern in patterns):
            topics.append((topic_name, topic_slug))
    return topics

def build_topic_section(topics: list[tuple[str, str]]) -> str:
    if not topics:
        return ""
    lines = ["## Conexiones", "", "### Temas", ""]
    for topic_name, _topic_slug in topics:
        lines.append(f"- [[Atlas/Temas/{safe_filename(topic_name, 80)}]]")
    lines += ["", "### Uso", "", "- Conecta esta nota con otras fuentes sobre el mismo tema dentro del vault."]
    return "\n".join(lines)

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

    # Evitar duplicados en la sección de artículos
    already_exists = f"`{page_id}`" in content
    
    page_line = f"- [p] **{page_title}** · {date_published or 's.d.'} · {page_url} · `{page_id}`\n"
    
    # Insertar en sección Artículos
    lines = content.splitlines(keepends=True)
    new_lines = []
    inserted = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if (not already_exists and not inserted and
            "## Artículos" in "\n".join(lines[:i+1]) and line.strip() == "---"):
            new_lines.pop()
            new_lines.append(page_line)
            new_lines.append(line)
            inserted = True
    
    # Actualizar wikilink en "Notas generadas"
    final_content = "".join(new_lines)
    if already_exists:
        final_content = re.sub(
            rf"^\s*-\s*\[(?: |x|p)\]\s+\*\*.*?\*\*\s+·\s+.*?\s+·\s+https?://.*?\s+·\s+`{re.escape(page_id)}`\s*$",
            page_line.strip(),
            final_content,
            flags=re.MULTILINE,
        )

    if not already_exists and not inserted:
        final_content = final_content.replace(
            "\n## Artículos",
            f"\n- [p] **{page_title}** · {date_published or 's.d.'} · {page_url} · `{page_id}`\n\n## Artículos"
        )
    
    if wikilink_page not in final_content:
        final_content = final_content.replace(
            "## Notas generadas\n",
            f"## Notas generadas\n\n{wikilink_page}"
        )
    
    # Actualizar total-articulos contando solo líneas de artículos
    article_count = len(
        re.findall(r"^\s*-\s*\[(?: |x|p)\]\s+\*\*.*?\*\*\s+·\s+.*?\s+·\s+https?://.*?\s+·\s+`[^`]+`\s*$",
                   final_content,
                   flags=re.MULTILINE)
    )
    final_content = re.sub(
        r"total-articulos: \d+",
        f"total-articulos: {article_count}",
        final_content,
        count=1
    )
    
    persona_path.write_text(final_content, encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 page_to_obsidian.py <URL>", file=sys.stderr)
        sys.exit(1)

    requested_url = sys.argv[1]
    
    # 1. Descargar página
    print(f">> [1/4] Descargando: {requested_url}", file=sys.stderr)
    try:
        html = fetch(requested_url)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    source_url, source_html, followed_home_article = resolve_preferred_source_url(requested_url, html)
    if followed_home_article:
        print(f">> [1.5/4] Portada detectada, usando primer artículo: {source_url}", file=sys.stderr)
    
    # 2. Extraer metadatos
    print(">> [2/4] Extrayendo metadatos...", file=sys.stderr)
    raw_title = extract_title(source_html)
    site_name = extract_site_name(source_url, source_html, raw_title)
    title = clean_title(raw_title, site_name)
    date_published = extract_date(source_html)
    author = extract_author(source_html)
    page_id = page_id_from_url(source_url)
    
    # 3. Convertir HTML → Markdown
    print(">> [3/4] Convirtiendo a Markdown...", file=sys.stderr)
    content_html = extract_content(source_html)
    markdown_content = html_to_markdown(content_html)
    topics = detect_topics(title, markdown_content)
    
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
            site_name, title, source_url, page_id,
            date_published or "s.d.", wikilink_page
        )
        created_now = True
    else:
        add_page_to_persona(
            persona_path, title, source_url, page_id,
            date_published or "s.d.", wikilink_page
        )
        created_now = False

    # 5. Guardar nota técnica en Atlas/Recursos/<Sitio>/
    source_tag = re.sub(r"[^\w-]", "-", safe_filename(site_name).lower())
    topic_tags = [topic_slug for _topic_name, topic_slug in topics]
    tag_list = ", ".join(["atlas", "recurso", "web", source_tag] + topic_tags)
    topic_names = ", ".join(f'"{topic_name}"' for topic_name, _topic_slug in topics)
    topic_section = build_topic_section(topics)

    note_text = f"""---
tags: [{tag_list}]
url: {source_url}
sitio: \"{site_name}\"
persona: \"[[Atlas/Personas/{safe_filename(site_name)}]]\"
author: \"{author or 's.d.'}\"
date-published: \"{date_published or 's.d.'}\"
date-saved: {date.today().isoformat()}
temas: [{topic_names}]
---

# {title}

> 👤 Por: [[Atlas/Personas/{safe_filename(site_name)}]]
> 📅 Publicado: {date_published or 's.d.'}
> 🔗 [Leer original]({source_url})

---

## Contenido

{markdown_content}

---

{topic_section}

---

## Fuentes
- [Artículo original]({source_url}) — {site_name}
"""
    target_note.write_text(note_text, encoding="utf-8")
    
    # Emitir JSON
    output = {
        "title": title,
        "site_name": site_name,
        "url": source_url,
        "requested_url": requested_url,
        "resolved_from_home": followed_home_article,
        "page_id": page_id,
        "date_published": date_published,
        "author": author,
        "content": markdown_content,
        "target_note": str(target_note),
        "saved": True,
        "fecha_guardado": date.today().isoformat(),
        "persona": {
            "name": site_name,
            "path": str(persona_path),
            "wikilink": f"[[Atlas/Personas/{safe_filename(site_name)}]]",
            "created_now": created_now,
        }
    }
    
    print("\n--- PAGE_TO_OBSIDIAN_JSON_START ---", file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False, indent=2), file=sys.stderr)
    print("--- PAGE_TO_OBSIDIAN_JSON_END ---", file=sys.stderr)

if __name__ == "__main__":
    main()
