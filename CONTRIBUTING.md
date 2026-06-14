# Contributing to DWD UV Index Integration

> ⚠️ **Please Note:** This is a personal project that is not actively maintained. While contributions are appreciated, there is no guarantee of responses or merges. If you need an actively maintained fork, please feel free to create one!

First of all, thank you for considering contributing to the DWD UV Index integration! It's people like you that make this integration such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by the [Home Assistant Community Code of Conduct](https://github.com/home-assistant/core/blob/dev/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your Home Assistant version and Python version**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and what you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- End all files with a newline

## Development Setup

### Prerequisites

- Python 3.11 or later
- Home Assistant development environment (optional)

### Setting up your development environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/ian/dwd-hoas.git
   cd dwd-hoas
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Tests and Linting

- **Lint the code:**
  ```bash
  pylint dwd_uv_index
  ```

- **Check for syntax errors:**
  ```bash
  python -m py_compile dwd_uv_index/*.py
  ```

## Styleguides

### Python Styleguide

- Follow [PEP 8](https://pep8.org/)
- Use type hints where applicable
- Write docstrings for all functions and classes
- Use `from __future__ import annotations` at the top of files
- No trailing whitespace
- Maximum line length: 88 characters (Black formatter compatible)

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Documentation Styleguide

- Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
- Reference function names in backticks: `some_function()`
- Reference variable names in backticks: `some_variable`

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help organize and categorize issues and pull requests.

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed

## Resources

- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Home Assistant Architecture](https://developers.home-assistant.io/docs/architecture_index/)
- [Creating a Custom Integration](https://developers.home-assistant.io/docs/creating_component_index)

Thank you for contributing! 🎉
