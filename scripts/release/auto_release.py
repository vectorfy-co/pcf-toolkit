#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "gitpython>=3.1.44",
#   "packaging>=24.2",
#   "pydantic>=2.6",
#   "pydantic-settings>=2.2",
#   "rich>=13.7",
#   "tomlkit>=0.12.5",
#   "typer>=0.12",
# ]
# ///

"""Automated version bumping + tagging for pcf-toolkit.

This script is designed to be run in CI on pushes to `main`.

It will:
  - detect whether changes since the last `v*` tag require a version bump
  - choose bump level via Conventional Commits (major/minor/patch) or default to patch
  - update `pyproject.toml` (`[project].version`)
  - commit the bump
  - create an annotated git tag `vX.Y.Z`

Publishing to PyPI and creating a GitHub Release is handled by GitHub Actions.
"""

from __future__ import annotations

import re
import tomllib
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Final, Literal

import typer
from git import Repo
from git.exc import GitCommandError
from packaging.version import Version
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from rich.console import Console
from tomlkit import dumps, parse

APP = typer.Typer(add_completion=False, no_args_is_help=False)
CONSOLE: Final[Console] = Console()

BumpLevel = Literal["major", "minor", "patch"]

CONVENTIONAL_SUBJECT_RE: Final[re.Pattern[str]] = re.compile(
    r"^(?P<type>[a-zA-Z]+)(?:\([^)]+\))?(?P<breaking>!)?:\s+.+$"
)

BUMP_WORTHY_PREFIXES: Final[tuple[str, ...]] = ("src/", "schemas/", "tests/")
NO_BUMP_PREFIXES: Final[tuple[str, ...]] = ("docs/", "examples/", ".github/")
NO_BUMP_FILES: Final[tuple[str, ...]] = ("README.md", "LICENSE.md", ".gitignore")


class GitHubEnv(BaseSettings):
    """GitHub Actions environment variables."""

    github_output: Path | None = Field(default=None, validation_alias="GITHUB_OUTPUT")


class ProjectMetadata(BaseModel):
    """Subset of `[project]` used for versioning."""

    name: str = Field(..., description="Project name.")
    version: str = Field(..., description="Project version (X.Y.Z).")


class PyProject(BaseModel):
    """Subset of `pyproject.toml` used for versioning."""

    project: ProjectMetadata = Field(..., description="PEP 621 project metadata.")


class ChangeDetectionResult(BaseModel):
    """Change detection output since the last tag."""

    since_tag: str | None = Field(default=None, description="Last v* tag name (if any).")
    changed_files: list[str] = Field(default_factory=list, description="Changed paths since since_tag.")
    bump_worthy: bool = Field(..., description="Whether a release is warranted by file changes.")
    docs_only: bool = Field(..., description="Whether changes are docs/meta-only.")
    pyproject_version_only: bool = Field(..., description="Whether only pyproject version changed.")


class VersionDecision(BaseModel):
    """Versioning decision."""

    bump_level: BumpLevel = Field(..., description="Chosen semantic bump level.")
    current_version: str = Field(..., description="Current version from pyproject.")
    next_version: str = Field(..., description="Next version to write.")
    tag: str = Field(..., description="Git tag to create (vX.Y.Z).")


class ReleasePlan(BaseModel):
    """Complete release plan."""

    config: ReleaseConfig = Field(..., description="Release configuration inputs.")
    do_release: bool = Field(..., description="Whether a release will be performed.")
    reason: str = Field(..., description="Human-readable reason for the decision.")
    change_detection: ChangeDetectionResult = Field(..., description="Change detection details.")
    version_decision: VersionDecision | None = Field(default=None, description="Version decision if releasing.")


class ReleaseConfig(BaseModel):
    """Release configuration inputs."""

    pyproject_path: Path = Field(..., description="Resolved path to pyproject.toml.")
    dry_run: bool = Field(default=False, description="If true, do not commit or tag.")
    force: bool = Field(default=False, description="Force a release even for docs/meta-only changes.")
    bump_override: BumpLevel | None = Field(default=None, description="Explicit bump override.")
    github_output: Path | None = Field(default=None, description="Path to $GITHUB_OUTPUT, if any.")


class GitOperationResult(BaseModel):
    """Results of git operations performed by this script."""

    commit_sha: str = Field(..., description="Created commit SHA.")
    tag: str = Field(..., description="Created tag name.")


def _repo() -> Repo:
    """Open the git repository."""
    return Repo(Path.cwd(), search_parent_directories=True)


def _repo_root(repo: Repo) -> Path:
    """Get repository root path."""
    root = repo.working_tree_dir
    if root is None:
        raise ValueError("Repository has no working tree directory.")
    return Path(root)


def _get_last_tag(repo: Repo) -> str | None:
    """Return the last `v*` tag reachable from HEAD, if any."""
    try:
        # GitPython's dynamic `repo.git.*` API is typed as `Any`; normalize to `str` for strict mypy.
        return str(repo.git.describe("--tags", "--abbrev=0", "--match", "v*")).strip()
    except GitCommandError:
        return None


def _changed_files(repo: Repo, since_tag: str | None) -> list[str]:
    """Return changed file paths since a tag (or all files if no tag)."""
    if since_tag:
        out = repo.git.diff("--name-only", f"{since_tag}..HEAD").strip()
        return [line for line in out.splitlines() if line.strip()]
    out = repo.git.ls_files().strip()
    return [line for line in out.splitlines() if line.strip()]


def _is_docs_only(paths: Iterable[str]) -> bool:
    """True if all changes are docs/meta-only."""
    for p in paths:
        if p.startswith(NO_BUMP_PREFIXES) or p in NO_BUMP_FILES:
            continue
        return False
    return True


def _load_pyproject(pyproject_path: Path) -> PyProject:
    """Load and validate `pyproject.toml`."""
    raw = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return PyProject.model_validate(raw)


def _strip_project_version(toml_text: str) -> str:
    """Normalize TOML by setting `[project].version` to a sentinel string."""
    # tomlkit has incomplete typing; treat document as `Any` for strict mypy.
    doc: Any = parse(toml_text)
    if "project" in doc and "version" in doc["project"]:
        doc["project"]["version"] = "__VERSION__"
    # tomlkit returns `Any` (no stubs); normalize to `str` for strict mypy.
    return str(dumps(doc))


def _pyproject_version_only_changed(repo: Repo, since_tag: str | None) -> bool:
    """Return True if only `[project].version` changed in pyproject.toml since the tag."""
    if not since_tag:
        return False
    try:
        before = repo.git.show(f"{since_tag}:pyproject.toml")
    except GitCommandError:
        return False
    after = Path(_repo_root(repo) / "pyproject.toml").read_text(encoding="utf-8")
    return _strip_project_version(before) == _strip_project_version(after) and before != after


def _is_bump_worthy_file(path: str, pyproject_version_only: bool) -> bool:
    """Return True if a path requires a version bump."""
    if path.startswith(BUMP_WORTHY_PREFIXES):
        return True
    if path == "pyproject.toml":
        return not pyproject_version_only
    return False


def _has_bump_worthy_changes(paths: Iterable[str], pyproject_version_only: bool) -> bool:
    """True if any changed file requires a bump."""
    return any(_is_bump_worthy_file(p, pyproject_version_only) for p in paths)


def _choose_bump_level(messages: list[str], default_if_needed: bool) -> BumpLevel | None:
    """Choose bump level from Conventional Commits."""
    major = False
    minor = False
    patch = False

    for msg in messages:
        if "BREAKING CHANGE" in msg or "BREAKING-CHANGE" in msg:
            major = True
        subject = next((ln.strip() for ln in msg.splitlines() if ln.strip()), "")
        match = CONVENTIONAL_SUBJECT_RE.match(subject)
        if not match:
            continue
        typ = match.group("type").lower()
        breaking = match.group("breaking") == "!"
        if breaking:
            major = True
        if typ == "feat":
            minor = True
        if typ in {"fix", "perf", "refactor"}:
            patch = True

    if major:
        return "major"
    if minor:
        return "minor"
    if patch:
        return "patch"
    return "patch" if default_if_needed else None


def _commit_messages(repo: Repo, since_tag: str | None) -> list[str]:
    """Return commit messages since a tag (or all history if none)."""
    rev = f"{since_tag}..HEAD" if since_tag else "HEAD"

    def _as_str(value: str | bytes) -> str:
        return value.decode("utf-8", errors="replace") if isinstance(value, (bytes, bytearray)) else value

    return [_as_str(c.message) for c in repo.iter_commits(rev)]

def _commit_subjects(repo: Repo, since_tag: str | None, limit: int = 50) -> list[str]:
    """Return commit subjects since a tag (newest first)."""
    rev = f"{since_tag}..HEAD" if since_tag else "HEAD"
    subjects: list[str] = []

    def _as_str(value: str | bytes) -> str:
        return value.decode("utf-8", errors="replace") if isinstance(value, (bytes, bytearray)) else value

    for commit in repo.iter_commits(rev, max_count=limit):
        msg = _as_str(commit.message)
        subject = msg.splitlines()[0].strip()
        if subject:
            subjects.append(subject)
    return subjects


def _parse_strict_semver(value: str) -> Version:
    """Parse and validate that version is a plain `X.Y.Z` release."""
    parsed = Version(value)
    if parsed.release is None or len(parsed.release) != 3:
        raise ValueError(f"Version must be X.Y.Z (got {value!r})")
    if parsed.pre is not None or parsed.post is not None or parsed.dev is not None:
        raise ValueError(f"Version must be a plain release (got {value!r})")
    return parsed


def _bump_version(version: Version, bump: BumpLevel) -> Version:
    """Bump a version."""
    major, minor, patch = version.release
    if bump == "major":
        return Version(f"{major + 1}.0.0")
    if bump == "minor":
        return Version(f"{major}.{minor + 1}.0")
    return Version(f"{major}.{minor}.{patch + 1}")


def _write_pyproject_version(pyproject_path: Path, next_version: str) -> None:
    """Write `[project].version` using tomlkit (preserving formatting)."""
    # tomlkit has incomplete typing; treat document as `Any` for strict mypy.
    doc: Any = parse(pyproject_path.read_text(encoding="utf-8"))
    doc["project"]["version"] = next_version
    pyproject_path.write_text(str(dumps(doc)), encoding="utf-8")

def _build_tag_message(repo: Repo, since_tag: str | None, tag: str) -> str:
    """Build an annotated tag message including a short changelog."""
    subjects = _commit_subjects(repo, since_tag)
    lines = [tag, "", "Changes:"]
    if not subjects:
        lines.append("- (no commits found)")
    else:
        for subject in subjects:
            lines.append(f"- {subject}")
    return "\n".join(lines) + "\n"


def _tag_exists(repo: Repo, tag: str) -> bool:
    """Check if a tag exists locally."""
    return any(t.name == tag for t in repo.tags)


def _plan_release(
    repo: Repo,
    config: ReleaseConfig,
) -> ReleasePlan:
    """Compute the release plan."""
    last_tag = _get_last_tag(repo)
    changed = _changed_files(repo, last_tag)
    pyproject_version_only = _pyproject_version_only_changed(repo, last_tag)
    bump_worthy = _has_bump_worthy_changes(changed, pyproject_version_only)
    docs_only = _is_docs_only(changed)

    change_detection = ChangeDetectionResult(
        since_tag=last_tag,
        changed_files=changed,
        bump_worthy=bump_worthy,
        docs_only=docs_only,
        pyproject_version_only=pyproject_version_only,
    )

    pyproject = _load_pyproject(config.pyproject_path)
    current = _parse_strict_semver(pyproject.project.version)

    if config.force:
        bump_level: BumpLevel = config.bump_override or "patch"
        next_v = str(_bump_version(current, bump_level))
        tag = f"v{next_v}"
        return ReleasePlan(
            config=config,
            do_release=True,
            reason="force=true",
            change_detection=change_detection,
            version_decision=VersionDecision(
                bump_level=bump_level,
                current_version=str(current),
                next_version=next_v,
                tag=tag,
            ),
        )

    if docs_only and not bump_worthy:
        return ReleasePlan(
            config=config,
            do_release=False,
            reason="docs/meta-only changes since last tag",
            change_detection=change_detection,
        )

    if (not bump_worthy) and ("pyproject.toml" in changed) and pyproject_version_only:
        return ReleasePlan(
            config=config,
            do_release=False,
            reason="only pyproject.toml version changed since last tag",
            change_detection=change_detection,
        )

    if not bump_worthy:
        return ReleasePlan(
            config=config,
            do_release=False,
            reason="no bump-worthy changes detected since last tag",
            change_detection=change_detection,
        )

    if config.bump_override:
        bump_level = config.bump_override
        reason = "bump override"
    else:
        bump_level = _choose_bump_level(_commit_messages(repo, last_tag), default_if_needed=True) or "patch"
        reason = "conventional-commit analysis (default patch)"

    next_v = str(_bump_version(current, bump_level))
    tag = f"v{next_v}"
    return ReleasePlan(
        config=config,
        do_release=True,
        reason=reason,
        change_detection=change_detection,
        version_decision=VersionDecision(
            bump_level=bump_level,
            current_version=str(current),
            next_version=next_v,
            tag=tag,
        ),
    )


def _write_github_output(output_path: Path, plan: ReleasePlan) -> None:
    """Write outputs to GitHub Actions `$GITHUB_OUTPUT`."""
    with output_path.open("a", encoding="utf-8") as f:
        f.write(f"do_release={'true' if plan.do_release else 'false'}\n")
        if plan.version_decision is None:
            f.write("bump_level=\n")
            f.write("current_version=\n")
            f.write("next_version=\n")
            f.write("tag=\n")
        else:
            f.write(f"bump_level={plan.version_decision.bump_level}\n")
            f.write(f"current_version={plan.version_decision.current_version}\n")
            f.write(f"next_version={plan.version_decision.next_version}\n")
            f.write(f"tag={plan.version_decision.tag}\n")
        f.write(f"since_ref={plan.change_detection.since_tag or ''}\n")
        f.write(f"reason={plan.reason}\n")


def _write_github_output_with_result(output_path: Path, plan: ReleasePlan, result: GitOperationResult) -> None:
    """Write outputs including git operation results."""
    with output_path.open("a", encoding="utf-8") as f:
        f.write(f"commit_sha={result.commit_sha}\n")


def _print_plan(plan: ReleasePlan) -> None:
    """Pretty-print the plan."""
    cd = plan.change_detection
    CONSOLE.print(f"[bold]since_ref:[/bold] {cd.since_tag or '(none)'}")
    CONSOLE.print(f"[bold]do_release:[/bold] {plan.do_release}")
    CONSOLE.print(f"[bold]reason:[/bold] {plan.reason}")
    CONSOLE.print(f"[bold]changed_files:[/bold] {len(cd.changed_files)}")
    if plan.version_decision is not None:
        vd = plan.version_decision
        CONSOLE.print(f"[bold]bump_level:[/bold] {vd.bump_level}")
        CONSOLE.print(f"[bold]current_version:[/bold] {vd.current_version}")
        CONSOLE.print(f"[bold]next_version:[/bold] {vd.next_version}")
        CONSOLE.print(f"[bold]tag:[/bold] {vd.tag}")


@APP.command()
def main(
    pyproject: Path = typer.Option(Path("pyproject.toml"), exists=True, dir_okay=False),
    dry_run: bool = typer.Option(False, help="Compute and print plan without committing/tagging."),
    force: bool = typer.Option(False, help="Force a release even if changes are docs/meta-only."),
    bump: BumpLevel | None = typer.Option(None, help="Override bump level (patch/minor/major)."),
    github_output: Path | None = typer.Option(None, help="Path to $GITHUB_OUTPUT (overrides env)."),
) -> None:
    """Compute and optionally apply a release bump + tag."""
    repo = _repo()
    root = _repo_root(repo)
    pyproject_path = (root / pyproject).resolve()
    env = GitHubEnv()
    output_path = github_output or env.github_output
    config = ReleaseConfig(
        pyproject_path=pyproject_path,
        dry_run=dry_run,
        force=force,
        bump_override=bump,
        github_output=output_path,
    )

    plan = _plan_release(repo, config=config)
    _print_plan(plan)

    if config.github_output is not None:
        _write_github_output(config.github_output, plan)

    if not plan.do_release or config.dry_run:
        return

    assert plan.version_decision is not None
    tag = plan.version_decision.tag
    if _tag_exists(repo, tag):
        CONSOLE.print(f"[red]Refusing to create existing tag[/red] {tag}")
        raise typer.Exit(code=1)

    _write_pyproject_version(pyproject_path, plan.version_decision.next_version)
    repo.index.add([str(pyproject_path.relative_to(root))])
    commit = repo.index.commit(f"chore(release): {tag}")
    repo.create_tag(tag, message=_build_tag_message(repo, plan.change_detection.since_tag, tag), annotate=True)

    result = GitOperationResult(commit_sha=str(commit.hexsha), tag=tag)
    CONSOLE.print(f"[green]Created[/green] commit {result.commit_sha}")
    CONSOLE.print(f"[green]Created[/green] tag {result.tag}")
    if config.github_output is not None:
        _write_github_output_with_result(config.github_output, plan, result)


if __name__ == "__main__":
    APP()

