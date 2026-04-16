#!/usr/bin/env python3
"""
web_to_obsidian.py  —  Skill WebToObsidian

Two-phase pipeline to capture a web site into an Obsidian Second Brain.
Supports: WordPress (REST API), RSS/Atom feeds, Sitemap.xml, static single-page sites.

  Phase 1 — Scan (default):
      python3 web_to_obsidian.py <URL>
      → Auto-detects site type, creates/updates Atlas/Personas/<SiteName>.md
        with a checklist of all articles/sections. Opens in Obsidian.
        Mark with [x] the items you want to process.

  Phase 2 — Process:
      python3 web_to_obsidian.py <URL> --process
      → Downloads and converts [x] items to Markdown notes in
        Atlas/Recursos/<SiteName>/.

Requirements: Python 3.9+ (stdlib only). Optional: pip install html2text
"""

import sys
import os
import re
import json
import time
import platform
from pathlib import Path
from datetime import date
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, quote
import xml.etree.ElementTree as ET

# ── Configuration ──────────────────────────────────────────────────────────────

_DEFAULT_VAULTS = {
    "Darwin":  "/Users/lunasoft/Library/Mobile Documents/iCloud~md~obsidian/Documents/Luna",
    "Windows": os.path.expanduser("~/Documents/Obsidian/MyVault"),
    "Linux":   os.path.expanduser("~/Documents/Obsidian/MyVault"),
}
VAULT = Path(
    os.environ.get("OBSIDIAN_VAULT")
    or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Linux"])
)
VAULT_NAME    = os.environ.get("OBSIDIAN_VAULT_NAME") or VAULT.name
PERSONAS_DIR  = VAULT / "Atlas" / "Personas"
RECURSOS_DIR  = VAULT / "Atlas" / "Recursos"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# ── HTTP helper ────────────────────────────────────────────────────────────────

def fetch(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={
        "User-Agent":      UA,
        "Accept":          "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "es,en;q=0.9",
    })
    with urlopen(req, timeout=timeout) as r:
        raw  = r.read()
        ct   = r.headers.get("Content-Type", "")
    # 1. Try charset from Content-Type header
    enc = None
    m = re.search(r"charset=([^\s;\"']+)", ct)
    if m:
        enc = m.group(1).strip('"').lower()
    # 2. Try charset from HTML <meta> tag
    if not enc:
        sniff = raw[:4096].decode("ascii", errors="replace")
        m2 = re.search(r'charset=["\']?([\w-]+)', sniff, re.IGNORECASE)
        if m2:
            enc = m2.group(1).lower()
    # 3. Default: try utf-8, fall back to latin-1
    if not enc:
        try:
            raw.decode("utf-8")
            enc = "utf-8"
        except UnicodeDecodeError:
            enc = "latin-1"
    return raw.decode(enc, errors="replace")

# ── HTML utilities ─────────────────────────────────────────────────────────────

def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)

def _decode_entities(text: str) -> str:
    for ent, ch in [
        ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
        ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " "), ("&nbsp", " "),
        ("&apos;", "'"), ("&mdash;", "—"), ("&ndash;", "–"),
        ("&hellip;", "…"), ("&laquo;", "«"), ("&raquo;", "»"),
    ]:
        text = text.replace(ent, ch)
    text = re.sub(r"&#(\d+);",          lambda m: chr(int(m.group(1))),     text)
    text = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)), text)
    # Clean up leftover whitespace from multiple &nbsp replacements
    text = re.sub(r"  +", " ", text)
    return text.strip()

def html_to_md(html: str) -> str:
    """Convert HTML to Markdown. Uses html2text if available."""
    try:
        import html2text  # type: ignore
        h = html2text.HTML2Text()
        h.ignore_links  = False
        h.ignore_images = True
        h.body_width    = 0
        h.unicode_snob  = True
        return h.handle(html).strip()
    except ImportError:
        return _basic_html_to_md(html)

def _extract_code_table(m: re.Match) -> str:
    """Convert <table bgcolor="#E4E4E4"> code blocks to ```vba fences."""
    inner = m.group(0)
    # Try to find the code cell by class (textoCodeNegro10) or by width="760"
    td_m = re.search(r'class=["\']textoCodeNegro10["\'][^>]*>(.*?)</td>',
                     inner, re.DOTALL | re.IGNORECASE)
    if not td_m:
        td_m = re.search(r'<td[^>]+width=["\']760(?:px)?["\'][^>]*>(.*?)</td>',
                         inner, re.DOTALL | re.IGNORECASE)
    if not td_m:
        return inner
    code = td_m.group(1)
    # Convert <br> to newlines before stripping tags
    code = re.sub(r"<br\s*/?>", "\n", code, flags=re.IGNORECASE)
    code = _strip_tags(code)
    # Decode HTML entities WITHOUT collapsing spaces (preserve indentation)
    for ent, ch in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                    ("&quot;", '"'), ("&#39;", "'"), ("&apos;", "'"),
                    ("&nbsp;", " "), ("&nbsp", " "),
                    ("&mdash;", "—"), ("&ndash;", "–")]:
        code = code.replace(ent, ch)
    code = re.sub(r"&#(\d+);",           lambda m2: chr(int(m2.group(1))),      code)
    code = re.sub(r"&#x([0-9a-fA-F]+);", lambda m2: chr(int(m2.group(1), 16)), code)
    # Normalize indentation: strip common leading whitespace per line
    lines = code.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    if non_empty:
        indent = min(len(ln) - len(ln.lstrip()) for ln in non_empty)
        lines  = [ln[indent:] if len(ln) >= indent else ln for ln in lines]
    code = "\n".join(lines).strip()
    # Collapse consecutive blank lines to single blank inside code block
    code = re.sub(r"\n{3,}", "\n\n", code)
    return f"\n```vba\n{code}\n```\n"

def _basic_html_to_md(html: str) -> str:
    """Stdlib-only HTML → Markdown converter."""
    # Remove noise tags
    for tag in ("script", "style", "nav", "footer", "aside", "noscript", "iframe", "form"):
        html = re.sub(rf"<{tag}[\s>].*?</{tag}>", "", html,
                      flags=re.DOTALL | re.IGNORECASE)
    # Code blocks — accessaplicaciones.com style: <table bgcolor="#E4E4E4">
    html = re.sub(
        r"<table\b[^>]+bgcolor=[\"']#E4E4E4[\"'][^>]*>.*?</table>",
        _extract_code_table,
        html, flags=re.DOTALL | re.IGNORECASE
    )
    # Code blocks (before other replacements)
    html = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        lambda m: f"\n```\n{_strip_tags(m.group(1))}\n```\n",
        html, flags=re.DOTALL | re.IGNORECASE
    )
    html = re.sub(
        r"<code[^>]*>(.*?)</code>",
        lambda m: f"`{_strip_tags(m.group(1))}`",
        html, flags=re.DOTALL | re.IGNORECASE
    )
    # Headings
    for n in range(6, 0, -1):
        html = re.sub(
            rf"<h{n}[^>]*>(.*?)</h{n}>",
            lambda m, level=n: f"\n{'#' * level} {_strip_tags(m.group(1)).strip()}\n",
            html, flags=re.DOTALL | re.IGNORECASE
        )
    # Lists
    html = re.sub(r"<li[^>]*>(.*?)</li>",
                  lambda m: f"- {_strip_tags(m.group(1)).strip()}\n",
                  html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<[ou]l[^>]*>",  "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</[ou]l>",       "\n", html, flags=re.IGNORECASE)
    # Inline formatting
    html = re.sub(r"<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>",
                  lambda m: f"**{_strip_tags(m.group(1)).strip()}**",
                  html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<(?:em|i)[^>]*>(.*?)</(?:em|i)>",
                  lambda m: f"*{_strip_tags(m.group(1)).strip()}*",
                  html, flags=re.DOTALL | re.IGNORECASE)
    # Links
    html = re.sub(
        r"<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>",
        lambda m: f"[{_strip_tags(m.group(2)).strip()}]({m.group(1)})",
        html, flags=re.DOTALL | re.IGNORECASE
    )
    # Block elements
    html = re.sub(r"<br\s*/?>", "\n",  html, flags=re.IGNORECASE)
    html = re.sub(r"<p[^>]*>(.*?)</p>",
                  lambda m: f"\n{_strip_tags(m.group(1)).strip()}\n",
                  html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"</?div[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Strip remaining tags and clean
    result = _decode_entities(_strip_tags(html))
    # Strip leading whitespace from each line outside code blocks
    lines    = result.split("\n")
    in_code  = False
    cleaned  = []
    for ln in lines:
        stripped = ln.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            cleaned.append(stripped)
        elif in_code:
            cleaned.append(ln)          # preserve indentation inside code
        else:
            cleaned.append(stripped)    # strip outside code
    result = "\n".join(cleaned)
    result = re.sub(r"\n{3,}", "\n\n", result)
    # Remove back-to-top artifacts: [](#arriba) or similar empty anchor links
    result = re.sub(r"\[[^\]]*\]\(#[^\)]*\)", "", result)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()

# ── Content extraction ─────────────────────────────────────────────────────────

def extract_article_html(html: str) -> str:
    """Extract main article body from a full page HTML."""
    for pattern in (
        r"<article[^>]*>(.*?)</article>",
        r"<div[^>]+class=[\"'][^\"']*(?:post-content|entry-content|article-content|article-body)[^\"']*[\"'][^>]*>(.*?)</div\s*>(?=\s*</)",
        r"<div[^>]+class=[\"'][^\"']*(?:content|post|entry)[^\"']*[\"'][^>]*>(.*?)</div\s*>(?=\s*</)",
        r"<main[^>]*>(.*?)</main>",
        r"<div[^>]+id=[\"'](?:content|main|post|article)[\"'][^>]*>(.*?)</div>",
    ):
        m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if m and len(m.group(1)) > 300:
            return m.group(1)
    m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else html

def extract_section_by_anchor(html: str, anchor: str) -> str:
    """Extract a named section from a single-page site by its anchor."""
    start_pos = -1
    for p in (
        rf'<a\b[^>]+\bid=["\']?{re.escape(anchor)}["\']?[^>]*>',
        rf'<[^>]+\bid=["\']?{re.escape(anchor)}["\']?[^>]*>',
        rf"<a\s+name=[\"']?{re.escape(anchor)}[\"']?[^>]*>",
    ):
        m = re.search(p, html, re.IGNORECASE)
        if m:
            start_pos = m.start()
            break

    if start_pos == -1:
        return extract_article_html(html)

    # Find next section boundary: next <a id="..."> section anchor
    next_m = re.search(
        rf'<a\b[^>]+\bid=["\'][^"\']+["\'][^>]*>(?=.*?class=["\'][^"\']*(?:Titulo|titulo|title)[^"\']*["\'])'
        rf'|<a\s+name=["\'][\w-]+["\']'
        rf'|<h[123][^>]+id=',
        html[start_pos + 50:],
        re.IGNORECASE | re.DOTALL
    )
    if not next_m:
        # Fallback: next <a id="m\d+|rt\d+|sq\d+"> pattern
        next_m = re.search(
            r'<a\b[^>]+\bid=["\'](?:m\d+|rt\d+|sq\d+|mar\w+|ot\d+)["\']',
            html[start_pos + 50:],
            re.IGNORECASE
        )
    if next_m:
        return html[start_pos: start_pos + 50 + next_m.start()]
    return html[start_pos:]

def extract_page_title(html: str) -> str:
    for pattern in (
        r"<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"']([^\"']+)",
        r"<meta[^>]+content=[\"']([^\"']+)[\"'][^>]+property=[\"']og:title",
        r"<h1[^>]*>(.*?)</h1>",
        r"<title[^>]*>(.*?)</title>",
    ):
        m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if m:
            return _decode_entities(_strip_tags(m.group(1)).strip())
    return "Sin título"

def extract_pub_date(html: str) -> str:
    for pattern in (
        r"<time[^>]+datetime=[\"'](\d{4}-\d{2}-\d{2})",
        r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',
        r"<meta[^>]+(?:article:published_time|datePublished)[^>]+content=[\"'](\d{4}-\d{2}-\d{2})",
    ):
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            return m.group(1)[:10]
    return ""

# ── Utilities ──────────────────────────────────────────────────────────────────

def safe_name(s: str, max_len: int = 80) -> str:
    return re.sub(r'[\\/*?:"<>|#\[\]]', "", s).strip()[:max_len].strip()

def url_to_slug(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] if "/" in path else path
    slug = re.sub(r"[^\w-]", "-", slug).strip("-")[:50]
    if not slug:
        slug = re.sub(r"[^\w-]", "-", urlparse(url).netloc.replace("www.", ""))[:30]
    return slug

def site_name_from_url(url: str) -> str:
    netloc = urlparse(url).netloc.replace("www.", "")
    name = netloc.split(".")[0] if "." in netloc else netloc
    return name.replace("-", " ").title()

# ── Site type detection ────────────────────────────────────────────────────────

def detect_site(base_url: str) -> tuple[str, list[dict]]:
    """
    Auto-detect site type and return (site_type, items).
    Order: WordPress REST API → RSS/Atom → Sitemap → Single-page
    """
    base = base_url.rstrip("/")

    # 1. WordPress REST API
    try:
        api_url = f"{base}/wp-json/wp/v2/posts?per_page=1&_fields=id"
        data = json.loads(fetch(api_url))
        if isinstance(data, list):
            print(">> Detectado: WordPress REST API", file=sys.stderr)
            return "wordpress", scan_wordpress_api(base)
    except Exception:
        pass

    # 2. RSS / Atom
    for feed_path in ("/feed", "/feed/", "/rss", "/rss.xml", "/atom.xml",
                      "/contenido.xml", "/index.xml"):
        try:
            feed_url = base + feed_path
            content = fetch(feed_url)
            if any(tag in content for tag in ("<rss", "<feed", "<channel>", "<item>")):
                print(f">> Detectado: RSS en {feed_url}", file=sys.stderr)
                items = parse_rss(content)
                if items:
                    return "rss", items
        except Exception:
            continue

    # 3. Sitemap
    for sitemap_path in ("/sitemap.xml", "/sitemap_index.xml"):
        try:
            sitemap_url = base + sitemap_path
            content = fetch(sitemap_url)
            if "<urlset" in content or "<sitemapindex" in content:
                print(f">> Detectado: Sitemap en {sitemap_url}", file=sys.stderr)
                items = parse_sitemap(content, sitemap_url, base)
                if items:
                    return "sitemap", items
        except Exception:
            continue

    # 4. Single-page fallback
    print(">> Detectado: Página estática (secciones)", file=sys.stderr)
    try:
        content = fetch(base_url)
        items = scan_single_page(content, base_url)
        return "single-page", items
    except Exception as e:
        print(f"ERROR: No se pudo acceder a {base_url}: {e}", file=sys.stderr)
        sys.exit(1)

# ── Scanners ───────────────────────────────────────────────────────────────────

def scan_wordpress_api(base_url: str) -> list[dict]:
    items = []
    page  = 1
    base  = base_url.rstrip("/")
    while True:
        url = (f"{base}/wp-json/wp/v2/posts"
               f"?per_page=100&page={page}&_fields=id,title,link,date,slug")
        try:
            data = json.loads(fetch(url))
        except Exception:
            break
        if not isinstance(data, list) or not data:
            break
        for post in data:
            title_raw = post.get("title", {})
            title = _decode_entities(_strip_tags(
                title_raw.get("rendered", "") if isinstance(title_raw, dict) else str(title_raw)
            ))
            post_url = post.get("link", "")
            items.append({
                "title": title,
                "url":   post_url,
                "date":  post.get("date", "")[:10],
                "slug":  post.get("slug", "") or url_to_slug(post_url),
            })
        print(f"   Página {page}: {len(data)} posts (total: {len(items)})", file=sys.stderr)
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.3)
    return items

def parse_rss(xml_content: str) -> list[dict]:
    items = []
    try:
        xml_clean = re.sub(r"<\?xml[^>]+\?>", "", xml_content)
        xml_clean = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", xml_clean, flags=re.DOTALL)
        xml_clean = re.sub(r'\s+xmlns[^=]*="[^"]*"', "", xml_clean)
        root = ET.fromstring(xml_clean)
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link")  or "").strip()
            pub   = (item.findtext("pubDate") or item.findtext("date") or "").strip()
            date_str = ""
            try:
                from email.utils import parsedate_to_datetime
                date_str = parsedate_to_datetime(pub).strftime("%Y-%m-%d")
            except Exception:
                m = re.search(r"(\d{4}-\d{2}-\d{2})", pub)
                if m:
                    date_str = m.group(1)
            if link:
                items.append({
                    "title": _decode_entities(title) or "Sin título",
                    "url":   link,
                    "date":  date_str,
                    "slug":  url_to_slug(link),
                })
    except ET.ParseError:
        # Regex fallback
        for block in re.finditer(r"<item>(.*?)</item>", xml_content, re.DOTALL):
            item_xml = block.group(1)
            title_m  = re.search(r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item_xml, re.DOTALL)
            link_m   = re.search(r"<link>(.*?)</link>", item_xml, re.DOTALL)
            date_m   = re.search(r"<pubDate>(.*?)</pubDate>", item_xml, re.DOTALL)
            if link_m:
                link_url = link_m.group(1).strip()
                pub      = date_m.group(1).strip() if date_m else ""
                date_str = ""
                d = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})", pub)
                if d:
                    date_str = d.group(1)
                items.append({
                    "title": _decode_entities(title_m.group(1).strip()) if title_m else "Sin título",
                    "url":   link_url,
                    "date":  date_str,
                    "slug":  url_to_slug(link_url),
                })
    return items

def parse_sitemap(xml_content: str, sitemap_url: str, base_url: str) -> list[dict]:
    items = []
    if "<sitemapindex" in xml_content:
        for sub_url in re.findall(r"<loc>(.*?)</loc>", xml_content)[:5]:
            try:
                items.extend(parse_sitemap(fetch(sub_url.strip()), sub_url.strip(), base_url))
                time.sleep(0.3)
            except Exception:
                continue
        return items

    SKIP = re.compile(
        r"\.(jpg|jpeg|png|gif|pdf|zip|css|js|svg|webp)$"
        r"|/tag/|/category/|/page/\d+|/wp-content/|/feed/",
        re.IGNORECASE
    )
    for block in re.finditer(r"<url>(.*?)</url>", xml_content, re.DOTALL):
        url_block = block.group(1)
        loc     = re.search(r"<loc>(.*?)</loc>",         url_block)
        lastmod = re.search(r"<lastmod>(.*?)</lastmod>",  url_block)
        if not loc:
            continue
        url = loc.group(1).strip()
        if SKIP.search(url):
            continue
        date_str = lastmod.group(1).strip()[:10] if lastmod else ""
        slug     = url_to_slug(url)
        title    = slug.replace("-", " ").replace("_", " ").title()
        items.append({"title": title, "url": url, "date": date_str, "slug": slug})
    return items

def scan_single_page(html: str, page_url: str) -> list[dict]:
    """Extract sections from a static page using named anchors and headings."""
    items     = []
    seen      = set()
    base_url  = page_url.split("#")[0]

    SKIP_IDS = {"menu", "nav", "top", "arriba", "inicio", "home", "header", "footer"}

    # Pattern 1: <a id="m01" ...>Title text</a>  (accessaplicaciones.com style)
    for m in re.finditer(
        r'<a\b[^>]+\bid=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        html, re.DOTALL | re.IGNORECASE
    ):
        anchor    = m.group(1).strip()
        title_raw = m.group(2).strip()
        title     = _decode_entities(_strip_tags(title_raw)).strip()
        # Only keep non-empty titles that look like section headers (>4 chars, not nav links)
        if (title and len(title) > 4 and anchor not in seen
                and anchor.lower() not in SKIP_IDS
                and not re.search(r'^https?://', title)):
            seen.add(anchor)
            items.append({
                "title": title,
                "url":   f"{base_url}#{anchor}",
                "date":  "",
                "slug":  anchor[:50],
            })

    # Pattern 2: <a name="anchor"> before/inside a heading
    if not items:
        for m in re.finditer(
            r"<a\s+name=[\"']?([\w-]+)[\"']?[^>]*>\s*(?:</a>)?\s*<h[23][^>]*>(.*?)</h[23]>"
            r"|<h[23][^>]*>\s*<a\s+name=[\"']?([\w-]+)[\"']?[^>]*>(.*?)</a>",
            html, re.DOTALL | re.IGNORECASE
        ):
            anchor    = (m.group(1) or m.group(3) or "").strip()
            title_raw = (m.group(2) or m.group(4) or "").strip()
            title     = _decode_entities(_strip_tags(title_raw))
            if title and anchor and anchor not in seen:
                seen.add(anchor)
                items.append({
                    "title": title,
                    "url":   f"{base_url}#{anchor}",
                    "date":  "",
                    "slug":  anchor[:50],
                })

    # Pattern 3: headings with id attribute
    if not items:
        for m in re.finditer(
            r"<h[23][^>]+id=[\"']([^\"']+)[\"'][^>]*>(.*?)</h[23]>",
            html, re.DOTALL | re.IGNORECASE
        ):
            anchor = m.group(1).strip()
            title  = _decode_entities(_strip_tags(m.group(2)).strip())
            if title and anchor not in seen and anchor.lower() not in SKIP_IDS:
                seen.add(anchor)
                items.append({
                    "title": title,
                    "url":   f"{base_url}#{anchor}",
                    "date":  "",
                    "slug":  anchor[:50],
                })

    # Pattern 4: any h2 (last resort)
    if not items:
        for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.DOTALL | re.IGNORECASE):
            title = _decode_entities(_strip_tags(m.group(1)).strip())
            if title and len(title) > 3:
                slug = re.sub(r"[^\w-]", "-", title.lower())[:50].strip("-")
                if slug not in seen:
                    seen.add(slug)
                    items.append({"title": title, "url": page_url, "date": "", "slug": slug})

    return items

# ── Index management ───────────────────────────────────────────────────────────

def site_index_path(site_name: str) -> Path:
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    return PERSONAS_DIR / f"{safe_name(site_name)}.md"

def load_existing_index(path: Path) -> dict[str, str]:
    states = {}
    if not path.exists():
        return states
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"- \[([ xXpP✓])\].*`([^`]+)`", line)
        if m:
            states[m.group(2)] = m.group(1).strip()
    return states

def write_index(path: Path, site_name: str, site_url: str, site_type: str,
                items: list[dict], existing_states: dict):
    today = date.today().isoformat()
    lines = [
        "---",
        "tags: [atlas, persona, web]",
        f'sitio: "{site_name}"',
        f'url: "{site_url}"',
        f'tipo: "{site_type}"',
        f"updated: {today}",
        f"total-items: {len(items)}",
        "---",
        "",
        f"# {site_name} — Índice web",
        "",
        f"> Sitio web capturado ({site_type}) con {len(items)} artículos/secciones.",
        f"> Marca con `[x]` los que quieras procesar con WebToObsidian.",
        f"> Los marcados con `[p]` ya han sido procesados (notas en Atlas/Recursos/{safe_name(site_name)}/).",
        "",
        "---",
        "",
        "## Artículos",
        "",
    ]
    for item in items:
        slug  = item["slug"]
        state = existing_states.get(slug, " ") or " "
        mark  = f"[{state}]"
        title = item["title"].replace("|", "–")[:80]
        parts = [p for p in [item.get("date", ""), item.get("url", "")] if p]
        meta  = " · ".join(parts)
        lines.append(f"- {mark} **{title}** · {meta} · `{slug}`")

    lines += [
        "",
        "---",
        "",
        "## Notas generadas",
        "",
        "> Los artículos procesados aparecerán aquí como wikilinks.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")

def update_index_processed(path: Path, slug: str):
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    content = re.sub(
        rf"(- \[)[xX](\].*`{re.escape(slug)}`)",
        r"\1p\2",
        content
    )
    path.write_text(content, encoding="utf-8")

def append_wikilinks_to_index(path: Path, wikilinks: list[str]):
    if not path.exists() or not wikilinks:
        return
    content = path.read_text(encoding="utf-8")
    marker  = "> Los artículos procesados aparecerán aquí como wikilinks."
    insert  = "\n" + "\n".join(wikilinks)
    if marker in content:
        content = content.replace(marker, marker + insert, 1)
    else:
        content += insert + "\n"
    path.write_text(content, encoding="utf-8")

# ── Obsidian opener ────────────────────────────────────────────────────────────

def open_in_obsidian(abs_path: Path):
    rel     = abs_path.relative_to(VAULT)
    encoded = quote(str(rel).replace("\\", "/"), safe="/")
    uri     = f"obsidian://open?vault={quote(VAULT_NAME)}&file={encoded}"
    sys_name = platform.system()
    if sys_name == "Darwin":
        os.system(f'open "{uri}"')
    elif sys_name == "Windows":
        os.system(f'cmd /c start "" "{uri}"')
    else:
        os.system(f'xdg-open "{uri}"')

# ── Note generation ────────────────────────────────────────────────────────────

def process_item(item: dict, site_name: str, page_cache: dict) -> Path:
    """Download, convert and save one article/section as a Markdown note."""
    url       = item["url"]
    title     = item["title"]
    item_date = item.get("date", "")
    anchor    = urlparse(url).fragment
    base_url  = url.split("#")[0]

    # Fetch with cache (single-page sites share the same base URL)
    if base_url not in page_cache:
        print(f"   Descargando: {base_url}", file=sys.stderr)
        page_cache[base_url] = fetch(base_url)
    html = page_cache[base_url]

    # Extract content
    article_html = (
        extract_section_by_anchor(html, anchor)
        if anchor
        else extract_article_html(html)
    )

    # Refine title and date if missing
    if not title or title == "Sin título":
        title = extract_page_title(html)
    if not item_date:
        item_date = extract_pub_date(html)

    content_md = html_to_md(article_html)

    # Clean up content: strip trailing whitespace per line, remove % artifacts
    content_md = "\n".join(ln.rstrip() for ln in content_md.splitlines())
    content_md = re.sub(r"#ai-generated[^\n]*", "", content_md).strip()

    # Build note
    note_title  = safe_name(title)
    source_tag  = re.sub(r"[^\w-]", "-", safe_name(site_name).lower())
    note_lines  = [
        "---",
        f"tags: [atlas, recurso, web, {source_tag}]",
        f'fuente: "{site_name}"',
        f'url: "{url}"',
        f'fecha: "{item_date}"',
        f"capturado: {date.today().isoformat()}",
        "---",
        "",
        f"# {title}",
        "",
        f"> [Fuente original]({url}){' — ' + item_date if item_date else ''}",
        "",
        "---",
        "",
        content_md,
        "",
        "#ai-generated",
    ]

    site_dir   = RECURSOS_DIR / safe_name(site_name)
    site_dir.mkdir(parents=True, exist_ok=True)
    note_path  = site_dir / f"{note_title}.md"
    note_path.write_text("\n".join(note_lines), encoding="utf-8")
    print(f"   ✓ {note_path.relative_to(VAULT)}", file=sys.stderr)
    return note_path

# ── Phase 1: Scan ──────────────────────────────────────────────────────────────

def phase_scan(url: str):
    base_url  = url.rstrip("/")
    site_name = site_name_from_url(base_url)

    print(f">> Escaneando: {base_url}", file=sys.stderr)
    print(f">> Nombre del sitio: {site_name}", file=sys.stderr)

    site_type, items = detect_site(base_url)

    if not items:
        print(f"ERROR: No se encontraron artículos en {base_url}", file=sys.stderr)
        sys.exit(1)

    print(f">> {len(items)} artículos/secciones encontrados ({site_type})", file=sys.stderr)

    index_path = site_index_path(site_name)
    existing   = load_existing_index(index_path)
    write_index(index_path, site_name, base_url, site_type, items, existing)

    print(f">> Índice guardado: {index_path}", file=sys.stderr)
    print(f">> Marca con [x] los artículos que quieras procesar,", file=sys.stderr)
    print(f"   luego ejecuta: python3 web_to_obsidian.py {url} --process", file=sys.stderr)

    open_in_obsidian(index_path)

# ── Phase 2: Process ───────────────────────────────────────────────────────────

def phase_process(url: str):
    base_url  = url.rstrip("/")
    site_name = site_name_from_url(base_url)
    index_path = site_index_path(site_name)

    if not index_path.exists():
        print(f"ERROR: Índice no encontrado: {index_path}", file=sys.stderr)
        print(f"   Ejecuta primero: python3 web_to_obsidian.py {url}", file=sys.stderr)
        sys.exit(1)

    # Parse [x] lines from index
    # Format: - [x] **Title** · date · https://url · `slug`
    selected = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"- \[[xX]\]", line):
            continue
        m = re.match(r"- \[[xX]\] \*\*(.*?)\*\*(.*?)`([^`]+)`\s*$", line)
        if not m:
            continue
        title  = m.group(1).strip()
        meta   = m.group(2).strip(" ·")
        slug   = m.group(3).strip()
        parts  = [p.strip() for p in meta.split("·") if p.strip()]
        item_url  = next((p for p in parts if p.startswith("http")), base_url)
        item_date = next((p for p in parts if re.match(r"\d{4}-\d{2}-\d{2}", p)), "")
        selected.append({"title": title, "url": item_url, "date": item_date, "slug": slug})

    if not selected:
        print(">> No hay artículos marcados con [x].", file=sys.stderr)
        print(f"   Abre {index_path} en Obsidian y marca con [x] lo que quieras procesar.", file=sys.stderr)
        sys.exit(0)

    print(f">> Procesando {len(selected)} artículo(s)...", file=sys.stderr)

    page_cache = {}
    wikilinks  = []

    for i, item in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}] {item['title']}", file=sys.stderr)
        try:
            note_path = process_item(item, site_name, page_cache)
            update_index_processed(index_path, item["slug"])
            stem = note_path.stem
            wikilinks.append(
                f"- [[Atlas/Recursos/{safe_name(site_name)}/{stem}]]"
                f" — {item.get('date', '')} · {item['title']}"
            )
        except Exception as e:
            print(f"   ✗ Error: {e}", file=sys.stderr)
        time.sleep(0.5)

    append_wikilinks_to_index(index_path, wikilinks)
    print(
        f"\n>> Listo. {len(wikilinks)} nota(s) en Atlas/Recursos/{safe_name(site_name)}/",
        file=sys.stderr
    )
    open_in_obsidian(index_path)

# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url

    if "--process" in sys.argv:
        phase_process(url)
    else:
        phase_scan(url)

if __name__ == "__main__":
    main()
