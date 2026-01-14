---
title: Quick Start
description: Get PCF Toolkit running in under 5 minutes with a manifest workflow and local proxy.
---

# Quick Start

This guide assumes you already have a PCF component project and a build output under `out/controls/<Component>`.

## 1) Install (recommended)

```bash
uv tool install pcf-toolkit@latest
```

No `uv` yet? See [Installation](guide/installation.md).

## 2) Create a proxy config

```bash
pcf-toolkit proxy init
```

This writes `pcf-proxy.yaml` in your project root and optionally adds `dev:proxy` to `package.json`.

## 3) Build your control

Make sure your build outputs to `out/controls/<Component>` (default). If your build output is different, update `bundle.dist_path` in `pcf-proxy.yaml`.

## 4) Start the proxy

```bash
pcf-toolkit proxy start MyNamespace.MyComponent
```

Component names follow the `namespace.constructor` format. If you are unsure, use auto-detect.


If the component name is unknown, you can use auto-detection:

```bash
pcf-toolkit proxy start auto
```

## Verify it works

- Your browser opens with the correct proxy settings (unless disabled).
- The console shows the proxy ports and active component.
- Requests to `/webresources/<Component>/...` resolve to your local build output.

## 60-second mental model

Think of the proxy as a **local mirror**. Power Apps asks for webresources, and the proxy swaps the response with your local build output. No publish step required.

## Next

- [Architecture Overview](guide/architecture.md)
- [Proxy workflow details](proxy/workflow.md)
