# Fabricantes de Bolas — URLs para Búsqueda

Usa `fetch_webpage` con estas URLs para obtener specs actualizadas de bolas.

## Catálogos completos (listar todas las bolas)

| Fabricante | URL catálogo |
|---|---|
| Storm | https://www.stormbowling.com/balls |
| Roto Grip | https://www.rotogrip.com/balls |
| Brunswick | https://www.brunswickbowling.com/balls |
| Hammer | https://www.hammerbowling.com/balls |
| Motiv | https://motivbowling.com/balls |
| Track | https://trackbowling.com/balls |
| 900 Global | https://www.900global.com/balls |
| Columbia 300 | https://www.columbia300.com/balls |
| Ebonite | https://www.ebonite.com/balls |
| DV8 | https://www.dv8bowling.com/balls |

## Búsqueda directa de bola por nombre

Patrón general de URLs (sustituir espacios por guiones, en minúsculas):

| Fabricante | Patrón URL bola individual |
|---|---|
| Storm | `https://www.stormbowling.com/balls/[nombre-de-la-bola]` |
| Roto Grip | `https://www.rotogrip.com/balls/[nombre-de-la-bola]` |
| Brunswick | `https://www.brunswickbowling.com/balls/[nombre-de-la-bola]` |
| Hammer | `https://www.hammerbowling.com/balls/[nombre-de-la-bola]` |
| Motiv | `https://motivbowling.com/balls/[nombre-de-la-bola]` |
| Track | `https://trackbowling.com/balls/[nombre-de-la-bola]` |

**Ejemplos:**
- Storm Phaze II → `https://www.stormbowling.com/balls/phaze-ii`
- Motiv Jackal Flash → `https://motivbowling.com/balls/jackal-flash`
- Hammer Black Widow 3.0 → `https://www.hammerbowling.com/balls/black-widow-3-0`

## Datos a extraer del fetch

Cuando hagas fetch de una página de bola, busca:

```
- Cover stock (nombre del material reactivo)
- Core (nombre del núcleo + si es asym/sym)
- Factory finish (grit y acabado de fábrica)
- RG (Radius of Gyration, típico 2.45–2.65)
- Differential (medida de flare potential, típico 0.01–0.06)
- Mass Bias Diff (para Asym, típico 0.01–0.02)
- Color / imagen URL
- Precio sugerido (si aparece)
```

## Sitios de reviews y comparativas

| Recurso | URL | Utilidad |
|---|---|---|
| BowlerX | https://www.bowlerx.com | Specs + comparativas |
| BowlingThis Week | https://www.bowlingthisweek.com | Reviews detalladas |
| USBC Equipment Specs | https://bowl.com/equipment/equipment-specifications | Specs oficiales certificadas |
| Track Bowling (scores) | https://www.bowl.com | Datos de torneos USBC |

## Notas de uso

- Algunos sitios requieren JavaScript para cargar el contenido — si `fetch_webpage` devuelve HTML vacío, prueba con la URL del catálogo general y busca en el HTML.
- Las URLs pueden cambiar con el tiempo — si falla, prueba el catálogo general y navega desde ahí.
- Para imágenes: busca en el HTML tags `<img>` con el nombre de la bola en el `alt` o en la URL.
