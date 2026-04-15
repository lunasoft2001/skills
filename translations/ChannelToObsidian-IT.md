# ChannelToObsidian

## Scopo
Skill in due fasi per acquisire un intero canale YouTube in un Second Brain Obsidian. La fase 1 analizza tutti i video del canale e genera una checklist Markdown. La fase 2 elabora solo i video selezionati tramite il pipeline completo VideoToObsidian.

## Struttura
- `ChannelToObsidian/SKILL.md` — definizione dello skill e workflow completo in due fasi
- `ChannelToObsidian/scripts/channel_to_obsidian.py` — script che recupera tutti i video del canale (InnerTube browse API), costruisce l'indice e delega a VideoToObsidian gli elementi selezionati

**Dipende da:** skill `VideoToObsidian` (deve essere installato nella directory adiacente)

## Funzionalità principali
- Recupera tutti i video del canale tramite InnerTube browse API (senza dipendenze esterne, paginazione inclusa)
- Crea/aggiorna `Atlas/Personas/<NomeCanale>.md` come checklist selezionabile
- Marcatori di stato: `[ ]` non esaminato · `[x]` selezionato · `[p]` già elaborato
- La fase 2 richiama VideoToObsidian per ogni elemento `[x]` e lo segna `[p]` al termine
- Supporta URL di canale: handle (`@nome`), `/c/`, `/channel/UC…` o URL di video
- Percorso vault configurabile tramite variabile d'ambiente `OBSIDIAN_VAULT`

## Casi d'uso tipici
- Costruire una base di conoscenza da un canale tecnico preferito
- Esaminare tutti i video di un creatore prima di decidere quali studiare
- Elaborazione in batch di un intero canale o playlist con curazione selettiva
- Mantenere aggiornato un indice di canale man mano che vengono pubblicati nuovi video
