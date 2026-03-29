# Presentation Bundle Manager

Este documento descreve o skill `presentation-bundle-manager`.

## Descrição

Agrupa todos os entregáveis da apresentação em uma pasta de projeto estruturada. Gera um índice `index.xlsx` (duas planilhas: Resumo + Arquivos) e um `manifest.json` com hashes SHA256 e status de validação.

## Ativadores

`agrupe a apresentação`, `empacote os entregáveis`, `crie o manifesto`, `gere o índice`, `finalize o pacote de apresentação`

## Arquivos de Saída

| Arquivo | Descrição |
|---------|-----------|
| `index.xlsx` | Índice Excel com duas planilhas: Resumo + Arquivos |
| `manifest.json` | Manifesto JSON com hashes e validação |

## Uso

```bash
python3 scripts/bundle_manager.py \
  --slug meu-slug \
  --title "Minha Apresentação" \
  --author "João Silva"
```

## Requisitos

- Python 3.9+ (somente biblioteca padrão para `manifest.json`)
- `pip install openpyxl` (para `index.xlsx`)
