---
title: Best Practices
description: Practical patterns for reliable manifests, proxy workflows, and CI automation.
---

# Best Practices

## Keep manifests small and readable

- Prefer **YAML** for human reviews.
- Use descriptive `display-name-key` and `description-key` values.
- Group related properties and keep naming consistent.

## Treat XML as a build artifact

Think of XML like compiled output. You shouldn't hand-edit it; generate it from YAML/JSON so every build is reproducible.

## Validate early

- Run `pcf-toolkit validate` locally before committing.
- Add schema validation to your editor.
- Fail fast in CI using `pcf-toolkit validate`.

## Stabilize your diffs

- Stick with deterministic generation for XML.
- Avoid reordering keys unless the schema changes.

## Proxy workflow hygiene

- Set `bundle.dist_path` once and keep it consistent.
- Add `dev:proxy` to `package.json` for a single-command workflow.
- Use `proxy doctor` before demoing or recording.

## Use environments intentionally

- Use `environments` to avoid mis-targeting production.
- Mark one environment as `active` to avoid accidental switches.

Next: [Performance](advanced/performance.md)
