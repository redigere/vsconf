# developing

## Creating The Virtual Environment

Start by creating an isolated Python environment. This keeps your system Python clean and ensures reproducible builds. Install vsconf in editable mode so that changes to the source code take effect immediately without reinstalling.

```
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

The `[dev]` extra pulls in ruff for linting and formatting, mypy for static type checking, and pytest for running the test suite.

## Running The CLI

Execute any vsconf command through the virtual environment binary. The most common workflow is the full installation, which writes settings, installs extensions, and runs the security audit in one step.

```
.venv/bin/vsconf install
```

For more granular control, run individual subcommands.

```
.venv/bin/vsconf settings
.venv/bin/vsconf extensions
.venv/bin/vsconf security
.venv/bin/vsconf list
.venv/bin/vsconf status
.venv/bin/vsconf runners
.venv/bin/vsconf uninstall
```

## Linting

Ruff checks for common errors, unused imports, and style issues. Mypy verifies type annotations are consistent across the codebase. Run both together to see the full picture.

```
.venv/bin/ruff check src/
.venv/bin/mypy src/
```

## Formatting

Ruff can auto-fix many of the issues it finds, and it can reformat your code to match the project style. Running both commands ensures that your code is both correct and consistently formatted.

```
.venv/bin/ruff check src/ --fix
.venv/bin/ruff format src/
```

## Testing

Pytest discovers and runs all tests in the `tests/` directory. The suite validates that data files load correctly, platform detection works, extensions are parsed properly, and configuration paths exist.

```
.venv/bin/pytest tests/ -v
```

## All Checks At Once

Chain linting, type checking, and testing into a single command to verify everything passes before committing. This is the same sequence that CI runs on every push.

```
.venv/bin/ruff check src/ && .venv/bin/mypy src/ && .venv/bin/pytest tests/ -v
```

## Cleaning Up

Remove the virtual environment and all cached files if you need a fresh start. This deletes `.venv/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, and `.ruff_cache/`.

```
rm -rf .venv __pycache__ .pytest_cache .mypy_cache .ruff_cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
```
