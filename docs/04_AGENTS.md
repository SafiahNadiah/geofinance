# 04_AGENTS.md — AI Development Guide

**Product:** GeoFinance
**Document owner:** Solution Architecture
**Status:** Draft v1.0
**Depends on:** `01_PRD.md`, `02_SRS.md`, `03_DATABASE.md`
**Audience:** AI coding assistants (GitHub Copilot, Claude Code, Cursor) and human engineers using them

---

## 1. Executive Summary

This document is the operating manual for any AI coding assistant
working in this repository. It exists so that an assistant can
generate correct, convention-compliant code from a single prompt
referencing this file — without re-deriving architecture, naming, or
workflow decisions already made in `01_PRD.md`, `02_SRS.md`, and
`03_DATABASE.md`.

**Read order for an AI assistant starting fresh in this repo:**
`01_PRD.md` (what/why) → `02_SRS.md` (architecture/API) →
`03_DATABASE.md` (schema) → this document (how to actually write the
code).

---

## 2. Project Context (summary an assistant can act on)

| Fact | Value |
| --- | --- |
| Product | GeoFinance — financial + geospatial intelligence platform |
| Architecture | Clean Architecture, Repository Pattern, Service Layer, DDD tactics where warranted |
| Frontend | Next.js + React + TypeScript + Tailwind CSS |
| Backend | Node.js + Express + TypeScript |
| Database | PostgreSQL + PostGIS, UUID PKs, soft delete via `deleted_at` |
| AI service | Python, RAG, Vector DB, internal API only (not public-facing) |
| Auth | JWT (access + refresh), RBAC with roles `admin` / `analyst` / `viewer` |
| API style | REST, `/api/v1`, resource-plural, RFC 7807 errors |

If a generated change contradicts any of the above, treat this
document (and the three it depends on) as the source of truth over
any inferred convention or general best-practice default.

---

## 3. Folder Structure (authoritative)

```
geofinance/
├── frontend/
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable UI components
│   ├── lib/                 # API client, utils
│   └── types/                # Shared frontend TypeScript types
├── backend/
│   └── src/
│       ├── domain/           # Entities, value objects — no framework imports
│       ├── application/
│       │   ├── services/     # Business logic, one file per bounded use case
│       │   └── dtos/         # Request/response DTOs
│       ├── infrastructure/
│       │   ├── repositories/ # DB access, implements domain repository interfaces
│       │   ├── geoserver/    # GeoServer client
│       │   └── db/           # Connection, migrations runner
│       ├── interfaces/
│       │   ├── controllers/  # HTTP handlers — thin, delegate to services
│       │   ├── routes/       # Express route registration
│       │   └── middleware/   # Auth, RBAC, validation, error handling
│       └── shared/            # Errors, config, logger
├── ai-service/                # Python RAG service (separate deployable)
├── database/
│   ├── migrations/
│   └── seed-data/
├── geoserver/
├── docker/
├── docs/                       # This document set
└── architecture/
```

**Rule for an assistant generating a new file:** place it according to
this table by what it *is*, not by what feature it belongs to — do not
create feature-based top-level folders (e.g. no `backend/src/loans/`);
features are cross-cut through `domain/`, `application/`,
`infrastructure/`, `interfaces/` per the layer it belongs to.

---

## 4. Coding Standards (binding — restated from `02_SRS.md §3.1`)

**Always do:**
- TypeScript strict mode; no `any` without an inline justification comment
- UUID v4 primary keys everywhere (`gen_random_uuid()` at the DB level, never generated client-side for persisted entities)
- Repository interfaces defined in `domain/`, implementations in `infrastructure/repositories/`
- One service method per use case; services depend on repository *interfaces*, injected — not concrete classes
- DTOs for every controller input/output; validate DTOs at the controller boundary before calling a service
- REST conventions from `02_SRS.md §4.1` (pagination shape, RFC 7807 errors, `/api/v1` prefix)
- Snake_case in SQL/DB, camelCase in TypeScript — mapping happens in the repository layer, nowhere else
- Every new table gets a GiST index on its geometry column (see `03_DATABASE.md §4`) in the same migration that creates it

**Never do:**
- Raw SQL in a controller or service — SQL only inside `infrastructure/repositories/`
- Business logic inside an Express route handler or middleware
- Hardcoded config/secrets — read from a typed config module backed by environment variables
- New auto-increment integer PKs
- Direct AI-service-to-PostgreSQL writes in production paths (read-only access permitted for RAG context retrieval; writes must go through the backend API — see `02_SRS.md §8`)
- Introducing a new top-level dependency (ORM, validation library, etc.) without checking it doesn't duplicate one already chosen in `02_SRS.md §3`

---

## 5. Code Generation Recipes

These are the shapes an assistant should produce for the most common
change requests in this repo.

### 5.1 Adding a new REST endpoint

1. Define/extend the request and response DTOs in `application/dtos/`
2. Add or extend the service method in `application/services/`
3. Add the repository method (interface in `domain/`, implementation in `infrastructure/repositories/`) if new data access is needed
4. Add the controller method in `interfaces/controllers/`, calling the service — no logic beyond mapping request → DTO → service call → response
5. Register the route in `interfaces/routes/`, apply auth + RBAC middleware per `02_SRS.md §6`
6. Add validation middleware/schema for the request DTO

### 5.2 Adding a new database table

1. Write a migration in `database/migrations/` following `03_DATABASE.md §3.1` naming conventions
2. Include the GiST index in the same migration if the table has a geometry column
3. Add the domain entity in `backend/src/domain/`
4. Add the repository interface + implementation
5. Update `03_DATABASE.md` §2 (ER diagram) and §3 (table definition) in the same change

### 5.3 Adding a spatial query

- Prefer PostGIS functions over application-level distance math: `ST_DWithin`, `ST_Within`, `ST_Intersects`, `ST_Distance`
- Always operate in `SRID 4326` for storage; reproject only at query time if an accurate metric distance/area calculation requires it
- Verify the query hits the GiST index via `EXPLAIN ANALYZE` before merging, per `03_DATABASE.md §4`

### 5.4 Adding an AI Assistant query template

Per `02_SRS.md §7`, the AI Assistant is templated, not open-ended, in
v1:
1. Add the new question pattern to the supported-templates list (this document, §7 below, and `02_SRS.md §7`)
2. Implement the parser/matcher in `ai-service/`
3. Ensure the response includes the grounding data (record IDs/counts) — a response without a grounding reference is a spec violation, not a style preference

---

## 6. Testing Expectations

| Layer | Required tests |
| --- | --- |
| Domain | Unit tests for entity invariants and value object validation |
| Service | Unit tests with repository interfaces mocked |
| Repository | Integration tests against a real (test) PostGIS instance — no mocking of PostGIS spatial functions |
| Controller | Integration tests covering auth/RBAC rejection paths, not just happy path |
| Spatial queries | At least one test asserting correct results for a known point/radius fixture |

An assistant generating a new service method or endpoint should
generate the corresponding test alongside it, not as a separate
follow-up step.

---

## 7. AI Assistant Supported Query Templates (living list)

Carried from `02_SRS.md §7`; append here as new templates are added.
Do not implement a query pattern not listed here without first adding
it to this table.

| Template | Example |
| --- | --- |
| Count entities within radius of point/branch, filtered by attribute | "High-risk loans within 5km of Branch X" |
| Compare risk tier distribution across regions | "Compare risk tiers between Shah Alam and Klang branches" |
| Summarize a single entity's risk factors | "Why is loan LN00123 high risk?" |

---

## 8. Assumptions

Carried from `01_PRD.md §8`, `02_SRS.md §8`, `03_DATABASE.md §7`. No
additional assumptions specific to this document.

## 9. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| AI assistant (coding) generates code that satisfies a prompt but violates a convention in this doc | Medium | Treat this doc as a lint target — reviewers check generated PRs against §4 explicitly before merge |
| Drift between this doc and actual codebase as the project evolves | Medium | Update `04_AGENTS.md` in the same PR as any convention-level change, not as a follow-up |
| Over-reliance on AI-generated code without human review of business logic correctness (esp. risk scoring) | High | Risk-scoring logic (`loan_risk_assessments`) requires human review sign-off, not AI-only merge, given its role in financial decisions |

## 10. Future Enhancements

- Add a machine-readable convention lint config (e.g. ESLint custom rule set) that enforces §4 automatically rather than relying on review
- Expand AI Assistant template set (§7) based on real analyst usage patterns post-launch
- Add an architecture decision record (ADR) log under `architecture/adr/` for decisions made outside this document set

---

## 11. Document Sign-off Checklist

- [ ] Folder structure matches actual repository layout
- [ ] Coding standards reviewed by engineering lead
- [ ] Code generation recipes validated against at least one real PR
- [ ] AI Assistant template list agreed with product
- [ ] Full documentation set (01–04) considered complete for Sprint 0 exit

---

*End of 04_AGENTS.md — final document in the initial set (01–04).
Documentation set complete pending review.*
