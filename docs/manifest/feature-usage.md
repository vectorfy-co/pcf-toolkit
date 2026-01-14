---
title: Feature Usage
description: Declare platform features used by your PCF control.
---

# Feature Usage

Feature usage declarations tell the platform what features the control relies on.

## feature-usage fields

| Field | Type | Description |
| --- | --- | --- |
| `uses-feature` | array | List of features used. |

Each feature entry contains:

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Feature name. |
| `required` | boolean | Whether the feature is required. |

## Example

```yaml
feature-usage:
  uses-feature:
    - name: Utility
      required: true
```

Next: [External Service Usage](manifest/external-services.md)
