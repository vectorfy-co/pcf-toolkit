"""Load manifest definitions from JSON or YAML."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import yaml

from pcf_manifest_toolkit.models import Manifest


def load_manifest(path: str) -> Manifest:
    """Load a manifest definition from JSON or YAML.

    Args:
      path: Path to the input file, or '-' to read from stdin.

    Returns:
      A validated Manifest instance.
    """
    data = _load_data(path)
    return Manifest.model_validate(data)


def _load_data(path: str) -> dict[str, Any]:
    if path == "-":
        raw = sys.stdin.read()
        return _loads_by_content(raw)

    file_path = Path(path)
    raw = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(raw)
    if file_path.suffix.lower() == ".json":
        return json.loads(raw)
    return _loads_by_content(raw)


def _loads_by_content(raw: str) -> dict[str, Any]:
    stripped = raw.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return json.loads(raw)
    return yaml.safe_load(raw)
