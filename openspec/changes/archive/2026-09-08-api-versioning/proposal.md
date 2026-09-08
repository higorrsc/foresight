## Why

We need to introduce API versioning to allow the API contracts, endpoints, and behavior to evolve without breaking clients that depend on previous versions. As the Foresight API expands, maintaining backward compatibility and providing a clear contract for consumers is essential.

## What Changes

- Introduce **URL-based versioning** (e.g., `/api/v1/...`) as the primary versioning strategy.
- Restructure the `src/api/` directory to group routers and schemas by version (e.g., `src/api/v1/routers/`).
- **BREAKING (Delayed)**: Existing unversioned endpoints will be aliased to `/api/v1` and marked as deprecated in the OpenAPI documentation. They will be removed in a future release.
- Business logic (Use Cases, Domain Entities) will remain shared across API versions. Version-specific logic will only be introduced at the router and schema levels.
- Enhance OpenAPI documentation to explicitly categorize and expose different API versions.

## Capabilities

### New Capabilities
- `api-versioning`: Defines the architectural standards, directory structure, routing strategy, and deprecation policies for maintaining multiple API versions in the FastAPI application.

### Modified Capabilities

## Impact

- **API Consumers**: Clients will need to migrate to `/api/v1/` URLs. Old URLs will continue to work during the deprecation window but will be marked as deprecated.
- **Codebase**: `src/api/main.py` and `src/api/routers/` will be reorganized. New routers will be mounted under an `APIRouter(prefix="/api/v1")`.
- **Tests**: API tests will need to be updated to target the new `/api/v1/` endpoints.
- **Documentation**: Swagger UI will expose a clean `v1` definition.
