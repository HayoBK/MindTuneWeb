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

## 2026-09-12 — v2 "dosel": rediseño completo por indicaciones de Hayo

Hayo: *"a nivel estético me cargó la página actual por completo"*. Se rehízo entera, contenido y forma.

**Estética.** Fuera el logo animado y fuera el fondo de nubes (`partials/cielo.html` eliminado). Manda la
paleta oscura de la app en todo el sitio; la marca vuelve a ser estática. Fondo nuevo `partials/dosel.html`:
degradado hondo + dosel de hojas que se mueven con el viento + luz que se filtra + velo + grano, todo SVG/CSS
sin imágenes externas. Las hojas se generan con `bin/generar_dosel.py` → `partials/dosel-capas.html`
(43 KB en crudo, ~14 KB toda la portada comprimida). Tres capas: la lejana borrosa y quieta, las dos cercanas
rotando con periodos distintos; en pantallas altas el dosel se ensancha en vez de estirarse.

**Video de fondo.** No se pudo bajar un clip desde la sesión (la red no llega a Pexels/Pixabay), así que quedó
el slot listo y documentado: `params.video_fondo` + `bin/preparar-video-dosel.sh` + `GUIA-VIDEO-DE-FONDO.md`
(dónde bajarlo con licencia, o grabarlo él mismo, y el ffmpeg). Con el archivo puesto, el video reemplaza a las
capas dibujadas sin tocar plantillas. CSP con `media-src 'self'`.

**Contenido.** Portada reescrita: titular *"No hay un tinnitus. Hay el tuyo."*; **Dos maneras de usarla**
(autónoma / con equipo de salud, complemento y nunca requisito); **Perfil de Tinnitus** (por qué hay perfiles
distintos, las cuatro dimensiones, el perfilamiento se hace en la app y mejora con evaluación presencial);
**Terapias** (las cuatro, cada una con a qué perfil sirve — se botó "una terapia para cada momento del
tinnitus" y la ilustración destacada); **Aprender** (programa formativo, las cuatro ramas de H7); **De dónde
viene** con Clínica Alemana bajado a una línea como variante presencial del modelo (sin tarjeta de derivación
ni botón de tomar hora); Tus datos; **Acceso anticipado** como el bloque de más peso.

**Acceso anticipado.** Un formulario, dos caminos (`PERFIL` = paciente | clínico). Al clínico se le piden
profesión y lugar; cambia el botón y la línea legal. Texto explícito de que **no hace falta ser especialista en
tinnitus**. Dos listas de Brevo (`action_paciente`, `action_clinico`); sin ellas el envío arma un correo con
asunto distinto según el camino. `<noscript>` con el correo directo.

**Páginas interiores.** `aviso-medico`, `terminos`, `soporte` y la sección 11 de `privacidad` alineadas a la
doble modalidad (ya no dicen que la terapia se hace "bajo indicación" como condición de uso) y a los datos que
pide el formulario clínico.

**Build** verde con Hugo 0.162.1 extended (`HUGO_ENVIRONMENT=production hugo --minify --gc`), sin WARN.
Revisado en 1440×1000 y 390×844.

**Pendiente de esta vuelta:**
- Correr `hugo` y `git` en Claude Code y publicar (bloque entregado en el chat).
- Decidir si va video de fondo; si sí, seguir `GUIA-VIDEO-DE-FONDO.md`.
- Crear las **dos** listas en Brevo y pegar los dos `action`.
- `data/centros.yaml` quedó sin uso: dejarlo por si vuelve la sección, o borrarlo.
- Sigue pendiente de antes: razón social (D-W5), `assets/images/og.png`, revisión del abogado.

## 2026-09-12 (tarde) — Brevo: guía y ajuste del formulario

`GUIA-CORREO-Y-LISTAS-MINDTUNE.md` (nueva, en la raíz del repo): los pasos para dejar las dos
listas funcionando — cuenta, autenticación del dominio en Cloudflare (TXT del código Brevo + DKIM +
DMARC; **los MX no se tocan**, ahí vive el Email Routing), los cuatro atributos `NOMBRE` / `PERFIL` /
`PROFESION` / `LUGAR`, las dos listas, los dos formularios (**Marketing → Forms → Sign-up →
Full page/embedded**), sacar el `action` desde **Share → Embed code → Simple HTML**, pegarlo en
`hugo.yaml` y probar los dos caminos.

Ajuste de código: en `partials/guiones.html`, los campos del camino clínico ahora se **deshabilitan**
cuando están ocultos, para que el camino paciente no mande a Brevo atributos que su lista no tiene.

**Falta:** que Hayo pase los dos bloques `<form …>` de la Simple HTML de Brevo, para calzar los
campos ocultos exactos que espera el endpoint antes de dar por cerrado el tema.

**Corrección 2026-09-13.** La guía pasó a llamarse `GUIA-CORREO-Y-LISTAS-MINDTUNE.md` y cubre dos partes:
**A** Cloudflare Email Routing (`contacto@mindtune.cl` → `hayo.bk@gmail.com`: verificar el destino y crear
la regla; catch-all recomendado) y **B** Brevo **en modo solo-registro**: confirmación en *No confirmation*
y sin notificación al equipo, de modo que no sale ningún correo ni al inscrito ni a Hayo. Con eso la
autenticación del dominio en Brevo **queda postergada** hasta que efectivamente se escriba a la lista
(los pasos quedaron anotados al final de la guía). Decisión de Hayo: por ahora el formulario junta correos
y nada más; el `mailto` de respaldo desaparece solo al pegar los dos `action`.

## 2026-09-13 — Brevo conectado: las dos listas funcionando

**Cuenta nueva de Brevo solo para MindTune** (`contacto@mindtune.cl`), separada de la que maneja
LabONCE y Neurociencia. Atributos `NOMBRE` / `PERFIL` / `PROFESION` / `LUGAR`; listas #3
*Acceso anticipado - pacientes* y #4 *… - profesionales de salud*; dos formularios de suscripción,
cada uno a su lista, ambos con **Sin e-mail de confirmación** y sin notificación al equipo: el
sistema **no envía ni un correo**, solo acumula contactos.

**Cambios en el sitio.** Los dos `action` de Brevo quedaron en `hugo.yaml`. En el formulario se
agregó el oculto `html_type=simple` que el endpoint de Brevo espera, y el radio del conmutador
pasó de `PERFIL` a **`mt_perfil`** (con su JS) para no mandarle a Brevo un atributo que sus
formularios no declaran; el perfil ya queda dicho por la lista en la que cae la persona.
Los campos del camino clínico siguen deshabilitados cuando están ocultos, así el camino paciente
manda exactamente los campos del formulario A.

**Probado de punta a punta** contra el endpoint real: `hayo.bk+prueba.paciente@` cayó en la #3 y
`hayo.bk+prueba.clinico@` en la #4 con PROFESION y LUGAR. Los dos contactos de prueba quedaron
en Brevo para que Hayo los vea; se pueden borrar.

**Cloudflare.** No hizo falta tocar nada: la CSP ya permitía `*.sibforms.com` y no hay envío de
correo, así que la autenticación de dominio en la cuenta nueva queda para más adelante. Sí quedó
anotado el pendiente de **sacar `mindtune.cl` de la cuenta vieja de Brevo** cuando se autentique
en la nueva. (Email Routing de `contacto@mindtune.cl` → Gmail quedó andando el mismo día.)

**Pendiente:** publicar el sitio con los dos `action` (bloque entregado a Claude Code).
