---
title: CLI Overview
description: Understand the PCF Toolkit CLI structure and the main command groups.
---

# CLI Overview

The CLI is the primary interface to PCF Toolkit. It is organized into:

- **Core commands**: validate, generate, import-xml
- **Schema tools**: export-schema, export-json-schema
- **Developer tools**: examples, doctor
- **Proxy commands**: proxy init/start/stop/doctor

## Quick command map

```text
pcf-toolkit validate            Validate manifest YAML/JSON
pcf-toolkit generate            Generate ControlManifest.Input.xml
pcf-toolkit import-xml          Convert XML back to YAML/JSON
pcf-toolkit export-schema       Export schema snapshot
pcf-toolkit export-json-schema  Export JSON Schema
pcf-toolkit examples            Show curated examples
pcf-toolkit doctor              Check local setup
pcf-toolkit proxy ...           Local proxy workflow
```

## Global options

- `--version`: print the installed version and exit
- `--help`: show help for any command

Next: [Command Reference](cli/commands.md)
