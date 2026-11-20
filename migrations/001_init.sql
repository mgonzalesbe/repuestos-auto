CREATE TABLE IF NOT EXISTS vehicle_settings (
    id SERIAL PRIMARY KEY,
    current_odometer INTEGER NOT NULL DEFAULT 0,
    last_oil_change_km INTEGER NOT NULL DEFAULT 0,
    vehicle_label TEXT NOT NULL DEFAULT 'Mi vehículo',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS maintenance_records (
    id SERIAL PRIMARY KEY,
    service_date DATE NOT NULL,
    part_type TEXT NOT NULL,
    parts_price NUMERIC(12, 2) NOT NULL DEFAULT 0,
    labor_price NUMERIC(12, 2) NOT NULL DEFAULT 0,
    is_original BOOLEAN NOT NULL DEFAULT TRUE,
    next_change_date DATE,
    odometer_km INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_maintenance_service_date
    ON maintenance_records (service_date DESC);
