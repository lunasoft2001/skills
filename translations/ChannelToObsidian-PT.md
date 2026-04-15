# ChannelToObsidian

## Propósito
Skill em duas fases para capturar um canal do YouTube completo num Second Brain do Obsidian. A fase 1 analisa todos os vídeos do canal e gera uma lista de verificação Markdown. A fase 2 processa apenas os vídeos selecionados através do pipeline completo VideoToObsidian.

## Estrutura
- `ChannelToObsidian/SKILL.md` — definição do skill e workflow completo em duas fases
- `ChannelToObsidian/scripts/channel_to_obsidian.py` — script que obtém todos os vídeos do canal (InnerTube browse API), constrói o índice e delega a VideoToObsidian os itens selecionados

**Depende de:** skill `VideoToObsidian` (deve estar instalado na pasta vizinha)

## Funcionalidades principais
- Obtém todos os vídeos do canal através da InnerTube browse API (sem dependências externas, paginação incluída)
- Cria/atualiza `Atlas/Personas/<NomeCanal>.md` como lista de verificação selecionável
- Marcadores de estado: `[ ]` não revisto · `[x]` selecionado · `[p]` já processado
- A fase 2 chama VideoToObsidian para cada item `[x]` e marca-o `[p]` ao terminar
- Suporta URLs de canal: handle (`@nome`), `/c/`, `/channel/UC…` ou URL de vídeo
- Caminho do vault configurável através da variável de ambiente `OBSIDIAN_VAULT`

## Casos de uso típicos
- Construir uma base de conhecimento a partir de um canal técnico favorito
- Rever todos os vídeos de um criador antes de decidir quais estudar
- Processamento em lote de um canal ou playlist completo com curadoria seletiva
- Manter um índice de canal atualizado à medida que novos vídeos são publicados
