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
   "TRAC" en ningún texto visible; cada terapia lleva su ícono, su frase y **a qué perfil sirve**, nada más.
6-bis. **Las dos ideas que la página tiene que dejar clarísimas** (Hayo, 2026-09-12): (a) la **doble
   modalidad** — se usa sola, y *además* puede acompañarla un equipo de salud, que es complemento y nunca
   requisito; (b) **no hay un tinnitus**: hay perfiles distintos, la app trae un proceso de perfilamiento
   y terapias específicas para cada perfil, más un programa formativo. Prohibido volver a "una terapia para
   cada momento del tinnitus". Clínica Alemana se menciona **en una línea**, como la variante presencial del
   modelo MindTune; sin tarjeta de derivación ni botón de tomar hora (por eso `data/centros.yaml` quedó sin uso).
7. Lo editable por dato va en `hugo.yaml` (`params`) o en `data/centros.yaml`; no en plantillas.
8. Commits chicos, en español.

## Arquitectura

- `layouts/_default/baseof.html` → esqueleto. Partials: `head.html`, `cabecera.html` (menú
  `main` + botón noticias; menú móvil), `pie.html` (menú `footer`, razón social, aviso),
  `marca.html` (SVG de la marca; `(dict "animada" true)` dibuja el trazo al cargar), `guiones.html`
  (menú móvil + aparición por `IntersectionObserver`, respeta `prefers-reduced-motion`).
- **Dirección visual v2 "dosel" (2026-09-12):** manda la **paleta oscura de la app** en todo el sitio
  (`:root` = tokens del modo oscuro; no hay modo claro en la web). Fondo fijo `partials/dosel.html`:
  degradado + dosel de hojas + luz que se filtra + velo + grano, todo SVG y CSS, sin imágenes externas.
  Las hojas están **generadas**: `bin/generar_dosel.py` escribe `partials/dosel-capas.html` (no editar a
  mano; volver a correr el script si se cambia la geometría). Tres capas: la lejana va borrosa y quieta,
  las dos cercanas rotan unos grados alrededor de su nacimiento con periodos distintos. Sobre eso,
  superficies de vidrio oscuro (`.mt-vidrio`).
  **La marca es estática**: se eliminó la coreografía en canvas de la v1 (y con ella `partials/cielo.html`).
- **Video de fondo (opcional):** si `params.video_fondo` trae un nombre y existe `static/video/<nombre>.mp4`,
  el video reemplaza a las capas dibujadas. `bin/preparar-video-dosel.sh` lo convierte y `GUIA-VIDEO-DE-FONDO.md`
  dice de dónde sacarlo. La CSP ya trae `media-src 'self'`.
- `layouts/index.html` → portada: marca estática + chip de estado + titular; **Dos maneras de usarla**
  (autónoma / con equipo de salud); **Perfil de Tinnitus** (por qué hay perfiles distintos + las cuatro
  dimensiones); **Terapias** (las cuatro, cada una con a qué perfil sirve; íconos en
  `partials/icono-terapia.html`, matices §4.15); **Aprender** (programa formativo, cuatro ramas) junto a
  **De dónde viene** (programa clínico + la línea de la variante presencial en Clínica Alemana + paper);
  Tus datos; **Acceso anticipado** (el bloque con más peso de la página).
- `layouts/_default/single.html` → páginas interiores con índice lateral (`.TableOfContents`, h2).
  Render hooks: tablas envueltas para scroll horizontal; enlaces externos con `rel="noopener"`.
- `content/`: `_index.md`, `privacidad.md` (generado), `aviso-medico.md`, `soporte.md`,
  `terminos.md` (borrador; lo revisa el abogado). Los cuatro se alinearon a la doble modalidad el
  2026-09-12: ya no dicen que la terapia se hace "bajo indicación" como condición de uso.
- `static/_headers`: cabeceras de seguridad para Cloudflare Pages (CSP permite `form-action` a
  Brevo). Si se agrega un script o dominio externo, actualizar la CSP.

## Formulario de acceso anticipado (Brevo, D-W3)

Un solo formulario con **dos caminos**: *Tengo tinnitus* / *Soy profesional de salud* (radios
`PERFIL`). Al elegir clínico aparecen dos campos más (`PROFESION`, `LUGAR`), cambia el texto del
botón y el de la línea legal. Todo eso lo hace `partials/guiones.html`.

`hugo.yaml → params.brevo.action_paciente` y `action_clinico`: **dos listas distintas**. Si la
del camino elegido está vacía, el envío arma un `mailto:` a `params.correo` con lo escrito, con
asunto distinto según el camino. El honeypot `email_address_check` y `locale=es` ya están.
Hay `<noscript>` con el correo directo.

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
