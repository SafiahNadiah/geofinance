-- GeoFinance — schema for seed data
-- Run after: CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS branches (
    id              UUID PRIMARY KEY,
    code            VARCHAR(10) UNIQUE NOT NULL,
    name            VARCHAR(120) NOT NULL,
    type            VARCHAR(40),
    address         TEXT,
    geom            GEOMETRY(Point, 4326),
    opened_date     DATE,
    staff_count     INTEGER
);

CREATE TABLE IF NOT EXISTS customers (
    id                  UUID PRIMARY KEY,
    code                VARCHAR(12) UNIQUE NOT NULL,
    full_name           VARCHAR(120) NOT NULL,
    email               VARCHAR(120),
    phone               VARCHAR(20),
    occupation          VARCHAR(60),
    monthly_income_myr  NUMERIC(12,2),
    home_geom           GEOMETRY(Point, 4326),
    nearest_branch_id   UUID REFERENCES branches(id),
    customer_since      DATE
);

CREATE TABLE IF NOT EXISTS properties (
    id                 UUID PRIMARY KEY,
    code               VARCHAR(12) UNIQUE NOT NULL,
    owner_customer_id  UUID REFERENCES customers(id),
    type                VARCHAR(40),
    address             TEXT,
    geom                GEOMETRY(Point, 4326),
    market_value_myr    NUMERIC(14,2),
    floor_area_sqft     INTEGER,
    year_built          INTEGER
);

CREATE TABLE IF NOT EXISTS risk_zones (
    id            UUID PRIMARY KEY,
    code          VARCHAR(10) UNIQUE NOT NULL,
    name          VARCHAR(120),
    hazard_type   VARCHAR(30),
    severity      VARCHAR(10),
    geom          GEOMETRY(Polygon, 4326)
);

CREATE TABLE IF NOT EXISTS loans (
    id                    UUID PRIMARY KEY,
    code                  VARCHAR(12) UNIQUE NOT NULL,
    customer_id           UUID REFERENCES customers(id),
    property_id           UUID REFERENCES properties(id),
    branch_id             UUID REFERENCES branches(id),
    loan_type             VARCHAR(40),
    principal_amount_myr  NUMERIC(14,2),
    interest_rate_pct     NUMERIC(5,2),
    tenure_years          INTEGER,
    status                VARCHAR(20),
    application_date      DATE
);

-- Spatial indexes
CREATE INDEX IF NOT EXISTS idx_branches_geom ON branches USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_customers_geom ON customers USING GIST (home_geom);
CREATE INDEX IF NOT EXISTS idx_properties_geom ON properties USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_risk_zones_geom ON risk_zones USING GIST (geom);

-- risk_zones.geom is loaded separately from risk_zones.geojson (see import.sh)
