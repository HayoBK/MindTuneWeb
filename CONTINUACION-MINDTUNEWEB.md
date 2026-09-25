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

## 2026-09-20 — Pop-up de éxito y aviso por inscripción (Worker propio)

Dos pedidos de Hayo: que la pantalla de "success" de Brevo (blanca y pobre) desapareciera, y
recibir un correo por cada inscripción con nombre/correo/tipo en el asunto y el conteo de las
listas en el cuerpo. Brevo no tiene ninguna variable de tamaño de lista, así que el conteo obligaba
a consultar su API: se resolvió metiendo un endpoint propio en medio.

**`src/worker.js` (nuevo).** El sitio pasa de ser solo assets a un Worker con assets
(`main` + `assets.binding: ASSETS` en `wrangler.jsonc`). Expone `POST /api/inscribir`, que
inscribe en la lista según `mt_perfil`, consulta `totalSubscribers` de las dos listas y manda el
aviso por `/v3/smtp/email`. Orden de prioridades explícito: si fallan el conteo o el aviso, la
respuesta sigue siendo exitosa — solo el alta del contacto puede hacer fallar la petición.
Trampa de bots (`email_address_check`), límite de cuerpo, saneado de campos y `replyTo` apuntando
al inscrito. Config en `vars`; la clave va como secreto (`npx wrangler secret put BREVO_API_KEY`).

**Front.** El formulario postea a `/api/inscribir` por `fetch`; al volver bien se oculta y en su
lugar aparece un bloque "Quedaste anotado", más un pop-up `.mt-aviso` (marca, título, texto y
botón *Seguir explorando*) que cierra con botón, Escape o clic fuera y deja a la persona donde
estaba. Estado de error propio, con salida a `contacto@mindtune.cl`, sin perder lo escrito.
Sin JS el POST normal devuelve una página de confirmación sobria desde el Worker.

**Dos detalles que costaron y conviene no volver a pisar:** el pop-up vive al final del `main`,
**fuera de todo `.mt-vidrio`**, porque `backdrop-filter` convierte al elemento en bloque contenedor
de sus hijos `fixed` y lo encerraba dentro de la tarjeta; y `.mt-formulario` necesitó
`[hidden]{display:none}` porque su `display:flex` le ganaba al atributo `hidden`.

**Limpieza.** Fuera el bloque `brevo` de `hugo.yaml` y `*.sibforms.com` de `form-action` en la CSP:
ya no se postea a Brevo desde el navegador. Los dos formularios de Brevo quedan sin uso (se pueden
dejar como respaldo). Sección 11 de privacidad menciona ahora el aviso interno.

**Verificado** con un endpoint simulado en 1440×1000 y 390×844: éxito, error y cierre, sin errores
de consola. Remitente `MindTune <contacto@mindtune.cl>` ya estaba verificado en Brevo.

**Pendiente de Hayo:** crear la clave API en Brevo y cargarla con `wrangler secret put`; recién
ahí el endpoint funciona. Sigue pendiente la autenticación del dominio en la cuenta nueva (mejora
la entregabilidad del aviso y hace falta el día que se escriba a la lista).

## 2026-09-20 (tarde) — Las dos tarjetas de early adopter son atajos; repaso en iPhone

Hayo: en el teléfono las descripciones de *pacientes* y *clínicos* quedaban largas y nada indicaba
que más abajo había un formulario que completar.

**Las tarjetas ahora son enlaces** (`<a href="#formulario-anticipado" data-perfil="…">`): tocarlas
baja al formulario y deja marcado el camino que corresponde — el manejador `[data-perfil]` que ya
existía para el botón de la portada hace el resto. Cada una cierra con **"Este soy yo, anotarme →"**
en teal, que es lo que vuelve obvio el gesto; la flecha se corre al pasar el cursor. El texto del
clínico se acortó (salió la enumeración larga y la frase del panel, que ahora vive en el pop-up).
Sin JS igual funcionan: son anclas de verdad.

**Tres arreglos de teléfono que salieron del repaso:**
- `.mt-seccion { scroll-margin-top: 88px }` y lo mismo en `#formulario-anticipado`: la cabecera
  pegajosa se estaba comiendo la etiqueta de sección al llegar desde el menú.
- El conmutador *Tengo tinnitus / Soy profesional de salud* ocupa el ancho completo y se parte en
  dos mitades iguales bajo 600 px; antes quedaba dentado.
- `text-wrap: pretty` en titulares bajo 620 px: `balance` dejaba líneas colgando de dos palabras
  en títulos de cuatro líneas.

**Revisado** en 390×844 y 375×667 con UA y touch de iPhone: sin scroll horizontal (`scrollWidth`
igual al ancho de ventana), sin errores de consola, y al tocar la tarjeta de clínico el formulario
queda a 96 px del borde con el camino ya marcado y los campos extra visibles.

## 2026-09-21 — Favicon e íconos del sitio

**Punto de partida.** El favicon ya existía y ya estaba enlazado (`static/favicon.svg`, copia del
appicon de placa clara, con ~8 KB de metadatos C2PA pegados). Lo que faltaba era todo lo demás:
no había `favicon.ico` (los navegadores lo piden solo a la raíz y devolvía 404), el
`apple-touch-icon` apuntaba a un SVG —que iOS **ignora**: ahí tiene que ir un PNG de 180— y no
había PNG de 192/512 ni manifest.

**Decisión de Hayo.** El favicon usa la **placa oscura del sitio** (`#0E1620`, anillo `#E6EDF3`,
señal `#4CB5A5`) con la marca casi al borde: es la única variante que a 16 px deja leer los cinco
segmentos y la pieza suelta. Se descartaron la placa clara actual y la versión sin placa (esta
última desaparece sobre pestaña clara).

**Hecho.** `bin/generar-favicon.py` (Pillow) dibuja todo desde la geometría canónica de la marca
—los arcos del SVG salen idénticos, byte a byte, a `static/brand/mindtune_mark_dark.svg`— y escribe
`static/favicon.svg` (576 bytes, sin metadatos), `static/favicon.ico` (16/32/48, cada tamaño
dibujado a su medida), `static/apple-touch-icon.png` (180, opaco y sin esquinas redondeadas: iOS
aplica su máscara y rechaza alfa), `static/icon-192.png` y `static/icon-512.png`. Más
`static/site.webmanifest` (`display: browser` — el sitio es el sitio, la app está en la App Store).
`layouts/partials/head.html` enlaza los cuatro.

El apple-touch-icon y los PNG del manifest llevan el margen del ícono de iOS (inset 0,88), que es
lo que la máscara redondeada del sistema necesita; el favicon no.

**Para regenerar:** `python3 bin/generar-favicon.py` desde la raíz del repo.

**Ojo con el caché.** Los favicons se cachean con ganas: para verificar el cambio, recarga dura o
abre `https://mindtune.cl/favicon.ico` directo.

## 2026-09-21 (tarde) — El favicon estaba publicado; lo que faltaba era el caché y la doc del deploy

**Verificado en vivo** (navegador, sin caché): `mindtune.cl` sirve `/favicon.ico` (200,
`image/vnd.microsoft.icon`, 5.895 bytes, con 16/32/48 dentro), `/favicon.svg` (576 bytes),
`/apple-touch-icon.png`, `/icon-192.png` y `/site.webmanifest`, y el `<head>` publicado trae los
cuatro enlaces. Igual en `www.mindtune.cl`. **El sitio estaba bien**: lo que mostraba el ícono
viejo era el caché de favicons del navegador, que no se refresca con recarga dura.

**Hecho.** `hugo.yaml → params.iconos_version` (hoy `"2026-09-21"`) y el `?v=` correspondiente en
los cuatro enlaces del `head`. Al regenerar iconos hay que subir esa fecha: es la única forma de
que el navegador vuelva a pedirlos.

**Corregida la documentación del hosting, que estaba desactualizada y es trampa cara.** `CLAUDE.md`
y `GUIA-DEPLOY-MINDTUNEWEB.md` decían "Cloudflare Pages conectado a GitHub, publica solo con el
push". Desde el 2026-09-20 el sitio lo sirve el **Worker** de `wrangler.jsonc`, que sube `public/`
—y `public/` está en `.gitignore`—, así que **el push no publica: publica `npx wrangler deploy`**.
El Bloque 3 de la guía ya lleva ese paso; los Bloques 1–2 y Pasos A–C quedan como historia del
montaje con Pages.

## 2026-09-23 — Sección «Cómo se ve»: video preview de la app en la portada

**Hecho (Cowork).** Nueva sección `#como-se-ve` en `layouts/index.html`, entre la portada y «Dos maneras
de usarla»: marco `.mt-vidrio.mt-video` con etiqueta, una línea de texto y un `<video controls playsinline
preload="none">` con póster. **Sin autoplay** a propósito (el dosel ya se mueve). CSS `.mt-video*` en
`assets/css/mindtune.css` (borde 1 px, sin sombra). Archivos en `static/video/preview.mp4` (1080p, 30 fps,
31 s, sin audio, 3 MB) y `static/video/preview-poster.jpg`. La CSP ya permitía `media-src 'self'`.

**Origen del video.** Grabación real del iPhone (QuickTime) compuesta por Cowork en HTML/Playwright/ffmpeg
(fuentes en la carpeta OneDrive `MindTune2027/Presentacion_Colegas_2026-09/`). Siete planos con títulos:
terapias de sonido en el teléfono · la música del paciente como vehículo · perfil guía la recomendación ·
cuatro modalidades · dos maneras de usarla · modo autónomo · modo acompañado. Es la **variante web**: dos
bajadas se reescribieron en voz de paciente (la versión para colegas vive en la carpeta de la presentación).
Revisado contra D-L8 (sin eficacia ni cifras) y contra la regla 6-bis (doble modalidad).

**Pendiente (Hayo, en Claude Code):** build verde + `npx wrangler deploy` + commit. Si más adelante hay
video con tinnitumetría o con la Lección 0, se reemplaza el mismo archivo sin tocar plantillas.

## 2026-09-25 — «Cómo se ve»: el video parte solo

**Hecho (Cowork), a pedido de Hayo.** Revierte el «sin autoplay» del 2026-09-23. El `<video>` lleva
`muted loop data-autoplay` (sigue con `controls playsinline preload="none"` y póster) y `partials/guiones.html`
lo enciende con un `IntersectionObserver` (umbral 0,5) cuando se ve en pantalla y lo pausa al salir, así no
descarga los 3 MB a quien no baja hasta ahí. Con `prefers-reduced-motion` no parte (queda el póster). Si la
persona lo pausa a mano, no se vuelve a encender solo.
