---
title: FAQ
description: Frequently asked questions about PCF Toolkit usage.
---

# FAQ

## Do I need to publish my control to use the proxy?

No. The proxy replaces webresource requests with your local build output, so you can iterate without publishing each change.

## Can I keep using XML directly?

You can, but the recommended approach is to author YAML/JSON and generate XML deterministically.

## Does PCF Toolkit store credentials?

No. Authentication is handled by your browser/PAC CLI. The toolkit does not store tokens.

## Is mitmproxy required?

Only for the proxy workflow. Manifest authoring and XML generation work without it.

## Can I use this in CI?

Yes. The CLI is designed to run in CI, and the repo includes scripts to validate schemas.

## What Python versions are supported?

Python 3.13+.

Next: [Contributing](project/contributing.md)
