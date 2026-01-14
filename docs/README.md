---
title: PCF Toolkit Docs
description: Developer-first docs for PCF Toolkit — manifest authoring, deterministic XML, and local proxy workflows for Power Apps PCF.
---

# Build PCF controls without the publish loop

PCF Toolkit gives Power Apps developers a faster, cleaner workflow for PCF manifests and local debugging. Author your manifest in YAML/JSON, generate deterministic XML on demand, and proxy local webresources so you can iterate without republishing.

<div class="cards">
  <div class="card">
    <strong>What it is</strong>
    <p>A Python CLI that turns PCF manifests into code, backed by schema validation and a local proxy workflow.</p>
  </div>
  <div class="card">
    <strong>Why it matters</strong>
    <p>Shorter feedback loops, safer diffs, and less time spent wrangling XML or republishing controls.</p>
  </div>
  <div class="card">
    <strong>How it works</strong>
    <p>Write YAML/JSON → validate → generate deterministic XML → proxy local builds during runtime.</p>
  </div>
</div>

<a href="#/guide/quickstart" class="button primary">Start in 5 minutes</a>
<a href="#/manifest/overview" class="button secondary">Jump to manifest docs</a>

## The problems it solves

- **Publish-loop fatigue**: The default PCF loop often requires publishing just to see a change. The proxy workflow keeps the runtime pointed at your local build output.
- **XML friction**: ControlManifest.Input.xml is verbose and error-prone. YAML/JSON is cleaner and easier to review.
- **Unstable diffs**: Deterministic serialization means your diffs stay stable, so reviews and audits are faster.
- **Missing validation**: Schema-based validation and strong typing give immediate, actionable feedback.

## Value proposition

**PCF Toolkit replaces repetitive manual work with a consistent, automatable pipeline.**

- **Develop faster**: keep Power Apps running and serve fresh builds locally.
- **Ship safely**: validate manifests against the same schema every time.
- **Collaborate better**: keep manifests human-readable and diff-friendly.

## Use cases

- **Local dev**: iterate on PCF controls without republishing every change.
- **CI/CD**: validate manifests and generate XML as part of a build.
- **Legacy upgrades**: import existing XML and keep authoring in YAML/JSON.

## Quick start (summary)

```bash
uv tool install pcf-toolkit@latest
pcf-toolkit proxy init
pcf-toolkit proxy start MyComponent
```

Need more detail? See the full [Quick Start](guide/quickstart.md).

## How it compares

| Workflow | With PCF Toolkit | Without PCF Toolkit |
| --- | --- | --- |
| Edit manifest | YAML/JSON with schema validation | Manual XML edits |
| Diffs | Deterministic, stable | Non-deterministic noise |
| Local testing | Proxy local webresources | Publish loop |
| CI automation | CLI commands | Custom scripts |

## What’s inside

- **Manifest tooling**: validate, generate, import, export schema.
- **Proxy workflow**: mitmproxy + local HTTP server + PAC CLI integration.
- **Developer utilities**: examples and doctor checks.

## Next steps

- [Install the toolkit](guide/installation.md)
- [Author your first manifest](manifest/overview.md)
- [Run the local proxy](proxy/overview.md)

---

> Tip: Looking for keyboard navigation? See [Keyboard Shortcuts](meta/keyboard-shortcuts.md).
