---
title: Manifest Overview
description: Author PCF ControlManifest.Input.xml as YAML or JSON with schema validation and deterministic output.
---

# Manifest Overview

PCF Toolkit lets you author the PCF manifest as **YAML or JSON** and generate `ControlManifest.Input.xml` deterministically.

## Why this matters

XML is great for machines but hard for humans. YAML/JSON gives you structure, typing, and better diffs -- without changing how Power Apps consumes the manifest.

## Authoring formats

- **YAML**: human-friendly and concise
- **JSON**: explicit and tooling-friendly

Both formats map to the same schema.

## Schema header (YAML)

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/vectorfy-co/pcf-toolkit/refs/heads/main/schemas/pcf-manifest.schema.json
```

## Minimal manifest

```yaml
control:
  namespace: MyNameSpace
  constructor: MyControl
  version: 1.0.0
  display-name-key: MyControl_Display_Key
  resources:
    code:
      path: index.ts
      order: 1
```

## Validation and generation

```bash
pcf-toolkit validate manifest.yaml
pcf-toolkit generate manifest.yaml -o ControlManifest.Input.xml
```


## Schema rules

- Unknown keys are rejected (strict validation).
- Required fields must be present.
- Lists such as `type-group.type` and `property.types` must not be empty.

## Structure at a glance

```
control
- properties
- events
- data-set
- type-group
- feature-usage
- external-service-usage
- platform-action
- resources
```

Start with [Control](manifest/control.md) or jump straight to the [Full Example](manifest/full-example.md).
