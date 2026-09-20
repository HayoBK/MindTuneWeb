/**
 * Worker de mindtune.cl
 *
 * Sirve el sitio estático (binding ASSETS) y expone un único endpoint propio:
 *
 *   POST /api/inscribir
 *
 * que hace las tres cosas del acceso anticipado, en este orden:
 *   1. inscribe el contacto en la lista de Brevo que corresponde a su perfil;
 *   2. consulta cuántos hay en cada lista;
 *   3. le manda a Hayo un aviso con nombre, correo y tipo en el asunto, y los
 *      conteos en el cuerpo.
 *
 * Reglas: el paso 1 manda. Si fallan el 2 o el 3, la persona igual quedó inscrita
 * y la respuesta es exitosa — un aviso perdido es molesto, un contacto perdido no
 * se recupera nunca.
 *
 * Configuración: vars en wrangler.jsonc + el secreto BREVO_API_KEY
 * (`npx wrangler secret put BREVO_API_KEY`). Ver GUIA-CORREO-Y-LISTAS-MINDTUNE.md.
 */

const BREVO = "https://api.brevo.com/v3";
const MAX_CUERPO = 8 * 1024;

const PERFILES = {
  paciente: { etiqueta: "Paciente", lista: "Pacientes con tinnitus" },
  clinico: { etiqueta: "Profesional", lista: "Profesionales de salud" },
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/inscribir") {
      if (request.method !== "POST") {
        return json({ ok: false, error: "metodo" }, 405, { Allow: "POST" });
      }
      return inscribir(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};

/* ---------------------------------------------------------------- utilidades */

function json(datos, estado = 200, extra = {}) {
  return new Response(JSON.stringify(datos), {
    status: estado,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra },
  });
}

function limpiar(valor, max = 200) {
  return String(valor ?? "").replace(/[\r\n\t]+/g, " ").trim().slice(0, max);
}

function correoValido(correo) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(correo) && correo.length <= 254;
}

function escapar(texto) {
  return String(texto).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function ahoraEnSantiago() {
  try {
    return new Intl.DateTimeFormat("es-CL", {
      timeZone: "America/Santiago", dateStyle: "long", timeStyle: "short",
    }).format(new Date());
  } catch {
    return new Date().toISOString();
  }
}

async function brevo(env, ruta, opciones = {}) {
  const r = await fetch(BREVO + ruta, {
    ...opciones,
    headers: {
      "api-key": env.BREVO_API_KEY,
      accept: "application/json",
      ...(opciones.body ? { "content-type": "application/json" } : {}),
      ...(opciones.headers || {}),
    },
  });
  return r;
}

/* ------------------------------------------------------------------ endpoint */

async function inscribir(request, env) {
  if (!env.BREVO_API_KEY) return json({ ok: false, error: "sin_configurar" }, 500);

  // --- leer el cuerpo, venga como formulario o como JSON ---
  let datos;
  try {
    const tipo = request.headers.get("content-type") || "";
    const crudo = await request.text();
    if (crudo.length > MAX_CUERPO) return json({ ok: false, error: "cuerpo_grande" }, 413);
    if (tipo.includes("application/json")) {
      datos = JSON.parse(crudo);
    } else {
      datos = Object.fromEntries(new URLSearchParams(crudo));
    }
  } catch {
    return json({ ok: false, error: "cuerpo_invalido" }, 400);
  }

  const quiereHtml = (request.headers.get("accept") || "").includes("text/html");

  // --- trampa para bots: si el campo señuelo viene lleno, fingimos éxito ---
  if (limpiar(datos.email_address_check)) {
    return quiereHtml ? paginaGracias(env, "paciente") : json({ ok: true });
  }

  const perfil = datos.mt_perfil === "clinico" ? "clinico" : "paciente";
  const correo = limpiar(datos.EMAIL, 254).toLowerCase();
  const nombre = limpiar(datos.NOMBRE, 120);
  const profesion = limpiar(datos.PROFESION, 120);
  const lugar = limpiar(datos.LUGAR, 160);

  if (!correoValido(correo)) return json({ ok: false, error: "correo_invalido" }, 400);

  const listaId = Number(perfil === "clinico" ? env.LISTA_CLINICOS : env.LISTA_PACIENTES);
  if (!listaId) return json({ ok: false, error: "sin_configurar" }, 500);

  // --- 1. inscribir (lo único que no puede fallar en silencio) ---
  const atributos = { NOMBRE: nombre, PERFIL: perfil };
  if (perfil === "clinico") {
    atributos.PROFESION = profesion;
    atributos.LUGAR = lugar;
  }
  for (const k of Object.keys(atributos)) if (!atributos[k]) delete atributos[k];

  let alta;
  try {
    alta = await brevo(env, "/contacts", {
      method: "POST",
      body: JSON.stringify({ email: correo, attributes: atributos, listIds: [listaId], updateEnabled: true }),
    });
  } catch {
    return json({ ok: false, error: "brevo_inalcanzable" }, 502);
  }
  if (!alta.ok && alta.status !== 204) {
    const detalle = await alta.text().catch(() => "");
    console.log("brevo /contacts", alta.status, detalle.slice(0, 300));
    return json({ ok: false, error: "brevo_rechazo" }, 502);
  }

  // --- 2 y 3. conteos y aviso: mejor esfuerzo, nunca hacen fallar la inscripción ---
  let conteos = null;
  try {
    conteos = await contarListas(env);
  } catch (e) {
    console.log("conteo falló", String(e).slice(0, 200));
  }
  try {
    await avisar(env, { perfil, correo, nombre, profesion, lugar, conteos });
  } catch (e) {
    console.log("aviso falló", String(e).slice(0, 200));
  }

  return quiereHtml ? paginaGracias(env, perfil) : json({ ok: true, perfil });
}

/* -------------------------------------------------------------------- conteos */

async function contarListas(env) {
  const ids = { paciente: Number(env.LISTA_PACIENTES), clinico: Number(env.LISTA_CLINICOS) };
  const [p, c] = await Promise.all([
    brevo(env, `/contacts/lists/${ids.paciente}`).then((r) => (r.ok ? r.json() : null)),
    brevo(env, `/contacts/lists/${ids.clinico}`).then((r) => (r.ok ? r.json() : null)),
  ]);
  if (!p && !c) return null;
  return {
    paciente: p ? p.totalSubscribers : null,
    clinico: c ? c.totalSubscribers : null,
  };
}

/* ---------------------------------------------------------------------- aviso */

async function avisar(env, { perfil, correo, nombre, profesion, lugar, conteos }) {
  const { etiqueta, lista } = PERFILES[perfil];
  const quien = nombre ? `${nombre} <${correo}>` : correo;
  const asunto = `MindTune · ${etiqueta} — ${quien}`;

  const filas = [
    ["Tipo", lista],
    ["Nombre", nombre || "—"],
    ["Correo", correo],
  ];
  if (perfil === "clinico") {
    filas.push(["Profesión", profesion || "—"]);
    filas.push(["Dónde atiende", lugar || "—"]);
  }
  filas.push(["Cuándo", ahoraEnSantiago()]);

  const total = conteos && conteos.paciente != null && conteos.clinico != null
    ? conteos.paciente + conteos.clinico
    : null;
  const n = (v) => (v == null ? "no disponible" : String(v));

  const texto = [
    "Nueva inscripción al acceso anticipado de MindTune.",
    "",
    ...filas.map(([k, v]) => `${k}: ${v}`),
    "",
    "Cómo van las listas",
    `Pacientes con tinnitus: ${n(conteos && conteos.paciente)}`,
    `Profesionales de salud: ${n(conteos && conteos.clinico)}`,
    `Total: ${n(total)}`,
    "",
    "Este aviso lo manda el sitio mindtune.cl. Los contactos están en Brevo.",
  ].join("\n");

  const html = `<!doctype html><meta charset="utf-8">
<div style="font-family:-apple-system,'Segoe UI',system-ui,sans-serif;font-size:15px;line-height:23px;color:#16202C;max-width:560px">
  <p style="margin:0 0 18px">Nueva inscripción al acceso anticipado de MindTune.</p>
  <table style="border-collapse:collapse;width:100%;margin-bottom:22px">
    ${filas.map(([k, v]) => `<tr>
      <td style="padding:7px 14px 7px 0;color:#556879;white-space:nowrap;vertical-align:top">${escapar(k)}</td>
      <td style="padding:7px 0;color:#16202C">${escapar(v)}</td></tr>`).join("")}
  </table>
  <div style="border:1px solid #D7E0E8;border-radius:12px;padding:16px 18px">
    <div style="font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#556879;margin-bottom:10px">Cómo van las listas</div>
    <table style="border-collapse:collapse;width:100%">
      <tr><td style="padding:4px 0;color:#16202C">Pacientes con tinnitus</td>
          <td style="padding:4px 0;text-align:right;font-weight:600">${escapar(n(conteos && conteos.paciente))}</td></tr>
      <tr><td style="padding:4px 0;color:#16202C">Profesionales de salud</td>
          <td style="padding:4px 0;text-align:right;font-weight:600">${escapar(n(conteos && conteos.clinico))}</td></tr>
      <tr><td style="padding:10px 0 0;border-top:1px solid #D7E0E8;color:#556879">Total</td>
          <td style="padding:10px 0 0;border-top:1px solid #D7E0E8;text-align:right;font-weight:600">${escapar(n(total))}</td></tr>
    </table>
  </div>
  <p style="margin:22px 0 0;font-size:13px;color:#556879">Lo manda el sitio mindtune.cl. Los contactos están en Brevo.</p>
</div>`;

  const r = await brevo(env, "/smtp/email", {
    method: "POST",
    body: JSON.stringify({
      sender: { name: env.REMITENTE_NOMBRE || "MindTune", email: env.REMITENTE_EMAIL },
      to: [{ email: env.AVISO_A, name: env.AVISO_NOMBRE || "" }],
      replyTo: { email: correo, name: nombre || correo },
      subject: asunto,
      textContent: texto,
      htmlContent: html,
    }),
  });
  if (!r.ok) console.log("brevo /smtp/email", r.status, (await r.text().catch(() => "")).slice(0, 300));
}

/* ------------------------------------------- respuesta para navegador sin JS */

function paginaGracias(env, perfil) {
  const mensaje = perfil === "clinico"
    ? "Quedaste anotado. Te escribimos cuando abramos el acceso clínico del piloto."
    : "Quedaste anotado. Te escribimos apenas haya cupo en el piloto.";
  return new Response(`<!doctype html>
<html lang="es-CL"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Listo · MindTune</title>
<style>
  :root{color-scheme:dark}
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0B1219;color:#E6EDF3;
    font-family:-apple-system,"Segoe UI",system-ui,sans-serif;font-size:16px;line-height:24px;padding:24px}
  .caja{max-width:460px;text-align:center;border:1px solid #24344A;border-radius:16px;padding:40px 32px;background:#0E1620}
  h1{font-size:26px;line-height:32px;margin:0 0 14px;letter-spacing:-.02em}
  p{margin:0 0 26px;color:#94A9BC}
  a{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 26px;border-radius:12px;
    background:#4CB5A5;color:#0E1620;text-decoration:none;font-weight:600}
</style></head>
<body><div class="caja"><h1>Listo.</h1><p>${escapar(mensaje)}</p><a href="/">Volver a MindTune</a></div></body></html>`,
    { status: 200, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
}
