---
name: commit-and-open-pr
description: Analyze code changes, create atomic commits using Conventional Commits with Gitmojis, push the current branch, and open a well-written Pull Request in English.
---

# Commit & Pull Request Skill

## Objective

After completing any code changes, the agent must:

1. Review all modifications.
2. Organize related changes into logical commits.
3. Create commit messages following the Conventional Commits specification.
4. Prefix every commit with an appropriate Gitmoji.
5. Write **all Git-related messages in English**, including:
   - Commit messages
   - Pull Request title
   - Pull Request description
6. Push the current branch.
7. Open a Pull Request with a complete description.

---

# Workflow

## 1. Review the changes

Before creating any commit, inspect the repository.

Run:

```bash
git status
git diff
git diff --cached
```

Review:

- modified files
- new files
- deleted files
- accidental changes
- debug code
- logs
- generated files
- secrets

Never commit:

- `.env`
- credentials
- API keys
- temporary files
- logs
- build artifacts that should not be versioned
- commented debugging code

If unrelated changes are detected, exclude them from the commit.

---

## 2. Organize commits

Group changes by logical purpose.

Examples:

- new feature
- bug fix
- refactoring
- documentation
- tests
- CI/CD
- dependency updates
- configuration

Prefer multiple small commits instead of one large commit whenever the changes are unrelated.

Every commit should represent one logical unit of work.

---

# Commit Message Standard

Commit messages **must always be written in English**.

Format:

```
<type>(scope): <gitmoji> short description
```

Examples:

```
feat(auth): ✨ add Google authentication

fix(api): 🐛 handle request timeout correctly

refactor(user): ♻️ simplify validation logic

docs(readme): 📝 update installation guide

test(auth): ✅ add middleware unit tests

perf(cache): 🚀 improve cache lookup performance

chore: 🔥 remove unused legacy code

chore(ci): 🔧 update GitHub Actions workflow

style(ui): 💄 improve dashboard spacing

chore(deps): ⬆️ upgrade express to v5
```

Rules:

- English only.
- Use the imperative mood.
- Keep descriptions concise.
- Use lowercase except for proper nouns or acronyms.
- Do not end the message with a period.
- Clearly describe what the change does.

---

# Conventional Commit Types

Use the most appropriate type.

| Type     | Purpose                       |
| -------- | ----------------------------- |
| feat     | New feature                   |
| fix      | Bug fix                       |
| docs     | Documentation                 |
| style    | Formatting or UI-only changes |
| refactor | Code refactoring              |
| perf     | Performance improvements      |
| test     | Tests                         |
| build    | Build system                  |
| ci       | CI/CD                         |
| chore    | Maintenance                   |
| revert   | Revert changes                |

---

# Preferred Gitmojis

Use the Gitmoji that best matches the change.

| Gitmoji | Purpose            |
| ------- | ------------------ |
| ✨      | New feature        |
| 🐛      | Bug fix            |
| ♻️      | Refactoring        |
| 📝      | Documentation      |
| 🚀      | Performance        |
| ✅      | Tests              |
| 🔧      | Configuration      |
| ⬆️      | Dependency updates |
| 🔥      | Remove code/files  |
| 💄      | UI improvements    |
| 🚑️      | Critical hotfix    |
| 🚨      | Fix lint warnings  |
| 🔒      | Security           |

---

# Automatic Commit Type Selection

Infer the commit type automatically.

| Change                  | Commit          |
| ----------------------- | --------------- |
| New functionality       | feat ✨         |
| Bug fix                 | fix 🐛          |
| Refactoring             | refactor ♻️     |
| Documentation           | docs 📝         |
| Tests                   | test ✅         |
| Performance             | perf 🚀         |
| Configuration           | chore 🔧        |
| Dependency updates      | chore (deps) ⬆️ |
| Remove unused code      | chore 🔥        |
| UI improvements         | style 💄        |
| Security                | fix 🔒          |
| Critical production fix | fix 🚑️          |

---

# Creating Commits

Stage only the files that belong to the current logical change.

Example:

```bash
git add <files>

git commit -m "feat(auth): ✨ add JWT authentication"
```

Repeat the process for each logical group of changes.

Never create generic commit messages such as:

- update
- changes
- fixes
- misc
- work
- wip
- adjustments
- improvements

Every commit message must be meaningful and descriptive.

---

# Push

After all commits have been created successfully:

```bash
git push origin <current-branch>
```

---

# Pull Request

After pushing the branch, create a Pull Request.

## Pull Request Title

The title **must be written in English** and follow the same format as the primary commit.

Example:

```
feat(auth): ✨ add JWT authentication
```

---

## Pull Request Description

The description **must be written entirely in English** using the following template.

```markdown
## Summary

Briefly describe the purpose of this Pull Request.

## Changes

- Change 1
- Change 2
- Change 3

## Motivation

Explain why these changes were necessary.

## How to Test

1. Step one
2. Step two
3. Step three

## Checklist

- [ ] Code reviewed
- [ ] Tests executed
- [ ] Documentation updated (if applicable)
- [ ] No temporary or unnecessary files included
```

The Pull Request should clearly explain:

- what changed
- why the change was made
- how reviewers can validate it

Avoid vague descriptions.

---

# Best Practices

Always:

- create atomic commits
- keep commits focused
- write meaningful commit messages
- use Conventional Commits
- use Gitmojis
- write all Git messages in English
- create a complete Pull Request description
- verify the repository is clean before finishing

Never:

- create generic commit messages
- mix unrelated changes in the same commit
- commit secrets
- commit temporary files
- commit debug code
- create WIP commits
- open Pull Requests with incomplete descriptions

---

# Quality Checklist

Before finishing, verify that:

- All changes have been reviewed.
- Every commit is atomic.
- Every commit follows Conventional Commits.
- Every commit includes an appropriate Gitmoji.
- Every commit message is written in English.
- Only relevant files are included.
- The current branch has been pushed successfully.
- The Pull Request title is written in English.
- The Pull Request description is written entirely in English.
- The Pull Request accurately describes the implemented changes.
- The repository is left in a clean state.
