---
title: Python API
description: Programmatic usage of PCF Toolkit modules for validation and XML generation.
---

# Python API

The CLI is the primary interface, but advanced users can leverage the internal modules directly.

> These APIs are considered internal. Pin your dependency version if you use them in production scripts.

## Load and validate a manifest

```python
from pcf_toolkit.io import load_manifest

manifest = load_manifest("manifest.yaml")
```

If validation fails, `pydantic.ValidationError` is raised.

## Generate deterministic XML

```python
from pcf_toolkit.io import load_manifest
from pcf_toolkit.xml import ManifestXmlSerializer

manifest = load_manifest("manifest.yaml")
serializer = ManifestXmlSerializer(xml_declaration=True)
xml_text = serializer.to_string(manifest)

with open("ControlManifest.Input.xml", "w", encoding="utf-8") as f:
    f.write(xml_text)
```

## Parse an existing XML manifest

```python
from pcf_toolkit.xml_import import parse_manifest_xml_path

raw = parse_manifest_xml_path("ControlManifest.Input.xml")
```

If you need strong typing, validate the parsed structure:

```python
from pcf_toolkit.models import Manifest

manifest = Manifest.model_validate(raw)
```

## Export JSON Schema

```python
from pcf_toolkit.json_schema import manifest_schema_text

schema_text = manifest_schema_text()
```

Next: [Best Practices](advanced/best-practices.md)
