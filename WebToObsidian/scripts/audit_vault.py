#!/usr/bin/env python3
"""
audit_vault.py

Genera una auditoría de salud del vault Obsidian a partir de las notas
ya enriquecidas por enrich_second_brain.py.

Uso directo:
    python3 audit_vault.py
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re


def _extract_frontmatter_date(frontmatter: list[str]) -> str:
    """Devuelve la fecha más relevante encontrada en frontmatter (YYYY-MM-DD)."""
    date_keys = ["capturado", "capturado", "date-guardado", "fecha-guardado", "captured", "updated"]
    for key in date_keys:
        prefix = f"{key}:"
        for line in frontmatter:
            if line.startswith(prefix):
                raw = line[len(prefix):].strip().strip('"')
                m = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
                if m:
                    return m.group(1)
    return ""


def _status_for_count(count: int) -> str:
    if count >= 20:
        return "OK"
    if count >= 10:
        return "MEJORABLE"
    return "BAJO"


def build_audit_report(vault: Path, notes: list[dict], topic_index: dict) -> str:
    generated = datetime.now().isoformat(timespec="seconds")

    source_counts: dict[str, int] = defaultdict(int)
    source_latest: dict[str, str] = {}

    notes_with_topics = 0
    for note in notes:
        source = note.get("source") or "Desconocida"
        source_counts[source] += 1

        if note.get("topics"):
            notes_with_topics += 1

        note_date = _extract_frontmatter_date(note.get("frontmatter", []))
        if note_date and (source not in source_latest or note_date > source_latest[source]):
            source_latest[source] = note_date

    total_notes = len(notes)
    total_topics = len(topic_index)
    total_sources = len(source_counts)

    lines: list[str] = [
        "---",
        "tags: [atlas, meta, auditoria]",
        f"generated: {generated}",
        f"total-notas: {total_notes}",
        f"notas-con-temas: {notes_with_topics}",
        f"total-temas: {total_topics}",
        f"total-fuentes: {total_sources}",
        "---",
        "",
        f"# Auditoria del vault - {generated[:10]}",
        "",
        "## Resumen de salud",
        "",
        "| Metrica | Valor |",
        "|---|---|",
        f"| Notas totales auditadas | {total_notes} |",
        f"| Notas con temas detectados | {notes_with_topics} |",
        f"| Temas distintos | {total_topics} |",
        f"| Fuentes distintas | {total_sources} |",
        "",
        "## Cobertura por tema",
        "",
        "| Tema | Notas | Fuentes | Estado |",
        "|---|---:|---:|---|",
    ]

    low_coverage: list[tuple[str, int]] = []
    for (topic_name, _topic_slug), topic_notes in sorted(topic_index.items(), key=lambda x: x[0][0].lower()):
        count = len(topic_notes)
        source_set = {n.get("source") or "Desconocida" for n in topic_notes}
        status = _status_for_count(count)
        if count < 10:
            low_coverage.append((topic_name, count))
        lines.append(f"| {topic_name} | {count} | {len(source_set)} | {status} |")

    lines += [
        "",
        "## Estado por fuente",
        "",
        "| Fuente | Notas | Ultima fecha detectada |",
        "|---|---:|---|",
    ]

    for source in sorted(source_counts):
        latest = source_latest.get(source, "sin-fecha")
        lines.append(f"| {source} | {source_counts[source]} | {latest} |")

    lines += ["", "## Recomendaciones", ""]

    if low_coverage:
        lines.append("- Priorizar captura en temas con baja cobertura (<10 notas):")
        for topic_name, count in low_coverage[:8]:
            lines.append(f"- {topic_name}: {count} notas")
    else:
        lines.append("- No hay temas con baja cobertura por debajo de 10 notas.")

    sources_without_date = [s for s in sorted(source_counts) if s not in source_latest]
    if sources_without_date:
        lines.append("- Normalizar fechas en frontmatter para estas fuentes:")
        for source in sources_without_date:
            lines.append(f"- {source}")

    lines.append("")
    lines.append("#ai-generated")
    lines.append("")
    return "\n".join(lines)


def write_audit_report(vault: Path, notes: list[dict], topic_index: dict) -> Path:
    meta_dir = vault / "Atlas" / "Meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    report_path = meta_dir / "Auditoria.md"
    content = build_audit_report(vault, notes, topic_index)
    report_path.write_text(content, encoding="utf-8")
    return report_path


def main() -> int:
    # Import local para reutilizar la misma logica de captura/enriquecimiento
    from enrich_second_brain import VAULT, collect_notes

    notes = collect_notes()
    topic_index = {}
    for note in notes:
        for topic_name, topic_slug in note.get("topics", []):
            topic_index.setdefault((topic_name, topic_slug), []).append(note)

    report = write_audit_report(VAULT, notes, topic_index)
    print(f"AUDIT_REPORT {report}")
    print(f"AUDIT_NOTES {len(notes)}")
    print(f"AUDIT_TOPICS {len(topic_index)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
