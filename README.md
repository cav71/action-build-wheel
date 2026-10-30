# Build a python wheel, using template substitution

A simple GitHub Action that build a wheel, in a controlled way.

## Features

- ✅ get values from the environment
- ✅ replace from a list of files the @VAR@ with them
- ✅ build the wheel file


## Usage

### Basic Usage

Create a workflow file (e.g., `.github/workflows/hello.yml`) in your repository:

```yaml
name: Hello World

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v7

      - name: Create python wheel
        uses: cav71/action-build-wheel@v1

      - name: Display generated wheel
        run: echo "Built wheel ${{ steps.hello.outputs.python_wheel }}"
```

### Using in Another Repository

To use this action from another repository:

```yaml
- name: Run Hello World Action
  uses: your-username/your-repo@v1
  id: hello
  with:
    who-to-greet: 'Your Name'
```

### Custom Greeting

You can customize who to greet:

```yaml
- name: Greet specific person
  uses: ./
  with:
    who-to-greet: 'Alice'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `who-to-greet` | The name of the person to greet | Yes | `World` |

## Outputs

| Output | Description |
|--------|-------------|
| `time` | The timestamp when the greeting occurred |

## Example Workflow with Output

```yaml
name: Greet and Log

on: [push]

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Greet
        uses: ./
        id: greeting
        with:
          who-to-greet: 'Developer'

      - name: Show greeting info
        run: |
          echo "Greeted: ${{ inputs.who-to-greet }}"
          echo "Time: ${{ steps.greeting.outputs.time }}"
```

## Local Testing

To test the Python script locally:

```bash
# Run with default name (World)
python src/hello.py

# Run with custom name
python src/hello.py --name "Your Name"
```

## Project Structure

```
action-build-wheel/
├── action.yml          # Action configuration
├── src/
│   └── hello.py        # Python script that does the greeting
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
