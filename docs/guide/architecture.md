---
title: Architecture Overview
description: Understand the PCF Toolkit architecture, data flow, and core components.
---

# Architecture Overview

PCF Toolkit is composed of two main subsystems:

1. **Manifest tooling**: YAML/JSON → validation → deterministic XML output.
2. **Proxy workflow**: local webresource proxy using mitmproxy + a local HTTP server.

## Manifest tooling flow

```text
YAML/JSON → Pydantic validation → deterministic XML serializer → ControlManifest.Input.xml
```

- **Pydantic models** enforce the PCF schema.
- **Serialization** produces stable, ordered XML for clean diffs.
- **Schema export** provides JSON Schema for editor validation.

## Proxy flow

```text
Power Apps request → mitmproxy intercept → rewrite webresource → local HTTP server → built files
```

Key components:

- `pcf_toolkit.proxy.mitm`: spawns and manages mitmproxy
- `pcf_toolkit.proxy.server`: serves local files
- `pcf_toolkit.proxy.addons.redirect_bundle`: rewrites webresource paths
- `pcf_toolkit.proxy.doctor`: validates prerequisites (ports, certs, dist paths)

## Where configuration lives

- **Manifest**: YAML/JSON file you author.
- **Proxy**: `pcf-proxy.yaml` or `pcf-proxy.json`.
- **Schemas**: `schemas/pcf-manifest.schema.json` and `schemas/pcf-proxy.schema.json`.

## Why deterministic XML matters

Think of XML as the “assembly output” of your manifest. When the output is deterministic, every build is predictable, making diffs, reviews, and CI gates reliable.

Next: [Manifest Authoring](manifest/overview.md)
