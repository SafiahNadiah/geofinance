# SPRINT_CHECKLIST.md — GeoFinance 90-Day Execution Checklist

**Companion to:** `ROADMAP.md` (this file breaks each of the 12 weekly
sprints into day-by-day actionable checkboxes)
**How to use:** Work top to bottom. Tick a box only when it's actually
done and demoable — not "code written but untested." At the end of
each sprint, do the Definition of Done check before moving on; do not
start the next sprint with an unfinished DoD.

---

## Sprint 1 — Docker & Project Scaffold (Days 1–7)

**Goal:** `docker compose up` boots the full stack from a cold clone.

**Day 1–2: Docker foundation**
- [ ] Write `docker-compose.yml` with 3 services: `postgres` (image `postgis/postgis:16-3.4`), `backend`, `frontend`
- [ ] Add `.env.example` at root with `DATABASE_URL`, `JWT_SECRET`, `PORT` placeholders
- [ ] Confirm `postgres` container starts and `psql` connects manually
- [ ] Add a named volume so Postgres data persists across `docker compose down`

**Day 3–4: Backend scaffold**
- [ ] `npm init` backend with TypeScript, Express
- [ ] Create folder skeleton per `02_SRS.md §2.3`: `domain/`, `application/`, `infrastructure/`, `interfaces/`, `shared/`
- [ ] Add `tsconfig.json` with strict mode on (per `04_AGENTS.md §4`)
- [ ] Implement `GET /health` returning `{ status: "ok" }`
- [ ] Add `Dockerfile` for backend, wire into `docker-compose.yml`

**Day 5–6: Frontend scaffold**
- [ ] `create-next-app` with TypeScript + Tailwind CSS
- [ ] Create folder skeleton: `app/`, `components/`, `lib/`, `types/`
- [ ] Add a placeholder landing page confirming the app boots
- [ ] Add `Dockerfile` for frontend, wire into `docker-compose.yml`

**Day 7: Integration & review**
- [ ] `docker compose up` from a clean `docker compose down -v` succeeds with zero manual steps
- [ ] `curl localhost:<backend-port>/health` returns `200`
- [ ] Frontend reachable in browser
- [ ] Commit + push, tag `v0.1.0-setup`

**Definition of Done:**
- [ ] Fresh clone → `docker compose up` → both health checks pass, no manual DB/env fixing needed

---

## Sprint 2 — PostGIS, GeoServer & Seed Data (Days 8–14)

**Goal:** Database schema live, GeoServer serving one layer, seed data loaded.

**Day 8–9: Schema migrations**
- [ ] Choose migration tool (per `02_SRS.md` open decision) and install
- [ ] Migration 0001: `CREATE EXTENSION IF NOT EXISTS postgis;`
- [ ] Migrations for all 8 tables from `03_DATABASE.md §2` (branches, customers, properties, loans, risk_zones, loan_risk_assessments, users, roles, audit_logs)
- [ ] Add GiST indexes on every geometry column in the same migration that creates the table (`03_DATABASE.md §4`)
- [ ] Run migrations against the Dockerized Postgres, confirm all tables exist

**Day 10: Seed data UUID update**
- [ ] Update `generate_seed_data.py` to generate/attach `uuid4()` as `id`, keep existing string as `code`
- [ ] Re-run generator, confirm output CSVs have both `id` and `code` columns
- [ ] Update `import.sh` / `schema.sql` column lists to match

**Day 11: Load seed data**
- [ ] Run `import.sh` against the Dockerized DB
- [ ] Verify row counts match `database/seed-data/README.md` (18 branches, 2000 customers, 1200 properties, 900 loans, 12 risk zones)
- [ ] Spot-check 3 random rows per table for correct geometry (`ST_AsText(geom)`)

**Day 12–13: GeoServer**
- [ ] Add GeoServer container to `docker-compose.yml`
- [ ] Connect GeoServer to Postgres as a datastore
- [ ] Publish `branches` as a WMS layer
- [ ] Confirm the layer renders in GeoServer's own preview

**Day 14: Review**
- [ ] All containers boot together via `docker compose up`
- [ ] Commit + push, tag `v0.1.1-data`

**Definition of Done:**
- [ ] `SELECT postgis_version();` succeeds; seed row counts correct; GeoServer preview shows branch points on a map

---

## Sprint 3 — Authentication & RBAC (Days 15–21)

**Goal:** Working login with role-based access enforced server-side.

**Day 15–16: Users/roles data + password handling**
- [ ] Seed 3 demo users (one per role: admin/analyst/viewer) with bcrypt-hashed passwords (cost ≥ 12)
- [ ] Implement `roles` lookup with `permissions` JSONB per `03_DATABASE.md §3.8`

**Day 17–18: Auth endpoints**
- [ ] `POST /api/v1/auth/login` — validates credentials, issues access token (15min JWT) + refresh token (httpOnly cookie)
- [ ] `POST /api/v1/auth/refresh` — rotates refresh token
- [ ] Error responses follow RFC 7807 format (`02_SRS.md §4.1`)

**Day 19: RBAC middleware**
- [ ] Middleware that decodes JWT, attaches `role` to request context
- [ ] Middleware that rejects a request if role isn't in an endpoint's allowed list
- [ ] Apply to one test-protected endpoint, confirm 401/403 behave correctly

**Day 20: Frontend auth**
- [ ] Login page (email/password form)
- [ ] Store access token in memory (not localStorage), refresh flow wired
- [ ] Protected route wrapper redirects unauthenticated users to `/login`

**Day 21: Review**
- [ ] Manually test all 3 roles against the protected test endpoint
- [ ] Commit + push, tag `v0.2.0-auth`

**Definition of Done:**
- [ ] Each of the 3 demo users can log in; each role sees correctly gated access on at least one endpoint

---

## Sprint 4 — Customer Module (Days 22–28)

**Goal:** First full vertical slice — the template for Sprints 5–7.

**Day 22: Domain layer**
- [ ] `Customer` entity in `domain/` with invariants (e.g. valid email format, income >= 0)
- [ ] `CustomerRepository` interface in `domain/`

**Day 23: Infrastructure layer**
- [ ] `CustomerRepository` implementation in `infrastructure/repositories/` (Postgres queries)
- [ ] Repository excludes soft-deleted rows by default (`deleted_at IS NULL`)

**Day 24: Application layer**
- [ ] `CustomerService` with `create`, `list`, `getById`, `update`, `softDelete` methods
- [ ] Request/response DTOs in `application/dtos/`

**Day 25: Interface layer**
- [ ] `CustomerController` — thin, maps request → DTO → service call → response
- [ ] Routes registered under `/api/v1/customers`, protected by auth middleware
- [ ] Input validation at controller boundary

**Day 26–27: Frontend**
- [ ] Customer list page (paginated table)
- [ ] Customer create/edit form
- [ ] Customer detail view
- [ ] Delete confirmation flow (soft delete)

**Day 28: Tests & review**
- [ ] Unit tests for `CustomerService` (repository mocked)
- [ ] Integration test for `CustomerRepository` against test DB
- [ ] Manual end-to-end: create → view → edit → delete through the UI
- [ ] Commit + push, tag `v0.3.0-customer`

**Definition of Done:**
- [ ] Full CRUD works end-to-end via UI with no console errors; this pattern is documented as the template to copy for Sprints 5–7

---

## Sprint 5 — Branch Module (Days 29–35)

**Goal:** Second vertical slice, first with map-based geometry input.

**Day 29–30: Backend (copy Customer pattern)**
- [ ] `Branch` entity, repository interface + implementation, service, DTOs, controller, routes under `/api/v1/branches`

**Day 31–33: Frontend + geometry picker**
- [ ] Branch list/detail/create/edit UI
- [ ] Map-based location picker component (click to set point) — reusable, will be needed again in Sprint 6
- [ ] Wire picker output to `geom` field on save

**Day 34: Tests**
- [ ] Unit + integration tests mirroring Sprint 4
- [ ] Verify saved branch geometry is valid `GEOMETRY(Point,4326)` via `ST_AsText`

**Day 35: Review**
- [ ] End-to-end manual test: create branch with real coordinates, confirm on map
- [ ] Commit + push, tag `v0.4.0-branch`

**Definition of Done:**
- [ ] Branch created via UI has a verifiable, correct point geometry in the DB

---

## Sprint 6 — Property Module (Days 36–42)

**Goal:** Third vertical slice, first with a required foreign-key relationship.

**Day 36–37: Backend**
- [ ] `Property` entity + repository + service + DTOs + controller under `/api/v1/properties`
- [ ] `owner_customer_id` FK validated — reject if customer doesn't exist

**Day 38–40: Frontend**
- [ ] Property list/detail/create/edit UI
- [ ] Owner selection (searchable customer dropdown)
- [ ] Reuse the location picker from Sprint 5

**Day 41: Tests**
- [ ] Test: creating a property with a non-existent `owner_customer_id` returns a validation error, not a DB constraint crash
- [ ] Unit + integration tests mirroring prior sprints

**Day 42: Review**
- [ ] Commit + push, tag `v0.5.0-property`

**Definition of Done:**
- [ ] Property correctly links to an existing customer; invalid owner is rejected with a clean error, not a 500

---

## Sprint 7 — Loan Module & Risk Scoring (Days 43–49)

**Goal:** Fourth vertical slice + the first domain-specific algorithm (risk scoring).

**Day 43–44: Loan CRUD**
- [ ] `Loan` entity + repository + service + DTOs + controller under `/api/v1/loans`
- [ ] FKs to customer, property (nullable), branch — all validated

**Day 45–46: Risk scoring service**
- [ ] Port the risk formula logic from `generate_seed_data.py` into a proper `RiskScoringService`
- [ ] On loan create/update, compute distance to nearest `risk_zones` polygon via `ST_Distance`/`ST_DWithin`
- [ ] Write result to `loan_risk_assessments` with `score_breakdown` JSONB (include a `schema_version` key per `03_DATABASE.md §8`)
- [ ] `GET /api/v1/loans/:id/risk-score` endpoint

**Day 47–48: Frontend**
- [ ] Loan list/detail/create/edit UI
- [ ] Risk tier badge (color-coded) on loan detail and list
- [ ] Risk breakdown display on loan detail (from `score_breakdown`)

**Day 49: Tests & review**
- [ ] Test: risk score recalculates correctly for a known fixture (property near a known risk zone)
- [ ] Commit + push, tag `v0.6.0-loan-risk`

**Definition of Done:**
- [ ] Creating a loan auto-computes and persists a risk tier that's visible on the loan detail page and matches manual calculation for a test case

---

## Sprint 8 — Interactive Map (Days 50–56)

**Goal:** First real GIS payoff — all entities visible on one map.

**Day 50–51: Map foundation**
- [ ] Install MapLibre GL (or OpenLayers) on frontend
- [ ] `/map` page with base map centered on Klang Valley
- [ ] Consume GeoServer WMS layer for branches (from Sprint 2)

**Day 52–53: Entity markers**
- [ ] Add property markers (fetched from API, not GeoServer, to prove both paths work)
- [ ] Color-code markers by risk tier (from Sprint 7 data) where applicable
- [ ] Click-to-popup showing entity name + key fields + link to detail page

**Day 54: Layer controls**
- [ ] Toggle control for at least 2 layers (branches, properties)
- [ ] Basic zoom/pan controls confirmed working

**Day 55: Performance check**
- [ ] Measure map load time against reference dataset — target < 2s
- [ ] If slow, check marker clustering is needed (add if so)

**Day 56: Review**
- [ ] Commit + push, tag `v0.7.0-map`

**Definition of Done:**
- [ ] `/map` loads under 2s, shows branches + properties, marker click shows correct data, at least 2 layers toggleable

---

## Sprint 9 — Spatial Search (Days 57–63)

**Goal:** Ad-hoc spatial querying, backend + UI.

**Day 57–58: Backend spatial search endpoint**
- [ ] `GET /api/v1/spatial/search` — supports entity type, radius (`ST_DWithin`), and polygon (`ST_Within`) params
- [ ] `EXPLAIN ANALYZE` confirms the GiST index is used (per `03_DATABASE.md §4`) — screenshot/log this for the record
- [ ] Pagination on results per `02_SRS.md §4.1`

**Day 59–60: Frontend draw-search UI**
- [ ] Add radius-draw and polygon-draw tools to the map (reuse Sprint 8 map)
- [ ] Wire drawn shape to the search API call
- [ ] Display results as both a highlighted map layer and a results list

**Day 61: Export**
- [ ] CSV/GeoJSON export of search results (stretch — skip if time-constrained, not a hard requirement)

**Day 62: Tests**
- [ ] Test against a known fixture: a point + radius that should return exactly N known records

**Day 63: Review**
- [ ] Commit + push, tag `v0.8.0-spatial-search`

**Definition of Done:**
- [ ] Radius and polygon search both return correct, verified results; GiST index usage confirmed

---

## Sprint 10 — Risk Analysis View (Days 64–70)

**Goal:** Dedicated risk analysis screen tying together Sprint 7 (scoring) and Sprint 8–9 (map/spatial).

**Day 64–65: Risk zone overlay**
- [ ] Render `risk_zones` polygons on the map, color-coded by severity
- [ ] `/risk-analysis` page as a focused view (map + filters, no unrelated clutter)

**Day 66–67: Filtering**
- [ ] Filter loans by `risk_tier` (multi-select) — updates map markers and a result list simultaneously
- [ ] Filter by region (reuse polygon-draw from Sprint 9, or predefined branch-radius regions)

**Day 68: Portfolio summary**
- [ ] Summary panel: count of loans per risk tier for the current filter
- [ ] Confirm summary count matches the map/list result count exactly

**Day 69: Tests**
- [ ] Test matching `01_PRD.md` US-02 acceptance criteria: filtering by tier + region narrows results correctly

**Day 70: Review**
- [ ] Commit + push, tag `v0.85.0-risk-analysis`

**Definition of Done:**
- [ ] Filtering by "high" risk tier narrows both the map and the summary count correctly and consistently

---

## Sprint 11 — Dashboard (Days 71–77)

**Goal:** Default post-login screen aggregating everything built so far.

**Day 71–72: Metrics API**
- [ ] `GET /api/v1/dashboard/summary` — aggregate counts (loans by tier, customers, branches, total portfolio value)
- [ ] Ensure this is a real aggregate query, not client-side summing of a full unpaginated fetch

**Day 73–74: Charts**
- [ ] Install a charting library (e.g. Recharts)
- [ ] Loans-by-risk-tier chart
- [ ] Branch performance or customer-growth-over-time chart (pick one, keep scope tight)

**Day 75: Dashboard layout**
- [ ] Metric cards (per `01_PRD.md` persona needs) + charts + a mini map preview
- [ ] Set as default route after login

**Day 76: Performance & correctness check**
- [ ] Dashboard load time < 2s with reference dataset
- [ ] Spot-check 2–3 numbers against a manual DB count

**Day 77: Review**
- [ ] Commit + push, tag `v0.9.0-dashboard`

**Definition of Done:**
- [ ] Dashboard loads fast, is the default screen post-login, and every number reconciles against a manual check

---

## Sprint 12 — Hardening & Demo Polish (Days 78–90)

**Goal:** No new features — make what exists demo-proof. This sprint is longer (13 days) to absorb slippage from earlier sprints; use any earned slack for extra polish, not new scope.

**Day 78–80: Bug sweep**
- [ ] Walk every module (Customer/Branch/Property/Loan/Map/Search/Risk/Dashboard) end-to-end as if you were the recruiter — fix every broken interaction found
- [ ] Add loading states and error boundaries where missing
- [ ] Check console for any warnings/errors across all pages

**Day 81–82: Clean-machine test**
- [ ] On a fresh clone (or `docker compose down -v && docker compose up`), run through the entire demo checklist from `ROADMAP.md §1` start to finish
- [ ] Fix anything that requires undocumented manual steps

**Day 83–84: Documentation polish**
- [ ] Finalize `README.md`: setup steps, tech stack badges, links to all docs
- [ ] Confirm `01_PRD.md`–`04_AGENTS.md`, `BACKLOG.md`, `ROADMAP.md` all reflect the actually-shipped state (per `ROADMAP.md §10`)

**Day 85: Architecture diagram**
- [ ] Export a clean architecture diagram (the Mermaid diagrams in `02_SRS.md`/`03_DATABASE.md` rendered as images, or redrawn) into `architecture/`
- [ ] Link it from `README.md`

**Day 86: Screenshots**
- [ ] Capture: login, dashboard, map, one CRUD module, spatial search, risk analysis
- [ ] Add to `README.md` or a `docs/screenshots/` folder

**Day 87: Commit hygiene check**
- [ ] Confirm commit count is on track for 100+ (per `ROADMAP.md §11`) — if short, this is a signal earlier sprints committed in oversized chunks, not a reason to pad history artificially
- [ ] Confirm each of the 12 version tags exists with release notes

**Day 88–89: Buffer**
- [ ] Reserved for whatever slipped — do not add new features here even if time remains; polish existing modules further instead

**Day 90: Final review & tag**
- [ ] Full demo checklist (`ROADMAP.md §12`) run through one more time, unassisted, timed
- [ ] Tag `v1.0.0-demo-ready`

**Definition of Done:**
- [ ] A person who has never seen the project can clone, run `docker compose up`, log in, and complete the full demo checklist without asking a question

---

## Master progress tracker

| Sprint | Days | Module | Status |
| --- | --- | --- | --- |
| 1 | 1–7 | Docker & scaffold | ☐ Not started |
| 2 | 8–14 | PostGIS, GeoServer, seed data | ☐ Not started |
| 3 | 15–21 | Auth & RBAC | ☐ Not started |
| 4 | 22–28 | Customer module | ☐ Not started |
| 5 | 29–35 | Branch module | ☐ Not started |
| 6 | 36–42 | Property module | ☐ Not started |
| 7 | 43–49 | Loan & risk scoring | ☐ Not started |
| 8 | 50–56 | Interactive map | ☐ Not started |
| 9 | 57–63 | Spatial search | ☐ Not started |
| 10 | 64–70 | Risk analysis view | ☐ Not started |
| 11 | 71–77 | Dashboard | ☐ Not started |
| 12 | 78–90 | Hardening & demo polish | ☐ Not started |

Update the status column weekly (`☐ Not started` → `◐ In progress` →
`☑ Done`) as part of the Day 7 (or Day 90) review checklist in each
sprint above.
