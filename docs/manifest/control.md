---
title: Control Element
description: Reference for the control element and its required and optional fields.
---

# Control element

The root of every manifest is the `control` object. It describes the component and links to resources, properties, and optional behaviors.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `namespace` | string | Component namespace. |
| `constructor` | string | Component constructor/class name. |
| `version` | string | Component version (semantic recommended). |
| `display-name-key` | string | Localized display name key. |
| `resources` | object | Resource declarations (see [Resources](manifest/resources.md)). |

## Optional fields

| Field | Type | Description |
| --- | --- | --- |
| `description-key` | string | Localized description key. |
| `control-type` | `standard` \| `virtual` | Control type. |
| `preview-image` | string | Path to preview image. |
| `property` | array | Property definitions. |
| `event` | array | Event definitions. |
| `data-set` | array | Dataset definitions. |
| `type-group` | array | Custom type groups. |
| `property-dependencies` | object | Property dependency mapping. |
| `feature-usage` | object | Feature usage declarations. |
| `external-service-usage` | object | External service declaration. |
| `platform-action` | object | Platform action settings. |

## Example

```yaml
control:
  namespace: Contoso
  constructor: TaskBoard
  version: 1.2.0
  display-name-key: TASKBOARD_NAME
  description-key: TASKBOARD_DESC
  control-type: standard
  preview-image: img/preview.png
  resources:
    code:
      path: index.ts
      order: 1
```

Next: [Properties](manifest/properties.md)
