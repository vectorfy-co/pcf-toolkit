---
title: Events
description: Define event elements for PCF controls.
---

# Events

Events describe events raised by your control. They appear under `control.event`.

## event fields

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Event name (required). |
| `display-name-key` | string | Display name key. |
| `description-key` | string | Description key. |
| `pfx-default-value` | string | Default value for Power Fx. |

## Example

```yaml
event:
  - name: OnItemSelected
    display-name-key: EVENT_SELECTED_LABEL
    description-key: EVENT_SELECTED_DESC
    pfx-default-value: ""
```

Next: [Dependencies](manifest/dependencies.md)
