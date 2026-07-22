# vsconf

cross platform provisioning for vs code. pure code, no ai.

## Cloning The Repository

Clone the repository and move into the project directory.

```
git clone https://github.com/redigere/vsconf.git
cd vsconf
```

## Creating The Virtual Environment

Create an isolated Python environment so that dependencies do not conflict with your system Python. This step also installs vsconf in editable mode along with all development tools (ruff, mypy, pytest).

```
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

On Windows the activation path differs slightly.

```
python -m venv .venv
.venv\Scripts\pip install -e ".[dev]"
```

## Running The CLI

All commands are invoked through the virtual environment. The full installation writes your vs code settings, keybindings, and snippets, installs the whitelisted extensions, and runs a security audit.

```
.venv/bin/vsconf install
```

You can also run individual steps instead of the full pipeline.

```
.venv/bin/vsconf settings      write settings only
.venv/bin/vsconf extensions    install extensions only
.venv/bin/vsconf security      run security audit
.venv/bin/vsconf list          list all whitelisted extensions
.venv/bin/vsconf status        show which extensions are installed
.venv/bin/vsconf runners       show runner shortcuts
.venv/bin/vsconf uninstall     remove non-whitelisted extensions
```

## What It Does

vsconf reads platform-specific configuration from `data/paths.json`, then writes your vs code settings, keybindings, and snippets from `config/linux/`, `config/macos/`, or `config/windows/`. Extensions are managed through JSON whitelists stored in `extensions/`. A security audit checks that the marketplace is blocked, telemetry is off, copilot is disabled, and agent features are off.

## Source Layout

`src/vsconf/` contains the Python package. `data/` holds JSON resources such as messages, paths, and shortcuts. `config/` stores platform settings, keybindings, and snippets. `extensions/` lists the extension whitelists by category. `tests/` runs the pytest suite.

## Continuous Integration

GitHub Actions runs linting (ruff, mypy), tests (pytest across three operating systems and four Python versions), and JSON validation on every push and pull request to main.

## License

GPL-3.0
