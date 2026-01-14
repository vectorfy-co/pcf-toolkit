---
title: Proxy Workflow
description: Step-by-step guide for using the proxy workflow locally and in CI.
---

# Proxy Workflow

This guide covers the full proxy lifecycle: configuration, start, detach, and cleanup.

## Initialize config

```bash
pcf-toolkit proxy init
```

This creates `pcf-proxy.yaml` and optionally adds a `dev:proxy` script to `package.json`.

## Start the proxy

```bash
pcf-toolkit proxy start MyNamespace.MyComponent
```

If the component name is unknown:

```bash
pcf-toolkit proxy start auto
```

## Choose an environment

If you have multiple environments defined (via PAC CLI), select one:

```bash
pcf-toolkit proxy start MyComponent --env "Contoso Dev"
```

You can also pass the CRM URL directly:

```bash
pcf-toolkit proxy start MyComponent --crm-url https://yourorg.crm.dynamics.com/
```

## Run in the background

```bash
pcf-toolkit proxy start MyComponent --detach
```

When detached, logs are written to `.pcf-toolkit/proxy.log`, and session metadata is stored in `.pcf-toolkit/proxy.session.json`.

## Stop the proxy

```bash
pcf-toolkit proxy stop
```

## Helpful overrides

- `--dist-path`: override the build output path
- `--proxy-port` / `--http-port`: change ports
- `--browser` / `--browser-path`: control browser launching
- `--mitmproxy-path`: use a custom mitmproxy binary

Next: [Doctor checks](proxy/doctor.md)
