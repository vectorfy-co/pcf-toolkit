"""Generate JSON Schema for PCF manifest YAML/JSON validation."""

from __future__ import annotations

import json
from typing import Any

from pcf_manifest_toolkit.models import Manifest


JSON_SCHEMA_URL = "https://json-schema.org/draft/2020-12/schema"


def manifest_schema() -> dict[str, Any]:
    """Return the JSON Schema for the manifest model."""
    schema = Manifest.model_json_schema(by_alias=True)
    schema["$schema"] = JSON_SCHEMA_URL
    return schema


def manifest_schema_text() -> str:
    """Return the JSON Schema as pretty-printed JSON."""
    return json.dumps(manifest_schema(), indent=2, ensure_ascii=True)
