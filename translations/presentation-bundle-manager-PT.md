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

## Estrutura do manifest.json

```json
{
  "schema_version": "1.0",
  "project": { "title", "slug", "author", "generated_at", "generated_by" },
  "deliverables": [
    { "file": "storyboard.docx", "type": "storyboard", "sha256": "...", "status": "present" },
    { "file": "storyboard.json", "type": "storyboard_json", "sha256": "...", "status": "present" },
    { "file": "deck.pptx", "type": "presentation", "sha256": "...", "status": "present" },
    { "file": "speaker-notes.docx", "type": "speaker_notes", "sha256": "...", "status": "present" }
  ],
  "validation": { "all_core_files_present": true, "warnings": [] }
}
```

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

## Estrutura

```
suites/presentation/presentation-bundle-manager/
  SKILL.md
  scripts/
    bundle_manager.py
  evals/
    evals.json
```
