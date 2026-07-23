---
name: git-flow
description: Manage the development workflow using the Git Flow extension by creating and finishing feature, release, and hotfix branches while enforcing branch naming conventions and repository state validation.
---

# Git Flow Skill

## Objective

This skill manages the Git branching workflow using the **Git Flow** extension.

The agent is responsible for:

- Creating Feature branches
- Finishing Feature branches
- Creating Release branches
- Finishing Release branches
- Creating Hotfix branches
- Finishing Hotfix branches
- Validating the repository state before every Git Flow operation
- Following the team's branch naming conventions

This skill **does not create commits or Pull Requests**. Those responsibilities belong to other skills.

---

# General Rules

Before executing any Git Flow command, always verify that:

- The repository is initialized with Git Flow.
- The working tree is clean.
- There are no uncommitted changes.
- There are no unresolved merge conflicts.
- The current branch is appropriate for the requested operation.

Run:

```bash
git status
```

If the repository is not clean, stop the operation and explain what must be committed, stashed, or discarded before proceeding.

Never execute Git Flow commands on a dirty working tree.

---

# Verify Git Flow

Before using Git Flow commands, verify that Git Flow is available.

Example:

```bash
git flow version
```

If Git Flow is not installed or initialized, stop and explain the issue instead of attempting alternative workflows.

---

# Branch Naming Convention

Branch names must be:

- written in lowercase
- use kebab-case
- concise
- descriptive
- use only letters, numbers and hyphens

Examples:

```
feature/user-authentication

feature/oauth-google

feature/payment-webhook

feature/export-csv

feature/add-dark-mode

release/2.4.0

hotfix/login-timeout
```

Avoid:

```
feature/NewFeature

feature/my_feature

feature/test

feature/temp

feature/wip

feature/fix123

feature/john-work
```

---

# Feature Workflow

## Starting a Feature

Before creating a feature:

1. Ensure the repository is clean.
2. Switch to `develop`.
3. Update the local branch from the remote.

Example:

```bash
git checkout develop
git pull origin develop
git flow feature start user-authentication
```

The feature name should describe the functionality, not the implementation.

Good examples:

```
user-authentication

payment-webhook

dark-mode

audit-log

shopping-cart
```

---

## Finishing a Feature

Before finishing:

- Ensure all intended changes have been committed.
- Ensure there are no uncommitted changes.
- Ensure the current branch is the feature branch being finished.

Run:

```bash
git flow feature finish user-authentication
```

If the finish operation produces merge conflicts, stop and allow them to be resolved before continuing.

---

# Release Workflow

## Starting a Release

Only start a release when:

- the development cycle is complete
- the release version is defined

Example:

```bash
git checkout develop
git pull origin develop
git flow release start 2.4.0
```

Release names should follow semantic versioning whenever possible.

Examples:

```
1.0.0

2.4.1

3.0.0
```

Avoid arbitrary release names.

---

## Finishing a Release

Before finishing:

- Ensure the repository is clean.
- Ensure release-specific changes have been committed.
- Verify the release version.

Execute:

```bash
git flow release finish 2.4.0
```

If configured, this operation may:

- merge into `main`
- merge back into `develop`
- create a Git tag

Verify that the process completes successfully before continuing.

---

# Hotfix Workflow

## Starting a Hotfix

Hotfixes must originate from the production branch.

Example:

```bash
git checkout main
git pull origin main
git flow hotfix start login-timeout
```

Use concise descriptive names.

Examples:

```
login-timeout

payment-crash

security-patch

jwt-validation
```

---

## Finishing a Hotfix

Before finishing:

- Ensure all changes have been committed.
- Ensure the working tree is clean.

Execute:

```bash
git flow hotfix finish login-timeout
```

Verify that:

- the hotfix has been merged correctly
- the tag was created if configured
- both `main` and `develop` received the fix

---

# Repository Validation

Before every operation, verify:

- Working tree is clean.
- Correct branch is checked out.
- Git Flow is available.
- Remote branches are up to date.
- There are no merge conflicts.

If any validation fails, stop the workflow and explain the issue.

---

# Error Handling

Do not attempt to recover automatically from situations such as:

- merge conflicts
- detached HEAD
- dirty working tree
- missing remote branches
- failed merges
- failed tags
- failed Git Flow commands

Instead:

1. Explain the problem.
2. Show the relevant Git error if available.
3. Recommend the next manual action.

---

# Best Practices

Always:

- update the base branch before creating a new branch
- keep branch names short and descriptive
- use kebab-case
- verify the repository state before every operation
- ensure Git Flow commands complete successfully
- follow semantic versioning for releases

Never:

- create features directly from `main`
- develop directly on `main`
- develop directly on `develop`
- use uppercase letters in branch names
- use spaces or underscores
- execute Git Flow commands with uncommitted changes
- ignore merge conflicts
- create temporary or meaningless branch names

---

# Quality Checklist

Before completing any workflow, verify that:

- Git Flow is installed and initialized.
- The repository is in a clean state.
- The correct base branch was used.
- The branch name follows the naming convention.
- The appropriate Git Flow command completed successfully.
- No merge conflicts remain unresolved.
- The repository is ready for the next development step.
