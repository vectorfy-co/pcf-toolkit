"""Build JSON Schema for manifest validation."""

from __future__ import annotations

from pathlib import Path

from pcf_toolkit.json_schema import manifest_schema_text

OUTPUT_PATH = Path("schemas/pcf-manifest.schema.json")
PACKAGE_OUTPUT_PATH = Path("src/pcf_toolkit/data/manifest.schema.json")


def main() -> None:
    schema_text = manifest_schema_text()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(schema_text, encoding="utf-8")
    PACKAGE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE_OUTPUT_PATH.write_text(schema_text, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Wrote {PACKAGE_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
