---
title: Resources
description: Reference for resources: code, CSS, images, resx, platform libraries, and dependencies.
---

# Resources

`resources` is required and defines the files your control depends on.

## resources fields

| Field | Type | Description |
| --- | --- | --- |
| `code` | object | Main script entry (required). |
| `css` | array | CSS resources. |
| `img` | array | Image resources. |
| `resx` | array | Localized string resources. |
| `platform-library` | array | Platform libraries (React, Fluent). |
| `dependency` | array | Dependent control libraries. |

## code

| Field | Type | Description |
| --- | --- | --- |
| `path` | string | Path to the script file. |
| `order` | integer | Load order. |

## css

| Field | Type | Description |
| --- | --- | --- |
| `path` | string | Path to the CSS file. |
| `order` | integer | Load order. |

## img

| Field | Type | Description |
| --- | --- | --- |
| `path` | string | Image path. |

## resx

| Field | Type | Description |
| --- | --- | --- |
| `path` | string | Path to .resx file. |
| `version` | string | Resource version. |

## platform-library

| Field | Type | Description |
| --- | --- | --- |
| `name` | `React` \| `Fluent` | Platform library name. |
| `version` | string | Library version. |

## dependency

| Field | Type | Description |
| --- | --- | --- |
| `type` | `control` | Dependency type. |
| `name` | string | Schema name of the control. |
| `order` | integer | Optional load order. |
| `load-type` | `onDemand` | Optional load type. |

## Example

```yaml
resources:
  code:
    path: index.ts
    order: 1
  css:
    - path: css/controls.css
      order: 1
  resx:
    - path: strings/Control.1033.resx
      version: 1.0.0
  platform-library:
    - name: React
      version: 16.14.0
```

Next: [Data Sets](manifest/datasets.md)
