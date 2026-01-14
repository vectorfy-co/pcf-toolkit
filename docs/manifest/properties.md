---
title: Properties
description: Property definitions for PCF controls, including types, usage, and enum values.
---

# Properties

Properties define the inputs/outputs exposed by your control. Each property entry appears under `control.property`.

## Property fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Property name (required). |
| `display-name-key` | string | Localized display name key. |
| `description-key` | string | Localized description key. |
| `of-type` | enum | Built-in type (see list below). |
| `of-type-group` | string | Custom type-group name. |
| `usage` | `bound` \| `input` \| `output` | Property usage. |
| `required` | boolean | Mark the property required. |
| `default-value` | string | Default value for the property. |
| `pfx-default-value` | string | Default value for Power Fx. |
| `types` | object | Type list (required for some composite types). |
| `value` | array | Enum values (only when `of-type: Enum`). |

### Supported `of-type` values

```
Currency
DateAndTime.DateAndTime
DateAndTime.DateOnly
Decimal
Enum
FP
Lookup.Simple
Multiple
MultiSelectOptionSet
Object
OptionSet
SingleLine.Email
SingleLine.Phone
SingleLine.Text
SingleLine.TextArea
SingleLine.Ticker
SingleLine.URL
TwoOptions
Whole.None
```

> Note: some PCF platform types are not supported by the schema (e.g. `Lookup.Customer`, `Status`, `Whole.Duration`). Keep those out of your manifest or handle them externally.

## Example: bound property

```yaml
property:
  - name: title
    display-name-key: TITLE_LABEL
    description-key: TITLE_DESC
    of-type: SingleLine.Text
    usage: bound
    required: true
```

## Example: enum property

```yaml
property:
  - name: status
    display-name-key: STATUS_LABEL
    of-type: Enum
    usage: input
    value:
      - name: New
        display-name-key: STATUS_NEW
        value: 0
      - name: Active
        display-name-key: STATUS_ACTIVE
        value: 1
```

## Example: custom type group

```yaml
control:
  type-group:
    - name: NumericLike
      type:
        - value: Decimal
        - value: Whole.None
  property:
    - name: amount
      display-name-key: AMOUNT_LABEL
      of-type-group: NumericLike
      usage: input
```

Next: [Property Sets](manifest/property-sets.md)
