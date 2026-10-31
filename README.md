# Build a Python Wheel with Template Substitution

A GitHub Action that builds a Python wheel, applying template substitution to replace `@VAR@` placeholders with values from the environment.

## Features

- ✅ Get values from the GitHub Actions environment
- ✅ Replace `@VAR@` placeholders in specified files with environment values
- ✅ Build the wheel file
- ✅ Support for different build modes (beta, release, post)
- ✅ Debug mode for troubleshooting

## Usage

### Basic Usage

Create a workflow file (e.g., `.github/workflows/build.yml`) in your repository:

```yaml
name: Build Python Wheel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: '3.x'

      - name: Build wheel
        uses: cav71/action-build-wheel@v1
        id: build
        with:
          mode: release

      - name: Display generated wheel
        run: echo "Built wheel: ${{ steps.build.outputs.python_wheel }}"
```

### Using in Another Repository

To use this action from another repository:

```yaml
- name: Build Python wheel
  uses: cav71/action-build-wheel@v1
  id: build
  with:
    mode: release
    files: "setup.py pyproject.toml"
```

### Build Modes

The action supports three build modes:

- **beta**: Build a beta version of the wheel
- **release**: Build a release version (default)
- **post**: Build a post-release version

```yaml
- name: Build beta wheel
  uses: cav71/action-build-wheel@v1
  with:
    mode: beta
```

### Custom Python Command

You can specify a custom Python command:

```yaml
- name: Build wheel with custom Python
  uses: cav71/action-build-wheel@v1
  with:
    python: python3.11
    mode: release
```

### File Template Substitution

Specify which files should have `@VAR@` placeholders replaced:

```yaml
- name: Build wheel with template substitution
  uses: cav71/action-build-wheel@v1
  with:
    mode: release
    files: "setup.py src/__version__.py"
```

### Debug Mode

Enable debug mode to dump environment information:

```yaml
- name: Build wheel with debug
  uses: cav71/action-build-wheel@v1
  with:
    mode: release
    debug: true
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python` | Configure the python command | No | `python` |
| `mode` | What kind of package to build (beta, release, post) | Yes | `release` |
| `files` | Files to apply `@VAR@` replacement | No | `` |
| `debug` | Dumps debug data | No | `false` |

## Outputs

| Output | Description |
|--------|-------------|
| `python_wheel` | The path to the generated wheel file |

## Example Workflow with Output

```yaml
name: Build and Upload Wheel

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: '3.x'

      - name: Build wheel
        uses: cav71/action-build-wheel@v1
        id: build
        with:
          mode: release
          files: "setup.py"

      - name: Upload wheel
        uses: actions/upload-artifact@v4
        with:
          name: python-wheel
          path: ${{ steps.build.outputs.python_wheel }}
```

## Environment Variables

The action automatically injects GitHub context information as environment variables, which can be used for template substitution:

- `GITHUB_DUMP`: JSON containing repository information, ref, sha, run number, etc.

## Project Structure

```
action-build-wheel/
├── action.yml          # Action configuration
├── src/
│   └── support/
│       ├── __init__.py
│       ├── builder.py  # Main build logic
│       ├── info.py     # Debug information
│       └── ureporting.py
├── README.md           # This file
└── .github/
    └── workflows/
        └── test.yml    # Optional: test workflow
```

## Requirements

- GitHub Actions runner (Linux, macOS, or Windows)
- Python 3.x (automatically set up by the action)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
