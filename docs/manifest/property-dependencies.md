---
title: Property Dependencies
description: Define dependencies between properties for schema-aware behavior.
---

# Property Dependencies

`property-dependencies` defines relationships between properties when one depends on another (e.g., schema validation behavior).

## property-dependencies fields

| Field | Type | Description |
| --- | --- | --- |
| `property-dependency` | array | List of dependencies (required). |

Each dependency contains:

| Field | Type | Description |
| --- | --- | --- |
| `input` | string | Input property name. |
| `output` | string | Output property name. |
| `required-for` | `schema` | Required-for value. |

## Example

```yaml
property-dependencies:
  property-dependency:
    - input: selectedId
      output: selectedRecord
      required-for: schema
```

Next: [Feature Usage](manifest/feature-usage.md)
