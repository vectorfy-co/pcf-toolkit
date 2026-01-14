---
title: Getting Started
description: Overview of the PCF Toolkit workflow, prerequisites, and first steps.
---

# Getting Started

PCF Toolkit is designed to make PCF development feel like modern software development: predictable, automated, and fast.

## Prerequisites

- Python 3.13+
- `uv` (recommended)
- A PCF component project with a build output folder

## First steps

1. [Install the CLI](guide/installation.md)
2. [Create a proxy config](guide/first-proxy.md)
3. [Validate a manifest](manifest/overview.md)

## Workflow at a glance

```text
YAML/JSON manifest -> validate -> generate XML -> build control -> proxy local webresources
```

## If you are new to PCF

Think of the manifest as a "contract" describing your control. PCF Toolkit gives you a safer, clearer way to write that contract.

Next: [Quick Start](guide/quickstart.md)
