# RepuestosAuto

App web (español, sin login) para registrar mantenimiento y repuestos del vehículo, con recordatorio de cambio de aceite cada **7.000 km**.

## Stack

- **Backend:** Flask (MVC: `models` / `controllers` / `services` + templates)
- **DB:** PostgreSQL vía `DATABASE_URL` (Neon / Cursor Apps Postgres). Sin secreto → **SQLite** local en `data/repuestos.db`
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
| Sin `DATABASE_URL` | SQLite en `data/repuestos.db` (datos de ejemplo al primer arranque) |
| Con `DATABASE_URL` | PostgreSQL (Neon u otro). Migraciones en `migrations/*.sql` |

Para publicar en Cursor Apps: `cursor-app.json` declara `"database": "postgres"`. La plataforma inyecta `DATABASE_URL`; **no** hace falta (ni se debe) bindear ese secreto a mano.

Migración opcional con Postgres:

```bash
DATABASE_URL="postgresql://..." python scripts/migrate.py
```

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

## Publish (Cursor)

1. Arrancar el servidor local.
2. `publish-app` con `project_dir` `.` y `preview_url` `http://127.0.0.1:5000`.
3. Confirmar en el diálogo de Cursor (slug sugerido: `repuestos-auto`).
