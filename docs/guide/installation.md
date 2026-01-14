---
title: Installation
description: Install PCF Toolkit with uv (recommended) or run it directly in CI.
---

# Installation

PCF Toolkit is a Python 3.13+ CLI. The recommended install path uses `uv`, which provides fast, isolated tools without managing virtual environments.

## Prerequisites

- **Python 3.13+**
- **uv** (recommended)
- **mitmproxy** (required for proxy mode; can be auto-installed)
- **PAC CLI** (optional, for Power Apps environment discovery)

## Recommended: install as a tool

```bash
uv tool install pcf-toolkit@latest
```

Verify:

```bash
pcf-toolkit --version
```

## Run without installing

Useful for CI or one-off usage:

```bash
uvx pcf-toolkit --help
```

## Optional: add mitmproxy

If you use the proxy workflow and do not already have mitmproxy installed, you can allow the toolkit to install it automatically with `auto_install: true` in `pcf-proxy.yaml`.

```yaml
auto_install: true
```

## Optional: PAC CLI

PAC CLI enables automatic environment discovery when starting the proxy. If you already use PAC CLI for Power Platform, nothing else is needed. If not, keep it optional and pass `--crm-url` manually.

## Troubleshooting install

- Python version mismatch: confirm `python3 --version` is 3.13+
- PATH issues: ensure `~/.local/bin` (or uv tool path) is in your shell PATH

Next: [First Local Proxy](guide/first-proxy.md)
