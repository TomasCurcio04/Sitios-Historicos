-- Migración para convertir latitude/longitude a PostGIS
-- Ejecutar después de agregar la columna location

-- 1. Agregar columna location
ALTER TABLE site ADD COLUMN location geography(POINT, 4326);

-- 2. Migrar datos existentes
UPDATE site 
SET location = ST_GeogFromText('POINT(' || longitude || ' ' || latitude || ')')
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- 3. Crear índice espacial
CREATE INDEX idx_site_location ON site USING GIST (location);

-- 4. Opcional: Eliminar columnas antiguas después de verificar
-- ALTER TABLE site DROP COLUMN latitude;
-- ALTER TABLE site DROP COLUMN longitude;