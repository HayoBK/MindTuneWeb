# Guía de publicación — mindtune.cl (paso a paso para Hayo)

> Escrita por Cowork el 2026-09-11. Cuatro bloques para **Claude Code** (pegar tal cual, uno a la
> vez, y devolver la salida al chat si algo no dice lo esperado) y tres pasos en el **panel de
> Cloudflare** que solo puedes hacer tú porque piden tus credenciales. Tiempo total: 20–30 min.
> Modelo recomendado para Claude Code en esta tarea: **Sonnet**.

Estado de partida: el sitio ya está escrito en `~/Git_Web/MindTuneWeb`, `mindtune.cl` está
inscrito en NIC Chile y el dominio ya está agregado en Cloudflare (nameservers cambiados).

---

## Bloque 1 — Verificar el build en tu Mac

Abre Terminal y pega:

```bash
cd ~/Git_Web/MindTuneWeb && claude
```

Dentro de Claude Code, pega:

```text
Estamos en el repo del sitio web MindTune (Hugo autocontenido, ver CLAUDE.md). Haz solo esto y muéstrame la salida completa:

1. hugo version   (debe decir v0.162.1 extended; si no, dímelo y no sigas)
2. HUGO_ENVIRONMENT=production hugo --minify --gc
3. Si el build termina sin ERROR, corre `hugo server -D` en segundo plano, dime la URL local y déjalo corriendo para que yo lo revise en el navegador. No cambies ningún archivo.
```

Abre `http://localhost:1313/` en el navegador. Revisa la portada, `/privacidad/`, `/soporte/`,
`/aviso-medico/`, `/terminos/`, y el menú en una ventana angosta. Si algo se ve mal, cópialo al
chat de Cowork (captura o descripción) antes de seguir. Cuando estés conforme, en Claude Code:
`detén el hugo server`.

---

## Bloque 2 — Repo local y GitHub (cuenta HayoBK)

En Claude Code:

```text
Publica este sitio en GitHub. Haz exactamente esto, en orden, y muéstrame la salida de cada paso:

1. git init -b main
2. Verifica que .gitignore excluya public/ y resources/_gen/ (ya debería).
3. git add -A && git commit -m "Sitio MindTune v0: portada, privacidad, soporte, aviso médico y términos"
4. gh auth status   (debe mostrar la cuenta HayoBK activa; si muestra otra, usa `gh auth switch --user HayoBK`)
5. gh repo create HayoBK/MindTuneWeb --public --source=. --remote=origin --push --description "Sitio web de MindTune (mindtune.cl) — Hugo autocontenido, Cloudflare Pages"
6. git remote -v y git log --oneline -1

No agregues workflows de GitHub Actions ni archivo CNAME: el hosting es Cloudflare Pages.
```

Comprueba en el navegador que `https://github.com/HayoBK/MindTuneWeb` existe y muestra los
archivos. El repo puede ser público: no contiene nada privado (la razón social es un marcador).

---

## Paso A (tú, en Cloudflare) — Crear el proyecto de Pages

1. Entra a https://dash.cloudflare.com → menú lateral **Workers & Pages** → **Create** →
   pestaña **Pages** → **Connect to Git**.
2. Autoriza GitHub si te lo pide y elige la cuenta **HayoBK** → repositorio **MindTuneWeb** →
   **Begin setup**.
3. Configuración del build:
   - *Project name:* `mindtune` (la URL provisional será `mindtune.pages.dev`).
   - *Production branch:* `main`.
   - *Framework preset:* **Hugo**.
   - *Build command:* `hugo --gc --minify`
   - *Build output directory:* `public`
   - Despliega **Environment variables (advanced)** y agrega:
     `HUGO_VERSION` = `0.162.1`
     (esta variable es la que hace que Cloudflare use la misma versión de Hugo que tu Mac).
4. **Save and Deploy**. El primer build tarda 1–2 minutos. Cuando diga *Success*, abre
   `https://mindtune.pages.dev` y verifica que sea el sitio.

Si el build falla, copia el log al chat de Cowork. La causa habitual es la versión de Hugo.

---

## Paso B (tú, en Cloudflare) — Conectar el dominio

1. En el proyecto **mindtune** → pestaña **Custom domains** → **Set up a custom domain**.
2. Escribe `mindtune.cl` → **Continue**. Como el dominio ya está en tu cuenta de Cloudflare,
   te ofrece crear el registro DNS automáticamente → **Activate domain**.
3. Repite con `www.mindtune.cl`. Cloudflare crea un CNAME y redirige `www` a la raíz.
4. Espera a que ambos digan **Active** (minutos; puede tardar hasta una hora la primera vez).
5. En el sitio del dominio (menú lateral → `mindtune.cl` → **SSL/TLS** → **Edge Certificates**)
   activa **Always Use HTTPS**.

Abre `https://mindtune.cl`. Debe cargar con candado y sin avisos.

---

## Paso C (tú, en Cloudflare) — Correo `contacto@mindtune.cl`

1. Menú lateral → `mindtune.cl` → **Email** → **Email Routing** → **Get started**.
2. *Custom address:* `contacto` → *Destination:* tu correo personal → **Save**. Te llega un correo
   de verificación al destino: acéptalo.
3. Cloudflare te pide agregar los registros MX y TXT: pulsa **Add records and enable**.
4. Prueba: envíate un correo a `contacto@mindtune.cl` desde otra cuenta. Debe llegar a tu bandeja.
   (Opcional después: en Gmail, *Configuración → Cuentas → Enviar como* para responder desde
   `contacto@mindtune.cl`; necesita SMTP de terceros, no hace falta para el trámite de Apple.)

Con esto Apple ya tiene lo que exige: dominio propio con HTTPS, sitio con contenido, política de
privacidad en `https://mindtune.cl/privacidad/`, soporte en `https://mindtune.cl/soporte/`, y
correo en el dominio.

---

## Bloque 3 — Ciclo de edición de aquí en adelante

Cada vez que Cowork cambie archivos del sitio, en Claude Code:

```text
Valida y publica los cambios del sitio MindTune:
1. git status (muéstrame qué cambió)
2. HUGO_ENVIRONMENT=production hugo --minify --gc  (sin ERROR)
3. git add -A && git commit -m "<mensaje corto en español que describa el cambio>"
4. git push
Cloudflare Pages publica solo con el push; dime cuando termine.
```

En Cloudflare, **Workers & Pages → mindtune → Deployments** muestra cada publicación y su log.

---

## Pendientes que dependen de ti (no del código)

| Qué | Dónde se pone | Estado |
|---|---|---|
| Razón social de la EIRL (D-W5) | `hugo.yaml → params.razon_social` + regenerar privacidad | ⏸️ no se publica por ahora (decisión 2026-09-11) |
| Formulario Brevo (D-W3): crear cuenta y formulario, pegar `action` | `hugo.yaml → params.brevo.action` | ⏳ mientras, el botón abre un correo |
| Imagen OpenGraph (vista previa al compartir el enlace) | `assets/images/og.png` (1200×630) | ⏳ Cowork la genera cuando digas |
| Revisión del abogado de privacidad y términos | textos en `content/` | ⏳ paso 5 de la estrategia maestra |
| DOI del paper | `hugo.yaml → params.paper.url` | ✅ verificado contra el PDF (10.3390/brainsci16060644) |
