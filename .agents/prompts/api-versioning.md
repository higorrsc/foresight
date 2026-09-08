# Proposal: FastAPI API Versioning

Analyze the current project and propose a specification for implementing versioning for the REST API built with FastAPI.

## Objective

We need to introduce API versioning in a way that allows the API contracts, endpoints, and behavior to evolve without breaking clients that still depend on previous versions.

The proposal should consider the project's existing architecture and prioritize a solution that is simple, consistent, scalable, and aligned with FastAPI best practices.

## Before proposing the solution

Analyze the existing codebase to identify:

- Current directory and module structure.
- How FastAPI routers are organized.
- Where the `FastAPI()` application is instantiated.
- How routers are registered in the application.
- Organization of Pydantic schemas/models.
- Organization of services/use cases.
- Organization of repositories.
- Existing middleware and dependencies.
- API-related configuration.
- Existing tests and their organization.
- Current OpenAPI/Swagger documentation.
- Currently exposed public endpoints.
- Potential coupling between routers, schemas, and business logic.

Do not propose a broad architectural restructuring just to introduce versioning. Reuse the existing architecture whenever possible.

## Versioning strategy

Evaluate the most appropriate versioning strategies for this project, especially:

1. URL-based versioning:
   - `/api/v1/...`
   - `/api/v2/...`

2. Header-based versioning, if appropriate for the current architecture.

3. Other relevant strategies, if there is a technical reason to consider them.

Compare the alternatives based on:

- Compatibility with existing clients.
- Maintainability.
- Clarity for API consumers.
- FastAPI integration.
- OpenAPI documentation support.
- Testability.
- Ease of introducing a future `v2`.
- Impact on the existing codebase.

At the end of the analysis, recommend one strategy and provide a technical justification for the decision.

## Functional requirements

The proposed solution must allow us to:

- Keep the current API version available without introducing breaking changes.
- Introduce new versions of endpoints when necessary.
- Allow different API versions to coexist during a migration period.
- Clearly identify which version is being consumed.
- Generate appropriate OpenAPI/Swagger documentation for the available versions.
- Avoid unnecessary duplication of business logic.
- Allow contract changes to be isolated between versions.
- Make it easy to deprecate and eventually remove obsolete versions.

Also consider how to handle:

- Changes to request schemas.
- Changes to response schemas.
- Changes to parameters.
- Changes to behavior.
- Endpoint deprecation.
- Backward compatibility.

## Technical requirements

Explain how versioning should be structured in FastAPI.

For example, evaluate a structure similar to:

```text
app/
├── api/
│   ├── v1/
│   │   ├── routers/
│   │   └── schemas/
│   └── v2/
│       ├── routers/
│       └── schemas/
├── services/
├── repositories/
└── main.py
```

However, do not assume this structure is mandatory. Adapt the proposal to the structure discovered in the existing project.

An important principle is to separate the **API contract** from the **business logic**.

When two API versions have identical business behavior, the implementation should be shared through services/use cases instead of duplicated.

When there are actual contract differences, consider keeping version-specific schemas and routers.

## Compatibility

Analyze the existing endpoints and define:

- Which version will be considered the current API version.
- What the URLs of the versioned endpoints will be.
- Whether the existing endpoints will remain available for backward compatibility.
- How existing endpoints will be migrated to `v1`.
- Whether redirects should be used or not.
- How to avoid breaking changes during the migration.

Do not introduce breaking changes silently.

## Deprecation

Propose a strategy for deprecated versions/endpoints, including:

- How to mark endpoints as deprecated in OpenAPI.
- How to communicate deprecation to API consumers.
- How to define a support policy.
- How to remove an old API version in the future.

## Documentation

Explain how the API documentation should work after introducing versioning.

Consider:

- Swagger UI.
- ReDoc.
- OpenAPI.
- Separation or grouping of API versions.
- Clear identification of the version for each endpoint.
- How to avoid ambiguity when `v1` and `v2` coexist.

## Testing

Propose a testing strategy to ensure:

- Endpoints for each version continue to work.
- Request/response contracts are preserved.
- Changes in `v2` do not break `v1`.
- Shared business logic continues to work correctly.
- New versioned endpoints have appropriate test coverage.

If the project already has tests, follow the existing testing patterns and conventions.

## Security and observability

Check whether API versioning has any impact on:

- Authentication.
- Authorization.
- Rate limiting.
- Logging.
- Metrics.
- Tracing.
- Auditing.

The proposal should preserve the existing mechanisms and identify any changes that may be required.

## Acceptance criteria

The proposal must satisfy the following criteria:

- A clear API versioning strategy is defined.
- The chosen strategy has a technical justification.
- Existing clients are not broken without an explicit migration path.
- At least two API versions can coexist.
- Incompatible schemas can coexist between versions.
- Business logic is not unnecessarily duplicated.
- OpenAPI documentation correctly identifies the available API versions.
- Tests exist to guarantee compatibility between versions.
- There is a clear deprecation and removal strategy for old versions.
- The solution is compatible with the project's existing architecture.

## Deliverable

Do not implement the code yet.

First, produce a **change proposal** containing:

1. Context and problem statement.
2. Analysis of the current architecture.
3. Strategies considered.
4. Recommended strategy.
5. Proposed architecture.
6. Required changes to the project structure.
7. Migration strategy for existing endpoints.
8. Strategy for schemas and API contracts.
9. Strategy for sharing business logic.
10. Testing strategy.
11. OpenAPI documentation strategy.
12. Deprecation strategy.
13. Risks and trade-offs.
14. Acceptance criteria.
15. Examples showing how endpoints would look before and after versioning.
16. Directory structure and code examples only when necessary to clarify the proposal.

### Important

Do not make architectural decisions based solely on generic best practices.

Decisions must be justified based on the actual codebase and architecture discovered during the analysis.

If multiple solutions are viable, present the alternatives and explain why one of them is preferable.

**Do not implement the change at this stage. The goal is to produce a sufficiently detailed specification/proposal so that the implementation can be carried out safely afterward.**
