# PCF Manifest Toolkit

Author Power Apps Component Framework (PCF) manifests as typed YAML/JSON (or Python), then generate deterministic `ControlManifest.Input.xml`.

<div align="right">
  <table>
    <tr>
      <td><strong>Lifecycle</strong></td>
      <td>
        <a href="https://github.com/andrewmaspero/pcf-manifest-toolkit/actions/workflows/ci.yml">
          <img src="https://img.shields.io/github/actions/workflow/status/andrewmaspero/pcf-manifest-toolkit/ci.yml?branch=main&style=flat&logo=githubactions&logoColor=white" alt="CI status" />
        </a>
        <a href="https://pypi.org/project/pcf-manifest/">
          <img src="https://img.shields.io/pypi/v/pcf-manifest?style=flat&logo=pypi&logoColor=white" alt="PyPI version" />
        </a>
        <a href="https://pypi.org/project/pcf-manifest/">
          <img src="https://img.shields.io/pypi/pyversions/pcf-manifest?style=flat&logo=python&logoColor=white" alt="Supported Python versions" />
        </a>
        <img src="https://img.shields.io/badge/Status-Beta-f59e0b?style=flat&logo=github&logoColor=white" alt="Status: beta" />
        <img src="https://img.shields.io/badge/License-None-ef4444?style=flat&logo=creativecommons&logoColor=white" alt="License: none" />
      </td>
    </tr>
    <tr>
      <td><strong>Core Stack</strong></td>
      <td>
        <img src="https://img.shields.io/badge/Python-%3E%3D3.13-3776AB?style=flat&logo=python&logoColor=white" alt="Python >=3.13" />
        <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat&logo=pydantic&logoColor=white" alt="Pydantic v2" />
        <img src="https://img.shields.io/badge/Typer-CLI-111827?style=flat&logo=typer&logoColor=white" alt="Typer CLI" />
        <img src="https://img.shields.io/badge/Rich-Console-0f172a?style=flat&logo=rich&logoColor=white" alt="Rich console output" />
        <img src="https://img.shields.io/badge/YAML%2FJSON-Authoring-0ea5e9?style=flat&logo=yaml&logoColor=white" alt="YAML and JSON authoring" />
        <img src="https://img.shields.io/badge/XML-Deterministic-64748b?style=flat&logo=xml&logoColor=white" alt="Deterministic XML" />
      </td>
    </tr>
    <tr>
      <td><strong>Navigation</strong></td>
      <td>
        <a href="#quick-start"><img src="https://img.shields.io/badge/Local%20Setup-Quick%20Start-059669?style=flat&logo=python&logoColor=white" alt="Quick start" /></a>
        <a href="#features"><img src="https://img.shields.io/badge/Overview-Features-7c3aed?style=flat&logo=simpleicons&logoColor=white" alt="Features" /></a>
        <a href="#cli"><img src="https://img.shields.io/badge/Usage-CLI-2563eb?style=flat&logo=typer&logoColor=white" alt="CLI usage" /></a>
        <a href="#schemas"><img src="https://img.shields.io/badge/Validation-JSON%20Schema-0ea5e9?style=flat&logo=json&logoColor=white" alt="JSON Schema" /></a>
        <a href="#python-api"><img src="https://img.shields.io/badge/Usage-Python%20API-111827?style=flat&logo=python&logoColor=white" alt="Python API" /></a>
        <a href="#development"><img src="https://img.shields.io/badge/Contribute-Development-6366f1?style=flat&logo=git&logoColor=white" alt="Development" /></a>
        <a href="#architecture"><img src="https://img.shields.io/badge/Details-Architecture-1f2937?style=flat&logo=github&logoColor=white" alt="Architecture" /></a>
        <a href="#troubleshooting"><img src="https://img.shields.io/badge/Help-Troubleshooting-f97316?style=flat&logo=github&logoColor=white" alt="Troubleshooting" /></a>
      </td>
    </tr>
  </table>
</div>

What you get:

- Strict validation (typos and unknown keys are rejected).
- Deterministic XML output (stable ordering for clean diffs).
- JSON Schema for editor + CI validation.
- Optional "docs snapshot" pipeline backed by Microsoft Learn examples.

<a id="quick-start"></a>
## ![Quick Start](https://img.shields.io/badge/Quick%20Start-4%20steps-059669?style=for-the-badge&logo=python&logoColor=white)

Prerequisites:

- Python >= 3.13
- `pip` or `uv` (recommended)

### Install from PyPI

```bash
pip install pcf-manifest
pcf-manifest --help
```

### Run without installing (uvx)

```bash
uvx pcf-manifest --help
uvx pcf-manifest validate manifest.yaml
```

Run directly from a local checkout (no install into your environment):

```bash
uvx --from . pcf-manifest --help
uvx --from . pcf-manifest validate manifest.yaml
```

### Minimal useful example

Create `manifest.yaml`:

```yaml
# yaml-language-server: $schema=./schemas/pcf-manifest.schema.json
control:
  namespace: MyNameSpace
  constructor: JSHelloWorldControl
  version: 1.0.0
  display-name-key: JS_HelloWorldControl_Display_Key
  description-key: JS_HelloWorldControl_Desc_Key
  control-type: standard
  property:
    - name: myFirstProperty
      display-name-key: myFirstProperty_Display_Key
      description-key: myFirstProperty_Desc_Key
      of-type: SingleLine.Text
      usage: bound
      required: true
  resources:
    code:
      path: JS_HelloWorldControl.js
      order: 1
    css:
      - path: css/JS_HelloWorldControl.css
        order: 1
```

Validate it:

```bash
pcf-manifest validate manifest.yaml
```

Generate `ControlManifest.Input.xml`:

```bash
pcf-manifest generate manifest.yaml -o ControlManifest.Input.xml
```

<a id="features"></a>
## ![Features](https://img.shields.io/badge/Features-Highlights-7c3aed?style=for-the-badge&logo=simpleicons&logoColor=white)

| Feature | Why it matters |
| --- | --- |
| ![Typed](https://img.shields.io/badge/Typed-Pydantic%20models-E92063?style=flat&logo=pydantic&logoColor=white) | Catch invalid manifests early with strict validation. |
| ![Deterministic](https://img.shields.io/badge/XML-Deterministic-64748b?style=flat&logo=xml&logoColor=white) | Stable output ordering means clean PR diffs. |
| ![Schema](https://img.shields.io/badge/JSON%20Schema-Exportable-0ea5e9?style=flat&logo=json&logoColor=white) | Editor hints + CI checks for YAML/JSON manifests. |
| ![Import](https://img.shields.io/badge/Import-XML%20%E2%86%92%20YAML%2FJSON-2563eb?style=flat&logo=yaml&logoColor=white) | Migrate existing `ControlManifest.Input.xml` into a maintainable form. |
| ![Docs](https://img.shields.io/badge/Docs-backed-Examples-f97316?style=flat&logo=github&logoColor=white) | Tests verify against examples extracted from Microsoft Learn. |
| ![CLI](https://img.shields.io/badge/CLI-Polished%20help-111827?style=flat&logo=typer&logoColor=white) | Rich help output, completion, and a `doctor` command. |

<a id="cli"></a>
## ![CLI](https://img.shields.io/badge/CLI-Commands-2563eb?style=for-the-badge&logo=typer&logoColor=white)

Validate a manifest (YAML/JSON):

```bash
pcf-manifest validate path/to/manifest.yaml
```

Validate from stdin (useful in CI):

```bash
cat path/to/manifest.yaml | pcf-manifest validate -
```

Generate XML:

```bash
pcf-manifest generate manifest.yaml -o ControlManifest.Input.xml
```

Omit the XML declaration header:

```bash
pcf-manifest generate manifest.yaml --no-declaration
```

Import XML to YAML (default) or JSON:

```bash
pcf-manifest import-xml ControlManifest.Input.xml -o manifest.yaml
pcf-manifest import-xml ControlManifest.Input.xml --format json -o manifest.json
```

Export JSON Schema (for editor + CI validation):

```bash
pcf-manifest export-json-schema -o schemas/pcf-manifest.schema.json
```

Export the docs-derived schema snapshot:

```bash
pcf-manifest export-schema -o data/schema_snapshot.json
```

See curated examples:

```bash
pcf-manifest examples
```

Environment checks (schema files, Python version, etc.):

```bash
pcf-manifest doctor
pcf-manifest doctor --strict
```

Shell completion (Typer):

```bash
pcf-manifest --install-completion
pcf-manifest --show-completion
```

<a id="schemas"></a>
## ![Schemas](https://img.shields.io/badge/Validation-JSON%20Schema-0ea5e9?style=for-the-badge&logo=json&logoColor=white)

This repo includes `schemas/pcf-manifest.schema.json`. If you are authoring YAML in this repo, add this to the top of your file:

```yaml
# yaml-language-server: $schema=./schemas/pcf-manifest.schema.json
```

If you installed the package elsewhere, export the schema into your project and point your editor at that copy:

```bash
pcf-manifest export-json-schema -o pcf-manifest.schema.json
```

<a id="python-api"></a>
## ![Python API](https://img.shields.io/badge/Python-API-111827?style=for-the-badge&logo=python&logoColor=white)

The package exports:

- `pcf_manifest_toolkit.Manifest` (alias of `pcf_manifest_toolkit.models.Manifest`)
- `pcf_manifest_toolkit.ManifestXmlSerializer` (from `pcf_manifest_toolkit.xml`)

Minimal example:

```python
from pcf_manifest_toolkit import Manifest, ManifestXmlSerializer

manifest = Manifest.model_validate(
    {
        "control": {
            "namespace": "MyNameSpace",
            "constructor": "MyControl",
            "version": "1.0.0",
            "display-name-key": "MyControl_Display_Key",
            "resources": {"code": {"path": "index.ts", "order": 1}},
        }
    }
)

xml_text = ManifestXmlSerializer().to_string(manifest)
print(xml_text)
```

<a id="architecture"></a>
## ![Architecture](https://img.shields.io/badge/Architecture-How%20it%20works-1f2937?style=for-the-badge&logo=github&logoColor=white)

Data flow:

```
YAML/JSON (or dict) -> load_manifest() -> Pydantic models -> ManifestXmlSerializer -> ControlManifest.Input.xml
                              |
                              +-> manifest_schema_text() -> JSON Schema (editor/CI)
```

Core modules:

- `src/pcf_manifest_toolkit/models.py`: Pydantic models for the manifest schema (strict validation + dashed aliases like `display-name-key`).
- `src/pcf_manifest_toolkit/xml.py`: deterministic XML serializer built on `xml.etree.ElementTree`.
- `src/pcf_manifest_toolkit/io.py`: YAML/JSON loading helpers (including stdin).
- `src/pcf_manifest_toolkit/json_schema.py`: JSON Schema generation from the Pydantic model.
- `src/pcf_manifest_toolkit/cli.py`: Typer-based CLI (`pcf-manifest`).
- `src/pcf_manifest_toolkit/schema_snapshot.py`: loads/exports the docs-derived snapshot data.

Docs snapshot pipeline (optional):

1. `scripts/extract_spec.py` uses Playwright to scrape Microsoft Learn into `data/spec_raw.json`.
2. `scripts/build_schema_snapshot.py` normalizes into `data/schema_snapshot.json` (and copies into `src/pcf_manifest_toolkit/data/` for packaging).
3. Tests use extracted docs examples to verify serialization.

<a id="development"></a>
## ![Development](https://img.shields.io/badge/Development-Contributing-6366f1?style=for-the-badge&logo=git&logoColor=white)

### Prerequisites

- Python >= 3.13 (package requirement)
- `uv` (recommended)

### Set up a dev environment

```bash
uv python install 3.13
uv sync --extra dev
```

### Run tests

```bash
uv run pytest -q
```

### Regenerate schemas and snapshots

```bash
uv run python scripts/build_schema_snapshot.py
uv run python scripts/build_json_schema.py
```

### Refresh the raw docs extraction (requires Playwright)

```bash
uv run python scripts/extract_spec.py
uv run playwright install
```

<a id="ci-cd"></a>
## ![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-1F4B99?style=for-the-badge&logo=githubactions&logoColor=white)

This repo uses GitHub Actions (`.github/workflows/ci.yml`) for:

- Tests on PRs and pushes to `main`
- Package build + publish to PyPI on tags matching `v*` (OIDC / trusted publishing)
- Schema snapshot + JSON Schema regeneration (CI fails if generated outputs are not committed)

<a id="configuration"></a>
## ![Configuration](https://img.shields.io/badge/Configuration-Runtime-0ea5e9?style=for-the-badge&logo=simpleicons&logoColor=white)

There are no required environment variables. Runtime behavior is configured via:

- CLI flags (for example `--no-declaration`, `--format`, `--strict`)
- Your input manifest file (YAML/JSON)

<a id="examples"></a>
## ![Examples](https://img.shields.io/badge/Examples-YAML-22c55e?style=for-the-badge&logo=yaml&logoColor=white)

Dataset with `property-set`:

```yaml
control:
  namespace: MyNamespace
  constructor: MyControl
  version: 1.0.0
  display-name-key: MyControl_Display_Key
  resources:
    code:
      path: index.ts
      order: 1
  data-set:
    - name: dataSetGrid
      display-name-key: DataSetGridProperty
      cds-data-set-options: displayCommandBar:true;displayViewSelector:true;displayQuickFind:true
      property-set:
        - name: MyColumn
          display-name-key: MyColumn_Display_Key
          description-key: MyColumn_Desc_Key
          of-type: SingleLine.Text
          usage: bound
```

Feature usage:

```yaml
control:
  namespace: MyNamespace
  constructor: MyControl
  version: 1.0.0
  display-name-key: MyControl_Display_Key
  resources:
    code:
      path: index.ts
      order: 1
  feature-usage:
    uses-feature:
      - name: Device.captureImage
        required: true
      - name: WebAPI
        required: false
```

External service usage:

```yaml
control:
  namespace: MyNamespace
  constructor: MyControl
  version: 1.0.0
  display-name-key: MyControl_Display_Key
  resources:
    code:
      path: index.ts
      order: 1
  external-service-usage:
    enabled: true
    domain:
      - value: www.Microsoft.com
```

Enum property:

```yaml
control:
  namespace: MyNamespace
  constructor: MyControl
  version: 1.0.0
  display-name-key: MyControl_Display_Key
  resources:
    code:
      path: index.ts
      order: 1
  property:
    - name: YesNo
      display-name-key: YesNo_Display_Key
      description-key: YesNo_Desc_Key
      of-type: Enum
      usage: input
      required: false
      value:
        - name: Yes
          display-name-key: Yes
          value: 0
        - name: No
          display-name-key: No
          value: 1
```

<a id="troubleshooting"></a>
## ![Troubleshooting](https://img.shields.io/badge/Troubleshooting-Common%20issues-f97316?style=for-the-badge&logo=github&logoColor=white)

### "Manifest is invalid" but my YAML looks fine

Common culprits:

- Unknown keys: models are strict (`extra="forbid"`), so typos like `display_name_key` vs `display-name-key` are rejected.
- Missing `resources.code`: `resources` is required, and `resources.code` is required.
- Enum without values: `of-type: Enum` requires at least one `value` entry.
- Feature usage empty: `feature-usage.uses-feature` must have at least one item.
- `external-service-usage` enabled but no domains: `enabled: true` requires at least one `domain`.

### "Value must contain only letters or numbers" for `namespace` / `constructor`

This toolkit enforces `str.isalnum()` for both `control.namespace` and `control.constructor`. If your real-world manifest uses underscores or dots, you will need to either:

- adjust your names to be alphanumeric, or
- relax the rule in `src/pcf_manifest_toolkit/models.py` (and update tests accordingly).

### Playwright extraction fails / Microsoft Learn blocks requests

`scripts/extract_spec.py` drives a real browser. If Microsoft Learn changes markup, requires auth, or rate-limits, extraction can fail or produce partial pages. In practice:

- rerun after `uv run playwright install`
- try running with a visible browser (modify the script to `launch(headless=False)` while debugging)
- keep `data/spec_raw.json` and `data/schema_snapshot.json` committed so consumers do not need to scrape docs

<a id="contributing"></a>
## ![Contributing](https://img.shields.io/badge/Contributing-PRs%20welcome-10b981?style=for-the-badge&logo=git&logoColor=white)

Contributions that help most:

- expanding model coverage in `src/pcf_manifest_toolkit/models.py`
- adding Microsoft Learn examples to `tests/test_examples.py`
- improving the extraction/normalization pipeline under `scripts/`

Suggested workflow:

1. Create a branch.
2. Run `uv run pytest`.
3. If you change models, regenerate outputs:
   - `uv run python scripts/build_schema_snapshot.py`
   - `uv run python scripts/build_json_schema.py`
4. Open a PR explaining the "why" (especially if you add/adjust validation rules).

Also: please add gaps/assumptions to `GAPS.md` when the docs are ambiguous.

<a id="license"></a>
## ![Credits%20%26%20License](https://img.shields.io/badge/Credits%20%26%20License-Dependencies%20%26%20legal-0f172a?style=for-the-badge&logo=creativecommons&logoColor=white)

Key dependencies:

- Pydantic: strict validation and JSON Schema generation
- Typer: CLI framework
- PyYAML: YAML parsing
- Playwright (dev dependency): docs extraction via a real browser

License:

There is currently no `LICENSE` file in this repository. If you intend this to be open source, add a license (MIT/Apache-2.0 are common) and update this section accordingly.
