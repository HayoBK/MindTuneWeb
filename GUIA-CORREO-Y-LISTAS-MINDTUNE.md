# Correo y listas de MindTune — guía paso a paso

Dos cosas distintas que se suelen confundir:

- **Parte A — el correo.** Que lo que llegue a `contacto@mindtune.cl` aterrice en tu Gmail.
  Es Cloudflare, son cinco minutos.
- **Parte B — las listas.** Que el formulario del sitio **guarde** los correos de quien se
  inscribe, en vez de abrirte un mail. Es Brevo, y quedó configurado **sin que se envíe ni un
  solo correo** —ni a ti ni a quien se inscribe— hasta que tú decidas. **Ya está hecho**; la
  Parte B de abajo es la documentación de cómo quedó.

Ambas quedaron funcionando el 2026-09-13.

---

# Parte A — `contacto@mindtune.cl` → `hayo.bk@gmail.com`

El dominio ya está en Cloudflare y ya tienes Email Routing andando para `hola@`. Falta la
dirección `contacto@` y, probablemente, verificar el Gmail como destino.

### A1. Entra a Email Routing

Cloudflare → tu cuenta → **Compute → Email Service → Email Routing** → elige `mindtune.cl`.

Si el dominio todavía no aparece activado ahí, aprieta **Onboard Domain**, elige `mindtune.cl`,
revisa los registros que Cloudflare va a agregar (MX + un TXT de SPF + un TXT de DKIM) y
confirma con **Done**. Cloudflare los escribe solo; no hay que copiar nada a mano.

### A2. Verifica tu Gmail como destino

Pestaña **Destination Addresses** → escribe `hayo.bk@gmail.com` → enviar.

Cloudflare te manda un correo a ese Gmail. Ábrelo y aprieta **Verify email address**.
Hasta que no hagas eso, la dirección queda en *Pending* y **no llega nada** — es la causa más
común de "no me redirige".

Si ya aparece ahí en verde (*Verified*), sáltate el paso.

### A3. Crea la regla de `contacto@`

Pestaña **Routing Rules** → **Create routing rule**:

- **Email pattern / Custom address:** `contacto` @ `mindtune.cl`
- **Action:** *Send to an email*
- **Destination:** `hayo.bk@gmail.com`
- **Save**

### A4. Opcional pero recomendable: el catch-all

En la misma pestaña **Routing Rules**, abajo, hay una regla **Catch-all address**. Actívala
apuntando al mismo Gmail. Así cualquier cosa que alguien escriba a `@mindtune.cl` —`info@`,
`hola@`, un typo, lo que sea— igual te llega, y no pierdes un contacto por una letra.

### A5. Pruébalo

Desde tu Gmail, mándate un correo a `contacto@mindtune.cl`. Debería volver en menos de un
minuto. Si no llega: revisa la carpeta de spam, y revisa que en **Destination Addresses** el
Gmail diga *Verified*.

> **Ojo con una cosa.** Los registros **MX** de `mindtune.cl` son de Email Routing y no se
> tocan nunca. Más adelante, cuando quieras *enviar* correos desde `@mindtune.cl` con Brevo,
> Brevo te va a pedir sus propios registros (TXT y DKIM): esos se **agregan**, no reemplazan
> nada. Si algún día borras los MX, dejas de recibir correo.

---

# Parte B — Brevo: cómo quedó (2026-09-13)

**Cuenta propia de MindTune**, separada de la que maneja LabONCE y el Depto. de Neurociencia.
Registrada con `contacto@mindtune.cl`. Plan gratuito.

## Lo que hay adentro

**Atributos de contacto** (Settings → Contacts → Contact attributes), todos texto:
`NOMBRE` (ya venía), `PERFIL`, `PROFESION`, `LUGAR`.

**Dos listas** (CRM → Listas):

| # | Lista | Quién cae ahí |
|---|---|---|
| 3 | `Acceso anticipado - pacientes` | Quien marca *Tengo tinnitus* en mindtune.cl |
| 4 | `Acceso anticipado - profesionales de salud` | Quien marca *Soy profesional de salud* |

**Dos formularios** (Marketing → Formularios → Suscripción):

| Formulario | Campos | Lista | Confirmación |
|---|---|---|---|
| `MindTune acceso anticipado - pacientes` | EMAIL (obligatorio), NOMBRE | #3 | **Sin e-mail de confirmación** |
| `MindTune acceso anticipado - profesionales de salud` | EMAIL (obligatorio), NOMBRE, PROFESION, LUGAR | #4 | **Sin e-mail de confirmación** |

Sus páginas propias no las va a ver nadie: de cada formulario solo se usa su dirección de envío,
que está pegada en `hugo.yaml` (`params.brevo.action_paciente` y `action_clinico`).

## Por qué no sale ningún correo

Tres cosas, las tres deliberadas: la confirmación de cada formulario está en **Sin e-mail de
confirmación**; **no** está activada la notificación al equipo; y el dominio **no** está
autenticado en esta cuenta, así que aunque alguien apretara "enviar campaña" por error, no
saldría con la cara de MindTune. Brevo solo acumula contactos.

## Cómo se ve un contacto que llega

Queda en su lista, con la fecha, y en su ficha se ven NOMBRE y —si es clínico— PROFESION y
LUGAR. En el historial del contacto dice por cuál formulario entró. Para bajarlo a Excel:
la lista → menú de la derecha → exportar.

## Probado de punta a punta

Se enviaron dos inscripciones de prueba y cada una cayó en su lista, con sus campos:

- `hayo.bk+prueba.paciente@gmail.com` → lista #3
- `hayo.bk+prueba.clinico@gmail.com` → lista #4, con profesión y lugar

**Bórralos cuando quieras** (Contactos → seleccionar → eliminar). Los dejé para que puedas
verlos.

## Lo que falta para el día en que sí quieras escribirle a la lista

1. **Sacar `mindtune.cl` de la cuenta vieja de Brevo** (la de LabONCE), donde hoy está
   autenticado. Mientras siga ahí, esa cuenta puede enviar correos como MindTune.
2. **Autenticarlo en esta cuenta:** *Senders, Domains & Dedicated IPs → Domains → Add a domain*
   → `mindtune.cl`. Los tres registros (TXT del código Brevo, DKIM, DMARC) van a Cloudflare →
   DNS → Records, con el **proxy en gris**, **sin tocar los MX** (ahí vive el Email Routing).
   Los registros `brevo1/brevo2._domainkey` y el `brevo-code` que ya están en el DNS son de la
   cuenta vieja: se reemplazan por los nuevos en ese momento.
3. **Crear el remitente** `MindTune <contacto@mindtune.cl>`.
4. **Cambiar la confirmación a doble opt-in** en los dos formularios, si para entonces te
   acomoda. Con la Ley 21.719 vigente es la posición más cómoda.
5. Brevo pone solo el enlace de desuscripción en cada campaña. No lo saques.

## Un par de cosas que conviene tener en mente

- **La lista se enfría.** Alguien que se inscribió en septiembre y recibe el primer correo en
  marzo ya no se acuerda de qué se trataba. Cuando esto empiece a juntar gente de verdad, vale
  la pena mandar algo breve cada tanto.
- **Segmenta por `PROFESION`.** No le vas a escribir lo mismo a un otorrino que a un médico
  general que ve tinnitus de pasada.
- **Si cambias lo que pide el formulario**, hay que actualizar la sección 11 de
  `content/privacidad.md`, que hoy declara exactamente estos campos.
- La contraseña de esta cuenta conviene que sea larga: custodia una base de contactos de
  pacientes.
