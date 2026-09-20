# Simple Calculator

A simple calculator with a modern `tkinter` UI, managed as a [uv](https://docs.astral.sh/uv/) project.

## Project layout

```
simple-calculator/
├── pyproject.toml
├── .flake8
├── src/
│   └── calculator/
│       ├── __init__.py
│       ├── logic.py     # pure calculation logic (unit tested)
│       └── app.py       # tkinter UI
├── tests/
│   └── test_logic.py
└── .github/
    └── workflows/
        └── ci.yml
```

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it, then from the project root:

```bash
uv sync --group dev
```

This creates a virtual environment and installs the project plus dev dependencies (`pytest`, `flake8`). The project pins `requires-python = ">=3.10,<3.13"`, so `uv` will automatically pick (and download, if needed) a compatible Python — no manual steps needed.

> **Windows note:** Python 3.13.0 has a known bug ([cpython#125235](https://github.com/python/cpython/issues/125235)) where `tkinter` fails inside a virtual environment on Windows with `Can't find a usable init.tcl`. This project pins to `<3.13` to avoid it. If `uv` doesn't already have a 3.12 build, run `uv python install 3.12` first.

## Run the calculator

```bash
uv run calculator
```

or

```bash
uv run python -m calculator.app
```

## Run tests

```bash
uv run pytest
```

## Run linting

```bash
uv run flake8 .
```

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs linting and tests automatically on every push/PR to `main`, across Python 3.10–3.12, using `uv` for dependency management.
