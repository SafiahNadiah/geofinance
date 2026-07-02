#!/usr/bin/env bash
# Loads generate_seed_data.py output into a PostgreSQL/PostGIS database.
# Usage: DATABASE_URL=postgres://user:pass@localhost:5432/geofinance ./import.sh

set -e
DB_URL="${DATABASE_URL:-postgres://postgres:postgres@localhost:5432/geofinance}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Creating schema..."
psql "$DB_URL" -f "$DIR/schema.sql"

echo "Loading CSVs..."
psql "$DB_URL" -c "\copy branches(branch_id,name,type,address,latitude,longitude,opened_date,staff_count) FROM '$DIR/output/branches.csv' WITH (FORMAT csv, HEADER true)"
psql "$DB_URL" -c "\copy customers(customer_id,full_name,ic_number_fake,email,phone,occupation,monthly_income_myr,home_latitude,home_longitude,nearest_branch_id,customer_since) FROM '$DIR/output/customers.csv' WITH (FORMAT csv, HEADER true)"
psql "$DB_URL" -c "\copy properties(property_id,owner_customer_id,type,address,latitude,longitude,market_value_myr,floor_area_sqft,year_built) FROM '$DIR/output/properties.csv' WITH (FORMAT csv, HEADER true)"
psql "$DB_URL" -c "\copy loans(loan_id,customer_id,property_id,branch_id,loan_type,principal_amount_myr,interest_rate_pct,tenure_years,status,application_date,nearest_risk_zone,nearest_risk_zone_hazard,distance_to_risk_zone_km,risk_score,risk_tier) FROM '$DIR/output/loans.csv' WITH (FORMAT csv, HEADER true)"

echo "Populating geometry columns..."
psql "$DB_URL" -c "UPDATE branches SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);"
psql "$DB_URL" -c "UPDATE customers SET geom = ST_SetSRID(ST_MakePoint(home_longitude, home_latitude), 4326);"
psql "$DB_URL" -c "UPDATE properties SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);"

echo "Loading risk zones from GeoJSON (requires ogr2ogr / GDAL)..."
ogr2ogr -f "PostgreSQL" PG:"$DB_URL" "$DIR/output/risk_zones.geojson" \
  -nln risk_zones_import -overwrite

psql "$DB_URL" -c "
INSERT INTO risk_zones (zone_id, name, hazard_type, severity, geom)
SELECT zone_id, name, hazard_type, severity, wkb_geometry
FROM risk_zones_import
ON CONFLICT (zone_id) DO NOTHING;
DROP TABLE IF EXISTS risk_zones_import;
"

echo "Done. Row counts:"
psql "$DB_URL" -c "SELECT 'branches' t, count(*) FROM branches
UNION ALL SELECT 'customers', count(*) FROM customers
UNION ALL SELECT 'properties', count(*) FROM properties
UNION ALL SELECT 'loans', count(*) FROM loans
UNION ALL SELECT 'risk_zones', count(*) FROM risk_zones;"
