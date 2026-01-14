---
title: Advanced Troubleshooting
description: Deep troubleshooting for manifest validation, XML import, and schema tooling.
---

# Advanced Troubleshooting

## Manifest validation errors

**Symptom**: `Manifest is invalid` with a list of fields.

**Fix**:

1. Follow the error location path to the field.
2. Ensure the field exists in the schema.
3. Re-run `pcf-toolkit validate`.

**Tip**: enable editor schema validation to catch issues before running the CLI.

## Import XML fails

**Symptom**: `Import failed` or unexpected parsing errors.

**Fix**:

- Ensure the file is a valid `ControlManifest.Input.xml`.
- Use `--format json` to inspect the parsed output.
- Run with `--no-validate` if you need to inspect raw output.

## Schema exports differ in CI

**Symptom**: `git diff --exit-code` fails after `build_schema_snapshot`.

**Fix**:

- Run `uv run --python 3.13 --script scripts/build_schema_snapshot.py` locally.
- Commit updated `data/schema_snapshot.json` and `schemas/pcf-manifest.schema.json`.

## Proxy validation warnings

**Symptom**: `proxy doctor` reports warnings.

**Fix**: Most warnings can be resolved by updating config values (`crm_url`, `bundle.dist_path`) or installing mitmproxy.

## Still stuck?

- Re-run `pcf-toolkit doctor` and `pcf-toolkit proxy doctor`.
- Inspect `.pcf-toolkit/proxy.log` for detailed errors.

Next: [FAQ](advanced/faq.md)
