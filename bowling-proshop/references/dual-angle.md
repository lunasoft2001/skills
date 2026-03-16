# Dual Angle System — Referencia Completa

Sistema de Mo Pinel. Define la posición del pin y el mass bias en relación al PAP y el VAL (Vertical Axis Line) para controlar **cuándo** y **cómo** reacciona la bola.

## Tabla de contenidos
1. Los tres ángulos
2. Pin-to-PAP: distancia y efecto
3. Drilling Angle (DA): ángulo de taladrado
4. VAL Angle: ángulo a la línea vertical
5. Mass Bias (solo Asym)
6. CG position
7. Tabla de referencia rápida
8. Ajustes por perfil de jugador
9. Cómo medir PAP
10. Errores comunes

---

## 1. Los tres ángulos

```
Layout = Drilling Angle (DA) × Pin-to-PAP (pulgadas) × VAL Angle
Ejemplo: 55° × 4.5" × 45°
```

- **DA (Drilling Angle)**: Ángulo entre la línea de perforación (del dedo corazón al pulgar) y la línea Pin-PAP. Controla la posición del track flare.
- **Pin-to-PAP**: Distancia en pulgadas desde el pin hasta el PAP del jugador. Controla la magnitud del flare y el timing.
- **VAL Angle**: Ángulo entre la línea Pin-PAP y el VAL (Vertical Axis Line). Controla la posición del CG y ayuda a definir la forma del arco.

---

## 2. Pin-to-PAP: distancia y efecto

| Distancia | Efecto | Cuándo usar |
|---|---|---|
| 2" – 3" | Reacción muy fuerte y temprana, máximo flare | Patrones muy largos/oily, speed-dominant extremo |
| 3" – 4" | Fuerte, temprana, snap pronunciado | Patrones largos, rev-dominant en pistas secas |
| 4" – 5" | Balance entre continuidad y reacción — **zona más versátil** | Mayoría de situaciones |
| 5" – 6" | Arco más suave y continuo, menos flare | Patrones cortos, strokers, alta fricción |
| 6" – 6.75" | Mínima reacción (bola "muerta"), casi recto | Spare ball, pistas muy cortas |

**Regla práctica**: Cuanto más cerca el pin del PAP → más flare → más tracción en el aceite → reacción más fuerte/temprana.

---

## 3. Drilling Angle (DA)

Rango típico: **30° – 90°**

| DA | Efecto | Perfil |
|---|---|---|
| 30° – 45° | Máximo flip, snap violento en backend | Rev-dominant, busca ángulo extremo |
| 45° – 60° | Balance — snap controlado con buen carry | Tweener, mayoría de layouts |
| 60° – 75° | Arco continuo, menos agresivo en backend | Stroker, patrones cortos |
| 75° – 90° | Mínimo flip, arco suavísimo / casi recto | Mucha fricción, spare |

**Combinaciones comunes:**
- DA bajo + pin corto = flip muy agresivo (cuidado: puede over-react)
- DA alto + pin largo = control máximo
- DA medio + pin medio = all-around versátil

---

## 4. VAL Angle

El VAL (Vertical Axis Line) pasa por el PAP horizontalmente. El VAL Angle es el ángulo entre la línea Pin-PAP y el VAL.

| VAL Angle | Efecto |
|---|---|
| 0° – 30° | Pin sobre o cerca del VAL → reacción muy fuerte / early |
| 30° – 45° | Pin ligeramente bajo el VAL → buen balance hook+length |
| 45° – 60° | Pin claramente bajo el VAL → más length, snap en backend |
| 60° – 90° | Pin muy bajo → máxima longitud, reacción late y sharp |

**Nota**: VAL Angle y DA trabajan juntos. No subas ambos a la vez sin considerar el pin-to-PAP.

---

## 5. Mass Bias (solo Asym)

En bolas asimétricas existe un tercer punto de desequilibrio: el **Mass Bias (MB)**.
- Posición del MB relativa al PAP determina cuánto contribuye la asimetría a la reacción
- **MB cerca del PAP** (~1.5"– 2"): máxima angularidad
- **MB lejos del PAP** (>3.5"): efecto más suave, similar a simétrica
- Siempre indicar en el layout dónde queda el MB respecto al PAP y al VAL

---

## 6. CG Position

El CG (Center of Gravity) queda definido por los tres ángulos. No suele ser el parámetro principal en el sistema Dual Angle, pero:
- CG **above VAL** → tiende a más hook
- CG **below VAL** → tiende a más length
- En bolas Asym el MB domina sobre el CG

---

## 7. Tabla de referencia rápida

| Situación | DA | Pin-to-PAP | VAL |
|---|---|---|---|
| Patrón largo + mucho aceite | 45–55° | 3–4.5" | 35–50° |
| Patrón medio (house/sport) | 50–65° | 4–5" | 45–60° |
| Patrón corto / alta fricción | 60–75° | 5–6" | 55–70° |
| Rev-dominant en burn | 65–75° | 5–6" | 60–70° |
| Speed-dominant en oily | 45–55° | 3.5–4.5" | 40–50° |
| Spare (recto) | 70–90° | 6–6.75" | 70–90° |

---

## 8. Ajustes por perfil de jugador

**Speed-dominant** (velocidad relativa > rev rate):
- Necesita más tracción → pin más corto, VAL más pequeño, DA menor
- Superficie más áspera (500–2000 grit sanded)

**Rev-dominant** (rev rate relativa > velocidad):
- Menos tracción para controlar → pin más largo, VAL más grande, DA mayor
- Superficie más fina/pulida (3000–4000 + polish)

**Stroker** (eje de rotación bajo, poca inclinación de eje):
- Layouts continuos: DA 60–75°, pin 5–6", VAL 55–70°
- Evitar layouts demasiado agresivos: la bola se irá temprano

**Cranker** (alta rotación, alta inclinación de eje):
- Más control: DA 55–65°, pin 4.5–5.5", VAL 50–65°
- Superficie más fina para compensar alta rev rate

**Two-hander**:
- Rev rate muy elevado → tratar como cranker agresivo
- Cuidado con layouts demasiado cortos en pistas secas

---

## 9. Cómo medir PAP

El PAP (Positive Axis Point) es el punto de la bola que queda estático al inicio del swing.

**Método estándar:**
1. Lanzar la bola y observar dónde aparece el track (anillo de aceite)
2. El track es perpendicular al eje de rotación
3. PAP ≈ el punto más alejado del track, en la misma línea del eje
4. Se mide como: X pulgadas a la derecha + Y pulgadas arriba/abajo del centro del agujero del dedo corazón (para diestros)

**PAP típico diestro**: 4.5–5.25" derecha, 0.25–0.75" arriba  
**PAP típico zurdo**: 4.5–5.25" izquierda, 0.25–0.75" arriba  
**Two-hander**: puede variar mucho — medir siempre antes de perforar

**Sin PAP conocido**: dar layout como rango provisional y pedir que lo midan en el proshop antes de perforar. No perforar sin PAP en bolas Asym.

---

## 10. Errores comunes

| Error | Consecuencia | Solución |
|---|---|---|
| Pin demasiado corto en pista seca | Over-reaction, split 7-10 | Subir pin-to-PAP |
| Pin demasiado largo en pista larga | La bola no reacciona | Bajar pin-to-PAP |
| DA muy bajo + rev-dominant | Flip incontrolable | Subir DA o usar cover menos agresivo |
| Ignorar el MB en Asym | Layout indefinido | Siempre especificar posición MB |
| Layout agresivo en stroker | Reacción demasiado temprana | DA>65°, pin>5" |
