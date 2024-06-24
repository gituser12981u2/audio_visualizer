## Contributing

Contribution to are welcome! Here's how you can help.

## Getting Started

1. Fork the repository.
2. Create a new branch(`git checkout -b feature-branch`).
3. Commit changes(`git commit -am 'Add new feature'`)
4. Push to the branch(`git push origin feature-branch`)..
5. Create a new Pull Request.

## Linting and Formatting

Before submitting a pull request, please ensure that any updates adhere to the project's style guidelines:

### Using Flake8 for Linting

- Run flake8 to check for linting issues:
```bash
flake8 audio_visualizer tests
```

- Run autopep8 to format the code to flake8 standards

```bash
autopep8 --in-place --aggressive --aggressive audio_visualizer tests
```
**Note**: that autopep8 doesn't work 100% so some manual formatting may be necessary

### Setting up Pre-Commit Hooks

One can also set up a pre-commit hook to automate these checks:

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Create a .pre-commit-config.yaml file with the following content:
```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-autopep8
    rev: v1.5.7
    hooks:
      - id: autopep8
        args: [--aggressive, --aggressive]

  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
```

3. Install the pre-commit hooks:
```bash
pre-commit install
```

This will ensure that autopep8 and flake8 run automatically before each commit.

## Testing and CI/CD Integration

Please ensure contributions pass the automated tests which can be run locally using the following command:

```bash
xvfb-run --auto-servernum python -m unittest discover tests
```

**Note**: xvfb is a linux program and can these tests must be passed on a linux distribution--though this project is for macOS and Windows too, linux is the only one tested due to audio loop back issues with the former.

The continuous integration (CI) process also includes linting with flake8, so check for linting issues before pushing

```bash
flake8 audio_visualizer tests
```

For more details on the CI/CD processes, ses the `.github/workflows/ci.yml` file

## Code Style and Documentation

The code must adhere to the Google style for docstring in this codebase. Please ensure that all public classes and functions include doctrings that follow this format:

```python
class ClassName:
    """
    Short description.

    Attributes:
        attribute1 (type): Description
        attribute2 (type): Description
        ...
    """
        
    def Method(args):
        """
            method_name: Description

            Args:
                arg1 (type): Description
                arg2 (type): Description
                ...

            Returns:
                return1 (type): description 
                return2 (type): description
        """
```

## Using the Issue and Feature Templates

For reporting bugs or requesting new features, please use the predefined templates, or use a custom one if your communication does not fit any template. This ensures that all necessary information is provided and helps to address issues and enhancements efficiently.

