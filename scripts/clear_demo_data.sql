-- One-shot wipe of demo / sample data in RepuestosAuto (Render Postgres).
-- Safe for schema: does NOT drop tables or schema_migrations.
-- Run once in the Render dashboard → Postgres → Connect / Query (or psql).
-- After this, the app starts empty (no Toyota Corolla, no fake mantenimientos).

BEGIN;

DELETE FROM maintenance_records;

UPDATE vehicle_settings
SET
  current_odometer = 0,
  last_oil_change_km = 0,
  vehicle_label = 'Mi vehículo',
  updated_at = NOW();

COMMIT;

-- Optional check:
-- SELECT COUNT(*) AS mantenimientos FROM maintenance_records;
-- SELECT * FROM vehicle_settings;
