-- GeoFinance — schema for seed data (Sprint 1)
-- Run after: CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS branches (
    branch_id       VARCHAR(10) PRIMARY KEY,
    name            VARCHAR(120) NOT NULL,
    type            VARCHAR(40),
    address         TEXT,
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    geom            GEOMETRY(Point, 4326),
    opened_date     DATE,
    staff_count     INTEGER
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id         VARCHAR(12) PRIMARY KEY,
    full_name           VARCHAR(120) NOT NULL,
    ic_number_fake       VARCHAR(20),
    email               VARCHAR(120),
    phone               VARCHAR(20),
    occupation          VARCHAR(60),
    monthly_income_myr   NUMERIC(12,2),
    home_latitude        DOUBLE PRECISION,
    home_longitude        DOUBLE PRECISION,
    geom                GEOMETRY(Point, 4326),
    nearest_branch_id     VARCHAR(10) REFERENCES branches(branch_id),
    customer_since        DATE
);

CREATE TABLE IF NOT EXISTS properties (
    property_id         VARCHAR(12) PRIMARY KEY,
    owner_customer_id     VARCHAR(12) REFERENCES customers(customer_id),
    type                VARCHAR(40),
    address             TEXT,
    latitude            DOUBLE PRECISION,
    longitude           DOUBLE PRECISION,
    geom                GEOMETRY(Point, 4326),
    market_value_myr     NUMERIC(14,2),
    floor_area_sqft       INTEGER,
    year_built           INTEGER
);

CREATE TABLE IF NOT EXISTS risk_zones (
    zone_id       VARCHAR(10) PRIMARY KEY,
    name          VARCHAR(120),
    hazard_type   VARCHAR(30),
    severity      VARCHAR(10),
    geom          GEOMETRY(Polygon, 4326)
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id                     VARCHAR(12) PRIMARY KEY,
    customer_id                  VARCHAR(12) REFERENCES customers(customer_id),
    property_id                  VARCHAR(12) REFERENCES properties(property_id),
    branch_id                    VARCHAR(10) REFERENCES branches(branch_id),
    loan_type                    VARCHAR(40),
    principal_amount_myr          NUMERIC(14,2),
    interest_rate_pct             NUMERIC(5,2),
    tenure_years                 INTEGER,
    status                       VARCHAR(20),
    application_date              DATE,
    nearest_risk_zone             VARCHAR(120),
    nearest_risk_zone_hazard       VARCHAR(30),
    distance_to_risk_zone_km        NUMERIC(6,2),
    risk_score                   NUMERIC(5,1),
    risk_tier                    VARCHAR(10)
);

-- Spatial indexes
CREATE INDEX IF NOT EXISTS idx_branches_geom ON branches USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_customers_geom ON customers USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_properties_geom ON properties USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_risk_zones_geom ON risk_zones USING GIST (geom);

-- After loading the CSVs with \copy (see import.sh), populate geom columns:
-- UPDATE branches SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
-- UPDATE customers SET geom = ST_SetSRID(ST_MakePoint(home_longitude, home_latitude), 4326);
-- UPDATE properties SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
-- risk_zones.geom is loaded separately from risk_zones.geojson (see import.sh)
