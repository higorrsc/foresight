## Purpose

Establishes the behavioral contract and lifecycle policies for API versioning, ensuring clients can rely on stable endpoints while the system evolves.

## Requirements

### Requirement: API URLs MUST be versioned
All new and current endpoints SHALL be exposed under a versioned path prefix, starting with `/api/v1`. The system SHALL respond to these paths as the primary interface.

#### Scenario: Requesting a versioned endpoint
- **WHEN** a client makes a valid request to `/api/v1/plans/`
- **THEN** the system returns a `200 OK` response with the expected data

### Requirement: Unversioned endpoints SHALL be supported temporarily
For backward compatibility, existing unversioned endpoints SHALL continue to function and route to the same underlying logic as their `v1` counterparts.

#### Scenario: Requesting a legacy unversioned endpoint
- **WHEN** a client makes a valid request to `/plans/`
- **THEN** the system returns a `200 OK` response identical to `/api/v1/plans/`
- **THEN** the endpoint operates normally but is marked as deprecated in documentation

### Requirement: Version schemas SHALL be explicitly documented
The OpenAPI specification (`/docs` or `/openapi.json`) SHALL clearly display the API version (`v1`) and clearly mark legacy endpoints as deprecated.

#### Scenario: Accessing OpenAPI docs
- **WHEN** a client accesses the OpenAPI schema
- **THEN** they see version `v1` prominently
- **THEN** any legacy endpoints are tagged with `deprecated=True`
