# Presentación Factory Orchestrator

Este documento describe el skill `presentation-factory-orchestrator`.

## Descripción

Orquestador end-to-end que coordina el pipeline completo de creación de presentaciones en cuatro etapas: storyboard → constructor de PPTX → notas del presentador → gestor de bundle. Valida las entradas mínimas y enruta cada etapa al sub-skill correspondiente, entregando el paquete completo en `/deliverables/<slug>/`.

## Activadores

`crea una presentación`, `prepara un deck`, `necesito diapositivas`, `paquete completo de presentación`, `armá una presentación`, `presentación de principio a fin`

## Etapas del Pipeline

1. **Etapa 1** — `presentation-storyboard`: estructura narrativa
2. **Etapa 2** — `presentation-pptx-builder`: archivo de diapositivas
3. **Etapa 3** — `presentation-speaker-notes`: guión del presentador
4. **Etapa 4** — `presentation-bundle-manager`: índice + manifiesto

## Entradas Requeridas

- **topic** — tema de la presentación
- **audience** — quién asiste y su nivel de experiencia
- **duration** — duración total en minutos
- **slug** — identificador corto para la carpeta de salida (p. ej. `q2-hoja-de-ruta-2026`)

## Salida

```
/deliverables/<slug>/
  storyboard.docx
  deck.pptx
  speaker-notes.docx
  index.xlsx
  manifest.json
```

## Estructura

```
suites/presentation/presentation-factory-orchestrator/
  SKILL.md
  evals/
    evals.json
  references/
    pipeline-stages.md
```
