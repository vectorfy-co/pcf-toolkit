---
title: First Local Proxy
description: Configure and run your first local proxy session for a PCF component.
---

# First Local Proxy

This walkthrough sets up a proxy session that serves your local PCF build output without republishing.

## 1) Generate a config

```bash
pcf-toolkit proxy init
```

This creates `pcf-proxy.yaml` in your project. Open it and confirm:

- `crm_url` points to your Power Apps environment
- `bundle.dist_path` matches your build output

## 2) Build your component

Run your normal PCF build so that `out/controls/<Component>` exists.

## 3) Start the proxy

```bash
pcf-toolkit proxy start MyNamespace.MyComponent
```

If you don’t know the name, use auto-detect:

```bash
pcf-toolkit proxy start auto
```

## 4) Stop the proxy

```bash
pcf-toolkit proxy stop
```

## Behind the scenes

- `mitmproxy` listens on `proxy.port` (default 8080)
- A local HTTP server hosts your build output on `http_server.port` (default 8082)
- The proxy rewrites `/webresources/<Component>/...` to your local server

## Common issues

- **Dist path missing**: build output doesn’t exist → update `bundle.dist_path`
- **Port in use**: change `proxy.port` or `http_server.port`
- **Browser doesn’t open**: ensure `crm_url` is set and `browser.prefer` is valid

Next: [Proxy configuration reference](proxy/configuration.md)
