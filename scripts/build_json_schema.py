#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pydantic>=2.6",
#   "pyyaml>=6.0",
#   "rich>=13.7",
#   "typer>=0.12",
# ]
# ///

"""Build JSON Schema for manifest validation.

This script generates `schemas/pcf-manifest.schema.json` and also writes a copy
into the package at `src/pcf_toolkit/data/manifest.schema.json`.

Note:
  This script imports the local `pcf_toolkit` package from `src/` directly so it
  can run in uv script mode without installing the project.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

import typer
from rich.console import Console

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from pcf_toolkit.json_schema import manifest_schema_text  # noqa: E402

APP = typer.Typer(add_completion=False)
CONSOLE: Final[Console] = Console()

OUTPUT_PATH = Path("schemas/pcf-manifest.schema.json")
PACKAGE_OUTPUT_PATH = Path("src/pcf_toolkit/data/manifest.schema.json")


@APP.command()
def main() -> None:
    """Generate and write the manifest JSON Schema."""
    schema_text = manifest_schema_text()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(schema_text, encoding="utf-8")
    PACKAGE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE_OUTPUT_PATH.write_text(schema_text, encoding="utf-8")
    CONSOLE.print(f"[green]Wrote[/green] {OUTPUT_PATH}")
    CONSOLE.print(f"[green]Wrote[/green] {PACKAGE_OUTPUT_PATH}")


if __name__ == "__main__":
    APP()
