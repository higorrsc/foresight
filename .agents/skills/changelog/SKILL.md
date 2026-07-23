---
name: changelog
description: Generate and maintain a high-quality CHANGELOG.md following the Keep a Changelog specification and Semantic Versioning.
---

# Changelog Skill

## Objective

This skill is responsible for generating and maintaining the project's `CHANGELOG.md`.

The changelog must:

- Follow the **Keep a Changelog** specification.
- Follow **Semantic Versioning (SemVer)**.
- Be written entirely in **English**.
- Clearly summarize user-facing changes.
- Remain organized and easy to read.

This skill **does not**:

- create commits
- create Git tags
- publish releases
- open Pull Requests

Those responsibilities belong to other skills.

---

# General Rules

The changelog file must always be named:

```
CHANGELOG.md
```

If it does not exist, create it.

If it already exists, preserve its formatting and append new entries instead of rewriting the entire file.

Never remove previous release entries unless explicitly requested.

---

# Changelog Standard

Follow the **Keep a Changelog** format.

Structure:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
```

Only include sections that contain changes.

Avoid empty sections inside released versions.

---

# Release Entries

Each released version should follow this format:

```markdown
## [2.4.0] - 2026-07-23

### Added

- Added JWT authentication.
- Added password reset endpoint.

### Changed

- Improved validation for user registration.

### Fixed

- Fixed OAuth callback timeout.

### Security

- Improved token validation.
```

Use the ISO date format:

```
YYYY-MM-DD
```

---

# Categorizing Changes

Categorize changes according to their impact.

| Category   | Description                    |
| ---------- | ------------------------------ |
| Added      | New features                   |
| Changed    | Existing behavior improvements |
| Deprecated | Features scheduled for removal |
| Removed    | Removed functionality          |
| Fixed      | Bug fixes                      |
| Security   | Security improvements          |

Choose the most appropriate category.

Avoid duplicate entries.

---

# Writing Guidelines

Every entry must:

- be written in English
- describe the user-visible impact
- be concise
- use the past tense
- begin with a verb

Good examples:

```
Added dark mode support.

Improved authentication performance.

Fixed an issue where sessions expired unexpectedly.

Removed deprecated API endpoints.

Improved password validation.

Updated OAuth provider integration.
```

Avoid:

```
Did stuff.

Changes.

Bug fixes.

Updated things.

Misc improvements.

Refactoring.
```

Internal implementation details should only be included if they affect users, developers, deployment, or maintenance.

---

# Unreleased Section

Maintain an `Unreleased` section at the top of the file.

Example:

```markdown
## [Unreleased]

### Added

- Added support for OAuth login.

### Fixed

- Fixed session expiration issue.
```

When a release is created:

1. Move the contents of `Unreleased` into the new version.
2. Create a new empty `Unreleased` section.

---

# Version Ordering

Versions must appear in reverse chronological order.

Example:

```text
Unreleased

2.4.0

2.3.1

2.3.0

2.2.0
```

Never reorder historical releases.

---

# Release Dates

Use the release date.

Format:

```
YYYY-MM-DD
```

Example:

```
2026-07-23
```

Do not use localized date formats.

---

# Breaking Changes

Breaking changes should be clearly documented.

Example:

```markdown
### Changed

- Updated the authentication API to require JWT tokens.

**Breaking Change:** API clients must include the Authorization header in every authenticated request.
```

Breaking changes must be explicit.

---

# Dependency Updates

Do not include dependency updates unless they have a meaningful impact on users, deployment, security, or maintainability.

Good examples:

```
Updated OpenSSL to address security vulnerabilities.

Upgraded PostgreSQL driver to improve compatibility.
```

Avoid listing routine dependency bumps with no notable impact.

---

# Documentation Changes

Only include documentation updates when they affect project usage or developer onboarding.

Example:

```
Updated installation instructions.

Added deployment documentation.

Improved API usage examples.
```

---

# Automatic Generation

When generating changelog entries, derive information from:

- merged Pull Requests
- commit history
- release notes
- implemented features
- bug fixes

Never invent changes.

If there is insufficient information, ask for clarification rather than guessing.

---

# Best Practices

Always:

- follow Keep a Changelog
- follow Semantic Versioning
- write in English
- describe user-facing changes
- keep entries concise
- preserve previous releases
- maintain the Unreleased section
- use consistent formatting

Never:

- rewrite release history
- invent changes
- duplicate entries
- include empty sections
- document internal implementation details that have no external impact
- use vague descriptions

---

# Quality Checklist

Before completing the changelog update, verify that:

- The file follows the Keep a Changelog specification.
- All entries are written in English.
- The Unreleased section exists.
- Release entries use Semantic Versioning.
- Dates follow the YYYY-MM-DD format.
- Changes are categorized correctly.
- No duplicate entries exist.
- No empty sections are present in released versions.
- Historical entries have been preserved.
- All documented changes are based on actual project modifications.
