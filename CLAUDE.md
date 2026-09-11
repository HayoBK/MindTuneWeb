# CLAUDE.md — Sitio web MindTune (mindtune.cl)

Contexto y reglas para trabajar en este repositorio con Claude (Cowork planifica y edita;
Claude Code corre `hugo` y `git`). Propietario: **Hayo Breinbauer**. Idioma: **español de Chile**.

## Qué es

Sitio público de **MindTune**, la app de terapia sonora para tinnitus (repo de la app:
`~/development/MindTune_Pilot_v2027`). Existe por dos razones: (1) es requisito del trámite de
Apple Developer Program como organización (dominio propio + política de privacidad + soporte),
y (2) es la portada del producto: qué hace, dónde se indica, y suscripción a noticias.

**Los normativos viven fuera de este repo**, en la carpeta OneDrive
`…/2026.06.26_PlanFondefIDeA 2027/MindTune2027/app_piloto/`:

| Qué manda | Archivo |
|---|---|
| Colores, tipografía, espaciado, prohibiciones | `MindTune_Design_System.md` (§0–§3, §6) |
| Marca "Ruta 5, anillo abierto" | `brand/README.md` + los tres SVG (copiados en `static/brand/`) |
| Qué se puede afirmar (D-L8, "wellness indicado") | `../ESTRATEGIA_MAESTRA_Legal_Negocio.md` |
| Política de privacidad (fuente de `content/privacidad.md`) | `MindTune_Politica_de_Privacidad.md` (H6.7) |
| Decisiones del sitio (D-W1…D-W5) | `OPCIONES_Sitio_Web_MindTune_2026-09-10.md` |
| Diseño de referencia | canvas https://claude.ai/code/artifact/bc6f6108-aec1-4967-9dc0-6c43c284eeb9 (fuentes en `design_canvas_web/`) |

## Stack

- **Hugo extended 0.162.1, autocontenido**: sin tema externo, sin módulos Go, sin npm. Plantillas
  en `layouts/`, CSS en `assets/css/mindtune.css` (pasa por `minify | fingerprint` en `head.html`).
- **Hosting: Cloudflare Pages** (D-W1), conectado al repo GitHub `HayoBK/MindTuneWeb`, rama `main`.
  Build: `hugo --gc --minify`, variable `HUGO_VERSION=0.162.1`. No hay workflow de GitHub Actions
  ni `CNAME`: el dominio se configura en el panel de Cloudflare. Ver `GUIA-DEPLOY-MINDTUNEWEB.md`.
- **DNS y correo**: Cloudflare (Email Routing `hola@mindtune.cl` → correo de Hayo).
- **baseURL** es la raíz del dominio (`https://mindtune.cl/`), así que las rutas absolutas
  (`/fonts/…`, `/privacidad/`) funcionan; igual se usa `relURL`/`pageRef` en plantillas por hábito.
- Fuente **IBM Plex Sans autoalojada** (`static/fonts/`, licencia OFL incluida). No cargar Google Fonts.

## Reglas de oro

1. **Build verde antes de commitear**: `HUGO_ENVIRONMENT=production hugo --minify` sin `ERROR`.
2. **El sistema de diseño manda** (§0): un solo acento (`--acento`), bordes de 1 px y **nunca sombras**,
   piso de 15 px en todo lo que se lee, sin rojo, sin emoji, sin formas de onda, sin candados ni
   "desbloquear". Los tokens están en `:root` (oscuro) y en `@media (prefers-color-scheme: light)`.
   Clases con prefijo `mt-`; estados con prefijo `es-` (`es-visible`, `es-abierta`, `es-hecha`).
3. **D-L8 en todo texto público**: describir qué hace la app y remitir la eficacia al paper
   (Henríquez et al., Brain Sci. 2026;16:644). **Nunca** "reduce", "trata", "cura", ni cifras de THI.
   Redacción §6: segunda persona, presente, frases cortas, sin "¡Muy bien!" ni "Error".
4. **`content/privacidad.md` no se edita a mano.** Se regenera desde el normativo con el script de
   abajo. Lo único que se agrega en este repo es la sección "11. Este sitio web" (ver el script).
5. **Razón social**: por decisión de Hayo (2026-09-11) **no se muestra en la web por ahora**; los textos
   legales dicen "MindTune". Cuando decida publicarla va en `hugo.yaml → params.razon_social` y en
   `privacidad.md` / `terminos.md` (regenerar privacidad con el script). Correo público: `contacto@mindtune.cl`.
6. **Menos es más en esta etapa** (Hayo, 2026-09-11): sin duraciones de terapias, sin detalles clínicos, sin
   "TRAC" en ningún texto visible; las cuatro terapias se nombran y se muestran con su ícono y su frase, nada más.
7. Lo editable por dato va en `hugo.yaml` (`params`) o en `data/centros.yaml`; no en plantillas.
8. Commits chicos, en español.

## Arquitectura

- `layouts/_default/baseof.html` → esqueleto. Partials: `head.html`, `cabecera.html` (menú
  `main` + botón noticias; menú móvil), `pie.html` (menú `footer`, razón social, aviso),
  `marca.html` (SVG de la marca; `(dict "animada" true)` dibuja el trazo al cargar), `guiones.html`
  (menú móvil + aparición por `IntersectionObserver`, respeta `prefers-reduced-motion`).
- **Dirección visual v1 "cielo" (2026-09-11):** fondo fijo de cielo con tres capas de nubes que derivan
  (`partials/cielo.html`, ruido fractal SVG, sin imágenes), recuadros de vidrio claros (`.mt-vidrio`), y el
  oscuro de la app reservado a las "ventanas flotantes" de las cuatro terapias (`.mt-terapia`). La marca
  animada es la protagonista de la portada: `<canvas id="marca-viva">` dibujado en `partials/guiones.html`
  con la coreografía del Design System §4.14 (tres vueltas → cierre dorado con halo → respira → se apaga →
  una pieza se suelta → continúa). Con `prefers-reduced-motion` se muestra la marca estática.
- `layouts/index.html` → portada: marca animada + recuadro con titular y CTA; Cuatro terapias (destacada
  Inducción de filtrado con ilustración animada, luego mMIDST, Inhibición residual, Manejo de hiperacusia;
  íconos en `partials/icono-terapia.html`, matices §4.15); Origen (programa clínico de Clínica Alemana +
  paper) y Dónde hacer la terapia (`data/centros.yaml`); Tus datos (una línea); Noticias.
- `layouts/_default/single.html` → páginas interiores con índice lateral (`.TableOfContents`, h2).
  Render hooks: tablas envueltas para scroll horizontal; enlaces externos con `rel="noopener"`.
- `content/`: `_index.md`, `privacidad.md` (generado), `aviso-medico.md`, `soporte.md`,
  `terminos.md` (borrador; lo revisa el abogado).
- `static/_headers`: cabeceras de seguridad para Cloudflare Pages (CSP permite `form-action` a
  Brevo). Si se agrega un script o dominio externo, actualizar la CSP.

## Formulario de noticias (Brevo, D-W3)

`hugo.yaml → params.brevo.action` vacío ⇒ el botón abre un `mailto:`. Cuando Hayo cree el
formulario en Brevo (Contactos → Formularios → Compartir → HTML), pegar el `action` ahí y
verificar el nombre del campo (`EMAIL` por defecto). El honeypot `email_address_check` y
`locale=es` ya están en la plantilla.

## Regenerar `content/privacidad.md`

```bash
python3 - <<'EOF'
import re, pathlib
SRC = pathlib.Path.home()/'Library/CloudStorage/OneDrive-Personal/2-Casper/00-CurrentResearch/2026.06.26_PlanFondefIDeA 2027/MindTune2027/app_piloto/MindTune_Politica_de_Privacidad.md'
src = SRC.read_text(encoding='utf-8')
body = src[src.index('## A. Política de privacidad de {{APP}}'):src.index('## B. App Store Connect')]
body = body.replace('## A. Política de privacidad de {{APP}}\n', '', 1).rstrip().rstrip('-').rstrip()
for k, v in {'{{APP}}': 'MindTune', '{{DOMINIO}}': 'mindtune.cl', '{{CONTACTO}}': 'contacto@mindtune.cl'}.items():
    body = body.replace(k, v)
assert '{{APP}}' not in body and '{{CONTACTO}}' not in body
body = body.replace('{{RAZON_SOCIAL}}', 'MindTune')   # la razón social no se publica todavía (Hayo, 2026-09-11)
body = re.sub(r'^### ', '## ', body, flags=re.M)
dest = pathlib.Path('content/privacidad.md')
actual = dest.read_text(encoding='utf-8')
fm = actual[:actual.index('\n---\n', 4) + 5]          # conserva el front matter
web = actual[actual.index('## 11. Este sitio web'):]  # conserva la sección propia del sitio
dest.write_text(fm + '\n' + body + '\n\n' + web, encoding='utf-8')
print('privacidad.md regenerado')
EOF
```

## Modo de trabajo

Cowork (hilo del proyecto MindTune, con `~/Git_Web` conectado) escribe archivos y textos, y
entrega a Hayo bloques para pegar en Claude Code (`cd ~/Git_Web/MindTuneWeb && claude`), que
corre `hugo` y `git`. Los textos publicables se muestran completos en el chat antes de escribirlos.
Al cerrar un hilo: actualizar `CONTINUACION-MINDTUNEWEB.md`, y en la carpeta MindTune2027 la
bitácora del `ROADMAP_MAESTRO.md` §3-bis y el `CLAUDE.md` del proyecto.
