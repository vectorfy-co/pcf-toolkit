---
title: External Service Usage
description: Declare external service usage and required domains.
---

# External Service Usage

`external-service-usage` is used to declare when your control calls external services.

## external-service-usage fields

| Field | Type | Description |
| --- | --- | --- |
| `enabled` | boolean | Whether external services are used. |
| `domain` | array | Domains referenced by the control. Required when enabled. |

Each domain entry contains:

| Field | Type | Description |
| --- | --- | --- |
| `value` | string | Domain name. |

## Example

```yaml
external-service-usage:
  enabled: true
  domain:
    - value: api.contoso.com
    - value: cdn.contoso.com
```

Next: [Platform Action](manifest/platform-action.md)
