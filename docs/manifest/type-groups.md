---
title: Type Groups
description: Define reusable type groups to simplify property type definitions.
---

# Type Groups

Type groups let you define a reusable list of types that can be referenced by properties.

## type-group fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Type group name (required). |
| `type` | array | List of type elements (required). |

Each `type` entry contains:

| Field | Type | Description |
| --- | --- | --- |
| `value` | enum | One of the supported `TypeValue` enums. |

## Example

```yaml
control:
  type-group:
    - name: NumericLike
      type:
        - value: Decimal
        - value: Whole.None
```

Use it in a property:

```yaml
property:
  - name: amount
    display-name-key: AMOUNT_LABEL
    of-type-group: NumericLike
    usage: input
```

Next: [Property Dependencies](manifest/property-dependencies.md)
