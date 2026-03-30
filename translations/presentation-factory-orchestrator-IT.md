# Presentation Factory Orchestrator

Questo documento descrive lo skill `presentation-factory-orchestrator`.

## Descrizione

Un orchestratore end-to-end che coordina la pipeline completa di creazione di presentazioni in quattro fasi: storyboard → costruttore PPTX → note del relatore → gestore bundle. Valida gli input minimi e instrada ogni fase al sub-skill appropriato, consegnando il pacchetto completo in `/deliverables/<slug>/`.

## Trigger

`crea una presentazione`, `prepara un deck`, `costruisci diapositive`, `pacchetto presentazione completo`, `presentazione end-to-end`

## Fasi della Pipeline

1. **Fase 1** — `presentation-storyboard`: struttura narrativa
2. **Fase 2** — `presentation-pptx-builder`: file di presentazione
3. **Fase 3** — `presentation-speaker-notes`: script del relatore
4. **Fase 4** — `presentation-bundle-manager`: indice + manifesto

## Input Richiesti

- **topic** — argomento della presentazione
- **audience** — chi partecipa e il loro livello
- **duration** — durata totale in minuti
- **slug** — identificatore breve per la cartella di output (es. `q2-roadmap-2026`)

## Output

```
/deliverables/<slug>/
  storyboard.docx
  deck.pptx
  speaker-notes.docx
  index.xlsx
  manifest.json
```
