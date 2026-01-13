"""Build a machine-readable schema snapshot from raw extraction."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

RAW_PATH = Path("data/spec_raw.json")
OUTPUT_PATH = Path("data/schema_snapshot.json")
PACKAGE_OUTPUT_PATH = Path("src/pcf_toolkit/data/schema_snapshot.json")
PACKAGE_RAW_PATH = Path("src/pcf_toolkit/data/spec_raw.json")

PARAMETER_TABLES = {"Parameters", "Properties", "Attributes"}


def _normalize_row(headers: list[str], row: list[str]) -> dict[str, str]:
    return {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}


def _extract_tables(page: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for table in page.get("tables", []):
        label = table.get("label") or table.get("heading") or "Table"
        headers = table.get("headers", [])
        rows = []
        for row in table.get("rows", []):
            rows.append(_normalize_row(headers, row))
        result.setdefault(label, []).extend(rows)
    return result


def build_snapshot() -> dict[str, Any]:
    payload = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    elements: dict[str, Any] = {}

    for page in payload.get("pages", []):
        slug = page.get("slug")
        if not slug:
            continue
        tables = _extract_tables(page)
        elements[slug] = {
            "title": page.get("title"),
            "summary": page.get("summary"),
            "available_for": page.get("available_for"),
            "parameters": [row for label, rows in tables.items() if label in PARAMETER_TABLES for row in rows],
            "child_elements": tables.get("Child Elements", []) + tables.get("Child Element", []),
            "parent_elements": tables.get("Parent Elements", []) + tables.get("Parent Element", []),
            "value_tables": {
                key: rows
                for key, rows in tables.items()
                if key not in PARAMETER_TABLES
                and key not in {"Child Elements", "Child Element", "Parent Elements", "Parent Element"}
            },
            "sections": page.get("sections"),
            "examples": page.get("code_blocks"),
            "url": page.get("url"),
        }

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "root_url": payload.get("root_url"),
        "slugs": payload.get("slugs"),
        "elements": elements,
    }


def _strip_generated_at(snapshot: dict[str, Any]) -> dict[str, Any]:
    data = dict(snapshot)
    data.pop("generated_at", None)
    return data


def _stable_generated_at(snapshot: dict[str, Any], path: Path) -> dict[str, Any]:
    if not path.exists():
        return snapshot
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return snapshot
    if _strip_generated_at(existing) == _strip_generated_at(snapshot):
        snapshot["generated_at"] = existing.get("generated_at", snapshot["generated_at"])
    return snapshot


def main() -> None:
    snapshot = build_snapshot()
    snapshot = _stable_generated_at(snapshot, OUTPUT_PATH)
    OUTPUT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=True), encoding="utf-8")
    PACKAGE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE_OUTPUT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=True), encoding="utf-8")
    PACKAGE_RAW_PATH.write_text(RAW_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {PACKAGE_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
