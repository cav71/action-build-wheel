# Hello World GitHub Action

A simple GitHub Action that greets someone and records the time. This action demonstrates how to create a basic composite action that runs a Python script.

## Features

- ✅ Greets a specified person or defaults to "World"
- ✅ Records the current time as an output
- ✅ Simple Python-based implementation
- ✅ Easy to integrate into your workflows

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
        uses: actions/checkout@v4

      - name: Run Hello World Action
        uses: ./
        id: hello
        with:
          who-to-greet: 'GitHub User'

      - name: Display greeting time
        run: echo "Greeted at ${{ steps.hello.outputs.time }}"
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
