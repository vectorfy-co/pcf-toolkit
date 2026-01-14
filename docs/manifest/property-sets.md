---
title: Property Sets
description: Reference for property sets used in data-set definitions.
---

# Property Sets

`property-set` entries are used inside `data-set` definitions to describe dataset columns and their data types.

## Property-set fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Property set name (required). |
| `display-name-key` | string | Display name key (required). |
| `description-key` | string | Description key. |
| `of-type` | enum | Built-in type. |
| `of-type-group` | string | Custom type-group name. |
| `usage` | `bound` \| `input` | Usage for dataset columns. |
| `required` | boolean | Required column. |
| `types` | object | Type list (when composite types are used). |

## Example

```yaml
data-set:
  - name: Items
    display-name-key: ITEMS_LABEL
    property-set:
      - name: Title
        display-name-key: TITLE_LABEL
        of-type: SingleLine.Text
        usage: bound
      - name: Amount
        display-name-key: AMOUNT_LABEL
        of-type: Decimal
        usage: bound
```

Next: [Resources](manifest/resources.md)
