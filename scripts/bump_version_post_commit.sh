#!/usr/bin/env bash
set -euo pipefail

# Avoid infinite loops when amending.
if [[ "${SKIP:-}" == *"bump-version-post-commit"* ]]; then
  exit 0
fi

# Bump patch version.
uv run --script scripts/bump_version.py --bump patch

# Amend the commit with the bumped version.
git add pyproject.toml
SKIP="${SKIP:-} bump-version-post-commit" git commit --amend --no-edit
