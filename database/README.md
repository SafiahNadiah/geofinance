# Database migrations

GeoFinance schema migrations live in `database/migrations/` and are managed with `node-pg-migrate`.

## Prerequisites

1. Docker is running.
2. The PostgreSQL/PostGIS container is up from repo root:

   docker compose up -d postgres

## Run migrations

From `database/`:

- Apply all pending migrations:

  npm run migrate:up

- Roll back one migration:

  npm run migrate:down

These scripts run `node-pg-migrate` inside a temporary `node:20-alpine`
container on the same Docker network as `geofinance-postgres`.

## Verify tables

From repo root:

- List all tables in the `geofinance` database:

  docker exec -it geofinance-postgres psql -U postgres -d geofinance -c "\\dt"

Expected tables after Sprint 2 Day 8-9 migrations:

- `branches`
- `customers`
- `properties`
- `loans`
- `risk_zones`
- `loan_risk_assessments`
- `roles`
- `users`
- `audit_logs`
