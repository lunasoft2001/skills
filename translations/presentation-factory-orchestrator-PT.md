# Presentation Factory Orchestrator

Este documento descreve o skill `presentation-factory-orchestrator`.

## Descrição

Um orquestrador end-to-end que coordena o pipeline completo de criação de apresentações em quatro etapas: storyboard → construtor PPTX → notas do apresentador → gerenciador de bundle. Valida os inputs mínimos e encaminha cada etapa ao sub-skill apropriado, entregando o pacote completo em `/deliverables/<slug>/`.

## Ativadores

`criar uma apresentação`, `preparar um deck`, `criar slides`, `pacote de apresentação completo`, `apresentação do início ao fim`

## Etapas do Pipeline

1. **Etapa 1** — `presentation-storyboard`: estrutura narrativa
2. **Etapa 2** — `presentation-pptx-builder`: arquivo de apresentação
3. **Etapa 3** — `presentation-speaker-notes`: roteiro do apresentador
4. **Etapa 4** — `presentation-bundle-manager`: índice + manifesto

## Inputs Necessários

- **topic** — tema da apresentação
- **audience** — quem participa e seu nível de expertise
- **duration** — duração total em minutos
- **slug** — identificador curto para a pasta de saída (ex. `q2-roadmap-2026`)

## Saída

```
/deliverables/<slug>/
  storyboard.docx
  deck.pptx
  speaker-notes.docx
  index.xlsx
  manifest.json
```
