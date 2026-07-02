#!/usr/bin/env bash
# Loads generate_seed_data.py output into a PostgreSQL/PostGIS database.
# Usage: DATABASE_URL=postgres://user:pass@localhost:5432/geofinance ./import.sh

set -e
DB_URL="${DATABASE_URL:-postgres://postgres:postgres@localhost:5432/geofinance}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Creating schema..."
psql "$DB_URL" -f "$DIR/schema.sql"

echo "Loading CSVs..."
psql "$DB_URL" -c "\copy branches(id,code,name,type,address,geom,opened_date,staff_count) FROM '$DIR/output/branches.csv' WITH (FORMAT csv, HEADER true)"
psql "$DB_URL" -c "\copy customers(id,code,full_name,email,phone,occupation,monthly_income_myr,home_geom,nearest_branch_id,customer_since) FROM '$DIR/output/customers.csv' WITH (FORMAT csv, HEADER true)"
psql "$DB_URL" -c "\copy properties(id,code,owner_customer_id,type,address,geom,market_value_myr,floor_area_sqft,year_built) FROM '$DIR/output/properties.csv' WITH (FORMAT csv, HEADER true)"
psql "$DB_URL" -c "\copy loans(id,code,customer_id,property_id,branch_id,loan_type,principal_amount_myr,interest_rate_pct,tenure_years,status,application_date) FROM '$DIR/output/loans.csv' WITH (FORMAT csv, HEADER true)"

echo "Loading risk zones from GeoJSON via Python..."
DATABASE_URL="$DB_URL" python "$DIR/load_risk_zones.py"

echo "Done. Row counts:"
psql "$DB_URL" -c "SELECT 'branches' t, count(*) FROM branches
UNION ALL SELECT 'customers', count(*) FROM customers
UNION ALL SELECT 'properties', count(*) FROM properties
UNION ALL SELECT 'loans', count(*) FROM loans
UNION ALL SELECT 'risk_zones', count(*) FROM risk_zones;"
