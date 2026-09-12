#!/usr/bin/env bash
# Prepara un video de fondo para el dosel de mindtune.cl.
#
#   bin/preparar-video-dosel.sh ~/Downloads/hojas.mp4 [nombre]
#
# Deja en static/video/: <nombre>.mp4 (H.264), <nombre>.webm (VP9) y <nombre>.jpg (póster).
# Después: poner `video_fondo: "<nombre>"` y `video_poster: "/video/<nombre>.jpg"` en hugo.yaml.
# Requiere ffmpeg (brew install ffmpeg).
set -euo pipefail

ORIGEN="${1:?Falta el archivo de origen}"
NOMBRE="${2:-dosel}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DESTINO="$RAIZ/static/video"
mkdir -p "$DESTINO"

# 1600 px de ancho basta: el fondo va oscurecido y desenfocado por el velo.
ESCALA="scale=1600:-2:flags=lanczos"

echo "→ mp4 (H.264)"
ffmpeg -y -i "$ORIGEN" -an -vf "$ESCALA,fps=25" \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 30 -preset slow \
  -movflags +faststart "$DESTINO/$NOMBRE.mp4"

echo "→ webm (VP9)"
ffmpeg -y -i "$ORIGEN" -an -vf "$ESCALA,fps=25" \
  -c:v libvpx-vp9 -crf 38 -b:v 0 -row-mt 1 "$DESTINO/$NOMBRE.webm"

echo "→ póster"
ffmpeg -y -i "$ORIGEN" -vf "$ESCALA,select=eq(n\,0)" -frames:v 1 -q:v 4 "$DESTINO/$NOMBRE.jpg"

echo
ls -lh "$DESTINO"
echo
echo "Si el mp4 pasa de ~4 MB, sube el -crf (32, 34…) o recorta el clip:"
echo "  ffmpeg -y -ss 3 -t 14 -i \"$ORIGEN\" -c copy /tmp/recorte.mp4"
