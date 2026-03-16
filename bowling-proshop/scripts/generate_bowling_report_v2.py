#!/usr/bin/env python3
"""
Bowling Pro Shop — Visual Report Generator v2
Sin dependencias externas (solo stdlib).

Usage:
  python generate_bowling_report_v2.py --example --output ~/Desktop/bowling.html
  python generate_bowling_report_v2.py --data datos.json --output ~/Desktop/bowling.html
"""

import argparse, json, math, os, re, urllib.request, urllib.error, urllib.parse
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PBA PLAYER DATABASE
# ─────────────────────────────────────────────────────────────────────────────
PBA_PLAYERS = [
    {"name": "Jason Belmonte", "style": "two-hander", "speed": 17.5, "rev": 520, "titles": 14, "note": "El mejor two-hander de todos los tiempos. Rev rate altísimo, muy versátil."},
    {"name": "EJ Tackett",     "style": "two-hander", "speed": 17.0, "rev": 480, "titles": 6,  "note": "Potencia y precisión combinadas. Very consistent en sport shots."},
    {"name": "Norm Duke",      "style": "stroker",    "speed": 15.0, "rev": 220, "titles": 40, "note": "Maestro del control. Línea directa, máxima repetición."},
    {"name": "Walter Ray Williams Jr", "style":"stroker","speed":15.5,"rev":200,"titles":47,"note":"El más ganador del PBA Tour. Juega muy recto, increíble precisión."},
    {"name": "Pete Weber",     "style": "tweener",    "speed": 15.5, "rev": 330, "titles": 37, "note": "«PDW». Tweener clásico agresivo, gran lector de pistas."},
    {"name": "Parker Bohn III","style": "cranker",    "speed": 14.5, "rev": 400, "titles": 35, "note": "Cranker suave y continuo. Excelente en patrones medianos."},
    {"name": "Chris Barnes",   "style": "tweener",    "speed": 16.5, "rev": 350, "titles": 19, "note": "Speed-rev muy equilibrado. Referencia del tweener moderno."},
    {"name": "Tommy Jones",    "style": "cranker",    "speed": 14.0, "rev": 420, "titles": 21, "note": "Cranker con gran ángulo. Muy efectivo en patrones largos."},
    {"name": "Sean Rash",      "style": "cranker",    "speed": 13.5, "rev": 450, "titles": 12, "note": "Rev-dominant. Bolas agresivas, juega muy ancho."},
    {"name": "Jesper Svensson","style": "two-hander", "speed": 16.0, "rev": 500, "titles": 8,  "note": "Two-hander sueco, muy controlado para su rev rate."},
    {"name": "Anthony Simonsen","style":"tweener",    "speed": 17.0, "rev": 380, "titles": 8,  "note": "Speed-dominant moderno. Gran lector, juega múltiples líneas."},
    {"name": "Ryan Ciminelli", "style": "stroker",    "speed": 16.0, "rev": 250, "titles": 10, "note": "Stroker rápido. Muy consistente en sport patterns."},
]

def find_pba_match(style: str, speed: float, rev: int) -> dict:
    """Find the most similar PBA player by weighted distance."""
    sl = style.lower()
    # Detectar two-hander primero (cubre español "dos manos", inglés "two hand", compuestos)
    if any(k in sl for k in ("dos manos", "two hand", "two-hand", "dosmanos")):
        s_val = 4
    elif "cranker" in sl:
        s_val = 3
    elif "tweener" in sl:
        s_val = 2
    elif "stroker" in sl:
        s_val = 1
    else:
        norm = sl.replace("-", "").replace("—", "").replace(" ", "")
        s_val = {"stroker": 1, "tweener": 2, "cranker": 3, "twohander": 4, "twohands": 4}.get(norm, 2)
    _sm = {"stroker": 1, "tweener": 2, "cranker": 3, "twohander": 4, "twohands": 4}
    best, best_d = PBA_PLAYERS[0], 1e9
    for p in PBA_PLAYERS:
        p_s = _sm.get(p["style"].replace("-","").replace(" ",""), 2)
        d = (abs(p["speed"] - speed) * 1.5 +
             abs(p["rev"] - rev) * 0.01 +
             abs(p_s - s_val) * 4.5)
        if d < best_d:
            best, best_d = p, d
    return best

# ─────────────────────────────────────────────────────────────────────────────
# SVG HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def arc_path(cx, cy, r, start_deg, end_deg):
    """SVG arc path string from start_deg to end_deg.
    Usa cy - r*sin para coordenadas SVG correctas (eje Y invertido)."""
    s = math.radians(start_deg)
    e = math.radians(end_deg)
    x1, y1 = cx + r * math.cos(s), cy - r * math.sin(s)
    x2, y2 = cx + r * math.cos(e), cy - r * math.sin(e)
    large = 1 if abs(end_deg - start_deg) > 180 else 0
    return f"M {x1:.2f},{y1:.2f} A {r},{r} 0 {large},1 {x2:.2f},{y2:.2f}"

def gauge_svg(value, vmin, vmax, label, unit, color, w=160, h=130):
    """Half-circle gauge SVG."""
    cx  = w / 2
    cy  = h - 28          # centro del arco: deja 28px debajo para label/min/max
    r   = (w - 30) / 2
    pct = max(0, min(1, (value - vmin) / (vmax - vmin)))
    # Background arc 180° izq→der
    bg    = arc_path(cx, cy, r, 180, 0)
    # Value arc
    end_a = 180 - pct * 180
    val_a = arc_path(cx, cy, r, 180, end_a) if pct > 0 else ""
    # Needle
    angle = math.radians(180 - pct * 180)
    nx = cx + (r - 6) * math.cos(angle)
    ny = cy - (r - 6) * math.sin(angle)   # negado: eje Y invertido en SVG

    svg  = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += f'<path d="{bg}" fill="none" stroke="#1e2e14" stroke-width="14" stroke-linecap="round"/>\n'
    if val_a:
        svg += f'<path d="{val_a}" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round"/>\n'
    svg += f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="white" stroke-width="2.5" stroke-linecap="round"/>\n'
    svg += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="white"/>\n'
    # Valor grande centrado sobre el arco
    svg += f'<text x="{cx}" y="{cy-16}" text-anchor="middle" font-size="20" font-weight="700" fill="{color}" font-family="Arial">{value}</text>\n'
    svg += f'<text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="9" fill="#8a9a6a" font-family="Arial">{unit}</text>\n'
    # Min / max en los extremos del arco
    svg += f'<text x="{cx-r+4}" y="{cy+12}" text-anchor="start" font-size="8" fill="#6a7a4a" font-family="Arial">{vmin}</text>\n'
    svg += f'<text x="{cx+r-4}" y="{cy+12}" text-anchor="end"   font-size="8" fill="#6a7a4a" font-family="Arial">{vmax}</text>\n'
    # Label debajo
    svg += f'<text x="{cx}" y="{cy+24}" text-anchor="middle" font-size="10" fill="#c9a227" font-family="Arial" font-weight="700">{label}</text>\n'
    svg += '</svg>\n'
    return svg

def radar_svg(labels, values, w=260, h=240, color="#e74c3c"):
    """Hexagonal radar chart SVG (values 0–100)."""
    n = len(labels)
    cx, cy, r = w/2, h/2+4, min(w,h)*0.36
    angles = [math.radians(90 + i * 360 / n) for i in range(n)]

    svg  = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n'
    # Grid rings
    for ring in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{cx + r*ring*math.cos(a):.1f},{cy - r*ring*math.sin(a):.1f}" for a in angles)
        svg += f'<polygon points="{pts}" fill="none" stroke="#1e2e14" stroke-width="1"/>\n'
    # Spokes
    for a in angles:
        x, y = cx + r*math.cos(a), cy - r*math.sin(a)
        svg += f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#1e2e14" stroke-width="1"/>\n'
    # Filled area
    pts = " ".join(
        f"{cx + r*(v/100)*math.cos(angles[i]):.1f},{cy - r*(v/100)*math.sin(angles[i]):.1f}"
        for i, v in enumerate(values)
    )
    svg += f'<polygon points="{pts}" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="2"/>\n'
    # Dots
    for i, v in enumerate(values):
        x = cx + r*(v/100)*math.cos(angles[i])
        y = cy - r*(v/100)*math.sin(angles[i])
        svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>\n'
    # Labels
    for i, lbl in enumerate(labels):
        lx = cx + (r+20)*math.cos(angles[i])
        ly = cy - (r+20)*math.sin(angles[i])
        svg += f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" font-size="9" fill="#8a7a4a" font-family="Arial" font-weight="600">{lbl}</text>\n'
        sv = values[i]
        svg += f'<text x="{lx:.1f}" y="{ly+15:.1f}" text-anchor="middle" font-size="8" fill="{color}" font-family="Arial">{sv}</text>\n'
    svg += '</svg>\n'
    return svg

# Paleta de colores realistas por categoría: (base_light, base_mid, base_dark, accent)
BALL_PALETTE = {
    "Asym Solid":   ("#c0392b", "#7b1a1a", "#2a0808", "#ff6b6b"),
    "Asym Hybrid":  ("#2980b9", "#1a3a6a", "#050518", "#74b9ff"),
    "Sym Solid":    ("#27ae60", "#145a32", "#021a0a", "#55efc4"),
    "Sym Hybrid":   ("#8e44ad", "#4a1070", "#0d0020", "#d7aefb"),
    "Sym Pearl":    ("#16a085", "#0a4a40", "#011210", "#81ecec"),
    "Sym Pearl Hybrid": ("#1abc9c", "#0e6251", "#021a15", "#a3f5e8"),
    "Urethane":     ("#7f8c8d", "#2c3e50", "#080d12", "#b2bec3"),
    "Plastic":      ("#f1c40f", "#d4ac0d", "#503a00", "#ffeaa7"),
}

def ball_svg(category="Asym Hybrid", ball_name="", w=220, h=220):
    """Photorealistic bowling ball SVG — multi-layer gradients, specular, texture, holes."""
    cx, cy = w / 2, h / 2
    r = w * 0.43
    bl, bm, bd, ac = BALL_PALETTE.get(category, BALL_PALETTE["Asym Hybrid"])
    gid = "b" + str(abs(hash(category + ball_name)) % 99999)

    # Hole positions (finger: middle, ring, thumb)
    hm = (cx - r*0.14, cy + r*0.22, r*0.095)   # middle finger
    hr = (cx + r*0.18, cy + r*0.18, r*0.095)   # ring finger
    ht = (cx - r*0.24, cy - r*0.10, r*0.115)   # thumb

    s  = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
    s += '<defs>'
    # Base gradient — deep 3-stop from upper-left bright to dark lower-right
    s += f'<radialGradient id="base{gid}" cx="36%" cy="32%" r="70%">'
    s += f'  <stop offset="0%"   stop-color="{bl}"/>'
    s += f'  <stop offset="42%"  stop-color="{bm}"/>'
    s += f'  <stop offset="78%"  stop-color="{bd}"/>'
    s += f'  <stop offset="100%" stop-color="#000"/>'
    s += '</radialGradient>'
    # Large soft ambient reflection (lower-right)
    s += f'<radialGradient id="amb{gid}" cx="72%" cy="74%" r="55%">'
    s += f'  <stop offset="0%"   stop-color="{bm}" stop-opacity="0.35"/>'
    s += f'  <stop offset="100%" stop-color="{bd}"  stop-opacity="0"/>'
    s += '</radialGradient>'
    # Sharp specular hot-spot — upper-left
    s += f'<radialGradient id="spec{gid}" cx="30%" cy="26%" r="28%">'
    s += f'  <stop offset="0%"   stop-color="white" stop-opacity="0.92"/>'
    s += f'  <stop offset="18%"  stop-color="white" stop-opacity="0.55"/>'
    s += f'  <stop offset="55%"  stop-color="white" stop-opacity="0.08"/>'
    s += f'  <stop offset="100%" stop-color="white" stop-opacity="0"/>'
    s += '</radialGradient>'
    # Pearl / reactive texture (soft swirl overlay)
    is_pearl = "Pearl" in category
    s += f'<radialGradient id="tex{gid}" cx="55%" cy="48%" r="50%">'
    if is_pearl:
        s += f'  <stop offset="0%"  stop-color="{ac}" stop-opacity="0.18"/>'
        s += f'  <stop offset="50%" stop-color="{ac}" stop-opacity="0.06"/>'
    else:
        s += f'  <stop offset="0%"  stop-color="{ac}" stop-opacity="0.07"/>'
        s += f'  <stop offset="100%" stop-color="{ac}" stop-opacity="0"/>'
    s += '</radialGradient>'
    # Edge darkening (vignette)
    s += f'<radialGradient id="vig{gid}" cx="50%" cy="50%" r="50%">'
    s += f'  <stop offset="62%"  stop-color="black" stop-opacity="0"/>'
    s += f'  <stop offset="100%" stop-color="black" stop-opacity="0.72"/>'
    s += '</radialGradient>'
    # Hole gradient — realistic depth
    s += f'<radialGradient id="hole{gid}" cx="30%" cy="25%" r="75%">'
    s += f'  <stop offset="0%"   stop-color="#2a2a2a"/>'
    s += f'  <stop offset="100%" stop-color="#000"/>'
    s += '</radialGradient>'
    # Clip ball shape
    s += f'<clipPath id="clip{gid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    s += '</defs>'

    # ── Ball body ──
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#base{gid})"/>'
    # Ambient lower reflection
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#amb{gid})"/>'
    # Pearl/reactive surface texture
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#tex{gid})"/>'

    # ── Track ring (worn equatorial band) ──
    s += f'<ellipse cx="{cx:.1f}" cy="{cy + r*0.06:.1f}" rx="{r*0.76:.1f}" ry="{r*0.19:.1f}" fill="none" stroke="rgba(255,255,255,0.09)" stroke-width="8" clip-path="url(#clip{gid})"/>'
    s += f'<ellipse cx="{cx:.1f}" cy="{cy + r*0.06:.1f}" rx="{r*0.76:.1f}" ry="{r*0.19:.1f}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="14" clip-path="url(#clip{gid})"/>'

    # ── Finger holes ──
    for hx, hy, hr2 in [hm, hr, ht]:
        # Shadow ring
        s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr2+3:.1f}" fill="rgba(0,0,0,0.45)"/>'
        # Hole fill with depth gradient
        s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr2:.1f}" fill="url(#hole{gid})"/>'
        # Inner rim highlight
        s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr2:.1f}" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>'
        # Glint inside hole
        s += f'<circle cx="{hx - hr2*0.3:.1f}" cy="{hy - hr2*0.35:.1f}" r="{hr2*0.22:.1f}" fill="rgba(255,255,255,0.15)"/>'

    # ── Edge vignette ──
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#vig{gid})"/>'

    # ── Specular highlight (sharp hot-spot) ──
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#spec{gid})"/>'

    # ── Category label bottom ──
    s += f'<text x="{cx}" y="{cy + r + 15:.1f}" text-anchor="middle" font-size="10" fill="{ac}" font-family="Arial" font-weight="600" opacity="0.8">{category}</text>'

    s += '</svg>'
    return s

# ─────────────────────────────────────────────────────────────────────────────
# LANE SVG (mejorada)
# ─────────────────────────────────────────────────────────────────────────────

def lane_svg(pattern_length=40, pattern_name="House Shot",
             foot_board=25, target_board=15,
             breakpoint_board=7, breakpoint_depth=42,
             is_right_handed=True, W=150, H=600):
    """
    Lane top-down diagram in the style of technical bowling lane charts:
    - Light wood background visible above oil pattern
    - Blue heatmap oil pattern (denser center) from foul line to pattern_length
    - Gray pins in 4-3-2-1 triangle at top
    - Black playing line (hockey-stick bezier: drift then sharp hook)
    - Range dots (7ft), arrows (15ft), foul line
    - Right panel with key measurements in orange
    """
    GW   = 7               # gutter width (px)
    RP   = 72              # right panel width (px) — labels outside lane
    LW   = W - 2 * GW      # lane playable width
    TOP  = 28              # vertical padding above pins
    BOT  = 20              # below foul line (board number labels)
    LH   = H - TOP - BOT  # usable lane height

    # Board → pixel x
    # Board 1 = right gutter (RH) / left gutter (LH)
    def bx(b):
        frac = (b - 0.5) / 39.0
        return (GW + LW * (1.0 - frac)) if is_right_handed else (GW + LW * frac)

    # Feet from foul line → pixel y  (fy(0)=bottom=foul line, fy(60)=top=pins)
    def fy(ft):
        return TOP + LH - (ft / 60.0) * LH

    foul_y = fy(0)
    oil_y  = fy(pattern_length)
    arr_y  = fy(15)
    dot_y  = fy(7)
    pocket = 17 if is_right_handed else 22

    # ── Pin geometry (pre-calculado para usarlo en el path) ───────────────
    pin_row_gap   = 5              # px entre filas (triángulo muy comprimido)
    pin_base_y    = TOP + 4        # y de la fila trasera (7-8-9-10)
    headpin_row_y = pin_base_y + 3 * pin_row_gap   # y del headpin (1)

    # ── Playing line key points ───────────────────────────────────────────
    xF, yF = bx(foot_board),          foul_y
    xT, yT = bx(target_board),         arr_y
    xB, yB = bx(breakpoint_board),     fy(breakpoint_depth)
    xP, yP = bx(pocket),               headpin_row_y

    # Bezier — phase 1: gentle drift (foul → breakpoint)
    cp1x = bx(foot_board    + (target_board    - foot_board)    * 0.35)
    cp1y = fy(breakpoint_depth * 0.12)
    cp2x = bx(target_board  + (breakpoint_board - target_board) * 0.60)
    cp2y = fy(breakpoint_depth * 0.62)
    # Bezier — phase 2: hook (breakpoint → pocket)
    cp3x = bx(breakpoint_board + (pocket - breakpoint_board) * 0.10)
    cp3y = fy(breakpoint_depth + 3)
    cp4x = bx(breakpoint_board + (pocket - breakpoint_board) * 0.55)
    cp4y = fy(58.5)

    path = (f"M{xF:.1f},{yF:.1f} "
            f"C{cp1x:.1f},{cp1y:.1f} {cp2x:.1f},{cp2y:.1f} {xB:.1f},{yB:.1f} "
            f"C{cp3x:.1f},{cp3y:.1f} {cp4x:.1f},{cp4y:.1f} {xP:.1f},{yP:.1f}")

    # ── SVG ──────────────────────────────────────────────────────────────
    LP = 55              # panel izquierdo (patrón)
    TW = LP + W + RP     # ancho total: izq + pista + panel derecho
    s  = f'<svg width="{TW}" height="{H}" viewBox="0 0 {TW} {H}" xmlns="http://www.w3.org/2000/svg">\n'
    s += '<defs>\n'

    # Wood: warm blonde maple grain
    s += ('<linearGradient id="lwood" x1="0" y1="0" x2="1" y2="0">'
          '<stop offset="0%"   stop-color="#b87a28"/>'
          '<stop offset="18%"  stop-color="#d9a23c"/>'
          '<stop offset="50%"  stop-color="#e8b84e"/>'
          '<stop offset="82%"  stop-color="#d9a23c"/>'
          '<stop offset="100%" stop-color="#b87a28"/>'
          '</linearGradient>\n')

    # Oil vertical fade (solid at foul line, fades at oil end)
    s += ('<linearGradient id="loilV" x1="0" y1="1" x2="0" y2="0">'
          '<stop offset="0%"   stop-color="#0d3d82" stop-opacity="0.78"/>'
          '<stop offset="55%"  stop-color="#1257b0" stop-opacity="0.52"/>'
          '<stop offset="100%" stop-color="#1257b0" stop-opacity="0.05"/>'
          '</linearGradient>\n')

    # Oil horizontal: heavier in center boards (house shot profile)
    s += ('<linearGradient id="loilH" x1="0" y1="0" x2="1" y2="0">'
          '<stop offset="0%"   stop-color="#0a2a60" stop-opacity="0.0"/>'
          '<stop offset="12%"  stop-color="#0a2a60" stop-opacity="0.0"/>'
          '<stop offset="28%"  stop-color="#1565c0" stop-opacity="0.40"/>'
          '<stop offset="50%"  stop-color="#1976d2" stop-opacity="0.62"/>'
          '<stop offset="72%"  stop-color="#1565c0" stop-opacity="0.40"/>'
          '<stop offset="88%"  stop-color="#0a2a60" stop-opacity="0.0"/>'
          '<stop offset="100%" stop-color="#0a2a60" stop-opacity="0.0"/>'
          '</linearGradient>\n')

    # Gutter gradient
    s += ('<linearGradient id="lgut" x1="0" y1="0" x2="1" y2="0">'
          '<stop offset="0%"   stop-color="#5a3010"/>'
          '<stop offset="100%" stop-color="#7a4818"/>'
          '</linearGradient>\n')

    s += '</defs>\n'

    # ── Dark surround (area outside lane) ────────────────────────────────
    s += f'<rect width="{TW}" height="{H}" fill="#111118" rx="6"/>\n'

    # ── Panel izquierdo: patrón ───────────────────────────────────────────
    oc  = "#f39c12"
    dim = "rgba(255,180,60,0.55)"
    s += (f'<line x1="{LP}" y1="{oil_y:.1f}" x2="{LP-5}" y2="{oil_y:.1f}" stroke="{oc}" stroke-width="1.5"/>\n')
    s += (f'<text x="{LP-8}" y="{oil_y-5:.1f}" text-anchor="end" font-size="9.5" fill="{oc}" '
          f'font-family="Arial" font-weight="700">{pattern_length}ft</text>\n')
    s += (f'<text x="{LP-8}" y="{oil_y+7:.1f}" text-anchor="end" font-size="7.5" fill="{dim}" '
          f'font-family="Arial">{pattern_name}</text>\n')

    # ── Todo el contenido de pista desplazado LP px a la derecha ──────────
    s += f'<g transform="translate({LP},0)">\n'

    # ── Gutters ───────────────────────────────────────────────────────────
    s += f'<rect x="0"      y="{TOP}" width="{GW}"   height="{LH}" fill="url(#lgut)" rx="2"/>\n'
    s += f'<rect x="{W-GW}" y="{TOP}" width="{GW}"   height="{LH}" fill="url(#lgut)" rx="2"/>\n'

    # ── Main lane wood ────────────────────────────────────────────────────
    s += f'<rect x="{GW}" y="{TOP}" width="{LW}" height="{LH}" fill="url(#lwood)"/>\n'

    # Board grain lines (every 5 boards slightly darker)
    for b in range(5, 40, 5):
        x = bx(b)
        s += f'<line x1="{x:.1f}" y1="{TOP}" x2="{x:.1f}" y2="{foul_y:.1f}" stroke="#9a6820" stroke-width="0.9" opacity="0.55"/>\n'

    # ── Oil pattern (two layers: vertical fade + horizontal center weight) ─
    oy = oil_y;  oh = foul_y - oil_y
    s += f'<rect x="{GW}" y="{oy:.1f}" width="{LW}" height="{oh:.1f}" fill="url(#loilV)"/>\n'
    s += f'<rect x="{GW}" y="{oy:.1f}" width="{LW}" height="{oh:.1f}" fill="url(#loilH)"/>\n'

    # Subtle horizontal banding to simulate track/carry-down zones
    for band_ft, band_op in [(10, 0.08), (20, 0.06), (30, 0.04)]:
        if band_ft < pattern_length:
            by_ = fy(band_ft)
            bh_ = min(LH / 60 * 6, foul_y - by_)
            s += f'<rect x="{GW}" y="{by_:.1f}" width="{LW}" height="{bh_:.1f}" fill="#5a9de8" opacity="{band_op}"/>\n'

    # Oil end dashed line
    s += (f'<line x1="{GW}" y1="{oil_y:.1f}" x2="{W-GW}" y2="{oil_y:.1f}" '
          f'stroke="#88ccff" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.65"/>\n')

    # ── Gutter borders ────────────────────────────────────────────────────
    s += f'<line x1="{GW}" y1="{TOP}" x2="{GW}" y2="{foul_y:.1f}" stroke="#3a1e08" stroke-width="1.5"/>\n'
    s += f'<line x1="{W-GW}" y1="{TOP}" x2="{W-GW}" y2="{foul_y:.1f}" stroke="#3a1e08" stroke-width="1.5"/>\n'

    # ── Foul line (thin red bar) ──────────────────────────────────────────
    s += f'<rect x="{GW}" y="{foul_y:.1f}" width="{LW}" height="3" fill="#cc1111" opacity="0.9" rx="1"/>\n'

    # Board numbers at foul line (solo 10/20/30 muy tenues)
    for b in [10, 20, 30]:
        s += (f'<text x="{bx(b):.1f}" y="{foul_y+13:.1f}" text-anchor="middle" '
              f'font-size="7" fill="rgba(255,255,255,0.28)" font-family="Arial">{b}</text>\n')

    # ── Range dots (7 ft from foul line) ─────────────────────────────────
    for b in [3, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37, 39]:
        s += (f'<circle cx="{bx(b):.1f}" cy="{dot_y:.1f}" r="3.5" '
              f'fill="#606060" stroke="#909090" stroke-width="0.8" opacity="0.85"/>\n')

    # ── Arrows (15 ft) — triangles pointing toward pins ───────────────────
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax = bx(b)
        s += (f'<polygon points="{ax:.1f},{arr_y-5:.1f} {ax-3:.1f},{arr_y+4:.1f} {ax+3:.1f},{arr_y+4:.1f}" '
              f'fill="#7a5218" stroke="#6a4210" stroke-width="0.8" opacity="0.95"/>\n')

    # ── Pins (4-3-2-1 triangle, gray circles) ────────────────────────────
    # pin_row_gap y pin_base_y ya calculados arriba (antes del path)
    pin_r  = 3.5
    # (board, row) — row 0 = trasera (7-8-9-10), row 3 = headpin
    pin_spots = [
        (4.25,  0), (14.75, 0), (25.25, 0), (35.75, 0),  # 7-8-9-10
        (9.5,   1), (20.0,  1), (30.5,  1),               # 4-5-6
        (14.75, 2), (25.25, 2),                            # 2-3
        (20.0,  3),                                        # headpin (1)
    ]
    for pb, row in pin_spots:
        px = bx(pb);  py = pin_base_y + row * pin_row_gap
        s += f'<circle cx="{px+1.0:.1f}" cy="{py+1.0:.1f}" r="{pin_r:.1f}" fill="rgba(0,0,0,0.30)"/>\n'
        s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{pin_r:.1f}" fill="#d0d0d0" stroke="#aaa" stroke-width="1"/>\n'
        s += f'<circle cx="{px-1.2:.1f}" cy="{py-1.2:.1f}" r="{pin_r*0.38:.1f}" fill="rgba(255,255,255,0.45)"/>\n'

    # Pocket indicator: flecha debajo del headpin
    headpin_y = pin_base_y + 3 * pin_row_gap
    s += (f'<text x="{bx(pocket):.1f}" y="{headpin_y + pin_r + 10:.1f}" text-anchor="middle" '
          f'font-size="9" fill="#dd2222" font-family="Arial" font-weight="bold">▲</text>\n')

    # ── Playing line ─────────────────────────────────────────────────────
    # White halo for contrast over both wood and oil
    s += f'<path d="{path}" fill="none" stroke="rgba(255,255,255,0.50)" stroke-width="6" stroke-linecap="round"/>\n'
    # Shadow
    s += f'<path d="{path}" fill="none" stroke="rgba(0,0,0,0.35)" stroke-width="5" stroke-linecap="round"/>\n'
    # Main black line
    s += f'<path d="{path}" fill="none" stroke="#111" stroke-width="2.8" stroke-linecap="round"/>\n'

    # Start dot (posición en línea de falta) – blanco para visibilidad
    s += f'<circle cx="{xF:.1f}" cy="{yF:.1f}" r="5.5" fill="white" stroke="#444" stroke-width="1.2"/>\n'

    # Target ring (at arrows)
    s += f'<circle cx="{xT:.1f}" cy="{yT:.1f}" r="5"   fill="none" stroke="#111" stroke-width="2"/>\n'
    s += f'<circle cx="{xT:.1f}" cy="{yT:.1f}" r="1.8" fill="#111"/>\n'

    # Breakpoint dot
    s += f'<circle cx="{xB:.1f}" cy="{yB:.1f}" r="4" fill="#111" opacity="0.70"/>\n'

    # ── Panel lateral: medidas en naranja ─────────────────────────────────
    oc  = "#f39c12"
    dim = "rgba(255,180,60,0.55)"
    lx  = W + 5

    def side_label(sy, value, sub):
        out  = f'<line x1="{W}" y1="{sy:.1f}" x2="{W+5}" y2="{sy:.1f}" stroke="{oc}" stroke-width="1.5"/>\n'
        out += (f'<text x="{lx+6}" y="{sy-5:.1f}" font-size="9.5" fill="{oc}" '
                f'font-family="Arial" font-weight="700">Bd {int(value)}</text>\n')
        out += (f'<text x="{lx+6}" y="{sy+7:.1f}" font-size="7.5" fill="{dim}" '
                f'font-family="Arial">{sub}</text>\n')
        return out

    s += side_label(yF, foot_board,       "Posición")
    s += side_label(yT, target_board,     "Objetivo")
    s += side_label(yB, breakpoint_board, "Breakpt")

    s += '</g>\n'   # cierre del grupo translate(LP)
    s += '</svg>\n'
    return s

# ─────────────────────────────────────────────────────────────────────────────
# DRILL SVG (mejorada)
# ─────────────────────────────────────────────────────────────────────────────

def drill_svg(da=55, pin_to_pap=4.5, val=45,
              pap_right=5.0, pap_up=0.5,
              is_right_handed=True, is_asym=False, W=340, H=360):
    """
    Drill diagram - vista posterior de la bola estilo técnico de perforación.
    PAP siempre visible y centrado en zona derecha (RH) o izquierda (LH).
    PIN posicionado desde PAP usando DA y pin_to_pap.
    CG en centro geométrico de la bola.
    VAL: línea horizontal a través del PAP con arco de ángulo.
    """
    # ── Dimensiones y centro de la bola ───────────────────────────────────
    PAD = 20          # margen para labels
    ball_w = W - 2 * PAD
    cx = W / 2
    cy = H / 2
    R  = min(ball_w, H - 2 * PAD) / 2 * 0.92
    # Scale: bola de bowling = 8.5" de diámetro
    scale = (2 * R) / 8.5
    sign = 1 if is_right_handed else -1

    # ── PAP: posición fija dentro de la bola ─────────────────────────────
    # PAP está a pap_right pulgadas del CG (que es el centro de la bola)
    # Para que sea visible, limitamos la posición máxima a 0.72 * R
    pap_offset_x = min(pap_right * scale, R * 0.72)
    pap_offset_y = min(abs(pap_up) * scale, R * 0.30) * (-1 if pap_up >= 0 else 1)
    pap_x = cx + sign * pap_offset_x
    pap_y = cy + pap_offset_y

    # CG = centro geométrico de la bola
    cg_x, cg_y = cx, cy

    # ── PIN: desde PAP, a pin_to_pap" en dirección DA ────────────────────
    # DA=0 → PIN directamente arriba del PAP (hacia pins)
    # DA aumenta → PIN rota hacia el centro de la bola
    da_rad = math.radians(da)
    # Dirección: hacia arriba es -π/2; PIN rota sign*DA hacia el centro
    pin_angle = -math.pi / 2 - sign * da_rad
    pin_dist = pin_to_pap * scale
    pin_x = pap_x + math.cos(pin_angle) * pin_dist
    pin_y = pap_y + math.sin(pin_angle) * pin_dist
    # Asegurar que PIN esté dentro de la bola
    d = math.sqrt((pin_x - cx)**2 + (pin_y - cy)**2)
    if d > R - 15:
        f = (R - 15) / d
        pin_x = cx + (pin_x - cx) * f
        pin_y = cy + (pin_y - cy) * f

    # ── MB (Mass Bias) para asimétricas ──────────────────────────────────
    # MB perpendicular a línea PIN-PAP, hacia abajo-centro
    if is_asym:
        # Vector PIN→PAP normalizado
        vx = pap_x - pin_x;  vy = pap_y - pin_y
        vn = math.sqrt(vx**2 + vy**2) or 1
        # Perpendicular (hacia abajo para que MB quede debajo del CG)
        perp_x = -vy / vn;  perp_y = vx / vn
        # Asegurar que MB queda en la mitad inferior
        if perp_y < 0:
            perp_x, perp_y = -perp_x, -perp_y
        mb_dist = 2.2 * scale
        mb_x = pin_x + perp_x * mb_dist
        mb_y = pin_y + perp_y * mb_dist
        # Clamping
        d = math.sqrt((mb_x - cx)**2 + (mb_y - cy)**2)
        if d > R - 15:
            f = (R - 15) / d
            mb_x = cx + (mb_x - cx) * f
            mb_y = cy + (mb_y - cy) * f

    # ── Grip holes ────────────────────────────────────────────────────────
    # Posicionadas cerca del CG, ligeramente hacia el lado del PAP
    hole_off = sign * 0.4 * scale
    mf_x = cx - sign * 0.5 * scale + hole_off * 0.2
    mf_y = cy - 0.2 * scale
    rf_x = cx + sign * 0.6 * scale + hole_off * 0.2
    rf_y = cy - 0.9 * scale
    # Pulgar: abajo del CG, con separación realista
    th_x = cx + sign * 0.05 * scale
    th_y = cy + 1.65 * scale

    # ── X Hole (si aplica, en el opuesto al PIN) ──────────────────────────
    xh_x = pap_x - math.cos(pin_angle) * 0.9 * scale
    xh_y = pap_y - math.sin(pin_angle) * 0.9 * scale

    # ── SVG ──────────────────────────────────────────────────────────────
    Hsvg = H + 28
    gid  = "db"
    s  = f'<svg width="{W}" height="{Hsvg}" viewBox="0 0 {W} {Hsvg}" xmlns="http://www.w3.org/2000/svg">\n'
    s += '<defs>'
    # Bola: gradiente radial gris azulado para fondo técnico
    s += f'<radialGradient id="{gid}bg" cx="38%" cy="30%" r="70%">'
    s += '<stop offset="0%"   stop-color="#5a6a8a"/>'
    s += '<stop offset="50%"  stop-color="#2c3a5a"/>'
    s += '<stop offset="100%" stop-color="#111827"/>'
    s += '</radialGradient>'
    s += f'<radialGradient id="{gid}sh" cx="32%" cy="26%" r="45%">'
    s += '<stop offset="0%"   stop-color="rgba(255,255,255,0.18)"/>'
    s += '<stop offset="100%" stop-color="rgba(255,255,255,0)"/>'
    s += '</radialGradient>'
    s += f'<clipPath id="{gid}cl"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}"/></clipPath>'
    s += f'<marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">'
    s += '<path d="M0,0 L6,3 L0,6 Z" fill="#f1c40f"/>'
    s += '</marker>'
    s += '</defs>\n'

    # ── Bola (cuerpo) ─────────────────────────────────────────────────────
    s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="url(#{gid}bg)" stroke="#445" stroke-width="1.5"/>\n'
    s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="url(#{gid}sh)"/>\n'

    # ── Líneas de referencia del ecuador y meridiano (muy tenue) ──────────
    s += f'<line x1="{cx - R:.1f}" y1="{cy:.1f}" x2="{cx + R:.1f}" y2="{cy:.1f}" stroke="rgba(255,255,255,0.07)" stroke-width="1" clip-path="url(#{gid}cl)"/>\n'
    s += f'<line x1="{cx:.1f}" y1="{cy - R:.1f}" x2="{cx:.1f}" y2="{cy + R:.1f}" stroke="rgba(255,255,255,0.07)" stroke-width="1" clip-path="url(#{gid}cl)"/>\n'

    # ── Etiquetas de brújula ──────────────────────────────────────────────
    faint = "rgba(255,255,255,0.40)"
    s += f'<text x="{cx:.0f}" y="{cy - R - 5:.0f}" text-anchor="middle" font-size="11" fill="{faint}" font-family="Arial" font-weight="bold">12</text>\n'
    s += f'<text x="{cx:.0f}" y="{cy + R + 15:.0f}" text-anchor="middle" font-size="11" fill="{faint}" font-family="Arial" font-weight="bold">6</text>\n'
    s += f'<text x="{cx - R - 8:.0f}" y="{cy + 4:.0f}" text-anchor="end"    font-size="11" fill="{faint}" font-family="Arial" font-weight="bold">9</text>\n'
    s += f'<text x="{cx + R + 8:.0f}" y="{cy + 4:.0f}" text-anchor="start"  font-size="11" fill="{faint}" font-family="Arial" font-weight="bold">3</text>\n'

    # ── Línea PIN → PAP (medición de distancia) ──────────────────────────
    dx = pap_x - pin_x;  dy = pap_y - pin_y
    nn = math.sqrt(dx**2 + dy**2) or 1
    # Perpendicular para offset de label
    px_n = -dy / nn;  py_n = dx / nn
    mid_x = (pin_x + pap_x) / 2;  mid_y = (pin_y + pap_y) / 2
    loff = 13
    lbx = mid_x + px_n * loff;  lby = mid_y + py_n * loff
    s += f'<line x1="{pin_x:.1f}" y1="{pin_y:.1f}" x2="{pap_x:.1f}" y2="{pap_y:.1f}" stroke="#f1c40f" stroke-width="2" stroke-dasharray="6,3"/>\n'
    # Ticks en los extremos
    for ex, ey in [(pin_x, pin_y), (pap_x, pap_y)]:
        s += f'<line x1="{ex + py_n*6:.1f}" y1="{ey - px_n*6:.1f}" x2="{ex - py_n*6:.1f}" y2="{ey + px_n*6:.1f}" stroke="#f1c40f" stroke-width="1.8"/>\n'
    # Label de distancia con fracción
    frac_map = {0.25:"¼",0.5:"½",0.75:"¾",0.0:""}
    whole = int(pin_to_pap);  frac = pin_to_pap - whole
    frac_str = frac_map.get(round(frac*4)/4, f"{frac:.2f}".lstrip("0"))
    dist_label = f'{whole}{frac_str}"' if whole else f'{frac_str}"'
    s += f'<text x="{lbx:.1f}" y="{lby + 4:.1f}" text-anchor="middle" font-size="10" fill="#f1c40f" font-family="Arial" font-weight="bold">{dist_label}</text>\n'

    # ── Línea de referencia vertical desde PAP (12 o'clock) ──────────────
    ref_top_y = pap_y - R * 0.42
    s += f'<line x1="{pap_x:.1f}" y1="{pap_y:.1f}" x2="{pap_x:.1f}" y2="{ref_top_y:.1f}" stroke="rgba(255,255,255,0.28)" stroke-width="1.2" stroke-dasharray="5,3"/>\n'

    # ── Arco DA (desde referencia vertical hasta línea PIN-PAP) ──────────
    arc_r = 38
    # Ángulo de la línea vertical hacia arriba desde PAP = -π/2
    ref_ang  = -math.pi / 2
    pin_ang  = math.atan2(pin_y - pap_y, pin_x - pap_x)
    ax1 = pap_x + arc_r * math.cos(ref_ang)
    ay1 = pap_y + arc_r * math.sin(ref_ang)
    ax2 = pap_x + arc_r * math.cos(pin_ang)
    ay2 = pap_y + arc_r * math.sin(pin_ang)
    large_da = 1 if da > 180 else 0
    sweep_da = 1 if is_right_handed else 0   # RH: PIN va hacia la izquierda (CW en pantalla)
    s += f'<path d="M{ax1:.1f},{ay1:.1f} A{arc_r},{arc_r} 0 {large_da},{sweep_da} {ax2:.1f},{ay2:.1f}" fill="none" stroke="#c0392b" stroke-width="2.5" stroke-linecap="round"/>\n'
    # Label DA próximo al arco
    mid_arc_a = (ref_ang + pin_ang) / 2 if not is_right_handed else ref_ang + (pin_ang - ref_ang + 2*math.pi) % (2*math.pi) / 2
    # Simplificado: usar ángulo promedio con corrección de cuadrante
    avg_a = math.atan2(
        math.sin(ref_ang) + math.sin(pin_ang),
        math.cos(ref_ang) + math.cos(pin_ang)
    )
    da_lx = pap_x + (arc_r + 16) * math.cos(avg_a)
    da_ly = pap_y + (arc_r + 16) * math.sin(avg_a)
    s += f'<text x="{da_lx:.1f}" y="{da_ly + 4:.1f}" text-anchor="middle" font-size="10" fill="#e74c3c" font-family="Arial" font-weight="bold">{da:.0f}°</text>\n'

    # ── VAL line (horizontal a través de PAP) ─────────────────────────────
    # Se extiende desde el lado opuesto al PAP hasta el borde derecho/izquierdo
    val_len = R * 0.55
    vx1 = pap_x - sign * val_len
    vx2 = pap_x + sign * R * 0.18   # pequeño saliente en el lado del PAP
    s += f'<line x1="{vx1:.1f}" y1="{pap_y:.1f}" x2="{vx2:.1f}" y2="{pap_y:.1f}" stroke="#27ae60" stroke-width="1.8" stroke-dasharray="7,3" opacity="0.85"/>\n'
    # Arco VAL (desde VAL horizontal hasta la línea PIN-PAP)
    val_arc_r = arc_r + 20
    # VAL horizontal = ángulo -π (hacia la izquierda para RH)
    val_ref_ang = math.pi if is_right_handed else 0
    vax1 = pap_x + val_arc_r * math.cos(val_ref_ang)
    vay1 = pap_y + val_arc_r * math.sin(val_ref_ang)
    vax2 = pap_x + val_arc_r * math.cos(pin_ang)
    vay2 = pap_y + val_arc_r * math.sin(pin_ang)
    large_val = 1 if val > 180 else 0
    sweep_val = 0 if is_right_handed else 1
    s += f'<path d="M{vax1:.1f},{vay1:.1f} A{val_arc_r},{val_arc_r} 0 {large_val},{sweep_val} {vax2:.1f},{vay2:.1f}" fill="none" stroke="#27ae60" stroke-width="1.8" stroke-linecap="round" opacity="0.75"/>\n'
    # Label VAL
    val_avg_a = math.atan2(
        math.sin(val_ref_ang) + math.sin(pin_ang),
        math.cos(val_ref_ang) + math.cos(pin_ang)
    )
    vl_lx = pap_x + (val_arc_r + 14) * math.cos(val_avg_a)
    vl_ly = pap_y + (val_arc_r + 14) * math.sin(val_avg_a)
    s += f'<text x="{vl_lx:.1f}" y="{vl_ly + 4:.1f}" text-anchor="middle" font-size="10" fill="#27ae60" font-family="Arial" font-weight="bold">VAL {val:.0f}°</text>\n'

    # ── Grip holes ────────────────────────────────────────────────────────
    for hx, hy, hr, lbl in [
        (mf_x, mf_y, 9,  "MF"),
        (rf_x, rf_y, 9,  "RF"),
        (th_x, th_y, 12, "T"),
    ]:
        # Sombra
        s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr+4:.0f}" fill="rgba(0,0,0,0.5)"/>\n'
        # Agujero oscuro con borde blanco
        s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr:.0f}" fill="#050510" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>\n'
        # Label fuera del agujero
        lbl_y = hy - hr - 4
        s += f'<text x="{hx:.1f}" y="{lbl_y:.1f}" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.65)" font-family="Arial">{lbl}</text>\n'

    # ── CG (centro de gravedad = centro de la bola) ───────────────────────
    s += f'<circle cx="{cg_x:.1f}" cy="{cg_y:.1f}" r="5" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>\n'
    s += f'<line x1="{cg_x-7:.1f}" y1="{cg_y:.1f}" x2="{cg_x+7:.1f}" y2="{cg_y:.1f}" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>\n'
    s += f'<line x1="{cg_x:.1f}" y1="{cg_y-7:.1f}" x2="{cg_x:.1f}" y2="{cg_y+7:.1f}" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>\n'
    s += f'<text x="{cg_x - 10:.1f}" y="{cg_y - 8:.1f}" text-anchor="end" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Arial">CG</text>\n'

    # ── PAP (Positive Axis Point) ─────────────────────────────────────────
    # Cruz grande azul con círculo
    cross = 8
    s += f'<circle cx="{pap_x:.1f}" cy="{pap_y:.1f}" r="14" fill="rgba(52,152,219,0.15)" stroke="#3498db" stroke-width="2"/>\n'
    s += f'<line x1="{pap_x - cross:.1f}" y1="{pap_y:.1f}" x2="{pap_x + cross:.1f}" y2="{pap_y:.1f}" stroke="#3498db" stroke-width="2.5"/>\n'
    s += f'<line x1="{pap_x:.1f}" y1="{pap_y - cross:.1f}" x2="{pap_x:.1f}" y2="{pap_y + cross:.1f}" stroke="#3498db" stroke-width="2.5"/>\n'
    s += f'<text x="{pap_x + sign*18:.1f}" y="{pap_y - 12:.1f}" text-anchor="{"start" if is_right_handed else "end"}" font-size="11" fill="#3498db" font-family="Arial" font-weight="bold">PAP</text>\n'
    s += f'<text x="{pap_x + sign*18:.1f}" y="{pap_y:.1f}" text-anchor="{"start" if is_right_handed else "end"}" font-size="9" fill="#1a6090" font-family="Arial">{pap_right}″ {("+" if pap_up >= 0 else "")}{pap_up}″</text>\n'

    # ── PIN ───────────────────────────────────────────────────────────────
    s += f'<circle cx="{pin_x:.1f}" cy="{pin_y:.1f}" r="12" fill="rgba(243,156,18,0.2)" stroke="#f39c12" stroke-width="2.5"/>\n'
    s += f'<circle cx="{pin_x:.1f}" cy="{pin_y:.1f}" r="4"  fill="#f39c12"/>\n'
    s += f'<text x="{pin_x:.1f}" y="{pin_y - 16:.1f}" text-anchor="middle" font-size="11" fill="#f39c12" font-family="Arial" font-weight="bold">Pin</text>\n'

    # ── MB (Mass Bias) ────────────────────────────────────────────────────
    if is_asym:
        s += f'<polygon points="{mb_x:.1f},{mb_y - 10:.1f} {mb_x - 8:.1f},{mb_y + 7:.1f} {mb_x + 8:.1f},{mb_y + 7:.1f}" fill="rgba(231,76,60,0.3)" stroke="#e74c3c" stroke-width="2"/>\n'
        s += f'<text x="{mb_x:.1f}" y="{mb_y + 21:.1f}" text-anchor="middle" font-size="10" fill="#e74c3c" font-family="Arial" font-weight="bold">MB</text>\n'

    # ── Leyenda inferior ──────────────────────────────────────────────────
    items = [
        ("⊕", "#3498db", "PAP"),
        ("●", "#f39c12", "Pin"),
        ("━", "#f1c40f", f"{pin_to_pap}\""),
        ("━", "#c0392b", f"DA {da:.0f}°"),
        ("━", "#27ae60", f"VAL {val:.0f}°"),
    ]
    if is_asym:
        items.append(("▲", "#e74c3c", "MB"))
    ly_leg = H + 18
    lx_step = W / len(items)
    for i, (sym, clr, lbl) in enumerate(items):
        lx = lx_step * i + lx_step / 2
        s += f'<text x="{lx:.0f}" y="{ly_leg}" text-anchor="middle" font-size="9" fill="{clr}" font-family="Arial">{sym} {lbl}</text>\n'

    s += '</svg>\n'
    return s

# ─────────────────────────────────────────────────────────────────────────────
# BALL IMAGE FETCHER
# ─────────────────────────────────────────────────────────────────────────────

# Mapa fabricante → URL base
MANUFACTURER_URLS = {
    "storm":      "https://www.stormbowling.com/balls/{slug}",
    "roto grip":  "https://www.rotogrip.com/balls/{slug}",
    "rotogrip":   "https://www.rotogrip.com/balls/{slug}",
    "brunswick":  "https://www.brunswickbowling.com/balls/{slug}",
    "hammer":     "https://www.hammerbowling.com/balls/{slug}",
    "motiv":      "https://motivbowling.com/balls/{slug}",
    "track":      "https://trackbowling.com/balls/{slug}",
    "900 global": "https://www.900global.com/balls/{slug}",
    "columbia":   "https://www.columbia300.com/balls/{slug}",
    "ebonite":    "https://www.ebonite.com/balls/{slug}",
    "dv8":        "https://www.dv8bowling.com/balls/{slug}",
}

# Catálogos reales que devuelven HTML con links a bolas individuales
CATALOG_URLS = {
    "storm":      "https://www.stormbowling.com/products/equipment/bowling-balls/",
    "roto grip":  "https://www.rotogrip.com/products/equipment/bowling-balls/",
    "rotogrip":   "https://www.rotogrip.com/products/equipment/bowling-balls/",
    "brunswick":  "https://www.brunswickbowling.com/balls/",
    "hammer":     "https://www.hammerbowling.com/balls/",
    "motiv":      "https://motivbowling.com/balls/",
    "track":      "https://trackbowling.com/balls/",
    "900 global": "https://www.900global.com/balls/",
    "columbia":   "https://www.columbia300.com/balls/",
    "ebonite":    "https://www.ebonite.com/balls/",
    "dv8":        "https://www.dv8bowling.com/balls/",
}

# Slugs exactos verificados en el catálogo activo del fabricante (marzo 2026).
# Usar estos slugs evita el keyword-matching fallido sobre bolas descatalogadas.
# Actualizar aquí cuando una bola nueva se añada al catálogo.
KNOWN_SLUG_MAP: dict[str, dict[str, str]] = {
    "storm": {
        "phaze ii":           "bbmtza-phaze-ii",
        "phaze ii pearl":     "bbmvzp-phaze-ii-pearl",
        "phaze ai":           "bbmvzi-phaze-ai",
        "hy-road":            "bbmtty-hy-road",
        "hy road":            "bbmtty-hy-road",
        "hyroad":             "bbmtty-hy-road",
        "hy-road 40":         "bbmvhy-hy-road-40",
        "pitch black":        "bbmtub-pitch-black",
        "ion max":            "bbmvio-ion-max",
        "ion max pearl":      "bbmvim-ion-max-pearl",
        "ion pro":            "bbmvip-ion-pro",
        "ion pro solid":      "bbmvis-ion-pro-solid",
        "bionic":             "bbmvbi-bionic",
        "concept":            "bbmvcn-concept",
        "equinox":            "bbmveq-equinox",
        "equinox solid":      "bbmvxd-equinox-solid",
        "level":              "bbmvle-level",
        "next factor":        "bbmvxf-next-factor",
        "q tour":             "bbmtqt-q-tour-edition",
        "q tour ai":          "bbmvqa-q-tour-ai",
        "q tour 78u":         "bbmvll-q-tour-78u",
        "road warrior":       "bbmvwr-road-warrior",
        "typhoon":            "bbmvty-typhoon",
        "identity":           "bbmvid-identity",
        "identity bcp":       "bbmvdb-identity-bcp",
        "tropical surge":     "bt1vkk-tropical-surge-black-blue-pink",
    },
    # Roto Grip — rellenar tras verificar con el catálogo de rotogrip.com
    "roto grip": {},
    "rotogrip":  {},
}

# Bases para construir URLs absolutas desde hrefs relativos
BASE_URLS = {
    "storm":      "https://www.stormbowling.com",
    "roto grip":  "https://www.rotogrip.com",
    "rotogrip":   "https://www.rotogrip.com",
    "brunswick":  "https://www.brunswickbowling.com",
    "hammer":     "https://www.hammerbowling.com",
    "motiv":      "https://motivbowling.com",
    "track":      "https://trackbowling.com",
    "900 global": "https://www.900global.com",
    "columbia":   "https://www.columbia300.com",
    "ebonite":    "https://www.ebonite.com",
    "dv8":        "https://www.dv8bowling.com",
}

# Detecta fabricante por prefijo del nombre de la bola
MANUFACTURER_PREFIXES = [
    ("storm ",      "storm"),
    ("roto grip ",  "roto grip"),
    ("brunswick ",  "brunswick"),
    ("hammer ",     "hammer"),
    ("motiv ",      "motiv"),
    ("track ",      "track"),
    ("900 global ", "900 global"),
    ("columbia ",   "columbia"),
    ("ebonite ",    "ebonite"),
    ("dv8 ",        "dv8"),
]

# Regex para capturar URLs de imágenes de producto en HTML
_IMG_PATTERNS = [
    # og:image (la más fiable — thumbnail de producto)
    re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https?://[^"\'>\s]+)["\']', re.I),
    re.compile(r'<meta[^>]+content=["\'](https?://[^"\'>\s]+)["\'][^>]+property=["\']og:image["\']', re.I),
    # JSON-LD "image"
    re.compile(r'"image"\s*:\s*["\'](https?://[^"\'>\s]+\.(?:jpg|jpeg|png|webp))["\']', re.I),
    # <img> con 'ball' o el slug en la src
    re.compile(r'<img[^>]+src=["\'](https?://[^"\'>\s]+(?:ball|product|item)[^"\'>\s]*\.(?:jpg|jpeg|png|webp))["\']', re.I),
    # Cualquier <img> con extensión de imagen en src
    re.compile(r'<img[^>]+src=["\'](https?://[^"\'>\s]+\.(?:jpg|jpeg|png|webp)(?:\?[^"\'>\s]*)?)["\']', re.I),
]

_ROMAN = {"ii": "2", "iii": "3", "iv": "4", "vi": "6", "vii": "7", "viii": "8"}

def _to_slug(name: str) -> str:
    """'Storm Phaze II' → 'phaze-ii'  (elimina el prefijo del fabricante si está)."""
    nl = name.lower().strip()
    for prefix, _ in MANUFACTURER_PREFIXES:
        if nl.startswith(prefix):
            nl = nl[len(prefix):]
            break
    slug = re.sub(r'[^a-z0-9]+', '-', nl).strip('-')
    return slug

def _slug_variants(slug: str):
    """Genera variantes del slug para aumentar tasa de éxito."""
    variants = [slug]
    # Números → romanos y viceversa
    with_nums = slug
    for roman, num in _ROMAN.items():
        with_nums = re.sub(rf'\b{roman}\b', num, with_nums)
    if with_nums != slug:
        variants.append(with_nums)
    with_roman = slug
    for roman, num in _ROMAN.items():
        with_roman = re.sub(rf'\b{num}\b', roman, with_roman)
    if with_roman != slug:
        variants.append(with_roman)
    # Prefijo 'the-'
    variants.append("the-" + slug)
    # Sin el último segmento numérico (ej. 'phaze-3-0' → 'phaze-3')
    shorter = re.sub(r'-\d+$', '', slug)
    if shorter != slug:
        variants.append(shorter)
    return variants

def _detect_manufacturer(name: str):
    nl = name.lower()
    for prefix, mfr in MANUFACTURER_PREFIXES:
        if nl.startswith(prefix):
            return mfr
    return None

def _fetch_html(url: str, timeout: int, referer: str = "") -> str:
    import gzip as _gzip, zlib as _zlib
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        enc = resp.headers.get("Content-Encoding", "")
        if enc == "gzip":
            raw = _gzip.decompress(raw)
        elif enc == "deflate":
            raw = _zlib.decompress(raw)
        charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")

def _extract_img(html: str, skip_words=("logo","icon","favicon","header","footer","banner","placeholder")) -> str:
    for pat in _IMG_PATTERNS:
        for m in pat.finditer(html):
            url = m.group(1)
            if not any(s in url.lower() for s in skip_words):
                return url
    return ""

# CDN directas que no pasan por Cloudflare — fabricante → patrón URL de imagen
_CDN_PATTERNS = {
    "storm":     "https://www.stormbowling.com/media/catalog/product/{a}/{b}/{slug}.jpg",
    "roto grip": "https://www.rotogrip.com/media/catalog/product/{a}/{b}/{slug}.jpg",
    "rotogrip":  "https://www.rotogrip.com/media/catalog/product/{a}/{b}/{slug}.jpg",
}

def _try_cdn_image(ball_name: str, mfr: str, timeout: int) -> tuple:
    """
    Intenta URL directa de CDN Magento del fabricante (no pasa por JS/Cloudflare).
    Variantes: slug, slug_1, slug_2, slug con numerales romanos, etc.
    """
    import urllib.error as _ue
    pattern = _CDN_PATTERNS.get(mfr, "")
    if not pattern:
        return "", ""
    slug = _to_slug(ball_name)
    for sv in [slug] + _slug_variants(slug)[1:]:
        a = sv[0] if sv else "a"
        b = sv[1] if len(sv) > 1 else "a"
        for suffix in ["", "_1", "_2", "-1"]:
            img_url = pattern.format(a=a, b=b, slug=sv + suffix)
            try:
                req = urllib.request.Request(img_url,
                    headers={"User-Agent": "Mozilla/5.0", "Accept": "image/*"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    if r.status == 200 and r.headers.get("Content-Type","").startswith("image"):
                        print(f"  ✅ CDN fabricante: {img_url[:80]}")
                        return img_url, ""
            except Exception:
                continue
    return "", ""


def _fetch_from_bowlingball_com(ball_name: str, mfr: str, timeout: int) -> tuple:
    """
    Intenta bowlingball.com con headers completos de navegador real.
    URL patrón: https://www.bowlingball.com/BowlVerts/Products/{mfr}-{slug}-bowling-ball
    Devuelve (image_url, page_url) o ("", search_url).
    """
    import urllib.parse as _up
    slug = _to_slug(ball_name)
    mfr_slug = mfr.replace(" ", "-")

    candidates = [f"https://www.bowlingball.com/BowlVerts/Products/{mfr_slug}-{slug}-bowling-ball"]
    for sv in _slug_variants(slug)[1:]:
        candidates.append(f"https://www.bowlingball.com/BowlVerts/Products/{mfr_slug}-{sv}-bowling-ball")

    referer = "https://www.bowlingball.com/"
    for page_url in candidates:
        try:
            html = _fetch_html(page_url, timeout, referer=referer)
            if "404" in html[:2000] and "not found" in html[:2000].lower():
                continue
            if len(html) < 500:  # respuesta vacía / bloqueo
                continue
            img = _extract_img(html)
            if img:
                if img.startswith("//"):
                    img = "https:" + img
                print(f"  ✅ bowlingball.com: {img[:80]}...")
                return img, page_url
        except Exception as e:
            print(f"  ⚠️  bowlingball.com: {e}")
            continue

    search_url = "https://www.bowlingball.com/BowlVerts/search/?q=" + _up.quote(ball_name)
    return "", search_url


def fetch_ball_image_url(ball_name: str, manufacturer: str = None, timeout: int = 12) -> tuple:
    """
    Obtiene imagen + URL de página del producto de una bola.
    Estrategia principal: catálogo del fabricante (leer HTML completo → buscar href → og:image).
    Storm/Roto-Grip sirven HTML estático completo con todos los links de producto.
    Devuelve (image_url, page_url).
    """
    import urllib.parse as _up
    mfr = (manufacturer or "").lower().strip() or _detect_manufacturer(ball_name) or ""
    if not mfr or mfr not in CATALOG_URLS:
        return "", ""

    catalog_url = CATALOG_URLS[mfr]
    base_url    = BASE_URLS.get(mfr, "")
    slug        = _to_slug(ball_name)
    keywords    = [w for w in slug.split("-") if len(w) > 2]

    # ── Paso 0: slug exacto del KNOWN_SLUG_MAP (más fiable y rápido) ────────
    ball_name_norm = ball_name.lower().strip()
    # Eliminar prefijo del fabricante para la búsqueda (ej: "storm phaze ii" → "phaze ii")
    for prefix in (mfr + " ", ):
        if ball_name_norm.startswith(prefix):
            ball_name_norm = ball_name_norm[len(prefix):]
    known_slugs = KNOWN_SLUG_MAP.get(mfr, {})
    known_slug = known_slugs.get(ball_name_norm, "")
    if known_slug:
        product_url = f"{base_url}/products/equipment/bowling-balls/{known_slug}"
        try:
            ball_html = _fetch_html(product_url, timeout, referer=catalog_url)
            img = _extract_img(ball_html)
            if img:
                if img.startswith("//"):  img = "https:" + img
                elif img.startswith("/"): img = base_url + img
                return img, product_url
        except Exception as e:
            print(f"  ⚠️  known_slug {product_url} → {e}")
        # Si falla la URL del slug conocido → continuar con búsqueda por catálogo

    # ── Paso 1: descargar catálogo completo ──────────────────────────────────
    try:
        catalog_html = _fetch_html(catalog_url, timeout)
    except Exception as e:
        print(f"  ⚠️  catálogo {catalog_url} → {e}")
        return "", ""

    # ── Paso 2: localizar href del producto en el catálogo ───────────────────
    href_pat = re.compile(r'href=["\']([^"\'> ]+)["\']', re.I)
    seen = set(); unique_candidates = []
    for m in href_pat.finditer(catalog_html):
        href = m.group(1)
        hl = href.lower()
        if sum(1 for kw in keywords if kw in hl) >= min(2, len(keywords)):
            full = href if href.startswith("http") else base_url + (href if href.startswith("/") else "/" + href)
            if full not in seen:
                seen.add(full)
                unique_candidates.append(full)

    # ── Paso 3: visitar cada candidato y extraer og:image ───────────────────
    for url in unique_candidates[:5]:
        try:
            ball_html = _fetch_html(url, timeout, referer=catalog_url)
            img = _extract_img(ball_html)
            if img:
                if img.startswith("//"):
                    img = "https:" + img
                elif img.startswith("/"):
                    img = base_url + img
                return img, url
        except Exception as e:
            print(f"  ⚠️  {url} → {e}")
            continue

    return "", ""

# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT EXPLANATION
# ─────────────────────────────────────────────────────────────────────────────

def layout_explain(da: float, ptp: float, val: float,
                  is_asym: bool, friction_need: str,
                  style: str, ball_name: str) -> str:
    """
    Genera un bloque HTML explicando en lenguaje natural qué hace este layout,
    cuándo usarlo y dónde jugar en pista.
    """

    # ─ DA: controla la longitud y el flare ──────────────────────────
    if da <= 35:
        da_desc = "DA bajo (≤35°) — la bola tendrá <strong>mayor continuidad</strong> y leerá el patrón más pronto. Ideal para patrones cortos o condiciones secas."
        da_icon = "🟢"
        da_when = "Short patterns, condiciones secas, jugadores que necesitan gancho suave y control."
    elif da <= 55:
        da_desc = "DA medio (36–55°) — equilibrio entre <strong>longitud y reakción en backend</strong>. El uso más versátil, válido para la mayoría de situaciones."
        da_icon = "🟡"
        da_when = "Patrones medianos (38–42ft), house shots, condiciones neutras."
    else:
        da_desc = "DA alto (>55°) — la bola <strong>aguanta más en el aceite</strong> y tiene una reacción más abrupta al final. Ideal para patrones largos o condiciones mojadas."
        da_icon = "🔴"
        da_when = "Long patterns, sport shots, condiciones pesadas de aceite."

    # ─ Pin-to-PAP: flare potential ───────────────────────────
    if ptp < 3.0:
        ptp_desc = f"Pin-to-PAP {ptp}\" corto — <strong>flare mínimo</strong>, bola más lenta y continua. Track alto."
        ptp_when = "Jugadores con alto rev rate que necesitan calmar la bola."
    elif ptp <= 4.5:
        ptp_desc = f"Pin-to-PAP {ptp}\" medio — <strong>flare moderado</strong>. Buen equilibrio entre cobertura de aceite y backend."
        ptp_when = "Perfil genérico: tweener o stroker en condiciones normales."
    elif ptp <= 5.5:
        ptp_desc = f"Pin-to-PAP {ptp}\" largo — <strong>máximo flare</strong>. La bola absorbe más aceite y tiene mayor potencial de gancho."
        ptp_when = "Rev-dominant o crankers en patrones pesados."
    else:
        ptp_desc = f"Pin-to-PAP {ptp}\" muy largo — <strong>flare máximo absoluto</strong>, solo recomendable en condiciones muy pesadas."
        ptp_when = "Crankers extremos o petroléo muy pesado."

    # ─ VAL: fase de gancho / timing ───────────────────────────
    if val <= 30:
        val_desc = f"VAL {val:.0f}° bajo — <strong>la bola se mueve pronto</strong>, con gancho suave y temprano."
        val_when = "Patrones cortos, condiciones secas o jugadores con velocidad alta."
    elif val <= 55:
        val_desc = f"VAL {val:.0f}° medio — <strong>transición equilibrada</strong>. La bola mantiene la línea y quiebra en la ventana."
        val_when = "Uso general, la gran mayoría de combinaciones jugador/patrón."
    else:
        val_desc = f"VAL {val:.0f}° alto — <strong>gancho tardío y fuerte</strong>. La bola aguanta en línea hasta el último momento."
        val_when = "Patrones largos o sport shots donde se busca máximo ángulo al pocket."

    # ─ Dónde jugar ─────────────────────────────────────
    style_l = style.lower()
    if "stroker" in style_l:
        where = "Línea directa, entre el 2º y 3er flecha. Juega más hacia el centro que otros estilos."
    elif "cranker" in style_l:
        where = "Línea ancha: pies en tablas 35–40, target en 10–12, breakpoint en tablas 5–7."
    elif "two-hand" in style_l or "two hand" in style_l:
        where = "Línea muy ancha. Ajusta el breakpoint entre tablas 3–8 según el patrón."
    else:  # tweener
        where = "Línea media: pies en tablas 25–30, target entre 2º y 3er flecha, breakpoint tablas 6–9."

    # ─ HTML output ───────────────────────────────────────
    asym_note = (
        "<li><strong>Bola Asym:</strong> La posición del Mass Bias también influye. "
        "Colocar MB a 45–90° del PAP reduce la reacción; más cerca del VAL la incrementa.</li>"
    ) if is_asym else ""

    return f'''
<div style="margin-top:14px;border-top:1px solid #101028;padding-top:12px;">
  <div style="font-size:.68em;text-transform:uppercase;letter-spacing:2px;color:#9b59b6;margin-bottom:10px;">ℹ️ Qué hace este layout</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;margin-bottom:12px;">
    <div style="background:#0a0a1e;border-radius:8px;padding:10px;border-left:3px solid #9b59b6;">
      <div style="font-size:.72em;font-weight:700;color:#9b59b6;">{da_icon} DA {da:.0f}°</div>
      <div style="font-size:.75em;color:#9a9ab8;margin-top:4px;line-height:1.5;">{da_desc}</div>
    </div>
    <div style="background:#0a0a1e;border-radius:8px;padding:10px;border-left:3px solid #f39c12;">
      <div style="font-size:.72em;font-weight:700;color:#f39c12;">📏 Pin-to-PAP {ptp}"</div>
      <div style="font-size:.75em;color:#9a9ab8;margin-top:4px;line-height:1.5;">{ptp_desc}</div>
    </div>
    <div style="background:#0a0a1e;border-radius:8px;padding:10px;border-left:3px solid #00ced1;">
      <div style="font-size:.72em;font-weight:700;color:#00ced1;">🔄 VAL {val:.0f}°</div>
      <div style="font-size:.75em;color:#9a9ab8;margin-top:4px;line-height:1.5;">{val_desc}</div>
    </div>
  </div>
  <ul style="list-style:none;padding:0;font-size:.78em;color:#8a8aaa;line-height:1.7;">
    <li><span style="color:#3498db;font-weight:700;">🕹️ Cuándo usar esta bola:</span>&nbsp; {da_when}</li>
    <li><span style="color:#3498db;font-weight:700;">🎯 Cuándo usar este Pin-to-PAP:</span>&nbsp; {ptp_when}</li>
    <li><span style="color:#3498db;font-weight:700;">📍 Cuándo usar este VAL:</span>&nbsp; {val_when}</li>
    <li><span style="color:#3498db;font-weight:700;">🏳️ Dónde jugar en pista:</span>&nbsp; {where}</li>
    {asym_note}
  </ul>
</div>
'''

# ─────────────────────────────────────────────────────────────────────────────
# HTML REPORT
# ─────────────────────────────────────────────────────────────────────────────

def generate_html(data: dict) -> str:
    p  = data.get("player", {})
    pt = data.get("pattern", {})
    b  = data.get("ball", {})
    lyt= data.get("layout", {})
    dx = data.get("diagnosis", {})
    adj= data.get("adjustments", [])
    ref= data.get("to_refine", [])

    speed     = float(p.get("speed", 15))
    rev       = int(p.get("rev_rate", 300))
    name      = p.get("name", "Jugador")
    style     = p.get("style", "tweener")
    is_rh     = bool(p.get("is_right_handed", True))
    pap_r     = float(p.get("pap_right", 5.0))
    pap_u     = float(p.get("pap_up", 0.5))
    ax_rot    = float(p.get("axis_rotation", 45))
    ax_tilt   = float(p.get("axis_tilt", 15))

    is_asym   = bool(b.get("is_asym", False))
    da_val    = float(lyt.get("da", 55))
    ptp_val   = float(lyt.get("pin_to_pap", 4.5))
    val_val   = float(lyt.get("val", 45))
    pattern_len = int(pt.get("length", 40))

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    hand = "Diestro" if is_rh else "Zurdo"

    # Logo LunaBowling embebido en base64
    import base64, os
    _logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.jpeg")
    try:
        with open(_logo_path, "rb") as _f:
            _logo_b64 = "data:image/jpeg;base64," + base64.b64encode(_f.read()).decode()
    except Exception:
        _logo_b64 = ""

    # PBA match
    pba = find_pba_match(style, speed, rev)

    # Radar values (0–100)
    hook_pct   = min(100, int(rev / 6))
    speed_pct  = min(100, int(speed / 0.22))
    power_pct  = min(100, int((rev * 0.5 + speed * 8) / 8))
    control_pct= max(0, 100 - hook_pct // 2)
    angle_pct  = min(100, int(ax_rot * 1.1))
    consist_pct= min(100, 50 + int(speed * 2))
    radar = radar_svg(
        ["Hook","Velocidad","Potencia","Control","Ángulo","Consistencia"],
        [hook_pct, speed_pct, power_pct, control_pct, angle_pct, consist_pct],
        color="#cc2200"
    )
    radar_pba = radar_svg(
        ["Hook","Velocidad","Potencia","Control","Ángulo","Consistencia"],
        [min(100,int(pba["rev"]/6)), min(100,int(pba["speed"]/0.22)),
         min(100,int((pba["rev"]*0.5+pba["speed"]*8)/8)),
         max(0,100-min(100,int(pba["rev"]/6))//2), 55, 88],
        color="#c9a227"
    )

    # Gauges
    g_speed = gauge_svg(speed, 10, 24, "VELOCIDAD", "mph", "#c9a227")
    g_rev   = gauge_svg(rev, 100, 600, "REV RATE", "rpm", "#cc2200")
    g_rot   = gauge_svg(ax_rot, 0, 90, "ROTATION", "°", "#8ab840")
    g_tilt  = gauge_svg(ax_tilt, 0, 40, "TILT", "°", "#c9a227")

    # SVGs — imagen de bola
    # Si el JSON trae image_url, úsala directamente.
    # Si no, generamos el HTML con un loader JS que el NAVEGADOR resuelve
    # (Chrome puede acceder a las webs del fabricante; Python no puede por bot-blocking).
    ball_name_str = b.get("name", "")
    ball_img      = b.get("image_url", "")       # URL directa proporcionada por el usuario
    ball_page_url = b.get("product_url", "")

    # Construir candidate URLs para que el navegador las intente en orden
    def _ball_cdn_candidates(name: str, mfr: str) -> list:
        """Genera lista de URLs que el navegador intentará cargar en orden."""
        import urllib.parse as _up
        slug = _to_slug(name)
        mfr_s = mfr.replace(" ", "-")
        a = slug[0] if slug else "a"
        b2 = slug[1] if len(slug) > 1 else "a"
        cands = []
        for sv in [slug] + _slug_variants(slug):
            a2, b3 = (sv[0], sv[1]) if len(sv) > 1 else (a, b2)
            # Storm/Roto-Grip Magento CDN
            if mfr in ("storm", "roto grip", "rotogrip"):
                base = "https://www.stormbowling.com" if mfr == "storm" else "https://www.rotogrip.com"
                for suffix in ["", "_1", "_2"]:
                    for ext in [".jpg", ".png", ".webp"]:
                        cands.append(f"{base}/media/catalog/product/{a2}/{b3}/{sv}{suffix}{ext}")
            # Brunswick/DV8/Hammer Magento CDN
            for b_base, b_mfr in [("https://www.brunswickbowling.com", "brunswick"),
                                   ("https://www.dv8bowling.com", "dv8"),
                                   ("https://www.hammerbowling.com", "hammer")]:
                if mfr == b_mfr:
                    for suffix in ["", "_1"]:
                        cands.append(f"{b_base}/media/catalog/product/{a2}/{b3}/{sv}{suffix}.jpg")
            # bowlingball.com product page OG image (browser puede acceder)
            cands.append(f"https://www.bowlingball.com/BowlVerts/Products/{mfr_s}-{sv}-bowling-ball")
        return cands

    mfr_detected = (b.get("manufacturer", "") or _detect_manufacturer(ball_name_str) or "").lower()
    svg_fallback = ball_svg(b.get("category", "Asym Hybrid"), ball_name_str)
    ball_uid = re.sub(r'[^a-z0-9]', '_', ball_name_str.lower())[:20]
    ball_discontinued_warning = False  # se activa si no se encuentra en catálogo activo

    # Si no hay image_url, intentar fetch Python (funciona para bolas en catálogo activo)
    if not ball_img:
        print(f"  🔍 Buscando imagen de '{ball_name_str}' en catálogo...")
        ball_img, ball_page_url = fetch_ball_image_url(ball_name_str, manufacturer=mfr_detected)
        if ball_img:
            print(f"  ✅ Imagen encontrada: {ball_img[:70]}...")
        else:
            print(f"  ⚠️  BOLA DESCATALOGADA: '{ball_name_str}' no encontrada en el catálogo activo del fabricante.")
            print(f"      Solo deben recomendarse bolas actuales de references/current-balls-2026.md")
            ball_discontinued_warning = True

    if ball_img:
        # URL directa conocida → <img> simple con fallback a SVG
        ball_html = (
            f'<img id="ballimg_{ball_uid}" src="{ball_img}" alt="{ball_name_str}" '
            f'style="width:220px;height:220px;object-fit:contain;border-radius:50%;'
            f'box-shadow:0 12px 40px rgba(0,0,0,0.85);display:block;margin:0 auto;" '
            f'onerror="this.style.display=\'none\';document.getElementById(\'ballsvg_{ball_uid}\').style.display=\'block\'"/>'
            f'<div id="ballsvg_{ball_uid}" style="display:none;width:220px;height:220px;margin:0 auto;">{svg_fallback}</div>'
        )
        if not ball_page_url:
            import urllib.parse as _up
            ball_page_url = f"https://www.bowlingball.com/BowlVerts/search/?q={_up.quote(ball_name_str)}"
    else:
        # Sin URL conocida → JS carga candidates en orden; fallback SVG
        candidates = _ball_cdn_candidates(ball_name_str, mfr_detected)
        # Serializar como JSON de URLs
        import json as _json
        cands_json = _json.dumps(candidates[:12])  # máximo 12 intentos
        ball_html = f"""<div id="ballwrap_{ball_uid}" style="width:220px;height:220px;margin:0 auto;">
  <img id="ballimg_{ball_uid}" style="width:220px;height:220px;object-fit:contain;border-radius:50%;box-shadow:0 12px 40px rgba(0,0,0,0.85);display:none;margin:0 auto;" alt="{ball_name_str}"/>
  <div id="ballsvg_{ball_uid}" style="width:220px;height:220px;">{svg_fallback}</div>
</div>
<script>
(function(){{
  var cands={cands_json};
  var img=document.getElementById('ballimg_{ball_uid}');
  var svg=document.getElementById('ballsvg_{ball_uid}');
  var i=0;
  function tryNext(){{
    if(i>=cands.length){{svg.style.display='block';img.style.display='none';return;}}
    img.onerror=function(){{i++;tryNext();}};
    img.onload=function(){{svg.style.display='none';img.style.display='block';}};
    img.src=cands[i];
  }}
  tryNext();
}})();
</script>"""
        if not ball_page_url:
            import urllib.parse as _up
            ball_page_url = f"https://www.bowlingball.com/BowlVerts/search/?q={_up.quote(ball_name_str)}"

    discontinued_banner_html = ""
    if ball_discontinued_warning:
        discontinued_banner_html = (
            f'<div style="background:#2a0000;border:2px solid #ff4444;border-radius:8px;'
            f'padding:8px 12px;margin-bottom:10px;color:#ff9999;font-size:.78em;text-align:center;">'
            f'⚠️ <strong>BOLA DESCATALOGADA</strong> — '
            f'<em>{ball_name_str}</em> no está en el catálogo activo. '
            f'El skill debe recomendar solo bolas de <code>current-balls-2026.md</code>.'
            f'</div>'
        )

    ball_link_html = (
        f'<a href="{ball_page_url}" target="_blank" rel="noopener" '
        f'style="display:inline-block;margin-top:8px;font-size:.72em;color:#c9a227;'
        f'text-decoration:none;border:1px solid #3a2a00;border-radius:12px;'
        f'padding:3px 12px;transition:background .2s;" '
        f'onmouseover="this.style.background=\'#1a1200\'" '
        f'onmouseout="this.style.background=\'transparent\'">'
        f'🔗 Ver bola en bowlingball.com</a>'
    )

    lane = lane_svg(pattern_len, str(pt.get("name","House")),
                    float(lyt.get("foot_board",25)), float(lyt.get("target_board",15)),
                    float(lyt.get("breakpoint_board",7)), float(lyt.get("breakpoint_depth",42)),
                    is_rh, W=150, H=600)
    drill = drill_svg(da_val, ptp_val, val_val, pap_r, pap_u, is_rh, is_asym)

    layout_exp = layout_explain(da_val, ptp_val, val_val, is_asym,
                                  dx.get('friction_need',''), style, b.get('name',''))

    adj_li   = "".join(f"<li>{a}</li>" for a in adj)
    ref_li   = "".join(f"<li>{r}</li>" for r in ref)
    spec_rows= "".join(
        f'<tr><td class="sl">{k}</td><td class="sv">{v}</td></tr>'
        for k,v in [
            ("Cover", b.get("cover","—")),
            ("Core", b.get("core","—")),
            ("Factory finish", b.get("factory_finish","—")),
            ("Superficie rec.", b.get("recommended_surface","—")),
            ("Shape", b.get("shape","—")),
            ("Alternativa", b.get("alternative","—")),
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>🎳 Bowling Report — {b.get('name','')}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#0e1509;color:#e8ddb5;min-height:100vh;padding:14px 10px 48px;}}
h1{{font-size:2em;color:#c9a227;letter-spacing:4px;text-shadow:0 0 30px rgba(201,162,39,.6);font-weight:900;}}
.sub{{color:#7a6a3a;font-size:.82em;margin-top:5px;}}
header{{text-align:center;padding:22px 0 16px;border-bottom:1px solid #1e2a10;margin-bottom:20px;}}
.section-title{{font-size:.7em;text-transform:uppercase;letter-spacing:2px;color:#c9a227;margin-bottom:12px;padding-bottom:5px;border-bottom:1px solid #1e2a10;}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:1100px;margin:0 auto 16px;}}
.grid3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;max-width:1100px;margin:0 auto 16px;}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;max-width:1100px;margin:0 auto 16px;}}
.card{{background:#111d0a;border:1px solid #263318;border-radius:14px;padding:18px;box-shadow:0 6px 22px rgba(0,0,0,.5);}}
.dg{{display:grid;grid-template-columns:1fr 1fr;gap:8px;}}
.di{{background:#0a1206;border-radius:8px;padding:8px;text-align:center;}}
.dl{{font-size:.62em;color:#5a6a3a;text-transform:uppercase;letter-spacing:.5px;}}
.dv{{font-size:1.1em;font-weight:700;margin-top:2px;}}
.dv.r{{color:#cc2200;}} .dv.b{{color:#c9a227;}} .dv.g{{color:#8ab840;}} .dv.o{{color:#c9a227;}} .dv.p{{color:#b58a20;}}
.diag-txt{{margin-top:12px;font-size:.8em;color:#8a7a4a;line-height:1.65;background:#0a1206;border-radius:8px;padding:10px;}}
.badge{{display:inline-block;padding:3px 12px;border-radius:20px;font-size:.7em;font-weight:700;letter-spacing:1px;}}
.badge-red{{background:#9a1800;color:#f5d080;}}
.ball-name{{font-size:1.3em;font-weight:700;color:#c9a227;margin:10px 0 6px;text-align:center;}}
table.specs{{width:100%;border-collapse:collapse;margin-top:8px;}}
.sl{{color:#5a6a3a;font-size:.78em;padding:5px 4px;border-bottom:1px solid #1e2a10;}}
.sv{{color:#d8c888;font-size:.78em;font-weight:500;padding:5px 4px;border-bottom:1px solid #1e2a10;text-align:right;}}
.layout-box{{background:#0a1206;border-radius:10px;padding:14px;text-align:center;margin:12px 0;}}
.lf{{font-size:1.9em;font-weight:700;color:#c9a227;letter-spacing:4px;}}
.lsub{{font-size:.68em;color:#5a6a3a;margin-top:4px;}}
ul.bullets{{list-style:none;padding:0;}}
ul.bullets li{{padding:6px 0 6px 16px;position:relative;border-bottom:1px solid #1a2510;font-size:.8em;line-height:1.5;color:#b0a870;}}
ul.bullets li::before{{content:"▸";position:absolute;left:0;color:#cc2200;font-size:.7em;top:9px;}}
ul.refine li::before{{color:#c9a227;}}
ul.refine li{{color:#c9a227;}}
.svg-center{{display:flex;justify-content:center;}}
.pba-card{{display:flex;align-items:flex-start;gap:12px;}}
.pba-avatar{{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#2a1a00,#c9a227);display:flex;align-items:center;justify-content:center;font-size:1.6em;flex-shrink:0;border:2px solid #c9a227;}}
.pba-name{{font-size:1em;font-weight:700;color:#c9a227;}}
.pba-titles{{font-size:.72em;color:#f39c12;margin-top:2px;}}
.pba-note{{font-size:.75em;color:#8a7a4a;margin-top:4px;line-height:1.5;}}
.gauge-grid{{display:grid;grid-template-columns:1fr 1fr;gap:4px;}}
footer{{text-align:center;margin-top:28px;padding:12px;color:#3a4a20;font-size:.72em;border-top:1px solid #1e2a10;}}
@media(max-width:760px){{.grid2,.grid3,.grid4{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>
<header style="display:flex;align-items:center;gap:24px;padding:18px 24px 16px;border-bottom:1px solid #1e2a10;margin-bottom:20px;max-width:1100px;margin-left:auto;margin-right:auto;">
  {'<img src="' + _logo_b64 + '" alt="LunaBowling" style="height:160px;flex-shrink:0;"/>' if _logo_b64 else '<span style="font-size:3em;">🎳</span>'}
  <div style="flex:1;">
    <div style="font-size:.8em;text-transform:uppercase;letter-spacing:2px;color:#7a6a3a;margin-bottom:8px;">PRO SHOP VIRTUAL &nbsp;·&nbsp; Sistema Dual Angle (Mo Pinel)</div>
    <div style="font-size:2.2em;font-weight:900;color:#c9a227;letter-spacing:2px;line-height:1.1;">{name}</div>
    <div style="margin-top:6px;font-size:.95em;color:#8a7a5a;letter-spacing:.5px;">{hand} &nbsp;·&nbsp; {style.title()} &nbsp;·&nbsp; {now}</div>
  </div>
</header>

<!-- ── ROW 1: Player profile ─────────────────────────────────────────────── -->
<div class="grid3" style="max-width:1100px;margin:0 auto 16px;">

  <!-- Gauges -->
  <div class="card">
    <div class="section-title">📊 Perfil del Jugador</div>
    <div class="gauge-grid">
      <div class="svg-center">{g_speed}</div>
      <div class="svg-center">{g_rev}</div>
      <div class="svg-center">{g_rot}</div>
      <div class="svg-center">{g_tilt}</div>
    </div>
    <div style="margin-top:10px;" class="dg">
      <div class="di"><div class="dl">PAP</div><div class="dv b">{pap_r}" · {'+' if pap_u>=0 else ''}{pap_u}"</div></div>
      <div class="di"><div class="dl">Estilo</div><div class="dv o">{style.title()}</div></div>
      <div class="di"><div class="dl">Mano</div><div class="dv">{hand}</div></div>
      <div class="di"><div class="dl">Fricción</div><div class="dv {'r' if dx.get('friction_need','')=='Alta' else 'g' if dx.get('friction_need','')=='Baja' else 'o'}">{dx.get('friction_need','—')}</div></div>
    </div>
  </div>

  <!-- Radar -->
  <div class="card">
    <div class="section-title">🕸️ Radar vs PBA</div>
    <div style="position:relative;">
      <div class="svg-center">{radar}</div>
      <div class="svg-center" style="margin-top:-6px;">{radar_pba}</div>
      <div style="display:flex;gap:16px;justify-content:center;margin-top:6px;">
        <span style="font-size:.72em;color:#cc2200;">■ {name}</span>
        <span style="font-size:.72em;color:#c9a227;">■ {pba['name'].split()[0]}</span>
      </div>
    </div>
  </div>

  <!-- PBA match + diagnosis -->
  <div class="card">
    <div class="section-title">🏆 Jugador PBA más parecido</div>
    <div class="pba-card">
      <div class="pba-avatar">🎳</div>
      <div>
        <div class="pba-name">{pba['name']}</div>
        <div class="pba-titles">⭐ {pba['titles']} títulos PBA · {pba['style'].title()}</div>
        <div class="pba-note">{pba['note']}</div>
      </div>
    </div>
    <div style="height:12px;"></div>
    <div class="section-title" style="margin-top:8px;">🔍 Diagnóstico</div>
    <div class="dg" style="margin-bottom:8px;">
      <div class="di"><div class="dl">Tipo</div><div class="dv o" style="font-size:.9em;">{dx.get('player_type','—')}</div></div>
      <div class="di"><div class="dl">Patrón</div><div class="dv g" style="font-size:.9em;">{pt.get('name','—')} {pattern_len}ft</div></div>
    </div>
    <div class="diag-txt">{dx.get('summary','')}</div>
  </div>

</div>

<!-- ── ROW 2: Ball + Lane + Drill ────────────────────────────────────────── -->
<div class="grid3" style="max-width:1100px;margin:0 auto 16px;">

  <!-- Ball -->
  <div class="card" style="text-align:center;">
    <div class="section-title">💿 Bola Recomendada</div>
    {discontinued_banner_html}
    {ball_html}
    <div class="ball-name">{b.get('name','—')}</div>
    <div style="margin-bottom:6px;"><span class="badge badge-red">{b.get('category','—')}</span></div>
    {ball_link_html}
    <table class="specs" style="margin-top:10px;">{spec_rows}</table>
  </div>

  <!-- Lane -->
  <div class="card">
    <div class="section-title">🛣️ Línea de Juego</div>
    <div class="svg-center">{lane}</div>
    <div style="margin-top:8px;text-align:center;font-size:.72em;color:#444464;">
      Pies Bd&nbsp;{int(lyt.get('foot_board',25))} &nbsp;·&nbsp;
      Target Bd&nbsp;{int(lyt.get('target_board',15))} &nbsp;·&nbsp;
      Breakpoint Bd&nbsp;{int(lyt.get('breakpoint_board',7))}
    </div>
  </div>

  <!-- Drill -->
  <div class="card">
    <div class="section-title">📐 Layout Dual Angle</div>
    <div class="layout-box">
      <div class="lf">{da_val:.0f}° × {ptp_val}" × {val_val:.0f}°</div>
      <div class="lsub">DA (Dual Angle) &nbsp;·&nbsp; Pin-to-PAP &nbsp;·&nbsp; VAL (Vertical Axis Line)</div>
    </div>

    {layout_exp}
  </div>

</div>

<!-- ── ROW 3: Adjustments ────────────────────────────────────────────────── -->
<div class="grid2" style="max-width:1100px;margin:0 auto;">
  <div class="card">
    <div class="section-title">👣 Ajustes en Pista</div>
    <ul class="bullets">{adj_li}</ul>
  </div>
  <div class="card">
    <div class="section-title">🔬 Para Afinar</div>
    <ul class="bullets refine">{ref_li}</ul>
  </div>
</div>

<footer>🎳 LunaBowling Pro Shop Virtual &nbsp;·&nbsp; Sistema Dual Angle (Mo Pinel) &nbsp;·&nbsp; {now}</footer>
</body>
</html>"""
    return html

# ─────────────────────────────────────────────────────────────────────────────
# EXAMPLE DATA
# ─────────────────────────────────────────────────────────────────────────────
EXAMPLE = {
    "player": {
        "name": "Juan García", "is_right_handed": True, "style": "tweener",
        "speed": 15.5, "rev_rate": 310, "pap_right": 5.0, "pap_up": 0.5,
        "axis_rotation": 48, "axis_tilt": 16,
    },
    "pattern": {"name": "House Shot", "length": 40, "type": "house"},
    "ball": {
        "name": "Storm Phaze II", "category": "Asym Hybrid",
        "cover": "R2X Pearl Reactive", "core": "Velocity (Asym)",
        "factory_finish": "500/1000 SiaAir + Royal Compound + Polish",
        "recommended_surface": "2000 grit Abralon",
        "shape": "Length + strong backend snap",
        "alternative": "Roto Grip UFO Alert (Sym Solid)",
        "is_asym": True, "image_url": "",
    },
    "layout": {
        "da": 55, "pin_to_pap": 4.5, "val": 45,
        "alt_layout": '65° × 5" × 55° (más control)',
        "foot_board": 25, "target_board": 15, "breakpoint_board": 7, "breakpoint_depth": 42,
    },
    "diagnosis": {
        "player_type": "Matched", "friction_need": "Media",
        "summary": ("Tweener equilibrado — 15.5 mph / 310 rpm. "
                    "House 40ft con ratio alto → buena guía lateral. "
                    "Necesidad de fricción media. Asym Hybrid es la categoría ideal."),
    },
    "adjustments": [
        "Si la bola se queda corta: abrir 2–3 tablones a la izquierda manteniendo el target.",
        "Si la bola se pasa: cerrar 1 tablón y mover target 1 tablón a la derecha.",
        "Game 4+: lijar a 3000 grit o pasar a pearl.",
        "Pista muy seca: mover línea completa 5 tablones a la izquierda.",
        "10-pin: plastic ball, tablón 3, línea recta.",
    ],
    "to_refine": [
        "Medir PAP exacto antes de perforar bola Asym (posición MB crítica).",
        "Confirmar axis tilt y rotation con Specto o cámara lenta.",
        "Velocidad exacta a la línea de pines (no solo en monitors).",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Bowling Pro Shop — HTML Report Generator v2")
    ap.add_argument("--data", help="JSON con datos de recomendación")
    ap.add_argument("--output", default="bowling_report.html", help="Archivo HTML de salida")
    ap.add_argument("--example", action="store_true", help="Genera reporte de ejemplo")
    args = ap.parse_args()

    data = EXAMPLE if (args.example or not args.data) else json.load(open(args.data, encoding="utf-8"))
    if args.example or not args.data:
        print("ℹ️  Usando datos de ejemplo.")

    html = generate_html(data)
    out = os.path.abspath(os.path.expanduser(args.output))
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Reporte generado: {out}")
    print(f"   Abrir: file://{out}")

if __name__ == "__main__":
    main()
