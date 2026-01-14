---
title: Command Reference
description: Detailed reference for every PCF Toolkit CLI command and option.
---

# Command Reference

This section mirrors the CLI interface in the repository. All options and defaults come directly from the CLI code in `pcf_toolkit.cli` and `pcf_toolkit.proxy.cli`.

## Core commands

### `pcf-toolkit validate <MANIFEST>`

Validate a YAML/JSON manifest definition.

```bash
pcf-toolkit validate manifest.yaml
pcf-toolkit validate - < manifest.yaml
```

**Arguments**

| Name | Description |
| --- | --- |
| `MANIFEST` | Path to YAML/JSON or `-` for stdin. |

### `pcf-toolkit generate <MANIFEST>`

Generate deterministic `ControlManifest.Input.xml`.

```bash
pcf-toolkit generate manifest.yaml -o ControlManifest.Input.xml
```

**Options**

| Option | Description |
| --- | --- |
| `-o, --output FILE` | Write XML to file instead of stdout. |
| `--no-declaration` | Omit the XML declaration header. |

### `pcf-toolkit import-xml <XML>`

Convert existing XML into YAML or JSON.

```bash
pcf-toolkit import-xml ControlManifest.Input.xml -o manifest.yaml
pcf-toolkit import-xml ControlManifest.Input.xml --format json
```

**Options**

| Option | Description |
| --- | --- |
| `-o, --output FILE` | Write output to file. |
| `--format` | `yaml` or `json` (default `yaml`). |
| `--schema-directive/--no-schema-directive` | Include schema header in output (default true). |
| `--schema-path` | Schema URL/path for the directive. |
| `--validate/--no-validate` | Validate imported manifest (default true). |

### `pcf-toolkit export-schema`

Export the docs-derived schema snapshot.

```bash
pcf-toolkit export-schema -o data/schema_snapshot.json
```

**Options**

| Option | Description |
| --- | --- |
| `-o, --output FILE` | Write snapshot JSON to file. |

### `pcf-toolkit export-json-schema`

Export JSON Schema for YAML/JSON validation.

```bash
pcf-toolkit export-json-schema -o schemas/pcf-manifest.schema.json
```

**Options**

| Option | Description |
| --- | --- |
| `-o, --output FILE` | Write JSON Schema to file. |

### `pcf-toolkit examples`

Print curated examples for quick reference.

```bash
pcf-toolkit examples
```

### `pcf-toolkit doctor`

Check your environment for common issues.

```bash
pcf-toolkit doctor
pcf-toolkit doctor --strict
```

**Options**

| Option | Description |
| --- | --- |
| `--strict` | Exit non-zero on warnings. |

## Proxy commands

### `pcf-toolkit proxy init`

Create a proxy config file.

```bash
pcf-toolkit proxy init
pcf-toolkit proxy init --global --no-interactive
```

**Options**

| Option | Description |
| --- | --- |
| `-c, --config PATH` | Explicit config file path. |
| `--global` | Write to `~/.pcf-toolkit/pcf-proxy.yaml`. |
| `--local` | Force local config in current directory. |
| `--force` | Overwrite existing config. |
| `--add-npm-script/--no-add-npm-script` | Add `dev:proxy` script to `package.json` (default true). |
| `--npm-script NAME` | Script name to add (default `dev:proxy`). |
| `--interactive/--no-interactive` | Prompt for settings (default true). |
| `--crm-url URL` | Set CRM URL without prompting. |
| `--install-mitmproxy/--no-install-mitmproxy` | Auto-install mitmproxy during setup. |

### `pcf-toolkit proxy start <COMPONENT>`

Start a proxy session.

```bash
pcf-toolkit proxy start MyNamespace.MyComponent
pcf-toolkit proxy start auto
```

**Options**

| Option | Description |
| --- | --- |
| `-c, --config PATH` | Config file path. |
| `--global` | Use global config even if a local config exists. |
| `--root PATH` | Project root (component folder). |
| `--crm-url URL` | Override CRM URL. |
| `--env, --environment` | Environment name or index from config. |
| `--proxy-port PORT` | Override proxy port. |
| `--http-port PORT` | Override HTTP server port. |
| `--browser` | Browser preference: `chrome` or `edge`. |
| `--browser-path PATH` | Explicit browser binary. |
| `--mitmproxy-path PATH` | Explicit mitmproxy binary. |
| `--dist-path PATH` | Override dist path template. |
| `--open-browser/--no-open-browser` | Auto-launch browser. |
| `--auto-install/--no-auto-install` | Auto-install mitmproxy if missing. |
| `--detach` | Run in background. |

### `pcf-toolkit proxy stop`

Stop a running proxy session.

```bash
pcf-toolkit proxy stop
```

**Options**

| Option | Description |
| --- | --- |
| `--root PATH` | Project root used when starting the proxy. |

### `pcf-toolkit proxy doctor`

Validate proxy prerequisites.

```bash
pcf-toolkit proxy doctor
pcf-toolkit proxy doctor --component MyComponent --fix
```

**Options**

| Option | Description |
| --- | --- |
| `--component NAME` | Component name to validate dist path. |
| `-c, --config PATH` | Config file path. |
| `--root PATH` | Project root (component folder). |
| `--fix` | Attempt safe fixes (mitmproxy install). |

Next: [Manifest Authoring](manifest/overview.md)
