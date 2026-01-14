---
title: CI/CD Integration
description: Automate manifest validation and schema generation in CI pipelines.
---

# CI/CD Integration

PCF Toolkit is designed to run in CI. Typical tasks include validation, XML generation, and schema export.

## Common CI tasks

- Validate manifests
- Generate `ControlManifest.Input.xml`
- Regenerate `schemas/pcf-manifest.schema.json`
- Fail builds on schema drift

## GitHub Actions example

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: uv sync --extra dev
      - run: uv run --python 3.13 pytest
      - run: uv run --python 3.13 --script scripts/build_schema_snapshot.py
      - run: uv run --python 3.13 --script scripts/build_json_schema.py
      - run: git diff --exit-code
```

## Validation in CI

```bash
pcf-toolkit validate path/to/manifest.yaml
```

## XML generation in CI

```bash
pcf-toolkit generate path/to/manifest.yaml -o ControlManifest.Input.xml
```

Next: [Editor Setup](integrations/editor.md)
