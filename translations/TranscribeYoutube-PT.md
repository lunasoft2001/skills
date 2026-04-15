# TranscribeYoutube

Skill para gerar notas de transcrição completas no Obsidian a partir de vídeos do YouTube.

## Propósito

Baixa a transcrição completa de qualquer vídeo do YouTube e salva como nota `.md` pronta para o Obsidian com frontmatter YAML e timestamps clicáveis — diretamente do VS Code, sem dependências externas.

## Estrutura

```text
TranscribeYoutube/
  SKILL.md
  scripts/
    transcribe_youtube.py
```

## Funcionalidades principais

- Usa a InnerTube Player API do YouTube (cliente iOS) — sem chaves de API, sem yt-dlp
- Zero dependências externas: apenas Python 3.9+ padrão
- Gera frontmatter YAML com metadados do vídeo
- Agrupa linhas de transcrição a cada 30 segundos (igual ao plugin YTranscript)
- Timestamps clicáveis que abrem o vídeo no segundo exato
- Cross-platform: macOS, Windows, Linux
- Abre o Obsidian automaticamente na nota criada
- Caminho do vault configurável via variável de ambiente `OBSIDIAN_VAULT`

## Casos de uso típicos

- Capturar um tutorial do YouTube no seu Second Brain
- Gerar uma nota de transcrição e vinculá-la à nota de recurso principal
- Arquivar conteúdo de vídeo para referência offline
