# VideoToObsidian

## Objetivo
Pipeline completo para capturar um vídeo do YouTube como nota técnica estruturada no Obsidian. Combina download automático de metadados e transcrição com análise inteligente do conteúdo para gerar o documento adequado ao tipo de vídeo.

## Estrutura
- `VideoToObsidian/SKILL.md` — definição do skill e fluxo completo passo a passo
- `VideoToObsidian/scripts/video_to_obsidian.py` — script que obtém metadados, delega a transcrição ao TranscribeYoutube e emite um JSON para o Copilot

**Depende de:** skill `TranscribeYoutube` (deve estar instalado no diretório irmão)

## Principais funcionalidades
- Obtém metadados do vídeo via InnerTube API (título, canal, descrição, duração)
- Delega a transcrição ao skill `TranscribeYoutube`
- Detecta o tipo de conteúdo: TUTORIAL / CONCEITO / DEMO / PALESTRA
- Aplica o template de nota correspondente (checklist de passos, pontos-chave, citações…)
- Gera uma nota Obsidian completa com vídeo incorporado, resumo e wikilink para a transcrição
- Abre a nota no Obsidian automaticamente (macOS / Windows / Linux)
- Caminho do vault configurável via variável de ambiente `OBSIDIAN_VAULT`

## Casos de uso típicos
- Capturar um tutorial do YouTube como nota de referência com passos
- Transformar um vídeo conceitual em uma entrada estruturada do Second Brain
- Documentar uma demo ou showcase de software
- Arquivar uma palestra ou entrevista com as ideias principais destacadas
