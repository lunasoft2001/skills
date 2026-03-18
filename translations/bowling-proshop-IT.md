# Bowling Pro Shop — Foratore Virtuale & Coach di Pista

Questo documento descrive il contenuto dello skill `bowling-proshop` in questo repository.

## Descrizione

Un foratore di palle da bowling virtuale e coach di pista specializzato nella selezione della palla e nei **layout Dual Angle** (metodo Mo Pinel). Conduce consultazioni interattive a piu fasi per costruire il profilo del giocatore e genera un **report HTML visivo completo** con immagine reale della palla, diagramma della pista, diagramma di foratura e analisi del layout.

Parole chiave: `selezione palla`, `layout`, `schema olio`, `foratura`, `rev rate`, `PAP`, `Dual Angle`, `potenziale hook`, `regolazioni pista`.

## Struttura

```text
bowling-proshop/
  SKILL.md                          # Istruzioni dello skill per GitHub Copilot
  assets/
    logo.jpeg                       # Logo LunaBowling per il report HTML
  references/
    ball-selection.md               # Euristiche di selezione cover/categoria
    current-balls-2026.md           # Catalogo palle attuali (2025-2026) con slug verificati
    dual-angle.md                   # Sistema Dual Angle completo (Mo Pinel)
    manufacturers.md                # URL dei produttori per le specifiche
    patterns-reference.md           # Schemi olio: house, sport, challenge
    player-types.md                 # Classificazione speed/rev dominance, PAP, track
  scripts/
    generate_bowling_report_v2.py   # Generatore di report HTML visivi
```

## Consultazione interattiva

Lo skill utilizza quattro fasi tramite `vscode_askQuestions`:

1. **Fase 1** — Mano dominante, tipo di pista, obiettivo
2. **Fase 2** — Velocita palla, rev rate, PAP/track
3. **Fase 3** — Superficie pista, aderenza, arsenale attuale
4. **Fase 4** — Report visivo (nome del giocatore)

## Report HTML visivo

Al termine della consultazione, lo skill genera un report HTML con:

- Scheda palla con immagine reale dal catalogo del produttore
- Diagramma SVG della pista dall'alto con la linea di gioco consigliata
- Diagramma SVG di foratura (pin, PAP, mass bias, fori)
- Layout Dual Angle con spiegazione in linguaggio naturale
- Regolazioni pista e dati da perfezionare

```bash
python3 scripts/generate_bowling_report_v2.py \
  --data /tmp/bowling_data.json \
  --output ~/Desktop/bowling_report.html

# O con dati di esempio:
python3 scripts/generate_bowling_report_v2.py --example
```

## Installazione

Copia la cartella nella directory degli skill di GitHub Copilot:

```bash
# macOS / Linux
cp -r bowling-proshop ~/.copilot/skills/bowling-proshop

# Windows (PowerShell)
Copy-Item -Path "bowling-proshop" -Destination "$env:USERPROFILE\.copilot\skills\bowling-proshop" -Recurse
```

Poi riavvia VS Code.

## Requisiti

- Python 3.11+
- Connessione internet (per le immagini delle palle dal catalogo del produttore)
- Nessuna dipendenza esterna — usa solo la libreria standard di Python

## Note

- Consiglia solo palle elencate in `references/current-balls-2026.md` (catalogo attivo, nessuna palla discontinuata).
- Le immagini delle palle Storm vengono recuperate tramite slug verificati (`KNOWN_SLUG_MAP` nello script) — senza indovinare.
- Il sistema di layout Dual Angle segue Mo Pinel: DA × Pin-to-PAP × VAL.
- Compatibile con giocatori a una e due mani, destrorsi e mancini.
