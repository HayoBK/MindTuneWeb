# Video de fondo del dosel — cómo conseguirlo y cómo instalarlo

El sitio funciona **sin** video: el fondo por defecto es un dosel de hojas dibujado en SVG
(`bin/generar_dosel.py` → `layouts/partials/dosel-capas.html`), que pesa nada y se mueve solo.
Si algún día hay un video, se enchufa y reemplaza a las capas dibujadas, sin tocar plantillas.

---

## 1. De dónde sacar el video

Sí hay material libre; lo que no hay es una descarga automática desde acá (la red de esta
sesión no llega a esos sitios). Son cuatro clics manuales.

| Sitio | Licencia | Qué buscar |
|---|---|---|
| **pexels.com/videos** | Licencia Pexels: uso comercial, sin atribución | `leaves wind`, `tree canopy`, `backlit leaves`, `forest canopy` |
| **pixabay.com/videos** | Licencia de contenido Pixabay: uso comercial, sin atribución | `hojas viento`, `canopy`, `olive tree wind` |
| **mixkit.co/free-stock-video** | Mixkit Free License: uso comercial, sin atribución | `leaves`, `treetop`, `foliage` |
| **coverr.co** | Uso libre, incluido comercial | `nature`, `leaves` |

**La opción más limpia es grabarlo tú.** Un árbol cualquiera un día con brisa, el teléfono en
4K sobre algo firme (no en la mano), 20–30 segundos, contrapicado contra el cielo. Cero
licencia de terceros que explicarle a nadie, y encaja mejor con "esto lo hicimos nosotros".

**Qué sirve para este sitio:** contrapicado contra el cielo o contra luz suave · movimiento
lento (brisa, no viento fuerte) · sin gente, sin logos, sin manos · encuadre estable, sin
paneo · 10–25 segundos · idealmente que el final se parezca al principio, para que el loop no
dé un salto. El fondo va muy oscurecido, así que **un clip claro funciona mejor que uno ya
oscuro**: el velo del sitio lo baja solo.

**Guarda la constancia de la licencia.** Baja la página de la licencia en PDF o anota la URL
del clip y la fecha en `static/video/LICENCIA.txt`. Es de las cosas que Apple y el abogado
pueden preguntar, y cuesta cinco minutos ahora y una tarde después.

---

## 2. Cómo instalarlo

```bash
cd ~/Git_Web/MindTuneWeb
bin/preparar-video-dosel.sh ~/Downloads/el-clip-que-bajaste.mp4 dosel
```

El script deja `static/video/dosel.mp4`, `dosel.webm` y `dosel.jpg` (póster). Después, en
`hugo.yaml`:

```yaml
  video_fondo: "dosel"
  video_poster: "/video/dosel.jpg"
```

Con eso el partial `dosel.html` cambia solo: usa el video y deja de dibujar las capas. Para
volver atrás, `video_fondo: ""`.

**Peso.** Apunta a **menos de 4 MB** el mp4. Si queda más pesado, sube el `-crf` en el script
(30 → 32 → 34) o recorta el clip a 12–15 segundos. Un fondo que tarda en cargar arruina
justamente lo que se buscaba.

**Ojo con lo que ya está resuelto:** el video va `muted`, en loop, `playsinline` (si no, iOS
lo abre en pantalla completa), no se carga con `prefers-reduced-motion`, y la CSP de
`static/_headers` ya trae `media-src 'self'`. No hay que tocar nada de eso.
