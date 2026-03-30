# Presentation PPTX Builder

Este documento descreve o skill `presentation-pptx-builder`.

## Descrição

Gera um arquivo `.pptx` a partir de um storyboard usando `python-pptx`. Aplica um layout profissional e limpo com quatro temas disponíveis. Insere marcadores rotulados para gráficos e diagramas em vez de fabricar dados.

## Ativadores

`gera o pptx`, `cria o deck`, `cria o PowerPoint`, `produz o arquivo de apresentação`

## Temas

| Tema | Estilo |
|------|--------|
| `corporate` | Branco + Azul marinho — padrão empresarial |
| `minimal` | Branco + Carvão — limpo e simples |
| `dark` | Escuro + Ciano — tecnologia e moderno |
| `vibrant` | Branco + Roxo — criativo e ousado |

## Uso

```bash
python3 scripts/build_pptx.py \
  --storyboard /deliverables/<slug>/storyboard.json \
  --output /deliverables/<slug>/deck.pptx \
  --theme corporate
```

## Requisitos

- Python 3.9+
- `pip install python-pptx`
