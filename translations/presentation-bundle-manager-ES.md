# Presentation Bundle Manager

Este documento describe el skill `presentation-bundle-manager`.

## Descripción

Empaqueta todos los entregables de la presentación en una carpeta de proyecto estructurada. Genera un índice `index.xlsx` (dos hojas: Resumen + Archivos) y un `manifest.json` con sumas de verificación SHA256 y estado de validación. Maneja bundles parciales cuando faltan archivos básicos.

## Activadores

`empaqueta la presentación`, `crea el índice de archivos`, `genera el manifest`, `arma el paquete final`, `finaliza el paquete de presentación`

## Archivos de Salida

| Archivo | Descripción |
|---------|-------------|
| `index.xlsx` | Índice Excel de dos hojas: Resumen + Archivos |
| `manifest.json` | Manifiesto JSON con checksums y validación |

## Uso

```bash
python3 scripts/bundle_manager.py \
  --slug mi-slug \
  --title "Mi Presentación" \
  --author "Juan García"
```

## Requisitos

- Python 3.9+ (solo biblioteca estándar para `manifest.json`)
- `pip install openpyxl` (para `index.xlsx`)

## Estructura

```
presentation-bundle-manager/
  SKILL.md
  scripts/
    bundle_manager.py
  evals/
    evals.json
```
