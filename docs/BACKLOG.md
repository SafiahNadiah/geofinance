# Backlog — GeoFinance

Use this as the source for GitHub Issues + a GitHub Project board (columns:
Backlog / In Progress / Review / Done). Each Sprint below = one Milestone.

## Sprint 0 — Architecture, Repository, Backlog (current)

- [x] Define vision, mission, tech stack (this blueprint)
- [ ] Create GitHub repository `geofinance`
- [ ] Push initial folder structure (frontend/backend/database/geoserver/docker/docs/architecture)
- [ ] Add README.md, architecture.md, BACKLOG.md
- [ ] Set up branch protection on `main` (require PR review, no direct push)
- [ ] Create GitHub Project board with 11 sprint milestones
- [ ] Resolve "Open Decisions" in architecture.md (REST vs GraphQL, auth strategy, vector DB, monorepo vs polyrepo, hosting target)
- [ ] Add `.gitignore`, `LICENSE`, `CODEOWNERS` (optional)

## Sprint 1 — Docker, PostgreSQL, PostGIS, GeoServer

- [ ] `docker-compose.yml` with postgres (postgis/postgis image), geoserver, adminer
- [ ] Verify PostGIS extension enabled (`CREATE EXTENSION postgis;`)
- [ ] Initial DB schema migration tool chosen (e.g. Prisma / Knex / node-pg-migrate)
- [ ] GeoServer workspace + a test layer connected to PostGIS
- [ ] `docs/local-dev-setup.md` — one-command local bootstrap

## Sprint 2 — Interactive Map

- [ ] Next.js app scaffold (App Router, Tailwind)
- [ ] MapLibre/OpenLayers base map rendering
- [ ] Render a WMS layer from GeoServer on the map
- [ ] Basic pan/zoom/layer-toggle controls

## Sprint 3 — Authentication & Users

- [ ] User table + RBAC schema (roles: admin, analyst, viewer)
- [ ] Auth endpoints (register/login/refresh) in Node API
- [ ] Frontend auth flow + protected routes
- [ ] Role-gated UI elements

## Sprint 4 — Customer & Branch

- [ ] Customer CRUD (API + DB)
- [ ] Branch CRUD with geolocation field
- [ ] Branch markers on the map
- [ ] Customer-to-branch association

## Sprint 5 — Loan & Property

- [ ] Loan CRUD + status workflow
- [ ] Property CRUD with geometry (parcel/point)
- [ ] Loan-property-customer relationships
- [ ] Property boundaries rendered on map

## Sprint 6 — Spatial Analysis

- [ ] Spatial queries (radius search, intersects, nearest-neighbor) via PostGIS
- [ ] Risk scoring based on location (flood zone, crime data, etc. — define data source)
- [ ] Spatial search UI (draw radius / polygon, filter results)

## Sprint 7 — AI Assistant

- [ ] Choose vector DB, set up embeddings pipeline
- [ ] RAG over internal docs/business data
- [ ] AI Assistant chat endpoint + frontend widget
- [ ] Risk-analysis recommendations surfaced via AI

## Sprint 8 — Dashboard

- [ ] Aggregate metrics (loans by risk tier, branch performance, customer growth)
- [ ] Charts (recharts/chart.js) wired to real API data
- [ ] Exportable reports (CSV/PDF)

## Sprint 9 — Cloud Deployment

- [ ] Choose cloud provider (AWS/GCP/Azure)
- [ ] Containerize all services for production
- [ ] Manual first deploy (no IaC yet) to validate

## Sprint 10 — Terraform & CI/CD

- [ ] Terraform modules for infra (VPC, DB, K8s cluster or equivalent)
- [ ] GitHub Actions: lint/test/build on PR, deploy on merge to main
- [ ] Kubernetes manifests / Helm chart
- [ ] Documented rollback procedure

## Success Criteria (from blueprint)

- [ ] Enterprise-grade GitHub repository
- [ ] Complete documentation
- [ ] Cloud-ready deployment
- [ ] Interview-ready portfolio
- [ ] Strong foundation for Solution Architect career
