## 1. Directory Restructuring

- [x] 1.1 Create the `src/api/v1/routers/` directory and `__init__.py` files, verifying the new structure is recognizable by Python.
- [x] 1.2 Move existing routers from `src/api/routers/` to `src/api/v1/routers/` and update all internal imports, verifying the FastAPI app can still start without `ImportError`.

## 2. Router Reconfiguration

- [x] 2.1 Update `src/api/main.py` to create a new `v1_router = APIRouter(prefix="/api/v1")`. Verify by running a quick syntax check on `main.py`.
- [x] 2.2 Include all `v1` routers into `v1_router`, and include `v1_router` into the main FastAPI app. Verify by starting the application and checking if `/api/v1/docs` or `/docs` lists the endpoints under `/api/v1`.

## 3. Legacy Backward Compatibility

- [x] 3.1 Expose the exact same existing routers under their legacy unversioned paths in `main.py` (e.g., without prefix) but add `deprecated=True` in a wrapper or via router inclusion options. Verify by checking `/docs` to see the unversioned endpoints marked as deprecated.
- [x] 3.2 Add tests (or update existing ones) to assert that both `/api/v1/plans/` and `/plans/` return the same successful response. Verify by running `pytest`.

## 4. OpenAPI Customization

- [x] 4.1 Update FastAPI app instantiation metadata (title, description, version) to clearly reflect the API Versioning in Swagger UI. Verify by reviewing the generated OpenAPI schema at `/openapi.json`.
