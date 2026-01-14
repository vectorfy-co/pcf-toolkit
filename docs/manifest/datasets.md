---
title: Data Sets
description: Define data-set elements for dataset-bound PCF controls.
---

# Data Sets

`data-set` is used for dataset-bound controls. It defines columns (via property sets) and optional CDS settings.

## data-set fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Dataset name (required). |
| `display-name-key` | string | Display name key (required). |
| `description-key` | string | Description key. |
| `cds-data-set-options` | string | Optional dataset options. |
| `property-set` | array | Column definitions (required). |

## Example

```yaml
data-set:
  - name: Records
    display-name-key: RECORDS_LABEL
    description-key: RECORDS_DESC
    cds-data-set-options: "DisplayName,PrimaryId"
    property-set:
      - name: Title
        display-name-key: TITLE_LABEL
        of-type: SingleLine.Text
        usage: bound
      - name: CreatedOn
        display-name-key: CREATED_LABEL
        of-type: DateAndTime.DateAndTime
        usage: bound
```

Next: [Events](manifest/events.md)
