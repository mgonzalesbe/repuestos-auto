# RepuestosAuto

App web (español, sin login) para registrar mantenimiento y repuestos del vehículo, con recordatorio de cambio de aceite cada **7.000 km**.

## Stack

- **Backend:** Flask (MVC: `models` / `controllers` / `services` + templates)
- **DB:** PostgreSQL vía `DATABASE_URL` (**Render Postgres** en producción). Sin secreto → **SQLite** local en `data/repuestos.db`. Arranca vacío (sin seed).
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
| Con `DATABASE_URL` | PostgreSQL (Render u otro). Migraciones en `migrations/*.sql` |

Migraciones (idempotentes):

```bash
DATABASE_URL="postgresql://..." python scripts/migrate.py
```

### Borrar datos demo existentes (una sola vez)

Si la DB de Render aún tiene el Toyota Corolla / mantenimientos de ejemplo (de un deploy anterior con seed), borrarlos **una vez**:

**Opción A — SQL en el dashboard de Render**

1. [dashboard.render.com](https://dashboard.render.com) → servicio **Postgres** `repuestos-auto-db` → **Connect** / query o `psql`.
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

## Deploy en Render (público, recomendado)

Blueprint en `render.yaml`: web service free + Postgres free, `gunicorn` en `0.0.0.0:$PORT`, migraciones en el `buildCommand`, `DATABASE_URL` inyectada desde la DB del Blueprint (`postgres://` se normaliza a `postgresql+psycopg://` en `app/config.py`).

### Una sola vez en el dashboard

1. Creá cuenta en [render.com](https://render.com) e iniciá sesión con GitHub.
2. **New → Blueprint** → conectá el repo `mgonzalesbe/repuestos-auto` (rama `main`).
3. Revisá el preview del Blueprint (`repuestos-auto` + `repuestos-auto-db`) → **Apply**.
4. Cuando el deploy termine, la URL pública es `https://repuestos-auto.onrender.com` (o la que muestre el servicio).

No hace falta setear `DATABASE_URL` a mano: el Blueprint la enlaza. `SECRET_KEY` se genera sola. Free web se duerme tras inactividad (~15 s cold start).

## Publish (Cursor Apps — opcional / privado)

1. Arrancar el servidor local.
2. `publish-app` con `project_dir` `.` y `preview_url` `http://127.0.0.1:5000`.
3. Confirmar en el diálogo de Cursor (slug sugerido: `repuestos-auto`).
