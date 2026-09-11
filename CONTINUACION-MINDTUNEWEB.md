# CONTINUACIÓN — Sitio web MindTune

Bitácora corta para el próximo hilo. Lo estable está en `CLAUDE.md`; aquí va lo que cambia.

## 2026-09-11 — v0 escrita (Cowork, hilo MindTune)

**Hecho.** Sitio Hugo autocontenido completo en `~/Git_Web/MindTuneWeb`: portada (hero con
teléfono, cómo funciona, tus datos C1/C2/C3, dónde hacer la terapia, quién está detrás + noticias),
`/privacidad/` (generada desde el normativo H6.7 + sección "11. Este sitio web"), `/aviso-medico/`,
`/soporte/`, `/terminos/` (borrador). Modo oscuro por defecto y claro por preferencia del sistema,
IBM Plex Sans autoalojada, cabeceras de seguridad para Cloudflare Pages, `robots.txt` y sitemap.
Build `HUGO_ENVIRONMENT=production hugo --minify --gc` verde con Hugo 0.162.1 (sin WARN).
Diseño de referencia en el canvas https://claude.ai/code/artifact/bc6f6108-aec1-4967-9dc0-6c43c284eeb9.

**Decisiones aplicadas** (documento `OPCIONES_Sitio_Web_MindTune_2026-09-10.md`, §8):
D-W1 Hugo + GitHub `HayoBK/MindTuneWeb` + Cloudflare Pages · D-W2 se trabaja desde el proyecto
Cowork MindTune · D-W3 Brevo · D-W4 sin formulario de contacto: sección "Dónde hacer la terapia"
con enlace a alemana.cl · D-W5 razón social pendiente (marcador `[[RAZON_SOCIAL]]`).

**Pendiente inmediato (Hayo):** correr los bloques de `GUIA-DEPLOY-MINDTUNEWEB.md` (git init,
repo GitHub, proyecto Pages, dominio, Email Routing).

**Pendiente de contenido:**
- Razón social EIRL en los tres lugares (`hugo.yaml`, `privacidad.md`, `terminos.md`).
- Brevo: crear formulario y pegar `params.brevo.action`.
- Imagen OpenGraph `assets/images/og.png` (1200×630) con lockup y titular.
- Capturas reales del iPhone para reemplazar el teléfono recreado en HTML, cuando haya build
  con la pantalla "Hoy" definitiva.
- Versión inglesa de la portada (opcional, después del trámite Apple).
- Revisión del abogado: privacidad y términos (estrategia maestra, paso 5).

**Ojo:** `content/privacidad.md` se regenera con el script de `CLAUDE.md`, no se edita a mano.
Si el normativo `MindTune_Politica_de_Privacidad.md` cambia (por ejemplo D-P4 retención),
regenerar y publicar.

## 2026-09-11 (tarde) — v1 "cielo": rediseño por indicaciones de Hayo

**Cambios pedidos y hechos.** Marca animada protagonista en el centro de la portada (coreografía §4.14 en
canvas: tres vueltas, cierre dorado con halo, respira, se apaga y continúa). Fondo vivo: cielo con nubes
lentas (SVG procedural, sin imágenes), recuadros semitransparentes claros; el oscuro de la app queda para
las "ventanas flotantes" de las terapias. Mucho menos texto: sin duraciones, sin detalles clínicos, sin
"TRAC". Cuatro terapias con sus nombres nuevos e íconos (Inducción de filtrado con Música —destacada, con
ilustración animada—, mMIDST, Inhibición residual, Manejo de hiperacusia). Origen: programa clínico de
Clínica Alemana de Santiago (enlace) + paper. Titular: "Terapia de sonido para reentrenar el cerebro
auditivo con tinnitus." / "Terapias de sonido incrustadas en tu música." Estado: "Próximamente".
Sin razón social en la web; correo `contacto@mindtune.cl`. El canvas de Claude Design quedó **atrás**
respecto del sitio (muestra la v0 oscura); re-sembrarlo cuando la dirección v1 esté aprobada.

**Nota para el Design System.** §4.14 dice que el cierre dorado es solo para procesos técnicos y §0 que
"no vuelve". En la web, por pedido de Hayo, el cierre es parte del relato de marca y se repite en bucle.
Conviene anotar la excepción en el DS (contexto sitio web) para que nadie lo "corrija".
