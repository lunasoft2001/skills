#!/usr/bin/env python3
"""
Bowling Pro Shop — Visual Report Generator
Generates a dark-themed HTML report with:
  - Player & pattern diagnosis card
  - Ball recommendation card with image
  - SVG lane diagram (top-down) with oil pattern + playing line
  - SVG drill diagram (top-down) with Dual Angle layout
  - Adjustments and refinement notes

Usage:
  python generate_bowling_report.py --data recommendation.json --output ~/Desktop/report.html
  python generate_bowling_report.py --example   # generates a sample report

Input JSON keys: player, pattern, ball, layout, diagnosis, adjustments, to_refine
See scripts/example_data.json for a full example.
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime


# ──────────────────────────────────────────────────────────────────────────────
# LANE SVG
# ──────────────────────────────────────────────────────────────────────────────

def generate_lane_svg(
    pattern_length: int = 40,
    pattern_name: str = "House Shot",
    foot_board: float = 25,
    target_board: float = 15,
    breakpoint_board: float = 7,
    breakpoint_depth: float = 40,
    is_right_handed: bool = True,
) -> str:
    W, H = 310, 510
    GUTTER = 12

    def bx(b: float) -> float:
        """Board number to SVG x. For RH: board 1 = right edge."""
        inner = W - 2 * GUTTER
        if is_right_handed:
            return GUTTER + inner - (b / 41.0) * inner
        else:
            return GUTTER + (b / 41.0) * inner

    def fy(feet: float) -> float:
        """Feet from foul line to SVG y (foul line near bottom)."""
        usable = H - 30  # 30px margin at top for pins
        return H - 15 - (feet / 62.0) * usable

    foul_y = fy(0)
    pins_y = fy(60)
    dots_y = fy(7)
    arrows_y = fy(15)
    oil_end_y = fy(pattern_length)

    pocket_board = 17 if is_right_handed else 23

    x0, y0 = bx(foot_board), foul_y + 8
    x1, y1 = bx(target_board), arrows_y
    x2, y2 = bx(breakpoint_board), fy(breakpoint_depth)
    x3, y3 = bx(pocket_board), pins_y

    # Bezier control points
    cx1 = bx(target_board * 0.75 + foot_board * 0.25)
    cy1 = fy(7)
    cx2 = bx((breakpoint_board + target_board) * 0.45)
    cy2 = fy(breakpoint_depth * 0.55)

    svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="display:block;">\n'

    # Lane background
    svg += f'<rect width="{W}" height="{H}" fill="#2a1f0e" rx="6"/>\n'

    # Oil zone (shaded)
    svg += (
        f'<rect x="{GUTTER}" y="{oil_end_y:.1f}" width="{W - 2*GUTTER}" '
        f'height="{foul_y - oil_end_y:.1f}" fill="#1a5276" fill-opacity="0.55"/>\n'
    )

    # Gutters
    svg += f'<rect x="0" y="0" width="{GUTTER}" height="{H}" fill="#5d4037" rx="6"/>\n'
    svg += f'<rect x="{W - GUTTER}" y="0" width="{GUTTER}" height="{H}" fill="#5d4037" rx="6"/>\n'
    svg += f'<line x1="{GUTTER}" y1="0" x2="{GUTTER}" y2="{H}" stroke="#795548" stroke-width="1"/>\n'
    svg += f'<line x1="{W - GUTTER}" y1="0" x2="{W - GUTTER}" y2="{H}" stroke="#795548" stroke-width="1"/>\n'

    # Board reference lines
    for b in range(5, 41, 5):
        x = bx(b)
        svg += f'<line x1="{x:.1f}" y1="{pins_y:.1f}" x2="{x:.1f}" y2="{foul_y:.1f}" stroke="#5d4037" stroke-width="0.7" stroke-dasharray="3,5"/>\n'
        svg += f'<text x="{x:.1f}" y="{foul_y + 12:.1f}" text-anchor="middle" font-size="7" fill="#7a5c3a" font-family="Arial">{b}</text>\n'

    # 7-dot markers
    for b in [3, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37, 39]:
        if 1 <= b <= 40:
            svg += f'<circle cx="{bx(b):.1f}" cy="{dots_y:.1f}" r="2.5" fill="#8d6e45"/>\n'

    # Arrow markers (≈ chevrons at 15ft)
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax = bx(b)
        svg += f'<polygon points="{ax:.1f},{arrows_y + 7:.1f} {ax - 4:.1f},{arrows_y - 3:.1f} {ax + 4:.1f},{arrows_y - 3:.1f}" fill="#8d6e45"/>\n'

    # Oil end dashed line
    svg += (
        f'<line x1="{GUTTER}" y1="{oil_end_y:.1f}" x2="{W - GUTTER}" y2="{oil_end_y:.1f}" '
        f'stroke="#3498db" stroke-width="1.5" stroke-dasharray="5,3"/>\n'
    )
    svg += (
        f'<text x="{W - GUTTER - 3:.1f}" y="{oil_end_y - 4:.1f}" text-anchor="end" '
        f'font-size="8" fill="#3498db" font-family="Arial">{pattern_length}ft · {pattern_name}</text>\n'
    )

    # Foul line
    svg += f'<line x1="{GUTTER}" y1="{foul_y:.1f}" x2="{W - GUTTER}" y2="{foul_y:.1f}" stroke="#e0e0e0" stroke-width="2"/>\n'

    # Pins (3-6-10 triangle, simplified)
    pin_layout = [
        (20, 0), (17.5, 1), (22.5, 1),
        (15, 2), (20, 2), (25, 2),
        (12.5, 3), (17.5, 3), (22.5, 3), (27.5, 3),
    ]
    for pb, prow in pin_layout:
        px = bx(pb)
        py = pins_y + prow * 7
        svg += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#e0e0e0" stroke="#aaa" stroke-width="1"/>\n'

    # Playing line shadow
    svg += (
        f'<path d="M {x0:.1f},{y0:.1f} C {cx1:.1f},{cy1:.1f} {cx2:.1f},{cy2:.1f} '
        f'{x2:.1f},{y2:.1f} S {(x2 + x3) / 2:.1f},{(y2 + y3) / 2:.1f} {x3:.1f},{y3:.1f}" '
        f'fill="none" stroke="#e74c3c" stroke-width="5" stroke-opacity="0.2" stroke-linecap="round"/>\n'
    )
    # Playing line
    svg += (
        f'<path d="M {x0:.1f},{y0:.1f} C {cx1:.1f},{cy1:.1f} {cx2:.1f},{cy2:.1f} '
        f'{x2:.1f},{y2:.1f} S {(x2 + x3) / 2:.1f},{(y2 + y3) / 2:.1f} {x3:.1f},{y3:.1f}" '
        f'fill="none" stroke="#e74c3c" stroke-width="2.5" stroke-linecap="round"/>\n'
    )

    # Markers
    # Foot position
    svg += f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="6" fill="#e74c3c"/>\n'
    svg += f'<text x="{x0 + 9:.1f}" y="{y0 + 4:.1f}" font-size="9" fill="#e74c3c" font-family="Arial" font-weight="bold">Bd{int(foot_board)}</text>\n'

    # Target
    svg += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="5" fill="none" stroke="#e74c3c" stroke-width="2"/>\n'
    svg += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="2" fill="#e74c3c"/>\n'
    svg += f'<text x="{x1 + 8:.1f}" y="{y1 + 4:.1f}" font-size="9" fill="#e74c3c" font-family="Arial">▶Bd{int(target_board)}</text>\n'

    # Breakpoint
    svg += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="5" fill="#f39c12" fill-opacity="0.85"/>\n'
    svg += f'<text x="{x2 + 8:.1f}" y="{y2 + 4:.1f}" font-size="8" fill="#f39c12" font-family="Arial">BP·Bd{int(breakpoint_board)}</text>\n'

    # Pocket arrow
    svg += f'<polygon points="{x3:.1f},{y3:.1f} {x3 - 5:.1f},{y3 - 11:.1f} {x3 + 5:.1f},{y3 - 11:.1f}" fill="#e74c3c"/>\n'

    # Handedness label
    hand_label = "→ Diestro" if is_right_handed else "← Zurdo"
    svg += f'<text x="{W // 2}" y="14" text-anchor="middle" font-size="10" fill="#aaa" font-family="Arial">{hand_label}</text>\n'

    svg += '</svg>'
    return svg


# ──────────────────────────────────────────────────────────────────────────────
# DRILL DIAGRAM SVG
# ──────────────────────────────────────────────────────────────────────────────

def generate_drill_svg(
    da: float = 55,
    pin_to_pap: float = 4.5,
    val: float = 45,
    pap_right: float = 5.0,
    pap_up: float = 0.5,
    is_right_handed: bool = True,
    is_asym: bool = False,
) -> str:
    W, H = 300, 310
    cx, cy = 150, 155
    R = 118

    scale = (2 * R) / 8.5  # px per inch
    sign = 1 if is_right_handed else -1

    # PAP position
    pap_x = cx + sign * pap_right * scale
    pap_y = cy - pap_up * scale

    # Pin position (VAL angle from horizontal VAL line, above it)
    val_rad = math.radians(val)
    pin_dx = math.cos(val_rad) * (-sign)  # toward center for RH
    pin_dy = -abs(math.sin(val_rad))       # upward in SVG

    pin_x = pap_x + pin_dx * pin_to_pap * scale
    pin_y = pap_y + pin_dy * pin_to_pap * scale

    # Keep pin inside ball
    dist = math.sqrt((pin_x - cx) ** 2 + (pin_y - cy) ** 2)
    if dist > R - 10:
        f = (R - 10) / dist
        pin_x = cx + (pin_x - cx) * f
        pin_y = cy + (pin_y - cy) * f

    # Grip area (below center for RH)
    grip_cx = cx + sign * 0.8 * scale
    grip_cy = cy + 2.0 * scale

    # Thumb direction from DA
    da_rad = math.radians(da)
    thumb_dx = math.sin(da_rad) * sign
    thumb_dy = math.cos(da_rad)
    span = 4.1 * scale

    mf_x = grip_cx - sign * 0.35 * scale
    mf_y = grip_cy - 1.3 * scale
    rf_x = grip_cx + sign * 0.35 * scale
    rf_y = grip_cy - 1.1 * scale
    th_x = grip_cx + thumb_dx * span
    th_y = grip_cy + thumb_dy * span

    # VAL line
    val_x1 = pap_x - R * 0.85
    val_x2 = pap_x + R * 0.85
    val_y_line = pap_y

    # Mass Bias (asym only)
    mb_angle = val_rad + math.pi / 2
    mb_dist = 2.2 * scale
    mb_x = pin_x + math.cos(mb_angle) * mb_dist * sign
    mb_y = pin_y + math.sin(mb_angle) * mb_dist
    if math.sqrt((mb_x - cx) ** 2 + (mb_y - cy) ** 2) > R * 0.88:
        mb_x = pin_x - math.cos(mb_angle) * mb_dist * sign
        mb_y = pin_y - math.sin(mb_angle) * mb_dist

    svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="display:block;">\n'

    # Ball body
    svg += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#12122a" stroke="#2c3e50" stroke-width="2"/>\n'
    # Shine
    svg += f'<ellipse cx="{cx - 32}" cy="{cy - 32}" rx="22" ry="15" fill="white" fill-opacity="0.07"/>\n'

    # VAL line
    svg += (
        f'<line x1="{val_x1:.1f}" y1="{val_y_line:.1f}" x2="{val_x2:.1f}" y2="{val_y_line:.1f}" '
        f'stroke="#3498db" stroke-width="1.5" stroke-dasharray="6,3"/>\n'
    )
    svg += f'<text x="{val_x1 - 3:.1f}" y="{val_y_line - 5:.1f}" font-size="9" fill="#3498db" font-family="Arial" font-weight="bold" text-anchor="end">VAL</text>\n'

    # Pin–PAP line
    svg += (
        f'<line x1="{pap_x:.1f}" y1="{pap_y:.1f}" x2="{pin_x:.1f}" y2="{pin_y:.1f}" '
        f'stroke="#f39c12" stroke-width="1.5" stroke-dasharray="4,2"/>\n'
    )

    # PAP
    svg += f'<circle cx="{pap_x:.1f}" cy="{pap_y:.1f}" r="7" fill="#3498db" stroke="white" stroke-width="1.5"/>\n'
    svg += f'<text x="{pap_x + 11:.1f}" y="{pap_y - 9:.1f}" font-size="9" fill="#3498db" font-family="Arial" font-weight="bold">PAP</text>\n'

    # Pin
    svg += f'<circle cx="{pin_x:.1f}" cy="{pin_y:.1f}" r="8" fill="#f39c12" stroke="white" stroke-width="1.5"/>\n'
    svg += f'<text x="{pin_x:.1f}" y="{pin_y + 4:.1f}" font-size="8" fill="white" font-family="Arial" font-weight="bold" text-anchor="middle">PIN</text>\n'

    # Finger holes
    svg += f'<ellipse cx="{mf_x:.1f}" cy="{mf_y:.1f}" rx="9" ry="9" fill="#555" stroke="#888" stroke-width="1.5"/>\n'
    svg += f'<text x="{mf_x:.1f}" y="{mf_y + 4:.1f}" font-size="7" fill="#ddd" font-family="Arial" text-anchor="middle">M</text>\n'

    svg += f'<ellipse cx="{rf_x:.1f}" cy="{rf_y:.1f}" rx="9" ry="9" fill="#555" stroke="#888" stroke-width="1.5"/>\n'
    svg += f'<text x="{rf_x:.1f}" y="{rf_y + 4:.1f}" font-size="7" fill="#ddd" font-family="Arial" text-anchor="middle">R</text>\n'

    # Thumb
    svg += f'<ellipse cx="{th_x:.1f}" cy="{th_y:.1f}" rx="11" ry="11" fill="#444" stroke="#888" stroke-width="1.5"/>\n'
    svg += f'<text x="{th_x:.1f}" y="{th_y + 4:.1f}" font-size="7" fill="#ddd" font-family="Arial" text-anchor="middle">T</text>\n'

    # Mass Bias (asym)
    if is_asym:
        svg += (
            f'<polygon points="{mb_x:.1f},{mb_y - 8:.1f} {mb_x - 6:.1f},{mb_y + 5:.1f} '
            f'{mb_x + 6:.1f},{mb_y + 5:.1f}" fill="#e74c3c" stroke="white" stroke-width="1"/>\n'
        )
        svg += f'<text x="{mb_x:.1f}" y="{mb_y + 18:.1f}" font-size="8" fill="#e74c3c" font-family="Arial" font-weight="bold" text-anchor="middle">MB</text>\n'

    # Layout annotation
    svg += (
        f'<text x="{cx}" y="{H - 7}" font-size="10" fill="#7f8c8d" font-family="Arial" '
        f'text-anchor="middle" font-style="italic">'
        f'{da:.0f}° × {pin_to_pap}" × {val:.0f}°</text>\n'
    )
    svg += f'<text x="8" y="15" font-size="8" fill="#555" font-family="Arial">Vista superior</text>\n'

    svg += '</svg>'
    return svg


# ──────────────────────────────────────────────────────────────────────────────
# HTML REPORT
# ──────────────────────────────────────────────────────────────────────────────

def generate_html_report(data: dict) -> str:
    player = data.get("player", {})
    pattern = data.get("pattern", {})
    ball = data.get("ball", {})
    layout = data.get("layout", {})
    adjustments = data.get("adjustments", [])
    to_refine = data.get("to_refine", [])
    diagnosis = data.get("diagnosis", {})

    lane_svg = generate_lane_svg(
        pattern_length=int(pattern.get("length", 40)),
        pattern_name=str(pattern.get("name", "House Shot")),
        foot_board=float(layout.get("foot_board", 25)),
        target_board=float(layout.get("target_board", 15)),
        breakpoint_board=float(layout.get("breakpoint_board", 7)),
        breakpoint_depth=float(layout.get("breakpoint_depth", 40)),
        is_right_handed=bool(player.get("is_right_handed", True)),
    )

    drill_svg = generate_drill_svg(
        da=float(layout.get("da", 55)),
        pin_to_pap=float(layout.get("pin_to_pap", 4.5)),
        val=float(layout.get("val", 45)),
        pap_right=float(player.get("pap_right", 5.0)),
        pap_up=float(player.get("pap_up", 0.5)),
        is_right_handed=bool(player.get("is_right_handed", True)),
        is_asym=bool(ball.get("is_asym", False)),
    )

    img_url = ball.get("image_url", "")
    if img_url:
        ball_img_html = (
            f'<img src="{img_url}" alt="{ball.get("name","")}" '
            f'style="width:160px;height:160px;object-fit:contain;border-radius:50%;'
            f'box-shadow:0 4px 24px rgba(0,0,0,0.6);"/>'
        )
    else:
        initial = (ball.get("name", "?")[0] if ball.get("name") else "?").upper()
        ball_img_html = (
            f'<div style="width:160px;height:160px;border-radius:50%;'
            f'background:radial-gradient(circle at 35% 35%,#444,#0d0d1a);'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:48px;color:#555;margin:0 auto;">{initial}</div>'
        )

    adj_items = "".join(f"<li>{a}</li>" for a in adjustments)
    refine_items = "".join(f"<li>{r}</li>" for r in to_refine)

    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    player_name = player.get("name", "Jugador")
    hand = "Diestro" if player.get("is_right_handed", True) else "Zurdo"
    style = player.get("style", "").capitalize()
    speed = player.get("speed", "—")
    rev = player.get("rev_rate", "—")

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>🎳 Bowling Report — {ball.get('name','')}</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0;}}
    body{{font-family:'Segoe UI',Arial,sans-serif;background:#0a0a18;color:#dde;min-height:100vh;padding:16px 12px 40px;}}
    h1{{font-size:1.8em;color:#e74c3c;letter-spacing:2px;text-shadow:0 0 20px rgba(231,76,60,.4);}}
    .subtitle{{color:#7f8c8d;font-size:.85em;margin-top:4px;}}
    header{{text-align:center;padding:24px 0 18px;border-bottom:2px solid #1c2a3a;margin-bottom:22px;}}
    .grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:1080px;margin:0 auto;}}
    .grid3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;max-width:1080px;margin:18px auto 0;}}
    .card{{background:#12122a;border:1px solid #1c2a3a;border-radius:12px;padding:18px;box-shadow:0 4px 18px rgba(0,0,0,.35);}}
    .card h2{{color:#3498db;font-size:.8em;text-transform:uppercase;letter-spacing:1px;margin-bottom:13px;padding-bottom:6px;border-bottom:1px solid #1c2a3a;}}
    .card h2 .ic{{margin-right:5px;}}
    .dg{{display:grid;grid-template-columns:1fr 1fr;gap:8px;}}
    .di{{background:#0d1a2e;border-radius:8px;padding:9px;text-align:center;}}
    .dl{{font-size:.65em;color:#7f8c8d;text-transform:uppercase;letter-spacing:.5px;}}
    .dv{{font-size:1.05em;font-weight:700;margin-top:2px;}}
    .dv.r{{color:#e74c3c;}} .dv.b{{color:#3498db;}} .dv.g{{color:#2ecc71;}} .dv.o{{color:#f39c12;}}
    .diag-summary{{margin-top:13px;padding:10px;background:#0d1a2e;border-radius:8px;font-size:.82em;color:#95a5a6;line-height:1.6;}}
    .ball-card{{text-align:center;}}
    .ball-name{{font-size:1.25em;font-weight:700;color:#e74c3c;margin:10px 0 4px;}}
    .badge{{display:inline-block;background:#e74c3c;color:#fff;padding:2px 10px;border-radius:20px;font-size:.72em;margin-bottom:10px;}}
    .spec{{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1c2a3a;font-size:.82em;}}
    .sl{{color:#7f8c8d;}} .sv{{color:#dde;font-weight:500;}}
    .layout-box{{background:#0d1a2e;border-radius:10px;padding:14px;text-align:center;margin:10px 0;}}
    .lf{{font-size:1.75em;font-weight:700;color:#f39c12;letter-spacing:3px;}}
    .la{{font-size:.85em;color:#7f8c8d;margin-top:6px;}}
    ul.adj{{list-style:none;padding:0;}}
    ul.adj li{{padding:6px 0 6px 18px;position:relative;border-bottom:1px solid #1c2a3a;font-size:.83em;line-height:1.4;}}
    ul.adj li::before{{content:"▶";position:absolute;left:0;color:#e74c3c;font-size:.65em;top:9px;}}
    ul.ref li::before{{color:#f39c12;}}
    ul.ref li{{color:#f39c12;}}
    .svg-wrap{{display:flex;justify-content:center;}}
    footer{{text-align:center;margin-top:28px;padding:12px;color:#3a3a5a;font-size:.75em;border-top:1px solid #1c2a3a;}}
    @media(max-width:720px){{.grid2,.grid3{{grid-template-columns:1fr;}}}}
  </style>
</head>
<body>
<header>
  <h1>🎳 Bowling Pro Shop</h1>
  <div class="subtitle">
    {player_name} &nbsp;·&nbsp; {hand} &nbsp;·&nbsp; {style}
    &nbsp;·&nbsp; {speed} mph &nbsp;·&nbsp; {rev} rpm
    &nbsp;·&nbsp; {date_str}
  </div>
</header>

<!-- ROW 1 -->
<div class="grid2">
  <!-- Diagnosis -->
  <div class="card">
    <h2><span class="ic">🔍</span>Diagnóstico</h2>
    <div class="dg">
      <div class="di"><div class="dl">Jugador</div><div class="dv o">{diagnosis.get('player_type','—')}</div></div>
      <div class="di"><div class="dl">Fricción necesaria</div><div class="dv b">{diagnosis.get('friction_need','—')}</div></div>
      <div class="di"><div class="dl">Velocidad</div><div class="dv">{speed} mph</div></div>
      <div class="di"><div class="dl">Rev Rate</div><div class="dv">{rev} rpm</div></div>
      <div class="di"><div class="dl">Patrón</div><div class="dv g">{pattern.get('name','—')}</div></div>
      <div class="di"><div class="dl">Longitud</div><div class="dv g">{pattern.get('length','—')} ft</div></div>
    </div>
    <div class="diag-summary">{diagnosis.get('summary','')}</div>
  </div>

  <!-- Ball -->
  <div class="card ball-card">
    <h2><span class="ic">💿</span>Bola Recomendada</h2>
    {ball_img_html}
    <div class="ball-name">{ball.get('name','—')}</div>
    <div class="badge">{ball.get('category','—')}</div>
    <div>
      <div class="spec"><span class="sl">Cover</span><span class="sv">{ball.get('cover','—')}</span></div>
      <div class="spec"><span class="sl">Core</span><span class="sv">{ball.get('core','—')}</span></div>
      <div class="spec"><span class="sl">Acabado fábrica</span><span class="sv">{ball.get('factory_finish','—')}</span></div>
      <div class="spec"><span class="sl">Superficie rec.</span><span class="sv" style="color:#e74c3c">{ball.get('recommended_surface','—')}</span></div>
      <div class="spec"><span class="sl">Shape</span><span class="sv">{ball.get('shape','—')}</span></div>
      <div class="spec" style="border:none"><span class="sl">Alternativa</span><span class="sv" style="color:#7f8c8d">{ball.get('alternative','—')}</span></div>
    </div>
  </div>
</div>

<!-- ROW 2 -->
<div class="grid3">
  <!-- Lane diagram -->
  <div class="card">
    <h2><span class="ic">🛣️</span>Línea de Juego</h2>
    <div class="svg-wrap">{lane_svg}</div>
    <div style="margin-top:8px;font-size:.75em;color:#7f8c8d;text-align:center;">
      Pies&nbsp;Bd&nbsp;{layout.get('foot_board','—')} &nbsp;·&nbsp;
      Target&nbsp;Bd&nbsp;{layout.get('target_board','—')} &nbsp;·&nbsp;
      BP&nbsp;Bd&nbsp;{layout.get('breakpoint_board','—')}
    </div>
  </div>

  <!-- Drill diagram -->
  <div class="card">
    <h2><span class="ic">📐</span>Layout Dual Angle</h2>
    <div class="layout-box">
      <div class="lf">{layout.get('da','—')}° × {layout.get('pin_to_pap','—')}" × {layout.get('val','—')}°</div>
      <div style="font-size:.7em;color:#7f8c8d;margin-top:4px;">DA × Pin-to-PAP × VAL</div>
    </div>
    <div class="svg-wrap">{drill_svg}</div>
    <div style="margin-top:6px;font-size:.75em;color:#7f8c8d;text-align:center;">
      Alt: {layout.get('alt_layout','—')}
    </div>
  </div>

  <!-- Adjustments -->
  <div class="card">
    <h2><span class="ic">👣</span>Ajustes en Pista</h2>
    <ul class="adj">{adj_items}</ul>
    <h2 style="margin-top:18px;"><span class="ic">🔬</span>Para Afinar</h2>
    <ul class="adj ref">{refine_items}</ul>
  </div>
</div>

<footer>
  🎳 Bowling Pro Shop Virtual &nbsp;·&nbsp;
  Layout: sistema Dual Angle (Mo Pinel) &nbsp;·&nbsp;
  {date_str}
</footer>
</body>
</html>"""
    return html


# ──────────────────────────────────────────────────────────────────────────────
# EXAMPLE DATA
# ──────────────────────────────────────────────────────────────────────────────

EXAMPLE_DATA = {
    "player": {
        "name": "Juan García",
        "is_right_handed": True,
        "style": "tweener",
        "speed": 15.5,
        "rev_rate": 310,
        "pap_right": 5.0,
        "pap_up": 0.5,
    },
    "pattern": {
        "name": "House Shot",
        "length": 40,
        "type": "house",
    },
    "ball": {
        "name": "Storm Phaze II",
        "category": "Asym Hybrid",
        "cover": "R2X Pearl Reactive",
        "core": "Velocity (Asym)",
        "factory_finish": "500/1000 SiaAir + Royal Compound + Polish",
        "recommended_surface": "2000 grit Abralon",
        "shape": "Length + strong backend snap",
        "alternative": "Roto Grip UFO Alert (Sym Solid)",
        "is_asym": True,
        "image_url": "",
    },
    "layout": {
        "da": 55,
        "pin_to_pap": 4.5,
        "val": 45,
        "alt_layout": '65° × 5" × 55° (más control)',
        "foot_board": 25,
        "target_board": 15,
        "breakpoint_board": 7,
        "breakpoint_depth": 42,
    },
    "diagnosis": {
        "player_type": "Matched",
        "friction_need": "Media",
        "summary": (
            "Jugador tweener con velocidad y rev rate equilibrados (15.5 mph / 310 rpm). "
            "Patrón house 40ft con ratio alto → buena guía lateral. "
            "Necesidad de fricción media — un Asym Hybrid funciona bien."
        ),
    },
    "adjustments": [
        "Si la bola se queda corta: abrir 2–3 tablones a la izquierda manteniendo el target.",
        "Si la bola se pasa: cerrar 1 tablón y mover target 1 tablón a la derecha.",
        "Game 4+: cambiar superficie a 3000 grit o pasar a pearl.",
        "Pista muy seca: mover línea completa 5 tablones a la izquierda.",
        "10-pin: plastic ball desde el lado izquierdo, recto al tablón 3.",
    ],
    "to_refine": [
        "Medir PAP exacto (especialmente para bolas Asym y posición del MB).",
        "Conocer axis tilt y rotation para ajustar pin-to-PAP con precisión.",
        "Velocidad exacta en la zona de los pines (no solo en los monitores).",
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bowling Pro Shop — Generador de reporte visual HTML"
    )
    parser.add_argument("--data", help="Ruta al JSON con los datos de la recomendación")
    parser.add_argument(
        "--output", default="bowling_report.html", help="Archivo HTML de salida"
    )
    parser.add_argument(
        "--example", action="store_true", help="Genera un reporte de ejemplo"
    )
    args = parser.parse_args()

    if args.example or not args.data:
        data = EXAMPLE_DATA
        print("ℹ️  Usando datos de ejemplo (--example o sin --data).")
    else:
        with open(args.data, "r", encoding="utf-8") as fh:
            data = json.load(fh)

    html = generate_html_report(data)

    output_path = os.path.expanduser(args.output)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    abs_path = os.path.abspath(output_path)
    print(f"✅ Reporte generado: {abs_path}")
    print(f"   Abre en el navegador: file://{abs_path}")


if __name__ == "__main__":
    main()
