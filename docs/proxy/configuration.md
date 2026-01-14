---
title: Proxy Configuration
description: Full reference for pcf-proxy.yaml and all proxy configuration options.
---

# Proxy Configuration

The proxy workflow is configured via `pcf-proxy.yaml` (or JSON). This reference documents **every option** in `schemas/pcf-proxy.schema.json`.

## Top-level keys

| Key | Type | Description |
| --- | --- | --- |
| `project_root` | string | Project root path for global configs. |
| `crm_url` | string | Power Apps environment URL. |
| `expected_path` | string | Request path template for PCF webresources. |
| `proxy` | object | mitmproxy listen settings. |
| `http_server` | object | Local HTTP server settings. |
| `bundle` | object | Build output location. |
| `browser` | object | Browser preference and path. |
| `mitmproxy` | object | mitmproxy path override. |
| `environments` | array | Named environments from PAC CLI. |
| `open_browser` | boolean | Auto-launch browser with proxy settings. |
| `auto_install` | boolean | Auto-install mitmproxy if missing. |

## proxy

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `host` | string | `127.0.0.1` | mitmproxy listen host. |
| `port` | integer | `8080` | mitmproxy listen port. |

## http_server

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `host` | string | `127.0.0.1` | Local file server host. |
| `port` | integer | `8082` | Local file server port. |

## bundle

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `dist_path` | string | `out/controls/{PCF_NAME}` | Relative build output path. |

## browser

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `prefer` | `chrome` \| `edge` \| `auto` | `chrome` | Browser preference. |
| `path` | string | null | Explicit browser executable path. |

## mitmproxy

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `path` | string | null | Explicit mitmproxy/mitmdump path. |

## environments

| Key | Type | Description |
| --- | --- | --- |
| `name` | string | Friendly environment name. |
| `url` | string | Environment URL. |
| `active` | boolean | Marks preferred environment. |

## Example

```yaml
crm_url: "https://yourorg.crm.dynamics.com/"
expected_path: "/webresources/{PCF_NAME}/"
proxy:
  host: "127.0.0.1"
  port: 8080
http_server:
  host: "127.0.0.1"
  port: 8082
bundle:
  dist_path: "out/controls/{PCF_NAME}"
browser:
  prefer: "chrome"
  path: null
mitmproxy:
  path: null
open_browser: true
auto_install: true
```

Next: [Proxy Workflow](proxy/workflow.md)
