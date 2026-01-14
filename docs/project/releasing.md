---
title: Release Automation
description: Automated versioning, tagging, GitHub Releases, and PyPI publishing.
---

# Release Automation

This repo uses **GitHub Actions** to automatically:

- decide whether a change warrants a new release
- bump the version in `pyproject.toml`
- create an annotated git tag (`vX.Y.Z`)
- publish to **PyPI**
- create a **GitHub Release** with generated release notes

The automation runs on pushes to `main` (and can be run manually).

---

## What triggers a version bump

### Bump-worthy changes

Any changes under:

- `src/` (code)
- `schemas/` (schema definitions)
- `tests/` (behavior verification)
- `pyproject.toml` **except** when only the `version = "..."` line changed

### No-bump changes (docs/meta only)

Changes limited to:

- `docs/`
- `examples/`
- `README.md`
- `.github/`
- common meta files (e.g. `LICENSE.md`, `.gitignore`)

If a push contains both bump-worthy and docs/meta changes, it **will bump**.

---

## How the bump level is chosen (SemVer)

The automation follows semantic versioning **MAJOR.MINOR.PATCH**:

- **MAJOR**: commit message contains `BREAKING CHANGE` or uses `!` (e.g. `feat!: ...`)
- **MINOR**: any `feat:` commit message
- **PATCH**: any `fix:`, `perf:`, or `refactor:` commit message
- If bump-worthy files changed but commit messages don’t follow conventions, it defaults to **PATCH**

---

## Conventional Commit examples

- **Patch**:
  - `fix: handle empty schema snapshot`
  - `perf: speed up xml import`
- **Minor**:
  - `feat: add proxy doctor --fix for cert install`
- **Major**:
  - `feat!: drop support for legacy xml format`
  - `fix: change proxy config defaults\n\nBREAKING CHANGE: ...`

---

## Manual runs (dry-run / force / override)

Go to **GitHub → Actions → Tests and Publish → Run workflow**:

- **dry_run=true**: prints the next version and exits (no commit/tag/publish)
- **force=true**: forces a release even for docs/meta-only changes
- **bump**: explicitly choose `patch`, `minor`, or `major`

---

## PyPI publishing (Trusted Publishing)

Publishing uses **Trusted Publishing (OIDC)** via `uv publish`.

On PyPI, configure a trusted publisher:

- **Owner**: `vectorfy-co`
- **Repository**: `pcf-toolkit`
- **Workflow file**: `ci.yml`
- **Environment**: `pypi`

---

## Troubleshooting

- **Release didn’t happen**:
  - It was a docs/meta-only change, or
  - Only `pyproject.toml` version changed, or
  - No bump-worthy paths changed since the last tag
- **Publish job is skipped**:
  - `publish` runs only on `v*` tag refs; on branch pushes it will be skipped
- **Workflow can’t push commit/tag**:
  - Your branch protections may block GitHub Actions from pushing to `main`
  - Either allow GitHub Actions to push, or switch to a PR-based release flow

