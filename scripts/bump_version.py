#!/usr/bin/env python3
# /// script
# dependencies = []
# ///

from __future__ import annotations

import argparse
import re
from pathlib import Path

VERSION_RE = re.compile(r'^(\s*version\s*=\s*")(\d+\.\d+\.\d+)("\s*)$')


def _bump(version: str, bump: str) -> str:
    major, minor, patch = [int(part) for part in version.split(".")]
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"Unknown bump: {bump}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump pyproject.toml version.")
    parser.add_argument(
        "--pyproject",
        default="pyproject.toml",
        help="Path to pyproject.toml (default: pyproject.toml)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to", dest="to_version", help="Set version to an explicit value")
    group.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        help="Bump version by semantic part",
    )

    args = parser.parse_args()
    path = Path(args.pyproject)
    text = path.read_text()

    updated = []
    replaced = False
    for line in text.splitlines():
        match = VERSION_RE.match(line)
        if match and not replaced:
            current = match.group(2)
            next_version = args.to_version or _bump(current, args.bump)
            updated.append(f"{match.group(1)}{next_version}{match.group(3)}")
            replaced = True
        else:
            updated.append(line)

    if not replaced:
        raise SystemExit("No version field found in pyproject.toml")

    path.write_text("\n".join(updated) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
