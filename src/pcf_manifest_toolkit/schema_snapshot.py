"""Utilities for schema snapshot export."""

from __future__ import annotations

from importlib import resources
from pathlib import Path


def load_schema_snapshot() -> str:
    """Load the schema snapshot JSON as a string."""
    package_path = _read_package_snapshot()
    if package_path is not None:
        return package_path

    file_path = Path("data/schema_snapshot.json")
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")

    fallback = Path("data/spec_raw.json")
    if fallback.exists():
        return fallback.read_text(encoding="utf-8")

    raise FileNotFoundError("schema snapshot not found")


def _read_package_snapshot() -> str | None:
    try:
        with resources.files("pcf_manifest_toolkit.data").joinpath(
            "schema_snapshot.json"
        ).open("r", encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        return None
    except ModuleNotFoundError:
        return None
