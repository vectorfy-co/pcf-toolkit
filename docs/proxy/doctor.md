---
title: Proxy Doctor
description: Diagnose proxy setup issues and apply safe fixes.
---

# Proxy Doctor

`pcf-toolkit proxy doctor` validates the prerequisites required to run the proxy.

## What it checks

- Config file readability
- Port availability
- mitmproxy presence
- mitmproxy certificate status
- Browser availability
- Dist path existence

## Run it

```bash
pcf-toolkit proxy doctor
```

## Validate a component

```bash
pcf-toolkit proxy doctor --component MyComponent
```

## Apply safe fixes

```bash
pcf-toolkit proxy doctor --fix
```

This currently attempts safe automation such as installing mitmproxy.

## Common failures

| Failure | Fix |
| --- | --- |
| Port in use | Change `proxy.port` or `http_server.port`. |
| Dist path missing | Run your build or update `bundle.dist_path`. |
| mitmproxy missing | Set `auto_install: true` or install manually. |
| Browser not found | Set `browser.path` or disable `open_browser`. |

Next: [Proxy Troubleshooting](proxy/troubleshooting.md)
