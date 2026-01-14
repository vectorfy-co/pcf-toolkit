---
title: Dependencies
description: Declare dependent control libraries in the manifest resources section.
---

# Dependencies

Dependencies are declared under `resources.dependency` and represent other control libraries your component requires.

## dependency fields

| Field | Type | Description |
| --- | --- | --- |
| `type` | `control` | Dependency type (required). |
| `name` | string | Schema name of the dependency (required). |
| `order` | integer | Optional load order. |
| `load-type` | `onDemand` | Optional load type. |

## Example

```yaml
resources:
  dependency:
    - type: control
      name: samples_SampleNS.SampleStubLibraryPCF
      load-type: onDemand
```

Next: [Type Groups](manifest/type-groups.md)
