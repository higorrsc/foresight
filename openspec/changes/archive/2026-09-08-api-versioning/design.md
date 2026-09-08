## Context

The current FastAPI application structures routers under `src/api/routers/<domain>/` and mounts them directly to the root application in `main.py`. This structure currently lacks a versioning mechanism. See `proposal.md` for motivation. We will implement URL-based versioning (`/api/v1/`) while maintaining the Clean Architecture approach in `src/core/` and other domains.

## Goals / Non-Goals

**Goals:**
- Implement a `/api/v1` APIRouter prefix for all new and existing routers.
- Maintain legacy unversioned endpoints with deprecation warnings to avoid breaking existing clients immediately.
- Define a clear directory structure for versioned routers (`src/api/v1/routers/`).

**Non-Goals:**
- Header-based versioning or query parameter versioning.
- Duplicating business logic; core application logic and use cases will remain strictly shared.
- Immediately dropping support for the legacy unversioned endpoints.

## Decisions

- **URL Versioning over Header Versioning**: 
  - *Rationale*: URL versioning (`/api/v1`) is explicit, easier to explore via Swagger/OpenAPI, and aligns well with standard FastAPI conventions.
  - *Alternative*: Header-based versioning (`Accept: application/vnd.api+json;version=1`). Rejected due to increased complexity in routing and testing, and poorer developer experience with browser-based tools.
- **Router Directory Restructuring**:
  - *Rationale*: By moving existing routers to `src/api/v1/routers/`, we create a clear separation for when `v2` is introduced. The root `main.py` will include a single `v1_router` that aggregates them.
  - *Alternative*: Keep existing routers in `src/api/routers/` and prefix the `include_router` call. Rejected because it does not scale well when different versions need distinct Pydantic schemas or contract variations.
- **Deprecation Strategy via Aliasing**:
  - *Rationale*: We will create a legacy module (`src/api/legacy_routers/`) or just mount the exact same `v1` routers at the root with `deprecated=True` to serve existing clients without duplicating code. This allows safe migration.
  - *Alternative*: Force all clients to update immediately. Rejected as it introduces unacceptable breaking changes.

## Risks / Trade-offs

- **[Risk] OpenAPI Clutter**: Mounting endpoints twice (once for `v1` and once for legacy) will duplicate entries in Swagger UI, which might confuse developers.
  - *Mitigation*: The legacy endpoints will be explicitly marked with `@router.get(..., deprecated=True)` and grouped under a "Legacy" tag if possible.
- **[Risk] Migration Effort**: Changing paths in frontend applications and third-party integrations.
  - *Mitigation*: The deprecated legacy endpoints give clients ample time to adopt the new `/api/v1` URLs before they are removed in the next major release.
