#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera layouts/partials/dosel-capas.html — el dosel de hojas del fondo (v2, 2026-09-12).

Tres capas de ramas con hojas, dibujadas como SVG estático. La capa lejana va borrosa y
quieta (no repinta); las dos cercanas solo rotan unos grados alrededor de su nacimiento,
con periodos primos entre sí para que el viento no se sienta cíclico.
Determinista: misma semilla, mismo archivo. Volver a correr solo si se cambia la geometría.
"""
import math, random, pathlib

W, H = 1600, 900
SALIDA = pathlib.Path(__file__).resolve().parent.parent / "layouts/partials/dosel-capas.html"

def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    return x, y

def tangente(p0, p1, p2, p3, t):
    u = 1 - t
    x = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    y = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return math.degrees(math.atan2(y, x))

def rama(rnd, ax, ay, direccion, largo, n_hojas, escala, borde="arriba"):
    """Devuelve (d_del_tallo, [(x, y, angulo, escala)]) para una rama."""
    if borde == "arriba":
        p0 = (ax, ay)
        p3 = (ax + direccion*largo*rnd.uniform(0.55, 0.9), ay + largo*rnd.uniform(0.75, 1.0))
        p1 = (ax + direccion*largo*rnd.uniform(0.05, 0.22), ay + largo*rnd.uniform(0.3, 0.45))
        p2 = (ax + direccion*largo*rnd.uniform(0.35, 0.65), ay + largo*rnd.uniform(0.65, 0.85))
    else:  # nace de un costado
        p0 = (ax, ay)
        p3 = (ax + direccion*largo*rnd.uniform(0.8, 1.05), ay + largo*rnd.uniform(0.15, 0.4))
        p1 = (ax + direccion*largo*rnd.uniform(0.25, 0.4), ay - largo*rnd.uniform(0.02, 0.12))
        p2 = (ax + direccion*largo*rnd.uniform(0.6, 0.8), ay + largo*rnd.uniform(0.05, 0.25))

    d = "M%.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f" % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])

    hojas = []
    for i in range(n_hojas):
        t = 0.10 + 0.90 * (i + rnd.uniform(-0.25, 0.25)) / max(1, n_hojas - 1)
        t = min(1.0, max(0.06, t))
        bx, by = bezier(p0, p1, p2, p3, t)
        ang = tangente(p0, p1, p2, p3, t)
        lado = 1 if i % 2 == 0 else -1
        sep = rnd.uniform(4, 26) * lado
        nx, ny = math.cos(math.radians(ang + 90)) * sep, math.sin(math.radians(ang + 90)) * sep
        # la hoja se abre hacia afuera del tallo, con harto azar para que no se vea peinada
        gh = ang + lado * rnd.uniform(24, 74) + rnd.uniform(-14, 14)
        eh = escala * rnd.uniform(0.62, 1.28) * (0.72 + 0.42 * t)
        hojas.append((bx + nx, by + ny, gh, eh))
    return d, hojas

def capa(nombre, semilla, ramas_spec, escala, grosor):
    rnd = random.Random(semilla)
    piezas = []
    for (ax, ay, direccion, largo, n, borde) in ramas_spec:
        d, hojas = rama(rnd, ax, ay, direccion, largo, n, escala, borde)
        usos = "".join(
            '<use href="#mt-hoja" transform="translate(%.0f %.0f) rotate(%.0f) scale(%.2f)"/>' % h
            for h in hojas)
        giro = round(rnd.uniform(0.55, 1.45), 2)
        dur = round(rnd.uniform(8.5, 15.5), 1)
        retardo = round(-rnd.uniform(0, 14), 1)
        piezas.append(
            '<g class="mt-rama" style="transform-origin:%.0fpx %.0fpx;--giro:%sdeg;'
            'animation-duration:%ss;animation-delay:%ss">'
            '<path class="mt-tallo" d="%s" stroke-width="%s"/>%s</g>'
            % (ax, ay, giro, dur, retardo, d, grosor, usos))
    return '<g class="mt-capa mt-capa--%s">%s</g>' % (nombre, "".join(piezas))

# --- Geometría: el dosel enmarca arriba y por los costados; el centro queda despejado ---
lejos = [(70, -30, 1, 300, 22, "arriba"), (210, -40, -1, 260, 20, "arriba"),
         (380, -30, 1, 320, 24, "arriba"), (540, -45, -1, 280, 21, "arriba"),
         (700, -30, 1, 300, 22, "arriba"), (880, -40, -1, 310, 23, "arriba"),
         (1040, -30, 1, 270, 20, "arriba"), (1200, -45, -1, 320, 24, "arriba"),
         (1360, -30, 1, 290, 21, "arriba"), (1540, -40, -1, 300, 22, "arriba")]
medio = [(120, -50, 1, 400, 26, "arriba"), (450, -60, -1, 360, 24, "arriba"),
         (760, -50, 1, 330, 22, "arriba"), (1120, -55, -1, 390, 26, "arriba"),
         (1480, -50, 1, 370, 25, "arriba"), (-40, 150, 1, 330, 20, "lado"),
         (1640, 190, -1, 350, 21, "lado")]
cerca = [(-20, -70, 1, 520, 28, "arriba"), (330, -80, -1, 430, 25, "arriba"),
         (880, -75, 1, 470, 26, "arriba"), (1300, -70, -1, 440, 25, "arriba"),
         (1660, -80, 1, 500, 27, "arriba")]

capas = "\n  ".join([
    capa("lejos", 20260912, lejos, 3.1, 1.4),
    capa("medio", 7761, medio, 4.1, 2.0),
    capa("cerca", 44917, cerca, 5.6, 2.8),
])

svg = f'''{{{{- /* GENERADO por bin/generar_dosel.py — no editar a mano. Dosel de hojas del fondo (v2). */ -}}}}
<svg class="mt-dosel__hojas" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false">
  <defs>
    <path id="mt-hoja" d="M0 0 C 3.6 -3.0, 9.4 -3.4, 12.6 0 C 9.4 3.4, 3.6 3.0, 0 0 Z"/>
  </defs>
  {capas}
</svg>
'''

SALIDA.write_text(svg, encoding="utf-8")
print("escrito %s (%.1f KB)" % (SALIDA, SALIDA.stat().st_size / 1024))
