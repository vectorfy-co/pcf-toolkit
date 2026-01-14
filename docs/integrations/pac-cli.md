---
title: PAC CLI Integration
description: Use Microsoft PAC CLI to discover and select Power Apps environments.
---

# PAC CLI Integration

PAC CLI is optional but recommended. When installed and authenticated, PCF Toolkit can read your available environments and auto-populate `environments` in `pcf-proxy.yaml`.

## Why it helps

- Avoid manual CRM URL typing
- Switch between environments by name
- Keep an "active" environment pinned

## Workflow

1. Install and authenticate PAC CLI.
2. Run `pcf-toolkit proxy init` or `pcf-toolkit proxy start`.
3. Select an environment when prompted, or pass `--env`.

## Manual fallback

If you don't use PAC CLI, pass the CRM URL directly:

```bash
pcf-toolkit proxy start MyComponent --crm-url https://yourorg.crm.dynamics.com/
```

Next: [CI/CD Integration](integrations/ci-cd.md)
