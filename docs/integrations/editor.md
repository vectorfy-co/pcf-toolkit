---
title: Editor Setup
description: Configure IDE validation using the PCF manifest JSON Schema.
---

# Editor Setup

PCF Toolkit ships JSON Schema for the manifest, enabling editor validation and auto-complete.

## YAML schema directive (recommended)

Add to the top of your manifest file:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/vectorfy-co/pcf-toolkit/refs/heads/main/schemas/pcf-manifest.schema.json
```

## VS Code settings

```json
{
  "yaml.schemas": {
    "https://raw.githubusercontent.com/vectorfy-co/pcf-toolkit/refs/heads/main/schemas/pcf-manifest.schema.json": "**/manifest*.yaml"
  }
}
```

## JSON schema

For JSON, you can include `$schema` directly:

```json
{
  "$schema": "https://raw.githubusercontent.com/vectorfy-co/pcf-toolkit/refs/heads/main/schemas/pcf-manifest.schema.json",
  "control": {
    "namespace": "MyNamespace",
    "constructor": "MyControl",
    "version": "1.0.0",
    "display-name-key": "MY_CONTROL_NAME",
    "resources": {
      "code": {"path": "index.ts", "order": 1}
    }
  }
}
```

Next: [Python API](api/python.md)
