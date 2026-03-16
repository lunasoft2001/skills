# Bowling Pro Shop — Virtueller Ball Driller & Lane Coach

Dieses Dokument beschreibt den Inhalt des Skills `bowling-proshop` in diesem Repository.

## Beschreibung

Ein virtueller Bowling-Ball-Driller und Lane-Coach, spezialisiert auf Ballauswahl und **Dual Angle Layouts** (Mo Pinel Methode). Fuehrt interaktive Mehrphasen-Konsultationen durch, um das Spielerprofil zu erstellen, und generiert einen vollstaendigen **visuellen HTML-Report** mit echtem Ballbild, Bahnsdiagramm, Drill-Diagramm und Layout-Analyse.

Ausloesebegriffe: `Ballauswahl`, `Layout`, `Oelmuster`, `Bohren`, `Rev Rate`, `PAP`, `Dual Angle`, `Hook-Potenzial`, `Bahnanpassungen`.

## Struktur

```text
bowling-proshop/
  SKILL.md                          # Skill-Anweisungen fuer GitHub Copilot
  assets/
    logo.jpeg                       # LunaBowling-Logo fuer den HTML-Report
  references/
    ball-selection.md               # Heuristiken zur Cover-/Kategorieauswahl
    current-balls-2026.md           # Aktueller Ballkatalog (2025-2026) mit verifizierten Slugs
    dual-angle.md                   # Vollstaendiges Dual Angle Layout-System (Mo Pinel)
    manufacturers.md                # Hersteller-URLs fuer Spezifikationssuchen
    patterns-reference.md           # Oelmuster: House, Sport, Challenge
    player-types.md                 # Speed/Rev Dominance, PAP, Track-Klassifizierung
  scripts/
    generate_bowling_report_v2.py   # Visueller HTML-Report-Generator
```

## Interaktive Konsultation

Der Skill nutzt vier Phasen ueber `vscode_askQuestions`:

1. **Phase 1** — Dominante Hand, Bahntyp, Ziel
2. **Phase 2** — Ballgeschwindigkeit, Rev Rate, PAP/Track
3. **Phase 3** — Bahnoberflaeche, Griffigkeit, aktuelles Arsenal
4. **Phase 4** — Visueller Report (Spielername)

## Visueller HTML-Report

Am Ende der Konsultation generiert der Skill einen HTML-Report mit:

- Ballkarte mit echtem Bild aus dem Herstellerkatalog
- SVG-Bahndiagramm von oben mit empfohlener Spiellinie
- SVG-Drill-Diagramm (Pin, PAP, Mass Bias, Fingerloechern)
- Dual Angle Layout mit erklaerung in einfacher Sprache
- Bahnanpassungen und zu verfeinernde Daten

```bash
python3 scripts/generate_bowling_report_v2.py \
  --data /tmp/bowling_data.json \
  --output ~/Desktop/bowling_report.html

# Oder mit Beispieldaten:
python3 scripts/generate_bowling_report_v2.py --example
```

## Installation

Kopiere den Ordner in das GitHub Copilot Skills-Verzeichnis:

```bash
# macOS / Linux
cp -r bowling-proshop ~/.copilot/skills/bowling-proshop

# Windows (PowerShell)
Copy-Item -Path "bowling-proshop" -Destination "$env:USERPROFILE\.copilot\skills\bowling-proshop" -Recurse
```

Starte danach VS Code neu.

## Anforderungen

- Python 3.11+
- Internetverbindung (fuer Ballbilder aus dem Herstellerkatalog)
- Keine externen Abhaengigkeiten — verwendet ausschliesslich die Python-Standardbibliothek

## Hinweise

- Empfiehlt nur Baelle aus `references/current-balls-2026.md` (aktiver Katalog, keine abgekuendigten Baelle).
- Storm-Ballbilder werden ueber verifizierte Slugs abgerufen (`KNOWN_SLUG_MAP` im Skript) — kein Raten.
- Das Dual Angle Layout-System folgt Mo Pinel: DA × Pin-to-PAP × VAL.
- Unterstuetzt Ein- und Zweihaender sowie Rechts- und Linkshaender.
