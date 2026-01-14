---
title: Full Manifest Example
description: A comprehensive YAML manifest example using most available options.
---

# Full Manifest Example

This example is intentionally comprehensive. Use it as a reference and trim to your needs.

```yaml
control:
  namespace: Vectorfy
  constructor: TaskBoard
  version: 1.2.0
  display-name-key: TASKBOARD_NAME
  description-key: TASKBOARD_DESC
  control-type: standard
  preview-image: img/preview.png
  type-group:
    - name: NumericLike
      type:
        - value: Decimal
        - value: Whole.None
  property:
    - name: title
      display-name-key: TITLE_LABEL
      description-key: TITLE_DESC
      of-type: SingleLine.Text
      usage: bound
      required: true
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
    - name: amount
      display-name-key: AMOUNT_LABEL
      of-type-group: NumericLike
      usage: input
  event:
    - name: OnItemSelected
      display-name-key: EVENT_SELECTED_LABEL
      description-key: EVENT_SELECTED_DESC
  data-set:
    - name: Items
      display-name-key: ITEMS_LABEL
      description-key: ITEMS_DESC
      property-set:
        - name: Title
          display-name-key: TITLE_LABEL
          of-type: SingleLine.Text
          usage: bound
        - name: Amount
          display-name-key: AMOUNT_LABEL
          of-type: Decimal
          usage: bound
  property-dependencies:
    property-dependency:
      - input: selectedId
        output: selectedRecord
        required-for: schema
  feature-usage:
    uses-feature:
      - name: Utility
        required: true
  external-service-usage:
    enabled: true
    domain:
      - value: api.contoso.com
  platform-action:
    action-type: afterPageLoad
  resources:
    code:
      path: index.ts
      order: 1
    css:
      - path: css/control.css
        order: 1
    img:
      - path: img/preview.png
    resx:
      - path: strings/Control.1033.resx
        version: 1.0.0
    platform-library:
      - name: React
        version: 16.14.0
    dependency:
      - type: control
        name: samples_SampleNS.SampleStubLibraryPCF
        load-type: onDemand
```

Next: [Proxy Overview](proxy/overview.md)
