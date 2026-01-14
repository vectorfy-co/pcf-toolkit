---
title: Proxy Overview
description: Local proxy workflow that serves PCF webresources without publishing.
---

# Proxy Overview

The proxy workflow keeps Power Apps pointed at your **local build output** while the environment runs normally. Think of it as a transparent redirect layer that swaps webresource requests for local files.

## Why use the proxy?

- **Skip the publish loop** while iterating on the control UI.
- **Keep your environment stable** by only publishing when ready.
- **Control the dev experience** by pinning the request path and local build location.

## Core commands

```bash
pcf-toolkit proxy init
pcf-toolkit proxy start MyComponent
pcf-toolkit proxy stop
pcf-toolkit proxy doctor
```

## How it works

1. mitmproxy listens for Power Apps webresource requests.
2. The addon checks the request path and rewrites to your local HTTP server.
3. The HTTP server serves the files from `bundle.dist_path`.

Next: [Proxy Configuration](proxy/configuration.md)
