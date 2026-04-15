# VideoToObsidian

## Scopo
Pipeline completa per acquisire un video YouTube come nota tecnica strutturata in Obsidian. Combina il download automatico di metadati e trascrizioni con l'analisi intelligente del contenuto per generare il documento adatto al tipo di video.

## Struttura
- `VideoToObsidian/SKILL.md` — definizione dello skill e workflow completo passo per passo
- `VideoToObsidian/scripts/video_to_obsidian.py` — script che recupera i metadati, delega la trascrizione a TranscribeYoutube e produce un JSON per Copilot

**Dipende da:** skill `TranscribeYoutube` (deve essere installato nella directory adiacente)

## Caratteristiche principali
- Recupera i metadati del video tramite InnerTube API (titolo, canale, descrizione, durata)
- Delega la trascrizione allo skill `TranscribeYoutube`
- Rileva il tipo di contenuto: TUTORIAL / CONCETTO / DEMO / CONFERENZA
- Applica il template di nota corrispondente (checklist di passi, punti chiave, citazioni…)
- Genera una nota Obsidian completa con video incorporato, riassunto e wikilink alla trascrizione
- Apre la nota in Obsidian automaticamente (macOS / Windows / Linux)
- Percorso del vault configurabile tramite variabile d'ambiente `OBSIDIAN_VAULT`

## Casi d'uso tipici
- Acquisire un tutorial YouTube come nota di riferimento con passi
- Trasformare un video concettuale in un'entrata strutturata del Second Brain
- Documentare una demo o showcase software
- Archiviare una conferenza o intervista con le idee chiave evidenziate
