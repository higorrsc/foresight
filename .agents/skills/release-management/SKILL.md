---
name: release-management
description: Manage application releases by validating the repository state, generating release notes, creating semantic version tags, publishing GitHub releases, and verifying a successful release process.
---

# Release Management Skill

## Objective

This skill manages the release process after development has been completed.

The agent is responsible for:

- Validating the repository state
- Determining the next release version
- Following Semantic Versioning (SemVer)
- Generating release notes
- Creating annotated Git tags
- Publishing a GitHub Release
- Verifying that the release was successfully published

This skill **does not**:

- create commits
- open Pull Requests
- manage Git Flow branches

Those responsibilities belong to other skills.

---

# General Rules

Before starting a release:

- Ensure the working tree is clean.
- Ensure there are no merge conflicts.
- Ensure all intended commits have been merged.
- Ensure the correct release branch or `main` branch is checked out.
- Ensure the local repository is synchronized with the remote.

Run:

```bash
git status
git fetch --all --tags
```

If any validation fails, stop the release process and explain the issue.

---

# Versioning

Follow **Semantic Versioning (SemVer)**.

```
MAJOR.MINOR.PATCH
```

Increase:

| Type  | When                             |
| ----- | -------------------------------- |
| MAJOR | Breaking changes                 |
| MINOR | New backward-compatible features |
| PATCH | Backward-compatible bug fixes    |

Examples:

```
1.0.0

1.1.0

1.1.1

2.0.0
```

Never invent arbitrary version numbers.

---

# Determine the Next Version

When the version is not explicitly provided, infer it from the changes:

Examples:

- only bug fixes → PATCH
- new features → MINOR
- breaking changes → MAJOR

If breaking changes cannot be determined with confidence, ask the user before proceeding.

---

# Validate the Release

Before creating a release, verify:

- repository is clean
- correct branch is checked out
- latest changes have been pulled
- latest tags have been fetched
- version does not already exist

Example:

```bash
git fetch --all --tags

git tag
```

If the version already exists, stop immediately.

---

# Generate Release Notes

Generate release notes in English.

Group changes by category.

Template:

```markdown
## What's Changed

### Features

- Added ...

### Bug Fixes

- Fixed ...

### Improvements

- Improved ...

### Documentation

- Updated ...

### Dependencies

- Upgraded ...
```

Only include categories that contain changes.

Do not invent changes that did not occur.

---

# Create the Git Tag

Use annotated tags.

Example:

```bash
git tag -a v2.4.0 -m "Release v2.4.0"
```

Never create lightweight tags.

---

# Push Tags

Push the new tag.

```bash
git push origin v2.4.0
```

or

```bash
git push --tags
```

Verify that the push completed successfully.

---

# Publish the GitHub Release

If the repository is hosted on GitHub and the GitHub CLI is available, create a release using the generated release notes.

Example:

```bash
gh release create v2.4.0 \
  --title "v2.4.0" \
  --notes-file RELEASE_NOTES.md
```

If release notes are generated in memory rather than a file, use the equivalent `gh release create` options to provide the notes.

If the GitHub CLI is unavailable, explain the limitation instead of attempting unsupported alternatives.

---

# Verify the Release

Confirm that:

- the tag exists locally
- the tag exists remotely
- the GitHub Release was created successfully (when applicable)

Example:

```bash
git tag

git ls-remote --tags origin
```

---

# Error Handling

Stop immediately if:

- repository is dirty
- merge conflicts exist
- tag already exists
- tag creation fails
- push fails
- GitHub Release creation fails

Explain:

- what happened
- why the process stopped
- the recommended next step

Do not attempt automatic recovery.

---

# Best Practices

Always:

- use Semantic Versioning
- generate clear release notes
- create annotated tags
- verify tag uniqueness before creation
- verify the release after publishing
- write all release content in English

Never:

- overwrite existing tags
- publish duplicate releases
- invent release notes
- publish a release with uncommitted changes
- create lightweight tags
- skip repository validation

---

# Quality Checklist

Before completing the release, verify that:

- The repository is clean.
- The local repository is synchronized with the remote.
- The release version follows Semantic Versioning.
- The version does not already exist.
- Release notes accurately describe the changes.
- The Git tag is annotated.
- The tag has been pushed successfully.
- The GitHub Release has been published successfully (when applicable).
- All release notes are written in English.
- The release process completed without errors.
