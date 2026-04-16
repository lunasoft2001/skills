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
from datetime import datetime, date
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
    """Semaforo de cobertura por tema para trabajo diario."""
    if count >= 30:
        return "SOLIDO"
    if count >= 15:
        return "OK"
    if count >= 8:
        return "MEJORABLE"
    if count >= 4:
        return "BAJO"
    return "CRITICO"


def _age_status_from_date(date_str: str, today: date) -> str:
    if not date_str:
        return "SIN_FECHA"
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "SIN_FECHA"

    days = (today - d).days
    if days <= 3:
        return "ACTIVA"
    if days <= 10:
        return "VIGILAR"
    return "DESACTUALIZADA"


def _priority_for_topic_status(status: str) -> str:
    if status == "CRITICO":
        return "P1"
    if status == "BAJO":
        return "P2"
    if status == "MEJORABLE":
        return "P3"
    return "OK"


def _priority_for_source_freshness(freshness: str) -> str:
    if freshness in {"DESACTUALIZADA", "SIN_FECHA"}:
        return "P1"
    if freshness == "VIGILAR":
        return "P2"
    return "OK"


def build_audit_report(vault: Path, notes: list[dict], topic_index: dict) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    today = date.today()

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
    coverage_pct = round((notes_with_topics / total_notes * 100), 1) if total_notes else 0.0

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
        f"| Cobertura semantica | {coverage_pct}% |",
        f"| Temas distintos | {total_topics} |",
        f"| Fuentes distintas | {total_sources} |",
        "",
        "## Cobertura por tema",
        "",
        "| Tema | Notas | Fuentes | Estado |",
        "|---|---:|---:|---|",
    ]

    low_coverage: list[tuple[str, int, str, str]] = []
    topic_priorities: list[tuple[str, str, int, str]] = []
    for (topic_name, _topic_slug), topic_notes in sorted(topic_index.items(), key=lambda x: x[0][0].lower()):
        count = len(topic_notes)
        source_set = {n.get("source") or "Desconocida" for n in topic_notes}
        status = _status_for_count(count)
        priority = _priority_for_topic_status(status)
        if status in {"CRITICO", "BAJO", "MEJORABLE"}:
            low_coverage.append((topic_name, count, status, priority))
            topic_priorities.append((priority, topic_name, count, status))
        lines.append(f"| {topic_name} | {count} | {len(source_set)} | {status} |")

    lines += [
        "",
        "## Estado por fuente",
        "",
        "| Fuente | Notas | Ultima fecha detectada | Estado |",
        "|---|---:|---|---|",
    ]

    source_priorities: list[tuple[str, str, str]] = []
    for source in sorted(source_counts):
        latest = source_latest.get(source, "sin-fecha")
        freshness = _age_status_from_date(latest if latest != "sin-fecha" else "", today)
        src_priority = _priority_for_source_freshness(freshness)
        if src_priority != "OK":
            source_priorities.append((src_priority, source, freshness))
        lines.append(f"| {source} | {source_counts[source]} | {latest} | {freshness} |")

    lines += [
        "",
        "## Prioridades operativas",
        "",
        "| Prioridad | Tipo | Elemento | Estado |",
        "|---|---|---|---|",
    ]

    combined = []
    for prio, topic_name, count, status in topic_priorities:
        combined.append((prio, "Tema", f"{topic_name} ({count} notas)", status))
    for prio, source, freshness in source_priorities:
        combined.append((prio, "Fuente", source, freshness))

    if combined:
        prio_order = {"P1": 1, "P2": 2, "P3": 3, "OK": 4}
        for prio, kind, element, state in sorted(combined, key=lambda x: (prio_order.get(x[0], 9), x[1], x[2].lower()))[:20]:
            lines.append(f"| {prio} | {kind} | {element} | {state} |")
    else:
        lines.append("| OK | Sistema | Sin elementos urgentes | Estable |")

    lines += ["", "## Recomendaciones", ""]

    if low_coverage:
        lines.append("- Priorizar captura en temas con cobertura insuficiente:")
        for topic_name, count, status, priority in low_coverage[:10]:
            lines.append(f"- {priority} {topic_name}: {count} notas ({status})")
    else:
        lines.append("- No hay temas con cobertura insuficiente.")

    sources_without_date = [s for s in sorted(source_counts) if s not in source_latest]
    if sources_without_date:
        lines.append("- Normalizar fechas en frontmatter para estas fuentes:")
        for source in sources_without_date:
            lines.append(f"- {source}")

    stale_sources = []
    for source in sorted(source_counts):
        latest = source_latest.get(source, "")
        freshness = _age_status_from_date(latest, today)
        if freshness == "DESACTUALIZADA":
            stale_sources.append(source)
    if stale_sources:
        lines.append("- Revisar fuentes desactualizadas (mas de 10 dias sin fecha reciente):")
        for source in stale_sources:
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
