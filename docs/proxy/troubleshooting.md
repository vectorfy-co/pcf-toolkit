---
title: Proxy Troubleshooting
description: Resolve common proxy workflow issues quickly.
---

# Proxy Troubleshooting

This checklist maps common failures to fixes.

## Ports already in use

**Symptom**: doctor reports `proxy_port` or `http_port` is in use.

**Fix**: update `proxy.port` or `http_server.port` in `pcf-proxy.yaml`, or stop the process using the port.

## Dist path missing

**Symptom**: dist path check fails for your component.

**Fix**: build the PCF control or update `bundle.dist_path` to match your output.

## mitmproxy not found

**Symptom**: doctor reports mitmproxy missing.

**Fix**: set `auto_install: true` and run `pcf-toolkit proxy doctor --fix`, or install mitmproxy manually.

## mitmproxy certificate missing

**Symptom**: doctor warns about `mitmproxy-ca-cert.pem`.

**Fix**: run mitmproxy once to generate the certificate, then trust it in your OS keychain.

## Browser did not open

**Symptom**: proxy starts but no browser opens.

**Fix**: set `crm_url` and verify `browser.prefer` or `browser.path`. You can also set `open_browser: false`.

## Incorrect webresource path

**Symptom**: request not rewritten, local files not served.

**Fix**: ensure your requests match `expected_path`, and use `{PCF_NAME}` placeholder correctly.

Need more? See [Advanced Troubleshooting](advanced/troubleshooting.md).
