---
title: Performance Optimization
description: Tips for faster local iteration and predictable build times.
---

# Performance Optimization

## Reduce proxy latency

- Keep `proxy` and `http_server` on localhost.
- Avoid heavy browser extensions when using a proxy.
- Keep your build output small and focused.

## Speed up local builds

- Use incremental builds in your PCF toolchain.
- Avoid full rebuilds when only CSS changes.
- Keep assets small and cache-friendly.

## Fast CI builds

- Cache Python dependencies between runs.
- Only regenerate schemas when source data changes.
- Keep the schema check (`git diff --exit-code`) to catch drift.

## Diagnose bottlenecks

- Use `pcf-toolkit proxy doctor` to confirm prerequisites.
- Inspect `.pcf-toolkit/proxy.log` for slow responses.

Next: [Security](advanced/security.md)
