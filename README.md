# RepuestosAuto

App web (español, sin login) para registrar mantenimiento y repuestos del vehículo, con recordatorio de cambio de aceite cada **7.000 km**.

## Stack

- **Backend:** Flask (MVC: `models` / `controllers` / `services` + templates)
- **DB:** PostgreSQL vía `DATABASE_URL` (**Neon** en producción). Sin secreto → **SQLite** local en `data/repuestos.db`. Arranca vacío (sin seed).
- **Frontend:** plantillas Jinja + CSS/JS estáticos

## Ejecutar en local

```bash
cd /agent   # o la carpeta del proyecto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/migrate.py
python wsgi.py
```

Abre [http://127.0.0.1:5000](http://127.0.0.1:5000).

Producción local:

```bash
gunicorn -b 127.0.0.1:5000 wsgi:app
```

## Base de datos

| Entorno | Comportamiento |
|--------|----------------|
| Sin `DATABASE_URL` | SQLite en `data/repuestos.db` (vacío; sin seed) |
| Con `DATABASE_URL` | PostgreSQL (Neon u otro). Migraciones en `migrations/*.sql` |

Migraciones (idempotentes):

```bash
DATABASE_URL="postgresql://..." python scripts/migrate.py
```

`postgres://` y `postgresql://` se normalizan a `postgresql+psycopg://` en `app/config.py`.

### Borrar datos demo existentes (una sola vez)

Si la DB aún tiene el Toyota Corolla / mantenimientos de ejemplo (de un deploy anterior con seed), borrarlos **una vez**:

**Opción A — SQL en Neon**

1. [console.neon.tech](https://console.neon.tech) → tu proyecto → **SQL Editor**.
2. Ejecutar el contenido de `scripts/clear_demo_data.sql` (DELETE de `maintenance_records` + reset de `vehicle_settings`).

**Opción B — script (local o Shell de Render)**

```bash
CONFIRM=YES python scripts/clear_demo_data.py
```

El script exige `CONFIRM=YES` y **no** se corre en el deploy. No elimina tablas ni migraciones.

Para publicar en Cursor Apps (opcional): `cursor-app.json` declara `"database": "postgres"`. **No** bindear `DATABASE_URL` a mano en Cursor.

## Rutas principales

| Ruta | Función |
|------|---------|
| `GET /` | Panel: recordatorio de aceite + resumen + últimos registros |
| `POST /odometro` | Actualizar odómetro / último cambio de aceite |
| `GET/POST /mantenimientos/` | Listado CRUD |
| `GET/POST /mantenimientos/nuevo` | Crear |
| `GET/POST /mantenimientos/<id>/editar` | Editar |
| `POST /mantenimientos/<id>/eliminar` | Eliminar |

## Campos de mantenimiento

Fecha, tipo de pieza/mantenimiento, precio de herramientas/repuestos, precio de mano de obra, si es original (sí/no), fecha esperada del próximo cambio (+ odómetro y notas opcionales).

## Deploy en Render + Neon (público, recomendado)

Blueprint en `render.yaml`: **solo** web service free (`gunicorn` en `0.0.0.0:$PORT`). La DB es **Neon** (externa). Pegá `DATABASE_URL` en el dashboard de Render. Migraciones corren en el `buildCommand`.

### Neon — crear la base (una sola vez)

1. Abrí [console.neon.tech](https://console.neon.tech) → **Sign up** (GitHub está bien).
2. **Create a project** (Free plan). Región cercana (p. ej. US West / Oregon si el web está en Oregon).
3. Cuando el proyecto esté listo → **Dashboard** → **Connection details**.
4. Copiá el connection string **pooled** (host tipo `….pooler.neon.tech`, a veces etiquetado *Pooled connection*).  
   Ejemplo de forma: `postgresql://USER:PASSWORD@ep-….pooler.neon.tech/neondb?sslmode=require`  
   (La app convierte `postgres://` / `postgresql://` a `postgresql+psycopg://` sola.)

### Render — pegar `DATABASE_URL` y quitar la DB vieja

1. [dashboard.render.com](https://dashboard.render.com) → servicio web **`repuestos-auto`**.
2. **Environment** → agregá o editá:
   - Key: `DATABASE_URL`
   - Value: la URI pooled de Neon (pegá tal cual)
3. **Save Changes** (dispara redeploy; el `buildCommand` corre `python scripts/migrate.py`).
4. Si todavía existe el Postgres del Blueprint **`repuestos-auto-db`**:
   - Abrí ese servicio Postgres → **Settings** → **Delete Database** (o desenlazalo del web).  
   - Confirmá que el web **ya no** tenga un link `fromDatabase` a Render Postgres; solo la env var manual.
5. Cuando el deploy esté verde: https://repuestos-auto.onrender.com

### Si hace falta wipe de seed

Tras migrar a Neon (DB nueva = vacía). Si reutilizás una DB con demos: Neon **SQL Editor** → `scripts/clear_demo_data.sql`, o `CONFIRM=YES python scripts/clear_demo_data.py` con `DATABASE_URL` apuntando a Neon.

### Blueprint desde cero (opcional)

1. Render → **New → Blueprint** → repo `mgonzalesbe/repuestos-auto` (rama `main`).
2. Apply. El Blueprint **no** crea Postgres.
3. Antes o justo después del primer deploy: pegá `DATABASE_URL` (Neon) en Environment. Sin eso el build/arranque falla a propósito.

`SECRET_KEY` se genera sola. Free web se duerme tras inactividad (~15–50 s cold start). Neon Free también puede suspender compute tras inactividad.

## Publish (Cursor Apps — opcional / privado)

1. Arrancar el servidor local.
2. `publish-app` con `project_dir` `.` y `preview_url` `http://127.0.0.1:5000`.
3. Confirmar en el diálogo de Cursor (slug sugerido: `repuestos-auto`).
