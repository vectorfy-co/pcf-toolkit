#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "packaging>=24.2",
#   "pydantic>=2.6",
#   "rich>=13.7",
#   "tomlkit>=0.12.5",
#   "typer>=0.12",
# ]
# ///

"""Bump the version in `pyproject.toml`.

This script updates the PEP 621 `[project].version` field using semantic
versioning rules (MAJOR.MINOR.PATCH).

It is intended for use in CI/CD and local tooling.

Examples:
  Bump patch:
    uv run --script scripts/bump_version.py --bump patch

  Set explicit version:
    uv run --script scripts/bump_version.py --to 1.2.3
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Final, Literal

import typer
from packaging.version import Version
from pydantic import BaseModel, Field
from rich.console import Console
from tomlkit import dumps, parse

APP = typer.Typer(add_completion=False, no_args_is_help=True)
CONSOLE: Final[Console] = Console()

Bump = Literal["patch", "minor", "major"]


class ProjectMetadata(BaseModel):
    """Pydantic model for the PEP 621 `[project]` table."""

    name: str = Field(..., description="Project name.")
    version: str = Field(..., description="Project version (semver).")


class PyProject(BaseModel):
    """Pydantic model for the subset of `pyproject.toml` we care about."""

    project: ProjectMetadata = Field(..., description="PEP 621 project metadata.")


class VersionPlan(BaseModel):
    """Validated version change plan."""

    current: str = Field(..., description="Current version from pyproject.")
    next: str = Field(..., description="Next version to write.")


def _parse_semver(value: str) -> Version:
    """Parse a SemVer-like string into a `packaging.version.Version`.

    Args:
      value: Version string.

    Returns:
      Parsed `Version`.

    Raises:
      ValueError: If the version is not a simple `X.Y.Z` release version.
    """
    parsed = Version(value)
    if parsed.release is None or len(parsed.release) != 3:
        raise ValueError(f"Version must be X.Y.Z (got {value!r})")
    if parsed.pre is not None or parsed.post is not None or parsed.dev is not None:
        raise ValueError(f"Version must be a plain release (got {value!r})")
    return parsed


def _bump(version: Version, bump: Bump) -> Version:
    """Bump a version.

    Args:
      version: Current version.
      bump: Which part to bump.

    Returns:
      Bumped version.
    """
    major, minor, patch = version.release
    if bump == "major":
        return Version(f"{major + 1}.0.0")
    if bump == "minor":
        return Version(f"{major}.{minor + 1}.0")
    return Version(f"{major}.{minor}.{patch + 1}")


def _load_pyproject(pyproject_path: Path) -> PyProject:
    """Load and validate `pyproject.toml`.

    Args:
      pyproject_path: Path to `pyproject.toml`.

    Returns:
      Validated pyproject subset.

    Raises:
      FileNotFoundError: If the file does not exist.
      ValueError: If TOML is invalid or required fields are missing.
    """
    text = pyproject_path.read_text(encoding="utf-8")
    raw = tomllib.loads(text)
    return PyProject.model_validate(raw)


def _write_version(pyproject_path: Path, next_version: str) -> None:
    """Write `[project].version` using tomlkit (preserving formatting).

    Args:
      pyproject_path: Path to `pyproject.toml`.
      next_version: Version to write.
    """
    doc = parse(pyproject_path.read_text(encoding="utf-8"))
    doc["project"]["version"] = next_version
    pyproject_path.write_text(dumps(doc), encoding="utf-8")


def _plan_version(pyproject: PyProject, bump: Bump | None, to_version: str | None) -> VersionPlan:
    """Compute the next version to write.

    Args:
      pyproject: Parsed project metadata.
      bump: Semantic part to bump.
      to_version: Explicit version (overrides bump).

    Returns:
      Version plan.

    Raises:
      ValueError: If inputs are invalid.
    """
    current = _parse_semver(pyproject.project.version)
    if to_version is not None:
        target = _parse_semver(to_version)
        return VersionPlan(current=str(current), next=str(target))
    if bump is None:
        raise ValueError("Either --bump or --to must be provided.")
    return VersionPlan(current=str(current), next=str(_bump(current, bump)))


@APP.command()
def main(
    pyproject: Path = typer.Option(Path("pyproject.toml"), exists=True, dir_okay=False),
    bump: Bump | None = typer.Option(None, help="Bump semantic part (patch/minor/major)."),
    to: str | None = typer.Option(None, "--to", help="Set version to an explicit X.Y.Z."),
) -> None:
    """Entry point."""
    try:
        pyproject_model = _load_pyproject(pyproject)
        plan = _plan_version(pyproject_model, bump=bump, to_version=to)
        _write_version(pyproject, plan.next)
        CONSOLE.print(f"[green]Updated[/green] {pyproject} {plan.current} -> {plan.next}")
    except (OSError, ValueError) as exc:
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    APP()
