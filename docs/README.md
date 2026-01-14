---
title: PCF Toolkit Docs
description: Developer-first docs for PCF Toolkit — manifest authoring, deterministic XML, and local proxy workflows for Power Apps PCF.
---

# Build PCF controls without the publish loop

PCF Toolkit gives Power Apps developers a faster, cleaner workflow for PCF manifests and local debugging. Author your manifest in YAML/JSON, generate deterministic XML on demand, and proxy local webresources so you can iterate without republishing.

<div class="cards">
  <div class="card">
    <strong>✨ Manifest as Code</strong>
    <p>Strong typing and JSON Schema validation keep ControlManifest.Input.xml clean and reviewable.</p>
  </div>
  <div class="card">
    <strong>⚡ Local Proxy Dev</strong>
    <p>Serve your built control locally while Power Apps runs—no publish loop required.</p>
  </div>
  <div class="card">
    <strong>🔒 Stable XML</strong>
    <p>Stable XML serialization means clean diffs, safer CI, and easier rollbacks.</p>
  </div>
</div>

<a href="#/guide/quickstart" class="button primary">Start in 5 minutes</a>
<a href="#/manifest/overview" class="button secondary">Jump to manifest docs</a>

---

## The problems it solves

- **Publish-loop fatigue** — The default PCF loop often requires publishing just to see a change. The proxy workflow keeps the runtime pointed at your local build output.
- **XML friction** — ControlManifest.Input.xml is verbose and error-prone. YAML/JSON is cleaner and easier to review.
- **Unstable diffs** — Deterministic serialization means your diffs stay stable, so reviews and audits are faster.
- **Missing validation** — Schema-based validation and strong typing give immediate, actionable feedback.

---

## Value proposition

**PCF Toolkit replaces repetitive manual work with a consistent, automatable pipeline.**

- **Develop faster** — keep Power Apps running and serve fresh builds locally.
- **Ship safely** — validate manifests against the same schema every time.
- **Collaborate better** — keep manifests human-readable and diff-friendly.

---

## Use cases

| Scenario | How PCF Toolkit helps |
| --- | --- |
| **Local dev** | Iterate on PCF controls without republishing every change |
| **CI/CD** | Validate manifests and generate XML as part of a build |
| **Legacy upgrades** | Import existing XML and keep authoring in YAML/JSON |

---

## Quick start

```bash
uv tool install pcf-toolkit@latest
pcf-toolkit proxy init
pcf-toolkit proxy start MyComponent
```

Need more detail? See the full [Quick Start](guide/quickstart.md).

---

## How it compares

| Workflow | With PCF Toolkit | Without PCF Toolkit |
| --- | --- | --- |
| Edit manifest | YAML/JSON with schema validation | Manual XML edits |
| Diffs | Deterministic, stable | Non-deterministic noise |
| Local testing | Proxy local webresources | Publish loop |
| CI automation | CLI commands | Custom scripts |

---

## Built by Vectorfy Co

PCF Toolkit is developed and maintained by [Vectorfy Co](https://vectorfy.co), an End-to-End AI & Technology Services company delivering enterprise-grade AI systems. We specialize in creating custom AI solutions using PCF controls in Power Apps and Dynamics 365, helping organizations build intelligent, scalable applications that transform business processes.

Whether you're developing AI-powered dashboards, intelligent data visualizations, or custom business logic components, PCF Toolkit provides the foundation for professional-grade Power Apps development.

---

## No telemetry

PCF Toolkit does not emit analytics or telemetry by default. Your data stays on your machine.

---

## What's inside

- **Manifest tooling** — validate, generate, import, export schema.
- **Proxy workflow** — mitmproxy + local HTTP server + PAC CLI integration.
- **Developer utilities** — examples and doctor checks.

---

## Next steps

- [Install the toolkit](guide/installation.md)
- [Author your first manifest](manifest/overview.md)
- [Run the local proxy](proxy/overview.md)

---

> **Tip:** Looking for keyboard navigation? Press `T` to toggle theme, `Cmd/Ctrl + K` to search, or see [Keyboard Shortcuts](meta/keyboard-shortcuts.md) for more.
