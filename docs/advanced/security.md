---
title: Security Considerations
description: Security guidance for local proxying, credentials, and environment isolation.
---

# Security Considerations

## Proxy trust model

The proxy intercepts traffic between your browser and Power Apps. Treat it as a trusted local tool and only run it on machines you control.

## Certificates

mitmproxy generates a local CA certificate used to intercept HTTPS requests. Install it only on your dev machine and remove it if it's no longer needed.

## Credentials

PCF Toolkit does **not** store credentials or tokens. Authentication is handled by your existing browser session and/or PAC CLI.

## Environment isolation

- Use separate environments for dev/test.
- Avoid pointing `crm_url` at production while proxying.

## Auditability

- Keep YAML/JSON manifests in source control.
- Regenerate XML in CI to ensure reproducibility.

Next: [Troubleshooting](advanced/troubleshooting.md)
