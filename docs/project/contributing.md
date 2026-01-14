---
title: Contributing
description: Contribute to PCF Toolkit with local setup, tests, and release guidance.
---

# Contributing

Thanks for contributing! This project is developer-first and welcomes improvements.

## Development setup

```bash
uv sync --extra dev
```

## Run tests

```bash
uv run --python 3.13 pytest
```

## Regenerate schemas

```bash
uv run --python 3.13 --script scripts/build_schema_snapshot.py
uv run --python 3.13 --script scripts/build_json_schema.py
```

## Playwright (optional)

If you run `scripts/extract_spec.py`, install browser binaries:

```bash
uv run --python 3.13 python -m playwright install
```

## Coding guidelines

- Keep output deterministic.
- Prefer readable errors over cryptic exceptions.
- Add tests for new behavior.

## Pull request checklist

- [ ] Tests pass
- [ ] Schema artifacts updated if required
- [ ] Docs updated (if behavior changes)

Next: [Changelog](project/changelog.md)
