# Architecture — GeoFinance

## 1. High-Level Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌───────────────────┐
│  Next.js    │───▶│  Node.js API  │───▶│  GeoServer  │───▶│ PostgreSQL/PostGIS │
│  Frontend   │◀───│  (Express)    │◀───│             │◀───│                    │
└─────────────┘     └──────┬───────┘     └─────────────┘     └───────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  AI Services  │
                    │ (Python/RAG)  │
                    └───────────────┘
```

- **Next.js Frontend** — user-facing app: dashboards, interactive GIS map,
  customer/branch/loan management UI.
- **Node.js API (Express)** — business logic, auth, orchestrates GeoServer
  and PostGIS queries, exposes REST/GraphQL endpoints to the frontend.
- **GeoServer** — serves spatial layers (WMS/WFS) sourced from PostGIS,
  used for map rendering and spatial queries.
- **PostgreSQL + PostGIS** — system of record for business data (customers,
  loans, properties, branches) and spatial data (geometries, boundaries).
- **AI Services** — consumes application + spatial data to power the AI
  Financial Assistant and risk-scoring recommendations (RAG over internal
  docs/data, LLM-backed).

## 2. Data Flow (typical request)

1. User interacts with the map/dashboard in the Next.js frontend.
2. Frontend calls the Node.js API.
3. API either:
   - queries PostgreSQL/PostGIS directly for business + spatial data, or
   - proxies spatial layer requests to GeoServer (WMS/WFS), or
   - calls the AI service for risk analysis / assistant responses.
4. API composes the response and returns it to the frontend.

## 3. Deployment Architecture

- **Local dev**: Docker Compose running Node API, PostgreSQL/PostGIS,
  GeoServer, and (later) the AI service as separate containers.
- **Cloud (later, Sprint 9–10)**: containers deployed via Kubernetes,
  provisioned with Terraform; CI/CD via GitHub Actions builds, tests, and
  deploys images on merge to main.

## 4. Key Modules → Architecture Mapping

| Module | Primary Layer |
| --- | --- |
| Authentication & RBAC | Node.js API |
| Customer / Branch / Loan / Property Management | Node.js API + PostgreSQL |
| Interactive GIS Map | Frontend (MapLibre/OpenLayers) + GeoServer |
| Spatial Search | GeoServer + PostGIS |
| Risk Analysis | Node.js API + AI Services |
| Dashboard & Analytics | Frontend + Node.js API |
| AI Assistant | AI Services (Python, RAG, Vector DB) |
| Administration Portal | Frontend + Node.js API (RBAC-gated) |

## 5. Open Decisions (to resolve during Sprint 0–1)

- [ ] REST vs GraphQL for the API layer
- [ ] Auth strategy (JWT + refresh tokens vs session-based; own implementation vs Auth0/Clerk)
- [ ] Vector DB choice for RAG (pgvector inside PostGIS instance vs standalone e.g. Qdrant)
- [ ] Monorepo (Turborepo/Nx) vs separate repos per service
- [ ] Hosting target for Sprint 9 (AWS / GCP / Azure / self-managed VPS)

## 6. Diagrams

Full C4-style diagrams (Context, Container, Component) to be added under
`architecture/` as the system grows past Sprint 1.
