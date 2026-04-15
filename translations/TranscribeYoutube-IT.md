# TranscribeYoutube

Skill per generare note di trascrizione complete in Obsidian da video YouTube.

## Scopo

Scarica la trascrizione completa di qualsiasi video YouTube e la salva come nota `.md` pronta per Obsidian con frontmatter YAML e timestamp cliccabili — direttamente da VS Code, senza dipendenze esterne.

## Struttura

```text
TranscribeYoutube/
  SKILL.md
  scripts/
    transcribe_youtube.py
```

## Funzionalità principali

- Usa l'API InnerTube Player di YouTube (client iOS) — nessuna chiave API, nessun yt-dlp
- Zero dipendenze esterne: solo Python 3.9+ standard
- Genera frontmatter YAML con i metadati del video
- Raggruppa le righe di trascrizione ogni 30 secondi (come il plugin YTranscript)
- Timestamp cliccabili che aprono il video al secondo esatto
- Cross-platform: macOS, Windows, Linux
- Apre Obsidian automaticamente sulla nota creata
- Percorso del vault configurabile tramite la variabile d'ambiente `OBSIDIAN_VAULT`

## Casi d'uso tipici

- Acquisire un tutorial YouTube nel proprio Second Brain
- Generare una nota di trascrizione e collegarla dalla nota risorsa principale
- Archiviare contenuti video per riferimento offline
