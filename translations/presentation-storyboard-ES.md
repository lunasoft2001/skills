# Presentation Storyboard

Este documento describe el skill `presentation-storyboard`.

## Descripción

Estructura el arco narrativo de una presentación diapositiva por diapositiva. Para cada slide produce un mensaje, objetivo, duración recomendada y tipo de visual sugerido. Aplica un arco de 3 actos (Contexto / Contenido / Acción) y la regla de un mensaje por diapositiva.

## Activadores

`planea mis diapositivas`, `estructura la presentación`, `arma el guión de slides`, `define el hilo narrativo`, `storyboard de presentación`, `outline del deck`

## Salida por Diapositiva

- **Título** — encabezado del slide
- **Mensaje** — único punto clave
- **Objetivo** — qué siente la audiencia después de esta slide
- **Duración** — tiempo asignado
- **Visual sugerido** — gráfico / diagrama / foto / solo texto
- **Transición** — frase que conecta con el siguiente slide

## Estructura

```
suites/presentation/presentation-storyboard/
  SKILL.md
  evals/
    evals.json
  references/
    slide-structure-guide.md
```

## Modelos Narrativos

- Negocio estándar (3 actos)
- Pitch deck (inversores)
- Educativo / taller
- Resumen ejecutivo (10 min o menos)

## Archivo de Salida

`/deliverables/<slug>/storyboard.docx` (y `storyboard.json` para uso programático)
