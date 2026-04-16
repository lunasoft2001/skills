#!/usr/bin/env python3
"""
enrich_second_brain.py

Enriquece notas ya capturadas en Obsidian para conectar el grafo por conceptos,
no solo por fuente. Crea notas-hub en Atlas/Temas y agrega secciones de
Conexiones a cada nota con temas, relacionadas y referencias cruzadas.

Uso:
    python3 enrich_second_brain.py
"""

import os
import platform
import re
from pathlib import Path
from urllib.parse import unquote
from audit_vault import write_audit_report

_DEFAULT_VAULTS = {
    "Darwin": "/Users/lunasoft/Library/Mobile Documents/iCloud~md~obsidian/Documents/Luna",
    "Windows": os.path.expanduser("~/Documents/Obsidian/MyVault"),
    "Linux": os.path.expanduser("~/Documents/Obsidian/MyVault"),
}

VAULT = Path(
    os.environ.get("OBSIDIAN_VAULT")
    or _DEFAULT_VAULTS.get(platform.system(), _DEFAULT_VAULTS["Darwin"])
)
RECURSOS_DIR = VAULT / "Atlas" / "Recursos"
TEMAS_DIR = VAULT / "Atlas" / "Temas"
TARGET_SOURCES = {"Accessaplicaciones", "Llodax", "Soydba", "Luna-soft"}
# Notas de YouTube están directamente en Atlas/Recursos/ (con campo canal:)
# o en Atlas/Recursos/Transcripciones/
YOUTUBE_SOURCES = {"Transcripciones"}  # subcarpetas de vídeos YouTube

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
    ("IA", "ia", [r"\binteligencia artificial\b", r"\b(?:ai|ia)\b", r"\bllm\b", r"\bgpt\b", r"\bchatgpt\b", r"\bcopilot\b"]),
    ("Python", "python", [r"\bpython\b", r"\bpypi\b", r"\bpip\b"]),
    ("Power Automate", "power-automate", [r"power automate", r"\bflow\b", r"power platform"]),
]
SEMANTIC_TAGS = {topic_slug for _topic_name, topic_slug, _patterns in TOPIC_SPECS}


def safe_name(value: str, max_len: int = 80) -> str:
    value = re.sub(r'[\\/*?:"<>|#\[\]]', '', value)
    return value.strip()[:max_len].strip()


def parse_frontmatter(text: str):
    if not text.startswith('---\n'):
        return [], text
    end = text.find('\n---\n', 4)
    if end == -1:
        return [], text
    frontmatter = text[4:end].splitlines()
    body = text[end + 5 :]
    return frontmatter, body


def extract_frontmatter_value(lines, key):
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return ""


def parse_tags(raw: str):
    raw = raw.strip()
    if not raw.startswith('[') or not raw.endswith(']'):
        return []
    inner = raw[1:-1].strip()
    if not inner:
        return []
    return [part.strip().strip('"') for part in inner.split(',') if part.strip()]


def set_frontmatter_value(lines, key, value):
    prefix = f"{key}:"
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = f"{prefix} {value}"
            return lines
    lines.append(f"{prefix} {value}")
    return lines


def detect_topics(title: str, content: str):
    haystack = f"{title}\n{content}".lower()
    topics = []
    for topic_name, topic_slug, patterns in TOPIC_SPECS:
        if any(re.search(pattern, haystack, re.IGNORECASE) for pattern in patterns):
            topics.append((topic_name, topic_slug))
    return topics


def extract_title(text: str, fallback: str):
    frontmatter, body = parse_frontmatter(text)
    match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return fallback


def build_connections_section(note, related_links, cross_links):
    topic_links = [f"- [[Atlas/Temas/{safe_name(topic_name)}]]" for topic_name, _topic_slug in note['topics']]
    lines = ["## Conexiones", "", "### Temas", ""]
    lines.extend(topic_links or ["- Pendiente de clasificar"])
    lines += ["", "### Relacionadas", ""]
    lines.extend(related_links or ["- Sin relacionadas detectadas todavía"])
    lines += ["", "### Referencias cruzadas", ""]
    lines.extend(cross_links or ["- Sin referencias cruzadas detectadas"])
    return "\n".join(lines)


def remove_connections_section(body: str) -> str:
    body = re.sub(r'\n## Conexiones\n.*?(?=\n## Fuentes\n|\n#ai-generated\n|\Z)', '\n', body, flags=re.S)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip() + '\n'


def insert_connections(body: str, section: str) -> str:
    if '\n## Fuentes\n' in body:
        return body.replace('\n## Fuentes\n', f'\n{section}\n\n## Fuentes\n', 1)
    if '\n#ai-generated' in body:
        return body.replace('\n#ai-generated', f'\n{section}\n\n#ai-generated', 1)
    return body.rstrip() + f'\n\n{section}\n'


def _make_note_entry(path):
    """Construye el dict de una nota a partir de su ruta."""
    text = path.read_text(encoding='utf-8')
    frontmatter, body = parse_frontmatter(text)
    body_for_detection = remove_connections_section(body)
    title = extract_title(text, path.stem)
    url = extract_frontmatter_value(frontmatter, 'url').strip().strip('"')
    source = extract_frontmatter_value(frontmatter, 'fuente').strip().strip('"')
    if not source:
        source = (extract_frontmatter_value(frontmatter, 'canal').strip().strip('"') or
                  extract_frontmatter_value(frontmatter, 'sitio').strip().strip('"') or
                  path.parent.name)
    topics = detect_topics(title, body_for_detection[:6000])
    return {
        'path': path,
        'rel_path': path.relative_to(VAULT).as_posix(),
        'wikilink': f"[[{path.relative_to(VAULT).as_posix()[:-3]}]]",
        'title': title,
        'source': source,
        'url': url,
        'frontmatter': frontmatter,
        'body': body,
        'body_for_detection': body_for_detection,
        'topics': topics,
    }


def collect_notes():
    notes = []
    for path in RECURSOS_DIR.rglob('*.md'):
        try:
            rel = path.relative_to(RECURSOS_DIR)
        except ValueError:
            continue
        if not rel.parts:
            continue
        source_name = rel.parts[0]
        # Fuentes web conocidas
        if source_name in TARGET_SOURCES:
            notes.append(_make_note_entry(path))
            continue
        # Transcripciones de YouTube
        if source_name in YOUTUBE_SOURCES:
            notes.append(_make_note_entry(path))
            continue
        # Notas de vídeo YouTube (directamente en Atlas/Recursos/)
        if len(rel.parts) == 1:
            text = path.read_text(encoding='utf-8')
            if 'canal:' in text or 'video-id:' in text:
                notes.append(_make_note_entry(path))
    return notes


def score_related(note, other):
    shared = {topic_name for topic_name, _slug in note['topics']} & {topic_name for topic_name, _slug in other['topics']}
    if not shared:
        return -1
    score = len(shared) * 10
    if note['source'] != other['source']:
        score += 5
    tokens_a = {token for token in re.findall(r'\w+', note['title'].lower()) if len(token) > 3}
    tokens_b = {token for token in re.findall(r'\w+', other['title'].lower()) if len(token) > 3}
    score += len(tokens_a & tokens_b)
    return score


def main():
    TEMAS_DIR.mkdir(parents=True, exist_ok=True)
    notes = collect_notes()
    url_map = {note['url']: note for note in notes if note['url']}

    topic_index = {}
    for note in notes:
        for topic_name, topic_slug in note['topics']:
            topic_index.setdefault((topic_name, topic_slug), []).append(note)

    for note in notes:
        tags = parse_tags(extract_frontmatter_value(note['frontmatter'], 'tags'))
        source_tag = re.sub(r'[^\w-]', '-', safe_name(note['source']).lower())
        topic_tags = [topic_slug for _topic_name, topic_slug in note['topics']]
        merged_tags = []
        base_tags = [tag for tag in tags if tag not in SEMANTIC_TAGS and tag != source_tag]
        for tag in base_tags + ['atlas', 'recurso', source_tag] + topic_tags:
            if tag and tag not in merged_tags:
                merged_tags.append(tag)
        topic_names = [topic_name for topic_name, _topic_slug in note['topics']]

        related = []
        for other in notes:
            if other['path'] == note['path']:
                continue
            score = score_related(note, other)
            if score <= 0:
                continue
            related.append((score, other))
        related.sort(key=lambda item: (-item[0], item[1]['title'].lower()))
        related_links = []
        seen_links = set()
        for _score, other in related:
            line = f"- {other['wikilink']} — {other['source']}"
            if line in seen_links:
                continue
            related_links.append(line)
            seen_links.add(line)
            if len(related_links) >= 5:
                break

        cross_links = []
        for url, other in url_map.items():
            if other['path'] == note['path']:
                continue
            if url and url in note['body']:
                cross_links.append(f"- {other['wikilink']} — referencia por URL")
        cross_links = sorted(dict.fromkeys(cross_links))[:5]

        connections = build_connections_section(note, related_links, cross_links)
        body_clean = remove_connections_section(note['body'])
        body_final = insert_connections(body_clean, connections)
        frontmatter_lines = list(note['frontmatter'])
        frontmatter_lines = set_frontmatter_value(frontmatter_lines, 'tags', '[' + ', '.join(merged_tags) + ']')
        frontmatter_lines = set_frontmatter_value(frontmatter_lines, 'temas', '[' + ', '.join(f'"{topic_name}"' for topic_name in topic_names) + ']')
        new_text = '---\n' + '\n'.join(frontmatter_lines) + '\n---\n' + body_final
        note['path'].write_text(new_text, encoding='utf-8')

    for (topic_name, topic_slug), topic_notes in sorted(topic_index.items(), key=lambda item: item[0][0].lower()):
        if len(topic_notes) < 2:
            continue
        topic_path = TEMAS_DIR / f"{safe_name(topic_name)}.md"
        lines = [
            '---',
            f'tags: [atlas, tema, {topic_slug}]',
            f'tema: "{topic_name}"',
            f'total-notas: {len(topic_notes)}',
            '---',
            '',
            f'# {topic_name}',
            '',
            '> Nota-hub generada automáticamente para conectar recursos del second brain por concepto.',
            '',
            '## Notas relacionadas',
            '',
        ]
        for note in sorted(topic_notes, key=lambda item: (item['source'].lower(), item['title'].lower())):
            lines.append(f"- {note['wikilink']} — {note['source']}")
        topic_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'NOTES_ENRICHED {len(notes)}')
    print(f'TOPIC_NOTES {sum(1 for notes_list in topic_index.values() if len(notes_list) >= 2)}')
    report_path = write_audit_report(VAULT, notes, topic_index)
    print(f'AUDIT_REPORT {report_path}')


if __name__ == '__main__':
    main()
