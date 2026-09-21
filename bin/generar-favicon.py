#!/usr/bin/env python3
"""Genera el favicon y los iconos del sitio mindtune.cl desde la geometria de la marca.

Fuente de verdad de la geometria: MindTune2027/app_piloto/brand/README.md
    viewBox 96x96 · anillo r=30 centrado en (48,48) · 5 celdas de 72 grados con
    centros en -18/54/126/198/270 · hueco de 20 grados · la celda de 270 es la
    vacia y ahi flota la pieza suelta, a r=38 · trazo 8, remates redondos.

Los arcos se expresan por su CENTRO y no por su inicio (H4.3b): al cambiar el
barrido la marca se acorta hacia adentro y no rota.

Regla de marca (ROADMAP §2.0-bis): la pieza suelta es la senal, presente y
reintegrandose. Nunca generar una variante que la borre, tache o silencie.

Decision del sitio (Hayo, 2026-09-21): el favicon usa la placa OSCURA del
sitio (#0E1620) con la marca casi al borde, porque a 16 px es la unica que
deja leer los cinco segmentos y la pieza suelta. El apple-touch-icon y los PNG
del manifest usan el margen del icono de iOS (0,88), que es lo que necesita la
mascara redondeada del sistema para no verse apretado.

Escribe:
    static/favicon.svg          marca sobre placa oscura, sin metadatos
    static/favicon.ico          16 / 32 / 48
    static/apple-touch-icon.png 180, opaco y sin esquinas redondeadas (iOS enmascara)
    static/icon-192.png         manifest
    static/icon-512.png         manifest

Uso:   python3 bin/generar-favicon.py          (requiere Pillow)
"""
import math
import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Falta Pillow. Instalalo con:  pip3 install pillow")

# --- Paleta (MindTune_Design_System.md §1, direccion A) ---
FONDO = "#0E1620"
ANILLO = "#E6EDF3"
SENAL = "#4CB5A5"

# --- Geometria canonica, en unidades del viewBox de 96 ---
CENTRO = 48.0
RADIO_ANILLO = 30.0
RADIO_SENAL = 38.0
TRAZO = 8.0
CENTROS_CELDA = [-18.0, 54.0, 126.0, 198.0, 270.0]   # grados, 0 = este, horario
CELDA_SUELTA = 4                                     # la de arriba, la vacia
HUECO = 20.0
BARRIDO = 72.0 - HUECO                               # 52 grados
RADIO_ESQUINA = 21.0                                 # rx del appicon, en unidades de 96

SUPERMUESTREO = 8   # se dibuja 8x y se reduce: bordes suaves a 16 px
INSET_PEQUENO = 1.0    # favicon: la marca conserva su margen propio (6/96)
INSET_IOS = 0.88       # bajo la mascara de iOS la marca necesita respirar


def _punto(angulo, radio):
    rad = math.radians(angulo)
    return CENTRO + radio * math.cos(rad), CENTRO + radio * math.sin(rad)


def svg():
    """El favicon como SVG, con la placa oscura y sin metadatos."""
    lineas = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" '
        'role="img" aria-label="MindTune">',
        f'  <rect width="96" height="96" rx="{RADIO_ESQUINA:g}" fill="{FONDO}"/>',
        f'  <g stroke="{ANILLO}" stroke-width="{TRAZO:g}" stroke-linecap="round" fill="none">',
    ]
    for i, c in enumerate(CENTROS_CELDA):
        if i == CELDA_SUELTA:
            continue
        x1, y1 = _punto(c - BARRIDO / 2, RADIO_ANILLO)
        x2, y2 = _punto(c + BARRIDO / 2, RADIO_ANILLO)
        lineas.append(f'    <path d="M{x1:.2f} {y1:.2f} '
                      f'A{RADIO_ANILLO:g} {RADIO_ANILLO:g} 0 0 1 {x2:.2f} {y2:.2f}"/>')
    lineas.append('  </g>')
    x1, y1 = _punto(CENTROS_CELDA[CELDA_SUELTA] - BARRIDO / 2, RADIO_SENAL)
    x2, y2 = _punto(CENTROS_CELDA[CELDA_SUELTA] + BARRIDO / 2, RADIO_SENAL)
    lineas.append(f'  <path d="M{x1:.2f} {y1:.2f} '
                  f'A{RADIO_SENAL:g} {RADIO_SENAL:g} 0 0 1 {x2:.2f} {y2:.2f}" '
                  f'stroke="{SENAL}" stroke-width="{TRAZO:g}" stroke-linecap="round" fill="none"/>')
    lineas.append('</svg>')
    return "\n".join(lineas) + "\n"


def _arco_con_remates(dibujo, centro, radio, inicio, barrido, ancho, color):
    """Arco de trazo centrado en `radio`, con remates redondos.

    Ojo con PIL: `arc(width=w)` crece HACIA ADENTRO desde la caja, o sea el
    borde exterior del trazo queda en el radio de la caja. Para centrar el
    trazo en `radio` hay que pasar una caja de radio `radio + ancho/2`.
    """
    externo = radio + ancho / 2.0
    caja = [centro - externo, centro - externo, centro + externo, centro + externo]
    dibujo.arc(caja, inicio, inicio + barrido, fill=color, width=int(round(ancho)))
    for grados in (inicio, inicio + barrido):
        rad = math.radians(grados)
        x = centro + radio * math.cos(rad)
        y = centro + radio * math.sin(rad)
        r = ancho / 2.0
        dibujo.ellipse([x - r, y - r, x + r, y + r], fill=color)


def dibujar(lado, inset, esquinas_redondas):
    """La marca sobre la placa oscura, como imagen RGBA de `lado` x `lado`."""
    grande = lado * SUPERMUESTREO
    k = grande / 96.0 * inset
    desplazamiento = grande * (1.0 - inset) / 2.0

    if esquinas_redondas:
        img = Image.new("RGBA", (grande, grande), (0, 0, 0, 0))
        mascara = Image.new("L", (grande, grande), 0)
        ImageDraw.Draw(mascara).rounded_rectangle(
            [0, 0, grande - 1, grande - 1],
            radius=int(round(grande * RADIO_ESQUINA / 96.0)), fill=255)
        img.paste(Image.new("RGBA", (grande, grande), FONDO), (0, 0), mascara)
    else:
        # iOS aplica su propia mascara y rechaza PNG con transparencia.
        img = Image.new("RGBA", (grande, grande), FONDO)

    d = ImageDraw.Draw(img)
    centro = CENTRO * k + desplazamiento
    for i, c in enumerate(CENTROS_CELDA):
        if i == CELDA_SUELTA:
            continue
        _arco_con_remates(d, centro, RADIO_ANILLO * k, c - BARRIDO / 2,
                          BARRIDO, TRAZO * k, ANILLO)
    _arco_con_remates(d, centro, RADIO_SENAL * k,
                      CENTROS_CELDA[CELDA_SUELTA] - BARRIDO / 2, BARRIDO,
                      TRAZO * k, SENAL)
    return img.resize((lado, lado), Image.LANCZOS)


def main():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    estatico = os.path.join(raiz, "static")
    if not os.path.isdir(estatico):
        sys.exit(f"No existe {estatico}: corre el script desde el repo del sitio.")

    escritos = []

    ruta = os.path.join(estatico, "favicon.svg")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(svg())
    escritos.append(ruta)

    # .ico: un cuadro por tamano, cada uno dibujado a su medida (mas nitido que
    # reducir uno grande). Pillow guarda el primero y adjunta el resto.
    cuadros = [dibujar(lado, INSET_PEQUENO, True) for lado in (48, 32, 16)]
    ruta = os.path.join(estatico, "favicon.ico")
    cuadros[0].save(ruta, format="ICO", sizes=[(48, 48), (32, 32), (16, 16)],
                    append_images=cuadros[1:])
    escritos.append(ruta)

    for nombre, lado in (("apple-touch-icon.png", 180), ("icon-192.png", 192),
                         ("icon-512.png", 512)):
        ruta = os.path.join(estatico, nombre)
        dibujar(lado, INSET_IOS, False).convert("RGB").save(ruta, optimize=True)
        escritos.append(ruta)

    for r in escritos:
        print(f"  {os.path.relpath(r, raiz):32s} {os.path.getsize(r):7d} bytes")
    print(f"\n{len(escritos)} archivos escritos en static/")


if __name__ == "__main__":
    main()
