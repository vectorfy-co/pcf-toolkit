#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pydantic>=2.6",
#   "rich>=13.7",
#   "typer>=0.12",
# ]
# ///

"""Build a machine-readable schema snapshot from raw extraction.

This script reads `data/spec_raw.json` (produced by `scripts/extract_spec.py`)
and produces:

- `data/schema_snapshot.json`
- `src/pcf_toolkit/data/schema_snapshot.json` (packaged copy)
- `src/pcf_toolkit/data/spec_raw.json` (packaged copy of the raw extraction)
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Final

import typer
from pydantic import BaseModel, Field, RootModel
from rich.console import Console

APP = typer.Typer(add_completion=False)
CONSOLE: Final[Console] = Console()

RAW_PATH = Path("data/spec_raw.json")
OUTPUT_PATH = Path("data/schema_snapshot.json")
PACKAGE_OUTPUT_PATH = Path("src/pcf_toolkit/data/schema_snapshot.json")
PACKAGE_RAW_PATH = Path("src/pcf_toolkit/data/spec_raw.json")

PARAMETER_TABLES: Final[set[str]] = {"Parameters", "Properties", "Attributes"}


class Row(RootModel[dict[str, str]]):
    """A validated, header-keyed row extracted from an HTML table."""


class RawTable(BaseModel):
    """A raw HTML table extracted from Microsoft Learn."""

    label: str | None = Field(default=None, description="Optional table label/caption.")
    heading: str | None = Field(default=None, description="Nearest heading title for the table.")
    headers: list[str] = Field(default_factory=list, description="Header labels.")
    rows: list[list[str]] = Field(default_factory=list, description="Row cells, aligned with headers.")


class RawCodeBlock(BaseModel):
    """A code block extracted from Microsoft Learn."""

    language: str | None = Field(default=None, description="Optional language identifier.")
    code: str = Field(..., description="Code text.")
    heading: str | None = Field(default=None, description="Nearest heading title for the code block.")


class RawPage(BaseModel):
    """A raw page extracted from Microsoft Learn."""

    title: str = Field(default="", description="Page title (H1).")
    summary: str = Field(default="", description="Short summary paragraph.")
    available_for: list[str] = Field(default_factory=list, description="Availability list.")
    sections: dict[str, list[str]] = Field(default_factory=dict, description="Section text keyed by heading.")
    tables: list[RawTable] = Field(default_factory=list, description="Tables found on the page.")
    code_blocks: list[RawCodeBlock] = Field(default_factory=list, description="Code blocks found on the page.")
    slug: str = Field(..., description="Relative slug for the element page.")
    url: str = Field(..., description="Canonical URL for the page.")


class RawSpec(BaseModel):
    """Root payload of the raw extraction."""

    root_url: str = Field(..., description="Root URL used for extraction.")
    slugs: list[str] = Field(default_factory=list, description="Sorted list of page slugs.")
    pages: list[RawPage] = Field(default_factory=list, description="Extracted pages.")


class ElementSnapshot(BaseModel):
    """Normalized element snapshot keyed by slug."""

    title: str = Field(default="", description="Element title.")
    summary: str = Field(default="", description="Element summary.")
    available_for: list[str] = Field(default_factory=list, description="Availability list.")
    parameters: list[Row] = Field(default_factory=list, description="Parameters/properties/attributes rows.")
    child_elements: list[Row] = Field(default_factory=list, description="Child element rows.")
    parent_elements: list[Row] = Field(default_factory=list, description="Parent element rows.")
    value_tables: dict[str, list[Row]] = Field(default_factory=dict, description="Other tables keyed by label.")
    sections: dict[str, list[str]] = Field(default_factory=dict, description="Section text keyed by heading.")
    examples: list[RawCodeBlock] = Field(default_factory=list, description="Code examples.")
    url: str = Field(..., description="Canonical URL.")


class SchemaSnapshot(BaseModel):
    """Snapshot payload written to disk."""

    generated_at: datetime = Field(..., description="Generation timestamp (stable if contents unchanged).")
    root_url: str = Field(..., description="Root URL used for extraction.")
    slugs: list[str] = Field(default_factory=list, description="Sorted list of element slugs.")
    elements: dict[str, ElementSnapshot] = Field(default_factory=dict, description="Snapshots by slug.")


def _normalize_row(headers: list[str], row: list[str]) -> Row:
    """Convert a list row into a header-keyed `Row`.

    Args:
      headers: Column headers.
      row: Row cell values.

    Returns:
      Validated `Row`.
    """
    keyed = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
    return Row.model_validate(keyed)


def _extract_tables(page: RawPage) -> dict[str, list[Row]]:
    """Extract and normalize all tables in a page."""
    result: dict[str, list[Row]] = {}
    for table in page.tables:
        label = table.label or table.heading or "Table"
        rows = [_normalize_row(table.headers, row) for row in table.rows]
        result.setdefault(label, []).extend(rows)
    return result


def build_snapshot(raw: RawSpec) -> SchemaSnapshot:
    """Build a normalized snapshot from the raw extraction.

    Args:
      raw: Validated raw extraction.

    Returns:
      Snapshot model.
    """
    elements: dict[str, ElementSnapshot] = {}
    for page in raw.pages:
        slug = page.slug.strip()
        if not slug:
            continue
        tables = _extract_tables(page)
        parameters = [row for label, rows in tables.items() if label in PARAMETER_TABLES for row in rows]
        child_elements = (tables.get("Child Elements", []) + tables.get("Child Element", []))
        parent_elements = (tables.get("Parent Elements", []) + tables.get("Parent Element", []))
        value_tables = {
            key: rows
            for key, rows in tables.items()
            if key not in PARAMETER_TABLES
            and key not in {"Child Elements", "Child Element", "Parent Elements", "Parent Element"}
        }
        elements[slug] = ElementSnapshot(
            title=page.title,
            summary=page.summary,
            available_for=page.available_for,
            parameters=parameters,
            child_elements=child_elements,
            parent_elements=parent_elements,
            value_tables=value_tables,
            sections=page.sections,
            examples=page.code_blocks,
            url=page.url,
        )

    return SchemaSnapshot(
        generated_at=datetime.now(UTC),
        root_url=raw.root_url,
        slugs=raw.slugs,
        elements=elements,
    )


def _strip_generated_at(snapshot: SchemaSnapshot) -> dict[str, object]:
    """Dump snapshot excluding `generated_at` for stable comparisons."""
    return snapshot.model_dump(mode="python", exclude={"generated_at"})


def _stable_generated_at(snapshot: SchemaSnapshot, path: Path) -> SchemaSnapshot:
    """Preserve `generated_at` if contents are unchanged from existing file."""
    if not path.exists():
        return snapshot
    try:
        existing = SchemaSnapshot.model_validate_json(path.read_text(encoding="utf-8"))
    except ValueError:
        return snapshot
    if _strip_generated_at(existing) == _strip_generated_at(snapshot):
        return snapshot.model_copy(update={"generated_at": existing.generated_at})
    return snapshot


@APP.command()
def main() -> None:
    """Read raw extraction and write normalized snapshots."""
    raw = RawSpec.model_validate_json(RAW_PATH.read_text(encoding="utf-8"))
    snapshot = _stable_generated_at(build_snapshot(raw), OUTPUT_PATH)

    # Use consistent JSON formatting with explicit newline at EOF
    json_output = snapshot.model_dump_json(indent=2) + "\n"
    OUTPUT_PATH.write_text(json_output, encoding="utf-8")
    PACKAGE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE_OUTPUT_PATH.write_text(json_output, encoding="utf-8")
    PACKAGE_RAW_PATH.write_text(RAW_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    CONSOLE.print(f"[green]Wrote[/green] {OUTPUT_PATH}")
    CONSOLE.print(f"[green]Wrote[/green] {PACKAGE_OUTPUT_PATH}")


if __name__ == "__main__":
    APP()
